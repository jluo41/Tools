#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["playwright"]
# ///
"""
Bundle a folder of ASCII .txt diagrams into one .excalidraw canvas.

- Each .txt is split into sections (default: on `─§ Title ─` markers; opt-in
  blank-line fallback for marker-less files).
- Each section is screenshotted as a PNG via headless Chromium (color emoji +
  monospace).
- All PNGs are embedded into one Excalidraw file, laid out as a grid: one
  column per source .txt, sections stacked top→bottom inside each column.

This script REBUILDS the canvas from scratch every run. If you want to add
ONE new .txt while keeping prior columns and any manual annotations you
drew in Excalidraw, use `txt-append-to-canvas.py` instead.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
from txt_to_canvas_lib import (  # type: ignore  # noqa: E402
    make_excalidraw_from_items,
    render_sections_to_pngs,
)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("inputs", nargs="+", help="A directory or one-or-more .txt files")
    ap.add_argument("--out", help="Output .excalidraw path (default: <dir>/canvas-YYMMDD.excalidraw)")
    ap.add_argument("--col-gutter", type=int, default=300,
                    help="Horizontal gap between file columns in px (default 300)")
    ap.add_argument("--row-gutter", type=int, default=50,
                    help="Vertical gap between sections within a column in px (default 50)")
    ap.add_argument("--png-dir", help="Where to put intermediate PNGs (default: <dir>/_pngs)")
    ap.add_argument(
        "--blank-lines", type=int, default=0,
        help=("Fallback only — used when a file has NO `─§` markers. Split that "
              "file at runs of this many+ consecutive blank lines. Default 0 "
              "(no fallback: marker-less files render as one PNG)."),
    )
    args = ap.parse_args()

    paths = [Path(p) for p in args.inputs]
    if len(paths) == 1 and paths[0].is_dir():
        base = paths[0]
        txts = sorted(base.glob("*.txt"))
        if not txts:
            print(f"no .txt found in {base}", file=sys.stderr)
            sys.exit(1)
    else:
        txts = sorted(p for p in paths if p.suffix == ".txt" and p.is_file())
        if not txts:
            print("no .txt files in arguments", file=sys.stderr)
            sys.exit(1)
        base = txts[0].parent

    date_tag = time.strftime("%y%m%d")
    out = Path(args.out) if args.out else base / f"canvas-{date_tag}.excalidraw"
    png_dir = Path(args.png_dir) if args.png_dir else base / "_pngs"

    print(
        f"[1/3] rendering {len(txts)} .txt -> sections -> PNG in {png_dir} "
        f"(marker=─§, blank-line fallback={args.blank_lines})",
        file=sys.stderr,
    )
    items = render_sections_to_pngs(txts, png_dir, blank_lines=args.blank_lines)

    n_files = len({txt for txt, *_ in items})
    print(
        f"[2/3] assembling Excalidraw — {n_files} columns (one per file), "
        f"{len(items)} sections total",
        file=sys.stderr,
    )
    doc = make_excalidraw_from_items(
        items, col_gutter=args.col_gutter, row_gutter=args.row_gutter
    )

    out.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        f"[3/3] wrote {out}  "
        f"({len(doc['elements'])} elements, {len(doc['files'])} images)",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
