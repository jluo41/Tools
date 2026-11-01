"""The nine sNN of j01 · The design pages, level by level: one per level (Block, Job, Task) and section (Report,
Work, Studio), each drawn in haipipe-studio's five parts (scripts/five_parts.py). Copied from b15 j01's
labeling_ui_cells.py, itself copied from b16 j01's paper_ui_cells.py (JL 261101: update the design theme the way the
paper and labeling themes did). Each sNN's builder is `build(Path(__file__).parent)`: its cell is found by its folder
name (s51-block-ui-report → block, report).

A cell's Design is its page's views, lettered A, B, C …, each drawn as the same full screen (window, title and section
word, view buttons with that view in orange, its sections as heading bars with one line each), the open question in
red under them. A view is settled one round at a time; a settled view's screen is written to delivery/ui/ (AGREED).

The Task page, as labeling's, letters the Task types: a design Job has three (haipipe-design: t00 reason ideas, one
Task per design, t99 review whole), so its Report and Work letter the types, one row each, and number each type's
steps (A1 Inputs, B2 Verify …). Each view is drawn from its run card and method step (task_views.py, with its
coverage table COVER). Names are folder names already public in b12's board.md; no design text is drawn (Tools is
public; the Block's designs are tailored to one demonstration participant and stay local).
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
sys.path.insert(0, str(HERE))
import task_views  # noqa: E402

VERB = {"report": "Report", "work": "Work", "studio": "Studio"}
BLOCK, JOB = "Design-PreVisitChecklist", "j01_prepare-before-visit_goal-only"
PAGE = {"block": (BLOCK, f"examples-5-design/ProjI-Insight-1-Wearable/design/{BLOCK}"),
        "job": (JOB, f"examples-5-design/…/{BLOCK}/{JOB}"),
        "task": ("t01_d01_keep-devices-on", f"examples-5-design/…/{JOB}/t01_d01_keep-devices-on")}
LETTERS = "ABCDEFGH"
W, CW, X0 = 780, 640, 70               # a screen, its content column, where it starts (the rails are hidden: short lines)
CRUMB = {"block": f"WellDoc-SPACE › examples-5-design › ProjI-Insight-1-Wearable › design › {BLOCK}",
         "job": f"WellDoc-SPACE › examples-5-design › ProjI-Insight-1-Wearable › design › {BLOCK} › {JOB}",
         "task": f"WellDoc-SPACE › examples-5-design › ProjI-Insight-1-Wearable › design › {BLOCK} › {JOB} › {{name}}"}
GOAL = {"block": "Purpose: checklists for the weeks before a clinic visit, one Job per goal × method",
        "job": "Goal: prepare-before-visit, by the goal-only method, on inputs version i1",
        "t00_reason-ideas": "Aim: ideas from the fenced inputs or own knowledge, each step traced to its source",
        "t01_d01_keep-devices-on": "Aim: one design, drafted, verified and revised until it passes",
        "t99_review-whole": "Aim: the passed designs ranked, the top 3 kept, each with its predicted effect"}
DESIGNS = ("t01_d01_keep-devices-on", "t02_d02_note-unusual-moments", "t03_d03_list-what-you-take", "t04_d04_log-daily-times",
           "t05_d05_note-sleep-and-activity", "t06_d06_mark-unusual-days", "t07_d07_write-your-questions", "t08_d08_countdown-to-visit")
LEFT = {"block": (BLOCK, "  j01_prepare-before-visit_goal-only", "  j02_prepare-before-visit_actionable-insights",
                  "  j03_questions-before-visit_goal-only", "  j04_questions-before-visit_actionable-insights"),
        "job": (JOB, "  t00_reason-ideas", *("  " + d for d in DESIGNS), "  t99_review-whole",
                "j02_prepare-before-visit_actionable-insights"),
        "task": ("t00_reason-ideas", *DESIGNS, "t99_review-whole")}
HERE = {}                            # a Task's rail word is its own folder name
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
    here = {"block": BLOCK, "job": JOB}.get(level) or name
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



# ── a Task view's sections, each drawn as what it is (task_views.py holds their words) ───────────────────────────
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


# ── b15's Workbench pieces (its deck's slides 16 to 23), in the workbench's colours; a colour always means a state ──
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
    """Your part of the step: an interaction that waits (orange, 🙋; a design Task has none), a sign gate (blue, ✍️),
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


