"""The nine sNN of j01 · The labeling pages, level by level: one per level (Block, Job, Task) and section (Report,
Work, Studio), each drawn in haipipe-studio's five parts (scripts/five_parts.py). Copied from b16 j01's
paper_ui_cells.py (JL 261031: copy the paper theme's model). Each sNN's builder is `build(Path(__file__).parent)`:
its cell is found by its folder name (s51-block-ui-report → block, report).

A cell's Design is its page's views, lettered A, B, C …, each drawn as the same full screen (window, title and section
word, view buttons with that view in orange, its sections as heading bars with one line each), the open question in
red under them. A view is settled one round at a time; a settled view's screen is written to delivery/ui/ (AGREED).

The Task page differs from paper's: a labeling Task is one of six types (s13: items · ground truth · meaning · expression ·
scanning · score), so its Report and Work letter the types, one row each, and number each type's steps (A1 Data,
A2 Items …). Each view is drawn from its step slide (task_views.py, with its coverage table COVER).
Names are the public DICES-350 dataset's; no item text is drawn (Tools is public).
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
PAGE = {"block": ("b01_dices350", "examples-6-labeling/Project-Labeling-SocialMediaWithLabels/labeling/b01_dices350"),
        "job": ("j01_dices350_response_safety", "examples-6-labeling/…/b01_dices350/j01_dices350_response_safety"),
        "task": ("t03_dices350_response_safety_meaning", "examples-6-labeling/…/j01_dices350_response_safety/t03_dices350_response_safety_meaning")}
LETTERS = "ABCDEFGH"
W, CW, X0 = 780, 640, 70               # a screen, its content column, where it starts (the rails are hidden: short lines)
CRUMB = {"block": "Physician-SPACE › examples-6-labeling › Project-Labeling-SocialMediaWithLabels › labeling › b01_dices350",
         "job": "Physician-SPACE › examples-6-labeling › Project-Labeling-SocialMediaWithLabels › labeling › b01_dices350 › j01_dices350_response_safety",
         "task": "Physician-SPACE › examples-6-labeling › Project-Labeling-SocialMediaWithLabels › labeling › b01_dices350 › j01_dices350_response_safety › {name}"}
GOAL = {"block": "Purpose: label the DICES-350 conversations, one Job per label",
        "job": "Goal: response safety as one person means it, on every item",
        "t01_dices350_items": "Aim: the corpus as items, the sealed test held back",
        "t02_dices350_ground_truth_profile": "Aim: the dataset's own labels, kept apart",
        "t03_dices350_response_safety_meaning": "Aim: what the label means to you, loop by loop, as rules you approve",
        "t04_dices350_response_safety_expression": "Aim: wording the models follow, under your approved meaning, released when ready",
        "t05_dices350_response_safety_scanning": "Aim: every item labeled under the release, then audited",
        "t06_dices350_response_safety_score": "Aim: how close the final labels are to the experts"}
LEFT = {"block": ("b01_dices350", "  j01_dices350_response_safety", "  j02_dices350_<label>"),
        "job": ("j01_dices350_response_safety", "  t01_dices350_items", "  t02_dices350_ground_truth_profile",
                "  t03_dices350_response_safety_meaning", "  t04_dices350_response_safety_expression", "  t05_dices350_response_safety_scanning", "  t06_dices350_response_safety_score", "j02_dices350_<label>"),
        "task": ("t01_dices350_items", "t02_dices350_ground_truth_profile", "t03_dices350_response_safety_meaning", "t04_dices350_response_safety_expression", "t05_dices350_response_safety_scanning", "t06_dices350_response_safety_score")}
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
    here = {"block": "b01_dices350", "job": "j01_dices350_response_safety"}.get(level) or name
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


# ── the slide deck's Workbench pieces (slides 16 to 23), in the workbench's colours; a colour always means a state ──
PILL = {"Q1": (OR, "#fff4e6"), "Q2": (OR, "#fff4e6"), "Q3": (OR, "#fff4e6"),
        "Needs your judgment": (OR, "#fff4e6"), "Needs review": (OR, "#fff4e6"), "waiting for you": (OR, "#fff4e6"),
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
        bw = 26 + 7.5 * len(verb) if verb else 0          # the pill sits left of its verb, however long the verb
        els += pill(f"{eid}{k}_p", min(x + w - 250, x + w - 24 - bw - (18 + 7 * len(state))), ry + 10, state) if state else []
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


# ── a step slide's own shape (slides 7 to 15): In → who works → Out, your part, the loop's iterations (JL 261101) ─────
def k_flow(eid, x, y, w, inn, who, out):
    """The step slide read left to right: what goes in, who works on it (an agent, or 🙋 you), what comes out; each box
    a title and up to two lines; the Run that did the work is the who box's last line."""
    bw = (w - 2 * 34) / 3
    els = []
    for k, (label, box) in enumerate((("In", inn), ("Who works", who), ("Out", out))):
        bx = x + k * (bw + 34)
        you = False                                    # one waiting mark per view: the orange bar, never the box
        els += [_el("rectangle", f"{eid}{k}", bx, y, bw, 84, OR if you else ROOM, "#ffffff", roundness={"type": 3})]
        els += text(f"{eid}{k}_l", bx + 10, y + 6, label, 10, OR if you else BODY)   # colour only where you act
        els += text(f"{eid}{k}_h", bx + 10, y + 22, box[0], 13, INK)
        for j, ln in enumerate(box[1:3]):
            els += text(f"{eid}{k}_{j}", bx + 10, y + 42 + 18 * j, ln, 11, BODY) if ln else []
        if k:
            els += arrow(f"{eid}{k}_a", [(bx - 30, y + 42), (bx - 4, y + 42)], ROOM)
    return els


