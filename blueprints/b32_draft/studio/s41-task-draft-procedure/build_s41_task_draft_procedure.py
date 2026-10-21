"""s41 · Task draft procedure: s41-task-draft-procedure.excalidraw, drawn by this builder.

How it looks and reads: /excalidraw-studio, its principles and scripts/draw.py. The topic, its face and sessions:
/haipipe-studio. A rebuild keeps whatever a person drew on the canvas (canvas.write, a seed snapshot beside it).
Its words are the face's yaml block (s41-task-draft-procedure.md). The map, the pass loop, the tree and the screens
are drawn the way b15 s42-task-building-procedure draws them (its helpers, copied here, as s42 copied s41's).
Read from disk on every build: the old draft tabs and the step each became (OLD_SUBS in servers/workbench/workbench-task-draft/task_draft.py), the version of
B21's draft, and b21 s05's Section canvas.

    python build_s41_task_draft_procedure.py
"""
import random
import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parents[3]
WELLDOC = HERE.parents[4] / "WellDoc-SPACE"
FRAME_PY = TOOLS / "plugins/haipipe-toolkit/servers/workbench/workbench-task-draft/task_draft.py"   # the draft Task layout (s41-D15)
B21_DRAFT = WELLDOC / "examples-0-cowork/Project-SHIFT-Study/cowork/b21_event_cgm/studio/s04-task21-updated-draft/draft"
sys.path.insert(0, str((HERE / "../../../../plugins/haipipe-toolkit/skills/1_base/excalidraw/excalidraw-studio/scripts").resolve()))
from draw import GREY, RED, Drawing, canvas  # noqa: E402

DATE = "261015"                               # the day of the changes the notes mark
CHANGES = []                                  # (date YYMMDD, what changed, (x, y)): a green note where it changed


def words() -> dict:
    text = (HERE / "s41-task-draft-procedure.md").read_text(encoding="utf-8")
    return yaml.safe_load(re.search(r"(?ms)^```yaml\n(.*?)^```", text).group(1))


def today_tabs() -> dict:
    """{old tab: the step tab it became}, as the screen maps an old link: OLD_SUBS in task_draft.py, read as text
    (the step tabs were built 2026-10-20, s41-D29)."""
    src = FRAME_PY.read_text(encoding="utf-8")
    block = re.search(r"(?ms)^OLD_SUBS = \{(.*?)\}", src).group(1)
    return dict(re.findall(r'"([^"]+)":\s*"([^"]+)"', block))


def b21_version() -> str:
    """The version of B21's current draft (its draft-version: line), or "?" when it is not on this machine."""
    for p in sorted(B21_DRAFT.glob("*-draft-v*.md")):
        m = re.search(r"(?m)^draft-version:\s*(\S+)", p.read_text(encoding="utf-8", errors="ignore"))
        if m:
            return m.group(1)
    return "?"


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
    LX, GAP, CGAP, RH, BH = 420, 40, 160, 190, 74               # CGAP: room after the state lanes for the loops
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
            if len(io) > 2:                                     # the skill page that does this step, under its output
                d.text(x + 30, y + BH + 30, io[2], 16, color=RED if io[2].startswith("❗") else GREY, code=True)
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
    for r, row in enumerate(face["map"]):                        # the loops, drawn closed: a pass on the left, a round on the right
        if row.get("loop"):
            back = row["loop_to"] if "loop_to" in row else \
                next(i for i in range(r, -1, -1) if (face["map"][i].get("step") or "").startswith("🔁"))
            tx, ty, tw, th = placed[back][row.get("loop_to_cell", 0)]
            if row.get("loop_side") == "right":                     # the big loop: out past the last lane, back in from the right
                sx, sy, sw_, sh = placed[r][-1]
                rx = f["width"] - 30
                d.line([(sx + sw_ + 6, sy + 37), (rx, sy + 37), (rx, ty + 37), (tx + tw + 6, ty + 37)], sw=3)
                d.para(lane_x(3), ty + 47, row["loop"], rx - lane_x(3) - 20, 26)
                continue
            sx, sy, sw_, sh = placed[r][0]
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



