#!/usr/bin/env python3
"""Call the native Claude or Codex CLI and keep a durable delegation receipt.

It keeps the provider's normal CLI configuration, model selection, skills,
tools, and permission behavior. This mode is for an explicitly requested
native CLI handoff, not for unattended least-privilege execution.

The wrapper borrows the useful contract from cc-skill-codex:

* parse structured provider output rather than scraping terminal text;
* return the final answer, an explicit provider session id, and receipt path;
* persist the complete envelope/event stream and stderr;
* resume by an explicit session id, never by ``--last`` or ``--continue``.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
import re
import shlex
import stat
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def _repo_root() -> Path:
    here = Path(__file__).resolve()
    for candidate in (Path.cwd(), *here.parents):
        if (candidate / "pyproject.toml").is_file() and (candidate / "code").is_dir():
            return candidate.resolve()
    raise RuntimeError("Could not find the Physician-SPACE repository root")


ROOT = _repo_root()
SCHEMA = "haipipe.agent-cli-receipt/v1"


def _claude_session_file(
    session_id: str,
    cwd: Path,
    config_dir: Path | None,
) -> Path | None:
    """Locate one Claude native transcript without using its display name."""
    configured = config_dir or os.environ.get("CLAUDE_CONFIG_DIR")
    home = Path(configured).expanduser() if configured else Path.home() / ".claude"
    projects = home / "projects"
    if not projects.is_dir():
        return None
    encoded_cwd = str(cwd).replace("/", "-")
    direct = projects / encoded_cwd / f"{session_id}.jsonl"
    if direct.is_file():
        return direct
    matches = sorted(projects.glob(f"*/{session_id}.jsonl"))
    return matches[0] if len(matches) == 1 else None


def _normalize_claude_resume_entrypoint(
    session_id: str,
    cwd: Path,
    config_dir: Path | None,
) -> Path | None:
    """Make a print-mode Claude transcript discoverable by native /resume.

    Claude's normal CLI can persist the first entrypoint as ``sdk-cli`` when
    launched in print mode. The resume picker excludes that marker. Change
    only the first entrypoint metadata field; leave the session id and all
    conversation content untouched.
    """
    path = _claude_session_file(session_id, cwd, config_dir)
    if path is None:
        return None
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    for index, line in enumerate(lines):
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(record, dict) or "entrypoint" not in record:
            continue
        if record.get("entrypoint") != "sdk-cli":
            return None
        updated = re.sub(
            r'("entrypoint"\s*:\s*)"sdk-cli"',
            r'\1"cli"',
            line,
            count=1,
        )
        if updated == line:
            record["entrypoint"] = "cli"
            newline = "\n" if line.endswith("\n") else ""
            updated = json.dumps(record, ensure_ascii=False, separators=(",", ":")) + newline
        lines[index] = updated
        temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
        try:
            temporary.write_text("".join(lines), encoding="utf-8")
            os.chmod(temporary, stat.S_IMODE(path.stat().st_mode))
            os.replace(temporary, path)
        finally:
            if temporary.exists():
                temporary.unlink()
        return path
    return None


def _jsonable(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return str(value)


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _write_json(path: Path, value: Any) -> None:
    _write_text(path, json.dumps(_jsonable(value), indent=2, ensure_ascii=False, sort_keys=True) + "\n")


def _read_prompt(args: argparse.Namespace) -> str:
    if args.prompt is not None and args.prompt_file is not None:
        raise ValueError("Use only one of --prompt or --prompt-file")
    if args.prompt is not None:
        prompt = args.prompt
    elif args.prompt_file is not None:
        prompt = args.prompt_file.read_text(encoding="utf-8")
    else:
        if sys.stdin.isatty():
            raise ValueError("Provide --prompt, --prompt-file, or a prompt on stdin")
        prompt = sys.stdin.read()
    prompt = prompt.strip()
    if not prompt:
        raise ValueError("The delegated prompt is empty")
    return prompt


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Call the native Claude or Codex CLI with a persistent receipt."
    )
    parser.add_argument("--provider", choices=("claude", "codex"), required=True)
    prompt = parser.add_mutually_exclusive_group()
    prompt.add_argument("--prompt")
    prompt.add_argument("--prompt-file", type=Path)
    session = parser.add_mutually_exclusive_group()
    session.add_argument("--session-id", "--resume-session", dest="session_id")
    session.add_argument(
        "--pair-name",
        help="Resume the provider session registered under this pair name in the current workspace",
    )
    parser.add_argument(
        "--sync-pair",
        action="store_true",
        help="Legacy opt-in: append this turn to the pair mailbox after success",
    )
    parser.add_argument("--model", help="Optional explicit native CLI model override")
    parser.add_argument(
        "--cli-arg",
        action="append",
        default=[],
        help="One extra argument passed to the native CLI; repeat as needed",
    )
    parser.add_argument("--config-dir", type=Path, help="Optional shared native home")
    parser.add_argument("--cwd", type=Path, default=ROOT, help="Native CLI working directory")
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true", help="Resolve the command without calling a provider")
    return parser


def _native_env(provider: str, config_dir: Path | None) -> dict[str, str]:
    environment = dict(os.environ)
    if config_dir is None:
        return environment
    if provider == "claude":
        environment["CLAUDE_CONFIG_DIR"] = str(config_dir)
    else:
        environment["CODEX_HOME"] = str(config_dir)
        environment["CODEX_SQLITE_HOME"] = str(config_dir / "sqlite")
    return environment


def _record_pair_turn(args: argparse.Namespace, prompt: str, result: dict[str, Any], cwd: Path) -> None:
    if os.environ.get("HAIPIPE_PAIR_SYNC") == "1":
        return
    session_id = result.get("session_id") or args.session_id
    response = result.get("response") or ""
    if not session_id or not response:
        return
    try:
        from pair_sync import find_pair, record_turn

        match = find_pair(provider=args.provider, session_id=session_id, cwd=str(cwd))
        if not match:
            return
        manifest_path, manifest = match
        record_turn(
            manifest_path=manifest_path,
            manifest=manifest,
            source_provider=args.provider,
            source_session_id=session_id,
            turn_id=None,
            user_text=prompt,
            assistant_text=response,
            usage=result.get("usage"),
            cost_usd=result.get("cost_usd"),
        )
    except Exception as error:  # Pair sync must never turn a provider success into a failure.
        print(f"Pair sync hook skipped: {error}", file=sys.stderr)


def _command(args: argparse.Namespace) -> list[str]:
    if args.provider == "claude":
        command = ["claude", "-p", "--output-format", "json"]
        if args.session_id:
            command += ["--resume", args.session_id]
        if args.pair_name:
            command += ["--name", args.pair_name]
        if args.model:
            command += ["--model", args.model]
        command += args.cli_arg
        return command

    # Codex's resume subcommand must come after its exec-level options.  This
    # also keeps options such as -s/-m before ``resume``, matching the native
    # CLI's parsing rules.
    command = ["codex", "exec", "--json"]
    if args.model:
        command += ["--model", args.model]
    command += args.cli_arg
    if args.session_id:
        command += ["resume", args.session_id, "-"]
    else:
        command += ["-"]
    return command


def _display_command(command: list[str]) -> str:
    return shlex.join(command)


def _base_receipt(
    args: argparse.Namespace,
    prompt: str,
    command: list[str],
    config_dir: Path | None,
    cwd: Path,
    out_dir: Path,
) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "created_at": datetime.now(UTC).isoformat(),
        "status": "started",
        "provider": args.provider,
        "transport": "native_cli",
        "profile": "lite",
        "command": _display_command(command),
        "requested_model": args.model,
        "session_id": args.session_id,
        "pair_name": args.pair_name,
        "sync_pair": args.sync_pair,
        "config_dir": str(config_dir) if config_dir else None,
        "working_directory": str(cwd),
        "receipt_dir": str(out_dir),
        "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        "permission_note": (
            "Native CLI mode intentionally inherits the provider CLI's configured "
            "skills, tools, model, approvals, and network permissions."
        ),
    }


def _parse_claude(stdout: str, returncode: int) -> dict[str, Any]:
    try:
        envelope = json.loads(stdout)
    except json.JSONDecodeError as error:
        return {
            "status": "malformed_output",
            "session_id": None,
            "response": "",
            "envelope": None,
            "usage": None,
            "cost_usd": None,
            "resolved_model": None,
            "error": f"Claude JSON envelope could not be parsed: {error}",
            "returncode": returncode,
        }
    provider_error = bool(envelope.get("is_error")) or returncode != 0
    response = envelope.get("result")
    session_id = envelope.get("session_id")
    if provider_error:
        status = "provider_error"
    elif not isinstance(response, str) or not response.strip() or not isinstance(session_id, str) or not session_id:
        status = "incomplete_output"
    else:
        status = "ok"
    return {
        "status": status,
        "session_id": session_id if status == "ok" else None,
        "response": response if isinstance(response, str) else "",
        "envelope": envelope,
        "usage": envelope.get("usage"),
        "cost_usd": envelope.get("total_cost_usd"),
        "resolved_model": envelope.get("model"),
        "error": (response if provider_error and isinstance(response, str) else None),
        "returncode": returncode,
    }


def _parse_codex(
    stdout: str,
    returncode: int,
    fallback_session_id: str | None = None,
) -> dict[str, Any]:
    events: list[dict[str, Any]] = []
    parse_errors: list[str] = []
    session_id: str | None = None
    response: str | None = None
    usage: Any = None
    resolved_model: str | None = None
    for line_number, line in enumerate(stdout.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as error:
            parse_errors.append(f"line {line_number}: {error}")
            continue
        if not isinstance(event, dict):
            parse_errors.append(f"line {line_number}: event is not an object")
            continue
        events.append(event)
        if event.get("type") == "thread.started":
            value = event.get("thread_id")
            if isinstance(value, str) and value:
                session_id = value
        if event.get("type") == "turn.completed":
            usage = event.get("usage", usage)
        if event.get("type") == "item.completed":
            item = event.get("item") or {}
            if isinstance(item, dict):
                if item.get("type") == "agent_message" and isinstance(item.get("text"), str):
                    response = item["text"]
                resolved_model = item.get("model", resolved_model)
        resolved_model = event.get("model", resolved_model)
    if not session_id and fallback_session_id and response:
        # ``codex exec resume`` may return the answer without repeating a
        # thread.started event.  The explicit resume id is authoritative.
        session_id = fallback_session_id
    provider_error = returncode != 0
    if provider_error:
        status = "provider_error"
    elif parse_errors or not events:
        status = "malformed_output"
    elif not response or not response.strip() or not session_id:
        status = "incomplete_output"
    else:
        status = "ok"
    return {
        "status": status,
        "session_id": session_id if status == "ok" else None,
        "response": response or "",
        "events": events,
        "usage": usage,
        "cost_usd": None,
        "resolved_model": resolved_model,
        "error": "; ".join(parse_errors) if parse_errors else None,
        "returncode": returncode,
    }


def _write_receipt(
    out_dir: Path,
    base: dict[str, Any],
    result: dict[str, Any],
    stderr: str,
    duration_ms: int,
) -> dict[str, Any]:
    if base["provider"] == "claude":
        _write_json(out_dir / "envelope.json", result.get("envelope"))
    else:
        with (out_dir / "events.jsonl").open("w", encoding="utf-8") as handle:
            for event in result.get("events", []):
                handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
    _write_text(out_dir / "stderr.log", stderr)
    _write_text(out_dir / "response.md", (result.get("response") or "").rstrip() + "\n")
    receipt = {
        **base,
        "status": result["status"],
        "session_id": result.get("session_id"),
        "resolved_model": result.get("resolved_model"),
        "usage": result.get("usage"),
        "cost_usd": result.get("cost_usd"),
        "resume_entrypoint": result.get("resume_entrypoint"),
        "session_transcript": result.get("session_transcript"),
        "returncode": result.get("returncode"),
        "duration_ms": duration_ms,
        "error": result.get("error"),
        "stderr_present": bool(stderr.strip()),
    }
    _write_json(out_dir / "usage_receipt.json", receipt)
    lines = ["# Native CLI receipt", ""]
    lines.extend(f"- {key}: `{value}`" for key, value in receipt.items())
    _write_text(out_dir / "receipt.md", "\n".join(lines) + "\n")
    return receipt


def main() -> int:
    args = _parser().parse_args()
    prompt = _read_prompt(args)
    config_dir = args.config_dir.expanduser().resolve() if args.config_dir else None
    cwd = args.cwd.expanduser().resolve()
    out_dir = args.out_dir.expanduser().resolve()
    if not cwd.is_dir():
        raise NotADirectoryError(f"Working directory does not exist: {cwd}")
    pair_manifest: dict[str, Any] | None = None
    if args.pair_name:
        try:
            from pair_sync import resolve_pair_session

            _manifest_path, pair_manifest, args.session_id = resolve_pair_session(
                pair_name=args.pair_name,
                provider=args.provider,
                cwd=cwd,
            )
        except Exception as error:
            raise ValueError(f"Could not resolve --pair-name {args.pair_name!r}: {error}") from error
    provider_prompt = prompt
    if pair_manifest is not None:
        from pair_sync import paired_session_context

        provider_prompt = (
            paired_session_context(
                manifest=pair_manifest,
                self_provider=args.provider,
                self_session_id=args.session_id or "",
            )
            + "\n\n[User task]\n"
            + prompt
        )
    if out_dir.exists() and any(out_dir.iterdir()):
        raise FileExistsError(f"Refusing to overwrite a non-empty receipt directory: {out_dir}")
    out_dir.mkdir(parents=True, exist_ok=True)
    command = _command(args)
    base = _base_receipt(args, provider_prompt, command, config_dir, cwd, out_dir)
    _write_text(out_dir / "prompt.md", provider_prompt + "\n")
    _write_json(out_dir / "request.json", base)
    if args.dry_run:
        base["status"] = "dry_run"
        _write_json(out_dir / "usage_receipt.json", base)
        print(json.dumps({"status": "dry_run", "command": command, "cwd": str(cwd), "receipt_dir": str(out_dir)}))
        return 0

    started = time.monotonic()
    child_env = _native_env(args.provider, config_dir)
    child_env["HAIPIPE_PAIR_WRAPPER"] = "1"
    pair_lock = contextlib.nullcontext()
    if args.session_id and os.environ.get("HAIPIPE_PAIR_SYNC") != "1":
        try:
            from pair_sync import find_pair, provider_lock

            match = find_pair(provider=args.provider, session_id=args.session_id, cwd=str(cwd))
            if match:
                pair_lock = provider_lock(match[0], args.provider)
        except Exception as error:
            print(f"Pair writer lock unavailable: {error}", file=sys.stderr)
    try:
        with pair_lock:
            completed = subprocess.run(
                command,
                input=provider_prompt + "\n",
                text=True,
                capture_output=True,
                cwd=str(cwd),
                env=child_env,
                check=False,
            )
    except OSError as error:
        result = {
            "status": "launcher_error",
            "session_id": None,
            "response": "",
            "usage": None,
            "cost_usd": None,
            "resolved_model": None,
            "error": str(error),
            "returncode": 127,
            "envelope": None,
            "events": [],
        }
        receipt = _write_receipt(out_dir, base, result, "", round((time.monotonic() - started) * 1000))
        print(f"DETAILS={out_dir}")
        print(f"Native CLI could not start: {error}", file=sys.stderr)
        return int(receipt["returncode"])

    result = (
        _parse_claude(completed.stdout, completed.returncode)
        if args.provider == "claude"
        else _parse_codex(completed.stdout, completed.returncode, args.session_id)
    )
    if args.provider == "claude" and result.get("status") == "ok":
        normalized = _normalize_claude_resume_entrypoint(
            result["session_id"],
            cwd,
            config_dir,
        )
        if normalized is not None:
            result["resume_entrypoint"] = "cli"
            result["session_transcript"] = str(normalized)
    duration_ms = round((time.monotonic() - started) * 1000)
    receipt = _write_receipt(out_dir, base, result, completed.stderr, duration_ms)
    if receipt["status"] == "ok":
        if args.sync_pair:
            _record_pair_turn(args, prompt, result, cwd)
        print(result["response"].rstrip())
        print()
        print(f"SESSION_ID={receipt['session_id']}")
    else:
        message = result.get("error") or "Native CLI did not return a complete delegated response"
        print(f"Native CLI delegation failed: {message}", file=sys.stderr)
        if completed.stderr.strip():
            print(completed.stderr.rstrip(), file=sys.stderr)
    print(f"DETAILS={out_dir}")
    return 0 if receipt["status"] == "ok" else (completed.returncode or 3)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"{type(error).__name__}: {error}", file=sys.stderr)
        raise SystemExit(2)
