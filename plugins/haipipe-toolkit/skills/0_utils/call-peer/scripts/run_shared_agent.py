#!/usr/bin/env python3
"""Run one bounded native SDK turn using the user's normal provider home.

This is the interactive counterpart to ``run_native_agent.py``.  It keeps the
provider-native transcript in ~/.claude or ~/.codex so the matching CLI/IDE
surface can resume the same session.  It intentionally keeps the bridge
permissions conservative; sharing a home is not permission escalation.
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import os
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
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


SCHEMA = "haipipe.agent-sdk-shared-receipt/v1"
DEFAULT_MODELS = {
    "claude": "claude-haiku-4-5-20251001",
    "codex": "gpt-5.6-luna",
}


def _jsonable(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    if hasattr(value, "model_dump"):
        return _jsonable(value.model_dump())
    if hasattr(value, "__dict__"):
        return _jsonable(vars(value))
    return str(value)


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _write_json(path: Path, value: Any) -> None:
    _write_text(path, json.dumps(_jsonable(value), indent=2, ensure_ascii=False, sort_keys=True) + "\n")


def _read_prompt(args: argparse.Namespace) -> str:
    if bool(args.prompt) == bool(args.prompt_file):
        raise ValueError("Provide exactly one of --prompt or --prompt-file")
    prompt = args.prompt_file.read_text(encoding="utf-8") if args.prompt_file else args.prompt
    prompt = prompt.strip()
    if not prompt:
        raise ValueError("The delegated prompt is empty")
    return prompt


def _read_system_prompt(args: argparse.Namespace) -> str:
    if args.system_prompt and args.system_prompt_file:
        raise ValueError("Use only one of --system-prompt or --system-prompt-file")
    if args.system_prompt_file:
        system = args.system_prompt_file.read_text(encoding="utf-8").strip()
    else:
        system = (args.system_prompt or "").strip()
    if not system:
        system = (
            "You are a bounded delegated agent. Work only from the prompt and "
            "the visible project context. Return a concise result to the caller."
        )
    for raw_path in args.skill_path:
        path = raw_path.resolve()
        if not path.is_file():
            raise FileNotFoundError(f"Skill context file not found: {path}")
        system += (
            "\n\n--- BEGIN EXPLICIT DELEGATED SKILL: "
            + str(path)
            + " ---\n"
            + path.read_text(encoding="utf-8")
            + "\n--- END EXPLICIT DELEGATED SKILL ---"
        )
    return system


def _default_config_dir(provider: str) -> Path:
    return Path.home() / (".claude" if provider == "claude" else ".codex")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run one shared-home Claude Agent SDK or Codex SDK turn."
    )
    parser.add_argument("--provider", choices=("claude", "codex"), required=True)
    parser.add_argument("--model")
    prompt = parser.add_mutually_exclusive_group()
    prompt.add_argument("--prompt")
    prompt.add_argument("--prompt-file", type=Path)
    parser.add_argument("--system-prompt")
    parser.add_argument("--system-prompt-file", type=Path)
    parser.add_argument("--skill-path", action="append", type=Path, default=[])
    parser.add_argument("--session-id", help="Resume this provider-native session/thread")
    parser.add_argument("--config-dir", type=Path, help="Defaults to ~/.claude or ~/.codex")
    parser.add_argument("--cwd", type=Path, default=ROOT, help="Shared project working directory")
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--web", choices=("disabled", "live"), default="disabled")
    parser.add_argument("--max-turns", type=int, default=1)
    parser.add_argument("--dry-run", action="store_true", help="Resolve paths without calling a provider")
    return parser


def _base(args: argparse.Namespace, prompt: str, system: str, model: str, config_dir: Path, cwd: Path, out_dir: Path) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "created_at": datetime.now(UTC).isoformat(),
        "mode": "shared",
        "status": "started",
        "provider": args.provider,
        "transport": "claude_agent_sdk" if args.provider == "claude" else "openai_codex_sdk",
        "profile": "shared-sdk",
        "requested_model": model,
        "session_id": args.session_id,
        "config_dir": str(config_dir),
        "working_directory": str(cwd),
        "receipt_dir": str(out_dir),
        "web_mode": args.web,
        "max_turns": args.max_turns,
        "prompt_sha256": _sha256(prompt),
        "system_prompt_sha256": _sha256(system),
        "permission_note": "Shared mode keeps the bridge permission policy conservative; use Claude CLI or VS Code for interactive approvals and full tool control.",
    }


def _find_rollout(config_dir: Path, provider: str, session_id: str) -> Path | None:
    if provider == "claude":
        candidates = sorted((config_dir / "projects").glob(f"**/{session_id}.jsonl"))
    else:
        candidates = sorted((config_dir / "sessions").glob(f"**/*{session_id}*.jsonl"))
    return candidates[-1].resolve() if candidates else None


def _claude_trace(message: Any) -> dict[str, Any] | None:
    name = getattr(message, "name", None)
    if name is None or not hasattr(message, "input"):
        return None
    return {
        "provider_tool": str(name),
        "input": _jsonable(getattr(message, "input", None)),
        "tool_use_id": getattr(message, "id", None),
    }


async def _run_claude(args: argparse.Namespace, prompt: str, system: str, model: str, config_dir: Path, cwd: Path) -> dict[str, Any]:
    from claude_agent_sdk import AssistantMessage, ClaudeAgentOptions, ClaudeSDKClient, ResultMessage, TextBlock

    allowed = ["WebSearch", "WebFetch"] if args.web == "live" else []
    environment = dict(os.environ)
    environment["CLAUDE_CONFIG_DIR"] = str(config_dir)
    options = ClaudeAgentOptions(
        cwd=str(cwd),
        tools=allowed,
        allowed_tools=allowed,
        disallowed_tools=[] if args.web == "live" else ["WebSearch", "WebFetch"],
        permission_mode="dontAsk",
        max_turns=args.max_turns,
        model=model,
        system_prompt=system,
        resume=args.session_id,
        # Shared transcript, conservative delegated context.  The CLI/VS Code
        # side can load the normal skills/tools when the human takes over.
        setting_sources=[],
        skills=[],
        plugins=[],
        env=environment,
    )
    raw_events: list[dict[str, Any]] = []
    text_parts: list[str] = []
    trace: list[dict[str, Any]] = []
    resolved_models: list[str] = []
    final: Any = None
    started = time.monotonic()
    async with ClaudeSDKClient(options=options) as client:
        await client.query(prompt)
        async for message in client.receive_response():
            raw_events.append(_jsonable(message))
            if isinstance(message, AssistantMessage):
                if message.model:
                    resolved_models.append(str(message.model))
                for block in message.content:
                    if isinstance(block, TextBlock):
                        text_parts.append(block.text)
                    else:
                        item = _claude_trace(block)
                        if item:
                            trace.append(item)
            elif isinstance(message, ResultMessage):
                final = message
    response = (getattr(final, "result", None) if final else None) or "\n\n".join(text_parts)
    session_id = str(getattr(final, "session_id", "") or "")
    if not session_id:
        raise RuntimeError("Claude Agent SDK did not return a session_id")
    if args.session_id and session_id != args.session_id:
        raise RuntimeError(f"Claude resumed {args.session_id} but returned {session_id}")
    errors = list(getattr(final, "errors", None) or []) if final else []
    is_error = bool(getattr(final, "is_error", False)) if final else not bool(response.strip())
    return {
        "resolved_model": resolved_models[-1] if resolved_models else model,
        "session_id": session_id,
        "turn_id": str(getattr(final, "uuid", "") or "") or None,
        "rollout_path": str(_find_rollout(config_dir, "claude", session_id) or ""),
        "raw_response": response,
        "raw_events": raw_events,
        "tool_trace": trace,
        "usage": _jsonable(getattr(final, "usage", None)) if final else None,
        "cost_usd": getattr(final, "total_cost_usd", None) if final else None,
        "duration_ms": getattr(final, "duration_ms", None) or round((time.monotonic() - started) * 1000),
        "is_error": is_error or bool(errors),
        "error": "; ".join(str(error) for error in errors) if errors else None,
    }


def _codex_config(web: str) -> dict[str, Any]:
    return {
        "project_doc_max_bytes": 0,
        "project_doc_fallback_filenames": [],
        "web_search": "live" if web == "live" else "disabled",
        "features": {
            "shell_tool": False,
            "unified_exec": False,
            "memories": False,
            "apps": False,
            "plugins": False,
            "multi_agent": False,
            "browser_use": False,
            "computer_use": False,
            "image_generation": False,
        },
        "memories": {"generate_memories": False, "dedicated_tools": False, "disable_on_external_context": True},
    }


def _run_codex(args: argparse.Namespace, prompt: str, system: str, model: str, config_dir: Path, cwd: Path) -> dict[str, Any]:
    from openai_codex import ApprovalMode, Codex, CodexConfig, Sandbox

    environment = dict(os.environ)
    environment["CODEX_HOME"] = str(config_dir)
    environment["CODEX_SQLITE_HOME"] = str(config_dir / "sqlite")
    config = CodexConfig(cwd=str(cwd), env=environment)
    started = time.monotonic()
    with Codex(config) as codex:
        common = {
            "approval_mode": ApprovalMode.deny_all,
            "base_instructions": system,
            "config": _codex_config(args.web),
            "cwd": str(cwd),
            "model": model,
            "sandbox": Sandbox.read_only,
        }
        thread = codex.thread_resume(args.session_id, **common) if args.session_id else codex.thread_start(ephemeral=False, **common)
        if args.session_id and thread.id != args.session_id:
            raise RuntimeError(f"Codex resumed {args.session_id} but returned {thread.id}")
        result = thread.run(prompt, sandbox=Sandbox.read_only)
    raw_events = [_jsonable(item) for item in result.items]
    return {
        "resolved_model": model,
        "session_id": thread.id,
        "turn_id": result.id,
        "rollout_path": str(_find_rollout(config_dir, "codex", thread.id) or ""),
        "raw_response": result.final_response or "",
        "raw_events": raw_events,
        "tool_trace": [],
        "usage": _jsonable(result.usage),
        "cost_usd": None,
        "duration_ms": result.duration_ms or round((time.monotonic() - started) * 1000),
        "is_error": _jsonable(result.status) == "failed" or not bool((result.final_response or "").strip()),
        "error": json.dumps(_jsonable(result.error), sort_keys=True) if result.error else None,
    }


def main() -> int:
    args = _parser().parse_args()
    model = args.model or DEFAULT_MODELS[args.provider]
    prompt = _read_prompt(args)
    system = _read_system_prompt(args)
    config_dir = (args.config_dir or _default_config_dir(args.provider)).expanduser().resolve()
    cwd = args.cwd.expanduser().resolve()
    out_dir = args.out_dir.expanduser().resolve()
    if not cwd.is_dir():
        raise NotADirectoryError(f"Working directory does not exist: {cwd}")
    if out_dir.exists() and any(out_dir.iterdir()):
        raise FileExistsError(f"Refusing to overwrite a non-empty receipt directory: {out_dir}")
    out_dir.mkdir(parents=True, exist_ok=True)
    base = _base(args, prompt, system, model, config_dir, cwd, out_dir)
    _write_text(out_dir / "prompt.md", prompt + "\n")
    _write_text(out_dir / "system_prompt.md", system + "\n")
    _write_json(out_dir / "request.json", base)
    if args.dry_run:
        base["status"] = "dry_run"
        _write_json(out_dir / "usage_receipt.json", base)
        print(json.dumps(base, ensure_ascii=False, sort_keys=True))
        return 0
    result = asyncio.run(_run_claude(args, prompt, system, model, config_dir, cwd)) if args.provider == "claude" else _run_codex(args, prompt, system, model, config_dir, cwd)
    receipt = {
        **base,
        "status": "provider_error" if result["is_error"] else "ok",
        "resolved_model": result["resolved_model"],
        "session_id": result["session_id"],
        "turn_id": result["turn_id"],
        "rollout_path": result["rollout_path"],
        "duration_ms": result["duration_ms"],
        "usage": result["usage"],
        "cost_usd": result["cost_usd"],
        "raw_event_count": len(result["raw_events"]),
        "tool_trace_count": len(result["tool_trace"]),
        "error": result["error"],
    }
    _write_json(out_dir / "turn.json", result)
    _write_json(out_dir / "usage_receipt.json", receipt)
    with (out_dir / "raw_sdk_events.jsonl").open("w", encoding="utf-8") as handle:
        for event in result["raw_events"]:
            handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True, default=str) + "\n")
    _write_text(out_dir / "response.md", result["raw_response"].rstrip() + "\n")
    _write_text(out_dir / "receipt.md", "# Shared Agent SDK receipt\n\n" + "\n".join(f"- {key}: `{value}`" for key, value in receipt.items()) + "\n")
    print(json.dumps({"status": receipt["status"], "provider": args.provider, "session_id": receipt["session_id"], "config_dir": str(config_dir), "working_directory": str(cwd), "response": result["raw_response"], "receipt_dir": str(out_dir)}, ensure_ascii=False))
    return 1 if result["is_error"] else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"{type(error).__name__}: {error}", file=sys.stderr)
        raise SystemExit(2)