def today_frame(d: Drawing, t: dict, tabs: dict) -> dict:
    """Ⓐ the draft tabs before the step tabs, each with the step tab it became (read from task_draft.py's OLD_SUBS;
    a tab that stayed, from the face's map)."""
    f = canvas.reads_down(canvas.explains(d.frame(t["frame"], 1700, 1400)))
    d.text(40, 22, t["frame"], 44)
    d.para(40, 92, t["sub"], 1600, 28)
    rows, last = [], None
    for space, names in t["spaces"].items():
        for tab in names:
            rows.append({"cells": [space if space != last else "", tab, tabs.get(tab) or t["map"].get(tab, "❓ not placed yet")]})
            last = space
    y = d.grid_table(40, 200, t["columns"], rows, [460, 520, 620], size=30, pad=22)
    y = d.para(40, y + 30, t["note"], 1600, 28)
    f["height"] = y + 50
    return f


def folders_frame(d: Drawing, b: dict) -> dict:
    """Ⓑ the Block's folders behind the Task's first and last tabs: a real folder tree (principle ④), its notes."""
    f = canvas.explains(d.frame(b["frame"], 1700, 1100))
    d.text(40, 22, b["frame"], 44)
    d.para(40, 92, b["sub"], 1600, 28)
    tree = b["tree"].rstrip()
    d.text(40, 190, tree, 28, code=True)
    y = 190 + (tree.count("\n") + 1) * 36 + 40
    for n in b["notes"]:
        y = d.para(40, y, n, 1600, 28, RED if n.startswith("❓") else None) + 14
    f["height"] = y + 40
    return f


WAS = re.compile(r"(?:was the skill|Replaces the retired|from the retired(?: skill)?|Folded from the retired)\s+`?([a-z0-9-]+)`?")


def inside(skill: Path, t: dict) -> list:
    """What a skill holds that was once its own skill, read from disk: a ref page whose first lines say "was the skill
    X", a skill kept inside it (a SKILL.md below it), and the face's `extra` lines. [(label, note, kind)]."""
    out = [(lab, note, "extra") for lab, note in t["extra"].get(skill.name, [])]
    for page in sorted((skill / "ref").glob("*.md")) if (skill / "ref").is_dir() else []:
        head = "\n".join(page.read_text(encoding="utf-8", errors="replace").splitlines()[:8])
        if (m := WAS.search(head)):
            out.append((f"ref/{page.name}", f"was {m[1]}", "page"))
    for sk in sorted(skill.rglob("SKILL.md")):
        if sk.parent != skill and "_archive" not in sk.parts:
            out.append((sk.parent.relative_to(skill).as_posix(), "a skill kept inside it", "skill"))
    return out


