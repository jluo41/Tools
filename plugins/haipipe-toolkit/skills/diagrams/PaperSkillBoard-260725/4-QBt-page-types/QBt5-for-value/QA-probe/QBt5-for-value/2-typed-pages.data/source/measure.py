#!/usr/bin/env python3
"""MEASURE the board estate: how many pages exist, and how many declare a type.

The producing run behind `2-typed-pages.md`. It prints a table; a person pastes
it into the record's `## Answer` fence, and `build.py` parses it into the CSV.

A page is counted the way `src/common.py` counts one: a `.md` whose name starts
Q, S, Agent- or Meeting-, with `_` and `.` segments and `fig/` skipped.

    python3 measure.py [boards-dir]
"""
import pathlib
import re
import sys

TYPED = re.compile(r"(?m)^(?:page-type|route)\s*:\s*\S+")
PREFIX = ("Q", "S", "Agent-", "Meeting-")
DEFAULT = "Tools/plugins/haipipe-toolkit/skills/diagrams"

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else DEFAULT).resolve()
boards = sorted(d for d in root.iterdir()
                if d.is_dir() and (d / "board.md").is_file())
if not boards:
    sys.exit(f"no board.md under {root}")

rows = []
for b in boards:
    pages = [f for f in b.rglob("*.md")
             if f.name.startswith(PREFIX)
             and not any(p.startswith(("_", ".")) or p == "fig"
                         for p in f.relative_to(b).parts)]
    typed = sum(1 for f in pages if TYPED.search(f.read_text(errors="ignore")[:1500]))
    rows.append((b.name, len(pages), typed))

w = max(len(r[0]) for r in rows)
print(f"  {'board':<{w}}  pages  typed")
print(f"  {'-' * w}  -----  -----")
for name, n, ty in rows:
    print(f"  {name:<{w}}  {n:>5}  {ty:>5}")
tp, tt = sum(r[1] for r in rows), sum(r[2] for r in rows)
print(f"\n  {len(rows)} boards · {tp} pages · {tt} declare a type key "
      f"({100 * tt // tp if tp else 0}%)")
