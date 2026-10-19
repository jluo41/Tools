"""s42 · Task building procedure: s42-task-building-procedure.excalidraw, drawn by this builder.

How it looks and reads: /excalidraw-studio, its principles and scripts/draw.py. The topic, its face and sessions:
/haipipe-studio. A rebuild keeps whatever a person drew on the canvas (canvas.write, a seed snapshot beside it).
Its words are the face's yaml block (s42-task-building-procedure.md); its screens are drawn like s41's.

    python build_s42_task_building_procedure.py
"""
import random
import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str((HERE / "../../../../plugins/haipipe-toolkit/skills/1_base/excalidraw/excalidraw-studio/scripts").resolve()))
from draw import GREY, RED, Drawing, canvas  # noqa: E402

DATE = "261014"                               # the day of the changes the notes mark
CHANGES = []                                  # (date YYMMDD, what changed, (x, y)): a green note where it changed


def words() -> dict:
    text = (HERE / "s42-task-building-procedure.md").read_text(encoding="utf-8")
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
        for lane, key in ((0, "corpus"), (1, "guideline")):     # what the corpus and the guideline are after this row
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


def algorithm_frame(d: Drawing, a: dict) -> dict:
    """Ⓐ the workflow as a paper's Method writes it (s42-D08): Algorithm 1 in a ruled box, numbered lines in code,
    a gate's comment beside its line; the Method's sections on the right, each tied to its lines."""
    f = canvas.explains(d.frame(a["frame"], 2160, 1100))
    d.text(40, 22, a["frame"], 44)
    x, y, w = 40, 110, 1300
    d.line([(x, y), (x + w, y)], arrow=False, sw=3)            # the booktabs rules of an algorithm box
    d.text(x + 10, y + 14, a["caption"], 32)
    d.line([(x, y + 66), (x + w, y + 66)], arrow=False, sw=1.5)
    yy = y + 84
    for s in (a["input"], a["output"]):
        d.text(x + 10, yy, s, 28)
        yy += 46
    for i, (code, note) in enumerate(a["lines"], 1):
        d.text(x + 10, yy, f"{i:>2}:", 26, code=True)
        d.text(x + 70, yy, code, 26, code=True)
        if note:
            d.text(x + 860, yy, "▷ " + note, 26)
        yy += 40
    d.line([(x, yy + 10), (x + w, yy + 10)], arrow=False, sw=3)
    if a.get("changed"):
        mark_change(d, f, x, yy + 26, a["changed"])
        yy += 30
    sx, sy = x + w + 60, y
    for block in (a["sections"], a["notation"]):
        d.text(sx, sy + 10, block[0], 36)
        for i, s in enumerate(block[1:]):
            d.text(sx, sy + 70 + i * 44, s, 26, code=block is a["notation"] and False)
        sy += 70 + len(block[1:]) * 44 + 40
    f["height"] = max(yy, sy) + 80
    return f


