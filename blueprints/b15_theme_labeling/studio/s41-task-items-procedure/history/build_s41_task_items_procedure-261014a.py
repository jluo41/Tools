"""s41 · Task items procedure: s41-task-items-procedure.excalidraw, drawn by this builder.

How it looks and reads: /excalidraw-studio, its principles and scripts/draw.py. The topic, its face and sessions:
/haipipe-studio. A rebuild keeps whatever a person drew on the canvas (canvas.write, a seed snapshot beside it).
Its words are the face's yaml block (s41-task-items-procedure.md); its pictures are shots/.

    python build_s41_task_items_procedure.py
"""
import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str((HERE / "../../../../plugins/haipipe-toolkit/skills/1_base/excalidraw/excalidraw-studio/scripts").resolve()))
from draw import GREY, RED, Drawing, canvas  # noqa: E402

CHANGES = []                                  # (date YYMMDD, what changed, (x, y)): a green note where it changed


def words() -> dict:
    text = (HERE / "s41-task-items-procedure.md").read_text(encoding="utf-8")
    return yaml.safe_load(re.search(r"(?ms)^```yaml\n(.*?)^```", text).group(1))


def step(d: Drawing, x: float, y: float, w: float, t: dict, dashed: bool = False) -> tuple:
    """One step: its name large, its Run, what it does, the tab it fills. Returns (x, y, w, h)."""
    lines = [*t["does"], ("🖥 " + t["tab"]) if t.get("tab") else ""]
    h = (24 + d.height(t["title"], w - 48, 40) + 12 + d.height(t["run"], w - 48, 28, code=True) + 8
         + sum(d.height(s, w - 48, 28) + 8 for s in lines if s) + 18)
    d.box(x, y, w, h, GREY if dashed else "#1e1e1e", 2.5, dashed=dashed)
    yy = d.para(x + 24, y + 22, t["title"], w - 48, 40) + 12
    yy = d.para(x + 24, yy, t["run"], w - 48, 28, code=True) + 8
    for s in lines:
        if s:
            yy = d.para(x + 24, yy, s, w - 48, 28) + 8
    return x, y, w, h


def main():
    out = HERE / "s41-task-items-procedure.excalidraw"
    face = words()
    d = Drawing()
    f1 = d.frame("① The items Task: three steps")
    d.heading("① The items Task: three steps", "one dataset's raw rows become the items a person labels")
    d.key(40, 190, 1760, 120)
    d.para(66, 212, face["key"], 1710, 30)
    W_, X0, DX, Y0, DY = 540, 60, 600, 400, 170
    boxes = [step(d, X0 + i * DX, Y0 + i * DY, W_, t) for i, t in enumerate(face["steps"])]
    for (bx, by, bw, bh), t in zip(boxes, face["steps"]):        # a green note under each step that changed
        if t.get("changed"):
            d.els.append(canvas.change_note(bx, by + bh + 8, t["changed"], "261014", f1["id"], size=22))
    boxes.append(step(d, X0 + 3 * DX, Y0 + 3 * DY, W_ - 60, face["then"], dashed=True))
    for (ax, ay, aw, ah), (bx, by, bw, bh), label in zip(boxes, boxes[1:], face["arrows"]):
        turn = bx + 70
        d.line([(ax + aw + 8, ay + 60), (turn, ay + 60), (turn, by - 8)], sw=4)
        d.text(ax + aw + 20, ay + 14, label, 28, code=True)
    sx = 1880                                                    # one tab's shape, beside the key point
    d.box(sx, 190, 620, 300, "#1e1e1e", 1.5)
    yy = 206
    for i, s in enumerate(face["shape"]):
        yy = d.para(sx + 24, yy, s, 580, 34 if i == 0 else 28) + 8
    yy = d.para(X0, Y0 + 3 * DY + boxes[-1][3] + 40, face["rule"], 1100, 30)
    if face.get("rule_changed"):                                   # its green note right under it
        d.els.append(canvas.change_note(X0, yy + 6, face["rule_changed"], "261014", f1["id"], size=22))
        yy += 40
    d.para(X0, yy + 14, face["open"], 1100, 30, RED)
    for i, (date, what, at) in enumerate(CHANGES):
        e = canvas.change_note(at[0], at[1], what, date, f1["id"])
        e["id"] = f"c{i}"
        d.els.append(e)
    d.badge(f1)
    frames = []
    for s in face["screens"]:
        f = canvas.explains(d.frame(s["title"], 1760, 1500))
        d.heading(s["title"], "", 1680)
        hh = d.picture(HERE / s["file"], 40, 130, 1680, 1180)
        d.para(40, 130 + hh + 30, s["read"], 1680, 28)
        f["height"] = 130 + hh + 30 + d.height(s["read"], 1680, 28) + 40
        d.badge(f)
        frames.append(f)
    placed = canvas.stairs(d.els, [f1["id"], *[f["id"] for f in frames]])
    d.fid = None
    for f, act in zip(placed, ("Act 1 · the three steps", "Act 2 · the steps on screen, dices350", "", "")):
        if act:
            d.para(f["x"] - 820, f["y"] + 20, act, 760, 56)
    for a, b, w in ((placed[0], placed[1], "on screen"), (placed[1], placed[2], "Step 2"), (placed[2], placed[3], "as a result")):
        x = b["x"] + 360
        d.line([(x, a["y"] + a["height"] + 14), (x, b["y"] - 14)], sw=6)
        d.text(x + 20, (a["y"] + a["height"] + b["y"]) / 2 - 24, w, 40)
    d.write(out, "build_s41_task_items_procedure.py")


if __name__ == "__main__":
    main()
