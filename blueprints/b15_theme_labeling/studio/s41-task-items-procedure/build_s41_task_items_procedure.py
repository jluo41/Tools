"""s41 · Task items procedure: s41-task-items-procedure.excalidraw, drawn by this builder.

How it looks and reads: /excalidraw-studio, its principles and scripts/draw.py. The topic, its face and sessions:
/haipipe-studio. A rebuild keeps whatever a person drew on the canvas (canvas.write, a seed snapshot beside it).
Its words are the face's yaml block (s41-task-items-procedure.md); its pictures are shots/.

    python build_s41_task_items_procedure.py
"""
import random
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


def buttons(d: Drawing, x: float, y: float, names: list, on: str = "", size: int = 22) -> float:
    """A row of the workbench's buttons; the open one bold (canvas.colour_ui makes it blue). Returns the x after it."""
    for n in names:
        w = d.measure(n, size) + 28
        d.box(x, y, w, size + 18, "#1e1e1e", 2.5 if n == on else 1)
        d.text(x + 14, y + 8, n, size)
        x += w + 10
    return x


def data_screen(d: Drawing, st: dict) -> dict:
    """Work › 1 · Data at one moment (s41-D09), drawn as the workbench draws it: the bars, the step, its chip, then
    the three lines that say what the data is, and the prompt once they are written. A red mark says what the
    person does here; a dashed box is new on this screen."""
    f = canvas.ui_frame(canvas.explains(d.frame(st["title"], 1760, 1000)))
    if st.get("sections"):                                     # the tab read top to bottom, its cards a list
        canvas.reads_down(f)
    d.text(40, 22, st["title"], 44)
    x0, y0, w = 40, 110, 1680
    buttons(d, x0 + 24, y0 + 20, ["Guide", "Studio", "Block", "j01_<job>", "Task · t01 · items", "Delivery"],
            "Task · t01 · items")
    d.text(x0 + 24, y0 + 84, "Labeling · Block b01 · Task t01 · <dataset> as items", 30)
    buttons(d, x0 + 24, y0 + 136, ["Description", "Report", "Work", "Runs"], "Work")
    buttons(d, x0 + 24, y0 + 190, ["1 · Data", "2 · Items", "3 · Embedding"], st.get("tab", "1 · Data"))
    px, py, pw = x0 + 24, y0 + 320, w - 48
    d.text(px, py - 62, "Operation", 36)                       # what a person does, then what the step made
    if not st.get("notes"):
        d.els.append(canvas.change_note(px + 200, py - 54, "Operation · Result; titles only", "261014", f["id"], size=22)
                     | {"id": f"note-op-{f['id']}"})
    step = st.get("step", "📥 Step 1 · Data")
    if "folded" in st:                                         # a done step folds to one line; opened on a click
        d.text(px + 24, py + 20, "▸ " + step, 32)
        buttons(d, px + 24 + d.measure("▸ " + step, 32) + 30, py + 18, [st["chip"]], st["chip"], 24)
        yy = py + 50
    else:
        d.text(px + 24, py + 20, step, 32)
        buttons(d, px + 24, py + 72, [st["chip"]], st["chip"], 24)
        yy = py + 140
    for b in [] if "folded" in st else st.get("boxes") or [{"title": st["box"], "rows": st["data"]}]:
        bh = len(b["rows"]) * 44 + 76
        d.box(px + 24, yy, pw - 48, bh, "#1e1e1e", 1, dashed=b.get("dashed", False))
        d.text(px + 48, yy + 16, b["title"], 28)
        for i, (k, v) in enumerate(b["rows"].items()):
            d.text(px + 48, yy + 62 + i * 44, k, 26)
            d.text(px + 230, yy + 62 + i * 44, v, 26, code=k in ("Folder", "File") or str(v).endswith((".jsonl", "/")))
        if b.get("button"):                                    # a person's button on the box
            bw_ = d.measure(b["button"], 26) + 40
            d.box(px + pw - bw_ - 48, yy + 14, bw_, 46, "#1e1e1e", 2.5, dashed=True)
            d.text(px + pw - bw_ - 28, yy + 23, b["button"], 26)
            if b.get("mark"):
                d.para(px + pw - bw_ - 560, yy + 22, b["mark"] + " →", 480, 28, RED)
        yy += bh + 24
    yy += 6
    if st.get("prompt") and "folded" not in st:
        notes = st.get("notes") or ["user feedback: notes, a row, an image"]
        nh = len(notes) * 38 + 30                               # the notes: the person's feedback, copied with it
        ph = d.height(st["prompt"], pw - 360, 24, code=True) + 70 + nh + 16
        d.box(px + 24, yy, pw - 48, ph, "#1e1e1e", 1)
        d.text(px + 48, yy + 14, "Prompt", 24)
        ny = d.para(px + 48, yy + 50, st["prompt"], pw - 360, 24, code=True) + 16
        d.box(px + 48, ny, pw - 96, nh, "#1e1e1e", 1.5, dashed=True)
        for i, n in enumerate(notes):
            d.text(px + 68, ny + 14 + i * 38, n, 24)
        bx = px + pw - 260
        d.box(bx, yy + 14, 200, 44, "#1e1e1e", 2.5, dashed=True)
        d.text(bx + 22, yy + 22, "Copy prompt", 24)
        if not st.get("sections"):
            d.para(bx - 560, yy + ph + 12, "↑ " + st["mark"], 760, 30, RED)
        yy += ph + (20 if st.get("sections") else 60)
    d.box(px, py, pw, yy - py + 20, "#1e1e1e", 1)              # the step's box closes after its prompt
    if st.get("sections"):                                     # below the step, not in it: one card per topic,
        yy += 50                                               #   full width, a list read down (s41-D09)
        d.text(px, yy, "Result", 36)
        yy += 66
    for c in st.get("sections", []):
        ch = 72 + (560 if c.get("map") else 0)                 # a card is its title only (no small grey words)
        d.box(px, yy, pw, ch, "#1e1e1e", 1.5, dashed=c.get("new", False))
        d.text(px + 24, yy + 16, "▸ " + c["t"], 32)
        if c.get("map"):                                       # the map opened: its buttons, axes, a hovered dot
            buttons(d, px + 40, yy + 84, ["2-D", "3-D", "Spin", "+", "−", "Reset"], "2-D", 22)
            mx, my, mw, mh = px + 40, yy + 150, 700, 380
            d.line([(mx, my), (mx, my + mh), (mx + mw, my + mh)], arrow=False, sw=2)
            d.text(mx + mw - 150, my + mh + 6, "t-SNE 1 →", 22)
            d.text(mx + 10, my - 30, "↑ t-SNE 2", 22)
            rnd = random.Random(7)
            centres = [(110, 140), (300, 90), (500, 200), (220, 270), (600, 120)]
            for g, (cx_, cy_) in enumerate(centres):
                for _ in range(26):
                    x_, y_ = cx_ + rnd.gauss(0, 34), cy_ + rnd.gauss(0, 28)
                    d.el("ellipse", mx + 20 + x_, my + y_, 12, 12, strokeColor="#1e1e1e")
            tx, ty = mx + mw + 60, my + 20                         # the hover box: the whole item
            d.box(tx, ty, 560, 196, "#1e1e1e", 1.5)
            d.text(tx + 16, ty + 12, "<item id> · G3", 24)
            d.text(tx + 16, ty + 52, "Person: <every earlier turn>", 22)
            d.text(tx + 16, ty + 86, "AI: …  Person: …", 22)
            d.box(tx + 12, ty + 126, 536, 54, "#1e1e1e", 1)
            d.text(tx + 28, ty + 140, "<the judged reply, whole>", 22)
            d.line([(mx + 620, my + 120), (tx - 8, ty + 60)], sw=2, color=RED)
            d.para(tx, ty + 214, "hover: the whole item · click: it opens below", 560, 26, RED)
            d.els.append(canvas.change_note(tx, ty + 260, "2-D · 3-D · axes · hover", "261014", f["id"], size=22)
                         | {"id": f"note-map-{f['id']}"})
        if c.get("button"):                                    # a button on the card, new on this screen
            bw_ = d.measure(c["button"], 26) + 40
            d.box(px + pw - bw_ - 24, yy + 16, bw_, 46, "#1e1e1e", 2.5, dashed=True)
            d.text(px + pw - bw_ - 4, yy + 25, c["button"], 26)
        yy += ch + 18
    d.box(x0, y0, w, yy - y0 + 50, "#1e1e1e", 1)
    if st.get("sections"):
        yy = d.para(40, yy + 80, "↑ " + st["mark"], 1680, 30, RED)
        if st.get("open"):
            yy = d.para(40, yy + 10, st["open"], 1680, 30)
        f["height"] = yy + 40
    else:
        f["height"] = yy + 90
    return f


