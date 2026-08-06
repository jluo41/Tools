#!/usr/bin/env python3
"""Extract this record's product from the answer it holds.

🚫 FABRICATED input.

This record is `route: local`: the answer was produced here, so there is no bank
elsewhere and the table above is the original. The script parses that table.

On a `task` or `discovery` route the only line that changes is SOURCE below: it
becomes the path in the record's `- bank:` key, and the parse runs against the
bank in its own tree. The bank is never copied into the paper, so this script
reads across rather than reading a local copy.

The parse is strict on purpose, and strict means every line inside the fence must
match. Matching only the lines that happen to parse is not strict, it is silent:
one mistyped digit turns a band into no band and the figure ships one bar short
with exit code 0. Proven 260806 by changing `48` to `4B` and watching it pass.
"""
import csv
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
DATA = HERE.parent                                    # 1-drift-counts.data/
RECORD = DATA.parent / (DATA.name[: -len(".data")] + ".md")
GROUP = DATA.parents[2]                               # the QBt group folder
OUT = DATA / "counts.csv"

COLUMNS = ["band", "pages", "drift_events", "ci_low", "ci_high"]
ROW = re.compile(
    r"^\s{2}(?P<band>\S.*?)\s{2,}"
    r"(?P<pages>\d+)\s+(?P<drift_events>\d+)\s+"
    r"(?P<ci_low>[\d.]+)\s+(?P<ci_high>[\d.]+)\s*$"
)
BANK_KEY = re.compile(r"^-\s*bank:\s*(\S+)\s*$", re.M)


def source_file():
    """Where the answer table actually is: this record, or the bank it binds to."""
    m = BANK_KEY.search(RECORD.read_text())
    if not m:
        return RECORD                       # route: local, this file is the original
    path = (GROUP / m.group(1)).resolve()
    if not path.exists():
        raise SystemExit(
            f"{RECORD.name} binds to a bank that is not reachable from here:\n"
            f"    {m.group(1)}\n"
            "  Clone the executor tree, or set route: local if the answer is produced here.")
    return path


FENCE = re.compile(r"```text\n(.*?)```", re.S)
SKIP = re.compile(r"^\s*$|^\s*[─-]+\s*$|^\s{2}band\b")


def table_rows(bank):
    """Every data line inside the bank's answer table, or a loud failure.

    Matching only the lines that happen to parse is not strict, it is silent: a
    single mistyped digit turns one band into no band and the figure ships one
    bar short with exit code 0. Proven 260806 by changing `48` to `4B` in the
    bank and watching the build succeed. So the fence is located first, and then
    EVERY line inside it must either be skippable or parse.
    """
    m = FENCE.search(bank.read_text())
    if not m:
        raise SystemExit(f"{bank.name}: no ```text table found in the answer")
    rows, bad = [], []
    for line in m.group(1).splitlines():
        if SKIP.match(line):
            continue
        hit = ROW.match(line)
        if hit:
            rows.append({c: hit.group(c).strip() for c in COLUMNS})
        else:
            bad.append(line)
    if bad:
        raise SystemExit(
            f"{bank.name}: {len(bad)} line(s) in the answer table did not parse.\n"
            + "\n".join(f"    {b}" for b in bad)
            + "\n  Fix the bank, or the extract silently ships fewer rows than the answer states.")
    if not rows:
        raise SystemExit(f"{bank.name}: the answer table has no data rows")
    return rows


if __name__ == "__main__":
    bank = source_file()
    rows = table_rows(bank)
    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)
    where = bank.name if bank == RECORD else bank
    print(f"{len(rows)} rows extracted from {where} -> {OUT.name}")
