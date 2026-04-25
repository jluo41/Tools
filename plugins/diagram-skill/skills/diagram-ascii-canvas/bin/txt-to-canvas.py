#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["playwright"]
# ///
"""
Bundle a folder of ASCII .txt diagrams into one .excalidraw canvas.

- Each .txt is split into sections (default: on runs of 2+ blank lines).
- Each section is screenshotted as a PNG via headless Chromium (color emoji + monospace).
- All PNGs are embedded into one Excalidraw file, laid out as a grid.
- A title text element is placed above each image.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
import struct
import sys
import time
from pathlib import Path

HTML_TEMPLATE = """<!doctype html>
<html><head><meta charset="utf-8"><style>
  html,body{margin:0;padding:0;background:#fff;}
  pre{
    margin:0;
    padding:20px;
    font-family: "Menlo","SF Mono","Monaco","Apple Color Emoji","Segoe UI Emoji",monospace;
    font-size:16px;
    line-height:1.35;
    white-space:pre;
    color:#111;
    display:inline-block;
  }
</style></head><body><pre id="d"></pre></body></html>
"""


def png_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as f:
        head = f.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"not a PNG: {path}")
    w, h = struct.unpack(">II", head[16:24])
    return w, h


# Explicit section divider:  "─§ Title ─...─"  or ASCII "--§ Title ---"
# A line whose first non-space chars are 1+ dashes (─ or -) followed by §,
# then optional title, then any trailing dash run.
SECTION_MARKER = re.compile(r"^\s*[─\-]+\s*§\s*(?P<title>.*?)\s*[─\-]*\s*$")


def _marker_title(line: str) -> str | None:
    """If `line` is a section divider, return its title (may be empty). Else None."""
    m = SECTION_MARKER.match(line)
    if not m:
        return None
    # Guard against false positives like "----" with no §.
    if "§" not in line:
        return None
    return m.group("title").strip()


def split_sections(content: str, blank_lines: int = 0) -> list[tuple[str, str | None]]:
    """Split text into sections.

    Primary signal: explicit divider lines of the form ``─§ Title ─...``
    (Unicode) or ``--§ Title ---`` (ASCII). The marker line itself is
    consumed (not rendered). Title comes from the marker.

    Secondary (optional, off by default): runs of `blank_lines`+ blank
    lines also split. Used as a fallback when files have no markers.

    Returns [(section_text, marker_title_or_None), ...]. If a section was
    started by a marker, its title is the marker's title; otherwise None
    and the caller falls back to the first-line heuristic.
    """
    lines = content.splitlines()
    n = len(lines)

    # boundary[i] = (line_index_where_section_starts, marker_title_or_None)
    # Consume the marker line itself.
    boundaries: list[tuple[int, str | None]] = [(0, None)]

    for i, ln in enumerate(lines):
        title = _marker_title(ln)
        if title is not None:
            # Section starts on the line AFTER the marker.
            boundaries.append((i + 1, title or None))

    # Blank-line splits (only if no markers found AND user opted in).
    has_markers = len(boundaries) > 1
    if not has_markers and blank_lines > 0:
        run = 0
        for i, ln in enumerate(lines):
            if ln.strip() == "":
                run += 1
            else:
                if run >= blank_lines and i > 0:
                    boundaries.append((i, None))
                run = 0

    boundaries.sort()
    boundaries.append((n, None))

    sections: list[tuple[str, str | None]] = []
    for (a, title), (b, _) in zip(boundaries[:-1], boundaries[1:]):
        chunk_lines = lines[a:b]
        # The marker line that triggers the NEXT section will sit at the END of
        # this chunk's slice (since boundary points to marker_idx + 1). Drop it
        # — and any trailing blanks before it — so it doesn't get rendered.
        while chunk_lines and (
            _marker_title(chunk_lines[-1]) is not None
            or chunk_lines[-1].strip() == ""
        ):
            chunk_lines.pop()
        # Drop leading blank lines for nicer rendering.
        while chunk_lines and chunk_lines[0].strip() == "":
            chunk_lines.pop(0)
        chunk = "\n".join(chunk_lines).rstrip()
        if chunk.strip():
            sections.append((chunk, title))
    return sections


def section_title(section: str, fallback: str) -> str:
    """Fallback title for sections that didn't have a marker — first non-blank line."""
    for line in section.splitlines():
        s = line.strip()
        if not s:
            continue
        s = s.rstrip("═─=- ")
        return (s[:70] + "…") if len(s) > 71 else s
    return fallback


def render_sections_to_pngs(
    txts: list[Path],
    png_dir: Path,
    blank_lines: int,
) -> list[tuple[Path, int, str, Path]]:
    """Render every section of every .txt to its own PNG.

    Returns list of (source_txt, section_index, section_title, png_path).
    """
    from playwright.sync_api import sync_playwright

    png_dir.mkdir(parents=True, exist_ok=True)
    out: list[tuple[Path, int, str, Path]] = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(device_scale_factor=2)
        page = ctx.new_page()
        page.set_content(HTML_TEMPLATE)
        for txt in txts:
            content = txt.read_text(encoding="utf-8")
            sections = split_sections(content, blank_lines=blank_lines)
            if not sections:
                continue
            single = len(sections) == 1
            for i, (sec, marker_title) in enumerate(sections):
                page.evaluate(
                    "t => { document.getElementById('d').textContent = t; }", sec
                )
                elem = page.query_selector("#d")
                assert elem is not None
                suffix = "" if single else f"__{i + 1:02d}"
                png = png_dir / f"{txt.stem}{suffix}.png"
                elem.screenshot(path=str(png))
                title = marker_title or section_title(sec, fallback=txt.name)
                out.append((txt, i, title, png))
                print(f"  rendered {txt.name} §{i + 1}/{len(sections)} -> {png.name}", file=sys.stderr)
        browser.close()
    return out


def make_excalidraw(
    items: list[tuple[Path, int, str, Path]],
    col_gutter: int = 300,
    row_gutter: int = 50,
    section_title_h: int = 22,
    file_header_h: int = 44,
) -> dict:
    """Layout: one column per file, sections stacked top→bottom in each column.

    items = [(txt_path, section_index, section_title, png_path), ...] in order.
    """
    elements: list[dict] = []
    files: dict[str, dict] = {}
    now_ms = int(time.time() * 1000)

    # Group items by source file, preserving file & section order.
    columns: list[tuple[Path, list[tuple[int, str, Path, tuple[int, int]]]]] = []
    by_file: dict[Path, list[tuple[int, str, Path, tuple[int, int]]]] = {}
    for txt, idx, title, png in items:
        w_native, h_native = png_size(png)
        # rendered at 2x DSF, halve for display
        sz = (w_native // 2, h_native // 2)
        by_file.setdefault(txt, []).append((idx, title, png, sz))
    seen: set[Path] = set()
    for txt, _i, _t, _p in items:
        if txt not in seen:
            seen.add(txt)
            columns.append((txt, by_file[txt]))

    seed_counter = [1]

    def seed():
        seed_counter[0] += 1
        return seed_counter[0] * 1000003 % (2**31)

    def base_props():
        return dict(
            angle=0,
            strokeColor="#1e1e1e",
            backgroundColor="transparent",
            fillStyle="solid",
            strokeWidth=2,
            strokeStyle="solid",
            roughness=0,
            opacity=100,
            groupIds=[],
            frameId=None,
            roundness=None,
            seed=seed(),
            version=1,
            versionNonce=seed(),
            isDeleted=False,
            boundElements=None,
            updated=now_ms,
            link=None,
            locked=False,
        )

    def add_text(eid: str, x: int, y: int, text: str, font_size: int) -> None:
        elements.append({
            "type": "text",
            "id": eid,
            "x": x,
            "y": y,
            "width": max(int(font_size * 0.62 * len(text)), 100),
            "height": int(font_size * 1.25),
            "text": text,
            "fontSize": font_size,
            "fontFamily": 3,  # monospace (Cascadia)
            "textAlign": "left",
            "verticalAlign": "top",
            "baseline": int(font_size * 1.1),
            "containerId": None,
            "originalText": text,
            "lineHeight": 1.25,
            "autoResize": True,
            **base_props(),
        })

    def add_image(eid: str, x: int, y: int, w: int, h: int, png: Path) -> None:
        png_bytes = png.read_bytes()
        file_id = hashlib.sha1(png_bytes).hexdigest()
        data_url = "data:image/png;base64," + base64.b64encode(png_bytes).decode("ascii")
        files[file_id] = {
            "mimeType": "image/png",
            "id": file_id,
            "dataURL": data_url,
            "created": now_ms,
            "lastRetrieved": now_ms,
        }
        elements.append({
            "type": "image",
            "id": eid,
            "x": x,
            "y": y,
            "width": w,
            "height": h,
            "fileId": file_id,
            "status": "saved",
            "scale": [1, 1],
            **base_props(),
        })

    # Column widths = max display width in that column.
    col_widths = [max(sz[0] for _i, _t, _p, sz in secs) for _txt, secs in columns]

    x = 0
    for col_idx, ((txt, secs), col_w) in enumerate(zip(columns, col_widths)):
        # Big file header at top of column.
        add_text(f"h-{col_idx:03d}", x, 0, f"📄 {txt.name}", font_size=22)
        y = file_header_h
        for sec_i, (s_idx, s_title, png, (w, h)) in enumerate(secs):
            # Section title
            label = f"§{sec_i + 1}/{len(secs)}  ·  {s_title}"
            add_text(
                f"st-{col_idx:03d}-{sec_i:03d}",
                x,
                y,
                label,
                font_size=14,
            )
            y += section_title_h
            # Image
            add_image(
                f"im-{col_idx:03d}-{sec_i:03d}",
                x,
                y,
                w,
                h,
                png,
            )
            y += h + row_gutter
        x += col_w + col_gutter

    return {
        "type": "excalidraw",
        "version": 2,
        "source": "diagram-ascii-canvas",
        "elements": elements,
        "appState": {
            "viewBackgroundColor": "#ffffff",
            "gridSize": None,
        },
        "files": files,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("inputs", nargs="+", help="A directory or one-or-more .txt files")
    ap.add_argument("--out", help="Output .excalidraw path (default: <dir>/canvas.excalidraw)")
    ap.add_argument(
        "--col-gutter",
        type=int,
        default=300,
        help="Horizontal gap between file columns in px (default 300)",
    )
    ap.add_argument(
        "--row-gutter",
        type=int,
        default=50,
        help="Vertical gap between sections within a column in px (default 50)",
    )
    ap.add_argument("--png-dir", help="Where to put intermediate PNGs (default: <dir>/_pngs)")
    ap.add_argument(
        "--blank-lines",
        type=int,
        default=0,
        help=(
            "Fallback only — used when a file has NO `─§` markers. Split that "
            "file at runs of this many+ consecutive blank lines. Default 0 "
            "(no fallback: marker-less files render as one PNG)."
        ),
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

    date_tag = time.strftime("%y%m%d")  # e.g. 260425
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
    doc = make_excalidraw(items, col_gutter=args.col_gutter, row_gutter=args.row_gutter)

    out.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[3/3] wrote {out}  ({len(doc['elements'])} elements, {len(doc['files'])} images)", file=sys.stderr)


if __name__ == "__main__":
    main()