def k_dcard(eid, x, y, w, kind, title, items, sources, review):
    """b12 s32's proposed design card, kept (JL 261101: "is it consistent to the previous versions?"): three columns,
    the design as its reader sees it (here a checklist), Process ③ (its idea, each element's source) and Review ④
    (the tests, the expected outcome, ⑤ its rank)."""
    h = 52 + 20 * max(len(items) + 1, len(sources), len(review))
    c1, c2 = w * 0.38, w * 0.31
    els = [_el("rectangle", eid, x, y, w, h, ROOM, "#ffffff", roundness={"type": 3})]
    for k, (cx, head_) in enumerate(((x, "Design"), (x + c1, "Process ③: each element's source"),
                                     (x + c1 + c2, "Review ④ · expected outcome"))):
        els += text(f"{eid}_h{k}", cx + 12, y + 8, head_, 10, BODY)
        if k:
            els += line(f"{eid}_s{k}", [(cx, y + 6), (cx, y + h - 6)], "#e9ecef", 1)
    els += [_el("rectangle", eid + "_m", x + 12, y + 28, c1 - 24, h - 40, ROOM, "#f8f9fa", roundness={"type": 3})]
    els += text(eid + "_mk", x + 22, y + 34, kind, 10, BODY) + text(eid + "_mt", x + 22, y + 50, title, 12, TITLE)
    for k, it in enumerate(items):
        els += text(f"{eid}_mi{k}", x + 22, y + 72 + 20 * k, it, 11, INK)
    for k, s in enumerate(sources):
        els += text(f"{eid}_p{k}", x + c1 + 12, y + 30 + 20 * k, s, 11, BODY if s.startswith(("from", "③")) else INK)
    for k, r in enumerate(review):
        els += text(f"{eid}_r{k}", x + c1 + c2 + 12, y + 30 + 20 * k, r, 11, GR if "passed" in r else INK)
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
        "dcard": (k_dcard, lambda a: 52 + 20 * max(len(a[2]) + 1, len(a[3]), len(a[4])) + 6),
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
    els += text(eid + "_goal", cx, top + 74, GOAL.get(level) or GOAL.get(name) or GOAL["t01_d01_keep-devices-on"], 13, INK)
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
# Block = one application, one channel; its views follow what a design Block holds: its bottom line, the signed goals,
# one row per Job (goal × method × inputs), the rounds (one per inputs version, with what an Exp returned) and the
# methods' scores. Report and Work share letters (b16 s32-D09). JL 261012: the Report opens on Summary.
BLOCK_REPORT = (
    ("Summary", (("1 · 🎯 The bottom line", "big", "4 Jobs ranked, 3 designs kept in each; none released yet", "waiting for you"),
                 ("2 · 📋 One row per Job", "rows", [("j01_prepare-before-visit_goal-only", "not approved", "Open"), ("j02_prepare-before-visit_actionable-insights", "not approved", "Open"), ("j03_questions-before-visit_goal-only", "not approved", "Open"), ("j04_questions-before-visit_actionable-insights", "not approved", "Open")]),
                 ("", "ask", "✍️ Next: review and approve each Job's kept designs, then build the summary", "Review", "gate"))),
    ("Goals", (("G01 prepare-before-visit", "aim · who · venue · n 3 · its own rules · signed ✅"),
               ("G02 questions-before-visit", "aim · who · venue · n 3 · its own rules · signed ✅"),
               ("The shared rules", "design-goal.md: each rule checkable on the text alone"))),
    ("Jobs", (("The map", "goals down × methods across; each cell its chain of Jobs"),
              ("j01_prepare-before-visit_goal-only", "inputs i1 · 8 designs · 3 kept"),
              ("j02_prepare-before-visit_actionable-insights", "inputs i1 · 8 designs · 3 kept · sees the insight"),
              ("j03_questions-before-visit_goal-only", "inputs i1 · 8 designs · 3 kept"),
              ("j04_questions-before-visit_actionable-insights", "inputs i1 · 8 designs · 3 kept · sees the insight"))),
    ("Rounds", (("i1 · preview", "inputs version 1: its Jobs and their releases"),
                ("Exp results", "observed/eNN: per-arm totals, scored against the frozen predictions"),
                ("i2", "the next inputs version: a signed handoff, the Jobs that move to it"))),
    ("Methods", (("Predicted vs observed", "each released design's prediction beside its Exp arm"),
                 ("Method scorecard", "the scores summed per method version"),
                 ("Cost", "each Job's Runs: time, tokens, rounds"))),
)
BLOCK_WORK = (
    ("Summary", (("1 · ✍️ Review and approve", "rows", [("j01_prepare-before-visit_goal-only", "waiting for you", "Review"), ("j02_prepare-before-visit_actionable-insights", "waiting for you", "Review"), ("j03_questions-before-visit_goal-only", "waiting for you", "Review"), ("j04_questions-before-visit_actionable-insights", "waiting for you", "Review")],
                  "each: read the 3 kept designs, then one sign freezes the predictions and releases"),
                 ("2 · 📄 Build the summary", "kv", [("Writes", "delivery/summary.pdf, one page"),
                                                   ("From", "only what the Runs wrote, no new claim")], ("Copy prompt",)))),
    ("Goals", (("+ Add a goal", "a new line in board.md ## Goals; you sign it", ("Copy prompt",)),
               ("Set the shared rules", "design-goal.md; you sign the rules", ("Copy prompt",)))),
    ("Jobs", (("j01_prepare-before-visit_goal-only", "ideas ✅ · 8 designs ✅ · ranked ✅ 3 kept · released ⬜"),
              ("+ Launch a Job", "a signed goal × a method version × an inputs version", ("Copy prompt",)),
              ("One clock moves", "each new Job moves the method or the inputs, never both"))),
    ("Rounds", (("+ Add an inputs version", "inputs/iN/: rules, theory, the insight handoff, frozen", ("Copy prompt",)),
                ("+ Add the Exp's data", "observed/eNN: per-arm totals only, never rows", ("Copy prompt",)))),
    ("Methods", (("Score the predictions", "each Exp arm against its frozen prediction", ("Copy prompt",)),
                 ("Propose a method change", "from the scores; the registry cuts the next version", ("Copy prompt",)))),
)
BLOCK_STUDIO = (                     # the groups of the Block's topics, in button order (placeholders)
    ("Goals", (("s01-<goal>-who-and-when", "who the goal is for, and when it applies", "explore"),)),
    ("Methods", (("s02-<method>-chains", "how a method's reasoning reaches its ideas", "shaping"),)),
    ("Rounds", (("s03-round-i1-to-i2", "what changed between two inputs versions", "explore"),)),
)
# Job = one goal × one method version × one inputs version → N designs; its views follow the method's steps:
# the pins (①), the ideas (②), the designs (③ ④), the ranking (⑤), then the release.
JOB_REPORT = (
    ("Setup", (("Goal", "G01 prepare-before-visit · n 3 · its rules"),
               ("Method", "M01 m2, pinned in inputs/method.md: its five steps"),
               ("Inputs", "inputs i1 as the fence: manifest.yaml lists every file it may read"))),
    ("Ideas", (("t00_reason-ideas", "ideas.yaml: one idea per design, each with a short name"),
               ("Chains", "each reasoning step's source: a fenced file, or own knowledge"))),
    ("Designs", (("1 · ✏️ d01 · keep-devices-on", "dcard", "Checklist", "<title>",
                  ["☐ Day 14: <what to do>", "☐ Day 10: <what to do>", "☐ Visit day: <what to do>"],
                  ["from idea I01", "<title> ← goal.md", "<day 14> ← rules.md r1", "<visit day> ← rules.md r2",
                   "③ run-generate-d01 · 2 drafts"],
                  ["④ T0 ✓ · T1 ✓ · passed", "expected <effect>", "⑤ rank #<n> · kept"]),
                 ("2 · 📋 The other designs", "rows", [("d02 · note-unusual-moments", "kept", "Open"),
                                                     ("d04 · log-daily-times", "kept", "Open"),
                                                     ("Dropped by t99 · d03, d05 to d08", "dropped", "Open")]))),
    ("Ranking", (("t99_review-whole", "ranking.csv: rank · predicted · why · kept"),
                 ("Coverage", "which parts of the goal the kept designs cover"))),
    ("Release", (("designs.md", "the kept designs, word for word, as released"),
                 ("Frozen predictions", "predicted · against · why, frozen when you signed"),
                 ("Predicted vs observed", "each design beside its Exp arm, once the Exp returns"))),
)
JOB_WORK = (
    ("Setup", (("Set up", "goal ✅ · method ✅ · inputs ✅ (run-setup-goal, -method, -inputs)"),
               ("Close the Job", "once every design is released or dropped; you sign", ("Copy prompt",)))),
    ("Ideas", (("t00_reason-ideas", "Reason ✅ · fence check ✅ pass · design Tasks opened"),
               ("Open the design Tasks", "one Task per idea, only after the fence check passes", ("Copy prompt",)))),
    ("Designs", (("t01_d01_keep-devices-on", "generate ✅ · verify v1 ✗ · revise ✅ · verify v2 ✅"),
                 ("t02_d02_note-unusual-moments", "generate ✅ · verify v1 ✅"),
                 ("t03 to t08", "one row each, its Runs in order; a failed verify says revise next"))),
    ("Ranking", (("t99_review-whole", "ranked ✅ · 3 of 8 kept · their predictions written"),)),
    ("Release", (("Waits on you", "✍️ Review and approve: freeze the predictions and release", ("Open",)),)),
)
JOB_STUDIO = (                       # its own topics, then the Block's (as b16 s37)
    ("This Job", (("Ask the agent", "Copy prompt: talk and sketch about this goal × method"),
                  ("s04-<job>-ideas-map", "how the ideas spread over the goal", "explore"))),
    ("Block", (("s01-<goal>-who-and-when", "who the goal is for, and when it applies", "explore"),
               ("s02-<method>-chains", "how a method's reasoning reaches its ideas", "shaping"))),
)
# Task = one step of the method in a Job, of three types (haipipe-design: t00 reason ideas, one Task per design,
# t99 review whole); the type sets the view buttons (its steps) and each step shows its own sections (task_views.py),
# drawn from the run cards (haipipe-design-workflow/references/run-cards.md) and the unit's steps (haipipe-design-unit).
TYPES = (                            # (letter, icon, type, task name, its steps)
    ("A", "💡", "reason ideas", "t00_reason-ideas", ("Inputs", "Chains", "Ideas", "Fence check")),
    ("B", "✏️", "design", "t01_d01_keep-devices-on", ("Draft", "Verify", "Revise", "State")),
    ("C", "🏆", "review whole", "t99_review-whole", ("Rank", "Coverage", "Kept")),
)
RULE = ["each view is its method step: In → who works → Out, your part, then Results; no Task asks you (JL 261101)",
        "💡 reason ideas   Inputs · Chains · Ideas · Fence check   ② reason ideas · t00",
        "✏️ design         Draft · Verify · Revise · State         ③ conduct, ④ review item · drafts v1, v2 …",
        "🏆 review whole   Rank · Coverage · Kept                  ⑤ review whole · t99 · you sign at the Job"]