def k_ask(eid, x, y, w, words, verb="", mode="interaction"):
    """Your part of the step: an interaction that waits (orange, 🙋, only in the meaning Task), a sign gate (blue, ✍️),
    a finished one (✅) or none (plain line)."""
    stroke, fill = {"interaction": (OR, "#fff4e6"), "gate": (BLUE, "#f1f8ff"), "wait": (BLUE, "#f1f8ff"),
                    "done": (ROOM, "#ffffff"), "none": ("#e9ecef", "#ffffff")}[mode]
    els = [_el("rectangle", eid, x, y, w, 36, stroke, fill, roundness={"type": 3})] + text(eid + "_t", x + 12, y + 9, words, 13, INK)
    if verb and mode == "wait":                        # a sign whose condition is not met yet: its button greyed (simulation 261101)
        bw = 26 + 7.5 * len(verb)
        return els + [_el("rectangle", eid + "_b", x + w - 10 - bw, y + 6, bw, 24, ROOM, "#f1f3f5", roundness={"type": 3})] + \
            text(eid + "_bt", x + w - 10 - bw + 13, y + 10, verb, 12, ROOM)
    return els + (_btns(eid + "_b", x + w - 10, y + 6, (verb,)) if verb else [])


def k_turns(eid, x, y, w, label, turns):
    """The loop made visible: its iterations (meaning's loops, expression's rounds) in order, each (name, state[, "now"]); the one marked now outlined."""
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


