#!/usr/bin/env python3
"""Register native Claude/Codex pair identities.

The pair registry lives in the user's shared home rather than in a task folder
or a provider call store. Provider transcripts remain owned by their native
``~/.claude`` and ``~/.codex`` homes. The default contract is only an identity
lookup: wrappers inject the pair name and both native session IDs before a run.

Legacy mailbox/hook code remains available only for explicit compatibility:

* a Stop hook appends a compact digest to the pair mailbox;
* a target configured for ``call`` receives that digest in a marked sync turn;
* a target configured for ``mailbox`` receives unread digests through its next
  UserPromptSubmit hook;
* marked sync turns never emit another pair event.
"""

from __future__ import annotations

import argparse
import contextlib
import fcntl
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterator

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from run_cli_agent import ROOT, _parse_claude, _parse_codex  # noqa: E402


PAIR_SCHEMA = "haipipe.native-pair/v2"
EVENT_SCHEMA = "haipipe.native-pair-event/v1"
SYNC_MARKER = "[HAIPIPE PAIR SYNC]"
PAIR_IGNORE = "PAIR_IGNORE"
PAIR_SYNC = "PAIR_SYNC"
DEFAULT_TEXT_LIMIT = 3600
CLAIM_TTL_SECONDS = 15 * 60


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _store_root() -> Path:
    configured = os.environ.get("HAIPIPE_PAIR_HOME")
    if configured:
        return Path(configured).expanduser().resolve()
    return Path.home() / ".config" / "haipipe" / "pairs"


def pair_slug(pair_name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", pair_name.lower()).strip("-")
    return slug or "pair"


def _resolved_cwd(cwd: Path | str | None) -> Path:
    return Path(cwd or ROOT).expanduser().resolve()


def _legacy_pair_file_for_name(pair_name: str) -> Path:
    return _store_root() / f"{pair_slug(pair_name)}.json"


def pair_file_for_name(pair_name: str, cwd: Path | str | None = None) -> Path:
    """Return a workspace-aware manifest path.

    The old slug-only path remains valid for backward compatibility.  Reuse it
    only when it already belongs to this exact workspace; otherwise new pairs
    receive a short workspace hash so two repositories can safely use the same
    human-readable pair name.
    """
    legacy = _legacy_pair_file_for_name(pair_name)
    if cwd is None:
        return legacy
    resolved = _resolved_cwd(cwd)
    existing = _read_json(legacy)
    if isinstance(existing, dict) and existing.get("cwd"):
        try:
            if Path(existing["cwd"]).expanduser().resolve() == resolved:
                return legacy
        except OSError:
            pass
    workspace_key = hashlib.sha256(str(resolved).encode("utf-8")).hexdigest()[:12]
    return _store_root() / f"{pair_slug(pair_name)}--{workspace_key}.json"


def _mailbox_path(manifest_path: Path) -> Path:
    return manifest_path.with_name(f"{manifest_path.stem}.mailbox.jsonl")


def _lock_path(manifest_path: Path) -> Path:
    return manifest_path.with_name(f"{manifest_path.stem}.lock")


def provider_lock_path(manifest_path: Path, provider: str) -> Path:
    return manifest_path.with_name(f"{manifest_path.stem}.{provider}.writer.lock")


def _ensure_private_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True, mode=0o700)
    try:
        path.chmod(0o700)
    except OSError:
        pass


def _make_private(path: Path) -> None:
    try:
        path.chmod(0o600)
    except OSError:
        pass


@contextlib.contextmanager
def provider_lock(manifest_path: Path, provider: str) -> Iterator[None]:
    _ensure_private_dir(manifest_path.parent)
    lock_path = provider_lock_path(manifest_path, provider)
    with lock_path.open("a+", encoding="utf-8") as handle:
        _make_private(lock_path)
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


