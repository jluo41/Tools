"""The nine sNN of b35 j02's UI cells (s11 to s19): how the Studio part shows on a Block, a Job and a Task page, in its
Report, Work and Studio, each drawn in haipipe-studio's five parts (scripts/five_parts.py), as b16's paper_ui_cells.py
and b17's work_ui_cells.py draw theirs (JL 261031: "please add more subgroup of the UI ... to direct others how to make
the UI for the report and work").

A cell's Design is the real page, never a redrawn one (shot by shoot_screens.py into `<cell>/screen.png`), with the
cell's Rules beside it and its first open question in red. Everything is read from the cell's face, so a rule changes
in the face and this is rerun:

    .venv/bin/python studio_ui_cells.py            every cell
    .venv/bin/python studio_ui_cells.py s13        one cell
"""
import base64
import json
import re
import sys
import textwrap
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = next(p for p in HERE.parents if (p / "plugins/haipipe-toolkit").is_dir())
sys.path.insert(0, str(TOOLS / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))
from five_parts import *  # noqa: E402,F401,F403  (the helpers and build())
from five_parts import _el  # noqa: E402
import five_parts  # noqa: E402

VERB = {"report": "Report · check", "work": "Work · do", "studio": "Studio · think"}
PAGE = {"block": "b35_studio", "job": "j02_studio_pages", "task": "t02_block_page"}
SHOT_W = 760                                              # the screen's width in the drawing


def section(face: str, name: str) -> list:
    """The numbered lines under a face's `Name` / `----` heading."""
    m = re.search(rf"(?ms)^{name}\n-+\n(.*?)(?:\n\S[^\n]*\n-+\n|\Z)", face)
    return re.findall(r"(?m)^\d+\.\s+(.+)$", m.group(1)) if m else []


def field(face: str, key: str) -> str:
    m = re.search(rf"(?m)^\*\*{key}:\*\*\s*(.+)$", face)
    return m.group(1).strip() if m else ""


def wrap(words: str, width: int) -> str:
    return "\n".join(textwrap.wrap(words, width))


def embed(drawing: Path, shot: Path, eid: str) -> None:
    """Put the real screen into the drawing as one image (its file named after the cell, never a hash), under the
    "A ·" label: five_parts moves and scales the Design after design() returns, so the label says where it landed."""
    from PIL import Image
    w0, h0 = Image.open(shot).size
    doc = json.loads(drawing.read_text(encoding="utf-8"))
    at = {e["id"]: e for e in doc["elements"]}
    a, b = at["scrT"], at["rulT"]
    k = (b["x"] - a["x"]) / (SHOT_W + 50)                  # how much the Design grew
    x, y, w = a["x"], a["y"] + a["height"] + 12 * k, SHOT_W * k
    h = w * h0 / w0
    fid = f"{drawing.parent.name}-screen"
    doc["elements"].append(_el("image", eid, x, y, w, h, INK, "transparent", fileId=fid, status="saved",
                               scale=[1, 1], crop=None, strokeWidth=1))
    data = base64.b64encode(shot.read_bytes()).decode()
    doc["files"] = {**(doc.get("files") or {}), fid: {"id": fid, "mimeType": "image/png", "created": 1,
                                                       "dataURL": f"data:image/png;base64,{data}"}}
    drawing.write_text(json.dumps(doc, ensure_ascii=False) + "\n", encoding="utf-8")


def screen_card(drawing: Path, shot: Path) -> Path:
    """The card picture of a UI cell: the top of its real screen, at the card's size (five_parts.card shows only the
    Idea and Now, which say nothing about a screen)."""
    from PIL import Image
    png = drawing.with_suffix(".png")
    im = Image.open(shot).convert("RGB")
    w, h = 838, 519
    im = im.resize((w, round(im.height * w / im.width)))
    im.crop((0, 0, w, min(h, im.height))).save(png)
    return png


def build(topic: Path) -> Path:
    topic = Path(topic).resolve()
    m = re.match(r"s(\d+)-(block|job|task)-ui-(report|work|studio)$", topic.name)
    nn, level, part = m.group(1), m.group(2), m.group(3)
    face = (topic / f"{topic.name}.md").read_text(encoding="utf-8")
    rules, asks = section(face, "Rules"), section(face, "Open")
    a = "a " + level.capitalize()
    spec = {"title": f"{level.capitalize()} UI · {VERB[part]}: the Studio on {a} page",
            "why": {"question": f"what shows in {a}'s {part.capitalize()}?",
                    "notes": [f"where an sNN shows in its {part.capitalize()}", "every Theme builds it the same"],
                    "quote": "JL 261031: \"to direct others how to make the UI for the report and work\""},
            "what": {"head": f"② what s{nn} hands over: the rules", "icon": "page", "name": "delivery/ui/", "type": "ui",
                     "deck_why": f"stays in s{nn}'s delivery/deck/, so anyone gets it in a minute",
                     "parts": [("page", f"ui/{level}-{part}", f"the Studio in {a}'s {part.capitalize()}",
                                (topic / "delivery" / "ui").is_dir() and any((topic / "delivery" / "ui").iterdir()))]},
            "job": topic.parent.parent,
            "target": "servers/workbench/focus_page.py (the shared page)",
            "missing": []}
    shot = topic / "screen.png"
    h = round(900 * SHOT_W / 920)

    def design():
        els = text("scrT", 690, 280, f"A · the real page: {PAGE[level]} › {part.capitalize()} (5623)", 18, TITLE)
        if not shot.is_file():
            els += text("scrN", 690, 320, "no screen yet: run shoot_screens.py", 16, INK)
        x = 690 + SHOT_W + 50
        els += text("rulT", x, 280, "B · the rules", 18, TITLE)
        y = 320
        for i, r in enumerate(rules, 1):
            words = wrap(f"{i}. {r}", 46)
            els += text(f"rul{i}", x, y, words, 16, INK)
            y += 22 * (words.count("\n") + 1) + 16
        if asks:
            els += sticky("askD", x + 190, max(y + 70, 320 + h - 70), 380, 96, wrap(asks[0], 44), 15, -0.02, RED, RE)
        return els

    out = five_parts.build(topic, spec, design, shift=1150)
    if shot.is_file():
        embed(out, shot, "screen")
        screen_card(out, shot)                              # its card is the real screen, the point of a UI cell
    return out


if __name__ == "__main__":
    want = sys.argv[1:]
    for cell in sorted(HERE.glob("t0[234]_*/s1[1-9]-*-ui-*/")):
        if not want or cell.name.split("-")[0] in want:
            build(cell)
