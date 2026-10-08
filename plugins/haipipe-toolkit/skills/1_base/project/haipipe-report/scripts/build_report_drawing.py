"""Build a Question's report drawing from studio frames (haipipe-report; moved here from
excalidraw-report/ref/ on 261007; designed in b03 studio/s04-studio-and-report).

A report drawing is generated, never drawn by hand. The report's own .md lists its figures,
each one named frame of a studio drawing. This script copies each frame, with what the person
drew in it except their red comment notes. It scales the frame to one width, straightens its
style, and stacks the figures top to bottom under a heading frame. Each figure carries its
number, its caption and its source.

To change a figure, change the studio drawing; to change the choice, change the list. Then
rebuild. The drawing is written as `reports/qNN_<topic>/qNN_<topic>.excalidraw`.

    python build_report_drawing.py <reports/qNN_topic/> [--width 3000]

The figure list, in `qNN_<topic>.md`, a yaml block under a `## Figures` heading:

    ## Figures

    ```yaml
    figures:
    - from: ../../studio/s01-overall-tree-structure/s01-overall-tree-structure.excalidraw
      frame: "1 · The ladder"
      caption: the levels a Question lives in
    ```

`from` is relative to the report folder; `frame` is the frame's exact name in that drawing.

The drawing is generated output, written whole on every build: nobody edits it, so there is
nothing to merge. Its ids are stable (a figure's elements keep their source ids, prefixed by the
figure), so a rebuild of an unchanged figure writes the same elements. Render its preview with
the caller's renderer (excalidraw-report ref/render_excalidraw.py, or haipipe-studio scripts/render_png.py).
"""
from __future__ import annotations

import argparse
import copy
import datetime as dt
import json
import re
import sys
from pathlib import Path

import yaml

SANS, MONO = 6, 3
INK, GRAY = "#1e1e1e", "#868e96"
REDS = {"#e03131", "#c92a2a", "#fa5252", "#f03e3e", "#ff0000", "#e8590c"}   # the person's comment ink
GAP, PAD, HEAD_H = 260, 60, 150


_N = [0]


def _el(kind, x, y, w, h, frame=None, color=INK, **extra):
    _N[0] += 1
    e = {"id": f"h{_N[0]:04d}", "type": kind, "x": x, "y": y, "width": w, "height": h,
         "angle": 0, "strokeColor": color, "backgroundColor": "transparent", "fillStyle": "solid",
         "strokeWidth": 1, "strokeStyle": "solid", "roughness": 0, "opacity": 100, "groupIds": [],
         "frameId": frame, "roundness": None, "seed": 1, "version": 1,
         "versionNonce": 1, "isDeleted": False, "boundElements": [],
         "updated": 1, "link": None, "locked": False}
    e.update(extra)
    return e


def _text(x, y, s, size, frame=None, color=INK, font=SANS, link=None):
    lines = s.split("\n")
    return _el("text", x, y, max(len(l) for l in lines) * size * (0.6 if font == MONO else 0.55),
               len(lines) * size * 1.25, frame, color, text=s, originalText=s, fontSize=size,
               fontFamily=font, textAlign="left", verticalAlign="top", containerId=None,
               autoResize=True, lineHeight=1.25, link=link)


def read_report(folder: Path) -> tuple[str, dict, list[dict]]:
    """The report's title, its header fields and its figure list."""
    md = folder / f"{folder.name}.md"
    text = md.read_text(encoding="utf-8")
    title = (re.search(r"(?m)^# (.+)$", text) or [None, folder.name])[1].strip()
    head = dict(re.findall(r"(?m)^(answers|answer-status|state):\s*(.+?)\s*$", text))
    block = re.search(r"(?ms)^## Figures\s*$(?:(?!^## ).)*?^```yaml\n(.*?)^```", text)
    if not block:
        sys.exit(f"{md}: no '## Figures' yaml block; nothing to build")
    figures = (yaml.safe_load(block.group(1)) or {}).get("figures") or []
    return title, head, figures


