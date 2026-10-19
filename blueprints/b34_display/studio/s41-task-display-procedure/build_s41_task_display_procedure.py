"""s41 · Display procedure: s41-task-display-procedure.excalidraw, drawn by this builder.

How it looks and reads: /excalidraw-studio, its principles and scripts/draw.py. The topic, its face and sessions:
/haipipe-studio. A rebuild keeps whatever a person drew on the canvas (canvas.write, a seed snapshot beside it).
Its words are the face's yaml block (s41-task-display-procedure.md). The map, the screens and the pictures are
drawn the way b32 s41-task-draft-procedure draws them (its helpers, copied here, not imported).
Read from disk on every build: the Overview Figure picture and b21 s05's canvas picture.

    python build_s41_task_display_procedure.py
"""
import random
import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parents[3]
WELLDOC = HERE.parents[4] / "WellDoc-SPACE"
sys.path.insert(0, str((HERE / "../../../../plugins/haipipe-toolkit/skills/1_base/excalidraw/excalidraw-studio/scripts").resolve()))
from draw import GREY, RED, Drawing, canvas  # noqa: E402

DATE = "261016"                               # the day of the changes the notes mark
CHANGES = []                                  # (date YYMMDD, what changed, (x, y)): a green note where it changed


def words() -> dict:
    text = (HERE / "s41-task-display-procedure.md").read_text(encoding="utf-8")
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


def data_screen(d: Drawing, st: dict, sc: dict) -> dict:
    """Work › 1 · Data at one moment (s41-D09), drawn as the workbench draws it: the bars, the step, its chip, then
    the three lines that say what the data is, and the prompt once they are written. A red mark says what the
    person does here; a dashed box is new on this screen."""
    f = canvas.ui_frame(canvas.explains(d.frame(st["title"], 1760, 1000)))
    if st.get("sections") or len(st.get("boxes") or []) > 2:  # the tab read top to bottom: cards, or a session
        canvas.reads_down(f)
    d.text(40, 22, st["title"], 44)
    if st.get("changed"):
        mark_change(d, f, 40, 78, st["changed"])
    x0, y0, w = 40, 110, 1680
    buttons(d, x0 + 24, y0 + 20, ["Guide", "Studio", "Block", "j01_<job>", sc["task"], "Delivery"], sc["task"])
    d.text(x0 + 24, y0 + 84, sc["line"], 30)
    buttons(d, x0 + 24, y0 + 136, ["Description", "Report", "Work", "Runs"], "Work")
    buttons(d, x0 + 24, y0 + 190, sc["tabs"], st.get("tab", sc["tabs"][0]))
    px, py, pw = x0 + 24, y0 + 320, w - 48
    d.text(px, py - 62, "Operation", 36)                       # what a person does, then what the step made
    step = st["step"]
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
            mark_end = d.para(px + 24, yy + ph + 20, "↑ " + st["mark"], pw - 48, 30, RED)
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


def mark_change(d: Drawing, f: dict, x: float, y: float, what: str, n: int = 0) -> None:
    """A green change note where the change is (haipipe-studio: "✎ <date> <what>"); its id unique per frame."""
    e = canvas.change_note(x, y, what, DATE, f["id"], size=22)
    e["id"] = f"note-{f['id']}-{n}"
    d.els.append(e)