def k_prompt(eid, x, y, w, title, lines, fields=(), session="<this Task's session>"):
    """A step's prompt, the draft Task's Prompt box redrawn (draft_steps._prompt_box): the words the page fills from the
    step's real inputs, the fields only you can fill, the line that sends it to the Task's chat session, and Copy prompt;
    you paste it there to start the step (JL 261101: "prepare the prompt template that the user can enter and copy to
    the chat session"). A prompt is you → the agent; an interaction is the agent → you, and only in 🧭 meaning."""
    h = 76 + 18 * len(lines) + 40 * len(fields)
    els = [_el("rectangle", eid, x, y, w, h, ROOM, "#ffffff", roundness={"type": 3})]
    els += text(eid + "_h", x + 12, y + 9, "✍️ Prompt · " + title, 13, INK) + _btns(eid + "_b", x + w - 10, y + 6, ("Copy prompt",))
    py = y + 36
    els += [_el("rectangle", eid + "_p", x + 10, py, w - 20, 18 * len(lines) + 10, "#e9ecef", "#f8f9fa", roundness={"type": 3})]
    for k, ln in enumerate(lines):
        els += text(f"{eid}_p{k}", x + 20, py + 6 + 18 * k, ln, 12, INK)
    fy = py + 18 * len(lines) + 18
    for k, field in enumerate(fields):                  # (label, hint), or (label, what you sent, True) once it ran
        label, words, sent = field[0], field[1], len(field) > 2 and field[2]
        els += text(f"{eid}_f{k}l", x + 12, fy + 40 * k + 1, label, 11, BODY)
        els += [_el("rectangle", f"{eid}_f{k}", x + 120, fy + 40 * k - 6, w - 132, 30, ROOM, "#ffffff", roundness={"type": 3})]
        els += text(f"{eid}_f{k}h", x + 130, fy + 40 * k + 1, words, 12, INK if sent else ROOM)
    ty = fy + 40 * len(fields) - 4
    return els + text(eid + "_t", x + 12, ty, f'Run this in the Claude session "{session}"; start it if it is not running.', 11, BODY)


