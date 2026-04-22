"""Excalidraw element builders + grid/table primitives for the inventory catalogs.

Each inventory folder (1-data, 2-model, 3-evaluation) has its own  build.py  that
imports from here and emits one or more .excalidraw files.  Common pattern:

    from inventory._shared.helpers import (
        Grid, Table, status_cell, mk_title, mk_legend,
        mk_timestamp, write_excalidraw,
    )

    elems = []
    elems += mk_title(...)
    elems += Grid(rows=..., cols=..., status=...).draw(x=..., y=...)
    elems += mk_legend(...)
    write_excalidraw("out.excalidraw", elems)

Colour palette matches the existing  training_grid.png  so all catalog figures share
one visual vocabulary (green ✓, orange ?, yellow in-progress, blank gray).
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

# ── colours (match training_grid) ──────────────────────────────────────────────

COLOR_DONE         = "#a7f3d0"   # green-200
COLOR_GAP          = "#fed7aa"   # orange-200
COLOR_IN_PROGRESS  = "#fde68a"   # yellow-200 — dir exists, not yet saved
COLOR_BLANK        = "#f3f4f6"   # pale gray
COLOR_ROW_HEADER   = "#ffffff"
COLOR_COL_HEADER   = "#ffffff"
COLOR_PHASE1_BOX   = "#1e40af"   # blue ring around phase-1 row

GLYPH_DONE         = "✓"
GLYPH_GAP          = "?"
GLYPH_IN_PROGRESS  = "…"

# status → (fill colour, glyph, glyph-colour)
STATUS_STYLE: dict[str, tuple[str, str, str]] = {
    "done":        (COLOR_DONE,        GLYPH_DONE,        "#047857"),
    "gap":         (COLOR_GAP,         GLYPH_GAP,         "#c2410c"),
    "in_progress": (COLOR_IN_PROGRESS, GLYPH_IN_PROGRESS, "#a16207"),
    "blank":       (COLOR_BLANK,       "",                "#9ca3af"),
}


# ── primitive element builders ─────────────────────────────────────────────────

def _seed(n: int) -> int:
    """Deterministic seed; any small int works for excalidraw."""
    return 100_000 + n


def mk_text(
    elem_id: str, x: float, y: float, w: float, h: float, text: str,
    *, size: int = 14, color: str = "#111827", align: str = "left",
    weight: str = "normal", seed: int = 0,
) -> dict:
    return {
        "type": "text", "id": elem_id,
        "x": x, "y": y, "width": w, "height": h,
        "text": text, "originalText": text,
        "fontSize": size, "fontFamily": 3,
        "textAlign": align, "verticalAlign": "middle",
        "strokeColor": color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid",
        "roughness": 0, "opacity": 100, "angle": 0,
        "seed": _seed(seed), "version": 1, "versionNonce": _seed(seed) + 1,
        "isDeleted": False, "groupIds": [], "boundElements": None,
        "link": None, "locked": False, "containerId": None, "lineHeight": 1.2,
        "bold": weight == "bold",
    }


def mk_rect(
    elem_id: str, x: float, y: float, w: float, h: float,
    *, fill: str = COLOR_BLANK, stroke: str = "#cbd5e1",
    stroke_width: int = 1, seed: int = 0,
) -> dict:
    return {
        "type": "rectangle", "id": elem_id,
        "x": x, "y": y, "width": w, "height": h,
        "strokeColor": stroke, "backgroundColor": fill,
        "fillStyle": "solid", "strokeWidth": stroke_width, "strokeStyle": "solid",
        "roughness": 0, "opacity": 100, "angle": 0,
        "seed": _seed(seed), "version": 1, "versionNonce": _seed(seed) + 1,
        "isDeleted": False, "groupIds": [], "boundElements": None,
        "link": None, "locked": False,
    }


# ── grid primitive ─────────────────────────────────────────────────────────────

@dataclass
class Grid:
    """A status grid with row + column labels.

    status[i][j] ∈ {"done", "gap", "in_progress", "blank"}.
    Optional  cell_text[i][j]  overrides the default glyph per cell.
    """
    row_labels: list[str]
    col_labels: list[str]
    status: list[list[str]]
    cell_text: list[list[str]] | None = None
    title: str | None = None
    row_label_w: int = 140
    col_label_h: int = 24
    cell_w: int = 40
    cell_h: int = 28
    phase1_row_idx: int | None = None   # row to box in blue (e.g. "P1: D=511M, ep=1")
    id_prefix: str = "grid"

    def size(self) -> tuple[int, int]:
        """Total drawn width, height (excluding title)."""
        n_rows = len(self.row_labels)
        n_cols = len(self.col_labels)
        w = self.row_label_w + n_cols * self.cell_w
        h = self.col_label_h + n_rows * self.cell_h
        return w, h

    def draw(self, x0: float, y0: float, seed_base: int = 0) -> list[dict]:
        elems: list[dict] = []
        n_rows, n_cols = len(self.row_labels), len(self.col_labels)
        cx0 = x0 + self.row_label_w          # first cell starts here horizontally
        cy0 = y0 + self.col_label_h          # first cell starts here vertically

        # optional title above the grid
        if self.title:
            elems.append(mk_text(
                f"{self.id_prefix}_title",
                x0, y0 - 26, self.row_label_w + n_cols * self.cell_w, 20,
                self.title, size=14, color="#1f2937", weight="bold",
                align="left", seed=seed_base,
            ))

        # column labels (sizes / epochs / etc.)
        for j, col in enumerate(self.col_labels):
            elems.append(mk_text(
                f"{self.id_prefix}_col_{j}",
                cx0 + j * self.cell_w, y0, self.cell_w, self.col_label_h,
                col, size=11, color="#374151", align="center",
                seed=seed_base + j + 1,
            ))

        # row labels
        for i, row in enumerate(self.row_labels):
            elems.append(mk_text(
                f"{self.id_prefix}_row_{i}",
                x0, cy0 + i * self.cell_h, self.row_label_w, self.cell_h,
                row, size=11, color="#374151", align="left",
                seed=seed_base + n_cols + i + 1,
            ))

        # cells
        for i in range(n_rows):
            for j in range(n_cols):
                st = self.status[i][j]
                fill, glyph, glyph_color = STATUS_STYLE.get(st, STATUS_STYLE["blank"])
                cx = cx0 + j * self.cell_w
                cy = cy0 + i * self.cell_h
                elems.append(mk_rect(
                    f"{self.id_prefix}_cell_{i}_{j}",
                    cx, cy, self.cell_w, self.cell_h,
                    fill=fill, seed=seed_base + 1000 + i * n_cols + j,
                ))
                txt = (self.cell_text[i][j] if self.cell_text else None) or glyph
                if txt:
                    elems.append(mk_text(
                        f"{self.id_prefix}_glyph_{i}_{j}",
                        cx, cy, self.cell_w, self.cell_h,
                        txt, size=14, color=glyph_color, align="center",
                        weight="bold", seed=seed_base + 2000 + i * n_cols + j,
                    ))

        # phase-1 row highlight box
        if self.phase1_row_idx is not None:
            cy = cy0 + self.phase1_row_idx * self.cell_h
            elems.append(mk_rect(
                f"{self.id_prefix}_p1_box",
                x0 - 2, cy - 2,
                self.row_label_w + n_cols * self.cell_w + 4, self.cell_h + 4,
                fill="transparent", stroke=COLOR_PHASE1_BOX, stroke_width=2,
                seed=seed_base + 9999,
            ))

        return elems


# ── text-cell table primitive (for data inventory) ─────────────────────────────

@dataclass
class Table:
    """Plain text table — no status codes, just labels in cells.

    Used for datasets/splits tables where every cell is a literal value.
    First row = headers (bold).  Optional per-row emphasis colour via  row_colors.
    """
    headers: list[str]
    rows: list[list[str]]
    col_widths: list[int] | None = None     # px; defaults to auto (equal)
    row_h: int = 32
    header_h: int = 34
    id_prefix: str = "table"
    row_colors: list[str] | None = None     # fill per row (header excluded)
    title: str | None = None

    def size(self) -> tuple[int, int]:
        w = sum(self._widths())
        h = self.header_h + len(self.rows) * self.row_h
        return w, h

    def _widths(self) -> list[int]:
        if self.col_widths:
            return self.col_widths
        return [140] * len(self.headers)

    def draw(self, x0: float, y0: float, seed_base: int = 0) -> list[dict]:
        elems: list[dict] = []
        widths = self._widths()

        if self.title:
            elems.append(mk_text(
                f"{self.id_prefix}_title",
                x0, y0 - 26, sum(widths), 20,
                self.title, size=14, color="#1f2937", weight="bold",
                seed=seed_base,
            ))

        # header row
        cx = x0
        for j, (h, w) in enumerate(zip(self.headers, widths)):
            elems.append(mk_rect(
                f"{self.id_prefix}_hdr_{j}", cx, y0, w, self.header_h,
                fill="#e5e7eb", stroke="#94a3b8", seed=seed_base + j + 1,
            ))
            elems.append(mk_text(
                f"{self.id_prefix}_hdr_t_{j}", cx, y0, w, self.header_h,
                h, size=12, color="#111827", align="center", weight="bold",
                seed=seed_base + 100 + j,
            ))
            cx += w

        # data rows
        for i, row in enumerate(self.rows):
            cy = y0 + self.header_h + i * self.row_h
            row_fill = (self.row_colors[i] if self.row_colors else None) or "#ffffff"
            cx = x0
            for j, (val, w) in enumerate(zip(row, widths)):
                elems.append(mk_rect(
                    f"{self.id_prefix}_r{i}_c{j}", cx, cy, w, self.row_h,
                    fill=row_fill, stroke="#cbd5e1",
                    seed=seed_base + 200 + i * len(row) + j,
                ))
                elems.append(mk_text(
                    f"{self.id_prefix}_r{i}_c{j}_t", cx + 6, cy, w - 12, self.row_h,
                    val, size=11, color="#1f2937", align="left",
                    seed=seed_base + 500 + i * len(row) + j,
                ))
                cx += w

        return elems


# ── convenience blocks ─────────────────────────────────────────────────────────

def mk_title(x: float, y: float, w: float, text: str, *, subtitle: str | None = None,
             seed: int = 0) -> list[dict]:
    out = [mk_text("title", x, y, w, 28, text,
                   size=20, color="#1e40af", weight="bold", seed=seed)]
    if subtitle:
        out.append(mk_text("subtitle", x, y + 30, w, 18, subtitle,
                           size=12, color="#64748b", seed=seed + 1))
    return out


def mk_legend(x: float, y: float, *, compact: bool = False, seed: int = 0) -> list[dict]:
    """A three-swatch legend explaining the status colours."""
    items = [
        (COLOR_DONE,        GLYPH_DONE,        "#047857", "trained / done"),
        (COLOR_IN_PROGRESS, GLYPH_IN_PROGRESS, "#a16207", "in progress"),
        (COLOR_GAP,         GLYPH_GAP,         "#c2410c", "gap — should do"),
        (COLOR_BLANK,       "",                "#9ca3af", "not in plan"),
    ]
    sw, sh = (14, 14) if compact else (20, 20)
    gap = 6
    label_w = 120
    elems: list[dict] = []
    cursor = x
    for k, (fill, glyph, gcol, label) in enumerate(items):
        elems.append(mk_rect(f"leg_sw_{k}", cursor, y, sw, sh, fill=fill,
                             seed=seed + k))
        if glyph:
            elems.append(mk_text(f"leg_gl_{k}", cursor, y, sw, sh, glyph,
                                 size=11, color=gcol, align="center", weight="bold",
                                 seed=seed + 100 + k))
        elems.append(mk_text(f"leg_lb_{k}", cursor + sw + 4, y - 1, label_w, sh + 2,
                             label, size=11, color="#374151", seed=seed + 200 + k))
        cursor += sw + 4 + label_w + gap
    return elems


def mk_timestamp(x: float, y: float, seed: int = 0) -> list[dict]:
    stamp = f"Rendered: {time.strftime('%Y-%m-%d %H:%M:%S %Z')}"
    return [mk_text("stamp", x, y, 300, 18, stamp,
                    size=11, color="#9ca3af", align="right", seed=seed + 999)]


# ── save .excalidraw ───────────────────────────────────────────────────────────

def write_excalidraw(path: str | Path, elements: Iterable[dict],
                     files: dict | None = None,
                     app_bg: str = "#ffffff") -> Path:
    path = Path(path)
    doc = {
        "type": "excalidraw",
        "version": 2,
        "source": "https://excalidraw.com",
        "elements": list(elements),
        "appState": {
            "gridSize": None,
            "viewBackgroundColor": app_bg,
        },
        "files": files or {},
    }
    path.write_text(json.dumps(doc, indent=2))
    return path
