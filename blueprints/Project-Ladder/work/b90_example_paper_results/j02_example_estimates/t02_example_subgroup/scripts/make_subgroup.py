"""Placeholder worker: the association in <the subgroup>, made up for the work theme's example Block.

Writes into RESULT_DIR (set by the Run's ticket) values.csv (key, value, unit, text, source) and headline.txt.
Every number is made up; the estimates are fixed placeholders, not fitted. sub.b is the same value the main Task returns.
"""
from __future__ import annotations

import csv
import os
from pathlib import Path

ROWS = [("sub.n_units", 3120, "units", ""),
        ("sub.b", 4.1234, "points", "4.12 (95% CI, 1.20 to 7.05)"),
        ("sub.ci_lo", 1.2034, "points", ""),
        ("sub.ci_hi", 7.0451, "points", "")]


def main() -> None:
    res = Path(os.environ["RESULT_DIR"])
    with (res / "values.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["key", "value", "unit", "text", "source"])
        w.writerows([key, value, unit, text, "r01_source:tables.csv"] for key, value, unit, text in ROWS)
    (res / "headline.txt").write_text("4 values; in <the subgroup> the association is 4.12 points (95% CI, 1.20 to 7.05)\n",
                                      encoding="utf-8")


if __name__ == "__main__":
    main()