def k_mindmap(eid, x, y, w, versions, on, root, branches):
    """The guideline as a mind map (JL 261101: "make the guideline as the mindmap, to make the rules to be very very
    clean"; "the Guideline Rule Mindmap with different versions"): its versions as buttons, the open one marked; the
    label's question at the root, each value a branch, each rule one short leaf; a card that asks about a rule carries
    its Q tag on that leaf."""
    els = text(eid + "_vl", x + 2, y + 6, "version", 11, BODY)
    bx = x + 62
    for k, v in enumerate(versions):
        vw, is_on = 24 + 7.5 * len(v), v == on
        els += [_el("rectangle", f"{eid}_v{k}", bx, y, vw, 26, OR if is_on else ROOM, "#fff4e6" if is_on else "#ffffff",
                    roundness={"type": 3})] + text(f"{eid}_v{k}t", bx + 12, y + 5, v, 12, INK)
        bx += vw + 8
    top, lh = y + 40, 30
    total = lh * sum(len(ls) for _, ls in branches)
    ry = top + total / 2 - 28
    els += [_el("rectangle", eid + "_r", x, ry, 170, 56, ROOM, "#ffffff", roundness={"type": 3})]
    for j, ln in enumerate(root[:2]):
        els += text(f"{eid}_r{j}", x + 10, ry + 9 + 18 * j, ln, 12, INK)
    li = 0
    for bi, (name, leaves) in enumerate(branches):
        by_ = top + lh * li + lh * len(leaves) / 2 - 13
        els += line(f"{eid}_rb{bi}", [(x + 170, ry + 28), (x + 210, by_ + 13)], ROOM, 1)
        els += [_el("rectangle", f"{eid}_b{bi}", x + 210, by_, 80, 26, ROOM, "#ffffff", roundness={"type": 3})]
        els += text(f"{eid}_b{bi}t", x + 222, by_ + 5, name, 12, INK)
        for leaf in leaves:
            words, tag = leaf if isinstance(leaf, tuple) else (leaf, "")
            ly = top + lh * li
            els += line(f"{eid}_bl{li}", [(x + 290, by_ + 13), (x + 330, ly + 15)], ROOM, 1)
            els += [_el("rectangle", f"{eid}_l{li}", x + 330, ly + 2, w - 330, 26, "#e9ecef", "#ffffff", roundness={"type": 3})]
            els += text(f"{eid}_l{li}t", x + 342, ly + 7, words, 12, INK)
            els += pill(f"{eid}_l{li}p", x + w - 52, ly + 4, tag) if tag else []
            li += 1
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
        "flow": (k_flow, lambda a: 92), "ask": (k_ask, lambda a: 44), "turns": (k_turns, lambda a: 50),
        "prompt": (k_prompt, lambda a: 84 + 18 * len(a[1]) + 40 * len(a[2])),
        "mindmap": (k_mindmap, lambda a: 48 + 30 * sum(len(ls) for _, ls in a[3]))}


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
    els += text(eid + "_goal", cx, top + 74, GOAL.get(level) or GOAL.get(name) or GOAL["t03_dices350_response_safety_meaning"], 13, INK)
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
# Block = one dataset; its views follow what a dataset holds: the corpus, one row per label (Job), their Handoffs
# and their scores. Report and Work share letters (b16 s32-D09).
BLOCK_REPORT = (
    ("Dataset", (("The corpus", "DICES-350: 350 conversations between people and a chatbot, public release", ("Open",)),
                 ("Items", "one item per conversation: its last chatbot turn is judged; a sealed test is held back",
                  ("Open",)),
                 ("Embedding", "the corpus map, every item placed by meaning and coloured by cluster", ("Open map",)),
                 ("The dataset's own labels", "the raters' safety ratings that came with DICES-350, kept apart",
                  ("Open",)))),
    ("Labels", (("j01_dices350_response_safety", "the label · who decides · phase · rounds · state"),
                ("j02_dices350_<label>", "another label on the same items: not started"))),
    ("Handoffs", (("Each label's release", "handoff hNN: rules, wording, labels; who signed, when"),
                  ("Not signed yet", "the labels still in their meaning or expression loop"))),
    ("Scores", (("Each label's score", "final labels against the experts' gold and the raters' spread"),
                ("Final labels", "each label's delivered file, one click to open"))),
)
BLOCK_WORK = (
    ("Dataset", (("Waits on you", "a sign about the corpus"),
                 ("Prepare a corpus", "the items Task's next step, or Add it"),
                 ("Open", "the dataset's open points"))),
    ("Labels", (("j01_dices350_response_safety", "items ✅ · meaning Loop 3 🙋 · expression e02 · scanning ⬜ · score ⬜"),
                ("+ Open a labeling job", "a new label on this dataset: a new Job"),
                ("Waits on you", "each label's sign or ruling, one row each"))),
    ("Handoffs", (("Waits for your sign", "each release that meets its criteria"),
                  ("Held back", "the open decisions that hold a release back"))),
    ("Scores", (("Each score Task", "run, or what it waits on: the final labels"),)),
)
BLOCK_STUDIO = (                     # the groups of the Block's _studio_groups.txt, in button order
    ("Dataset", (("s01-<dataset>-corpus", "what the corpus is, drawn", "explore"),)),
    ("Labels", (("s02-<label>-meaning", "what one label means, as the person sees it", "shaping"),
                ("s03-<label>-hard-cases", "the items at the label's edges", "explore"))),
    ("Method", (("s04-labeling-method", "what the agent does, what the person judges", "agreed"),)),
)
# Job = one dataset × one label; its views are the label, then its six Task types in pipeline order.
JOB_REPORT = (
    ("Label", (("1 · The label", "the question asked of each item, in one plain sentence"),
               ("2 · Who decides", "the one person whose meaning is learned"),
               ("schema.yaml", "the label's values: high · low · none"))),
    ("Items", (("t01_dices350_items", "items made, the sealed test held back"),
               ("Data · Items · Embedding", "each step's result, read only"))),
    ("Ground truth", (("t02_dices350_ground_truth_profile", "the dataset's own labels; the loops and scanning never read them"),)),
    ("Meaning", (("t03_dices350_response_safety_meaning", "meaning versions m01, m02, m03, each made by one loop of your answers"),
                 ("Meaning history", "every rule, and the interaction answer that made it"))),
    ("Expression", (("t04_dices350_response_safety_expression", "wording e01, e02 under each meaning; the round reports"),
                    ("The release", "handoff h01: signed or not, and what it freezes"))),
    ("Scanning", (("t05_dices350_response_safety_scanning", "the corpus labeled, risky cases reviewed, the audit"),
                  ("Final labels", "the file, its counts by value"))),
    ("Score", (("t06_dices350_response_safety_score", "agreement with the gold, and the raters' spread"),)),
)
JOB_WORK = (
    ("Label", (("Waits on you", "the contract and the first definition, to sign"),
               ("Open", "the label's open choices"))),
    ("Items", (("t01_dices350_items", "Data ✅ · Items ✅ · Embedding next"),)),
    ("Ground truth", (("t02_dices350_ground_truth_profile", "made; only the score Task reads it"),)),
    ("Meaning", (("t03_dices350_response_safety_meaning", "Loop 3 · Report ✅ · Preferences 🙋 waiting · Update ⬜"),
                 ("Interaction", "🙋 Loop 3: report-03 waits for your answers"))),
    ("Expression", (("t04_dices350_response_safety_expression", "under m02: e01 ✅ · e02 ✅ sent back to meaning · waits for m03"),)),
    ("Scanning", (("t05_dices350_response_safety_scanning", "⬜ not made yet: Add (it needs a signed release)"),)),
    ("Score", (("t06_dices350_response_safety_score", "⬜ optional: Add"),)),
)
JOB_STUDIO = (                       # its own topics, then the Block's (as b16 s37)
    ("This Job", (("Ask the agent", "Copy prompt: talk and sketch about this label"),
                  ("s03-<label>-hard-cases", "the items at the label's edges", "explore"))),
    ("Block", (("s01-<dataset>-corpus", "what the corpus is, drawn", "explore"),
               ("s04-labeling-method", "what the agent does, what the person judges", "agreed"))),
)
# Task = one step of a Job, of six types; the type sets the view buttons (its steps) and each step shows
# its own sections (task_views.py): the items steps from task_labeling.py's cards, Split and the meaning, expression and scanning
# steps from the slide deck, version 12, as s13 maps them (JL 261101: "go ahead and update them").
TYPES = (                            # (letter, icon, type, task name, its steps); one Task per loop (JL 261101)
    ("A", "📦", "items", "t01_dices350_items", ("Data", "Items", "Embedding", "Split")),
    ("B", "📏", "ground truth", "t02_dices350_ground_truth_profile", ("Labels",)),
    ("C", "🧭", "meaning", "t03_dices350_response_safety_meaning", ("Frame", "Report", "Preferences", "Update")),
    ("D", "🛠", "expression", "t04_dices350_response_safety_expression", ("Rewrite", "Run", "Evaluate", "Release")),
    ("E", "🔍", "scanning", "t05_dices350_response_safety_scanning", ("Batches", "Audit", "Final labels")),
    ("F", "📊", "score", "t06_dices350_response_safety_score", ("Agreement",)),
)
RULE = ["each view is its step slide: In → who works → Out, your part, then Results; only 🧭 meaning asks you (JL 261101)",
        "📦 items        Data · Items · Embedding · Split          step 0",
        "📏 ground truth Labels                                    input, fenced",
        "🧭 meaning      Frame · Report · Preferences · Update     steps 1 to 4 · Loop 1, 2 … make m01, m02 … · interactions",
        "🛠 expression   Rewrite · Run · Evaluate · Release        steps 5 and 6 · rounds e01, e02 … per meaning",
        "🔍 scanning     Batches · Audit · Final labels            step 7",
        "📊 score        Agreement                                 evaluation"]
