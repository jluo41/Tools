"""Placeholder worker: checks of the returned source tables, for the work theme's example Block.

Reads the source Run's all_tables.csv (j01_example_source/t01_example_source, Run r01_example_source) and writes into
RESULT_DIR (set by the Run's ticket) checks.csv (check, value, ok) and headline.txt. The checks are fixed placeholders:
units and outcomes hold one row per unit, and visits hold at least one row per unit. Nothing real is read.
"""
from __future__ import annotations

import csv
import os
from pathlib import Path

SOURCE = Path("t01_example_source/runs/r01_example_source/result/all_tables.csv")   # from the Job folder


def main() -> None:
    res = Path(os.environ["RESULT_DIR"])
    job = Path(__file__).resolve().parents[2]
    with (job / SOURCE).open(encoding="utf-8") as f:
        rows = {r["table"]: int(r["rows"]) for r in csv.DictReader(f)}
    checks = [("outcomes per unit", rows["outcomes"] / rows["units"], rows["outcomes"] == rows["units"]),
              ("visits per unit", rows["visits"] / rows["units"], rows["visits"] >= rows["units"])]
    with (res / "checks.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["check", "value", "ok"])
        w.writerows([name, f"{value:.2f}", "yes" if ok else "no"] for name, value, ok in checks)
    passed = sum(ok for _, _, ok in checks)
    (res / "headline.txt").write_text(f"{passed} of {len(checks)} source checks pass\n", encoding="utf-8")


if __name__ == "__main__":
    main()