TASK_STUDIO = (                      # always on the right-rail (as b16 s40)
    ("This Task", (("Ask the agent", "Copy prompt: talk and sketch about this step"),
                   ("No topic yet", "no Studio topic names this Task"))),
    ("Job", (("s04-<job>-ideas-map", "how the ideas spread over the goal", "explore"),
             ("s02-<method>-chains", "how a method's reasoning reaches its ideas", "shaping"))),
)


def type_rows(section):
    """The Task cells' rows: one per type, each step one screen with its own sections (no Runs view: a step shows its
    own Runs, JL 261101)."""
    rows = []
    for L, icon, typ, name, steps in TYPES:
        buttons = tuple(steps)
        row = []
        for i, step in enumerate(steps):
            key = f"{L}{i + 1}" if len(steps) > 1 else L
            row.append((key, f"{key} · {icon} {typ} · {step}", name, buttons, i, task_views.view(key, section),
                        f"{typ} · {step}", task_views.CAPTION[key]))
        rows.append(row)
    return rows


CAPTION = {
    ("block", "report"): {"Summary": "where this Block stands, from what its Runs wrote", "Goals": "the signed goals and the shared rules",
                          "Jobs": "each goal × method × inputs, and the map", "Rounds": "one round per inputs version",
                          "Methods": "how each method's predictions held up"},
    ("block", "work"): {"Summary": "what waits on you", "Goals": "add or sign a goal, set the rules",
                        "Jobs": "each Job's next move; launch a new one", "Rounds": "a new inputs version, an Exp's data",
                        "Methods": "score an Exp, propose a method change"},
    ("job", "report"): {"Setup": "the three pins: goal, method, inputs", "Ideas": "what t00 reasoned, from the fence only",
                        "Designs": "each design as it reads, and its verdict", "Ranking": "t99's ranking and coverage",
                        "Release": "what was released, and its frozen predictions"},
    ("job", "work"): {"Setup": "the three set-up Runs, and the close", "Ideas": "t00, and opening the design Tasks",
                      "Designs": "each design's next Run", "Ranking": "the t99 Task", "Release": "your sign"},
}


