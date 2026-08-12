#!/usr/bin/env python3
"""Count how many real artifact paths each page-type contract names.

The producing run behind `QA/1-artifact-paths.md`. It prints a table; the
QA-bank carries that table as its `## Answer`, and the consumer's QA-probe
extracts it into `counts.csv`. The numbers are typed exactly once, in the bank.

WHY THIS QUESTION. `QB6 §7` claims a page type owns folders and files, and that
the contracts do not say so. That is checkable: count, per contract, the
mentions of a path a page of that type actually owns.

    python3 measure_artifact_paths.py [contracts-dir]
"""
import pathlib
import re
import sys

PATHS = re.compile(
    r"float\.tex|preview\.|assets/|candidates/|QA-probe/|sections/|"
    r"\.bib\b|\.cls\b|\.bst\b")
DEFAULT = "Tools/plugins/haipipe-toolkit/skills/board/page-types"
ORDER = ["design", "display", "literature", "meeting", "section",
         "skill", "slide", "stage", "value", "venue"]

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else DEFAULT).resolve()
rows = []
for name in ORDER:
    f = root / f"haipipe-page-for-{name}" / "SKILL.md"
    if not f.is_file():
        sys.exit(f"missing contract: {f}")
    text = f.read_text(errors="ignore")
    rows.append((name, len(PATHS.findall(text)), len(text.splitlines())))

w = max(len(r[0]) for r in rows)
print(f"  {'contract':<{w}}  paths  lines")
print(f"  {'-' * w}  -----  -----")
for name, n, lines in rows:
    print(f"  {name:<{w}}  {n:>5}  {lines:>5}")
print(f"\n  {len(rows)} contracts · {sum(r[1] for r in rows)} artifact-path "
      f"mentions total · {sum(1 for r in rows if r[1] == 0)} name none at all")
