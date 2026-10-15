"""s13 · Labeling Task: five types in one Job: s13-labeling-task.excalidraw, drawn by this builder.

How it looks and reads: /excalidraw-studio, its principles and scripts/draw.py (frames, a map, the key point,
the density badge, stairs). The topic, its face and sessions: /haipipe-studio. A rebuild keeps whatever a person drew
on the canvas (canvas.write, a seed snapshot beside the drawing). Check it: excalidraw-studio's scripts/check.py.

Its words are the face's yaml block (s13-labeling-task.md); its pictures are shots/.

    python build_s13_labeling_task.py
"""
import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str((HERE / "../../../../plugins/haipipe-toolkit/skills/1_base/display/excalidraw-studio/scripts").resolve()))
from draw import GREY, RED, Drawing, canvas  # noqa: E402  (excalidraw-studio's helpers; canvas.write keeps a person's marks)

# every change to this drawing: (date YYMMDD, what changed, where). Each gets a green note where it changed
CHANGES = []


def words() -> dict:
    """The face's yaml block: the drawing's words."""
    text = (HERE / "s13-labeling-task.md").read_text(encoding="utf-8")
    return yaml.safe_load(re.search(r"(?ms)^```yaml\n(.*?)^```", text).group(1))


def step(d: Drawing, x: float, y: float, w: float, t: dict, dashed: bool = False) -> tuple:
    """One Task type: its name large, its task-type line, what it does, where it shows. Returns (x, y, w, h)."""
    screen = "🖥 " + t["screen"] if t.get("screen") else ""
    h = (24 + d.height(t["title"], w - 48, 40) + 12 + d.height(t["line"], w - 48, 28, code=True) + 8
         + sum(d.height(s, w - 48, 28) + 8 for s in [*t["does"], screen] if s) + 18)
    d.box(x, y, w, h, GREY if dashed else "#1e1e1e", 2.5, dashed=dashed)
    yy = d.para(x + 24, y + 22, t["title"], w - 48, 40) + 12
    yy = d.para(x + 24, yy, t["line"], w - 48, 28, code=True) + 8
    for s in t["does"]:
        yy = d.para(x + 24, yy, s, w - 48, 28) + 8
    if screen:
        d.para(x + 24, yy, screen, w - 48, 28)
    return x, y, w, h


