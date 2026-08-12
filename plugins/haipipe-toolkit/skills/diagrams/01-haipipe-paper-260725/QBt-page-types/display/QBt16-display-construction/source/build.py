#!/usr/bin/env python3
"""Build three display candidates from one existing QBt5 Value-bank output."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
UNIT = HERE.parent
GROUP = UNIT.parents[1]
BANK = GROUP / "QA-probe/QBt5-for-value/1-artifact-paths.data/counts.csv"
CANDIDATES = UNIT / "candidates"
STYLE = GROUP / "display/QBt3-for-display/source"

sys.path.insert(0, str(STYLE))
from paper_plot_style import plt  # noqa: E402


def read_rows() -> list[dict[str, int | str]]:
    with BANK.open(newline="", encoding="utf-8") as handle:
        raw = list(csv.DictReader(handle))
    required = {"contract", "paths", "lines"}
    if not raw or not required.issubset(raw[0]):
        missing = sorted(required - (set(raw[0]) if raw else set()))
        raise SystemExit(f"bank input is empty or missing columns: {missing}")
    rows = [
        {"contract": row["contract"], "paths": int(row["paths"]), "lines": int(row["lines"])}
        for row in raw
    ]
    if len({row["contract"] for row in rows}) != len(rows):
        raise SystemExit("bank input contains duplicate contract names")
    return rows


def save(fig, stem: str) -> None:
    CANDIDATES.mkdir(parents=True, exist_ok=True)
    for extension in ("png", "pdf"):
        fig.savefig(CANDIDATES / f"{stem}.{extension}")
    plt.close(fig)


def ranked_bars(rows: list[dict[str, int | str]]) -> None:
    ordered = sorted(rows, key=lambda row: (int(row["paths"]), str(row["contract"])))
    fig, axis = plt.subplots(figsize=(7.4, 4.3))
    y = list(range(len(ordered)))
    values = [int(row["paths"]) for row in ordered]
    colors = ["#b3402f" if value == max(values) else "#8795a1" for value in values]
    axis.barh(y, values, color=colors, height=0.66)
    axis.set_yticks(y, [str(row["contract"]) for row in ordered])
    axis.set_xlabel("Artifact-path mentions in the contract")
    axis.set_xlim(0, max(values) + 1.8)
    axis.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    for index, value in enumerate(values):
        axis.text(value + 0.15, index, str(value), va="center", fontsize=9)
    axis.spines["left"].set_visible(False)
    axis.tick_params(axis="y", length=0)
    fig.tight_layout()
    save(fig, "A-ranked-bars")


def paths_vs_lines(rows: list[dict[str, int | str]]) -> None:
    fig, axis = plt.subplots(figsize=(7.4, 4.6))
    x = [int(row["lines"]) for row in rows]
    y = [int(row["paths"]) for row in rows]
    axis.scatter(x, y, s=46, color="#526d82", edgecolor="white", linewidth=0.7, zorder=3)
    offsets = {
        "display": (5, 5),
        "literature": (5, -13),
        "value": (5, 5),
        "section": (5, 5),
        "design": (5, 5),
    }
    for row in rows:
        dx, dy = offsets.get(str(row["contract"]), (5, 5))
        axis.annotate(str(row["contract"]), (int(row["lines"]), int(row["paths"])),
                      xytext=(dx, dy), textcoords="offset points", fontsize=7.8)
    axis.set_xlabel("Contract length, source lines")
    axis.set_ylabel("Artifact-path mentions")
    axis.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    axis.grid(axis="both", color="#d9e2ec", linewidth=0.6, zorder=0)
    fig.tight_layout()
    save(fig, "B-paths-vs-lines")


def audit_table(rows: list[dict[str, int | str]]) -> None:
    ordered = sorted(rows, key=lambda row: str(row["contract"]))
    fig, axis = plt.subplots(figsize=(6.2, 4.5))
    axis.axis("off")
    cells = [[str(row["contract"]), str(row["paths"]), str(row["lines"])] for row in ordered]
    table = axis.table(
        cellText=cells,
        colLabels=["Contract", "Path mentions", "Source lines"],
        colLoc="left",
        cellLoc="left",
        loc="center",
        colWidths=[0.48, 0.24, 0.22],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 1.35)
    for (row_index, _), cell in table.get_celld().items():
        cell.set_edgecolor("#cbd5e1")
        cell.set_linewidth(0.6)
        if row_index == 0:
            cell.set_facecolor("#e5e9ef")
            cell.set_text_props(weight="bold")
    fig.tight_layout()
    save(fig, "C-audit-table")


def main() -> None:
    rows = read_rows()
    ranked_bars(rows)
    paths_vs_lines(rows)
    audit_table(rows)
    print(f"{len(rows)} bank rows -> 3 candidates -> {CANDIDATES}")


if __name__ == "__main__":
    main()
