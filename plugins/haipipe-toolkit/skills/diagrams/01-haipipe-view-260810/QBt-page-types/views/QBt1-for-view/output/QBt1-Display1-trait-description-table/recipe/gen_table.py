#!/usr/bin/env python3
"""Regenerate the promoted LaTeX table body from the approved intake snapshot."""

from __future__ import annotations

import csv
import pathlib


UNIT = pathlib.Path(__file__).resolve().parent.parent
SOURCE = UNIT / "intake" / "inputs" / "source_data.csv"
TARGET = UNIT / "assets" / "table.tex"


def escape(value: str) -> str:
    return value.replace("&", r"\&").replace("%", r"\%")


with SOURCE.open(encoding="utf-8", newline="") as handle:
    rows = list(csv.DictReader(handle))

lines = [
    r"\begin{tabularx}{\linewidth}{@{}p{0.16\linewidth}X p{0.12\linewidth}p{0.22\linewidth}@{}}",
    r"\toprule",
    r"Layer & What the View says & Evidence & Boundary \\",
    r"\midrule",
]
for row in rows:
    lines.append(" & ".join(escape(row[key]) for key in row) + r" \\")
lines.extend([r"\bottomrule", r"\end{tabularx}"])
TARGET.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(TARGET)