def shot_screen(d: Drawing, st: dict) -> dict:
    """The tab once its Run is done: the real screen, and in red what the Run put there."""
    f = canvas.explains(d.frame(st["title"], 1760, 1500))
    d.text(40, 22, st["title"], 44)
    hh = d.picture(HERE / st["file"], 40, 110, 1680, 1180)
    yy = d.para(40, 110 + hh + 24, "↑ " + st["mark"], 1680, 30, RED)
    if st.get("open"):
        yy = d.para(40, yy + 10, st["open"], 1680, 30)
    f["height"] = yy + 40
    return f


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
    rows = []                                                   # each tab at its moments, one row per tab
    for key in ("data_tab", "items_tab", "embed_tab"):
        tab = face[key]
        fs = [shot_screen(d, st) if st.get("file") else data_screen(d, st) for st in tab["states"]]
        for f in fs:
            d.badge(f)
        rows.append((tab, fs))
    order = [f1["id"]] + [f["id"] for _, fs in rows for f in fs]
    placed = canvas.stairs(d.els, order)
    d.fid = None

    def move(f, x, y):                                          # a frame and everything drawn in it
        mx, my = x - f["x"], y - f["y"]
        for e in d.els:
            if e is f or e.get("frameId") == f["id"]:
                e["x"], e["y"] = e["x"] + mx, e["y"] + my

    GAP = 260
    d.para(placed[0]["x"] - 820, placed[0]["y"] + 20, "Act 1 · the three steps", 760, 56)
    above, x_start, lead = placed[0], placed[0]["x"] + 520, placed[0]
    for n, (tab, fs) in enumerate(rows):                        # a tab's moments are peers: a row, left to right
        top = above["y"] + above["height"] + GAP
        move(fs[0], x_start, top)
        for l_, r_ in zip(fs, fs[1:]):
            move(r_, l_["x"] + l_["width"] + 440, top)        # room for the arrow's words
        d.para(fs[0]["x"] - 960, top + 380, tab["act"], 760, 56)
        d.para(fs[0]["x"] - 960, top + 540, tab["key"], 700, 30)
        for (l_, r_), w in zip(zip(fs, fs[1:]), [st["arrow"] for st in tab["states"] if st.get("arrow")]):
            y = top + 300
            d.line([(l_["x"] + l_["width"] + 14, y), (r_["x"] - 14, y)], sw=6)
            d.text(l_["x"] + l_["width"] + 30, y - 60, w, 40)
        x = fs[0]["x"] - 130                                    # down beside the screen, then into its left side,
        y0_ = lead["y"] + lead["height"] + 14                   #   never across a frame's name
        d.line([(x, y0_), (x, top + 300), (fs[0]["x"] - 14, top + 300)], sw=6)
        d.text(x - 30 - d.measure(tab["step_arrow"], 40), (y0_ + top) / 2, tab["step_arrow"], 40)
        above = max(fs, key=lambda f: f["y"] + f["height"]) | {"x": fs[0]["x"]}
        lead = fs[0]
        x_start += 520                                          # acts step down and right: stairs between rows
    d.write(out, "build_s41_task_items_procedure.py")


if __name__ == "__main__":
    main()
