"""A Section's examples topic drawn as what it is for: each published paper's same Section, a screenshot, one under the
other, so a person checks how others write it (JL 261104: "for the exmaples here, we just want to have the screenshot
intdouction to check"). No logic chains and no reference cards.

    python section_screens.py draw <topic folder>

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
SKILLS = HERE.parents[2]
sys.path.insert(0, str(SKILLS / "excalidraw/excalidraw-studio/scripts"))
sys.path.insert(0, str(SKILLS / "project/haipipe-studio/scripts"))
from draw import RED, Drawing  # noqa: E402
import canvas  # noqa: E402

W, PAD, PIC = 2400, 80, 2240


def config(topic: Path) -> dict:
    face = (topic / f"{topic.name}.md").read_text(encoding="utf-8")
    block = re.search(r"(?ms)^```yaml\n(related:.*?)^```", face)
    if not block:
        raise SystemExit(f"{topic.name}: its face has no related: yaml")
    return yaml.safe_load(block.group(1))["related"]


def draw(topic: Path) -> Path:
    topic = topic.resolve()
    cfg = config(topic)
    title = (topic / f"{topic.name}.md").read_text(encoding="utf-8").splitlines()[0]
    title = re.sub(r"^s\d+\s*·\s*", "", title).strip()
    d = Drawing()
    f = d.frame(title, W, 200)
    canvas.reads_down(f)
    x, y = f["x"] + PAD, f["y"] + 50
    d.text(x, y, title, size=46)
    y += 90
    height = d.height(cfg["key"], PIC - 60, 34)
    d.key(x, y, PIC, height + 40)
    d.para(x + 30, y + 20, cfg["key"], PIC - 60, 34)
    y += height + 90
    for p in cfg["papers"]:
        ref = p.get("ref") or {}                 # its topic first, by its full title (JL 261104: "要把每个 paper title 列一下")
        name = f'{ref.get("title") or p["item"]} ({p["item"]})'
        d.para(x, y, name, PIC, 36)
        y += d.height(name, PIC, 36) + 20
        shots = sorted(topic.glob(f"reads/{p['id']}-*/shots/section.jpg"))
        if not shots:
            d.text(x, y, f"? no screenshot yet: {p['item']}", size=28, color=RED)
            y += 90
            continue
        y += d.picture(shots[0], x, y, PIC, 1500, fid=f"{topic.name}-{p['id']}") + 80
    for line in cfg.get("open") or []:
        h = d.height("? " + str(line), PIC, 30)
        d.para(x, y, "? " + str(line), PIC, 30, color=RED)
        y += h + 24
    f["height"] = y - f["y"] + 40
    out = topic / f"{topic.name}.excalidraw"
    d.write(out, f"excalidraw-read ref/section_screens.py {topic.name}")
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
