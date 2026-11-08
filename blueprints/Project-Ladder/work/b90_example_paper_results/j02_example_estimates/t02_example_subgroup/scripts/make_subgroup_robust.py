"""Placeholder worker: the association in <the subgroup> under a second window, for the work theme's example Block.

Writes into RESULT_DIR (set by the Run's ticket) values.csv (key, value, unit, text, source) and headline.txt, the same
shape the first subgroup Run returns. Every number is made up; the estimates are fixed placeholders, not fitted.
"""
from __future__ import annotations

import csv
import os
from pathlib import Path

ROWS = [("sub_robust.n_units", 2980, "units", ""),
        ("sub_robust.b", 3.9817, "points", "3.98 (95% CI, 0.96 to 7.00)"),
        ("sub_robust.ci_lo", 0.9623, "points", ""),
        ("sub_robust.ci_hi", 7.0011, "points", "")]


def main() -> None:
    res = Path(os.environ["RESULT_DIR"])
    with (res / "values.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["key", "value", "unit", "text", "source"])
        w.writerows([key, value, unit, text, "r01_source:tables.csv"] for key, value, unit, text in ROWS)
    (res / "headline.txt").write_text("4 values; under the second window the subgroup association is 3.98 points\n",
                                      encoding="utf-8")


if __name__ == "__main__":
    main()