def journey_frame(d: Drawing, c: dict, l: dict) -> dict:
    """Ⓑ the corpus, Run by Run (s42-D20; JL 261014: "these two can be merged"): a step header, then one row per Run:
    the 350 items after it as a bar (the final exam dashed, gold in the one slight colour), then who acts and what
    the corpus, the guideline and the labels become; a ✍ cell is a gate."""
    unit = 1.9
    widths = [250, int(c["total"] * unit) + 20, 220, 220, 220, 200, 180, 220]
    order = [0, None, 1, 2, 3, 4, 6, 7]                         # ledger columns in this table's order (None: the bar,
                                                                #   which is the corpus: its column is not repeated)
    f = canvas.reads_down(Drawing.detail(canvas.explains(d.frame(l["frame"], sum(widths) + 80, 1500))))   # one table, read down
    d.text(40, 22, l["frame"], 44)
    d.text(40, 92, l["sub"], 28)
    x0, y = 40, 150
    heads = [l["columns"][0], "the 350 items"] + [l["columns"][i] for i in order[2:]]
    d.line([(x0, y), (x0 + sum(widths), y)], arrow=False, sw=3)
    x = x0
    for col, w in zip(heads, widths):
        d.text(x + 8, y + 12, col, 26)
        x += w
    y += 56
    d.line([(x0, y), (x0 + sum(widths), y)], arrow=False, sw=1.5)
    steps = dict((i, name) for i, name in l["steps"])
    for r, (row, bar) in enumerate(zip(l["rows"], l["bars"])):
        if r in steps:                                          # the step this Run belongs to
            d.text(x0 + 8, y + 10, steps[r], 30)
            y += 46
            d.line([(x0, y), (x0 + sum(widths), y)], arrow=False, sw=0.8)
        cells = [row[i] if i is not None else "" for i in order]
        tiny = sum(d.measure(f"{c['parts'][p][0]} {n}", 20) + 10 for p, n in bar
                   if d.measure(f"{c['parts'][p][0]} {n}", 20) + 8 >= n * unit)   # counts under the bar, their width
        lines = 1 if tiny else 0
        h = max([d.height(str(v), w - 16, 24) for v, w in zip(cells, widths) if v] + [54 + lines * 24]) + 6
        x = x0
        for i, (v, w) in enumerate(zip(cells, widths)):
            if i == 1:                                          # the bar
                bx, end, narrow = x + 8, x + w - 6, []
                for part, n in bar:
                    icon, name = c["parts"][part]
                    bw = n * unit
                    d.box(bx, y + 8, bw, 46, "#1e1e1e", 2 if part != "pool" else 1, dashed=part == "sealed")
                    if part == "gold":
                        d.key(bx, y + 8, bw, 46, sw=2)
                    label = f"{icon} {n}".strip()
                    if d.measure(label, 20) + 8 < bw:
                        d.text(bx + 4, y + 20, label, 20)
                    else:
                        narrow.append((bx, label))
                    bx += bw
                if narrow:                                      # too narrow: one line under the bar, inside its column
                    total = sum(d.measure(lb, 20) + 12 for _, lb in narrow)
                    lx = min(narrow[0][0], end - total)
                    for _, lb in narrow:
                        d.text(lx, y + 56, lb, 20)
                        lx += d.measure(lb, 20) + 12
            else:
                if str(v).startswith("✍"):
                    d.key(x + 3, y + 3, w - 6, h - 6, sw=1)
                d.para(x + 8, y + 6, str(v), w - 16, 24)
            x += w
        y += h
        d.line([(x0, y), (x0 + sum(widths), y)], arrow=False, sw=0.6)
    d.line([(x0, y), (x0 + sum(widths), y)], arrow=False, sw=3)
    lx, ly = x0, y + 22                                         # the legend, then the notes
    for part, (icon, name) in c["parts"].items():
        s = f"{icon} {name}".strip() if icon else f"▭ {name}"
        if lx + d.measure(s, 26) > x0 + sum(widths):            # the legend wraps inside the frame
            lx, ly = x0, ly + 40
        d.text(lx, ly, s, 26)
        lx += d.measure(s, 26) + 44
    yy = ly + 52
    for n in c["notes"] + [l["note"]]:
        yy = d.para(x0, yy, "· " + n, sum(widths), 26) + 6
    if l.get("changed"):
        mark_change(d, f, x0, yy + 8, l["changed"])
        yy += 40
    f["height"] = yy + 50
    return f


