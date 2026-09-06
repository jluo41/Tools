#!/usr/bin/env python3
"""Run one provider-native Agent SDK turn and write an auditable receipt.

This is intentionally a thin bridge over ``haiutils.agent_sdk``.  It is used by
the two delegation skills in this directory; it is not the LLMRec campaign
driver.  A receipt directory is one immutable-ish observation of one turn,
while ``--call-store`` is the persistent provider session store used for
resume.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
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

from haiutils.agent_sdk import (  # noqa: E402
    SessionSpec,
    campaign_sdk_home,
    neutral_workdir,
    package_version,
    run_turn,
)


SCHEMA = "haipipe.agent-sdk-delegation-receipt/v1"
DEFAULT_MODELS = {
    "claude": "claude-haiku-4-5-20251001",
    "codex": "gpt-5.6-luna",
}


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _write_json(path: Path, value: Any) -> None:
    _write_text(path, json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True, default=str) + "\n")


def _read_prompt(args: argparse.Namespace) -> str:
    if bool(args.prompt) == bool(args.prompt_file):
        raise ValueError("Provide exactly one of --prompt or --prompt-file")
    if args.prompt_file:
        prompt = args.prompt_file.read_text(encoding="utf-8")
    else:
        prompt = args.prompt
    prompt = prompt.strip()
    if not prompt:
        raise ValueError("The delegated prompt is empty")
    return prompt


def _read_system_prompt(args: argparse.Namespace) -> tuple[str, list[dict[str, str]]]:
    if args.system_prompt and args.system_prompt_file:
        raise ValueError("Use only one of --system-prompt or --system-prompt-file")
    if args.system_prompt_file:
        system = args.system_prompt_file.read_text(encoding="utf-8").strip()
    else:
        system = (args.system_prompt or "").strip()
    if not system:
        system = (
            "You are a delegated provider-native agent. The caller owns the "
            "overall task and will receive your final answer. Work only from "
            "the explicit prompt and context supplied in this turn; do not "
            "assume that the caller's current session, skills, or files are "
            "visible to you. State uncertainty instead of inventing context."
        )

    supplied_skills: list[dict[str, str]] = []
    for raw_path in args.skill_path:
        path = raw_path.resolve()
        if not path.is_file():
            raise FileNotFoundError(f"Skill context file not found: {path}")
        skill_text = path.read_text(encoding="utf-8")
        supplied_skills.append({"path": str(path), "sha256": _sha256(skill_text)})
        system += (
            "\n\n--- BEGIN EXPLICIT DELEGATED SKILL: "
            + str(path)
            + " ---\n"
            + skill_text
            + "\n--- END EXPLICIT DELEGATED SKILL ---"
        )
    return system, supplied_skills


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run one Claude Agent SDK or Codex Agent SDK turn and write a receipt."
    )
    parser.add_argument("--provider", choices=("claude", "codex"), required=True)
    parser.add_argument("--model", help="Exact provider model id; defaults to the low-cost validated arm")
    parser.add_argument("--campaign-id", required=True)
    parser.add_argument("--query-id", required=True)
    prompt = parser.add_mutually_exclusive_group()
    prompt.add_argument("--prompt")
    prompt.add_argument("--prompt-file", type=Path)
    parser.add_argument("--system-prompt")
    parser.add_argument("--system-prompt-file", type=Path)
    parser.add_argument(
        "--skill-path",
        action="append",
        type=Path,
        default=[],
        help="Explicitly append a local SKILL.md as delegated context; repeatable.",
    )
    parser.add_argument(
        "--call-store",
        type=Path,
        required=True,
        help="Persistent session/rollout store. Reuse this path when resuming.",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        required=True,
        help="Fresh directory for this turn's prompt, response, raw events, and receipt.",
    )
    parser.add_argument("--resume-session", help="Resume this exact provider session/thread id")
    parser.add_argument("--web", choices=("disabled", "live"), default="disabled")
    parser.add_argument("--max-turns", type=int, default=1)
    parser.add_argument(
        "--max-attempts",
        type=int,
        default=1,
        help="Transient retry attempts. Keep at 1 when avoiding duplicate billable calls.",
    )
    return parser


def _base_record(
    args: argparse.Namespace,
    prompt: str,
    system_prompt: str,
    supplied_skills: list[dict[str, str]],
    model: str,
    call_store: Path,
    out_dir: Path,
) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "created_at": datetime.now(UTC).isoformat(),
        "status": "started",
        "provider": args.provider,
        "transport": "claude_agent_sdk" if args.provider == "claude" else "openai_codex_sdk",
        "profile": "heavy",
        "sdk_package": "claude-agent-sdk" if args.provider == "claude" else "openai-codex",
        "sdk_version": package_version(args.provider),
        "requested_model": model,
        "campaign_id": args.campaign_id,
        "query_id": args.query_id,
        "resume_session": args.resume_session,
        "web_mode": args.web,
        "max_turns": args.max_turns,
        "max_attempts": args.max_attempts,
        "call_store": str(call_store),
        "receipt_dir": str(out_dir),
        "prompt_sha256": _sha256(prompt),
        "system_prompt_sha256": _sha256(system_prompt),
        "explicit_skill_context": supplied_skills,
        "billing_note": (
            "This records provider-reported per-turn usage/cost only. It does not "
            "expose remaining subscription or account-window quota; verify the "
            "provider usage view separately."
        ),
    }


def main() -> int:
    args = _parser().parse_args()
    model = args.model or DEFAULT_MODELS[args.provider]
    call_store = args.call_store.resolve()
    out_dir = args.out_dir.resolve()
    if out_dir == call_store or out_dir in call_store.parents:
        # The receipt may live below the call store, but the persistent store
        # must never be nested below a receipt directory.
        raise ValueError("--out-dir must not contain --call-store, and must not equal it")
    if out_dir.exists() and any(out_dir.iterdir()):
        raise FileExistsError(f"Refusing to overwrite a non-empty receipt directory: {out_dir}")
    out_dir.mkdir(parents=True, exist_ok=True)
    call_store.mkdir(parents=True, exist_ok=True)

    prompt = _read_prompt(args)
    system_prompt, supplied_skills = _read_system_prompt(args)
    base = _base_record(args, prompt, system_prompt, supplied_skills, model, call_store, out_dir)
    _write_text(out_dir / "prompt.md", prompt + "\n")
    _write_text(out_dir / "system_prompt.md", system_prompt + "\n")
    _write_json(out_dir / "request.json", base)

    spec = SessionSpec(
        provider=args.provider,
        model=model,
        campaign_id=args.campaign_id,
        query_id=args.query_id,
        sdk_home=campaign_sdk_home(call_store, args.provider, model, args.campaign_id),
        neutral_cwd=neutral_workdir(args.provider, args.campaign_id, args.query_id),
        system_prompt=system_prompt,
        web_mode=args.web,
        session_id=args.resume_session,
        max_turns=args.max_turns,
    )

    try:
        turn = run_turn(
            spec,
            prompt,
            call_store,
            max_attempts=args.max_attempts,
        )
    except KeyboardInterrupt as error:
        # A cancelled SDK process may have reached the provider before the
        # typed ResultMessage arrived. Never call this a free/zero-cost turn.
        failure = {
            **base,
            "status": "needs_recovery",
            "error_type": type(error).__name__,
            "error": "The local runner was interrupted before a ResultMessage arrived.",
            "provider_call_may_have_started": True,
            "cost_status": "unknown_until_provider_usage_is_checked",
        }
        _write_json(out_dir / "error.json", failure)
        print(json.dumps(failure, ensure_ascii=False, sort_keys=True))
        return 130
    except Exception as error:  # retain an actionable non-secret failure receipt
        failure = {
            **base,
            "status": "error",
            "error_type": type(error).__name__,
            "error": str(error),
            "provider_call_may_have_started": "unknown",
            "cost_status": "unknown_until_provider_usage_is_checked",
        }
        _write_json(out_dir / "error.json", failure)
        print(json.dumps(failure, ensure_ascii=False, sort_keys=True))
        return 1

    turn_dict = turn.as_dict()
    receipt = {
        **base,
        "status": "ok" if not turn.is_error else "provider_error",
        "resolved_model": turn.resolved_model,
        "session_id": turn.session_id,
        "turn_id": turn.turn_id,
        "rollout_path": turn.rollout_path,
        "sdk_home": turn.sdk_home,
        "neutral_cwd": turn.neutral_cwd,
        "duration_ms": turn.duration_ms,
        "is_error": turn.is_error,
        "error": turn.error,
        "usage": turn.usage,
        "cost_usd": turn.cost_usd,
        "raw_event_count": len(turn.raw_sdk_events),
        "tool_trace_count": len(turn.tool_trace),
        "web_search_count": turn.web_search_count,
        "web_fetch_count": turn.web_fetch_count,
        "quota_signal": {
            "sdk_reported_cost_usd": turn.cost_usd,
            "sdk_reported_usage": turn.usage,
            "remaining_account_limit": "not exposed by this SDK receipt",
        },
    }
    _write_json(out_dir / "turn.json", turn_dict)
    _write_json(out_dir / "usage_receipt.json", receipt)
    with (out_dir / "raw_sdk_events.jsonl").open("w", encoding="utf-8") as handle:
        for event in turn.raw_sdk_events:
            handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True, default=str) + "\n")
    _write_text(out_dir / "response.md", turn.raw_response.rstrip() + "\n")
    _write_text(
        out_dir / "receipt.md",
        "\n".join(
            [
                "# Agent SDK delegation receipt",
                "",
                f"- status: `{receipt['status']}`",
                f"- provider / transport: `{args.provider}` / `{receipt['transport']}`",
                f"- model: `{receipt['requested_model']}` → `{receipt['resolved_model']}`",
                f"- SDK: `{receipt['sdk_package']} {receipt['sdk_version']}`",
                f"- session: `{receipt['session_id']}`",
                f"- turn: `{receipt['turn_id']}`",
                f"- usage: `{json.dumps(receipt['usage'], ensure_ascii=False, sort_keys=True)}`",
                f"- SDK-reported cost: `{receipt['cost_usd']}`",
                f"- duration: `{receipt['duration_ms']} ms`",
                f"- rollout: `{receipt['rollout_path']}`",
                "",
                "> This is a per-turn SDK receipt, not a remaining-plan-limit meter. "
                "Subscription/account-window quota must be checked in the provider's "
                "own usage view.",
            ]
        )
        + "\n",
    )
    print(
        json.dumps(
            {
                "status": receipt["status"],
                "provider": args.provider,
                "model": receipt["resolved_model"],
                "session_id": receipt["session_id"],
                "cost_usd": receipt["cost_usd"],
                "usage": receipt["usage"],
                "response": turn.raw_response,
                "receipt_dir": str(out_dir),
            },
            ensure_ascii=False,
        )
    )
    return 0 if not turn.is_error else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"{type(error).__name__}: {error}", file=sys.stderr)
        raise SystemExit(2)
