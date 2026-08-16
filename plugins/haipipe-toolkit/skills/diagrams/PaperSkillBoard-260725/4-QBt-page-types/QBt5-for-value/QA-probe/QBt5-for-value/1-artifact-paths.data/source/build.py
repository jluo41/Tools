#!/usr/bin/env python3
"""Parse the record's ## Answer fence into counts.csv. Never retype a number.

The record is the one place the numbers are typed; this turns that fence into
the machine-readable form everything downstream reads. The parse is STRICT on
purpose: every non-rule line inside the fence must match, or it exits 1. A
lenient parser that skipped a malformed row would silently ship a short table,
and the whole reason the numbers live in exactly one place is so that cannot
happen.

    python3 build.py     ->  ../counts.csv
"""
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
# EXTRACT FROM THE BANK, not from the probe. The probe holds the binding and
# a digest; the answer is the executor's and lives in its own tree. Reading
# the probe made this record the original, which is the twin law backwards.
REC = HERE.parents[3] / "_bank/tasks/A01_page-type-contracts/QA/1-artifact-paths.md"
OUT = HERE.parent / "counts.csv"
ROW = re.compile(r"^\s{2}([a-z]+)\s+(\d+)\s+(\d+)\s*$")

fence = REC.read_text(encoding="utf-8").split("## Answer", 1)[1]
fence = fence.split("```text", 1)[1].split("```", 1)[0]

rows, bad = [], []
for line in fence.splitlines():
    if not line.strip() or set(line.strip()) <= set("- ") or "contract" in line:
        continue
    m = ROW.match(line)
    if not m:
        bad.append(line)
        continue
    rows.append(m.groups())

if bad:
    print("MALFORMED ROWS, refusing to write a short table:", file=sys.stderr)
    for line in bad:
        print(f"  {line!r}", file=sys.stderr)
    sys.exit(1)

OUT.write_text("contract,paths,lines\n"
               + "\n".join(",".join(r) for r in rows) + "\n", encoding="utf-8")
print(f"{len(rows)} rows -> {OUT.name} "
      f"({sum(int(r[1]) for r in rows)} paths, "
      f"{sum(1 for r in rows if r[1] == '0')} contracts naming none)")
