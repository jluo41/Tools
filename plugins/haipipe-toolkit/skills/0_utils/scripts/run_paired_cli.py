#!/usr/bin/env python3
"""Create or resume the other provider's native CLI session as a pair.

It uses the provider's normal ``~/.claude`` or ``~/.codex`` home, sends one
explicit context/task packet, and stores only the native session-id mapping.
It does not create an ``agent-calls`` store, a custom provider home, or a
transcript mirror.
"""

from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from run_cli_agent import (  # noqa: E402
    ROOT,
    _normalize_claude_resume_entrypoint,
    _native_env,
    _parse_claude,
    _parse_codex,
    _read_prompt,
)
from pair_sync import (  # noqa: E402
    pair_file_for_name,
    paired_session_context,
    provider_lock,
    register_pair,
    resolve_pair_session,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create or resume the other provider's native CLI session as a named pair."
    )
    parser.add_argument("--pair-name", required=True, help="Shared human-readable pair name")
    parser.add_argument("--caller-provider", choices=("claude", "codex"), required=True)
    parser.add_argument("--caller-session-id", help="Current caller session id, when available")
    parser.add_argument("--callee-provider", choices=("claude", "codex"), required=True)
    parser.add_argument(
        "--callee-session-id",
        "--session-id",
        dest="callee_session_id",
        help="Existing partner session id; pair name lookup is used when omitted",
    )
    parser.add_argument(
        "--new-session",
        action="store_true",
        help="Force a new partner session even when this pair name already has one",
    )
    prompt = parser.add_mutually_exclusive_group()
    prompt.add_argument("--prompt")
    prompt.add_argument("--prompt-file", type=Path)
    parser.add_argument("--model", help="Optional native CLI model override")
    parser.add_argument(
        "--cli-arg",
        action="append",
        default=[],
        help="One extra argument passed to the callee CLI; repeat as needed",
    )
    parser.add_argument("--cwd", type=Path, default=ROOT)
    parser.add_argument(
        "--timeout",
        type=float,
        default=300,
        help="Maximum seconds to wait for the native callee CLI (default: 300)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Show the native command without calling a provider")
    return parser


def _handshake(
    args: argparse.Namespace,
    cwd: Path,
    manifest: dict[str, Any] | None = None,
) -> str:
    """Return the identity-only context for the callee's first/resumed run."""
    context_manifest = manifest or {
        "pair_name": args.pair_name,
        "cwd": str(cwd),
        "providers": {
            args.caller_provider: {"session_id": args.caller_session_id or ""},
            args.callee_provider: {"session_id": args.callee_session_id or ""},
        },
    }
    return paired_session_context(
        manifest=context_manifest,
        self_provider=args.callee_provider,
        self_session_id=args.callee_session_id or "NEW_SESSION",
    )


def _infer_caller_session_id(args: argparse.Namespace) -> str | None:
    if args.caller_session_id:
        return args.caller_session_id
    names = (
        ("CODEX_THREAD_ID", "CODEX_SESSION_ID")
        if args.caller_provider == "codex"
        else ("CLAUDE_CODE_SESSION_ID",)
    )
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    return None


def _caller_identity_ids(args: argparse.Namespace) -> set[str]:
    names = (
        ("CODEX_THREAD_ID", "CODEX_SESSION_ID")
        if args.caller_provider == "codex"
        else ("CLAUDE_CODE_SESSION_ID",)
    )
    ids = {value for value in (args.caller_session_id, os.environ.get("HAIPIPE_PAIR_CALLER_SESSION_ID")) if value}
    ids.update(os.environ.get(name) for name in names if os.environ.get(name))
    return ids


def _command(args: argparse.Namespace) -> list[str]:
    if args.caller_provider == args.callee_provider:
        raise ValueError("caller and callee providers must be different")

    if args.callee_provider == "claude":
        command = ["claude", "-p", "--output-format", "json", "--name", args.pair_name]
        if args.callee_session_id:
            command += ["--resume", args.callee_session_id]
        if args.model:
            command += ["--model", args.model]
        command += args.cli_arg
        return command

    command = ["codex", "exec", "--json"]
    if args.model:
        command += ["--model", args.model]
    command += args.cli_arg
    if args.callee_session_id:
        command += ["resume", args.callee_session_id, "-"]
    else:
        command += ["-"]
    return command


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