def view_rows(level, items, section=""):
    """The Block and Job cells (and each Studio): one screen per view, lettered, three a row."""
    name = PAGE[level][0]
    views = tuple(v for v, _ in items)
    cap = CAPTION.get((level, section), {})
    flat = [(LETTERS[k], f"{LETTERS[k]} · {v}", name, views, k, secs, v, cap.get(v, f"the topics of the {v} group"))
            for k, (v, secs) in enumerate(items)]
    return [flat[i:i + 3] for i in range(0, len(flat), 3)]


VIEWS = {   # (level, section): (the line above the screens, the rows, the open question, green notes)
    ("block", "report"): ("one application, one channel: the bottom line, goals, Jobs, rounds, methods",
                          view_rows("block", BLOCK_REPORT, "report"), "? Summary first,\nor Jobs first", None),
    ("block", "work"): ("the same views and letters as Report; each is that view's work",
                        view_rows("block", BLOCK_WORK, "work"), "? Launch a Job in Jobs,\nor on the Map too", None),
    ("block", "studio"): ("the Block's topics by group, in button order; a topic's groups are its Tags",
                          view_rows("block", BLOCK_STUDIO, "studio"), "? Block topics only,\nor every Job's too", None),
    ("job", "report"): ("one goal × one method version × one inputs version → N designs, read only",
                        view_rows("job", JOB_REPORT, "report"), "? Release its own view,\nor inside Ranking", None),
    ("job", "work"): ("one row per Task; a design's row shows its Runs in order; a failed verify says revise",
                      view_rows("job", JOB_WORK, "work"), "? a row per design,\nor a row per state", None),
    ("job", "studio"): ("this Job's own topics, then the Block's",
                        view_rows("job", JOB_STUDIO, "studio"), "? a Job's own topics,\nor only the Block's", None),
    ("task", "report"): ("one row per type; each step its own result sections, read only",
                         type_rows("report"), "? one shape for all three\ntypes, or own per type", None),
    ("task", "work"): ("one row per type; each step: Process (In → who → Out, your part), then Results, then next",
                       type_rows("work"), "? the prediction in the\ndesign Task, or only t99", None),
    ("task", "studio"): ("always on the right-rail, even before a topic names the Task",
                         view_rows("task", TASK_STUDIO, "studio"), "? start a topic from here\nwith one click", None),
}
PIECE = {
    ("block", "report"): ("the Block's Report: the bottom line, goals, Jobs, rounds and methods",
                          ["the Block page opened\non six Spaces", "Summary hid inside\nAudience Report",
                           "rounds and scores were\nsub-tabs apart"]),
    ("block", "work"): ("the Block's Work: the same views, each one's next move",
                        ["Jobs showed as cards,\nnot their next move", "Launch a Job hid in\nthe Runs panel",
                         "no row said what\nwaits on you"]),
    ("block", "studio"): ("the Block's Studio: its topics, by group",
                          ["topics sat in the\nIdea Studio Space", "no group per goal\nor method", "a row said too much"]),
    ("job", "report"): ("a Job's Report: the pins, ideas, designs, ranking and release",
                        ["a Job page showed\nsix Spaces", "designs and verdicts\nsat apart",
                         "the release sat in\nDelivery, not Report"]),
    ("job", "work"): ("a Job's Work: each Task's next Run",
                      ["Runs were a Space\nof their own", "a failed verify did\nnot say revise next",
                       "Review and approve\nhid in Delivery"]),
    ("job", "studio"): ("a Job's Studio: the topics that name its goal × method",
                        ["a Job's topics had\nno place", "Job topics sat in\nthe Block", "no talk-and-sketch\nprompt here"]),
    ("task", "report"): ("a Task's Report: each type's steps, results only",
                         ["every Task had the\nsame six Spaces", "t00, a design and t99\nlooked alike",
                          "drafts and verdicts\nwere two views"]),
    ("task", "work"): ("a Task's Work: each step's In, who works, Out, and next",
                       ["Runs were a separate\nview", "the revise loop had\nno place", "no step said\nwhat comes next"]),
    ("task", "studio"): ("a Task's Studio: always on the right-rail",
                         ["Studio was a\nSpace below", "no topic named\nthe Task", "the prompt was\na long box"]),
}
TARGET = {"block": "servers/workbench-design/design_views.py · workbench-design/SKILL.md",
          "job": "servers/workbench-design/design_views.py · workbench-design/SKILL.md",
          "task": "servers/workbench-design/design_views.py · design_reader.py · workbench-design/SKILL.md"}