def skills_tree_frames(d: Drawing, t: dict) -> list:
    """Ⓓ Ⓔ the skills as their folders, read from disk: `1_base/<family>/` in the first column, its skills stacked in
    the next (a level holds many skills), and what each skill now holds one column further: the pages that were skills
    of their own until 2026-10-16 and the skills kept inside it (JL 261016: "每个 style 算作一列 … 按照这个 folder 的
    structure 把这个画出来"; "where are the old things? … you can unfolder more"). Two frames, each one screen."""
    base = TOOLS / "plugins/haipipe-toolkit/skills/1_base"
    FW, SW, KW, GAP, RH = 240, 470, 470, 46, 64

    pos = {}

    def node(x, y, w, label, sub, kind=""):
        pos[label] = (x, y, w)
        if label in t["key"]:
            d.key(x, y, w, RH - 10)
        else:
            d.box(x, y, w, RH - 10, sw=1 if kind == "skill" else 2)   # a skill kept inside: a thinner box
        d.text(x + 14, y + 4, label, 26)
        if sub:
            d.text(x + 14, y + 33, sub, 20, GREY)

    def link(px, py, pw, cx, cy, trunk):
        mid = (RH - 10) / 2
        if abs(cy - py) < 1:
            d.line([(px + pw + 4, py + mid), (cx - 6, cy + mid)], sw=2)
        else:
            d.line([(trunk, py + RH - 10), (trunk, cy + mid), (cx - 6, cy + mid)], sw=2)

    def first_line(py):
        import ast
        try:
            doc = ast.get_docstring(ast.parse(py.read_text(encoding="utf-8"))) or ""
        except SyntaxError:
            doc = ""
        line = (doc.strip().splitlines() or [""])[0]
        return line if len(line) <= 44 else line[:42].rstrip() + "…"

    def code_tree(x, y, rel):
        """The server folder behind the screens: its sub-folders, `workbench-task-draft/` opened file by file (each with its
        docstring's first line), the shared files in one box."""
        root = TOOLS / "plugins/haipipe-toolkit" / rel
        node(x, y, FW, rel.split("/")[-1] + "/", rel.rsplit("/", 1)[0] + "/ · the code")   # short, to fit its box
        dirs = sorted((p for p in root.iterdir() if p.is_dir() and not p.name.startswith(("_", ".", "tests"))),
                      key=lambda p: (not p.name.startswith("workbench-task-"), p.name))   # a Task type's folder first
        pys = sorted(p.name for p in root.glob("*.py"))
        yy, right = y, x + FW
        for dr in dirs:
            sx = x + FW + GAP
            files = [p for p in dr.rglob("*") if p.is_file() and "__pycache__" not in p.parts]
            task_dir = dr.name.startswith("workbench-task-")
            node(sx, yy, SW, dr.name + "/", f"a Task type's screen · {len(files)} files" if task_dir else f"{len(files)} files")
            link(x, y, FW, sx, yy, x + 26)
            right, ky = max(right, sx + SW), yy
            if task_dir:                                                  # a Task type's screen, opened up file by file
                kids = [(c.name + "/", f"{sum(1 for f in c.rglob('*') if f.is_file() and '__pycache__' not in f.parts)} files")
                        for c in sorted(dr.iterdir()) if c.is_dir() and not c.name.startswith(("_", "."))]
                kids += [(c.name, first_line(c)) for c in sorted(dr.glob("*.py"))]
                for label, note in kids:
                    kx = sx + SW + GAP
                    node(kx, ky, KW, label, note, "skill")
                    link(sx, yy, SW, kx, ky, sx + SW - 30)
                    right, ky = max(right, kx + KW), ky + RH
            yy = max(yy + RH, ky)
        node(x + FW + GAP, yy, SW, f"{len(pys)} shared .py", ", ".join(pys[:3]) + " …")
        link(x, y, FW, x + FW + GAP, yy, x + 26)
        return right, yy + RH

    def family(x, y, spec):
        if spec.startswith("code:"):
            return code_tree(x, y, spec[5:])
        fam, _, only = spec.partition(":")
        names = [n for n in only.split(",") if n] or None
        folder = base.parent / fam if fam.startswith("2_theme/") else base / fam   # a theme's skills too (s41-D15)
        skills = sorted((p for p in folder.iterdir() if (p / "SKILL.md").is_file() and (names is None or p.name in names)),
                        key=lambda p: (p.name not in t["key"], p.name))
        node(x, y, FW, fam.split("/")[-1] + "/", "" if names is None else f"{len(names)} of its skills")
        yy, right = y, x + FW
        for sk in skills:
            sx = x + FW + GAP
            if sk.name not in t["roles"]:                       # every skill says what it does (JL 261016)
                print(f"s41: no role for {sk.name} in the face's skills_tree.roles")
            node(sx, yy, SW, sk.name, t["roles"].get(sk.name, ""))
            link(x, y, FW, sx, yy, x + 26)
            right, ky = max(right, sx + SW), yy
            for label, note, kind in inside(sk, t):
                kx = sx + SW + GAP
                node(kx, ky, KW, label, note, kind)
                link(sx, yy, SW, kx, ky, sx + SW - 30)
                right, ky = max(right, kx + KW), ky + RH
            yy = max(yy + RH, ky)
        return right, yy

    frames = []
    for spec in t["frames"]:
        f = canvas.large(canvas.explains(d.frame(spec["frame"], 2800, 1600)))   # larger than a screen on purpose (JL 261016: "A large frame for all")
        pos.clear()
        d.text(40, 22, spec["frame"], 44)
        x, bottom = 40, 110
        for column in spec["columns"]:                          # a column of families, stacked
            y, right = 110, x
            for fam in column:
                r, b = family(x, y, fam)
                right, y = max(right, r), b + 40
            bottom, x = max(bottom, y), right + 80
        for names, target, words in t.get("links", []):     # a manual and the code it explains, dashed
            src = next((pos[n] for n in names if n in pos), None)
            if src and target in pos:
                (sx_, sy_, sw_), (tx_, ty_, _) = src, pos[target]
                mid_y = sy_ + 27                                # under the code column's first box, then up into its target
                d.line([(sx_ + sw_ + 6, mid_y), (tx_ - 22, mid_y), (tx_ - 22, ty_ + 27), (tx_ - 8, ty_ + 27)],
                       RED, dashed=True, sw=2)
                d.text(sx_ + sw_ + 24, mid_y + 6, words, 24, RED)
        yy = d.para(40, bottom + 10, t["out"], 2700, 26)
        f["width"] = max(x - 40, 1800)
        f["height"] = yy + 50
        frames.append(f)
    return frames


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


