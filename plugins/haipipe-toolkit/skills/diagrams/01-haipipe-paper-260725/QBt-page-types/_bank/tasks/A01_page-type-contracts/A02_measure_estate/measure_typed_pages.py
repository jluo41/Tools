#!/usr/bin/env python3
"""Count how many board pages exist, and how many declare a type key.

The producing run behind `QA/2-typed-pages.md`.

WHY THIS QUESTION. `QB6` admits ten page types and `§5.1` rule 1 ships a checker
that reads the head key. Neither says how much of the estate CARRIES one, and
that is the number deciding whether the type system is a design or a fact.

A page is counted the way `src/common.py` counts one: a `.md` whose name starts
Q, S, Agent- or Meeting-, with `_` and `.` segments and `fig/` skipped.

    python3 measure_typed_pages.py [boards-dir]
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