TASK_STUDIO = (                      # always on the right-rail (as b16 s40)
    ("This Task", (("Ask the agent", "Copy prompt: talk and sketch about this step"),
                   ("No topic yet", "no Studio topic names this Task"))),
    ("Job", (("s03-<label>-hard-cases", "the items at the label's edges", "explore"),
             ("s04-labeling-method", "what the agent does, what the person judges", "agreed"))),
)


def type_rows(section):
    """The Task cells' rows: one per type, each step one screen with its own sections; then the shared Runs screen."""
    rows = []
    for L, icon, typ, name, steps in TYPES:
        buttons = tuple(steps)              # no Runs view: a step shows its own Runs (JL 261101)
        row = []
        for i, step in enumerate(steps):
            key = f"{L}{i + 1}" if len(steps) > 1 else L
            row.append((key, f"{key} · {icon} {typ} · {step}", name, buttons, i, task_views.view(key, section),
                        f"{typ} · {step}", task_views.CAPTION[key]))
        rows.append(row)
    return rows


CAPTION = {
    ("block", "report"): {"Dataset": "what the corpus is, and the items made from it", "Labels": "each label on this dataset, one row each",
                          "Handoffs": "each label's signed release", "Scores": "how close each label's final labels are to the gold"},
    ("block", "work"): {"Dataset": "what the corpus still needs", "Labels": "each label's next move, and who has it",
                        "Handoffs": "the Handoffs waiting for a sign", "Scores": "the score Tasks still to run"},
    ("job", "report"): {"Label": "the label, who decides, its values", "Items": "the items this label is judged on",
                        "Ground truth": "the dataset's own labels, kept apart", "Meaning": "what the label means, version by version",
                        "Expression": "the wording the models follow, and the release",
                        "Scanning": "the corpus labeled, and its audit", "Score": "the final labels against the gold"},
    ("job", "work"): {"Label": "what the label waits on", "Items": "the items Task's steps, and which one waits",
                      "Ground truth": "the ground truth Task", "Meaning": "the meaning loop, and what waits on you",
                      "Expression": "the expression rounds, under the current meaning",
                      "Scanning": "the scanning Task, once the release is signed", "Score": "the score Task, optional"},
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
    ("block", "report"): ("one dataset: its corpus, then one row per label, their Handoffs and scores",
                          view_rows("block", BLOCK_REPORT, "report"), "? Scores as its own view,\nor inside Labels", None),
    ("block", "work"): ("the same views and letters as Report; each is that view's work",
                        view_rows("block", BLOCK_WORK, "work"), "? one row per label,\nor one per Task", None),
    ("block", "studio"): ("the groups of _studio_groups.txt, in button order; a topic's groups are its Tags",
                          view_rows("block", BLOCK_STUDIO, "studio"), "? Block topics only,\nor every Job's too", None),
    ("job", "report"): ("one dataset × one label: the label, then its Tasks by type, each read only",
                        view_rows("job", JOB_REPORT, "report"), "? Label first,\nor Meaning first", None),
    ("job", "work"): ("one row per Task; its step words open that step; a missing type is ⬜ Add",
                      view_rows("job", JOB_WORK, "work"), "? Release: inside expression,\nor a Task of its own", None),
    ("job", "studio"): ("this Job's own topics, then the Block's",
                        view_rows("job", JOB_STUDIO, "studio"), "? a Job's own topics,\nor only the Block's", None),
    ("task", "report"): ("one row per type; each step its own result sections (task_labeling.py), read only",
                         type_rows("report"), "? one shape for all six types,\nor own sections per type", None),
    ("task", "work"): ("one row per type; each step: 1 the step and its state, then its own result sections, then next",
                       type_rows("work"), "? a Sign here, or only\nin the Labeling workbench", None),
    ("task", "studio"): ("always on the right-rail, even before a topic names the Task",
                         view_rows("task", TASK_STUDIO, "studio"), "? start a topic from here\nwith one click", None),
}
PIECE = {
    ("block", "report"): ("the Block's Report: the dataset, its labels, Handoffs and scores",
                          ["the Block page showed\nonly Scope and Schema", "label status hid in\na Labeling sub-tab",
                           "no place said which\nlabel is done"]),
    ("block", "work"): ("the Block's Work: the same views, each one's next move",
                        ["Jobs and Labeling were\ntwo sub-tabs", "no row said who has\nthe next move",
                         "Open a labeling job\nhid in the Runs panel"]),
    ("block", "studio"): ("the Block's Studio: its topics, by group",
                          ["topics sat in a flat\nstudio/ folder", "no group per dataset\nor label", "a row said too much"]),
    ("job", "report"): ("a Job's Report: the label, then each Task type's result",
                        ["a Job page showed its\nTasks, not results", "the label itself was\nonly in schema.yaml",
                         "the release had no\nplace on screen"]),
    ("job", "work"): ("a Job's Work: its Tasks by type, and their steps",
                      ["missing types were dashed\ncards at the end", "no step word said\nwhat waits",
                       "a click went to the\nold Labeling workbench"]),
    ("job", "studio"): ("a Job's Studio: the topics that name its label",
                        ["a label's hard cases\nhad no place", "Job topics sat in\nthe Block", "no talk-and-sketch\nprompt here"]),
    ("task", "report"): ("a Task's Report: each type's steps, results only",
                         ["four engine Spaces sat\nin one page", "Report repeated\nthe Work cards",
                          "item text could leak\noutside the cards"]),
    ("task", "work"): ("a Task's Work: each step's input, prompt and sign",
                       ["building and scanning\nwere one Task", "a Sign sat two\nclicks away", "steps were tabs\nwith no state"]),
    ("task", "studio"): ("a Task's Studio: always on the right-rail",
                         ["Studio was a\nWork button", "no topic named\nthe Task", "the prompt was\na long box"]),
}
TARGET = {"block": "servers/workbench-labeling/labeling_theme.py · workbench-labeling/SKILL.md",
          "job": "servers/workbench-labeling/labeling_theme.py · workbench-labeling/SKILL.md",
          "task": "workbench-task-labeling/task_labeling.py · workbench-task-labeling/SKILL.md"}