def canvas_screen(d: Drawing, st: dict) -> dict:
    """The Revise tab's Result: the Section canvas as it stands today (b21 s05), one picture, its parts named in red."""
    f = canvas.reads_down(canvas.explains(d.frame(st["title"], 2400, 2700)))
    d.text(40, 22, st["title"], 44)
    from PIL import Image
    pic = WELLDOC / st["shot"]
    iw, ih = Image.open(pic).size
    top = 190 if st.get("fills") else 110                       # room above the picture for the red label
    hh = d.picture(pic, 40, top, 2320, 2400)
    if st.get("fills"):                                         # the column this step fills: a red box on the screen
        dw = iw * min(2320 / iw, 2400 / ih)
        a, b = st["fills"]
        d.box(40 + a * dw, top - 10, (b - a) * dw, hh + 20, RED, 6)
        d.text(40 + a * dw, top - 66, "↓ " + st["fills_label"], 36, RED)
    yy = d.para(40, top + hh + 24, "↑ " + st["mark"], 2320, 30, RED)
    if st.get("open"):
        yy = d.para(40, yy + 10, st["open"], 2320, 30, RED)
    f["height"] = yy + 40
    return f


def main():
    out = HERE / "s41-task-draft-procedure.excalidraw"
    face = words()
    version = b21_version()
    d = Drawing()
    f1 = workflow_map(d, face)
    rows = []                                                   # each tab at its moments, one row per tab
    for tab in face["tabs"]:
        fs = []
        for st in tab["states"]:
            if st.get("shot"):
                fs.append(canvas_screen(d, st))
                continue
            for b in st.get("boxes") or []:                     # the draft's version, read from disk
                b["rows"] = {k: str(v).replace("<version>", version) for k, v in b["rows"].items()}
            fs.append(data_screen(d, st, face["screen"]))
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
    d.para(placed[0]["x"] - 820, placed[0]["y"] + 20, "Act 1 · Studio, four stages, Delivery", 760, 56)
    above, x_start, lead = placed[0], placed[0]["x"] + 520, placed[0]
    for tab, fs in rows:                                        # a tab's moments are peers: a row, left to right
        top = above["y"] + above["height"] + GAP
        move(fs[0], x_start, top)
        for l_, r_ in zip(fs, fs[1:]):
            move(r_, l_["x"] + l_["width"] + 1500, top)       # room for the arrow's words and two skill boxes
        d.para(fs[0]["x"] - 1700, top + 380, tab["act"], 760, 56)
        d.para(fs[0]["x"] - 1700, top + 540, tab["key"], 700, 30)
        for (l_, r_), w in zip(zip(fs, fs[1:]), [st["arrow"] for st in tab["states"] if st.get("arrow")]):
            y = top + 300
            d.line([(l_["x"] + l_["width"] + 14, y), (r_["x"] - 14, y)], sw=6)
            d.text(l_["x"] + l_["width"] + 30, y - 60, w, 40)
        x = fs[0]["x"] - 130                                    # down beside the screen, then into its left side
        y0_ = lead["y"] + lead["height"] + 14
        d.line([(x, y0_), (x, top + 300), (fs[0]["x"] - 14, top + 300)], sw=6)
        d.text(x - 30 - d.measure(tab["step_arrow"], 40), (y0_ + top) / 2, tab["step_arrow"], 40)
        above = max(fs, key=lambda f: f["y"] + f["height"]) | {"x": fs[0]["x"]}
        lead = fs[0]
        x_start += 520                                          # acts step down and right: stairs between rows
        for st, f in zip(tab["states"], fs):                   # the skills behind each screen, outside it
            skill_boxes(d, f, st.get("skills") or [])
    fa = today_frame(d, face["today"], today_tabs())            # today's tabs, right of ①
    d.badge(fa)
    move(fa, placed[0]["x"] + placed[0]["width"] + 200, placed[0]["y"])
    fb = folders_frame(d, face["folders"])                      # the Block's folders, under Ⓐ
    d.badge(fb)
    move(fb, fa["x"], fa["y"] + fa["height"] + 200)
    (fd,) = skills_tree_frames(d, face["skills_tree"])       # Ⓓ the skills and the code, one large frame
    d.badge(fd)
    move(fd, fa["x"] + max(fa["width"], fb["width"]) + 200, fa["y"])   # right of Ⓐ and Ⓑ, tops aligned (JL 261019)
    d.write(out, "build_s41_task_draft_procedure.py")


if __name__ == "__main__":
    main()
