"""One drawing per leaf of a mind map, holding that leaf's slides (JL 261029: "一个 leaf 就一个 draw 然后里面可以有几个
slides"): `map/<leaf id>-<first words>.excalidraw` beside the `.mindmap.md`. The leaf's line carries a link to it that
opens in the page's pop-out, to draw on.

    sketch(md)            every leaf without a drawing gets one; an existing one is never touched
    drawing_of(md, id)    the leaf's drawing, or None
    slides_of(md)         the topic's slides, (id, leaf, picture), from `<topic>.slides.json`

A slide names its leaf (`"leaf": "n29"`) in `.slides.json`; a leaf's drawing is seeded with the leaf's words on top and
its slides in a row under them, each a JPEG 1600 wide, so a person marks them in red. A leaf with no slide starts with
its words only. A later sketch leaves an existing drawing alone. Branches (the sections) have no drawing.
"""
from __future__ import annotations

import base64
import io
import json
import random
import re
import textwrap
from pathlib import Path

import mmtree as MT

INK, RED, GREEN = "#1e1e1e", "#e03131", "#2f9e44"
ROLE = re.compile(r"^\[([^\]]+)\]\s*")


def folder_of(md: Path) -> Path:
    return Path(md).parent / "map"


def slug(words: str, n: int = 4) -> str:
    plain = re.sub(r"[^a-z0-9]+", "-", ROLE.sub("", MT.ID_MARK.sub("", words)).lower()).strip("-")
    return "-".join(plain.split("-")[:n]) or "leaf"


def drawing_of(md: Path, nid: str) -> Path | None:
    if not nid or nid.startswith("@"):
        return None
    found = sorted(folder_of(md).glob(f"{nid}-*.excalidraw")) + [p for p in [folder_of(md) / f"{nid}.excalidraw"] if p.is_file()]
    return found[0] if found else None


def slides_of(md: Path) -> list:
    """The topic's slides in order, (id, leaf, picture), from `<topic>.slides.json` beside the map."""
    topic = Path(md).resolve().parent
    try:
        slides = json.loads((topic / f"{topic.name}.slides.json").read_text(encoding="utf-8"))["slides"]
    except (OSError, ValueError, KeyError, TypeError):
        return []
    return [(str(s.get("id", "")), str(s.get("leaf", "")), topic / str(s.get("image", "")))
            for s in slides if isinstance(s, dict)]


def _base(kind, x, y, w, h, **more):
    el = {"id": "%016x" % random.getrandbits(64), "type": kind, "x": x, "y": y, "width": w, "height": h, "angle": 0,
          "strokeColor": INK, "backgroundColor": "transparent", "fillStyle": "solid", "strokeWidth": 1,
          "strokeStyle": "solid", "roughness": 1, "opacity": 100, "groupIds": [], "frameId": None, "roundness": None,
          "seed": random.randint(1, 2 ** 31), "version": 1, "versionNonce": random.randint(1, 2 ** 31),
          "isDeleted": False, "boundElements": None, "updated": 1, "link": None, "locked": False}
    el.update(more)
    return el


def _text(x, y, words, size=20, color=INK, width=40):
    lines = textwrap.wrap(words, width) or [""]
    body = "\n".join(lines)
    return _base("text", x, y, max(len(ln) for ln in lines) * size * 0.62, len(lines) * size * 1.25,
                 text=body, originalText=body, fontSize=size, fontFamily=8, textAlign="left", verticalAlign="top",
                 containerId=None, lineHeight=1.25, autoResize=True, strokeColor=color)


def seed(leaf: MT.Node, pictures: list) -> tuple:
    """The leaf's words on top, its slides in a row under them, each labelled; returns (elements, files)."""
    from PIL import Image
    words = MT.ID_MARK.sub("", leaf.text).replace("`", "")
    m = ROLE.match(words)
    role = m.group(1).lower() if m else ""
    colour = RED if role == "open" else GREEN if role == "agreed" else INK
    els, files, x = [_text(0, 0, ROLE.sub("", words).strip(), 32, colour, 70)], {}, 0
    for sid, pic in pictures:
        im = Image.open(pic).convert("RGB")
        im.thumbnail((1600, 1600))
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=88)
        fid = "slide" + "%035x" % random.getrandbits(140)
        files[fid] = {"mimeType": "image/jpeg", "id": fid, "created": 1,
                      "dataURL": "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()}
        w, h = 1200, round(1200 * im.height / im.width)
        els += [_text(x, 90, f"slide {sid}", 18, INK, 20),
                _base("image", x, 125, w, h, status="saved", fileId=fid, scale=[1, 1], strokeColor="transparent")]
        x += w + 100
    return els, files


def sketch(md: Path) -> list:
    """Each leaf without a drawing gets one, with the slides that name it. Returns the drawings written."""
    md = Path(md).resolve()
    mm = MT.load(md)
    slides = slides_of(md)
    out = []
    for node, parent, depth, _ in MT.walk(mm.root):
        if depth < 2 or node.id.startswith("@") or (parent and parent.id.startswith("@")) or drawing_of(md, node.id):
            continue                                  # sections have none; a drawing a person drew on is never rewritten
        pictures = [(sid, pic) for sid, leaf, pic in slides if leaf == node.id and pic.is_file()]
        path = folder_of(md) / f"{node.id}-{slug(node.text)}.excalidraw"
        path.parent.mkdir(exist_ok=True)
        els, files = seed(node, pictures)
        path.write_text(json.dumps({"type": "excalidraw", "version": 2, "source": "haipipe-mindmap sketch",
                                    "elements": els, "appState": {"viewBackgroundColor": "#ffffff"},
                                    "files": files}) + "\n", encoding="utf-8")
        out.append(path)
    return out
