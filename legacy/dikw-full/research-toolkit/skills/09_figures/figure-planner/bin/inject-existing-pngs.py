#!/usr/bin/env python3
"""inject-existing-pngs.py — figure-planner Step 4a.

Reads every `fig-*.txt` sketch in a paper's `0-display/_design/` folder.
For each sketch whose body references an existing PNG via either:
  - a `📌 REAL PNG: <relpath>` marker, or
  - a `📊 File: <paperpath>.png` header field,
embeds that PNG into `canvas.excalidraw` as an image element placed
underneath the matching column's ASCII section(s).

Multi-panel sketches (multiple `📌 REAL PNG: …` markers, e.g. the
appD per-trait-bars composite) inject each panel sequentially.

Usage:
    inject-existing-pngs.py <design-dir-or-canvas.excalidraw>

If passed a directory, looks for `canvas.excalidraw` inside it.
"""
from __future__ import annotations

import base64
import hashlib
import json
import re
import struct
import sys
import time
import uuid
from pathlib import Path

# `📊 File: 0-display/Figure/Fig1-...png` in the .txt header (paper-relative)
TXT_FILE_RE = re.compile(r"^\s*(?:📊\s*)?File:\s+(?P<path>.+\.png)\s*$", re.MULTILINE)
# `📌 REAL PNG: ../Figure/Fig1-...png [optional trailing comment]` (txt-relative)
REAL_PNG_RE = re.compile(r"^\s*📌\s*REAL PNG:\s*(?P<path>\S+\.png)", re.MULTILINE)
GUTTER_Y = 60
LABEL_FONT_SIZE = 20
LABEL_HEIGHT = 30


def png_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as f:
        head = f.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"not a PNG: {path}")
    w, h = struct.unpack(">II", head[16:24])
    return w, h


