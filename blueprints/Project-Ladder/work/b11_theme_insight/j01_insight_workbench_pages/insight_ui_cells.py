"""The nine sNN of b11 j01 · The insight pages, level by level: one per level (Board, Job, Task) and section (Report,
Work, Studio), each drawn in haipipe-studio's five parts (scripts/five_parts.py). Copied from b15 j01's
labeling_ui_cells.py, itself copied from b16 j01's paper_ui_cells.py (the same 3 x 3 in every theme Block). Each sNN's
builder is `build(Path(__file__).parent)`: its cell is found by its folder name (s51-block-ui-report → block, report).

A cell's Design is its page's views, lettered A, B, C …, each drawn as the same full screen (window, title and section
word, view buttons with that view in orange, its sections as heading bars with one line each), the open question in
red under them. A view is settled one round at a time; a settled view's screen is written to delivery/ui/ (AGREED).

Insight's ladder (haipipe-insight ref/insight-ladder.md, plan C): a Board is one dataset and its data freezes (F1, F2);
a Job is one analysis plan (AP, the Prototype's release pN) on one data freeze (vM); a Task is one question (D, I, K or
W level); a hard Run is one cut (r01_full, r02_<cut> …). Names are placeholders (<dataset>, <d>): the real Boards hold
one person's health data, and Tools is public.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = next(p for p in HERE.parents if (p / "plugins/haipipe-toolkit").is_dir())
sys.path.insert(0, str(TOOLS / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))
from five_parts import *  # noqa: E402,F401,F403  (the helpers and build())
from five_parts import _el  # noqa: E402
from canvas import change_note  # noqa: E402
import five_parts  # noqa: E402

VERB = {"report": "Report", "work": "Work", "studio": "Studio"}
BOARD, JOB, TASK = "Insight-<dataset>", "j03_p2_<d>v2", "t10_K01_control-and-timing"
PAGE = {"block": (BOARD, f"examples-5-design/ProjI-<topic>/insight/{BOARD}"),
        "job": (JOB, f"examples-5-design/…/insight/{BOARD}/{JOB}"),
        "task": (TASK, f"examples-5-design/…/{BOARD}/{JOB}/{TASK}")}
LETTERS = "ABCDEFGH"
W, CW, X0 = 780, 640, 70               # a screen, its content column, where it starts (the rails are hidden: short lines)
CRUMB = {"block": f"<SPACE> › examples-5-design › ProjI-<topic> › insight › {BOARD}",
         "job": f"<SPACE> › examples-5-design › ProjI-<topic> › insight › {BOARD} › {JOB}",
         "task": f"<SPACE> › examples-5-design › ProjI-<topic> › insight › {BOARD} › {JOB} › {{name}}"}
GOAL = {"block": "Purpose: what this dataset can and cannot say, one Job per analysis plan × data freeze",
        "job": "Goal: analysis plan AP2 on data freeze F2, every question answered at its level",
        TASK: "Aim: answer K01 at the Knowledge level, from its cuts, checked by another agent"}
LEFT = {"block": (BOARD, "  j01_p1_<d>v1", "  j03_p2_<d>v2"),
        "job": (JOB, "  t01_D01_extract-and-clock", "  t05_I01_glucose-control", "  t10_K01_control-and-timing",
                "  t15_W01_first-focus", "j01_p1_<d>v1"),
        "task": ("t01_D01_extract-and-clock", "t05_I01_glucose-control", TASK, "t14_K05_awake-asleep-pooling",
                 "t15_W01_first-focus")}
RIGHT = ("Report", "Work", "Studio", "Interactions", "Delivery", "Timeline", "Files")

# ── the screen's parts, one name each (haipipe-ui: path, title-&-section, view-button-list, goal-line, view-caption,
# content, left-rail, right-rail) ─────────────────────────────────────────────────────────────────────────────────
def window(eid, x, y, w, h, url):
    els = [_el("rectangle", eid, x, y, w, h, INK, "#ffffff", roundness={"type": 3})]
    els += line(eid + "_bar", [(x, y + 28), (x + w, y + 28)], ROOM, 1)
    return els + [_el("ellipse", f"{eid}_d{k}", x + 10 + k * 14, y + 9, 9, 9, ROOM, ROOM) for k in range(3)] + \
        text(eid + "_url", x + 60, y + 7, url, 12, BODY)


def head(eid, x, y, name, section, views, on=0):
    """The title-&-section, then the view-button-list, the open view in orange."""
    els = text(eid + "_t", x, y, name, 20, INK) + text(eid + "_s", x + 9.6 * len(name) + 18, y + 4, VERB[section], 15, ROOM)
    cx = x
    for k, v in enumerate(views):
        w = 12 + 8 * len(v)
        els += [_el("rectangle", f"{eid}_v{k}", cx, y + 38, w, 24, OR if k == on else ROOM,
                    "#fff4e6" if k == on else "#ffffff", roundness={"type": 3})] + text(f"{eid}_v{k}_t", cx + 6, y + 42, v, 12, INK)
        cx += w + 8
    return els


def rails(eid, x, y, level, name, section):
    """Both rails are hidden until hovered (JL 261031: "you know this is the railing, right? by default, it is
    hidden"): each shows only as pale short lines, one per page (left) or section (right), no words; the open one a
    little darker."""
    els = []
    here = {"block": BOARD, "job": JOB}.get(level) or name
    for k, w in enumerate(LEFT[level]):
        indent = 6 if w.startswith("  ") else 0
        els += line(f"{eid}_l{k}", [(x + 16 + indent, y + 50 + 12 * k), (x + 40, y + 50 + 12 * k)],
                    INK if w.strip() == here else "#dee2e6", 2)
    for k, s in enumerate(RIGHT):
        els += line(f"{eid}_r{k}", [(x + W - 40, y + 50 + 12 * k), (x + W - 16, y + 50 + 12 * k)],
                    OR if s == VERB[section] else "#dee2e6", 2)
    return els


def topic_row(eid, x, y, w, addr, words, stage):
    els = [_el("rectangle", eid, x, y, w, 64, ROOM, "#ffffff", roundness={"type": 3})]
    els += [_el("rectangle", eid + "_p", x + 10, y + 10, 70, 44, ROOM, "#f1f3f5")]
    els += text(eid + "_a", x + 92, y + 8, addr, 13, TITLE) + text(eid + "_w", x + 92, y + 28, words, 11, BODY)
    return els + text(eid + "_s", x + w - 110, y + 8, stage, 12, GR) + text(eid + "_v", x + 92, y + 44, "Slides · Draw · Mind map", 11, INK)


def secbar(eid, x, y, w, title, words, verbs=()):
    """A section as a box: its heading, then its content inside the box, its verbs (at most three) on the right."""
    els = ([_el("rectangle", eid, x, y, w, box_h(words), ROOM, "#ffffff", roundness={"type": 3})]
           + text(eid + "_t", x + 12, y + 8, title, 13, TITLE) + text(eid + "_w", x + 12, y + 34, words, 12, INK))
    cx = x + w - 12
    for k, v in enumerate(reversed(verbs[:3])):
        bw = 16 + 8 * len(v)
        cx -= bw
        els += [_el("rectangle", f"{eid}_b{k}", cx, y + 8, bw, 24, "#1864ab", "#ffffff", roundness={"type": 3})]
        els += text(f"{eid}_b{k}_t", cx + 8, y + 12, v, 12, "#1864ab")
        cx -= 8
    return els


def box_h(words):
    return 44 + 18 * (words.count("\n") + 1)


def is_topic(sec):
    return len(sec) == 3 and isinstance(sec[2], str)



# ── a Task view's sections, each drawn as what it is (the view tables below hold their words) ───────────────────────────
BLUE = "#1864ab"


def _btns(eid, x, y, verbs):
    """Verb buttons, right-aligned so they end at x."""
    els, cx = [], x
    for k, v in enumerate(reversed(verbs)):
        bw = 16 + 7.5 * len(v)
        cx -= bw
        els += [_el("rectangle", f"{eid}{k}", cx, y, bw, 24, BLUE, "#ffffff", roundness={"type": 3})]
        els += text(f"{eid}{k}_t", cx + 8, y + 5, v, 11, BLUE)
        cx -= 8
    return els


def k_big(eid, x, y, w, words, state):
    col = OR if state.startswith("waiting") else (GR if state in ("done", "kept apart") else BODY)
    return text(eid + "_w", x + 4, y, words, 18, INK) + (text(eid + "_s", x + 4, y + 28, state, 12, col) if state else [])


def k_kv(eid, x, y, w, rows, verbs):
    els = _btns(eid + "_b", x + w, y, verbs)
    for k, (key, val) in enumerate(rows):
        els += text(f"{eid}{k}k", x + 4, y + 4 + 22 * k, key, 12, BODY) + text(f"{eid}{k}v", x + 110, y + 4 + 22 * k, val, 12, INK)
    return els


def k_tiles(eid, x, y, w, items):
    tw = (w - 10 * (len(items) - 1)) / len(items)
    els = []
    for k, (big_, small) in enumerate(items):
        tx = x + k * (tw + 10)
        els += [_el("rectangle", f"{eid}{k}", tx, y, tw, 52, ROOM, "#ffffff", roundness={"type": 3})]
        els += text(f"{eid}{k}_t", tx + 10, y + 7, big_, 15, INK) + text(f"{eid}{k}_w", tx + 10, y + 31, small, 10, BODY)
    return els


def k_table(eid, x, y, w, head_, rows, verbs):
    cols = list(head_)
    while len(cols) > 1 and cols[-1] == "" and all(len(r) < len(head_) or r[len(cols) - 1] == "" for r in rows):
        cols.pop()                                   # trailing empty columns go; a first empty header stays
    cw = (w - 10) / len(cols)
    els = [_el("rectangle", eid, x, y, w, 22 * (len(rows) + 1) + 4, ROOM, "#ffffff", roundness={"type": 3})]
    for j, c in enumerate(cols):
        els += text(f"{eid}h{j}", x + 8 + j * cw, y + 5, c, 11, TITLE)
    for i, r in enumerate(rows):
        els += line(f"{eid}l{i}", [(x, y + 24 + 22 * i), (x + w, y + 24 + 22 * i)], "#e9ecef", 1)
        for j, c in enumerate(r[:len(cols)]):
            els += text(f"{eid}r{i}{j}", x + 8 + j * cw, y + 29 + 22 * i, c, 11, INK)
    return els + _btns(eid + "_b", x + w, y + 22 * (len(rows) + 1) + 12, verbs)


def k_bars(eid, x, y, w, caption, bars):
    els = text(eid + "_c", x + 4, y, caption, 11, BODY)
    top = max(n for _, n in bars) or 1
    for k, (lab, n) in enumerate(bars):
        by = y + 20 + 20 * k
        els += text(f"{eid}{k}_l", x + 4, by, lab, 11, INK)
        bw = (w - 160) * n / top
        els += [_el("rectangle", f"{eid}{k}", x + 90, by + 2, bw, 13, "#74c0fc", "#a5d8ff")]
        els += text(f"{eid}{k}_n", x + 98 + bw, by, str(n), 11, INK)
    return els


def k_chain(eid, x, y, w, steps, verb=""):
    bw = (w - 46 * (len(steps) - 1)) / len(steps)
    els = []
    for k, (role, name) in enumerate(steps):
        bx = x + k * (bw + 46)
        els += text(f"{eid}{k}_r", bx + 2, y, role, 10, BODY)
        els += [_el("rectangle", f"{eid}{k}", bx, y + 16, bw, 36, ROOM, "#ffffff", roundness={"type": 3})]
        els += text(f"{eid}{k}_w", bx + 10, y + 26, name, 12, INK)
        if k:
            els += arrow(f"{eid}{k}_a", [(bx - 40, y + 34), (bx - 6, y + 34)], ROOM)
    return els + (_btns(eid + "_v", x + w, y + 60, (verb,)) if verb else [])


def k_tabs(eid, x, y, w, items, detail, verbs=()):
    """Tiles that act as a view-button-list (b16 s32 B): the one that waits for you open, its detail in a panel below,
    the panel's verbs (Answer, Defer) on its first row."""
    tw = (w - 10 * (len(items) - 1)) / len(items)
    on = next((k for k, (_, s) in enumerate(items) if "waiting" in s), 0)   # the one that waits for you, else the first
    els = []
    for k, (t_, s) in enumerate(items):
        tx = x + k * (tw + 10)
        els += [_el("rectangle", f"{eid}{k}", tx, y, tw, 44, OR if k == on else ROOM, "#fff4e6" if k == on else "#ffffff",
                    roundness={"type": 3})]
        els += text(f"{eid}{k}_t", tx + 10, y + 6, t_, 13, TITLE) + text(f"{eid}{k}_w", tx + 10, y + 25, s, 10, BODY)
    py = y + 54
    els += [_el("rectangle", eid + "_d", x, py, w, 12 + 22 * len(detail), OR, "#ffffff", roundness={"type": 3})]
    for k, (n_, words) in enumerate(detail):
        els += text(f"{eid}_d{k}", x + 12, py + 8 + 22 * k, n_, 12, TITLE) + text(f"{eid}_d{k}w", x + 130, py + 8 + 22 * k, words, 12, INK)
    return els + _btns(eid + "_v", x + w - 10, py + 6, verbs)


def k_line(eid, x, y, w, words):
    return text(eid, x + 4, y, words, 12, INK)


def k_picture(eid, x, y, w, caption, verbs):
    return ([_el("rectangle", eid, x, y, 260, 80, ROOM, "#f1f3f5")] + text(eid + "_c", x + 274, y + 4, caption, 12, INK)
            + _btns(eid + "_b", x + w, y + 52, verbs))


# ── the slide deck's Workbench pieces (slides 16 to 23), in the workbench's colours; a colour always means a state ──
PILL = {"Needs your judgment": (OR, "#fff4e6"), "Needs review": (OR, "#fff4e6"), "waiting for you": (OR, "#fff4e6"),
        "Draft saved": (BLUE, "#e7f5ff"), "Uncertain": (BLUE, "#e7f5ff"), "running": (BLUE, "#e7f5ff"),
        "More evidence requested": (PU, "#f3f0ff"), "Awaiting qualification": (OR, "#fff4e6"),
        "Answered": (GR, "#ebfbee"), "done": (GR, "#ebfbee"), "Hard": (RE, "#fff5f5")}


def pill(eid, x, y, words):
    stroke, fill = PILL.get(words, (ROOM, "#f8f9fa"))
    w = 18 + 7 * len(words)
    return [_el("rectangle", eid, x, y, w, 22, stroke, fill, roundness={"type": 3})] + text(eid + "_t", x + 9, y + 4, words, 11, INK)


def primary(eid, x, y, words):
    """The one main action of a screen: a filled blue button (the workbench's colour for the current thing)."""
    w = 26 + 7.5 * len(words)
    return [_el("rectangle", eid, x - w, y, w, 28, BLUE, BLUE, roundness={"type": 3})] + text(eid + "_t", x - w + 13, y + 6, words, 12, "#ffffff")


def k_rows(eid, x, y, w, rows, foot=""):
    """Slide 17: one full-width row per question, its words large, its state a pill, its verb on the row."""
    els = []
    for k, (words, state, verb) in enumerate(rows):
        ry = y + 50 * k
        els += [_el("rectangle", f"{eid}{k}", x, ry, w, 42, ROOM, "#ffffff", roundness={"type": 3})]
        els += text(f"{eid}{k}_w", x + 14, ry + 11, words, 15, INK)
        els += pill(f"{eid}{k}_p", x + w - 250, ry + 10, state) if state else []
        els += _btns(f"{eid}{k}_b", x + w - 12, ry + 9, (verb,)) if verb else []
    return els + (text(eid + "_f", x + 14, y + 50 * len(rows) + 2, foot, 12, BODY) if foot else [])


def k_strip(eid, x, y, w, words):
    """Slides 20 and 23: the versions this view stands on, one quiet band."""
    return [_el("rectangle", eid, x, y, w, 30, ROOM, "#ffffff", roundness={"type": 3})] + text(eid + "_t", x + 12, y + 7, words, 13, INK)


def k_agent(eid, x, y, w, items):
    """Slide 17's Agent activity: who works on what now, one line each."""
    els = [_el("rectangle", eid, x, y, w, 12 + 24 * len(items), ROOM, "#ffffff", roundness={"type": 3})]
    for k, item in enumerate(items):
        who, doing, state = (item + ("",))[:3]
        words = f"🤖 {who}: {doing}" if who else f"      {doing}"
        els += text(f"{eid}{k}", x + 12, y + 8 + 24 * k, words, 13, INK)
        els += pill(f"{eid}{k}_p", x + w - 110, y + 5 + 24 * k, state) if state else []
    return els


def k_card(eid, x, y, w, question, cases, options, verbs=("Save draft", "Submit feedback")):
    """Slide 16's decision card: the question large, Case A and Case B side by side, every option unselected, your own
    rule, defer, a comment box, Save draft and the one main action."""
    els = text(eid + "_q", x + 4, y, question, 17, INK)
    cw = (w - 12) / 2
    for k, (label, words) in enumerate(cases):
        cx = x + k * (cw + 12)
        els += [_el("rectangle", f"{eid}_c{k}", cx, y + 32, cw, 50, ROOM, "#ffffff", roundness={"type": 3})]
        els += text(f"{eid}_c{k}_l", cx + 12, y + 38, label, 12, PU) + text(f"{eid}_c{k}_w", cx + 12, y + 58, words, 12, INK)
    oy = y + (94 if cases else 32)
    for k, words in enumerate(options):
        els += [_el("rectangle", f"{eid}_o{k}", x, oy + 32 * k, w, 26, ROOM, "#ffffff", roundness={"type": 3})]
        els += [_el("ellipse", f"{eid}_o{k}_r", x + 10, oy + 32 * k + 6, 14, 14, ROOM, "#ffffff")]
        els += text(f"{eid}_o{k}_t", x + 34, oy + 32 * k + 5, words, 13, INK)
    cy = oy + 32 * len(options) + 6
    els += [_el("rectangle", eid + "_cm", x, cy, w, 32, ROOM, "#ffffff", roundness={"type": 3})]
    els += text(eid + "_cm_t", x + 10, cy + 8, "Comments / alternative rule", 12, ROOM)
    by = cy + 44
    els += [_el("rectangle", eid + "_sd", x, by, 110, 28, BLUE, "#ffffff", roundness={"type": 3})] + text(eid + "_sd_t", x + 22, by + 6, verbs[0], 12, BLUE)
    return els + primary(eid + "_sb", x + w, by, verbs[1])


def k_compare(eid, x, y, w, decision, before, after, warn="", verb=""):
    """Slide 19: your confirmed decision, the wording before, the proposed wording, and what still needs clarifying."""
    els = [_el("rectangle", eid + "_d", x, y, w, 52, ROOM, "#ffffff", roundness={"type": 3})]
    els += text(eid + "_dl", x + 12, y + 6, "YOUR CONFIRMED DECISION", 10, GR) + text(eid + "_dw", x + 12, y + 24, decision, 15, INK)
    els += [_el("rectangle", eid + "_b", x, y + 60, w, 46, ROOM, "#ffffff", roundness={"type": 3})]
    els += text(eid + "_bl", x + 12, y + 66, "BEFORE", 10, BODY) + text(eid + "_bw", x + 12, y + 82, before, 13, INK)
    els += text(eid + "_ar", x + w / 2, y + 108, "↓", 14, ROOM)
    els += [_el("rectangle", eid + "_a", x, y + 128, w, 46, ROOM, "#ffffff", roundness={"type": 3})]
    els += text(eid + "_al", x + 12, y + 134, "PROPOSED WORDING", 10, PU) + text(eid + "_aw", x + 12, y + 150, after, 13, INK)
    els += _btns(eid + "_av", x + w - 10, y + 139, (verb,)) if verb else []
    if warn:
        els += [_el("rectangle", eid + "_w", x, y + 182, w, 30, "#ffe8cc", "#fff9db", roundness={"type": 3})]
        els += text(eid + "_wt", x + 12, y + 189, "⚠️ " + warn, 13, INK)
    return els


def k_checklist(eid, x, y, w, items, verb="", note=""):
    """Slide 21's Before starting: each condition a row with its circle, the action greyed until all are met."""
    els = []
    for k, item in enumerate(items):
        words, state = item if isinstance(item, tuple) else (item, "")
        els += [_el("ellipse", f"{eid}{k}_r", x + 8, y + 30 * k + 4, 14, 14, ROOM, "#ffffff")]
        els += text(f"{eid}{k}_t", x + 32, y + 30 * k + 3, words, 13, INK)
        els += text(f"{eid}{k}_s", x + w - 120, y + 30 * k + 3, state, 12, BODY) if state else []
    by = y + 30 * len(items) + 6
    if verb:
        els += [_el("rectangle", eid + "_v", x, by, 170, 28, ROOM, "#f1f3f5", roundness={"type": 3})]
        els += text(eid + "_vt", x + 14, by + 6, verb, 12, ROOM) + (text(eid + "_n", x + 184, by + 7, note, 12, BODY) if note else [])
    return els


def k_callout(eid, x, y, w, title, words, verb):
    """Slide 20's issue call-out: a rule or label question the round found, and the report that carries it."""
    els = [_el("rectangle", eid, x, y, w, 56, OR, "#fff4e6", roundness={"type": 3})]
    els += text(eid + "_h", x + 14, y + 8, "⚠️ " + title, 14, INK) + text(eid + "_w", x + 14, y + 32, words, 12, INK)
    return els + _btns(eid + "_b", x + w - 12, y + 14, (verb,))


# ── a step slide's own shape (slides 7 to 15): In → who works → Out, your part, the loop's turns (JL 261101) ─────
def k_flow(eid, x, y, w, inn, who, out):
    """The step slide read left to right: what goes in, who works on it (an agent, or 🙋 you), what comes out; each box
    a title and up to two lines; the Run that did the work is the who box's last line."""
    bw = (w - 2 * 34) / 3
    els = []
    for k, (label, box) in enumerate((("In", inn), ("Who works", who), ("Out", out))):
        bx = x + k * (bw + 34)
        you = k == 1 and box[0].startswith("🙋")
        els += [_el("rectangle", f"{eid}{k}", bx, y, bw, 84, OR if you else ROOM, "#ffffff", roundness={"type": 3})]
        els += text(f"{eid}{k}_l", bx + 10, y + 6, label, 10, OR if you else (PU if k == 1 else (GR if k == 2 else BODY)))
        els += text(f"{eid}{k}_h", bx + 10, y + 22, box[0], 13, INK)
        for j, ln in enumerate(box[1:3]):
            els += text(f"{eid}{k}_{j}", bx + 10, y + 42 + 18 * j, ln, 11, BODY) if ln else []
        if k:
            els += arrow(f"{eid}{k}_a", [(bx - 30, y + 42), (bx - 4, y + 42)], ROOM)
    return els


def k_ask(eid, x, y, w, words, verb="", mode="interaction"):
    """Your part of the step: an interaction that waits (orange, 🙋, only in the meaning Task), a sign gate (blue, ✍️),
    a finished one (✅) or none (plain line)."""
    stroke, fill = {"interaction": (OR, "#fff4e6"), "gate": (BLUE, "#f1f8ff"), "done": (GR, "#ffffff"),
                    "none": ("#e9ecef", "#ffffff")}[mode]
    els = [_el("rectangle", eid, x, y, w, 36, stroke, fill, roundness={"type": 3})] + text(eid + "_t", x + 12, y + 9, words, 13, INK)
    return els + (_btns(eid + "_b", x + w - 10, y + 6, (verb,)) if verb else [])


def k_turns(eid, x, y, w, label, turns):
    """The loop made visible: the Task's turns in order, each (name, state[, "now"]); the one marked now outlined."""
    els = text(eid + "_l", x + 2, y + 4, label, 11, BODY)
    bx = x + 150
    for k, turn in enumerate(turns):
        name, state = turn[0], turn[1]
        now = len(turn) > 2 and turn[2] == "now"
        cw = 26 + 7 * max(len(name), len(state))
        els += [_el("rectangle", f"{eid}{k}", bx, y, cw, 40, OR if now else ROOM, "#fff4e6" if now else "#ffffff", roundness={"type": 3})]
        els += text(f"{eid}{k}_n", bx + 10, y + 4, name, 13, INK) + text(f"{eid}{k}_s", bx + 10, y + 22, state, 10, BODY)
        if k:
            els += arrow(f"{eid}{k}_a", [(bx - 22, y + 20), (bx - 4, y + 20)], ROOM)
        bx += cw + 26
    return els


KIND = {"big": (k_big, lambda a: 50 if a[1] else 30), "kv": (k_kv, lambda a: 22 * len(a[0]) + 8),
        "tiles": (k_tiles, lambda a: 62), "table": (k_table, lambda a: 22 * (len(a[1]) + 1) + (44 if a[2] else 12)),
        "bars": (k_bars, lambda a: 26 + 20 * len(a[1])), "chain": (k_chain, lambda a: 62 + (34 if len(a) > 1 and a[1] else 0)),
        "tabs": (k_tabs, lambda a: 66 + 22 * len(a[1])), "line": (k_line, lambda a: 24),
        "picture": (k_picture, lambda a: 92),
        "rows": (k_rows, lambda a: 50 * len(a[0]) + (22 if len(a) > 1 and a[1] else 0)),
        "strip": (k_strip, lambda a: 36), "agent": (k_agent, lambda a: 18 + 24 * len(a[0])),
        "card": (k_card, lambda a: (94 if a[1] else 32) + 32 * len(a[2]) + 6 + 44 + 34),
        "compare": (k_compare, lambda a: 216 if len(a) > 3 and a[3] else 180),
        "checklist": (k_checklist, lambda a: 30 * len(a[0]) + (40 if len(a) > 1 and a[1] else 6)),
        "callout": (k_callout, lambda a: 62),
        "flow": (k_flow, lambda a: 92), "ask": (k_ask, lambda a: 44), "turns": (k_turns, lambda a: 50)}


def is_view_sec(sec):
    return len(sec) >= 2 and isinstance(sec[1], str) and (sec[1] in KIND or sec[0] in ("next", "group"))


def view_sec_h(sec):
    if sec[0] == "next":
        return 30
    if sec[0] == "group":
        return 40
    return (40 if sec[0] else 0) + KIND[sec[1]][1](sec[2:]) + 10


def view_sec(eid, x, y, w, sec):
    """A numbered heading bar (when the section has a title), then its content as what it is."""
    if sec[0] == "next":
        return text(eid, x + w - 12 * len(sec[1]) - 70, y + 6, f"next: {sec[1]} →", 12, BLUE)
    if sec[0] == "group":                          # a group heading: Process or Results, as the old Operation · Result
        return text(eid, x, y + 6, sec[1], 16, INK) + line(eid + "_l", [(x + 120, y + 18), (x + w, y + 18)], "#dee2e6", 1)
    els = []
    if sec[0]:
        els += [_el("rectangle", eid, x, y, w, 30, ROOM, "#ffffff", roundness={"type": 3})]
        els += text(eid + "_t", x + 12, y + 7, "▾ " + sec[0], 13, TITLE)
        y += 40
    return els + KIND[sec[1]][0](eid + "_c", x, y, w, *sec[2:])


def slug(view):
    return re.sub(r"[^a-z0-9]+", "-", view.lower()).strip("-")


def crumb_lines(words, width=112):
    """The path, wrapped on its separators so no folder name is cut."""
    out, cur = [], ""
    for part in words.split(" › "):
        nxt = part if not cur else cur + " › " + part
        if len(nxt) > width and cur:
            out.append(cur + " ›")
            cur = part
        else:
            cur = nxt
    return out + [cur]


def screen(eid, x, y, h, level, name, path, section, views, on, secs, caption):
    """One view as the full page: window, the rails, then in the content column the path, the title-&-section, the
    view-button-list with this view in orange, the goal-line, the view-caption, and its sections as boxes holding their
    content and verbs, or its topics (name, words, stage) as rows."""
    els = window(eid + "w", x, y, W, h, f"/_board/workbench?layout=focus&section={section}")
    els += rails(eid + "rl", x, y, level, name, section)
    cx = x + X0
    lines = crumb_lines(CRUMB[level].format(name=name))
    for k, ln in enumerate(lines):
        els += text(f"{eid}_crumb{k}", cx, y + 40 + 14 * k, ln, 10, ROOM)
    top = y + 46 + 14 * len(lines)
    els += head(eid + "h", cx, top, name, section, views, on)
    els += text(eid + "_goal", cx, top + 74, GOAL.get(level) or GOAL.get(name) or GOAL[TASK], 13, INK)
    els += text(eid + "_cap", cx, top + 98, caption, 12, BODY)
    yy = top + 130
    for k, sec in enumerate(secs):
        if is_view_sec(sec):
            els += view_sec(f"{eid}r{k}", cx, yy, CW, sec)
            yy += view_sec_h(sec)
            continue
        els += topic_row(f"{eid}r{k}", cx, yy, CW, *sec) if is_topic(sec) else secbar(f"{eid}r{k}", cx, yy, CW, *sec)
        yy += 76 if is_topic(sec) else box_h(sec[1]) + 12
    return els


def tall(secs):
    return sum(view_sec_h(sec) if is_view_sec(sec) else 76 if is_topic(sec) else box_h(sec[1]) + 12 for sec in secs)


# ── the views, each its sections in page order ───────────────────────────────────────────────────────────────────
# One grid per level (JL 261101: "go ahead"): every answer sits at question × cut × Job, and each level down fixes
# one axis. Board = question × Job, Job = question × cut, Task = cut × step. Report opens on the answer; Work opens on
# what waits on the person (set the cuts, sign a plan, close a Job, sign the handoff, triage proposals); no Task asks.
# Report and Work share letters (b16 s32-D09). No value from a real Board is drawn: answers are "one plain line".
BLOCK_REPORT = (
    ("Answers", (("", "big", "j03_p2_<d>v2 · AP2 × F2: the newest Job", "preview: its plan is not signed yet"),
                 ("1 · At a glance", "table", ("question", "answer", "how sure"),
                  [("X01 overall control", "one plain line", "moderate"), ("K01 control-and-timing", "one plain line", "moderate"),
                   ("W01 first-focus", "one plain line", "not signed")], ("Open the Overall Report",)))),
    ("Tracks", (("1 · Each question across Jobs", "table", ("question", "j01 · AP1 × F1", "j03 · AP2 × F2", "why"),
                 [("D01 extract-and-clock", "✅", "held", ""), ("I01 glucose-control", "✅", "changed", "data"),
                  ("K01 control-and-timing", "✅", "changed", "code + data"), ("I06 event-locked-glucose", "—", "new question", "code")], ()),
                ("Readings", "Coverage and Consistency: which question × cut × Job has an answer", ("Open",)))),
    ("Jobs", (("1 · Plan × freeze", "table", ("", "F1 · first window", "F2 · whole record"),
               [("AP1 · first ladder", "j01 · closed", ""), ("AP2 · adds events", "", "j03 · preview")], ()),
              ("❗ Two clocks moved", "j01 → j03 changed code and data: a changed answer has two causes"))),
    ("Data", (("1 · Data freezes", "table", ("freeze", "label", "frozen"),
               [("F1 · v1", "the first window", "261011"), ("F2 · v2", "the whole record", "261011")], ()),
              ("Cuts", "Full · awake · asleep, and Cross across them; set in the plan, signed"))),
    ("Handoff", (("", "big", "No handoff signed yet", "waits on W01, W02 and your sign"),
                 ("Design reads it", "only a signed handoff, by its pair: AP × F"))),
)
BLOCK_WORK = (
    ("Answers", (("🙋 Waits on you", "nothing: the answers are agent work"),
                 ("Write the Overall Report", "for j03, once every level is answered", ("Run",)))),
    ("Tracks", (("🙋 Triage proposals", "4 open: take into the next plan, or decline", ("Triage",)),
                ("Propose from j03", "run-propose-j03: changed answers become proposals", ("Run",)))),
    ("Jobs", (("🙋 Sign AP2", "in the Prototype; until then j03 is a preview", ("Sign",)),
              ("🙋 Close j03", "once every page is checked", ("Close",)),
              ("+ Add a Job", "one plan × one freeze; move one clock at a time", ("Add",)))),
    ("Data", (("+ Add a data freeze", "a dated, frozen copy; needs no new plan", ("Add",)),
              ("Propose a cut", "the Board proposes a cut; the next plan sets it", ("Propose",)))),
    ("Handoff", (("🙋 Sign the handoff", "the counsel and its pair, once drafted", ("Sign",)),
                 ("Draft the handoff", "run-draft-handoff, from the Wisdom counsel", ("Run",)))),
)
BLOCK_STUDIO = (                     # the Board's topics, by group, in button order
    ("Map", (("s01-question-map", "the questions as a map, generated", "explore"),)),
    ("Readings", (("s02-<what-moved>", "why an answer changed between Jobs", "explore"),
                  ("s03-<pattern-seen>", "a pattern seen across cuts", "explore"))),
    ("Cuts", (("s04-<cut-ideas>", "cuts worth proposing next", "explore"),)),
    ("Handoff", (("s05-<handoff-story>", "what Design should take from this", "shaping"),)),
)
# Job = one analysis plan × one data freeze; its main view is the question × cut grid, rows grouped by DIKW level.
GRID = ("question", "Full", "awake", "asleep", "Cross")
JOB_REPORT = (
    ("Overall", (("", "big", "Overall Report · AP2 × F2", "the plain answers, level X"),
                 ("1 · At a glance", "table", ("question", "answer", "rests on"),
                  [("X01 overall control", "one plain line", "K01 · t10, K04 · t13"),
                   ("X02 when it leaves range", "one plain line", "K01 · t10")], ("Open",)))),
    ("Grid", (("1 · Questions × cuts", "table", GRID,
               [("D · Data", "", "", "", ""), ("D01 extract-and-clock", "✅", "", "", ""),
                ("I · Information", "", "", "", ""), ("I01 glucose-control", "✅", "✅", "✅", ""),
                ("K · Knowledge", "", "", "", ""), ("K01 control-and-timing", "✅", "", "", ""),
                ("K05 awake-asleep-pooling", "", "", "", "pool"), ("W · Wisdom", "", "", "", ""),
                ("W01 first-focus", "⏳ page", "", "", "")], ()),)),
    ("vs previous", (("", "big", "against j01: code and data moved", "❗ a changed answer has two causes"),
                     ("1 · Per question", "table", ("question", "status", "why"),
                      [("D01 extract-and-clock", "held", ""), ("I01 glucose-control", "changed", "data"),
                       ("K01 control-and-timing", "changed", "code + data"), ("I06 event-locked-glucose", "new question", "code")], ()))),
    ("The pair", (("1 · This Job", "kv", [("plan", "AP2 · adds events and visit prep (p2)"),
                                          ("freeze", "F2 · the whole record (v2)"),
                                          ("state", "preview: AP2 not signed"), ("moved", "code and data, from j01")], ()),)),
)
JOB_WORK = (
    ("Overall", (("🙋 Waits on you", "nothing: X pages are agent work"),
                 ("Write the Overall Report", "X01, X02, once Knowledge is answered", ("Run",)))),
    ("Grid", (("Hard Runs", "one Run per question × cut", ("Launch",)),
              ("Pages to write", "12 ⏳ by the insight agent", ("Run all",)),
              ("Pages to check", "3 by another agent", ("Run all",)))),
    ("vs previous", (("Compare", "run-compare-j01 writes reports/vs-j01.md", ("Run",)),
                     ("Propose", "run-propose-j03: changed answers become proposals", ("Run",)))),
    ("The pair", (("🙋 Close the Job", "run-close-j03, once every page is checked", ("Close",)),
                  ("🙋 Sign AP2", "in the Prototype; until then this Job is a preview", ("Open",)))),
)
JOB_STUDIO = (                       # its own topics, then the Board's (as b16 s37)
    ("This Job", (("Ask the agent", "Copy prompt: talk and sketch about this Job"),
                  ("s02-<what-moved>", "why an answer changed from j01", "explore"))),
    ("Board", (("s01-question-map", "the questions as a map, generated", "explore"),
               ("s05-<handoff-story>", "what Design should take from this", "shaping"))),
)
# Task = one question in one Job; its main view is cut × step. Every step is agent work: no Task asks the person.
TASK_REPORT = (
    ("Answer", (("", "big", "K01 · is glucose well controlled, and when does it leave range?", "answered · check ✅"),
                ("Answer", "one plain line, from the face's answer:"),
                ("How sure", "one line, from the face's how-sure:"),
                ("May say", "Knowledge: only what survives tests across cuts"))),
    ("By cut", (("1 · One Run per cut", "table", ("cut", "Run", "power", "result"),
                 [("Full", "r01_full", "ok", "table · figure"), ("awake", "—", "", "not asked"),
                  ("asleep", "—", "", "not asked"), ("Cross", "—", "", "not asked")], ()),
                ("Each result", "its table and figure, read only", ("Open",)))),
    ("Across Jobs", (("1 · This question in each Job", "table", ("Job", "answer", "status"),
                      [("j01 · AP1 × F1", "one plain line", "first"), ("j03 · AP2 × F2", "one plain line", "changed")], ()),)),
    ("Plan", (("1 · Needs", "kv", [("need", "K01.E6: the hour curve read as windows of the day"),
                                    ("steps", "🧮 compute · 📎 reuse · ⚓ answer"), ("agreed", "✅ by another agent")], ()),)),
)
TASK_WORK = (
    ("Answer", (("1 · The chain", "chain", [("agent", "plan"), ("agent 2", "agree"), ("Runs", "cuts"),
                                            ("agent", "page"), ("agent 2", "check")], ""),
                ("Write the page", "run-write-t10 · haipipe-insight-knowledge", ("Run",)),
                ("Check the page", "run-check-t10 · another agent", ("Run",)),
                ("No sign here", "a Task never asks you; you sign at the Job"))),
    ("By cut", (("r01_full", "✅ ok", ("Rerun",)),
                ("Propose a cut", "awake or asleep: a proposal to the next plan", ("Propose",)))),
    ("Across Jobs", (("Track this question", "run-track-K01: one question across Jobs", ("Run",)),)),
    ("Plan", (("Plan the evidence", "its needs and work specs, before any run", ("Plan",)),
              ("Agree the plan", "another agent writes agreed:", ("Agree",)))),
)
TASK_STUDIO = (                      # always on the right-rail (as b16 s40)
    ("This Task", (("Ask the agent", "Copy prompt: talk and sketch about this question"),
                   ("No topic yet", "no Studio topic names this Task"))),
    ("Job", (("s02-<what-moved>", "why an answer changed from j01", "explore"),
             ("s01-question-map", "the questions as a map, generated", "explore"))),
)
RULE = ["one grid per level: question × Job · question × cut · cut × step (JL 261101)",
        "a grid cell: ✅ answered · ⏳ page to write · — not asked · pool / split on Cross",
        "rows are grouped D · I · K · W, so the DIKW levels need no tabs"]

CAPTION = {
    ("block", "report"): {"Answers": "the newest Job's answers, at a glance", "Tracks": "each question across the Jobs",
                          "Jobs": "each analysis plan × data freeze", "Data": "the data freezes and the cuts",
                          "Handoff": "the signed counsel Design reads"},
    ("block", "work"): {"Answers": "the Overall Report to write", "Tracks": "proposals to triage",
                        "Jobs": "plans to sign, Jobs to close or add", "Data": "a new freeze, a proposed cut",
                        "Handoff": "the handoff to draft and sign"},
    ("job", "report"): {"Overall": "the plain answers, level X", "Grid": "every question × cut",
                        "vs previous": "held or changed against j01", "The pair": "the plan and the freeze this Job runs"},
    ("job", "work"): {"Overall": "the X pages to write", "Grid": "Runs to launch, pages to write and check",
                      "vs previous": "compare, then propose", "The pair": "close the Job, sign its plan"},
    ("task", "report"): {"Answer": "the answer and how sure", "By cut": "one Run per cut",
                         "Across Jobs": "the same question in other Jobs", "Plan": "what the answer needs"},
    ("task", "work"): {"Answer": "the chain, and its next step", "By cut": "rerun a cut, propose one",
                       "Across Jobs": "track the question", "Plan": "plan and agree its needs"},
}


def view_rows(level, items, section=""):
    """One screen per view, lettered, three a row."""
    name = PAGE[level][0]
    views = tuple(v for v, _ in items)
    cap = CAPTION.get((level, section), {})
    flat = [(LETTERS[k], f"{LETTERS[k]} · {v}", name, views, k, secs, v, cap.get(v, f"the topics of the {v} group"))
            for k, (v, secs) in enumerate(items)]
    return [flat[i:i + 3] for i in range(0, len(flat), 3)]


VIEWS = {   # (level, section): (the line above the screens, the rows, the open question, green notes)
    ("block", "report"): ("one dataset: answers first, then each question across Jobs, the Jobs, the data, the handoff",
                          view_rows("block", BLOCK_REPORT, "report"), "? Answers first,\nor Tracks first", None),
    ("block", "work"): ("the same letters as Report; 🙋 rows are yours, the rest is agent work",
                        view_rows("block", BLOCK_WORK, "work"), "? Sign AP2 here,\nor only in the Prototype", None),
    ("block", "studio"): ("the Board's topics by group, in button order; a topic's groups are its Tags",
                          view_rows("block", BLOCK_STUDIO, "studio"), "? Board topics only,\nor every Job's too", None),
    ("job", "report"): ("one plan × one freeze: the Overall Report, then the question × cut grid",
                        view_rows("job", JOB_REPORT, "report"), "? Overall first,\nor the Grid first", None),
    ("job", "work"): ("the same letters; 🙋 rows are yours, the rest is agent work",
                      view_rows("job", JOB_WORK, "work"), "? Run all,\nor one button per row", None),
    ("job", "studio"): ("this Job's own topics, then the Board's",
                        view_rows("job", JOB_STUDIO, "studio"), "? a Job's own topics,\nor only the Board's", None),
    ("task", "report"): ("one question in one Job: the answer, each cut, other Jobs, the plan; read only",
                         view_rows("task", TASK_REPORT, "report"), "? one shape for D, I, K, W,\nor own sections per level", None),
    ("task", "work"): ("the same letters; every step is agent work, so nothing here asks you",
                       view_rows("task", TASK_WORK, "work"), "? the whole chain,\nor only the next step", None),
    ("task", "studio"): ("always on the right-rail, even before a topic names the Task",
                         view_rows("task", TASK_STUDIO, "studio"), "? start a topic from here\nwith one click", None),
}
PIECE = {   # the why notes: what the live focus page shows today (curled 261101 from the insight host)
    ("block", "report"): ("the Board's Report: answers first, then tracks",
                          ["Report shows only\nMindMap and Status", "no answer is shown\non the Board",
                           "the answers live on the\nold insight-board page"]),
    ("block", "work"): ("the Board's Work: your signs first",
                        ["each Job says \"no\nstate recorded\"", "no button signs a plan\nor closes a Job",
                         "proposals have no\nplace on screen"]),
    ("block", "studio"): ("the Board's Studio: its topics, by group",
                          ["no Studio section on\nthe focus page", "the Board has no\nstudio/ folder", "topics sit only\nin b11"]),
    ("job", "report"): ("a Job's Report: the Overall Report, then the grid",
                        ["Tasks are listed flat,\nt01 to t20", "no question × cut\ngrid", "the Overall Report\nis not shown"]),
    ("job", "work"): ("a Job's Work: what waits, and Run all",
                      ["every Task says \"no\nstate recorded\"", "no sign or close\nbutton", "what moved is only\nin the Job's face"]),
    ("job", "studio"): ("a Job's Studio: the topics that name it",
                        ["no Studio section", "no topic names\na Job", "no talk-and-sketch\nprompt here"]),
    ("task", "report"): ("a Task's Report: the answer, then each cut",
                         ["Report lists Runs:\nr01_full, run-write", "the answer sits in the\nface, never shown",
                          "gates hid in the old\nCheck Space"]),
    ("task", "work"): ("a Task's Work: the agents' chain",
                       ["Runs show ok or\nplanned, no verbs", "the evidence plan\nhas no place", "no chain shows\nwhat comes next"]),
    ("task", "studio"): ("a Task's Studio: always on the right-rail",
                         ["Studio was not\na section", "no topic names\nthe Task", "the prompt had\nno home"]),
}
TARGET = {"block": "servers/workbench-insight/insight_theme.py · workbench-insight/SKILL.md",
          "job": "servers/workbench-insight/insight_theme.py · workbench-insight/SKILL.md",
          "task": "servers/workbench-insight/insight_views.py · workbench-insight/SKILL.md"}

AGREED = {}                         # the letters settled so far: {(level, section): {key: sections}}; none yet
MOCK = """<!doctype html><meta charset=utf-8><title>{key} · {view}</title>
<!-- GENERATED by insight_ui_cells.py from AGREED; the agreed screen of {nn} view {key} -->
<style>body{{font:14px system-ui;margin:24px;max-width:820px;color:#1e1e1e;background:#fff}}h1{{font-size:22px;margin:0}}
h1 small{{color:#868e96;font-weight:400;margin-left:8px}}nav{{margin:12px 0 18px}}nav span{{display:inline-block;border:1px solid
#ced4da;border-radius:6px;padding:3px 9px;margin-right:6px;font-size:12px}}nav span.on{{border-color:#e8590c;background:#fff4e6}}
section{{border:1px solid #dee2e6;border-radius:8px;padding:9px 14px;margin:8px 0}}section b{{font-size:13px}}</style>
<h1>{name}<small>{section}</small></h1><nav>{nav}</nav>{secs}"""


def screens_of(level, section):
    return [s for row in VIEWS[(level, section)][1] for s in row]


def out_file(topic, level, section, key, view):
    return topic / "delivery" / "ui" / f"{level}-{section}" / f"{key}-{slug(view)}.html"


def write_agreed(topic, nn, level, section):
    """delivery/ui/<level>-<section>/<key>-<view>.html for each settled screen."""
    for key, label, name, buttons, on, _, view, _c in screens_of(level, section):
        secs = AGREED.get((level, section), {}).get(key)
        if secs is None:
            continue
        out = out_file(topic, level, section, key, view)
        out.parent.mkdir(parents=True, exist_ok=True)
        nav = "".join(f'<span class={"on" if k == on else "off"}>{b}</span>' for k, b in enumerate(buttons))
        out.write_text(MOCK.format(key=key, view=view, nn=f"s{nn}", name=name, section=VERB[section], nav=nav,
                                   secs="".join(f"<section><b>▾ {s[0]}</b><br><small>{s[1]}</small></section>" for s in secs))
                       + "\n", encoding="utf-8")


def build(topic: Path):
    topic = Path(topic).resolve()
    m = re.match(r"s(\d+)-(block|job|task)-ui-(report|work|studio)$", topic.name)
    nn, level, section = m.group(1), m.group(2), m.group(3)
    piece, why = PIECE[(level, section)]
    lay, rows, ask, changed = VIEWS[(level, section)]
    write_agreed(topic, nn, level, section)
    path = PAGE[level][1]
    pieces = [("page", f"ui/{level}-{section}/{key}-{slug(view)}.html", f"{key} · the {view} view",
               out_file(topic, level, section, key, view).exists()) for key, _, _, _, _, _, view, _ in screens_of(level, section)]
    sk = topic / "delivery" / "skill" / f"{level}-{section}-views.md"
    pieces.append(("book", f"skill/{sk.name}", "the views' manual, for workbench-insight", sk.exists()))
    first, last = pieces[0][2].split(" · ")[0], pieces[-2][2].split(" · ")[0]
    spec = {"title": f"{level.capitalize()} UI · {VERB[section]}: {piece.split(': ', 1)[1]}",
            "why": {"question": f"why do we need s{nn}?", "notes": why,
                    "quote": "JL 261101: read paper and labeling, then work on the insights"},
            "what": {"head": f"② what s{nn} hands over: one screen, {first} to {last}", "icon": "page", "name": "delivery/ui/",
                     "type": "ui", "deck_why": f"stays in s{nn}'s delivery/deck/, so anyone gets it in a minute", "parts": pieces},
            "job": topic.parent.parent,
            "target": TARGET[level],
            "missing": [(name, "not settled yet") for _, name, _, done in pieces if not done],
            "have": [(name, "agreed") for icon, name, _, done in pieces if done and icon == "page"]}

    def design():                                    # every view the same screen, lettered; no separate main sketch
        h = 250 + max(tall(s[5]) for row in rows for s in row)
        els = text("skA", 690, 280, f"{first} to {last} · {piece}, every view the same screen", 18, TITLE)
        els += text("lay", 690, 340, lay, 16, BODY)
        y = 380
        if level == "job" and section != "studio":    # the rule first: one grid per level
            for k, ln in enumerate(RULE):
                els += text(f"rule{k}", 690, y + 30 * k, ln, 18 if k == 0 else 16, OR if k == 0 else INK)
            y += 30 * len(RULE) + 40
        for r, row in enumerate(rows):
            for k, (key, label, name, buttons, on, secs, _, caption) in enumerate(row):
                sx = 690 + k * (W + 40)
                els += text(f"sc{r}_{k}_L", sx, y, label, 22, TITLE)
                if changed and key in changed:
                    els += [change_note(sx + 300, y + 4, changed[key], "261031", None)]
                where = f"…/{JOB}/{name}" if level == "task" else path   # each type its own Task
                els += screen(f"sc{r}_{k}", sx, y + 40, h, level, name, where, section, buttons, on, secs, caption)
            y += h + 80
        return els + sticky("askD", 1180, y + 20, 320, 76, ask, 15, -0.03, RED, RE)

    cols = max(len(row) for row in rows)
    return five_parts.build(topic, spec, design, shift=(W + 40) * cols + 80)


def letter_png(topic: Path, key: str, out: Path, scale: float = 1.0) -> Path:
    """One letter's screen alone, for a Design loop review (haipipe-ui, stage 1): <out>.excalidraw and <out>.png."""
    import subprocess
    topic = Path(topic).resolve()
    m = re.match(r"s(\d+)-(block|job|task)-ui-(report|work|studio)$", topic.name)
    level, section = m.group(2), m.group(3)
    rows = VIEWS[(level, section)][1]
    h = 250 + max(tall(s[5]) for row in rows for s in row)
    key_, label, name, buttons, on, secs, _, caption = next(s for s in screens_of(level, section) if s[0] == key)
    where = f"…/{JOB}/{name}" if level == "task" else PAGE[level][1]
    els = text("L", 0, 0, label, 22, TITLE) + screen("one", 0, 40, h, level, name, where, section, buttons, on, secs, caption)
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    drawing = out.with_suffix(".excalidraw")
    five_parts.write(drawing, els)
    render = TOOLS / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts/render_png.py"
    subprocess.run(["uv", "run", "--no-project", "-q", "--with", "pillow", "python", str(render), str(drawing),
                    str(out.with_suffix(".png")), str(scale)], check=True, stdout=subprocess.DEVNULL)
    return out.with_suffix(".png")


if __name__ == "__main__":                               # python insight_ui_cells.py <topic folder> <letter> <out>
    print(letter_png(Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])))