def round_frame(d: Drawing, r: dict) -> dict:
    """Ⓒ one round, step by step (s42-D26): seven boxes in a closed loop, each its purpose, who acts and the file it
    leaves; 1 to 4 left to right, 5 to 7 back right to left, then another round or Stop."""
    f = canvas.reads_down(Drawing.room(Drawing.detail(canvas.explains(d.frame(r["frame"], 2720, 1200)))))   # loop, then tree
    d.text(40, 22, r["frame"], 44)
    d.text(40, 92, r["sub"], 28)
    W, H, GAP = 560, 300, 80
    spots = [(120 + i * (W + GAP), 190) for i in range(4)] + [(120 + (3 - i) * (W + GAP), 190 + H + 150) for i in range(3)]
    for (x, y), (name, purpose, who, leaves) in zip(spots, r["steps"]):
        gate = "✍" in who
        d.box(x, y, W, H, "#1e1e1e", 3 if gate else 2)
        if gate:
            d.key(x, y, W, H, sw=3)
        yy = d.para(x + 22, y + 16, name, W - 44, 36) + 8
        yy = d.para(x + 22, yy, purpose, W - 44, 26) + 10
        yy = d.para(x + 22, yy, who, W - 44, 24) + 8
        d.para(x + 22, yy, leaves, W - 44, 20, code=True)
    for (ax, ay), (bx, by) in zip(spots[:3], spots[1:4]):          # 1 → 2 → 3 → 4
        d.line([(ax + W + 6, ay + H / 2), (bx - 6, by + H / 2)], sw=3)
    x4, y4 = spots[3]                                               # 4 down to 5
    d.line([(x4 + W / 2, y4 + H + 6), (x4 + W / 2, spots[4][1] - 6)], sw=3)
    for (ax, ay), (bx, by) in zip(spots[4:6], spots[5:7]):          # 5 → 6 → 7, right to left
        d.line([(ax - 6, ay + H / 2), (bx + W + 6, by + H / 2)], sw=3)
    x7, y7 = spots[6]                                               # 7 back up to 1: the loop, closed
    lx = spots[0][0] - 50                                           # left of step 1, never through it
    d.line([(x7 - 6, y7 + H / 2), (lx, y7 + H / 2), (lx, spots[0][1] + H / 2), (spots[0][0] - 6, spots[0][1] + H / 2)], sw=3)
    d.para(spots[0][0], y7 + H / 2 + 20, "↺ " + r["loop"], W, 28)
    sy = y7 + H + 80
    d.line([(x7 + W / 2, y7 + H + 6), (x7 + W / 2, sy + 70), (x7 + W + 40, sy + 70)], sw=3)
    d.text(x7 + W + 56, sy + 52, r["stop"], 30)
    yy = d.para(40, sy + 150, "from " + r["from"], 2400, 26)
    if r.get("tree"):                                               # Ⓒ and Ⓓ in one: the tree under the loop
        yy = tree_table(d, r["tree"], f, yy + 60)
    if r.get("changed"):
        mark_change(d, f, 40, yy + 12, r["changed"])
        yy += 40
    f["height"] = yy + 50
    return f


def tree_table(d: Drawing, t: dict, f: dict, y: float) -> float:
    """The building Task as a tree (s42-D28), drawn under the round's loop (s42-D32): one row per Stage, Stage 3's Steps
    indented under it (├─, └─), with purpose, who acts, the Run and what it leaves; a ✍ cell is a gate. Returns the y
    after it."""
    widths = [440, 700, 460, 330, 540]
    d.text(40, y, t["frame"], 34)
    d.text(40, y + 52, t["sub"], 26)
    x0, y = 40, y + 100
    d.line([(x0, y), (x0 + sum(widths), y)], arrow=False, sw=3)
    x = x0
    for col, w in zip(t["columns"], widths):
        d.text(x + 10, y + 12, col, 28)
        x += w
    y += 58
    d.line([(x0, y), (x0 + sum(widths), y)], arrow=False, sw=1.5)
    for depth, *cells in t["rows"]:
        name = ("├─ " if depth == 1 else "└─ " if depth == 2 else "") + cells[0]
        cells = [name] + cells[1:]
        size = 28 if not depth else 24
        h = max(d.height(str(v), w - 20 - (30 if i == 0 and depth else 0), size if i == 0 else 24, code=i in (3, 4))
                for i, (v, w) in enumerate(zip(cells, widths)) if v) + 16
        x = x0
        for i, (v, w) in enumerate(zip(cells, widths)):
            if "✍" in str(v) and i == 2:
                d.key(x + 4, y + 4, w - 8, h - 8, sw=1)
            pad = 40 if i == 0 and depth else 10
            d.para(x + pad, y + 8, str(v), w - pad - 10, size if i == 0 else 24, code=i in (3, 4))
            x += w
        y += h
        d.line([(x0, y), (x0 + sum(widths), y)], arrow=False, sw=0.8 if depth else 1.5)
    d.line([(x0, y), (x0 + sum(widths), y)], arrow=False, sw=3)
    return y + 20


