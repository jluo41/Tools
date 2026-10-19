"""s41 · Evidence procedure: s41-task-evidence-procedure.excalidraw, drawn by this builder.

How it looks and reads: /excalidraw-studio, its principles and scripts/draw.py. The topic, its face and sessions:
/haipipe-studio. A rebuild keeps whatever a person drew on the canvas (canvas.write, a seed snapshot beside it).
Its words are the face's yaml block (s41-task-evidence-procedure.md). The map and the screens are drawn the way b32 s41
draws them (its helpers, copied and adapted here). Read from disk on every build: C2's cards.yaml and proposals.md,
the output of cards.py check, each card's Task title, the draft version, and b21 s05's canvas picture.

    python build_s41_task_evidence_procedure.py
"""
import importlib.util
import random
import re
import subprocess
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parents[3]
WELLDOC = HERE.parents[4] / "WellDoc-SPACE"
CARDS_PY = TOOLS / "plugins/haipipe-toolkit/skills/1_base/evidence/haipipe-evidence/scripts/cards.py"
B21_EVIDENCE = WELLDOC / "examples-0-cowork/Project-SHIFT-Study/cowork/b21_event_cgm/studio/s04-task21-updated-draft/evidence"
B21_DRAFT = WELLDOC / "examples-0-cowork/Project-SHIFT-Study/cowork/b21_event_cgm/studio/s04-task21-updated-draft/draft"
sys.path.insert(0, str((HERE / "../../../../plugins/haipipe-toolkit/skills/1_base/excalidraw/excalidraw-studio/scripts").resolve()))
from draw import GREY, RED, Drawing, canvas  # noqa: E402

DATE = "261015"                               # the day of the changes the notes mark
CHANGES = []                                  # (date YYMMDD, what changed, (x, y)): a green note where it changed


def words() -> dict:
    text = (HERE / "s41-task-evidence-procedure.md").read_text(encoding="utf-8")
    return yaml.safe_load(re.search(r"(?ms)^```yaml\n(.*?)^```", text).group(1))


def b21_version() -> str:
    """The version of B21's current draft (its draft-version: line), or "?" when it is not on this machine."""
    for p in sorted(B21_DRAFT.glob("*-draft-v*.md")):
        m = re.search(r"(?m)^draft-version:\s*(\S+)", p.read_text(encoding="utf-8", errors="ignore"))
        if m:
            return m.group(1)
    return "?"


def load_cards():
    """The skill's own cards.py, imported from where it lives (it is the skill's code, not a copy)."""
    spec = importlib.util.spec_from_file_location("evidence_cards", CARDS_PY)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def cut_words(s: str, n: int = 78) -> str:
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


def task_title(project: Path, kind: str, source: str, cards) -> str:
    """A card's topic title: the first '# ' line of its Task page."""
    folder = cards.resolve(project, kind, source)
    for p in sorted(folder.glob("t*.md")):
        m = re.search(r"(?m)^# (.+)$", p.read_text(encoding="utf-8", errors="ignore"))
        if m:
            return m.group(1).strip()
    return source


