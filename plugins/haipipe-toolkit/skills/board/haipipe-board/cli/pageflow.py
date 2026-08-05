#!/usr/bin/env python3
"""Audit a serialized Page RUN without invoking any AI agent."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))

from src.page_lifecycle import audit_artifacts, audit_run, traversed_edges  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    audit = subparsers.add_parser("audit", help="validate one Page RUN receipt")
    audit.add_argument("receipt", type=Path)
    audit.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    try:
        run = json.loads(args.receipt.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR receipt-read {args.receipt}: {exc}", file=sys.stderr)
        return 2

    findings = audit_run(run) + audit_artifacts(run, args.receipt.parent)
    edges = traversed_edges(run.get("receipts", []))
    if args.as_json:
        print(
            json.dumps(
                {
                    "status": "pass" if not findings else "fail",
                    "findings": [finding.__dict__ for finding in findings],
                    "edges": edges,
                },
                indent=2,
                ensure_ascii=False,
            )
        )
    elif findings:
        for finding in findings:
            print(f"ERROR {finding.code} {finding.where}: {finding.message}")
        print(f"FAIL page-lifecycle: {len(findings)} finding(s); edges={','.join(edges)}")
    else:
        print(f"PASS page-lifecycle: {len(edges)} receipt(s); edges={','.join(edges)}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