AGREED = {}                         # the letters settled so far: {(level, section): {key: sections}}; none yet
MOCK = """<!doctype html><meta charset=utf-8><title>{key} · {view}</title>
<!-- GENERATED by labeling_ui_cells.py from AGREED; the agreed screen of {nn} view {key} -->
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
    pieces.append(("book", f"skill/{sk.name}", "the views' manual, for workbench-labeling", sk.exists()))
    first, last = pieces[0][2].split(" · ")[0], pieces[-2][2].split(" · ")[0]
    spec = {"title": f"{level.capitalize()} UI · {VERB[section]}: {piece.split(': ', 1)[1]}",
            "why": {"question": f"why do we need s{nn}?", "notes": why,
                    "quote": "JL 261031: copy the paper theme's 3 x 3 for labeling"},
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
                    els += [change_note(sx + 300, y + 4, changed[key], "261031", None)]
                where = f"…/j01_dices350_response_safety/{name}" if level == "task" else path   # each type its own Task
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
    where = f"…/j01_dices350_response_safety/{name}" if level == "task" else PAGE[level][1]
    els = text("L", 0, 0, label, 22, TITLE) + screen("one", 0, 40, h, level, name, where, section, buttons, on, secs, caption)
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    drawing = out.with_suffix(".excalidraw")
    five_parts.write(drawing, els)
    render = TOOLS / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts/render_png.py"
    subprocess.run(["uv", "run", "--no-project", "-q", "--with", "pillow", "python", str(render), str(drawing),
                    str(out.with_suffix(".png")), str(scale)], check=True, stdout=subprocess.DEVNULL)
    return out.with_suffix(".png")


if __name__ == "__main__":                               # python labeling_ui_cells.py <topic folder> <letter> <out>
    print(letter_png(Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])))