def reader_frame(d: Drawing, r: dict) -> dict:
    """Ⓔ how the agent reads the corpus (s42-D30): the corpus tools on the left, the search rules on the right, then the
    two guards and what changes at scale."""
    tw, rw = [470, 520, 360], [60, 400, 560]
    gap = 110
    f = canvas.reads_down(Drawing.detail(canvas.explains(d.frame(r["frame"], sum(tw) + gap + sum(rw) + 80, 1200))))
    d.text(40, 22, r["frame"], 44)
    d.text(40, 92, r["sub"], 28)

    def table(x0, y, title, cols, rows, widths, code0):
        d.text(x0, y, title, 32)
        y += 56
        d.line([(x0, y), (x0 + sum(widths), y)], arrow=False, sw=3)
        x = x0
        for c, w in zip(cols, widths):
            d.text(x + 10, y + 10, c, 26)
            x += w
        y += 50
        d.line([(x0, y), (x0 + sum(widths), y)], arrow=False, sw=1.5)
        for row in rows:
            h = max(d.height(str(v), w - 20, 24, code=code0 and i == 0) for i, (v, w) in enumerate(zip(row, widths))) + 14
            x = x0
            for i, (v, w) in enumerate(zip(row, widths)):
                d.para(x + 10, y + 7, str(v), w - 20, 24, code=code0 and i == 0)
                x += w
            y += h
            d.line([(x0, y), (x0 + sum(widths), y)], arrow=False, sw=0.8)
        d.line([(x0, y), (x0 + sum(widths), y)], arrow=False, sw=3)
        return y

    y1 = table(40, 160, r["tools_title"], r["tools_columns"], r["tools"], tw, True)
    y2 = table(40 + sum(tw) + gap, 160, r["rules_title"], r["rules_columns"], r["rules"], rw, False)
    yy = max(y1, y2) + 40
    total = sum(tw) + gap + sum(rw)
    d.text(40, yy, r["funnel_title"], 32)                      # the pick funnel: four boxes, joined by arrows
    yy += 60
    fw = (total - 3 * 80) / 4
    for i, (name, what, eye, out) in enumerate(r["funnel"]):
        fx = 40 + i * (fw + 80)
        d.box(fx, yy, fw, 170, "#1e1e1e", 2)
        d.text(fx + 20, yy + 14, name, 30)
        d.para(fx + 20, yy + 58, what, fw - 40, 24)
        d.text(fx + 20, yy + 130, eye + "  →  " + out, 24)
        if i:
            d.line([(fx - 74, yy + 85), (fx - 6, yy + 85)], sw=3)
    yy += 210
    yy = table(40, yy, r["methods_title"], r["methods_columns"], r["methods"], [300, 1100, total - 1400], True) + 30
    yy = table(40, yy, r["value_title"], r["value_columns"], r["value"], [300, 1100, total - 1400], True) + 20
    yy = d.para(40, yy, "🧮 " + r["split"], total, 26) + 24
    yy = d.para(40, yy, "🔒 " + r["guards"], total, 26) + 14
    d.key(36, yy - 4, total + 8, d.height("📏 " + r["scale"], total, 26) + 16, sw=2)
    yy = d.para(44, yy + 4, "📏 " + r["scale"], total - 8, 26) + 20
    if r.get("changed"):
        mark_change(d, f, 40, yy, r["changed"])
        yy += 40
    f["height"] = yy + 40
    return f