AGREED = {}                         # the letters settled so far: {(level, section): {key: sections}}; none yet
MOCK = """<!doctype html><meta charset=utf-8><title>{key} · {view}</title>
<!-- GENERATED by design_ui_cells.py from AGREED; the agreed screen of {nn} view {key} -->
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
    pieces.append(("book", f"skill/{sk.name}", "the views' manual, for workbench-design", sk.exists()))
    first, last = pieces[0][2].split(" · ")[0], pieces[-2][2].split(" · ")[0]
    spec = {"title": f"{level.capitalize()} UI · {VERB[section]}: {piece.split(': ', 1)[1]}",
            "why": {"question": f"why do we need s{nn}?", "notes": why,
                    "quote": "JL 261101: update the design theme as paper and labeling did"},
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
        if level == "task" and section != "studio":   # the rule first: the type is only the button list
            for k, ln in enumerate(RULE):
                els += text(f"rule{k}", 690, y + 30 * k, ln, 18 if k == 0 else 16, OR if k == 0 else INK)
            y += 30 * len(RULE) + 40
        for r, row in enumerate(rows):
            for k, (key, label, name, buttons, on, secs, _, caption) in enumerate(row):
                sx = 690 + k * (W + 40)
                els += text(f"sc{r}_{k}_L", sx, y, label, 22, TITLE)
                if changed and key in changed:
                    els += [change_note(sx + 300, y + 4, changed[key], "261101", None)]
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


if __name__ == "__main__":                               # python design_ui_cells.py <topic folder> <letter> <out>
    print(letter_png(Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])))
