#!/usr/bin/env python3
"""Inventory and validate workflow-owned Folder contracts."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

HERE = Path(__file__).resolve()
BOARD_SKILL = HERE.parent.parent
SKILLS = BOARD_SKILL.parent.parent
sys.path.insert(0, str(BOARD_SKILL))

from src.folder_contract import validate_tree  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="exit non-zero on findings")
    parser.add_argument("--skills-root", type=Path, default=SKILLS)
    parser.add_argument(
        "--workflow",
        action="append",
        default=[],
        help="validate only this workflow owner; repeat for more than one",
    )
    args = parser.parse_args()
    contracts, problems = validate_tree(args.skills_root.resolve())
    if args.workflow:
        requested = set(args.workflow)
        present = {item.workflow for item in contracts}
        contracts = [item for item in contracts if item.workflow in requested]
        selected_paths = {item.path.as_posix() for item in contracts}
        problems = [
            problem for problem in problems
            if any(path in problem for path in selected_paths)
        ]
        missing = sorted(requested - present)
    else:
        missing = []
    problems.extend(f"requested workflow not found: {name}" for name in missing)
    print("workflow                      folder kind          face  ruling       legacy")
    print("────────────────────────────  ───────────────────  ────  ───────────  ──────")
    for item in sorted(contracts, key=lambda x: (x.workflow, x.folder_kind)):
        print(
            f"{item.workflow:<28}  {item.folder_kind:<19}  "
            f"{item.primary_face:<4}  {item.page_ruling:<11}  "
            f"{item.legacy_page_type or '—'}"
        )
    for problem in problems:
        print(f"finding · {problem}")
    print(f"{len(contracts)} Folder contracts · {len(problems)} findings")
    return 1 if args.check and problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