def guideline_frame(d: Drawing, g: dict) -> dict:
    """Ⓖ the guideline format (s42-D54): the source and its two renderings, the seven sections, one rule card with
    its four laws, and the seven pools named with what each needs."""
    f = canvas.reads_down(Drawing.room(Drawing.detail(canvas.explains(d.frame(g["frame"], 2600, 1400)))))
    d.text(40, 22, g["frame"], 44)
    d.text(40, 92, g["sub"], 28)
    y0 = 170                                                    # the source, then its two readers
    d.key(40, y0, 520, 110, sw=2)
    d.text(64, y0 + 18, g["source"], 30)
    d.text(64, y0 + 64, g["source_note"], 24)
    for i, (name, what) in enumerate(g["readers"]):
        ry = y0 + 170 + i * 150
        d.box(140, ry, 600, 110, "#1e1e1e", 1.5)
        d.text(164, ry + 18, name, 30)
        d.para(164, ry + 62, what, 560, 24)
        d.line([(100, y0 + 114), (100, ry + 55), (134, ry + 55)], sw=2.5)
    sx = 840                                                    # the seven sections
    d.text(sx, y0, g["sections_title"], 32)
    for i, (n, name, what) in enumerate(g["sections"]):
        yy = y0 + 56 + i * 52
        d.text(sx, yy, n, 26, code=True)
        d.text(sx + 70, yy, name, 26)
        d.text(sx + 330, yy, what, 24)
    cx = 1880                                                   # one rule card and its laws
    d.text(cx, y0, g["card_title"], 32)
    d.box(cx, y0 + 56, 680, len(g["card"]) * 34 + 30, "#1e1e1e", 1.5)
    for i, line in enumerate(g["card"]):
        d.text(cx + 20, y0 + 70 + i * 34, line, 22, code=True)
    ly = y0 + 56 + len(g["card"]) * 34 + 50
    for i, law in enumerate(g["laws"]):
        d.text(cx, ly + i * 38, f"{i + 1}. {law}", 24)
    py = max(y0 + 56 + 7 * 52, ly + 4 * 38) + 60                # the seven pools, named
    d.text(40, py, g["pools_title"], 32)
    widths, x0, py = [260, 520, 760, 980], 40, py + 56
    d.line([(x0, py), (x0 + sum(widths), py)], arrow=False, sw=3)
    for x, (c, w) in zip([x0 + sum(widths[:i]) for i in range(4)], zip(g["pools_columns"], widths)):
        d.text(x + 10, py + 10, c, 26)
    py += 50
    d.line([(x0, py), (x0 + sum(widths), py)], arrow=False, sw=1.5)
    for row in g["pools"]:
        for i, (v, w) in enumerate(zip(row, widths)):
            d.text(x0 + sum(widths[:i]) + 10, py + 10, v, 26, code=i == 0)
        py += 50
        d.line([(x0, py), (x0 + sum(widths), py)], arrow=False, sw=0.8)
    d.line([(x0, py), (x0 + sum(widths), py)], arrow=False, sw=3)
    py += 30
    if g.get("changed"):
        mark_change(d, f, 40, py, g["changed"])
        py += 40
    f["height"] = py + 40
    return f


