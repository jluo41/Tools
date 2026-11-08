"""Placeholder worker: the source tables a server returns, made up for the work theme's example Block.

Writes into RESULT_DIR (set by the Run's ticket): tables.csv (one row per source table and its row count),
maps/source.mindmap.md (the source tables as a mind map, which the Block's Findings shows under Maps) and headline.txt.
Every number is made up; nothing is read from any real data.
"""
from __future__ import annotations

import csv
import os
from pathlib import Path

TABLES = [("units", 12480, "one row per unit, the analysis sample"),
          ("visits", 48210, "one row per visit of a unit"),
          ("outcomes", 12480, "one outcome row per unit, before and after")]


def main() -> None:
    res = Path(os.environ["RESULT_DIR"])
    with (res / "tables.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["table", "rows"])
        w.writerow([TABLES[0][0], TABLES[0][1]])     # the paper's value Tasks read units only; the others are below
    with (res / "all_tables.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["table", "rows", "what"])
        w.writerows(TABLES)
    (res / "maps").mkdir(exist_ok=True)
    lines = ["---", "mindmap: 1", "title: The returned source tables", "built: make_source.py", "---", "",
             "# The returned source tables", "", "Three tables: one row per unit, per visit and per outcome.", ""]
    for name, rows, what in TABLES:
        lines += [f"- {name}", f"  - {what}", f"  - {rows:,} rows"]
    (res / "maps" / "source.mindmap.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (res / "headline.txt").write_text(f"{len(TABLES)} source tables; the sample holds {TABLES[0][1]:,} units\n",
                                      encoding="utf-8")


if __name__ == "__main__":
    main()
