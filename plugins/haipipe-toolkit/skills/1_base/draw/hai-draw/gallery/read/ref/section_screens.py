"""A Section's examples topic drawn as what it is for: each published paper's same Section, a screenshot, one under the
other, so a person checks how others write it (JL 261104: "for the exmaples here, we just want to have the screenshot
intdouction to check"). No logic chains and no reference cards.

    python section_screens.py draw <topic folder>

Since 261111 each paper is its own area (frame) with its screenshot and its `logic:` (reads/<id>-*/reading.yaml),
in rows of four after a Pattern area (JL 261111: "I want each abstract to be a area").

Reads the face's `related:` yaml (key, open, papers: id, item) and each `reads/<id>-*/shots/section.jpg`, the Section
as a reader sees it: from the PDF (read_paper.py paras) or from the article's page when no PDF is free. A paper with
no screenshot draws a red line naming it. Written through canvas.write, so a person's marks survive every rebuild.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
SKILLS = HERE.parents[4]
sys.path.insert(0, str(SKILLS / "draw/hai-draw/scripts"))
sys.path.insert(0, str(SKILLS / "project/hai-studio/scripts"))
from draw import GREY, RED, Drawing  # noqa: E402
import canvas  # noqa: E402

W, PAD, PIC = 2400, 80, 2240
PW, PPIC = 1500, 1340                 # one paper's area (JL 261111: "I want each abstract to be a area")
PER_ROW = 4
SCAFFOLD = {"title", "subtitle", "spine", "again", "again_t"} | {f"st_{w}{t}" for w in
            ("explore", "shaping", "agreed", "closed") for t in ("", "_t")}   # new_topic's stub, not a person's mark


def config(topic: Path) -> dict:
    face = (topic / f"{topic.name}.md").read_text(encoding="utf-8")
    block = re.search(r"(?ms)^```yaml\n(related:.*?)^```", face)
    if not block:
        raise SystemExit(f"{topic.name}: its face has no related: yaml")
    return yaml.safe_load(block.group(1))["related"]


def drop_scaffold(out: Path) -> None:
    """The new-topic stub (title, stage bar, 'another round') is not a person's mark: drop it before the merge,
    or canvas.write keeps it on every rebuild and it sits over the pattern box (JL 261111)."""
    if not out.exists():
        return
    import json
    doc = json.loads(out.read_text(encoding="utf-8"))
    els = doc.get("elements", [])
    keep = [e for e in els if e.get("id") not in SCAFFOLD]
    if len(keep) != len(els):
        doc["elements"] = keep
        out.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")


def logic(topic: Path, pid: str) -> list:
    for r in sorted(topic.glob(f"reads/{pid}-*/reading.yaml")):
        return (yaml.safe_load(r.read_text(encoding="utf-8")) or {}).get("logic") or []
    return []


def logic_map(d, name: str, moves: list, x: float, y: float) -> float:
    """The paper's logic as a mind map (JL 261111: "why the logic is not the mind map???"): the paper at the left,
    one box per move to its right in order, each box its id and words with its role on top, joined by elbow lines.
    Returns the y below it."""
    rw, gap, cw = 300, 120, PPIC - 300 - 120
    cx = x + rw + gap
    boxes, yy = [], y
    for m in moves:
        text = str(m.get("text", ""))
        h = d.height(text, cw - 40, 24) + 56
        d.box(cx, yy, cw, h, sw=1.5)
        d.text(cx + 20, yy + 10, str(m.get("role", "")), size=20, color=GREY)
        d.para(cx + 20, yy + 38, text, cw - 40, 24)
        boxes.append((yy, h))
        yy += h + 18
    bottom = yy - 18
    rh = max(110, d.height(name, rw - 40, 30) + 50)
    ry = (y + bottom) / 2 - rh / 2
    d.key(x, ry, rw, rh, 3)
    d.para(x + 20, ry + 25, name, rw - 40, 30)
    bus = x + rw + gap / 2
    d.line([(x + rw, ry + rh / 2), (bus, ry + rh / 2)], arrow=False, sw=2)
    d.line([(bus, boxes[0][0] + boxes[0][1] / 2), (bus, boxes[-1][0] + boxes[-1][1] / 2)], arrow=False, sw=2)
    for by, bh in boxes:
        d.line([(bus, by + bh / 2), (cx, by + bh / 2)], arrow=False, sw=2)
    return bottom


def draw(topic: Path) -> Path:
    """One area (frame) per paper: its name, its Section's screenshot, then its logic, one move a line; a first
    area holds the shared pattern. Areas sit in rows of four, read left to right."""
    topic = topic.resolve()
    cfg = config(topic)
    title = (topic / f"{topic.name}.md").read_text(encoding="utf-8").splitlines()[0]
    title = re.sub(r"^s\d+\s*·\s*", "", title).strip()
    d = Drawing()
    f = d.frame("Pattern", 2600, 200)
    x, y = f["x"] + PAD, f["y"] + 50
    d.text(x, y, title, size=46)
    y += 90
    kw = 2600 - 2 * PAD
    height = d.height(cfg["key"], kw - 60, 34)
    d.key(x, y, kw, height + 40)
    d.para(x + 30, y + 20, cfg["key"], kw - 60, 34)
    y += height + 90
    for line in cfg.get("open") or []:
        if isinstance(line, dict):          # `- ours: "..."` reads as a dict; print it as "ours: ..."
            line = " · ".join(f"{k}: {v}" for k, v in line.items())
        h = d.height("? " + str(line), kw, 30)
        d.para(x, y, "? " + str(line), kw, 30, color=RED)
        y += h + 24
    f["height"] = y - f["y"] + 40
    ids = []
    for p in cfg["papers"]:
        ref = p.get("ref") or {}
        name = f'{ref.get("title") or p["item"]} ({p["item"]})'
        g = d.frame(p["item"], PW, 200)
        canvas.reads_down(g)
        ids.append(g["id"])
        x, y = g["x"] + PAD, g["y"] + 40
        y += d.height(name, PPIC, 36) + 20
        d.para(x, g["y"] + 40, name, PPIC, 36)
        shots = sorted(topic.glob(f"reads/{p['id']}-*/shots/section.jpg"))
        if not shots:                       # a reading cut into paragraphs (s23): its para-P<n>.jpg, in order
            shots = sorted(topic.glob(f"reads/{p['id']}-*/shots/para-P*.jpg"),
                           key=lambda q: int(re.sub(r"\D", "", q.stem) or 0))
        for i, shot in enumerate(shots):
            y += d.picture(shot, x, y, PPIC, 1800, fid=f"{topic.name}-{p['id']}-{i}") + (16 if i < len(shots) - 1 else 50)
        if not shots:
            d.text(x, y, f"? no screenshot yet: {p['item']}", size=28, color=RED)
            y += 70
        moves = logic(topic, p["id"])
        if moves:
            y = logic_map(d, p["item"], moves, x, y) + 20
        g["height"] = y - g["y"] + 40
    rows = [[f["id"]]] + [ids[i:i + PER_ROW] for i in range(0, len(ids), PER_ROW)]
    canvas.grid(d.els, rows)
    out = topic / f"{topic.name}.excalidraw"
    drop_scaffold(out)
    d.write(out, f"hai-draw read ref/section_screens.py {topic.name}")
    from render_png import render
    render(out, out.with_suffix(".png"))
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("cmd", choices=["draw"])
    ap.add_argument("topic", type=Path)
    a = ap.parse_args(argv)
    print(draw(a.topic))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