def frame_members(source: Path, name: str) -> tuple[dict, list[dict]]:
    """The named frame of a drawing and everything in it, the person's red notes left out."""
    els = [e for e in json.loads(source.read_text(encoding="utf-8"))["elements"] if not e.get("isDeleted")]
    frames = [e for e in els if e["type"] == "frame" and e.get("name") == name]
    if not frames:
        names = sorted(str(e.get("name")) for e in els if e["type"] == "frame")
        sys.exit(f"{source.name}: no frame named {name!r}; it has: {', '.join(names) or 'no frames'}")
    fr = frames[0]
    inside = [e for e in els if e.get("frameId") == fr["id"]]
    note = {e["id"] for e in inside if not e["id"].startswith("s-") and str(e.get("strokeColor", "")).lower() in REDS}
    note |= {e["id"] for e in inside if e.get("containerId") in note}
    return fr, [copy.deepcopy(e) for e in inside if e["id"] not in note]


def place(members: list[dict], fr: dict, x0: float, y0: float, s: float, frame_id: str, tag: str) -> None:
    """Move a frame's copy to (x0, y0), scaled by s, in the report's style, with ids of its own."""
    ids = {e["id"]: f"{tag}-{e['id']}" for e in members}
    for e in members:
        e["id"] = ids[e["id"]]
        e["x"] = x0 + (e["x"] - fr["x"]) * s
        e["y"] = y0 + (e["y"] - fr["y"]) * s
        e["width"], e["height"] = e.get("width", 0) * s, e.get("height", 0) * s
        if e.get("points"):
            e["points"] = [[px * s, py * s] for px, py in e["points"]]
        if e.get("fontSize"):
            e["fontSize"] = e["fontSize"] * s
        e["roughness"] = 0                                   # the report's style: straight and clean
        e["frameId"] = frame_id
        e["groupIds"] = [f"{tag}-{g}" for g in e.get("groupIds") or []]
        if e.get("containerId"):
            e["containerId"] = ids.get(e["containerId"])
        e["boundElements"] = [dict(b, id=ids[b["id"]]) for b in e.get("boundElements") or [] if b["id"] in ids]
        for end in ("startBinding", "endBinding"):
            if e.get(end):
                e[end] = dict(e[end], elementId=ids[e[end]["elementId"]]) if e[end].get("elementId") in ids else None


def build(folder: Path, width: float) -> Path:
    folder = folder.resolve()
    title, head, figures = read_report(folder)
    today = dt.date.today().strftime("%y%m%d")
    els: list[dict] = []
    # the heading frame: which Question, its state, and where every figure comes from
    lines = [f"{head.get('answers', '')} · answer-status: {head.get('answer-status', 'open')}".strip(" ·"),
             *[f"Fig {n} · {f['frame']}  ({Path(f['from']).stem})" for n, f in enumerate(figures, 1)],
             f"generated {today} by build_report_drawing.py from the studio frames above:",
             "change a figure in its studio drawing, or the list in this report's .md, then rebuild"]
    hf = _el("frame", 0, 0, width, 0, name=f"{folder.name.split('_')[0].upper()} · report")
    els += [hf, _text(PAD, PAD, title, 44, hf["id"])]
    els += [_text(PAD, PAD + 80 + i * 34, l, 24, hf["id"], GRAY) for i, l in enumerate(lines)]
    hf["height"] = PAD + 80 + len(lines) * 34 + PAD
    y = hf["height"] + GAP
    for n, f in enumerate(figures, 1):
        source = (folder / f["from"]).resolve()
        fr, members = frame_members(source, f["frame"])
        s = min(1.0, (width - 2 * PAD) / fr["width"])
        fig = _el("frame", 0, y, width, 0, name=f"Fig {n} · {f['frame']}")
        rel = Path(f["from"]).as_posix()
        els += [fig, _text(PAD, y + PAD, f"Fig {n} · {f.get('caption') or f['frame']}", 34, fig["id"]),
                _text(PAD, y + PAD + 56, f"from {Path(rel).stem} › {f['frame']} · built {today}", 22,
                      fig["id"], GRAY, link=rel)]
        top = y + PAD + HEAD_H
        place(members, fr, PAD, top, s, fig["id"], f"f{n}")
        els += members
        fig["height"] = top - y + fr["height"] * s + PAD
        y += fig["height"] + GAP
    out = folder / f"{folder.name}.excalidraw"
    out.write_text(json.dumps({"type": "excalidraw", "version": 2, "source": "haipipe-report/scripts/build_report_drawing.py",
                               "elements": els, "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None},
                               "files": {}}, ensure_ascii=False, indent=1))
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("report", type=Path, help="the report folder, reports/qNN_<topic>/")
    ap.add_argument("--width", type=float, default=3000)
    print(build(ap.parse_args().report, ap.parse_args().width))


if __name__ == "__main__":
    main()