def live_rows(kind: str) -> dict:
    """The rows of a box read from C2's real cards, the real `cards.py check` and the real proposals.md."""
    if not (B21_EVIDENCE / "cards.yaml").is_file():
        return {"?": "C2's evidence/ is not on this machine"}
    cards = load_cards()
    data = cards.load(B21_EVIDENCE / "cards.yaml")
    labelled = cards.order(data)
    project = cards.project_root(B21_EVIDENCE)
    if kind == "claims":                                        # one row per sentence: its first anchor and its kind
        seen, rows = set(), {}
        items = [(it["for"][0], it["anchor"][0], label, "need" in it) for card, label in labelled for it in card["items"] if it.get("anchor")]
        for sent, anchor, label, need in sorted(items):
            if sent in seen or len(rows) >= 9:
                continue
            seen.add(sent)
            rows[f"S{sent}"] = cut_words(f"\"{anchor}\" · {label}" + (" · needed" if need else ""))
        return rows
    if kind == "cite3":                                         # the real CITE 3 card, item by item
        for card, label in labelled:
            if card.get("source") == "b01.j21.t05":
                rows = {"Card": f"{label} · {card['source']}", "Topic": task_title(project, card["kind"], card["source"], cards)}
                for it in card["items"]:
                    rows[f"{it['run']} · S{it['for'][0]}"] = cut_words(f"\"{it['anchor'][0]}\" · fact {', '.join(it.get('fact', []))}")
                return rows
        return {"?": "CITE 3 not found"}
    if kind == "check":                                         # the script's own output, line by line
        r = subprocess.run([sys.executable, str(CARDS_PY), "check", str(B21_EVIDENCE / "cards.yaml")], capture_output=True, text=True)
        lines = [l for l in r.stdout.splitlines() if l.strip()]
        rows = {}
        for l in lines[:-1]:
            m = re.match(r"(\w+ \d+)\s+(\S+(?: \S+)?)\s+(\d+ items)", l)
            rows[m.group(1)] = f"{m.group(2):16} {m.group(3)}" if m else l
        rows["result"] = lines[-1] + f"   (exit {r.returncode})"
        return rows
    if kind == "propose":                                       # the real lines of proposals.md, shortened
        rows = {}
        for i, l in enumerate(re.findall(r"(?m)^- \[( |x)\] (.+)$", (B21_EVIDENCE / "proposals.md").read_text(encoding="utf-8"))):
            tick, text = l
            m = re.match(r"new discovery (run|task)(?: `([^`]+)`)? in `([^`]+)`.*?\((CITE \d+), [^ ]+ ([^)]+)\) · for: (.*?) · made by", text)
            where = f"{m.group(1)} in {m.group(3)}" if m and m.group(1) == "run" else f"task {m.group(2)[:3]} in {m.group(3)}" if m else ""
            rows[f"[{tick}] #{i + 1}"] = cut_words(f"{m.group(5)} · {where} · {m.group(6)}", 84) if m else cut_words(text)
        return rows
    return {}


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
        if st.get("open") and not st.get("sections"):
            yy += 70
            d.para(px + 24, yy - 20, st["open"], pw - 48, 30, RED)
            yy += 40
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
    """The Section canvas as it stands today (b21 s05), one picture, red boxes on the parts a step shows. A box is
    [x0, y0, x1, y1, label], fractions of the picture's width and height."""
    f = canvas.reads_down(canvas.explains(d.frame(st["title"], 2400, 2700)))
    d.text(40, 22, st["title"], 44)
    from PIL import Image
    pic = WELLDOC / st["shot"]
    iw, ih = Image.open(pic).size
    top = 190
    hh = d.picture(pic, 40, top, 2320, 2400)
    dw = iw * min(2320 / iw, 2400 / ih)
    for k, (x0, y0, x1, y1, label, *at) in enumerate(st["boxes"]):
        d.box(40 + x0 * dw, top + y0 * hh, (x1 - x0) * dw, (y1 - y0) * hh, RED, 6)
        if at:                                                  # the label in the picture's empty room, a line to its box
            lx, ly = 40 + at[0] * dw, top + at[1] * hh
            d.para(lx, ly, label, 640, 32, RED)
            d.line([(lx - 8, ly + 20), (40 + x1 * dw + 8, top + (y0 + y1) / 2 * hh)], sw=3, color=RED)
        else:                                                   # no room named: above the picture
            d.text(40 + x0 * dw, top - 66, label, 34, RED)
    yy = top + hh + 24
    if st.get("prompt"):
        ph = d.height(st["prompt"], 1900, 26, code=True) + 70
        d.box(40, yy, 2320, ph, "#1e1e1e", 1)
        d.text(64, yy + 12, "Prompt", 26)
        d.para(64, yy + 46, st["prompt"], 1900, 26, code=True)
        d.box(2120, yy + 14, 220, 46, "#1e1e1e", 2.5, dashed=True)
        d.text(2142, yy + 22, "Copy prompt", 24)
        yy += ph + 24
    yy = d.para(40, yy, "↑ " + st["mark"], 2320, 30, RED)
    if st.get("open"):
        yy = d.para(40, yy + 10, st["open"], 2320, 30, RED)
    f["height"] = yy + 40
    return f


def open_frame(d: Drawing, o: dict) -> dict:
    """Ⓒ what is still open: a short list in red, so nothing reads as finished that is not."""
    f = canvas.explains(d.frame(o["frame"], 1700, 700))
    d.text(40, 22, o["frame"], 44)
    y = 120
    for line in o["lines"]:
        y = d.para(40, y, line, 1600, 28, RED) + 18
    f["height"] = y + 40
    return f


def main():
    out = HERE / "s41-task-evidence-procedure.excalidraw"
    face = words()
    version = b21_version()
    d = Drawing()
    f1 = workflow_map(d, face)
    rows = []                                                   # each act at its moments, one row per act
    for tab in face["tabs"]:
        fs = []
        for st in tab["states"]:
            if st.get("shot"):
                fs.append(canvas_screen(d, st))
                continue
            for b in st.get("boxes") or []:                     # the draft's version and the real cards, from disk
                if b.get("live"):
                    b["rows"] = live_rows(b["live"])
                b["rows"] = {k: str(v).replace("<version>", version) for k, v in b["rows"].items()}
            if st.get("prompt"):
                st["prompt"] = st["prompt"].replace("<version>", version)
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
    d.para(placed[0]["x"] - 820, placed[0]["y"] + 20, "Act 1 · the map: find, cards, check, propose, show", 760, 56)
    above, x_start, lead = placed[0], placed[0]["x"] + 520, placed[0]
    for tab, fs in rows:                                        # an act's moments are peers: a row, left to right
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
    fb = folders_frame(d, face["folders"])                      # Ⓑ where the files sit, right of ①
    d.badge(fb)
    move(fb, placed[0]["x"] + placed[0]["width"] + 200, placed[0]["y"])
    fo = open_frame(d, face["open"])                            # Ⓒ what is still open, under Ⓑ
    d.badge(fo)
    move(fo, fb["x"], fb["y"] + fb["height"] + 200)
    d.write(out, "build_s41_task_evidence_procedure.py")


if __name__ == "__main__":
    main()
