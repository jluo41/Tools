#!/usr/bin/env python3
"""MEASURE how many real artifact paths each page-type contract names.

The producing run behind `1-artifact-paths.md`. It prints a table; a person
pastes that table into the record's `## Answer` fence, and `build.py` parses the
fence back into `counts.csv`. The numbers are typed exactly once, in the record.

WHY THIS QUESTION. `QB6 §7` claims a page type owns folders and files, and that
the contracts do not say so. That is checkable: count, per contract, the
mentions of a path a page of that type actually owns.

SCANNED, NEVER LISTED. This held ten contract names as a literal, and an
eleventh type, `for-labeling`, shipped on 260807 without ever being measured:
the instrument that found "the contracts do not say" could not see it. That is
the same defect this session had just fixed four times over in
`cli/asset-manifest.py`, in code it did not write: the rule was right and the
input set was guessed. A measurement that names its own inputs by hand goes
stale the first time the world adds one.

    python3 measure.py [contracts-dir]
"""
import pathlib
import re
import sys

PATHS = re.compile(
    r"float\.tex|preview\.|assets/|candidates/|QA-probe/|sections/|"
    r"\.bib\b|\.cls\b|\.bst\b")
DEFAULT = "Tools/plugins/haipipe-toolkit/skills/board/page-types"

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else DEFAULT).resolve()
rows = []
for d in sorted(root.glob("haipipe-page-for-*")):
    f = d / "SKILL.md"
    if not f.is_file():
        continue
    text = f.read_text(errors="ignore")
    rows.append((d.name.replace("haipipe-page-for-", ""),
                 len(PATHS.findall(text)), len(text.splitlines())))
if not rows:
    sys.exit(f"no contracts under {root}")

w = max(len(r[0]) for r in rows)
print(f"  {'contract':<{w}}  paths  lines")
print(f"  {'-' * w}  -----  -----")
for name, n, lines in rows:
    print(f"  {name:<{w}}  {n:>5}  {lines:>5}")
print(f"\n  {len(rows)} contracts · {sum(r[1] for r in rows)} artifact-path "
      f"mentions total · {sum(1 for r in rows if r[1] == 0)} name none at all")
