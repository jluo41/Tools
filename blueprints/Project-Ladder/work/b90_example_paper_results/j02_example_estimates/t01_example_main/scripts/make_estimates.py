"""Placeholder worker: the main association, made up for the work theme's example Block.

Reads the source Run named by the Block's src/inputs.yaml (key r01_source) for the sample size, and writes into
RESULT_DIR (set by the Run's ticket) values.csv, one row per value Paper-Example prints (key, value, unit, text,
source), and headline.txt. Every number is made up; the estimates are fixed placeholders, not fitted.
"""
from __future__ import annotations

import csv
import os
from pathlib import Path

import yaml

ESTIMATES = [("main.b", 2.3461, "points", "2.35 (95% CI, 0.84 to 3.85)"),
             ("main.ci_lo", 0.8412, "points", ""),
             ("main.ci_hi", 3.8519, "points", ""),
             ("main.p", 0.0021, "", ""),
             ("sub.b", 4.1234, "points", ""),
             ("mean.before", 41.27, "points", ""),
             ("mean.after", 43.62, "points", ""),
             ("extra.sd", 9.87, "points", "")]


def main() -> None:
    res = Path(os.environ["RESULT_DIR"])
    block = Path(__file__).resolve().parents[3]
    work = block.parent
    source = yaml.safe_load((block / "src" / "inputs.yaml").read_text(encoding="utf-8"))["runs"]["r01_source"]
    with (work / source["path"] / "result" / "tables.csv").open(encoding="utf-8") as f:
        units = next(int(r["rows"]) for r in csv.DictReader(f) if r["table"] == "units")
    rows = [("sample.n_units", units, "units", "")] + ESTIMATES
    with (res / "values.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["key", "value", "unit", "text", "source"])
        w.writerows([key, value, unit, text, "r01_source:tables.csv"] for key, value, unit, text in rows)
    (res / "headline.txt").write_text(f"{len(rows)} values; the main association is 2.35 points (95% CI, 0.84 to 3.85)\n",
                                      encoding="utf-8")


if __name__ == "__main__":
    main()
