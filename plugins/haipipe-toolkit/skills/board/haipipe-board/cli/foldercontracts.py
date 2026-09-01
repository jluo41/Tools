#!/usr/bin/env python3
"""Inventory and validate workflow-phase Folder contracts."""
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
    args = parser.parse_args()
    contracts, problems = validate_tree(args.skills_root.resolve())
    print("phase  workflow                      folder kind          face  ruling       legacy")
    print("─────  ────────────────────────────  ───────────────────  ────  ───────────  ──────")
    for item in sorted(contracts, key=lambda x: (x.workflow, x.phase)):
        print(
            f"{item.phase:<5}  {item.workflow:<28}  {item.folder_kind:<19}  "
            f"{item.primary_face:<4}  {item.page_ruling:<11}  "
            f"{item.legacy_page_type or '—'}"
        )
    for problem in problems:
        print(f"finding · {problem}")
    print(f"{len(contracts)} phase contracts · {len(problems)} findings")
    return 1 if args.check and problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
