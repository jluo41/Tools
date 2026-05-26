"""Shared helpers for txt-to-canvas.py (rebuild) and txt-append-to-canvas.py (append).

Exports:
- split_sections(content, blank_lines) -> [(section_text, marker_title_or_None)]
- render_sections_to_pngs(txts, png_dir, blank_lines) -> [(txt, idx, title, png)]
- make_column_elements(txt_path, section_items, x, y, col_id_suffix, row_gutter)
      -> (new_elements: list[dict], new_files: dict[str, dict])
- make_excalidraw_from_items(items, col_gutter, row_gutter) -> dict
- png_size(path) -> (w, h)
"""
from __future__ import annotations

import base64
import hashlib
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

SECTION_MARKER = re.compile(r"^\s*[─\-]+\s*§\s*(?P<title>.*?)\s*[─\-]*\s*$")


def png_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as f:
        head = f.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"not a PNG: {path}")
    w, h = struct.unpack(">II", head[16:24])
    return w, h


def _marker_title(line: str) -> str | None:
    m = SECTION_MARKER.match(line)
    if not m:
        return None
    if "§" not in line:
        return None
    return m.group("title").strip()


def split_sections(content: str, blank_lines: int = 0) -> list[tuple[str, str | None]]:
    lines = content.splitlines()
    n = len(lines)
    boundaries: list[tuple[int, str | None]] = [(0, None)]
    for i, ln in enumerate(lines):
        title = _marker_title(ln)
        if title is not None:
            boundaries.append((i + 1, title or None))
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
        while chunk_lines and (
            _marker_title(chunk_lines[-1]) is not None
            or chunk_lines[-1].strip() == ""
        ):
            chunk_lines.pop()
        while chunk_lines and chunk_lines[0].strip() == "":
            chunk_lines.pop(0)
        chunk = "\n".join(chunk_lines).rstrip()
        if chunk.strip():
            sections.append((chunk, title))
    return sections


def section_title(section: str, fallback: str) -> str:
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
                print(
                    f"  rendered {txt.name} §{i + 1}/{len(sections)} -> {png.name}",
                    file=sys.stderr,
                )
        browser.close()
    return out


# ── Excalidraw element helpers ───────────────────────────────────────────────


def _seed_factory():
    counter = [1]

    def seed():
        counter[0] += 1
        return counter[0] * 1000003 % (2**31)

    return seed


def _base_props(seed_fn, now_ms: int) -> dict:
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
        seed=seed_fn(),
        version=1,
        versionNonce=seed_fn(),
        isDeleted=False,
        boundElements=None,
        updated=now_ms,
        link=None,
        locked=False,
    )


def _text_element(eid: str, x: int, y: int, text: str, font_size: int,
                  seed_fn, now_ms: int) -> dict:
    return {
        "type": "text",
        "id": eid,
        "x": x,
        "y": y,
        "width": max(int(font_size * 0.62 * len(text)), 100),
        "height": int(font_size * 1.25),
        "text": text,
        "fontSize": font_size,
        "fontFamily": 3,
        "textAlign": "left",
        "verticalAlign": "top",
        "baseline": int(font_size * 1.1),
        "containerId": None,
        "originalText": text,
        "lineHeight": 1.25,
        "autoResize": True,
        **_base_props(seed_fn, now_ms),
    }


def _image_element(eid: str, x: int, y: int, w: int, h: int, file_id: str,
                   seed_fn, now_ms: int) -> dict:
    return {
        "type": "image",
        "id": eid,
        "x": x,
        "y": y,
        "width": w,
        "height": h,
        "fileId": file_id,
        "status": "saved",
        "scale": [1, 1],
        **_base_props(seed_fn, now_ms),
    }


def make_column_elements(
    txt_path: Path,
    section_items: list[tuple[int, str, Path]],
    x: int,
    y: int,
    col_id_suffix: str,
    row_gutter: int = 50,
    section_title_h: int = 22,
    file_header_h: int = 44,
) -> tuple[list[dict], dict[str, dict]]:
    """Build elements for ONE column, starting at (x, y).

    section_items: [(idx, title, png_path), ...] for this file.
    col_id_suffix: appended to element IDs to keep them unique (e.g. timestamp
                   when appending; index string when rebuilding).

    Returns (new_elements, new_files_by_fileid).
    """
    elements: list[dict] = []
    files: dict[str, dict] = {}
    now_ms = int(time.time() * 1000)
    seed_fn = _seed_factory()

    elements.append(
        _text_element(f"h-{col_id_suffix}", x, y, f"📄 {txt_path.name}",
                      font_size=22, seed_fn=seed_fn, now_ms=now_ms)
    )
    cy = y + file_header_h
    n = len(section_items)
    for sec_i, (s_idx, s_title, png) in enumerate(section_items):
        label = f"§{sec_i + 1}/{n}  ·  {s_title}"
        elements.append(
            _text_element(
                f"st-{col_id_suffix}-{sec_i:03d}",
                x, cy, label,
                font_size=14, seed_fn=seed_fn, now_ms=now_ms,
            )
        )
        cy += section_title_h
        # Image: read bytes, register file, place element.
        png_bytes = png.read_bytes()
        file_id = hashlib.sha1(png_bytes).hexdigest()
        if file_id not in files:
            data_url = "data:image/png;base64," + base64.b64encode(png_bytes).decode("ascii")
            files[file_id] = {
                "mimeType": "image/png",
                "id": file_id,
                "dataURL": data_url,
                "created": now_ms,
                "lastRetrieved": now_ms,
            }
        w_native, h_native = png_size(png)
        w, h = w_native // 2, h_native // 2
        elements.append(
            _image_element(
                f"im-{col_id_suffix}-{sec_i:03d}",
                x, cy, w, h, file_id,
                seed_fn=seed_fn, now_ms=now_ms,
            )
        )
        cy += h + row_gutter
    return elements, files


def make_excalidraw_from_items(
    items: list[tuple[Path, int, str, Path]],
    col_gutter: int = 300,
    row_gutter: int = 50,
) -> dict:
    """Multi-column layout for the rebuild script — one column per file."""
    # Group by file, preserving order of first appearance.
    columns: list[tuple[Path, list[tuple[int, str, Path]]]] = []
    by_file: dict[Path, list[tuple[int, str, Path]]] = {}
    for txt, idx, title, png in items:
        by_file.setdefault(txt, []).append((idx, title, png))
    seen: set[Path] = set()
    for txt, _i, _t, _p in items:
        if txt not in seen:
            seen.add(txt)
            columns.append((txt, by_file[txt]))

    all_elements: list[dict] = []
    all_files: dict[str, dict] = {}

    # Compute column widths from PNG sizes (display = native // 2).
    col_widths: list[int] = []
    for _txt, secs in columns:
        wmax = 0
        for _i, _t, png in secs:
            w_native, _h = png_size(png)
            wmax = max(wmax, w_native // 2)
        col_widths.append(wmax)

    x = 0
    for col_idx, ((txt, secs), col_w) in enumerate(zip(columns, col_widths)):
        col_elements, col_files = make_column_elements(
            txt_path=txt,
            section_items=secs,
            x=x,
            y=0,
            col_id_suffix=f"{col_idx:03d}",
            row_gutter=row_gutter,
        )
        all_elements.extend(col_elements)
        all_files.update(col_files)
        x += col_w + col_gutter

    return {
        "type": "excalidraw",
        "version": 2,
        "source": "diagram-ascii-canvas",
        "elements": all_elements,
        "appState": {
            "viewBackgroundColor": "#ffffff",
            "gridSize": None,
        },
        "files": all_files,
    }
