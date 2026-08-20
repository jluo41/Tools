#!/usr/bin/env python3
"""Parse the record's ## Answer fence into counts.csv. Never retype a number.

Strict on purpose: every non-rule line inside the fence must match or this
exits 1, because a lenient parser that skipped a malformed row would silently
ship a short table and the whole point of one-place numbers is that it cannot.

    python3 build.py     ->  ../counts.csv
"""
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
# EXTRACT FROM THE BANK, not from the probe. The probe holds the binding and
# a digest; the answer is the executor's and lives in its own tree. Reading
# the probe made this record the original, which is the twin law backwards.
REC = HERE.parents[3] / "_bank/tasks/A01_page-type-contracts/QA/2-typed-pages.md"
OUT = HERE.parent / "counts.csv"
ROW = re.compile(r"^\s{2}(\S+)\s+(\d+)\s+(\d+)\s*$")

fence = REC.read_text(encoding="utf-8").split("## Answer", 1)[1]
fence = fence.split("```text", 1)[1].split("```", 1)[0]

rows, bad = [], []
for line in fence.splitlines():
    # `line.split()[0] == "board"`, NOT `"board" in line`. The substring form
    # matched the DATA row for `BoardSkillBoard-260722` and dropped it, and the
    # skip path is silent by design, so the table shipped two rows instead of
    # three and the totals were wrong with no error. Exactly the failure the
    # strict parse below exists to stop, arriving through the one door that
    # bypasses it.
    if not line.strip() or set(line.strip()) <= set("- ") or line.split()[0] == "board":
        continue
    m = ROW.match(line)
    (rows if m else bad).append(m.groups() if m else line)

if bad:
    print("MALFORMED ROWS, refusing to write a short table:", file=sys.stderr)
    for line in bad:
        print(f"  {line!r}", file=sys.stderr)
    sys.exit(1)

OUT.write_text("board,pages,typed\n"
               + "\n".join(",".join(r) for r in rows) + "\n", encoding="utf-8")
print(f"{len(rows)} rows -> {OUT.name} "
      f"({sum(int(r[1]) for r in rows)} pages, {sum(int(r[2]) for r in rows)} typed)")
