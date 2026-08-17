#!/usr/bin/env python3
"""Read-only status probe for generic and Physician LLMRec runtimes."""

from __future__ import annotations

import argparse
import json
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any


PACKAGES = ("claude-agent-sdk", "openai-codex")
PROJECT = Path("examples/Project-LLMRec-Physician")


def locate_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in (current, *current.parents):
        if (candidate / "pyproject.toml").is_file() and (candidate / "code").is_dir():
            return candidate
    raise RuntimeError(f"Could not locate repository root from {start}")


def package_versions() -> dict[str, str | None]:
    values: dict[str, str | None] = {}
    for package in PACKAGES:
        try:
            values[package] = version(package)
        except PackageNotFoundError:
            values[package] = None
    return values


def receipt_summary(root: Path) -> dict[str, Any]:
    call_store = root / "_WorkSpace/A-LLMRecPhy/4-LLMCallStore"
    audit_roots = sorted(call_store.glob("v*/audits"))
    receipts = sorted(
        path
        for audit_root in audit_roots
        for path in audit_root.glob("*/*/audit_receipt_v5.json")
    )
    passed = 0
    invalid = 0
    for path in receipts:
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            invalid += 1
            continue
        if value.get("verdict") == "pass":
            passed += 1
        else:
            invalid += 1
    return {
        "roots": [str(path.relative_to(root)) for path in audit_roots],
        "receipts": len(receipts),
        "pass": passed,
        "nonpass_or_invalid": invalid,
    }


def status(root: Path) -> dict[str, Any]:
    runtime = root / PROJECT / "tasks/llmrec_agent_sdk.py"
    verifier = root / PROJECT / "tasks/verify_llmrec_agent_sdk.py"
    generic = root / "code/haiutils/llm_engine"
    return {
        "repository_root": str(root),
        "llmrec": {
            "runtime": str(runtime.relative_to(root)),
            "runtime_exists": runtime.is_file(),
            "verifier": str(verifier.relative_to(root)),
            "verifier_exists": verifier.is_file(),
            "call_store": "_WorkSpace/A-LLMRecPhy/4-LLMCallStore",
            "audits": receipt_summary(root),
        },
        "generic": {
            "runtime": str(generic.relative_to(root)),
            "runtime_exists": generic.is_dir(),
            "note": "Do not create on a read-only status request.",
        },
        "packages": package_versions(),
    }


def render(value: dict[str, Any]) -> str:
    llmrec = value["llmrec"]
    generic = value["generic"]
    audits = llmrec["audits"]
    packages = value["packages"]
    return "\n".join(
        (
            f"repository: {value['repository_root']}",
            f"llmrec runtime: {'present' if llmrec['runtime_exists'] else 'missing'} ({llmrec['runtime']})",
            f"llmrec verifier: {'present' if llmrec['verifier_exists'] else 'missing'} ({llmrec['verifier']})",
            f"generic runtime: {'present' if generic['runtime_exists'] else 'missing'} ({generic['runtime']})",
            f"SDK packages: claude-agent-sdk={packages['claude-agent-sdk'] or 'missing'}, "
            f"openai-codex={packages['openai-codex'] or 'missing'}",
            f"audit receipts: {audits['pass']} pass / {audits['receipts']} total / "
            f"{audits['nonpass_or_invalid']} nonpass-or-invalid",
        )
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    root = locate_root(args.root)
    value = status(root)
    print(json.dumps(value, indent=2, sort_keys=True) if args.json else render(value))
    return 0 if value["llmrec"]["runtime_exists"] or value["generic"]["runtime_exists"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