@contextlib.contextmanager
def _locked(manifest_path: Path) -> Iterator[None]:
    _ensure_private_dir(manifest_path.parent)
    lock_path = _lock_path(manifest_path)
    with lock_path.open("a+", encoding="utf-8") as handle:
        _make_private(lock_path)
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def _read_json(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return default


def _atomic_write_json(path: Path, value: Any, *, private: bool = False) -> None:
    if private:
        _ensure_private_dir(path.parent)
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if private:
        _make_private(temporary)
    temporary.replace(path)
    if private:
        _make_private(path)


def _default_skills() -> list[str]:
    return [
        str(ROOT / "Tools/plugins/haipipe-toolkit/skills/0_utils/call-peer/SKILL.md"),
    ]


def register_pair(
    *,
    pair_name: str,
    cwd: Path,
    caller_provider: str,
    caller_session_id: str,
    callee_provider: str,
    callee_session_id: str,
    caller_transport: str = "native_cli",
    callee_transport: str = "native_cli",
    caller_delivery: str = "mailbox",
    callee_delivery: str = "mailbox",
    manifest_path: Path | None = None,
) -> Path:
    if caller_provider == callee_provider:
        raise ValueError("pair providers must be different")
    if not caller_session_id or not callee_session_id:
        raise ValueError("both provider session ids are required")
    path = (manifest_path or pair_file_for_name(pair_name, cwd)).expanduser().resolve()
    with _locked(path):
        existing = _read_json(path, {})
        manifest = existing if isinstance(existing, dict) else {}
        manifest.update(
            {
                "schema": PAIR_SCHEMA,
                "pair_name": pair_name,
                "cwd": str(cwd.expanduser().resolve()),
                "skills": _default_skills(),
                "updated_at": _now(),
            }
        )
        manifest.setdefault("created_at", _now())
        providers = manifest.setdefault("providers", {})
        providers[caller_provider] = {
            "session_id": caller_session_id,
            "transport": caller_transport,
            "delivery": caller_delivery,
            "home": "~/.claude" if caller_provider == "claude" else "~/.codex",
        }
        providers[callee_provider] = {
            "session_id": callee_session_id,
            "transport": callee_transport,
            "delivery": callee_delivery,
            "home": "~/.claude" if callee_provider == "claude" else "~/.codex",
        }
        sync = manifest.setdefault("sync", {})
        # Pair registration is identity-only by default. Mailbox delivery is
        # legacy compatibility and must be enabled deliberately.
        sync.setdefault("enabled", False)
        sync.setdefault("seen_event_ids", [])
        sync.setdefault("delivery_status", {})
        sync.setdefault("injected_event_ids", {})
        _atomic_write_json(path, manifest, private=True)
    return path


def _manifest_matches(
    manifest: dict[str, Any], provider: str, session_id: str, cwd: str | None
) -> bool:
    record = (manifest.get("providers") or {}).get(provider) or {}
    if record.get("session_id") != session_id:
        return False
    if cwd:
        if not manifest.get("cwd"):
            return False
        try:
            return Path(manifest["cwd"]).resolve() == Path(cwd).expanduser().resolve()
        except OSError:
            return False
    return True


def find_pair(
    *,
    provider: str,
    session_id: str,
    cwd: str | None = None,
    manifest_path: Path | None = None,
    pair_name: str | None = None,
) -> tuple[Path, dict[str, Any]] | None:
    candidates: list[Path] = []
    if manifest_path:
        candidates.append(manifest_path.expanduser().resolve())
    elif pair_name:
        candidates.append(pair_file_for_name(pair_name, cwd))
        legacy = _legacy_pair_file_for_name(pair_name)
        if legacy not in candidates:
            candidates.append(legacy)
    else:
        candidates.extend(
            sorted(_store_root().glob("*.json"), key=lambda item: item.stat().st_mtime, reverse=True)
        )
    for candidate in candidates:
        manifest = _read_json(candidate)
        if (
            not isinstance(manifest, dict)
            or pair_name
            and manifest.get("pair_name") != pair_name
            or not _manifest_matches(manifest, provider, session_id, cwd)
        ):
            continue
        return candidate, manifest
    return None


def _compact(value: Any, limit: int = DEFAULT_TEXT_LIMIT) -> str:
    text = str(value or "").replace("\x00", "").strip()
    text = re.sub(r"\n{3,}", "\n\n", text)
    if len(text) <= limit:
        return text
    first = max(1, limit // 2)
    last = max(1, limit - first - 40)
    return f"{text[:first]}\n… [truncated] …\n{text[-last:]}"


def _prompt_directive(text: str) -> tuple[str, bool, bool]:
    """Return (clean_text, force_sync, ignore) for an explicit leading marker."""
    raw = str(text or "").strip()
    match = re.match(
        r"^(?:\[(PAIR_IGNORE|PAIR_SYNC)\]|(PAIR_IGNORE|PAIR_SYNC))(?=\s|$)",
        raw,
        flags=re.IGNORECASE,
    )
    if not match:
        return raw, False, False
    directive = (match.group(1) or match.group(2)).upper()
    clean = raw[match.end() :].lstrip()
    return clean, directive == PAIR_SYNC, directive == PAIR_IGNORE


def _sync_enabled(manifest: dict[str, Any]) -> bool:
    # Identity-only pairing is the default, including older manifests that
    # predate the explicit ``sync.enabled`` field.
    return (manifest.get("sync") or {}).get("enabled", False) is True


def _content_text(content: Any) -> str:
    if isinstance(content, str):
        return content.strip()
    if not isinstance(content, list):
        return ""
    parts: list[str] = []
    for item in content:
        if isinstance(item, str):
            parts.append(item)
            continue
        if not isinstance(item, dict):
            continue
        if item.get("type") in {"tool_result", "thinking", "redacted_thinking"}:
            continue
        text = item.get("text")
        if isinstance(text, str):
            parts.append(text)
        elif isinstance(item.get("content"), str):
            parts.append(item["content"])
    return "\n".join(part.strip() for part in parts if part.strip()).strip()


def _is_sync_text(text: str) -> bool:
    return SYNC_MARKER in text or "[Native paired-session handshake]" in text


def _record_role_text(record: dict[str, Any]) -> tuple[str | None, str]:
    message = record.get("message") if isinstance(record.get("message"), dict) else None
    payload = record.get("payload") if isinstance(record.get("payload"), dict) else None
    candidates = [message, payload, record]
    for candidate in candidates:
        if not candidate:
            continue
        role = candidate.get("role")
        if role not in {"user", "assistant"}:
            kind = candidate.get("type")
            if kind in {"user_message", "user_prompt"}:
                role = "user"
            elif kind in {"agent_message", "assistant_message"}:
                role = "assistant"
        if role not in {"user", "assistant"}:
            continue
        text = _content_text(candidate.get("content"))
        if not text:
            for key in ("text", "message", "prompt"):
                value = candidate.get(key)
                if isinstance(value, str):
                    text = value.strip()
                    if text:
                        break
        if text:
            return role, text
    return None, ""


def _read_transcript_turn(
    transcript_path: str | None, provider: str, last_assistant_message: str = ""
) -> tuple[str, str, Any, Any]:
    fallback_assistant = _compact(last_assistant_message)
    if not transcript_path:
        return "", fallback_assistant, None, None

    def _read_snapshot() -> tuple[str, str, Any, Any, bool]:
        try:
            lines = Path(transcript_path).read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            return "", fallback_assistant, None, None, False
        user_text = ""
        last_user_text = ""
        last_user_was_sync = False
        assistant_text = fallback_assistant
        terminal_assistant_text = ""
        usage: Any = None
        cost_usd: Any = None
        for raw in lines:
            try:
                record = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if not isinstance(record, dict):
                continue
            role, text = _record_role_text(record)
            if role == "user" and text:
                last_user_text = text
                last_user_was_sync = _is_sync_text(text)
                if not last_user_was_sync:
                    user_text = text
            elif role == "assistant" and text:
                assistant_text = text
                message = record.get("message") if isinstance(record.get("message"), dict) else record
                if isinstance(message, dict):
                    usage = message.get("usage", usage)
                    cost_usd = message.get("total_cost_usd", message.get("cost_usd", cost_usd))
                stop_reason = record.get("stop_reason")
                if not stop_reason and isinstance(message, dict):
                    stop_reason = message.get("stop_reason")
                if stop_reason in {"end_turn", "stop_sequence"}:
                    terminal_assistant_text = text
            payload = record.get("payload") if isinstance(record.get("payload"), dict) else {}
            if provider == "codex" and record.get("type") == "event_msg":
                if payload.get("type") == "turn_completed":
                    usage = payload.get("usage", usage)
            if provider == "codex":
                cost_usd = record.get("total_cost_usd", record.get("cost_usd", cost_usd))
        if last_user_was_sync:
            user_text = ""
        elif last_user_text:
            user_text = last_user_text
        answer = terminal_assistant_text or assistant_text
        return _compact(user_text), _compact(answer), usage, cost_usd, bool(terminal_assistant_text)

    # Claude's Stop hook can run just before the provider flushes its final
    # assistant record. Retry briefly so the digest contains the terminal
    # answer rather than an intermediate progress message.
    snapshot = ("", fallback_assistant, None, None, False)
    for attempt in range(4):
        snapshot = _read_snapshot()
        if snapshot[4] or attempt == 3:
            break
        time.sleep(0.15 * (attempt + 1))
    return snapshot[:4]


def _event_id(pair_name: str, provider: str, session_id: str, turn_id: str | None, user: str, answer: str) -> str:
    seed = "\0".join((pair_name, provider, session_id, str(turn_id or ""), user, answer))
    return hashlib.sha256(seed.encode("utf-8")).hexdigest()


def _make_event(
    *,
    manifest: dict[str, Any],
    source_provider: str,
    source_session_id: str,
    turn_id: str | None,
    user_text: str,
    assistant_text: str,
    usage: Any = None,
    cost_usd: Any = None,
    force_sync: bool = False,
) -> dict[str, Any]:
    providers = manifest.get("providers") or {}
    target_provider = "claude" if source_provider == "codex" else "codex"
    event_id = _event_id(
        manifest["pair_name"], source_provider, source_session_id, turn_id, user_text, assistant_text
    )
    return {
        "schema": EVENT_SCHEMA,
        "event_id": event_id,
        "created_at": _now(),
        "pair_name": manifest["pair_name"],
        "cwd": manifest.get("cwd"),
        "turn_id": turn_id,
        "from": {"provider": source_provider, "session_id": source_session_id},
        "to": {
            "provider": target_provider,
            "session_id": (providers.get(target_provider) or {}).get("session_id"),
        },
        "user_summary": _compact(user_text),
        "answer_summary": _compact(assistant_text),
        "usage": usage,
        "cost_usd": cost_usd,
        "force_sync": force_sync,
    }


def _append_event(manifest_path: Path, event: dict[str, Any]) -> bool:
    with _locked(manifest_path):
        manifest = _read_json(manifest_path)
        if not isinstance(manifest, dict):
            raise FileNotFoundError(f"Pair manifest is missing or invalid: {manifest_path}")
        sync = manifest.setdefault("sync", {})
        if not _sync_enabled(manifest) and not event.get("force_sync"):
            return False
        seen = sync.setdefault("seen_event_ids", [])
        if event["event_id"] in seen:
            return False
        mailbox_path = _mailbox_path(manifest_path)
        with mailbox_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
        _make_private(mailbox_path)
        seen.append(event["event_id"])
        sync["seen_event_ids"] = seen[-200:]
        sync["last_event_id"] = event["event_id"]
        sync["last_event_at"] = event["created_at"]
        _atomic_write_json(manifest_path, manifest, private=True)
    return True


def _read_events(manifest_path: Path) -> list[dict[str, Any]]:
    path = _mailbox_path(manifest_path)
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return []
    events: list[dict[str, Any]] = []
    for line in lines:
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(event, dict) and event.get("schema") == EVENT_SCHEMA:
            events.append(event)
    return events


def _load_event(manifest_path: Path, event_id: str) -> dict[str, Any] | None:
    for event in reversed(_read_events(manifest_path)):
        if event.get("event_id") == event_id:
            return event
    return None


def _claim_delivery(manifest_path: Path, event_id: str) -> bool:
    event = _load_event(manifest_path, event_id)
    if not event:
        return False
    with _locked(manifest_path):
        manifest = _read_json(manifest_path)
        if not isinstance(manifest, dict):
            return False
        if not _sync_enabled(manifest) and not event.get("force_sync"):
            return False
        status = manifest.setdefault("sync", {}).setdefault("delivery_status", {})
        current = status.get(event_id)
        now = time.time()
        if isinstance(current, dict):
            if current.get("state") == "delivered":
                return False
            if current.get("state") == "claimed" and now - float(current.get("epoch", now)) < CLAIM_TTL_SECONDS:
                return False
        status[event_id] = {"state": "claimed", "epoch": now, "at": _now()}
        _atomic_write_json(manifest_path, manifest, private=True)
        return True


def _finish_delivery(manifest_path: Path, event_id: str, result: dict[str, Any]) -> None:
    with _locked(manifest_path):
        manifest = _read_json(manifest_path)
        if not isinstance(manifest, dict):
            return
        status = manifest.setdefault("sync", {}).setdefault("delivery_status", {})
        status[event_id] = {
            "state": "delivered" if result.get("status") == "ok" else "failed",
            "at": _now(),
            "session_id": result.get("session_id"),
            "model": result.get("resolved_model"),
            "usage": result.get("usage"),
            "cost_usd": result.get("cost_usd"),
            "error": result.get("error"),
        }
        status_keys = list(status)[-200:]
        manifest["sync"]["delivery_status"] = {key: status[key] for key in status_keys}
        manifest["sync"]["last_delivery"] = status[event_id]
        _atomic_write_json(manifest_path, manifest, private=True)


def _named_manifest(pair_name: str, cwd: Path | str | None) -> Path | None:
    candidates = [pair_file_for_name(pair_name, cwd), _legacy_pair_file_for_name(pair_name)]
    seen: set[Path] = set()
    for candidate in candidates:
        candidate = candidate.expanduser().resolve()
        if candidate in seen:
            continue
        seen.add(candidate)
        manifest = _read_json(candidate)
        if not isinstance(manifest, dict) or manifest.get("pair_name") != pair_name:
            continue
        if cwd:
            try:
                manifest_cwd = manifest.get("cwd")
                if not manifest_cwd or Path(manifest_cwd).expanduser().resolve() != _resolved_cwd(cwd):
                    continue
            except OSError:
                continue
        return candidate
    return None


def _resolve_manifest(
    *, manifest_path: Path | None, pair_name: str | None, cwd: Path | str | None
) -> Path:
    if manifest_path:
        return manifest_path.expanduser().resolve()
    if not pair_name:
        raise ValueError("provide --manifest or --pair-name")
    found = _named_manifest(pair_name, cwd)
    return found or pair_file_for_name(pair_name, cwd).expanduser().resolve()


def resolve_pair_session(
    *, pair_name: str, provider: str, cwd: Path | str | None = None
) -> tuple[Path, dict[str, Any], str]:
    """Resolve one provider's native session ID from a human pair name."""
    if provider not in {"claude", "codex"}:
        raise ValueError(f"unsupported provider: {provider}")
    manifest_path = _named_manifest(pair_name, cwd)
    if not manifest_path:
        raise FileNotFoundError(
            f"No pair named {pair_name!r} is registered for workspace {_resolved_cwd(cwd)}"
        )
    manifest = _read_json(manifest_path)
    record = (manifest.get("providers") or {}).get(provider) if isinstance(manifest, dict) else None
    session_id = record.get("session_id") if isinstance(record, dict) else None
    if not isinstance(session_id, str) or not session_id:
        raise ValueError(f"Pair {pair_name!r} has no {provider} session id")
    return manifest_path, manifest, session_id


def paired_session_context(
    *, manifest: dict[str, Any], self_provider: str, self_session_id: str
) -> str:
    """Render the identity-only context injected before a paired provider run."""
    providers = manifest.get("providers") or {}
    self_record = providers.get(self_provider) or {}
    partner_provider = "claude" if self_provider == "codex" else "codex"
    partner_record = providers.get(partner_provider) or {}
    return "\n".join(
        [
            "[HAIPIPE PAIRED SESSION CONTEXT]",
            "Identity context only; this is not a new task and does not request turn synchronization.",
            f"pair_name: {manifest.get('pair_name', '(unnamed)')}",
            f"working_directory: {manifest.get('cwd', '(unknown)')}",
            f"self_provider: {self_provider}",
            f"self_session_id: {self_session_id or self_record.get('session_id', '(unknown)')}",
            f"partner_provider: {partner_provider}",
            f"partner_session_id: {partner_record.get('session_id', '(not registered)')}",
            "Do not call the partner or copy its transcript unless the user explicitly asks.",
        ]
    )


def _status_payload(manifest_path: Path) -> dict[str, Any]:
    manifest = _read_json(manifest_path)
    if not isinstance(manifest, dict):
        raise FileNotFoundError(f"Pair manifest is missing or invalid: {manifest_path}")
    sync = manifest.get("sync") or {}
    status = sync.get("delivery_status") or {}
    events = _read_events(manifest_path)
    pending: dict[str, int] = {provider: 0 for provider in (manifest.get("providers") or {})}
    state_counts: dict[str, int] = {}
    for event in events:
        target_provider = (event.get("to") or {}).get("provider")
        if target_provider:
            event_state = (status.get(event.get("event_id")) or {}).get("state", "pending")
            if event_state != "delivered":
                pending[target_provider] = pending.get(target_provider, 0) + 1
            state_counts[event_state] = state_counts.get(event_state, 0) + 1
    providers = {}
    for provider, record in (manifest.get("providers") or {}).items():
        if not isinstance(record, dict):
            continue
        providers[provider] = {
            "session_id": record.get("session_id"),
            "delivery": record.get("delivery"),
            "transport": record.get("transport"),
        }
    return {
        "schema": PAIR_SCHEMA,
        "manifest": str(manifest_path),
        "pair_name": manifest.get("pair_name"),
        "cwd": manifest.get("cwd"),
        "sync_enabled": _sync_enabled(manifest),
        "providers": providers,
        "event_count": len(events),
        "pending_by_provider": pending,
        "delivery_state_counts": state_counts,
        "last_event": {
            "event_id": sync.get("last_event_id"),
            "created_at": sync.get("last_event_at"),
        },
        "last_delivery": sync.get("last_delivery"),
    }


def _set_enabled(manifest_path: Path, enabled: bool) -> dict[str, Any]:
    with _locked(manifest_path):
        manifest = _read_json(manifest_path)
        if not isinstance(manifest, dict):
            raise FileNotFoundError(f"Pair manifest is missing or invalid: {manifest_path}")
        sync = manifest.setdefault("sync", {})
        sync["enabled"] = enabled
        manifest["updated_at"] = _now()
        _atomic_write_json(manifest_path, manifest, private=True)
    return _status_payload(manifest_path)


def _sync_prompt(event: dict[str, Any]) -> str:
    source = event["from"]["provider"]
    return "\n".join(
        [
            SYNC_MARKER,
            f"pair_name: {event['pair_name']}",
            f"event_id: {event['event_id']}",
            f"source_provider: {source}",
            f"source_session_id: {event['from']['session_id']}",
            "This is context synchronization, not a new user task.",
            "Do not modify files, call the other provider, or emit another pair-sync event.",
            "Absorb the digest and reply with a short SYNC_ACK containing the key decisions and next step.",
            "",
            "User request in the source session:",
            event.get("user_summary", "(not available)"),
            "",
            "Source session answer:",
            event.get("answer_summary", "(not available)"),
        ]
    )


def _target_command(provider: str, session_id: str, pair_name: str) -> list[str]:
    if provider == "claude":
        return [
            "claude",
            "-p",
            "--output-format",
            "json",
            "--resume",
            session_id,
            "--name",
            pair_name,
        ]
    return ["codex", "exec", "--json", "resume", session_id, "-"]


def _deliver(manifest_path: Path, event_id: str, timeout: float = 300) -> int:
    event = _load_event(manifest_path, event_id)
    if not event:
        print(f"Pair event not found: {event_id}", file=sys.stderr)
        return 2
    if not _claim_delivery(manifest_path, event_id):
        return 0
    target_provider = event["to"]["provider"]
    target_session_id = event["to"].get("session_id")
    if not target_session_id:
        result = {"status": "failed", "error": "target session id is missing"}
        _finish_delivery(manifest_path, event_id, result)
        print(result["error"], file=sys.stderr)
        return 2
    command = _target_command(target_provider, target_session_id, event["pair_name"])
    env = dict(os.environ)
    env.update(
        {
            "HAIPIPE_PAIR_SYNC": "1",
            "HAIPIPE_PAIR_EVENT_ID": event_id,
            "HAIPIPE_PAIR_NAME": event["pair_name"],
            "HAIPIPE_PAIR_CALLER_PROVIDER": event["from"]["provider"],
            "HAIPIPE_PAIR_CALLER_SESSION_ID": event["from"]["session_id"],
        }
    )
    cwd = Path(event.get("cwd") or ROOT).expanduser().resolve()
    try:
        with provider_lock(manifest_path, target_provider):
            completed = subprocess.run(
                command,
                input=_sync_prompt(event) + "\n",
                text=True,
                capture_output=True,
                cwd=str(cwd),
                env=env,
                check=False,
                timeout=timeout,
            )
    except (OSError, subprocess.TimeoutExpired) as error:
        result = {"status": "failed", "error": str(error)}
        _finish_delivery(manifest_path, event_id, result)
        print(f"Pair sync failed: {error}", file=sys.stderr)
        return 124 if isinstance(error, subprocess.TimeoutExpired) else 127
    result = (
        _parse_claude(completed.stdout, completed.returncode)
        if target_provider == "claude"
        else _parse_codex(completed.stdout, completed.returncode, target_session_id)
    )
    _finish_delivery(manifest_path, event_id, result)
    if result.get("status") != "ok":
        print(f"Pair sync failed: {result.get('error') or 'incomplete provider output'}", file=sys.stderr)
        if completed.stderr.strip():
            print(completed.stderr.rstrip(), file=sys.stderr)
        return completed.returncode or 3
    return 0


def _pending_context(manifest_path: Path, provider: str, session_id: str) -> str:
    with _locked(manifest_path):
        manifest = _read_json(manifest_path)
        if not isinstance(manifest, dict):
            return ""
        sync = manifest.setdefault("sync", {})
        enabled = _sync_enabled(manifest)
        status = sync.setdefault("delivery_status", {})
        injected = sync.setdefault("injected_event_ids", {})
        pending: list[dict[str, Any]] = []
        for event in _read_events(manifest_path):
            if (event.get("to") or {}).get("provider") != provider:
                continue
            if (event.get("to") or {}).get("session_id") != session_id:
                continue
            if not enabled and not event.get("force_sync"):
                continue
            event_id = event.get("event_id")
            if not event_id or status.get(event_id, {}).get("state") == "delivered":
                continue
            if event_id in injected:
                continue
            pending.append(event)
        if not pending:
            return ""
        pending = pending[-10:]
        for event in pending:
            injected[event["event_id"]] = {"session_id": session_id, "at": _now()}
        injected_keys = list(injected)[-200:]
        sync["injected_event_ids"] = {key: injected[key] for key in injected_keys}
        _atomic_write_json(manifest_path, manifest, private=True)
    blocks = [
        "[HAIPIPE PAIR CONTEXT]",
        "The following completed turn digest(s) came from the paired session.",
        "Treat them as context already handled; do not call the other provider just because you saw this block.",
    ]
    for event in pending:
        blocks.extend(
            [
                "",
                f"event_id: {event['event_id']}",
                f"from: {event['from']['provider']} ({event['from']['session_id']})",
                "User request:",
                event.get("user_summary", "(not available)"),
                "Source answer:",
                event.get("answer_summary", "(not available)"),
            ]
        )
    return "\n".join(blocks)


def _hook_payload() -> dict[str, Any]:
    raw = sys.stdin.read().strip()
    if not raw:
        return {}
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def _session_id_from_payload(payload: dict[str, Any]) -> str:
    value = payload.get("session_id")
    if isinstance(value, str) and value.strip():
        return value.strip()
    transcript = payload.get("transcript_path")
    if isinstance(transcript, str):
        match = re.search(r"([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})", transcript, re.I)
        if match:
            return match.group(1)
    return ""


def _hook_stop(provider: str, payload: dict[str, Any]) -> int:
    if os.environ.get("HAIPIPE_PAIR_SYNC") == "1" or os.environ.get("HAIPIPE_PAIR_WRAPPER") == "1":
        return 0
    if payload.get("stop_hook_active") is True:
        return 0
    event_name = payload.get("hook_event_name")
    if event_name and event_name != "Stop":
        return 0
    session_id = _session_id_from_payload(payload)
    if not session_id:
        return 0
    match = find_pair(provider=provider, session_id=session_id, cwd=payload.get("cwd"))
    if not match:
        return 0
    manifest_path, manifest = match
    user_text, assistant_text, usage, cost_usd = _read_transcript_turn(
        payload.get("transcript_path"), provider, payload.get("last_assistant_message", "")
    )
    if not user_text or not assistant_text or _is_sync_text(user_text):
        return 0
    record_turn(
        manifest_path=manifest_path,
        manifest=manifest,
        source_provider=provider,
        source_session_id=session_id,
        turn_id=payload.get("turn_id"),
        user_text=user_text,
        assistant_text=assistant_text,
        usage=payload.get("usage", usage),
        cost_usd=payload.get("cost_usd", cost_usd),
    )
    return 0


def record_turn(
    *,
    manifest_path: Path,
    manifest: dict[str, Any],
    source_provider: str,
    source_session_id: str,
    turn_id: str | None,
    user_text: str,
    assistant_text: str,
    usage: Any = None,
    cost_usd: Any = None,
) -> dict[str, Any] | None:
    """Append one completed turn and schedule configured delivery."""
    clean_user_text, force_sync, ignore = _prompt_directive(user_text)
    if ignore or not clean_user_text or not assistant_text or _is_sync_text(clean_user_text):
        return None
    event = _make_event(
        manifest=manifest,
        source_provider=source_provider,
        source_session_id=source_session_id,
        turn_id=turn_id,
        user_text=clean_user_text,
        assistant_text=assistant_text,
        usage=usage,
        cost_usd=cost_usd,
        force_sync=force_sync,
    )
    if not _append_event(manifest_path, event):
        return None
    target = (manifest.get("providers") or {}).get(event["to"]["provider"]) or {}
    if target.get("delivery") == "call" and target.get("session_id"):
        log_path = manifest_path.with_suffix(".sync.log")
        command = [
            sys.executable,
            str(Path(__file__).resolve()),
            "deliver",
            "--manifest",
            str(manifest_path),
            "--event-id",
            event["event_id"],
        ]
        with log_path.open("a", encoding="utf-8") as log:
            _make_private(log_path)
            subprocess.Popen(
                command,
                cwd=manifest.get("cwd") or str(ROOT),
                env=dict(os.environ),
                stdin=subprocess.DEVNULL,
                stdout=log,
                stderr=log,
                start_new_session=True,
            )
    return event


def _hook_prompt(provider: str, payload: dict[str, Any]) -> int:
    if os.environ.get("HAIPIPE_PAIR_SYNC") == "1":
        return 0
    session_id = _session_id_from_payload(payload)
    if not session_id:
        return 0
    match = find_pair(provider=provider, session_id=session_id, cwd=payload.get("cwd"))
    if not match:
        return 0
    manifest_path, _manifest = match
    context = _pending_context(manifest_path, provider, session_id)
    if not context:
        return 0
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "UserPromptSubmit",
                    "additionalContext": context,
                }
            },
            ensure_ascii=False,
        )
    )
    return 0


