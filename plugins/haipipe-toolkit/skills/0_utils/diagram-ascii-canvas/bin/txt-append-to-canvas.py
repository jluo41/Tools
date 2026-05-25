#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["playwright"]
# ///
"""
Append ONE .txt as a new rightmost column to an existing .excalidraw canvas.

Use when you want to add a new session-log .txt to a daily canvas while
preserving prior columns AND any manual annotations (arrows, sticky notes,
re-arranged tiles) that you drew in Excalidraw.

Contrast with txt-to-canvas.py which rebuilds the whole canvas from the
.txt files in a folder — that wipes manual edits.

Usage:
    txt-append-to-canvas.py <canvas.excalidraw> <new.txt> [--png-dir DIR]
                            [--col-gutter PX] [--row-gutter PX]
                            [--blank-lines N]

Layout:
    Renders the new .txt's sections as PNGs (same engine as txt-to-canvas).
    Finds the rightmost x+width across all existing image+text elements,
    places the new column at that edge + col-gutter. Top-aligns to the
    minimum y of existing elements (so the new column starts at the same
    "row 0" as the others).
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

# Reuse rendering + element-building helpers from the rebuild script.
_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
from txt_to_canvas_lib import (  # type: ignore  # noqa: E402
    make_column_elements,
    render_sections_to_pngs,
)


def existing_extent(elements: list[dict]) -> tuple[int, int, int]:
    """Return (right_edge_x, top_y, max_x_of_visible_content).

    Considers only elements with positive width (skips deleted/zero-size).
    Falls back to (0, 0, 0) if the canvas is empty.
    """
    if not elements:
        return 0, 0, 0
    xs_right: list[int] = []
    ys_top: list[int] = []
    for el in elements:
        if el.get("isDeleted"):
            continue
        x = el.get("x", 0) or 0
        y = el.get("y", 0) or 0
        w = el.get("width", 0) or 0
        xs_right.append(int(x + w))
        ys_top.append(int(y))
    if not xs_right:
        return 0, 0, 0
    return max(xs_right), min(ys_top), max(xs_right)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("canvas", help="Existing .excalidraw file to append to")
    ap.add_argument("txt", help="New .txt file to render and append as a column")
    ap.add_argument("--png-dir", help="Where to put intermediate PNGs (default: <canvas-dir>/_pngs)")
    ap.add_argument("--col-gutter", type=int, default=300,
                    help="Horizontal gap before the new column (default 300)")
    ap.add_argument("--row-gutter", type=int, default=50,
                    help="Vertical gap between sections (default 50)")
    ap.add_argument("--blank-lines", type=int, default=0,
                    help="Fallback split only when no `─§` markers (default 0)")
    args = ap.parse_args()

    canvas_path = Path(args.canvas).resolve()
    txt_path = Path(args.txt).resolve()
    if not canvas_path.is_file():
        print(f"canvas not found: {canvas_path}", file=sys.stderr)
        sys.exit(1)
    if not txt_path.is_file() or txt_path.suffix != ".txt":
        print(f"not a .txt file: {txt_path}", file=sys.stderr)
        sys.exit(1)

    # Load existing canvas.
    doc = json.loads(canvas_path.read_text(encoding="utf-8"))
    elements: list[dict] = list(doc.get("elements", []))
    files: dict[str, dict] = dict(doc.get("files", {}))

    # Find the right edge of existing content; new column starts at edge + gutter.
    right_edge, top_y, _ = existing_extent(elements)
    start_x = right_edge + args.col_gutter if elements else 0
    start_y = top_y if elements else 0

    # Render new .txt → PNGs.
    png_dir = Path(args.png_dir) if args.png_dir else canvas_path.parent / "_pngs"
    print(
        f"[1/3] rendering {txt_path.name} -> sections -> PNG in {png_dir}",
        file=sys.stderr,
    )
    items = render_sections_to_pngs([txt_path], png_dir, blank_lines=args.blank_lines)
    if not items:
        print(f"no sections rendered from {txt_path}", file=sys.stderr)
        sys.exit(1)

    # Build new column elements (image + section-title text + file-header text).
    # Use a unique col_idx so element IDs don't collide with anything previously
    # produced by txt-to-canvas (those use 000..N from the rebuild run; here we
    # tag with a timestamp suffix to guarantee uniqueness across appends).
    suffix = time.strftime("%y%m%d-%H%M%S")
    new_elements, new_files = make_column_elements(
        txt_path=txt_path,
        section_items=[(i, t, p) for (_t, i, t, p) in items],
        x=start_x,
        y=start_y,
        col_id_suffix=suffix,
        row_gutter=args.row_gutter,
    )

    print(
        f"[2/3] appending column at x={start_x} (right edge was {right_edge}) — "
        f"{len(new_elements)} new elements, {len(new_files)} new images",
        file=sys.stderr,
    )

    elements.extend(new_elements)
    files.update(new_files)
    doc["elements"] = elements
    doc["files"] = files

    canvas_path.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        f"[3/3] wrote {canvas_path}  "
        f"({len(elements)} total elements, {len(files)} total images)",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