def sha1_id(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()


def random_id() -> str:
    return uuid.uuid4().hex[:16]


def now_ms() -> int:
    return int(time.time() * 1000)


def sketch_to_pngs(txt_path: Path, design_dir: Path) -> list[Path]:
    """Return all real-result PNG paths referenced by a .txt sketch.

    Priority order:
    1. All `📌 REAL PNG: <relpath>` markers in the body (relative to the
       .txt file's directory). Handles multi-panel sketches naturally —
       each marker becomes one PNG injection.
    2. Fallback: `📊 File: <path>` header line (paper-relative).

    Returns the deduped, existing PNG paths in source order.
    """
    text = txt_path.read_text(encoding="utf-8")
    paper_root = design_dir.parent.parent
    paths: list[Path] = []
    seen: set[Path] = set()
    for m in REAL_PNG_RE.finditer(text):
        raw = m.group("path").strip()
        candidate = (txt_path.parent / raw).resolve()
        if candidate.exists() and candidate not in seen:
            paths.append(candidate)
            seen.add(candidate)
    if paths:
        return paths
    m = TXT_FILE_RE.search(text)
    if m:
        raw = m.group("path").strip()
        candidate = (paper_root / raw).resolve()
        if candidate.exists() and candidate not in seen:
            paths.append(candidate)
    return paths


def column_anchor(canvas: dict, txt_basename: str) -> tuple[float, float, float] | None:
    """Find the bottom-left of the column whose first title text mentions <txt_basename>.

    Returns (x, bottom_y, col_width) or None if not found.
    """
    txts = [e for e in canvas["elements"]
            if e.get("type") == "text" and txt_basename in (e.get("text") or "")]
    if not txts:
        return None
    top_text = min(txts, key=lambda e: e["y"])
    col_x = top_text["x"]
    # collect elements in roughly the same column (x within +/- 50 of col_x)
    col_elements = [e for e in canvas["elements"]
                    if abs(e.get("x", 0) - col_x) < 50]
    bottom = max((e["y"] + e.get("height", 0)) for e in col_elements)
    col_width = max(e.get("width", 0) for e in col_elements if e.get("type") == "image") or 800
    return (col_x, bottom, col_width)


def make_image_element(file_id: str, x: float, y: float, w: float, h: float) -> dict:
    return {
        "id": random_id(),
        "type": "image",
        "x": x,
        "y": y,
        "width": w,
        "height": h,
        "angle": 0,
        "strokeColor": "transparent",
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": 1,
        "strokeStyle": "solid",
        "roughness": 1,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": None,
        "seed": 1,
        "version": 1,
        "versionNonce": 1,
        "isDeleted": False,
        "boundElements": None,
        "updated": now_ms(),
        "link": None,
        "locked": False,
        "fileId": file_id,
        "scale": [1, 1],
        "status": "saved",
        "index": None,
    }


def make_text_element(text: str, x: float, y: float, width: float) -> dict:
    return {
        "id": random_id(),
        "type": "text",
        "x": x,
        "y": y,
        "width": width,
        "height": LABEL_HEIGHT,
        "angle": 0,
        "strokeColor": "#1971c2",
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": 1,
        "strokeStyle": "solid",
        "roughness": 1,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": None,
        "seed": 1,
        "version": 1,
        "versionNonce": 1,
        "isDeleted": False,
        "boundElements": None,
        "updated": now_ms(),
        "link": None,
        "locked": False,
        "text": text,
        "fontSize": LABEL_FONT_SIZE,
        "fontFamily": 3,
        "textAlign": "left",
        "verticalAlign": "top",
        "containerId": None,
        "originalText": text,
        "lineHeight": 1.25,
        "autoResize": True,
    }


def main(arg: str) -> int:
    target = Path(arg).resolve()
    if target.is_dir():
        design_dir = target
        canvas_path = target / "canvas.excalidraw"
    else:
        canvas_path = target
        design_dir = target.parent
    if not canvas_path.exists():
        print(f"ERROR: canvas not found at {canvas_path}", file=sys.stderr)
        return 1
    canvas = json.loads(canvas_path.read_text(encoding="utf-8"))
    canvas.setdefault("files", {})
    canvas.setdefault("elements", [])
    sketches = sorted(design_dir.glob("fig-*.txt"))
    injected = 0
    skipped_no_png = 0
    skipped_no_column = 0
    for sketch in sketches:
        png_paths = sketch_to_pngs(sketch, design_dir)
        if not png_paths:
            skipped_no_png += 1
            continue
        # column key = the .txt's own basename
        txt_basename = sketch.name
        anchor = column_anchor(canvas, txt_basename)
        if anchor is None:
            skipped_no_column += 1
            print(f"  ?  no column for {sketch.name} (expected '{txt_basename}' in canvas)", file=sys.stderr)
            continue
        col_x, col_bottom, col_width = anchor
        cursor_y = col_bottom + GUTTER_Y
        for png_path in png_paths:
            png_bytes = png_path.read_bytes()
            file_id = sha1_id(png_bytes)
            if file_id not in canvas["files"]:
                canvas["files"][file_id] = {
                    "mimeType": "image/png",
                    "id": file_id,
                    "dataURL": "data:image/png;base64," + base64.b64encode(png_bytes).decode("ascii"),
                    "created": now_ms(),
                    "lastRetrieved": now_ms(),
                }
            nat_w, nat_h = png_size(png_path)
            if nat_w > col_width:
                scale = col_width / nat_w
                w = col_width
                h = nat_h * scale
            else:
                w = nat_w
                h = nat_h
            canvas["elements"].append(
                make_text_element(f"📷 RESULT · {png_path.name}", col_x, cursor_y, w)
            )
            img_y = cursor_y + LABEL_HEIGHT + 8
            canvas["elements"].append(
                make_image_element(file_id, col_x, img_y, w, h)
            )
            cursor_y = img_y + h + GUTTER_Y
            injected += 1
            print(f"  +  {sketch.name}  ←  {png_path.relative_to(design_dir.parent.parent)}")
    canvas_path.write_text(json.dumps(canvas, indent=2), encoding="utf-8")
    print(f"\ninjected {injected} PNGs; skipped {skipped_no_png} sketches w/o PNG ref, "
          f"{skipped_no_column} sketches w/o matching canvas column")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