def _hook_entry(command: str) -> dict[str, Any]:
    return {"hooks": [{"type": "command", "command": command, "timeout": 30}]}


def _hook_python() -> str:
    virtualenv_python = ROOT / ".venv" / "bin" / "python"
    return str(virtualenv_python if virtualenv_python.is_file() else Path(sys.executable))


def _install_one_hook(path: Path, provider: str, dry_run: bool) -> None:
    existing = _read_json(path, {})
    if not isinstance(existing, dict):
        raise ValueError(f"Hook config is not a JSON object: {path}")
    hooks = existing.setdefault("hooks", {})
    script = str(Path(__file__).resolve())
    for event, event_name in (("Stop", "stop"), ("UserPromptSubmit", "prompt")):
        command = f'"{_hook_python()}" "{script}" hook --provider {provider} --event {event_name}'
        entries = hooks.setdefault(event, [])
        if not isinstance(entries, list):
            raise ValueError(f"Hook entry is not a list: {path}:{event}")
        already_present = any(
            isinstance(group, dict)
            and any(
                isinstance(item, dict) and item.get("command") == command
                for item in (group.get("hooks") or [])
            )
            for group in entries
        )
        if not already_present:
            entries.append(_hook_entry(command))
    if not dry_run:
        _atomic_write_json(path, existing)


