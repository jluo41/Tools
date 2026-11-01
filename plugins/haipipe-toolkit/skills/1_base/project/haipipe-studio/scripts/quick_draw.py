"""A topic's quick drawing, `sNN-<topic>.excalidraw` beside its face: a light sketch to mark up, opened from the ✎ on
the topic's line in its Block's map (JL 261029: "we might have the sNN's quick draw here ... where is the pop out
excalidraw for it?"; "could you add them as the default?").

    python quick_draw.py <topic folder> [...]     each topic without a drawing gets one; an existing one is never touched

A drawing, never a report (JL 261029, of a first version that listed the face's lines: "this is fucking report, not
the draw"). It follows coleam00/excalidraw-diagram-skill (Tools-SPACE/references/workflow-diagrams/): the idea drawn
as a pattern (cycle, timeline, tree, fan-in), free text unless a shape carries meaning, colour as meaning
(SEM below), and rendered and looked at before it is shown. A new topic gets its life line with its stage marked; the
picture of its idea is drawn by hand with the kit below (box, oval, diamond, arrow, line, dot, text).
"""
from __future__ import annotations

import json
import random
import re
import sys
from pathlib import Path

# colour as meaning (excalidraw-diagram-skill references/color-palette.md): (fill, stroke)
SEM = {"start": ("#fed7aa", "#c2410c"), "end": ("#a7f3d0", "#047857"), "decision": ("#fef3c7", "#b45309"),
       "agent": ("#ddd6fe", "#6d28d9"), "warn": ("#fee2e2", "#dc2626"), "plain": ("#dbeafe", "#1e3a5f"),
       "none": ("transparent", "#1e3a5f")}
TITLE, BODY, ON, SLATE = "#1e40af", "#64748b", "#374151", "#64748b"
FONT, WIDE = 8, 0.62   # Excalidraw's code font, Comic Shanns (JL 261030: "could you use this font type?"); its width per size
STAGES = ("explore", "shaping", "agreed", "closed")


def _el(kind, eid, x, y, w, h, stroke=SLATE, fill="transparent", **more):
    el = {"id": eid, "type": kind, "x": x, "y": y, "width": w, "height": h, "angle": 0, "strokeColor": stroke,
          "backgroundColor": fill, "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid", "roughness": 1,
          "opacity": 100, "groupIds": [], "frameId": None, "roundness": None, "seed": random.randint(1, 2 ** 31),
          "version": 1, "versionNonce": random.randint(1, 2 ** 31), "isDeleted": False, "boundElements": None,
          "updated": 1, "link": None, "locked": False}
    el.update(more)
    return el


def text(eid, x, y, words, size=18, color=BODY, align="left"):
    lines = words.split("\n")
    w, h = max(len(ln) for ln in lines) * size * WIDE, len(lines) * size * 1.25
    x = x - w / 2 if align == "center" else x
    return [_el("text", eid, x, y, w, h, color, text=words, originalText=words, fontSize=size, fontFamily=FONT,
                textAlign=align, verticalAlign="top", containerId=None, lineHeight=1.25, autoResize=True)]


def _shape(kind, eid, x, y, w, h, label, sem, size, dashed=False):
    fill, stroke = SEM[sem]
    els = [_el(kind, eid, x, y, w, h, stroke, fill, strokeStyle="dashed" if dashed else "solid",
               roundness={"type": 3} if kind == "rectangle" else None)]
    if label:
        n = label.count("\n") + 1
        els += text(eid + "_t", x + w / 2, y + h / 2 - n * size * 0.62, label, size, stroke if sem == "warn" else ON, "center")
    return els


def box(eid, x, y, w, h, label="", sem="plain", size=20, dashed=False):
    return _shape("rectangle", eid, x, y, w, h, label, sem, size, dashed)


def oval(eid, x, y, w, h, label="", sem="plain", size=20):
    return _shape("ellipse", eid, x, y, w, h, label, sem, size)


def diamond(eid, x, y, w, h, label="", sem="decision", size=18):
    return _shape("diamond", eid, x, y, w, h, label, sem, size)


def ask(eid, x, y, words, w=None):
    """An open question: a red note, the one thing a person owes here."""
    w = w or len(words) * 18 * WIDE + 40
    return box(eid, x, y, w, 46, words, "warn", 18)


def arrow(eid, pts, color=SLATE, label="", at=None, dashed=False, width=2):
    x0, y0 = pts[0]
    rel = [[px - x0, py - y0] for px, py in pts]
    xs, ys = [p[0] for p in rel], [p[1] for p in rel]
    els = [_el("arrow", eid, x0, y0, max(xs) - min(xs), max(ys) - min(ys), color, points=rel, strokeWidth=width,
               strokeStyle="dashed" if dashed else "solid", startArrowhead=None, endArrowhead="arrow",
               lastCommittedPoint=None, startBinding=None, endBinding=None, roundness={"type": 2})]
    if label:
        ax, ay = at or ((pts[0][0] + pts[-1][0]) / 2, (pts[0][1] + pts[-1][1]) / 2 - 30)
        els += text(eid + "_t", ax, ay, label, 16, color, "center")
    return els


def line(eid, pts, color=SLATE, width=2, dashed=False):
    els = arrow(eid, pts, color, width=width, dashed=dashed)
    els[0].update(type="line", endArrowhead=None)
    return els


def dot(eid, cx, cy, r=10, sem="plain"):
    fill, stroke = SEM[sem]
    return [_el("ellipse", eid, cx - r, cy - r, 2 * r, 2 * r, stroke, stroke if sem != "none" else fill)]


def heading(title, sub=""):
    return text("title", 0, 0, title, 32, TITLE) + (text("subtitle", 0, 48, sub, 18, BODY) if sub else [])


def write(path: Path, els: list) -> Path:
    Path(path).write_text(json.dumps({"type": "excalidraw", "version": 2, "source": "haipipe-studio quick_draw",
                                      "elements": els, "appState": {"viewBackgroundColor": "#ffffff", "gridSize": 20},
                                      "files": {}}, ensure_ascii=False) + "\n", encoding="utf-8")
    return Path(path)


def life_line(stage: str, x=0, y=200) -> list:
    """The topic's life as a timeline, its stage marked: explore, shaping, agreed, closed."""
    els = line("spine", [(x, y), (x + 900, y)], "#1e3a5f", 3)
    for i, name in enumerate(STAGES):
        cx = x + 60 + i * 260
        on = name == stage
        els += dot(f"st_{name}", cx, y, 14 if on else 9, "start" if on else "plain")
        els += text(f"st_{name}_t", cx, y - 50, name, 22 if on else 18, SEM["start"][1] if on else BODY, "center")
    return els + arrow("again", [(x + 320, y + 20), (x + 320, y + 70), (x + 60, y + 70), (x + 60, y + 24)],
                       SEM["decision"][1], "another round", (x + 190, y + 80))


def quick(topic: Path) -> Path | None:
    topic = Path(topic).resolve()
    out, face = topic / f"{topic.name}.excalidraw", topic / f"{topic.name}.md"
    if out.exists() or not face.is_file():
        return None
    text_ = face.read_text(encoding="utf-8")
    stage = re.search(r"(?mi)^\*\*Stage:\*\*\s*`?([a-z]+)", text_)
    title = text_.splitlines()[0].strip()
    return write(out, heading(title, "draw the idea here") + life_line(stage.group(1).lower() if stage else "explore", 0, 160))


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        made = quick(Path(arg))
        print(made or f"{arg}: has a drawing already (or no face); left alone")