def main():
    out = HERE / "s13-labeling-task.excalidraw"
    face = words()
    d = Drawing()

    # ① the five types, as stairs: items → building ─🔒 Handoff─▶ scanning → score; ground truth below, fenced to score
    f1 = d.frame("① A labeling Job: five Task types")
    d.heading("① One labeling Job, five Task types", face["sub"])
    d.key(40, 190, 2000, 120)
    d.para(66, 212, face["key"], 1950, 30)
    W_, X0, DX, Y0, DY = 540, 60, 600, 400, 150
    boxes = [step(d, X0 + i * DX, Y0 + i * DY, W_, t) for i, t in enumerate(face["types"])]
    for (ax, ay, aw, ah), (bx, by, bw, bh), label in zip(boxes, boxes[1:], face["arrows"]):
        turn = bx + 70
        d.line([(ax + aw + 8, ay + 60), (turn, ay + 60), (turn, by - 8)], sw=4)
        if label.startswith("🔒"):
            kh_ = d.height(label, 360, 30) + 28                   # the one crossing, on its arrow
            d.key(turn + 24, ay + 26, 400, kh_, sw=2)
            d.para(turn + 44, ay + 40, label, 360, 30)
        else:
            d.text(ax + aw + 20, ay + 14, label, 28)
    bx0, by0, bw0, bh0 = boxes[0]
    k = face["ground_truth"]
    kx, ky, kw, kh = step(d, X0, 1040, W_, {**k, "screen": ""}, dashed=True)
    d.line([(bx0 + bw0 / 2, by0 + bh0 + 8), (bx0 + bw0 / 2, ky - 8)], sw=3, dashed=True)
    d.text(bx0 + bw0 / 2 + 18, (by0 + bh0 + ky) / 2 - 18, face["relate"], 28)
    d.para(X0, ky + kh + 44, face["close"], 1500, 30)
    sx, sy, sw_, sh = boxes[-1]
    d.line([(kx + kw + 8, ky + kh / 2), (sx + sw_ / 2, ky + kh / 2), (sx + sw_ / 2, sy + sh + 8)], sw=3, dashed=True)
    d.text(kx + kw + 40, ky + kh / 2 + 10, k["fence"], 28)
    b1, b2 = boxes[1], boxes[2]                                     # today's one Page spans building and scanning
    d.box(b1[0] - 24, b1[1] - 24, b2[0] + b2[2] - b1[0] + 48, b2[1] + b2[3] - b1[1] + 48, "#1e1e1e", 1.5, dashed=True)
    d.text(b1[0] - 20, b2[1] + b2[3] + 34, face["today"], 28)
    d.text(b1[0] - 20, b2[1] + b2[3] + 72, face["unshown"], 28, RED)
    d.para(sx + sw_ / 2 + 30, sy + sh + 30, face["open"], 2520 - (sx + sw_ / 2 + 30), 30, RED)
    for i, (date, what, at) in enumerate(CHANGES):
        e = canvas.change_note(at[0], at[1], what, date, f1["id"])
        e["id"] = f"c{i}"
        d.els.append(e)
    d.badge(f1)

    # ② ③ the screens that show it, each small, explaining ①
    frames = []
    for s in face["screens"]:
        f = canvas.explains(d.frame(s["title"], 1760, 1500))
        d.heading(s["title"], s["sub"], 1680)
        hh = d.picture(HERE / s["file"], 40, 170, 1680, 1180)
        d.para(40, 170 + hh + 30, s["read"], 1680, 28)
        f["height"] = 170 + hh + 30 + d.height(s["read"], 1680, 28) + 40
        d.badge(f)
        frames.append(f)

    # ④ the words, the three real Jobs and the open points: the detail ① leaves out (principle 7)
    g = face["glossary"]
    f4 = canvas.explains(d.frame(g["title"], 1900, 1600))
    d.heading(g["title"], g["sub"], 1300)
    y = d.grid_table(40, 180, ["word", "what it means"], [{"cells": w} for w in g["words"]], [360, 1460], 26, 16)
    y = d.grid_table(40, y + 60, ["Job (dataset · label)", "📦 items", "📏 ground truth", "🏗🔍 building + scanning", "📊 score"],
                     [{"cells": j} for j in g["jobs"]], [470, 170, 560, 450, 190], 26, 16)
    d.para(40, y + 40, face["close"], 1820, 30)
    y += 40 + d.height(face["close"], 1820, 30) + 24
    for o in g["opens"]:
        y = d.para(40, y, o, 1820, 30) + 8
    f4["height"] = y + 40
    d.badge(f4)
    frames.append(f4)

    placed = canvas.stairs(d.els, [f1["id"], frames[0]["id"], frames[1]["id"], f4["id"]])
    d.fid = None                                                  # the acts and the steps between frames
    for f, act in zip(placed, ("Act 1 · the five types", "Act 2 · today, on screen", "", "Act 3 · the words, the Jobs, what is open")):
        if act:
            d.para(f["x"] - 820, f["y"] + 20, act, 760, 56)
    for a, b, words_ in ((placed[0], placed[1], "on screen today"), (placed[1], placed[2], "open its items Task")):
        x = b["x"] + 360
        d.line([(x, a["y"] + a["height"] + 14), (x, b["y"] - 14)], sw=6)
        d.text(x + 20, (a["y"] + a["height"] + b["y"]) / 2 - 24, words_, 40)
    d.write(out, "build_s13_labeling_task.py")


if __name__ == "__main__":
    main()