def _install_hooks(args: argparse.Namespace) -> int:
    claude_path = args.claude_settings.expanduser().resolve()
    codex_path = args.codex_hooks.expanduser().resolve()
    _install_one_hook(claude_path, "claude", args.dry_run)
    _install_one_hook(codex_path, "codex", args.dry_run)
    print(json.dumps({"claude_settings": str(claude_path), "codex_hooks": str(codex_path), "dry_run": args.dry_run}))
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Maintain and synchronize native Claude/Codex pairs")
    subparsers = parser.add_subparsers(dest="command", required=True)

    register = subparsers.add_parser("register")
    register.add_argument("--pair-name", required=True)
    register.add_argument("--cwd", type=Path, default=ROOT)
    register.add_argument("--caller-provider", choices=("claude", "codex"), required=True)
    register.add_argument("--caller-session-id", required=True)
    register.add_argument("--callee-provider", choices=("claude", "codex"), required=True)
    register.add_argument("--callee-session-id", required=True)
    register.add_argument("--caller-transport", default="native_cli")
    register.add_argument("--callee-transport", default="native_cli")
    register.add_argument("--caller-delivery", choices=("call", "mailbox"), default="mailbox")
    register.add_argument("--callee-delivery", choices=("call", "mailbox"), default="mailbox")
    register.add_argument("--manifest", type=Path)

    deliver = subparsers.add_parser("deliver")
    deliver.add_argument("--manifest", type=Path, required=True)
    deliver.add_argument("--event-id", required=True)
    deliver.add_argument("--timeout", type=float, default=300)

    hook = subparsers.add_parser("hook")
    hook.add_argument("--provider", choices=("claude", "codex"), required=True)
    hook.add_argument("--event", choices=("stop", "prompt"), required=True)

    install = subparsers.add_parser("install-hooks")
    install.add_argument(
        "--claude-settings",
        type=Path,
        default=Path.home() / ".claude" / "settings.json",
    )
    install.add_argument(
        "--codex-hooks",
        type=Path,
        default=Path.home() / ".codex" / "hooks.json",
    )
    install.add_argument("--dry-run", action="store_true")

    status = subparsers.add_parser("status", help="Show pair identity, sync state, and pending digests")
    status_target = status.add_mutually_exclusive_group(required=True)
    status_target.add_argument("--manifest", type=Path)
    status_target.add_argument("--pair-name")
    status.add_argument("--cwd", type=Path, default=ROOT)

    enabled = subparsers.add_parser("set-enabled", help="Pause or resume automatic pair synchronization")
    enabled_target = enabled.add_mutually_exclusive_group(required=True)
    enabled_target.add_argument("--manifest", type=Path)
    enabled_target.add_argument("--pair-name")
    enabled.add_argument("--cwd", type=Path, default=ROOT)
    enabled_value = enabled.add_mutually_exclusive_group(required=True)
    enabled_value.add_argument("--enabled", action="store_true")
    enabled_value.add_argument("--disabled", action="store_true")

    return parser