def workflow_map(d: Drawing, face: dict) -> dict:
    """① the main frame: a workflow map (s42-D07). One row per moment, read down; four actor lanes and the corpus
    (s42-D35); each box with its input above and its output below; each row's cells joined left or right, each row to
    the next from the box's left foot, the round loop drawn closed; the corpus lane says what the corpus holds."""
    f = canvas.reads_down(Drawing.room(Drawing.detail(d.frame(face["heading"][0], 2800, 1600))))
    d.heading(*face["heading"])
    d.key(40, 180, 2720, 70)
    d.para(66, 196, face["key"], 2680, 30)
    top_low = 274
    for i, k in enumerate(("problem", "novelty")):             # why it matters, before how it runs (s42-D09)
        bx = 40 + i * 1380
        h = d.height(face[k], 1290, 30) + 40
        d.box(bx, 274, 1340, h, "#1e1e1e", 2)
        d.para(bx + 24, 292, face[k], 1290, 30)
        top_low = max(top_low, 274 + h)
    LX, GAP, CGAP, RH, BH = 420, 40, 160, 170, 74               # CGAP: room after the state lanes for the loops
    Y0 = max(560, top_low + 150)                                  # the lanes start below the taller box
    LWS = face["lane_w"]
    lane_x = lambda i: LX + sum(LWS[:i]) + i * GAP + (CGAP - GAP if i > 1 else 0)
    bottom = Y0 + len(face["map"]) * RH
    for i, name in enumerate(face["lanes"]):
        d.text(lane_x(i) + 20, Y0 - 86, name, 34)
        if i and i != 2:                                        # the state lanes are set off by the loops' room
            d.line([(lane_x(i) - GAP / 2, Y0 - 96), (lane_x(i) - GAP / 2, bottom)], arrow=False, dashed=True, sw=1)
    placed = []                                                 # (x, y, w, h) per cell, in reading order
    state = {0: [], 1: []}                                      # each state box: its centre x, top, bottom
    for r, row in enumerate(face["map"]):
        y = Y0 + r * RH
        if row.get("step"):                                     # a long step name wraps in its column
            sy = d.para(40, y + 8, row["step"], LX - 50, 34)
            d.text(80, sy + 4, row.get("screens", ""), 28)
        cells = []
        for lane, words_, *io in row["cells"]:
            w = d.measure(words_, 28) + 48
            x = lane_x(lane) + (LWS[lane] - w) / 2
            gate = words_.startswith("✍")
            d.box(x, y, w, BH, "#1e1e1e", 3 if gate else 1.5, dashed=words_.startswith("🔍"))
            if gate:
                d.key(x, y, w, BH, sw=3)
            d.text(x + 24, y + 20, words_, 28)
            if io:                                              # what it takes, above; what it leaves, below
                d.text(x + 30, y - 32, "in: " + io[0], 22)
                d.text(x + 30, y + BH + 6, "out: " + io[1], 22)
            cells.append((x, y, w, BH))
        for (ax, ay, aw, ah), (bx, by, bw, bh) in zip(cells, cells[1:]):   # within a row: left or right
            if bx > ax:
                d.line([(ax + aw + 6, ay + 37), (bx - 6, by + 37)], sw=3)
            else:
                d.line([(ax - 6, ay + 37), (bx + bw + 6, by + 37)], sw=3)
        for lane, key in ((0, "text"), (1, "plan")):            # what the text and the plan are after this row
            if row.get(key):
                cw = d.measure(row[key], 26) + 40
                cx = lane_x(lane) + (LWS[lane] - cw) / 2
                d.box(cx, y + 6, cw, BH - 12, "#1e1e1e", 1.5, dashed=True)
                d.text(cx + 20, y + 22, row[key], 26)
                state[lane].append((cx + cw / 2, y + 6, y + BH - 6))
        placed.append(cells)
    for boxes in state.values():                                 # the state over time: each box down to the next
        for (ax, _, ab), (bx, bt, _) in zip(boxes, boxes[1:]):
            d.line([(ax, ab + 4), (bx, bt - 4)], sw=1.5)
    for r, i, word in face.get("marks") or []:                  # where each novelty happens: beside its box, off the arrow
        x, y, w, h = placed[r][i]
        d.text(x - 8 - d.measure(word, 30), y + 18 if i == 0 else y - 34, word, 30)
    for prev, nxt in zip(placed, placed[1:]):                    # each row to the next: from the left foot, across, down
        ax, ay, aw, ah = prev[-1]
        bx, by, bw, bh = nxt[0]
        mid = ay + ah + (RH - ah) / 2
        d.line([(ax + 14, ay + ah + 4), (ax + 14, mid), (bx + 14, mid), (bx + 14, by - 4)], sw=3)
    for r, row in enumerate(face["map"]):                        # the round loop, drawn closed on the left
        if row.get("loop"):
            back = row["loop_to"] if "loop_to" in row else \
                next(i for i in range(r, -1, -1) if (face["map"][i].get("step") or "").startswith("🔁"))
            sx, sy, sw_, sh = placed[r][0]
            tx, ty, tw, th = placed[back][0]
            lx = lane_x(2) - 50
            d.line([(sx - 6, sy + 37), (lx, sy + 37), (lx, ty + 37), (tx - 6, ty + 37)], sw=3)
            d.para(lane_x(1) + LWS[1] + 8, (sy + ty) / 2, row["loop"], lx - lane_x(1) - LWS[1] - 14, 26)   # in the loop's room
    for r, row in enumerate(face["map"]):                        # the round's rows, boxed in each state lane
        if row.get("span"):
            back = next(i for i in range(r, -1, -1) if (face["map"][i].get("step") or "").startswith("🔁"))
            top, low = Y0 + back * RH - 14, Y0 + r * RH + BH + 14
            for lane in (0, 1):
                d.box(lane_x(lane) - 4, top, LWS[lane] + 8, low - top, "#1e1e1e", 2)
                d.text(lane_x(lane) + 4, top - 30, row["span"], 24)
    for i, c in enumerate(face.get("changes", {}).get("map", [])):   # a note beside what it changed
        if "at" in c:
            x, y = c["at"]
        elif c.get("under") == "boxes":
            x, y = 40, top_low + 10
        elif "lane" in c:
            x, y = lane_x(c["lane"]), Y0 - 40
        else:
            x, y = 40, Y0 + c["row"] * RH + c["dy"]
        mark_change(d, f, x, y, c["text"], i)
    sy_ = bottom + 50                                           # the symbols: each size and budget named once
    d.text(40, sy_, face["symbols"]["title"], 34)
    half = (len(face["symbols"]["rows"]) + 1) // 2
    for j, (sym, means) in enumerate(face["symbols"]["rows"]):
        cx, cy = 40 + (j // half) * 1360, sy_ + 64 + (j % half) * 44
        d.text(cx, cy, sym, 28, code=True)
        d.text(cx + 220, cy, means, 28)
    f["height"] = sy_ + 64 + half * 44 + 50
    d.badge(f)
    return f



def skills_tree_frame(d: Drawing, t: dict) -> dict:
    """Ⓓ how the skills work: one door, then each helper a step down and to the right (a stair tree), what it does in
    its box, the folder it writes beside it, what was merged into it under it (JL 261016: "a new frame to use the
    stair tree to show how does it work"; it replaces b32 s21)."""
    f = canvas.reads_down(canvas.explains(d.frame(t["frame"], 2400, 1600)))
    d.text(40, 22, t["frame"], 44)
    BW, BH, STEP_X, STEP_Y, y0 = 760, 120, 150, 210, 140
    last = None
    for k, st in enumerate(t["steps"]):
        x, y = 40 + k * STEP_X, y0 + k * STEP_Y
        d.box(x, y, BW, BH, sw=4 if k == 0 else 2)
        d.text(x + 24, y + 16, st["skill"], 34)
        d.text(x + 24, y + 64, st["does"], 32, GREY)
        d.text(x + BW + 40, y + 22, st["folder"], 30, code=True)
        d.text(x + BW + 40, y + 70, "was: " + st["was"], 26, GREY)
        if last:                                                # down from the step above, then right into this one
            lx, ly = last
            d.line([(lx + 50, ly + BH), (lx + 50, y + BH / 2), (x - 6, y + BH / 2)], sw=3)
        last = (x, y)
    y = y0 + len(t["steps"]) * STEP_Y + 20
    y = d.para(40, y, t["out"], 2100, 30)
    f["height"] = y + 50
    return f


def skill_boxes(d: Drawing, f: dict, skills: list) -> None:
    """Beside a screen, outside it: on the left the skill that makes it, `[skill] ──▶`; on the right the one that
    reads or checks it, `◀── [skill]`; each box says what was merged into it (JL 261016)."""
    BW, gap = 600, 80
    for sk in skills:
        h = 84 + Drawing.height(sk["note"], BW - 40, 26)
        y = f["y"] + f["height"] - h - 120
        x = f["x"] - gap - BW if sk["side"] == "left" else f["x"] + f["width"] + gap
        person = sk["skill"] == "you"
        d.box(x, y, BW, h, sw=2, dashed=person)               # a person's part is dashed: no skill does it
        d.text(x + 20, y + 16, sk["skill"], 40)
        d.para(x + 20, y + 72, sk["note"], BW - 40, 26, GREY)
        if sk["side"] == "left":
            d.line([(x + BW + 6, y + h / 2), (f["x"] - 10, y + h / 2)], sw=4)
        else:
            d.line([(x - 6, y + h / 2), (f["x"] + f["width"] + 10, y + h / 2)], sw=4)



def homes_frame(d: Drawing, t: dict) -> dict:
    """Ⓐ where displays live today: one table, the new home last."""
    f = canvas.reads_down(canvas.explains(d.frame(t["frame"], 2300, 900)))
    d.text(40, 22, t["frame"], 44)
    d.para(40, 92, t["sub"], 2200, 28)
    rows = [{"cells": r} for r in t["rows"]]
    y = d.grid_table(40, 220, t["columns"], rows, [520, 760, 900], size=30, pad=22)
    y = d.para(40, y + 30, t["note"], 2200, 28, RED)
    f["height"] = y + 50
    return f


def folders_frame(d: Drawing, b: dict) -> dict:
    """Ⓑ / ⑤ one unit's folder: a real one beside the one Display1 would be (real folders, so a tree), notes under."""
    f = canvas.explains(d.frame(b["frame"], 2400, 1100))
    d.text(40, 22, b["frame"], 44)
    d.para(40, 92, b["sub"], 2300, 28)
    t1, t2 = b["tree"].rstrip(), b["tree2"].rstrip()
    d.text(40, 190, t1, 28, code=True)
    d.text(1240, 190, t2, 28, code=True)
    y = 190 + (max(t1.count("\n"), t2.count("\n")) + 1) * 36 + 40
    for n in b["notes"]:
        y = d.para(40, y, n, 2300, 28, RED if n.startswith("❓") else None) + 14
    f["height"] = y + 40
    return f


def canvas_screen(d: Drawing, st: dict) -> dict:
    """A real picture on a frame: fills = [x0, x1, (y0, y1)] as shares of the picture, a red box and a label above."""
    f = canvas.reads_down(canvas.explains(d.frame(st["title"], 2400, 2700)))
    d.text(40, 22, st["title"], 44)
    from PIL import Image
    pic = WELLDOC / st["shot"]
    iw, ih = Image.open(pic).size
    top = 190 if st.get("fills") else 110
    hh = d.picture(pic, 40, top, 2320, 2400)
    if st.get("fills"):
        sc = min(2320 / iw, 2400 / ih)
        dw, dh = iw * sc, ih * sc
        x0, x1, y0, y1 = st["fills"]
        d.box(40 + x0 * dw, top + y0 * dh - 10, (x1 - x0) * dw, (y1 - y0) * dh + 20, RED, 6)
        d.text(40, top - 66, "↓ " + st["fills_label"] + " (red box, bottom right)", 36, RED)
    yy = d.para(40, top + hh + 24, "↑ " + st["mark"], 2320, 30, RED)
    if st.get("open"):
        yy = d.para(40, yy + 10, st["open"], 2320, 30, RED)
    f["height"] = yy + 40
    return f


def main():
    out = HERE / "s41-task-display-procedure.excalidraw"
    face = words()
    d = Drawing()
    f1 = workflow_map(d, face)
    rows = []
    for tab in face["tabs"]:
        fs = []
        for st in tab["states"]:
            if st.get("shot"):
                fs.append(canvas_screen(d, st))
            elif st.get("tree"):
                fs.append(folders_frame(d, {**face["folders"], "frame": st["title"]}))
            else:
                fs.append(data_screen(d, st, face["screen"]))
        for f in fs:
            d.badge(f)
        rows.append((tab, fs))
    order = [f1["id"]] + [f["id"] for _, fs in rows for f in fs]
    placed = canvas.stairs(d.els, order)
    d.fid = None

    def move(f, x, y):
        mx, my = x - f["x"], y - f["y"]
        for e in d.els:
            if e is f or e.get("frameId") == f["id"]:
                e["x"], e["y"] = e["x"] + mx, e["y"] + my

    GAP = 260
    d.para(placed[0]["x"] - 820, placed[0]["y"] + 20, "Act 1 · the map", 760, 56)
    above, x_start, lead = placed[0], placed[0]["x"] + 520, placed[0]
    for tab, fs in rows:
        top = above["y"] + above["height"] + GAP
        move(fs[0], x_start, top)
        for l_, r_ in zip(fs, fs[1:]):
            move(r_, l_["x"] + l_["width"] + 440, top)
        d.para(fs[0]["x"] - 960, top + 380, tab["act"], 760, 56)
        d.para(fs[0]["x"] - 960, top + 540, tab["key"], 700, 30)
        for (l_, r_), w in zip(zip(fs, fs[1:]), [st["arrow"] for st in tab["states"] if st.get("arrow")]):
            y = top + 300
            d.line([(l_["x"] + l_["width"] + 14, y), (r_["x"] - 14, y)], sw=6)
            d.text(l_["x"] + l_["width"] + 30, y - 60, w, 40)
        x = fs[0]["x"] - 130
        y0_ = lead["y"] + lead["height"] + 14
        d.line([(x, y0_), (x, top + 300), (fs[0]["x"] - 14, top + 300)], sw=6)
        d.text(x - 30 - d.measure(tab["step_arrow"], 40), (y0_ + top) / 2, tab["step_arrow"], 40)
        above = max(fs, key=lambda f: f["y"] + f["height"]) | {"x": fs[0]["x"]}
        lead = fs[0]
        x_start += 520
    fa = homes_frame(d, face["homes"])
    d.badge(fa)
    move(fa, placed[0]["x"] + placed[0]["width"] + 200, placed[0]["y"])
    fb = folders_frame(d, face["folders"])
    d.badge(fb)
    move(fb, fa["x"], fa["y"] + fa["height"] + 200)
    d.write(out, "build_s41_task_display_procedure.py")


if __name__ == "__main__":
    main()