def main() -> int:
    args = _parser().parse_args()
    pair_name = args.pair_name.strip()
    if not pair_name:
        raise ValueError("--pair-name must not be empty")
    args.pair_name = pair_name
    if args.caller_provider == args.callee_provider:
        raise ValueError("caller and callee providers must be different")
    args.caller_session_id = _infer_caller_session_id(args)
    if args.callee_session_id and args.callee_session_id in _caller_identity_ids(args):
        raise ValueError(
            "Refusing to resume the caller's own session as the callee; "
            "use the partner provider session id"
        )

    prompt = _read_prompt(args)
    cwd = args.cwd.expanduser().resolve()
    if not cwd.is_dir():
        raise NotADirectoryError(f"Working directory does not exist: {cwd}")
    pair_manifest: dict[str, Any] | None = None
    if not args.callee_session_id and not args.new_session:
        try:
            _manifest_path, pair_manifest, args.callee_session_id = resolve_pair_session(
                pair_name=args.pair_name,
                provider=args.callee_provider,
                cwd=cwd,
            )
            if not args.caller_session_id:
                caller_record = (pair_manifest.get("providers") or {}).get(args.caller_provider) or {}
                registered_caller_id = caller_record.get("session_id")
                if isinstance(registered_caller_id, str) and registered_caller_id:
                    args.caller_session_id = registered_caller_id
        except FileNotFoundError:
            # First use of this pair name: create the partner below.
            pass
    handshake = _handshake(args, cwd, pair_manifest)
    delegated_prompt = f"{handshake}\n\n[Delegated task]\n{prompt}"
    command = _command(args)
    manifest_path = pair_file_for_name(args.pair_name, cwd)

    if args.dry_run:
        print(
            json.dumps(
                {
                    "status": "dry_run",
                    "pair_name": args.pair_name,
                    "caller_provider": args.caller_provider,
                    "caller_session_id": args.caller_session_id,
                    "callee_provider": args.callee_provider,
                    "callee_session_id": args.callee_session_id,
                    "command": command,
                    "display_command": shlex.join(command),
                    "cwd": str(cwd),
                    "native_home": "~/.claude" if args.callee_provider == "claude" else "~/.codex",
                },
                ensure_ascii=False,
            )
        )
        return 0

    try:
        with provider_lock(manifest_path, args.callee_provider):
            completed = subprocess.run(
                command,
                input=delegated_prompt + "\n",
                text=True,
                capture_output=True,
                cwd=str(cwd),
                env={
                    **_native_env(args.callee_provider, None),
                    "HAIPIPE_PAIR_NAME": args.pair_name,
                    "HAIPIPE_PAIR_FILE": str(manifest_path),
                    "HAIPIPE_PAIR_CALLER_PROVIDER": args.caller_provider,
                    "HAIPIPE_PAIR_CALLER_SESSION_ID": args.caller_session_id or "",
                },
                check=False,
                timeout=args.timeout,
            )
    except subprocess.TimeoutExpired:
        print(
            f"Native paired CLI timed out after {args.timeout:g}s; no partner session id was returned.",
            file=sys.stderr,
        )
        return 124
    except OSError as error:
        print(f"Native paired CLI could not start: {error}", file=sys.stderr)
        return 127

    result = (
        _parse_claude(completed.stdout, completed.returncode)
        if args.callee_provider == "claude"
        else _parse_codex(completed.stdout, completed.returncode, args.callee_session_id)
    )
    if args.callee_provider == "claude" and result.get("status") == "ok":
        normalized = _normalize_claude_resume_entrypoint(
            result["session_id"],
            cwd,
            None,
        )
        if normalized is not None:
            result["resume_entrypoint"] = "cli"
            result["session_transcript"] = str(normalized)
    if result["status"] != "ok":
        message = result.get("error") or "Native paired CLI did not return a complete response"
        print(f"Native paired CLI failed: {message}", file=sys.stderr)
        if completed.stderr.strip():
            print(completed.stderr.rstrip(), file=sys.stderr)
        return completed.returncode or 3

    registered_path = None
    if args.caller_session_id:
        delivery_by_provider = {"claude": "call", "codex": "mailbox"}
        registered_path = register_pair(
            pair_name=args.pair_name,
            cwd=cwd,
            caller_provider=args.caller_provider,
            caller_session_id=args.caller_session_id,
            callee_provider=args.callee_provider,
            callee_session_id=result["session_id"],
            caller_delivery=delivery_by_provider[args.caller_provider],
            callee_delivery=delivery_by_provider[args.callee_provider],
        )

    print(result["response"].rstrip())
    print()
    print(f"PAIR_NAME={args.pair_name}")
    print(f"CALLER_PROVIDER={args.caller_provider}")
    print(f"CALLER_SESSION_ID={args.caller_session_id or 'not supplied'}")
    print(f"CALLEE_PROVIDER={args.callee_provider}")
    print(f"CALLEE_SESSION_ID={result['session_id']}")
    print(f"CALLEE_MODEL={result.get('resolved_model') or 'not reported'}")
    if registered_path:
        print(f"PAIR_FILE={registered_path}")
    print(f"PROVIDER_REPORTED_COST_USD={result.get('cost_usd')}")
    print(
        "PROVIDER_REPORTED_USAGE="
        + json.dumps(result.get("usage"), ensure_ascii=False, sort_keys=True)
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"{type(error).__name__}: {error}", file=sys.stderr)
        raise SystemExit(2)