def main() -> int:
    args = _parser().parse_args()
    if args.command == "register":
        path = register_pair(
            pair_name=args.pair_name.strip(),
            cwd=args.cwd,
            caller_provider=args.caller_provider,
            caller_session_id=args.caller_session_id,
            callee_provider=args.callee_provider,
            callee_session_id=args.callee_session_id,
            caller_transport=args.caller_transport,
            callee_transport=args.callee_transport,
            caller_delivery=args.caller_delivery,
            callee_delivery=args.callee_delivery,
            manifest_path=args.manifest,
        )
        print(path)
        return 0
    if args.command == "deliver":
        return _deliver(args.manifest.expanduser().resolve(), args.event_id, args.timeout)
    if args.command == "install-hooks":
        return _install_hooks(args)
    if args.command == "status":
        path = _resolve_manifest(
            manifest_path=args.manifest,
            pair_name=args.pair_name,
            cwd=args.cwd,
        )
        print(json.dumps(_status_payload(path), ensure_ascii=False, sort_keys=True))
        return 0
    if args.command == "set-enabled":
        path = _resolve_manifest(
            manifest_path=args.manifest,
            pair_name=args.pair_name,
            cwd=args.cwd,
        )
        result = _set_enabled(path, args.enabled)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    payload = _hook_payload()
    return _hook_stop(args.provider, payload) if args.event == "stop" else _hook_prompt(args.provider, payload)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"{type(error).__name__}: {error}", file=sys.stderr)
        raise SystemExit(2)
