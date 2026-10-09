"""s03 · Design methods: s03-design-methods.excalidraw, s03's drawings in one canvas (JL 261007: "put both of
them in one excalidraw").

Each part keeps its own source and is drawn by its own script into parts/; this builder copies them into one
canvas, top to bottom, each under a heading and inside its own frame (a part that already has frames keeps
them). Ids are prefixed per part, so the parts never clash. Written through b03's canvas.write, so every
mark a person adds to the one canvas survives a rebuild.

    1 · the methods canvas         parts/design-methods.excalidraw        methods_drawing.py
                                   (redrawn 261007 on the design unit; the three families, each card naming its registered methods)
    2 · the design unit catalog    parts/design-unit-methods.excalidraw   design_unit_drawing.py

    python build_s03_design_methods.py [out.excalidraw]
"""
import copy
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "b03_project_workbench" / "studio" / "_build"))
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))  # canvas (haipipe-studio)
import canvas  # noqa: E402

PARTS = [("1 · How we design: the reasoning kinds, one design unit in the two loops, the 13 cards as method types",
          "design-methods.excalidraw", "methods_drawing.py"),
         ("2 · The design unit catalog: each step's options, then one row per method (M01 – M05)",
          "design-unit-methods.excalidraw", "design_unit_drawing.py")]
# parts/s03-design-unit.excalidraw (the same catalog, plain) stays a part of its own: JL 261007, the two
# catalogs are the same content, so the one drawing holds it once.
GAP, GRAY, INK = 400, "#868e96", "#1e1e1e"
random.seed(3)


def _base(kind, x, y, w, h, eid, frame=None):
    return {"id": eid, "type": kind, "x": x, "y": y, "width": w, "height": h, "angle": 0, "strokeColor": INK,
            "backgroundColor": "transparent", "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid",
            "roughness": 0, "opacity": 100, "groupIds": [], "frameId": frame, "roundness": None,
            "seed": random.randint(1, 2**31 - 1), "version": 1, "versionNonce": random.randint(1, 2**31 - 1),
            "isDeleted": False, "boundElements": [], "updated": 1, "link": None, "locked": False}


def _text(x, y, s, size, color, eid, frame=None):
    e = _base("text", x, y, len(s) * size * 0.6, size * 1.25, eid, frame)
    e.update(text=s, originalText=s, fontSize=size, fontFamily=6, textAlign="left", verticalAlign="top",
             containerId=None, autoResize=True, lineHeight=1.25, strokeColor=color)
    return e


def _copy(els, k, dx, dy):
    """The part's elements with ids prefixed `p<k>-` (every reference too), moved by (dx, dy)."""
    pid = lambda i: f"p{k}-{i}" if i else i
    out = []
    for e in els:
        e = copy.deepcopy(e)
        e["id"], e["x"], e["y"] = pid(e["id"]), e["x"] + dx, e["y"] + dy
        e["groupIds"] = [pid(g) for g in e.get("groupIds") or []]
        e["frameId"] = pid(e.get("frameId"))
        e["containerId"] = pid(e.get("containerId")) if e.get("containerId") else e.get("containerId")
        e["boundElements"] = [{**b, "id": pid(b["id"])} for b in e.get("boundElements") or []]
        for side in ("startBinding", "endBinding"):
            if e.get(side):
                e[side] = {**e[side], "elementId": pid(e[side]["elementId"])}
        out.append(e)
    return out


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s03-design-methods.excalidraw"
    els, y = [], 0
    els.append(_text(0, y, "s03 · Design methods: the methods canvas and the design unit catalog, in one drawing", 40, INK, "s03-title"))
    els.append(_text(0, y + 60, "Each part is drawn by its own script into parts/ and copied here; change a part's script, "
                                "then rebuild this. Marks you add here are kept.", 20, GRAY, "s03-sub"))
    y += 200
    for k, (title, name, script) in enumerate(PARTS, 1):
        src = json.loads((HERE / "parts" / name).read_text(encoding="utf-8"))
        part = [e for e in src["elements"] if not e.get("isDeleted")]
        x0, y0 = min(e["x"] for e in part), min(e["y"] for e in part)
        x1, y1 = max(e["x"] + e["width"] for e in part), max(e["y"] + e["height"] for e in part)
        has_frames = any(e["type"] == "frame" for e in part)
        fid = None if has_frames else f"s03-frame-{k}"
        els.append(_text(0, y, title, 32, INK, f"s03-head-{k}"))
        els.append(_text(0, y + 48, f"from parts/{name}, drawn by {script}", 18, GRAY, f"s03-from-{k}"))
        top = y + 140
        moved = _copy(part, k, 60 - x0, top + 60 - y0)
        if fid:
            fr = _base("frame", 0, top, (x1 - x0) + 120, (y1 - y0) + 120, fid)
            fr["name"], fr["strokeColor"] = title.split(":")[0], GRAY
            els.append(fr)
            for e in moved:
                e["frameId"] = e.get("frameId") or fid
        els.extend(moved)
        y = top + (y1 - y0) + 120 + GAP
    canvas.write(out, els, Path(__file__).name)


if __name__ == "__main__":
    main()