def versions_frame(d: Drawing, v: dict) -> dict:
    """Ⓕ design versions (s42-D31): one box per version, left to right as the corpus grows, linked by dashed arrows
    (--->); the proposed one in the one slight colour."""
    W, GAP = 540, 110
    n = len(v["items"])
    f = Drawing.room(Drawing.detail(canvas.explains(d.frame(v["frame"], 80 + n * W + (n - 1) * GAP, 1000))))   # room between versions
    d.text(40, 22, v["frame"], 44)
    d.text(40, 92, v["sub"], 28)
    y0, boxes = 200, []
    for i, it in enumerate(v["items"]):
        x = 40 + i * (W + GAP)
        lines = [("how", it["how"]), ("cost", it["cost"]), ("fits", it["fits"]), ("risk", it["risk"])]
        title = it["name"] + ("  · proposed" if it.get("proposed") else "")
        h = 30 + d.height(title, W - 44, 30) + 12 + sum(d.height(f"{k}: {t}", W - 44, 24) + 12 for k, t in lines) + 20
        boxes.append((x, h))
    H = max(h for _, h in boxes)
    for (x, _), it in zip(boxes, v["items"]):
        d.box(x, y0, W, H, "#1e1e1e", 3 if it.get("proposed") else 1.5)
        if it.get("proposed"):
            d.key(x, y0, W, H, sw=3)
        yy = d.para(x + 22, y0 + 18, it["name"] + ("  · proposed" if it.get("proposed") else ""), W - 44, 30) + 12
        for k in ("how", "cost", "fits", "risk"):
            yy = d.para(x + 22, yy, f"{k}: {it[k]}", W - 44, 24) + 12
    for (ax, _), (bx, _) in zip(boxes, boxes[1:]):             # ---> as the corpus grows
        d.line([(ax + W + 8, y0 + H / 2), (bx - 8, y0 + H / 2)], dashed=True, sw=3)
    d.text(40, y0 - 44, "- - -▶ " + v["arrow"] + ", left to right", 26)
    yy = d.para(40, y0 + H + 40, v["note"], n * W + (n - 1) * GAP, 26) + 16
    if v.get("changed"):
        mark_change(d, f, 40, yy, v["changed"])
        yy += 40
    f["height"] = yy + 40
    return f


def main():
    out = HERE / "s42-task-building-procedure.excalidraw"
    face = words()
    d = Drawing()
    f1 = workflow_map(d, face)
    rows = []                                                   # each tab at its moments, one row per tab
    for tab in face["tabs"]:
        fs = [data_screen(d, st, face["screen"]) for st in tab["states"]]
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
    d.para(placed[0]["x"] - 820, placed[0]["y"] + 20, "Act 1 · the four steps", 760, 56)
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
    ch = face.get("changes", {})
    # the person's arrangement (s42-D27, D33): Ⓑ right of ①; the method frames left of ①, right-aligned a gap past the
    # act names: Ⓐ, under it Ⓒ (the round and the tree), under that Ⓔ - - -▶ Ⓕ
    fb = journey_frame(d, face["corpus"], {**face["ledger"], "changed": ch.get("ledger")})   # the corpus, Run by Run
    d.badge(fb)
    move(fb, placed[0]["x"] + placed[0]["width"] + 200, placed[0]["y"] - 160)
    right = placed[0]["x"] - 1000                                  # the method column ends here
    fa = algorithm_frame(d, {**face["algorithm"], "changed": ch.get("algorithm")})          # the method, as a paper writes it
    d.badge(fa)
    move(fa, right - fa["width"], placed[0]["y"])
    fr = round_frame(d, {**face["round"], "tree": face["tree"], "changed": ch.get("round")})   # the round, then the tree
    d.badge(fr)
    move(fr, right - fr["width"], fa["y"] + fa["height"] + 200)
    fe = reader_frame(d, {**face["reader"], "changed": ch.get("reader")})                  # how the corpus is read
    fv = versions_frame(d, {**face["versions"], "changed": ch.get("versions")})            # its versions, --->
    d.badge(fe)
    d.badge(fv)
    move(fv, right - fv["width"], fr["y"] + fr["height"] + 200)
    move(fe, fv["x"] - 200 - fe["width"], fv["y"])
    d.line([(fe["x"] + fe["width"] + 20, fe["y"] + 300), (fv["x"] - 20, fv["y"] + 300)], dashed=True, sw=3)
    d.text(fe["x"] + fe["width"] + 30, fe["y"] + 250, "versions", 28)
    fg = guideline_frame(d, {**face["gformat"], "changed": ch.get("gformat")})              # what a guideline holds
    d.badge(fg)
    move(fg, min(fa["x"], fr["x"]) - 200 - fg["width"], fa["y"])    # left of the method column, beside Ⓐ
    d.write(out, "build_s42_task_building_procedure.py")


if __name__ == "__main__":
    main()
