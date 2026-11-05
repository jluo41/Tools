"""The nine sNN of j03 · The work pages, level by level: one per level (Block, Job, Task) and section (Report, Work,
Studio), each drawn in haipipe-studio's five parts (scripts/five_parts.py). Copied from b16's paper_ui_cells.py and
b15's labeling_ui_cells.py (JL 261101: "plase read Theme_Paper and Theme_Labeling"; "use /haipipe-ui loop to check all
the UIs here and think about how to update them"). Each sNN's builder is `build(Path(__file__).parent)`: its cell is
found by its folder name (s51-block-ui-report → block, report).

A cell's Design is its page's views, lettered A, B, C …, each drawn as the same full screen (haipipe-ui 0.2.3, "one
view, one screen"): the window, both rails as pale short lines, the path, the title-&-section, the view-button-list
with this view in orange, the goal-line, the view-caption, then the view's sections as numbered heading bars, each
holding its content as what it is (a map, cards, side tabs, rows), the helpers at the bottom after a dashed rule.
A letter is settled one round at a time: the Design loop reviews it (review/<L>-s1-rNN.md), JL looks once, then the
code; a settled letter's screen is written to delivery/ui/ (AGREED).

The example has the shape of the work theme's full example (board.md's ui-block, ui-job, ui-task: a Block with a table
Job and model Jobs, one Task per outcome, one hard Run per window), in neutral words: Tools is public, so no name,
number or result of a private Block is drawn.

    python work_ui_cells.py <topic folder> <letter> <out>     one letter's screen alone, for a review round
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

VERB = {"report": "Report", "work": "Work", "studio": "Studio"}       # no verb after the section word (b10-s33-D06)
LETTERS = "ABCDEFGH"
W, CW, X0 = 780, 640, 70             # a screen, its content column, where the column starts (the rails are short lines)
BLUE = "#1864ab"                     # the workbench's colour for the current thing (frame.py :root)
PALE = "#dee2e6"

# ── the example: neutral words in the shape of the full example (Tools is public) ──────────────────────────────────
SPACE = "Example-SPACE / Project-Example / work"
BLOCK, JOB, TASK = "b11_cohort_models", "j21_ols_by_outcome", "t01_outcome_a"
PAGE = {"block": (BLOCK, f"{SPACE} / {BLOCK}", "Purpose: one cohort's analysis table, and its models"),
        "job": (JOB, f"{SPACE} / {BLOCK} / {JOB}", "Goal: the OLS models, one Task per outcome"),
        "task": (TASK, f"{SPACE} / {BLOCK} / {JOB} / {TASK}", "Aim: outcome A's model, in every window")}
LEFT = {"block": (0, 5), "job": (1, 7), "task": (2, 6)}          # the left-rail: which pale line is this page, of how many
RIGHT = ("Report", "Work", "Studio", "Interactions", "Delivery", "Related", "Timeline", "Files")
TAGS = "Slide · Draw · Mind map · Work · Delivery"               # the tags below an sNN (s51-D02)
FORM, ASK = "r04_collect_window_choice", "Which window leads the table?"
S01, S02 = "b11-s01:cohort_models @ cohort_table", "b11-s02:cohort_models @ model_tables"
S03, S04 = "b11-s03:cohort_models @ iv_tables", "b11-s04:cohort_models @ codebook"
S11 = "b11-s11:cohort_models @ ols_model_design"
S21 = "b11-s21:cohort_models @ outcome_a_controls"


# ── the screen's parts, one name each (haipipe-ui: path, title-&-section, view-button-list, goal-line, view-caption,
# content, left-rail, right-rail) ─────────────────────────────────────────────────────────────────────────────────
def window(eid, x, y, w, h, url):
    els = [_el("rectangle", eid, x, y, w, h, INK, "#ffffff", roundness={"type": 3})]
    els += line(eid + "_bar", [(x, y + 28), (x + w, y + 28)], ROOM, 1)
    return els + [_el("ellipse", f"{eid}_d{k}", x + 10 + k * 14, y + 9, 9, 9, ROOM, ROOM) for k in range(3)] + \
        text(eid + "_url", x + 60, y + 7, url, 12, BODY)


def rails(eid, x, y, level, section):
    """Both rails hide until hovered (JL 261031): pale short lines, no words; the open page or section darker."""
    here, n = LEFT[level]
    els = []
    for k in range(n):
        els += line(f"{eid}_l{k}", [(x + 16 + (6 if 0 < k <= n - 1 and level != "block" else 0), y + 50 + 12 * k),
                                    (x + 40, y + 50 + 12 * k)], INK if k == here else PALE, 2)
    for k, s in enumerate(RIGHT):
        els += line(f"{eid}_r{k}", [(x + W - 40, y + 50 + 12 * k), (x + W - 16, y + 50 + 12 * k)],
                    OR if s == VERB[section] else PALE, 2)
    return els


def head(eid, x, y, name, section, views, on=0):
    """The title-&-section, then the view-button-list, the open view in orange."""
    els = text(eid + "_t", x, y, name, 20, INK) + text(eid + "_s", x + 12.4 * len(name) + 14, y + 4, VERB[section], 15, BODY)
    cx = x
    for k, v in enumerate(views):
        w = 14 + 8 * len(v)
        els += [_el("rectangle", f"{eid}_v{k}", cx, y + 36, w, 24, OR if k == on else ROOM,
                    "#fff4e6" if k == on else "#ffffff", roundness={"type": 3})] + text(f"{eid}_v{k}_t", cx + 7, y + 40, v, 12, INK)
        cx += w + 8
    return els


def state_color(word):
    w = word.lstrip("🙋✅⏳⬜ ")
    if word.startswith("🙋") or w.startswith("waits"):
        return OR
    if word.startswith("✅") or w in ("done", "agreed", "answered") or re.match(r"v\d", w):
        return GR
    if word.startswith("⏳") or w.startswith("running"):
        return BLUE
    return BODY


def _btns(eid, x, y, verbs, color=BLUE):
    """Verb buttons, right-aligned so they end at x."""
    els, cx = [], x
    for k, v in enumerate(reversed(verbs)):
        bw = 16 + 7.5 * len(v)
        cx -= bw
        els += [_el("rectangle", f"{eid}{k}", cx, y, bw, 24, color, "#ffffff", roundness={"type": 3})]
        els += text(f"{eid}{k}_t", cx + 8, y + 5, v, 11, color)
        cx -= 8
    return els


# ── a section's content, drawn as what it is (b16 s32's shapes) ──────────────────────────────────────────────────
def k_big(eid, x, y, w, words, state):
    """The view's main point: one large sentence, its state word under it (no edge, JL 261031)."""
    sy = y + 30 + 24 * words.count("\n")                 # the state word sits under the last line
    return text(eid + "_w", x + 4, y, words, 19, INK) + (text(eid + "_s", x + 4, sy, state, 12, state_color(state)) if state else [])


def k_asks(eid, x, y, w, items):
    """What waits on you: an orange bar each, its verb on the right."""
    els = []
    for k, (words, verb) in enumerate(items):
        by = y + 48 * k
        els += [_el("rectangle", f"{eid}{k}", x, by, w, 40, OR, "#fff4e6", roundness={"type": 3})]
        els += text(f"{eid}{k}_t", x + 14, by + 11, words, 13, INK)
        els += _btns(f"{eid}{k}_b", x + w - 10, by + 8, (verb,), OR)
    return els


def k_rows(eid, x, y, w, items):
    """One item a row: its state word, its real name, one line, its picture small, its verbs (at most three)."""
    els = []
    for k, (state, name, words, verbs, pic) in enumerate(items):
        ry = y + 60 * k
        els += [_el("rectangle", f"{eid}{k}", x, ry, w, 52, ROOM, "#ffffff", roundness={"type": 3})]
        els += text(f"{eid}{k}_s", x + 12, ry + 8, state, 12, state_color(state))
        els += text(f"{eid}{k}_n", x + 130, ry + 7, name, 13, TITLE) + text(f"{eid}{k}_w", x + 130, ry + 28, words, 11, BODY)
        right = x + w - 10
        if pic:                                      # the result itself, small, named (s58 r01: an empty box says nothing)
            els += [_el("rectangle", f"{eid}{k}_p", right - 66, ry + 7, 66, 38, ROOM, "#ffffff")]
            els += [e for j in range(3) for e in line(f"{eid}{k}_p{j}", [(right - 60, ry + 15 + 8 * j), (right - 6, ry + 15 + 8 * j)], PALE, 1)]
            els += text(f"{eid}{k}_pt", right - 60, ry + 37, pic, 8, BODY)
            right -= 76
        els += _btns(f"{eid}{k}_b", right, ry + 14, verbs, OR if state.startswith("🙋") else BLUE)
    return els


def k_cardtabs(eid, x, y, w, items, on, detail, verbs):
    """Card tabs (JL 261031): cards that act as a view-button-list, one open, its detail in the panel under them. The
    open card is blue, the workbench's current thing, so orange means only "waits on you" (s52 r01); a detail row may
    carry its own verb (s55 r01: Copy command on the Run it starts)."""
    tw = (w - 10 * (len(items) - 1)) / len(items)
    els = []
    for k, (t_, s) in enumerate(items):
        tx = x + k * (tw + 10)
        els += [_el("rectangle", f"{eid}{k}", tx, y, tw, 50, BLUE if k == on else ROOM, "#e7f5ff" if k == on else "#ffffff",
                    roundness={"type": 3})]
        els += text(f"{eid}{k}_t", tx + 10, y + 7, t_, 12, TITLE) + text(f"{eid}{k}_w", tx + 10, y + 28, s, 11, state_color(s))
    py = y + 60
    els += [_el("rectangle", eid + "_d", x, py, w, 14 + 24 * len(detail), ROOM, "#ffffff", roundness={"type": 3})]
    for k, (n_, words, *verb) in enumerate(detail):
        els += text(f"{eid}_d{k}", x + 12, py + 9 + 24 * k, n_, 12, TITLE)
        els += text(f"{eid}_d{k}w", x + 200, py + 9 + 24 * k, words, 12, state_color(words) if words[:1] in "🙋✅⏳⬜" else INK)
        if verb:
            els += _btns(f"{eid}_d{k}b", x + w - 10, py + 5 + 24 * k, verb, OR if words.startswith("🙋") else BLUE)
    return els + _btns(eid + "_v", x + w - 10, py + 6, verbs)


def k_sidetabs(eid, x, y, w, items, table, kv, verbs):
    """Side tabs (JL 261101): the list on the left, the first open (blue); on the right the open one to read: the thing
    itself (a small table), then its lines, then its tags. The panel has no coloured edge (s51 r01, JL 261031)."""
    lw = 160
    els = []
    for k, (head_, word) in enumerate(items):
        iy = y + k * 44
        els += [_el("rectangle", f"{eid}{k}", x, iy, lw, 38, BLUE if k == 0 else ROOM, "#e7f5ff" if k == 0 else "#ffffff",
                    roundness={"type": 3})]
        els += text(f"{eid}{k}_t", x + 8, iy + 4, head_, 11, TITLE) + text(f"{eid}{k}_w", x + 8, iy + 21, word, 10, state_color(word))
    px, pw = x + lw + 12, w - lw - 12
    ph = sidetabs_h(items, table, kv, verbs)
    els += [_el("rectangle", eid + "_d", px, y, pw, ph - 6, ROOM, "#ffffff", roundness={"type": 3})]
    yy = y + 10
    if table:
        cols, rows = table
        cw = (pw - 24) / len(cols)
        for j, c in enumerate(cols):
            els += text(f"{eid}_h{j}", px + 12 + j * cw, yy, c, 11, TITLE)
        for i, r in enumerate(rows):
            els += line(f"{eid}_l{i}", [(px + 12, yy + 19 + 20 * i), (px + pw - 12, yy + 19 + 20 * i)], "#e9ecef", 1)
            for j, c in enumerate(r):
                els += text(f"{eid}_r{i}{j}", px + 12 + j * cw, yy + 23 + 20 * i, c, 11, INK)
        yy += 30 + 20 * len(rows)
    for k, (n_, words) in enumerate(kv):
        vx = px + (36 if n_.isdigit() or not n_ else 90)      # a code line sits close to its number
        els += text(f"{eid}_k{k}", px + 12, yy + 22 * k, n_, 11, BODY) + text(f"{eid}_k{k}w", vx, yy + 22 * k, words, 11,
                                                                              BLUE if words.startswith("Open") else INK)
    yy += 22 * len(kv)
    if verbs:
        els += text(eid + "_tags", px + 12, yy + 4, verbs, 11, BLUE)
    return els


def sidetabs_h(items, table, kv, verbs):
    inner = 16 + (30 + 20 * len(table[1]) if table else 0) + 22 * len(kv) + (26 if verbs else 0)
    return max(44 * len(items), inner) + 6


def k_tree(eid, x, y, w, root, branches):
    """The map, drawn like the draft map (JL 261031: a pill, a short name, one plain line): the root on the left, a
    branch per Job, Task or kind of Run, its role word as a pill and what it must find out; its children on the right.
    No state words: where things stand is Work's (s52-D01; s51, s54, s57 r01)."""
    rows = [max(1, len(ch)) for *_, ch in branches]
    tot = sum(r * 30 + 10 for r in rows) - 10
    ry = y + tot / 2 - 18
    els = [_el("rectangle", eid + "_r", x, ry, 128, 36, INK, "#ffffff", roundness={"type": 3})]
    els += text(eid + "_rt", x + 10, ry + 10, root, 11, INK)
    by = y
    for k, (pill, name, words, children) in enumerate(branches):
        bh = rows[k] * 30
        cy = by + bh / 2
        els += line(f"{eid}{k}_l", [(x + 128, ry + 18), (x + 168, cy)], ROOM, 1)
        els += [_el("rectangle", f"{eid}{k}", x + 168, cy - 22, 270, 44, ROOM, "#ffffff", roundness={"type": 3})]
        nx = x + 178 + (6.2 * len(pill) + 8 if pill else 0)
        els += (text(f"{eid}{k}_p", x + 178, cy - 17, pill, 10, BODY) if pill else []) + text(f"{eid}{k}_n", nx, cy - 18, name, 12, TITLE)
        els += text(f"{eid}{k}_w", x + 178, cy + 3, words, 11, BODY)
        for j, cn in enumerate(children):
            chy = by + 30 * j + 2
            els += line(f"{eid}{k}_{j}_l", [(x + 438, cy), (x + 462, chy + 13)], ROOM, 1)
            els += [_el("rectangle", f"{eid}{k}_{j}", x + 462, chy, w - 462, 26, ROOM, "#ffffff", roundness={"type": 3})]
            els += text(f"{eid}{k}_{j}_n", x + 470, chy + 6, cn, 11, INK)
        by += bh + 10
    return els


def tree_h(branches):
    return sum(max(1, len(b[3])) * 30 + 10 for b in branches) - 10


def k_lead(eid, x, y, w, label, words, state, tags):
    """A topic or a delivery as its card, large: its picture, its name, its one line big, its word, its tags. A topic
    that waits on you carries Answer beside its word (s53, s56 r01), not a sixth tag."""
    els = [_el("rectangle", eid, x, y, w, 104, ROOM, "#ffffff", roundness={"type": 3})]
    els += [_el("rectangle", eid + "_p", x + 10, y + 10, 140, 84, ROOM, GHOST)]
    els += text(eid + "_a", x + 164, y + 10, label, 12, TITLE) + text(eid + "_w", x + 164, y + 32, words, 16, INK)
    els += text(eid + "_s", x + 164, y + 58, state, 12, state_color(state))
    if state.startswith("🙋"):
        els += _btns(eid + "_ans", x + 164 + 6.6 * len(state) + 86, y + 54, ("Answer",), OR)
    return els + text(eid + "_v", x + 164, y + 80, tags, 11, BLUE)


def k_trows(eid, x, y, w, items):
    """Studio rows (JL 261029): picture, name, the one line it asks, its stage as one word, then its tags; a rolled-up
    topic says where it sits (haipipe-ui: `s22 · j02`)."""
    els = []
    for k, (label, words, stage, *where) in enumerate(items):
        ry = y + 74 * k
        els += [_el("rectangle", f"{eid}{k}", x, ry, w, 66, ROOM, "#ffffff", roundness={"type": 3})]
        els += [_el("rectangle", f"{eid}{k}_p", x + 10, ry + 9, 76, 48, ROOM, GHOST)]
        els += text(f"{eid}{k}_a", x + 98, ry + 7, label, 11, TITLE) + text(f"{eid}{k}_w", x + 98, ry + 25, words, 12, INK)
        if where:
            els += text(f"{eid}{k}_at", x + 98 + 6.0 * len(label) + 8, ry + 7, f"· at {where[0]}", 11, BODY)
        els += text(f"{eid}{k}_s", x + w - 70, ry + 25, stage, 11, state_color(stage))
        els += text(f"{eid}{k}_v", x + 98, ry + 45, TAGS, 10, BLUE)
    return els


def k_line(eid, x, y, w, words):
    return text(eid, x + 4, y, words, 12, INK)


def k_agent(eid, x, y, w, verbs):
    """Ask the agent: one notes box, then its Copy prompt buttons (s58, s59)."""
    els = [_el("rectangle", eid, x, y, w, 36, ROOM, "#ffffff", roundness={"type": 3}, strokeStyle="dashed")]
    els += text(eid + "_t", x + 12, y + 10, "your notes, copied with the prompt", 12, BODY)
    return els + _btns(eid + "_b", x + w, y + 46, verbs)


# ── a step's own shape, as b15 draws each labeling step (JL 261101: "check ... b15_theme_labeling ... Task UI"):
# In → who works → Out, your part, then its results; the steps are haipipe-task's life (ref/lifecycle.md) ────────────
def k_flow(eid, x, y, w, inn, who, out):
    """The step read left to right: what goes in, who works on it (an agent, or 🙋 you), what comes out; each box a
    title and up to two lines; the Run that does the work is the who box's line."""
    bw = (w - 2 * 34) / 3
    els = []
    for k, (label, box) in enumerate((("In", inn), ("Who works", who), ("Out", out))):
        bx = x + k * (bw + 34)
        you = k == 1 and box[0].startswith("🙋")
        els += [_el("rectangle", f"{eid}{k}", bx, y, bw, 84, OR if you else ROOM, "#fff4e6" if you else "#ffffff", roundness={"type": 3})]
        els += text(f"{eid}{k}_l", bx + 10, y + 6, label, 10, OR if you else (PU if k == 1 else (GR if k == 2 else BODY)))
        els += text(f"{eid}{k}_h", bx + 10, y + 22, box[0], 13, INK)
        for j, ln in enumerate(box[1:3]):
            els += text(f"{eid}{k}_{j}", bx + 10, y + 42 + 18 * j, ln, 11, BODY) if ln else []
        if k:
            els += arrow(f"{eid}{k}_a", [(bx - 30, y + 42), (bx - 4, y + 42)], ROOM)
    return els


def k_ask(eid, x, y, w, words, verb="", mode="interaction"):
    """Your part of the step: one that waits on you (orange, 🙋), a sign or read you give (blue, ✍️), done (green, ✅),
    or none (a plain line)."""
    stroke, fill = {"interaction": (OR, "#fff4e6"), "gate": (BLUE, "#f1f8ff"), "done": (GR, "#ffffff"),
                    "none": ("#e9ecef", "#ffffff")}[mode]
    els = [_el("rectangle", eid, x, y, w, 36, stroke, fill, roundness={"type": 3})] + text(eid + "_t", x + 12, y + 9, words, 13, INK)
    return els + (_btns(eid + "_b", x + w - 10, y + 6, (verb,), OR if mode == "interaction" else BLUE) if verb else [])


def k_kv(eid, x, y, w, rows):
    els = []
    for k, (key, val) in enumerate(rows):
        els += text(f"{eid}{k}k", x + 4, y + 4 + 24 * k, key, 12, BODY)
        els += text(f"{eid}{k}v", x + 130, y + 4 + 24 * k, val, 13, state_color(val) if val[:1] in "🙋✅⏳⬜" else INK)
    return els


def k_table(eid, x, y, w, head_, rows):
    """A small table, as the file reads; the first column wider; a state cell keeps its word and colour."""
    n = len(head_)
    widths = [1.8] + [1.0] * (n - 1)
    unit = (w - 16) / sum(widths)
    xs = [x + 8 + unit * sum(widths[:j]) for j in range(n)]
    els = [_el("rectangle", eid, x, y, w, 24 * (len(rows) + 1) + 6, ROOM, "#ffffff", roundness={"type": 3})]
    for j, c in enumerate(head_):
        els += text(f"{eid}h{j}", xs[j], y + 6, c, 11, TITLE)
    for i, r in enumerate(rows):
        els += line(f"{eid}l{i}", [(x, y + 26 + 24 * i), (x + w, y + 26 + 24 * i)], "#e9ecef", 1)
        for j, c in enumerate(r):
            els += text(f"{eid}r{i}_{j}", xs[j], y + 31 + 24 * i, c, 11, state_color(c) if c[:1] in "🙋✅⏳⬜" else INK)
    return els


def k_checklist(eid, x, y, w, items):
    """What the close needs (haipipe-task ref/lifecycle.md § Close): each condition a row, its state word on the right."""
    els = []
    for k, (words, state, *verb) in enumerate(items):
        open_ = not state.startswith("✅")
        els += line(f"{eid}{k}_l", [(x, y + 30 * k + 24), (x + w, y + 30 * k + 24)], "#e9ecef", 1)
        els += text(f"{eid}{k}_t", x + 8, y + 30 * k + 3, words, 13, INK if open_ else BODY)
        els += text(f"{eid}{k}_s", x + 330, y + 30 * k + 3, state, 12, state_color(state) if open_ else GR)
        if verb:
            els += _btns(f"{eid}{k}_b", x + w - 4, y + 30 * k - 1, verb, OR if state.startswith("🙋") else BLUE)
    return els


def k_chain(eid, x, y, w, steps):
    """A sequence as boxes and arrows, a role word above each (b16, b15): what goes in, what it becomes, where it lands."""
    bw = (w - 30 * (len(steps) - 1)) / len(steps)
    els = []
    for k, (role, name) in enumerate(steps):
        bx = x + k * (bw + 30)
        els += text(f"{eid}{k}_r", bx + 2, y, role, 10, BODY)
        els += [_el("rectangle", f"{eid}{k}", bx, y + 16, bw, 46, ROOM, "#ffffff", roundness={"type": 3})]
        els += text(f"{eid}{k}_w", bx + 10, y + 24, name, 12, INK)
        if k:
            els += arrow(f"{eid}{k}_a", [(bx - 27, y + 39), (bx - 4, y + 39)], ROOM)
    return els


def k_picture(eid, x, y, w, caption, verbs):
    """A figure, small; a click opens it large in the pop-out."""
    els = [_el("rectangle", eid, x, y, 230, 92, ROOM, "#ffffff")]
    for k in range(4):                                       # a few bars, so it reads as a chart, not an empty box
        bh = (22, 48, 36, 60)[k]
        els += [_el("rectangle", f"{eid}_b{k}", x + 24 + 48 * k, y + 80 - bh, 26, bh, "#74c0fc", "#a5d8ff")]
    return els + text(eid + "_c", x + 246, y + 8, caption, 12, INK) + _btns(eid + "_v", x + w - 4, y + 60, verbs)


def k_grid(eid, x, y, w, steps, rows):
    """Each Task against its life's steps (as b16's version Work: one row per Section, its five step words): a row per
    Task, a cell per step, the word of where that step stands; a group row names the Job; a waiting cell is orange."""
    nw = 200
    cw = (w - nw) / len(steps)
    els = [text(f"{eid}_h{j}", x + nw + j * cw + 8, y, s, 11, TITLE)[0] for j, s in enumerate(steps)]
    yy = y + 22
    for i, (name, cells) in enumerate(rows):
        if cells is None:                                    # a group row: the Job these Tasks sit in
            els += text(f"{eid}g{i}", x + 2, yy + 6, name, 11, BODY)
            yy += 26
            continue
        els += text(f"{eid}n{i}", x + 8, yy + 7, name, 12, TITLE)
        for j, c in enumerate(cells):
            wait = c.startswith("🙋")
            els += [_el("rectangle", f"{eid}c{i}_{j}", x + nw + j * cw + 2, yy, cw - 6, 28, OR if wait else "#e9ecef",
                        "#fff4e6" if wait else "#ffffff", roundness={"type": 3})]
            els += text(f"{eid}c{i}_{j}t", x + nw + j * cw + 8, yy + 7, c, 11, state_color(c))
        yy += 34
    return els


def grid_h(rows):
    return 22 + sum(26 if c is None else 34 for _, c in rows)


def k_fork(eid, x, y, w, first, others):
    """The Jobs as a pipeline: the one that feeds the others on the left, the ones it feeds on the right, arrows between;
    each box its name, its state word, its one line."""
    def box(k, bx, by, b):
        name, state, words = b
        wait = state.startswith("🙋")
        return ([_el("rectangle", f"{eid}{k}", bx, by, 260, 62, OR if wait else ROOM, "#fff4e6" if wait else "#ffffff",
                     roundness={"type": 3})] + text(f"{eid}{k}_n", bx + 10, by + 6, name, 13, TITLE)
                + text(f"{eid}{k}_s", bx + 10, by + 26, state, 11, state_color(state)) + text(f"{eid}{k}_w", bx + 10, by + 43, words, 11, BODY))
    tot = 72 * len(others) - 10
    fy = y + tot / 2 - 31
    els = box("f", x, fy, first)
    for k, b in enumerate(others):
        oy = y + 72 * k
        els += arrow(f"{eid}{k}_a", [(x + 262, fy + 31), (x + w - 264, oy + 31)], ROOM) + box(k, x + w - 260, oy, b)
    return els


KIND = {"big": (k_big, lambda a: (56 if a[1] else 30) + 24 * a[0].count("\n")), "asks": (k_asks, lambda a: 48 * len(a[0]) - 8),
        "rows": (k_rows, lambda a: 60 * len(a[0]) - 8), "cardtabs": (k_cardtabs, lambda a: 74 + 24 * len(a[2])),
        "sidetabs": (k_sidetabs, lambda a: sidetabs_h(*a)), "tree": (k_tree, lambda a: tree_h(a[1])),
        "lead": (k_lead, lambda a: 104), "trows": (k_trows, lambda a: 74 * len(a[0]) - 8), "line": (k_line, lambda a: 20),
        "agent": (k_agent, lambda a: 70), "flow": (k_flow, lambda a: 84), "ask": (k_ask, lambda a: 36),
        "kv": (k_kv, lambda a: 24 * len(a[0])), "table": (k_table, lambda a: 24 * (len(a[1]) + 1) + 6),
        "checklist": (k_checklist, lambda a: 30 * len(a[0])), "picture": (k_picture, lambda a: 92),
        "grid": (k_grid, lambda a: grid_h(a[1])), "fork": (k_fork, lambda a: 72 * len(a[1]) - 10),
        "chain": (k_chain, lambda a: 62)}


def sec_h(sec):
    if sec[0] == "rule":
        return 24
    if sec[0] in ("group", "next"):
        return 36 if sec[0] == "group" else 26
    return (40 if sec[0] else 0) + KIND[sec[1]][1](sec[2:]) + (10 if sec[1] in ("flow",) and not sec[0] else 16)


def sec_draw(eid, x, y, w, sec):
    """A numbered heading bar (JL 261031: "each section to be the [heading bar] ... seems to be ordered"), then its
    content as what it is; a helper's bar has no number; the dashed rule sets the helpers apart; a group heading
    (⚙️ Process, 📊 Results) and the next step's link, as b15 draws them."""
    if sec[0] == "rule":
        return line(eid, [(x, y + 8), (x + w, y + 8)], ROOM, 1, dashed=True)
    if sec[0] == "group":
        return text(eid, x, y + 6, sec[1], 16, INK) + line(eid + "_l", [(x + 130, y + 18), (x + w, y + 18)], "#dee2e6", 1)
    if sec[0] == "next":
        return text(eid, x + w - 8.5 * len(sec[1]) - 70, y + 4, f"next: {sec[1]} →", 13, BLUE)
    els = []
    if sec[0]:
        els += [_el("rectangle", eid, x, y, w, 30, ROOM, "#ffffff", roundness={"type": 3})]
        els += text(eid + "_t", x + 12, y + 7, "▾ " + sec[0], 13, TITLE)
        y += 40
    return els + KIND[sec[1]][0](eid + "_c", x, y, w, *sec[2:])


def tall(secs):
    return sum(sec_h(s) for s in secs)


def screen(eid, x, y, h, level, section, views, on, secs, caption):
    """One view as the full page: window, both rails, then in the content column the path, the title-&-section, the
    view-button-list with this view in orange, the goal-line, the view-caption and the view's sections."""
    name, path, goal = PAGE[level]
    els = window(eid + "w", x, y, W, h, f"/_board/workbench?layout=focus&path=…/{name}&section={section}")
    els += rails(eid + "rl", x, y, level, section)
    cx = x + X0
    els += text(eid + "_crumb", cx, y + 40, path, 10, BODY)
    els += head(eid + "h", cx, y + 58, name, section, views, on)
    els += text(eid + "_goal", cx, y + 128, goal, 13, INK)
    els += text(eid + "_cap", cx, y + 152, caption, 12, BODY)
    yy = y + 184
    for k, sec in enumerate(secs):
        els += sec_draw(f"{eid}r{k}", cx, yy, CW, sec)
        yy += sec_h(sec)
    return els


# ── the nine cells' views: (view, its view-caption, its sections in page order) ───────────────────────────────────
# Revised 261101 from round 1's reviews (review/<L>-s1-r01.md): no state on a map (s52-D01); section 1 of a Work view
# is where it stands, one large sentence; what waits sits in the 🙋 Interactions helper at the bottom, naming where the
# form lives; the open card or side tab is blue, so orange means only "waits on you"; topic names in the short form.
WHERE_FORM = f"{ASK} · {TASK} · {FORM}"
WAITS = ("🙋 Interactions", "asks", ((WHERE_FORM, "Answer"),))
BLOCK_REPORT = (                       # s51-D01: the MindMap, then one view per delivery type; D02 to D05 on each card
    ("MindMap", "How it is built: each Job, what it makes, its Tasks.", (
        ("1 · 🗺️ The map", "tree", BLOCK, (
            ("", "j01_cohort_table", "makes b11-s01 · b11-s04", ("t01_build_table", "t02_describe_table")),
            ("", "j21_ols_by_outcome", "makes b11-s02", ("t01_outcome_a", "t02_outcome_b", "t03_outcome_c")),
            ("", "j22_iv_by_outcome", "makes b11-s03", ("t01_outcome_a_iv",)))),
        ("rule",), WAITS)),
    ("Data", "What it hands over as data, each as it reads now.", (
        ("1 · 📦 Deliveries", "sidetabs", (("b11-s01 · cohort_table", "v3 · j01_cohort_table"), ("b11-s04 · codebook", "planned · j01_cohort_table")),
         (("case_id", "year", "exposure", "outcome_a"), (("x", "2016", "x.x", "x"), ("x", "2017", "x.x", "x"), ("x", "…", "…", "…"))),
         (("For", "the table every model reads"),), TAGS),
        ("rule",), WAITS)),
    ("Display", "What it hands over as tables and figures, each as it reads now.", (
        ("1 · 📦 Deliveries", "sidetabs", (("b11-s02 · model_tables", "v2 · j21_ols_by_outcome"), ("b11-s03 · iv_tables", "planned · j22_iv_by_outcome")),
         (("", "outcome A", "outcome B", "outcome C"), (("exposure", "x.xx", "x.xx", "…"), ("age", "x.xx", "x.xx", "…"))),
         (("For", "the tables the paper prints"),), TAGS),
        ("rule",), WAITS)),
)
BLOCK_STUDIO = (                       # the Block's groups, each topic under where it sits (s53 r04 Q2, pick A)
    ("Data", "The topics in the Data group, at the Block and below.", (
        ("1 · 💡 Lead topic", "lead", S01, "keep the cases with no year?", "agreed", TAGS),
        ("2 · 🧩 At the Block", "trows", ((S04, "one codebook, or one per year?", "explore"),)))),
    ("Display", "The topics in the Display group, at the Block and below.", (
        ("1 · 💡 Lead topic", "lead", S02, ASK, "🙋 waits on you", TAGS),
        ("2 · 🧩 At the Block", "trows", ((S03, "which instrument?", "explore"),)),
        ("3 · 🧩 At j21_ols_by_outcome", "trows", ((S11, "cluster by state, or by physician?", "shaping", "j21"),
                                                  (S21, "add the age control?", "explore", "t01_outcome_a"))))),
)
JOB_STUDIO = (                         # s56: the topic it makes first, then its own, then its Tasks' (form Q1, pick A)
    ("Display", "The topics in the Display group: what this Job makes, its own, then its Tasks'.", (
        ("1 · 🎯 This Job makes", "lead", S02, ASK, "🙋 waits on you", TAGS),
        ("2 · 🧩 Its own", "trows", ((S11, "cluster by state, or by physician?", "shaping"),)),
        ("3 · 🧩 Its Tasks'", "trows", ((S21, "add the age control?", "explore", "t01_outcome_a"),)))),
)
TASK_STUDIO = (                        # s59: what this Task makes, its own topics; Ask the agent a helper (form Q4, pick A)
    ("Display", "The topics in the Display group: what this Task makes, then its own.", (
        ("1 · 🎯 This Task makes", "lead", S02, "its piece: outcome A's table, v2", "🙋 waits on you", TAGS),
        ("2 · 🧩 Its topics", "trows", ((S21, "add the age control?", "explore"),)),
        ("rule",), WAITS,
        ("✍️ Ask the agent", "agent", ("Copy prompt: talk and sketch", "Copy prompt: start a topic")))),
)
# ── the Task's life, step by step: the views b15 draws for each labeling step, here from haipipe-task's
# ref/lifecycle.md (what each step leaves on disk, and who writes it): plan ▶ build ▶ run ▶ read ▶ close ──────────────
TASK_STEP = {
    "Plan": ("Plan: the Job's item, the goal and close, a card per Run.", [
        ("group", "⚙️ Process"),
        ("1 · 🧭 Plan the Runs", "flow", ("j21's Deliverables item", "outcome A's table in b11-s02", "goal: and close:"),
         ("🤖 Agent", "run-plan-t01", "one Run per window"), ("Planned Run cards", "status: planned", "r01 to r03, r05, r06")),
        ("", "ask", "✅ you agreed the plan on 10-26", "", "done"),
        ("group", "📊 Results"),
        ("2 · 🎯 Goal and close", "kv", (("goal", "outcome A's model, in every window"),
                                        ("close", "every window's model has its table, read"),
                                        ("feeds", "j21's item: outcome A's table in b11-s02"))),
        ("3 · 📋 The Runs it plans", "table", ("Run", "role", "what it makes"),
         (("r01_years_16_19", "make", "the model, 2016 to 2019"), ("r02_years_16_23", "make", "the model, 2016 to 2023"),
          ("r03_years_16_23_robust", "make", "the same, robust errors"), ("r05_describe_table", "describe", "the Table Card"),
          ("r06_figures_coef", "figures", "the coefficient plot"))),
        ("next", "B · Build")]),
    "Build": ("Build: the worker, each Run's config and ticket, then the review.", [
        ("group", "⚙️ Process"),
        ("1 · 🔧 Build the code", "flow", ("Planned Run cards", "r01 to r03", ""),
         ("🤖 The fit skill's creator", "run-build-t01", ""), ("Worker · config · ticket", "scripts/fit_ols.py", "one config, one ticket a Run")),
        ("", "ask", "✅ the reviewer passed the code before any Run (Gate 1)", "Open review", "done"),
        ("group", "📊 Results"),
        ("2 · 📁 What it built", "table", ("file", "what it is"),
         (("scripts/fit_ols.py", "the worker, every window"), ("r03_…/config.yaml", "the window's values, its purpose first"),
          ("r03_…/r03_years_16_23_robust.sh", "the ticket: it writes the receipt"))),
        ("3 · 🔎 Code review", "kv", (("CODE_REVIEW.md", "✅ pass, 10-26"), ("checked", "the worker against the Task's goal"),
                                     ("open", "nothing"))),
        ("next", "C · Run")]),
    "Run": ("Run: each ticket pressed, its receipt from running to complete.", [
        ("group", "⚙️ Process"),
        ("1 · 🏃 Run the tickets", "flow", ("Ticket + config", "r03_years_16_23_robust.sh", ""),
         ("🙋 You press Run", "a long Run waits for you", "AGENTS rule 2"), ("The receipt", "result/runtime.yaml", "running ▶ complete")),
        ("", "ask", "🙋 r03_years_16_23_robust is built: press Run on the server", "Copy command", "interaction"),
        ("group", "📊 Results"),
        ("2 · 🧾 Receipts", "table", ("Run", "status", "started", "finished"),
         (("r01_years_16_19", "✅ complete", "10-27 09:12", "10-27 11:40"), ("r02_years_16_23", "⏳ running", "10-31 08:05", ""),
          ("r03_years_16_23_robust", "⬜ built", "", ""))),
        ("3 · 🔁 Passes", "line", "r02 failed once on 10-29; that pass stays in passes/p01-1029"),
        ("next", "D · Read")]),
    "Read": ("Read: the headline, its table and figure, and which window leads.", [
        ("group", "⚙️ Process"),
        ("1 · 📖 Read the results", "flow", ("result/ files", "r01: tables/, metrics.json", ""),
         ("🤖 Describe and figures Runs", "r05_describe_table", "r06_figures_coef"), ("Headline · Table Card · figure", "", "")),
        ("", "ask", f"🙋 {ASK} · {FORM}", "Answer", "interaction"),
        ("group", "📊 Results"),
        ("2 · 📌 Headline", "big", "Outcome A is higher where exposure is higher.", "draft until r04 is answered · r01_years_16_19"),
        ("", "ask", "✍️ your read: mark r01 read once you have read it", "Mark read", "gate"),
        ("3 · 📊 Table Card · r05_describe_table", "table", ("", "estimate", "95% CI", "n"),
         (("exposure", "x.xx", "x.xx to x.xx", "x,xxx"), ("age", "x.xx", "x.xx to x.xx", ""), ("year", "x.xx", "x.xx to x.xx", ""))),
        ("4 · 📈 Coefficient plot · r06_figures_coef", "picture", "the coefficients, window by window", ("Open",)),
        ("next", "E · Close")]),
    "Close": ("Close: every receipt against the close line; then the Job's item ticks.", [
        ("group", "⚙️ Process"),
        ("1 · 🏁 Check the close", "flow", ("Every receipt", "and the close: line", ""), ("🤖 Agent", "run-check-t01", ""),
         ("close: not yet", "then the Job's item ticks", "")),
        ("group", "📊 Results"),
        ("2 · 🚧 Where the close stands", "big", "Not closed yet: Runs to finish,\nyour answer and your read.", "⬜ not yet"),
        ("3 · 📋 What the close needs", "checklist", (
            ("which window leads", "🙋 waits on you", "Answer"),
            ("r01_years_16_19 read by you", "⬜ not yet", "Read"),
            ("r02_years_16_23 done", "⏳ running"), ("r03_years_16_23_robust done", "⬜ built, not run"),
            ("r05_describe_table, r06_figures_coef", "⬜ planned"),
            ("each Result gate passed", "✅ yes, r01"), ("each receipt current", "✅ yes"))),
        ("4 · 🎯 What it ticks", "kv", (("j21_ols_by_outcome", "⬜ not yet: outcome A's table in b11-s02 · model_tables"),))]),
}
STEPS = ("Plan", "Build", "Run", "Read", "Close")
MAP_TASK = ("1 · 🧠 The mind map", "tree", TASK, (
    ("topic", "b11-s21 · outcome_a_controls", "add the age control?", ()),
    ("make", "the model", "one Run per window", ("r01_years_16_19", "r02_years_16_23", "r03_years_16_23_robust")),
    ("read", "the results", "a Table Card, a figure", ("r05_describe_table", "r06_figures_coef")),
    ("check", "the close", "every receipt against it", ("run-check-t01",))))


def report_of(step):
    """Report shows a step's results only, read only (b15: "Report shows the Results only"), numbered from 1."""
    caption, secs = TASK_STEP[step]
    k = next(i for i, s in enumerate(secs) if s[0] == "group" and s[1] == "📊 Results")
    out, n = [], 0
    for s in secs[k + 1:]:
        if s[0] in ("next", "group"):
            continue
        n += 1
        out.append((re.sub(r"^\d+ · ", f"{n} · ", s[0]),) + s[1:])
    return out


TASK_WORK = tuple((s, TASK_STEP[s][0], tuple(TASK_STEP[s][1])) for s in STEPS)
TASK_REPORT = (                        # the MindMap first (s51-D01), then each step's results; Run and Close are Work's
    ("MindMap", "The Task as a map: its topic, its Runs by what they do.", (MAP_TASK, ("rule",), WAITS)),
    ("Plan", "What it set out to make, who makes it, where it lands.", (
        ("1 · 🎯 Done when", "big", "Every window's model has its table, and it is read.", "✅ agreed, 10-26"),
        ("2 · 🔗 What it makes", "flow", ("cohort_table", "v3, made by j01_cohort_table", ""),
         ("🤖 scripts/fit_ols.py", "r01 to r03, one Run a window", ""), ("Three window models", "r01 v2 · r02, r03 planned", "")),
        ("3 · 📦 Where it lands", "kv", (("b11-s02", "model_tables: outcome A's table, v2"),)))),
    ("Build", "The code its Runs run, and its review: the thing to read.", (   # Report shows the thing, not its steps (s57 C r05)
        ("1 · 🔎 Code review", "big", "scripts/fit_ols.py passed review against the Task's goal.", "✅ pass, 10-26"),
        ("", "rows", (("✅ pass", "CODE_REVIEW.md", "checked against the Task's goal · open issues: none", ("Open",), ""),)),
        ("2 · 📄 The code", "sidetabs", (("scripts/fit_ols.py", "the worker"), ("config.yaml", "r01_years_16_19"),
                                       ("r01_years_16_19.sh", "the ticket")),
         None, (("1", "def fit(window):"), ("2", "    rows = read_table(cohort_table, years=window)"),
                ("3", "    model = ols(outcome_a ~ exposure + age + year)"), ("4", "    write_table(model, result/tables/)"),
                ("", "Open the file")), ""))),
    ("Read", "What it found: the headline, the table, the figure.", tuple(report_of("Read")) + (("rule",), WAITS)),
)
JOB_WORK = (                           # s55: each Task against its five steps, as b16's version Work
    ("Progress", "Where it stands, then each Task against its five steps.", (
        ("1 · 📍 Where it stands", "big", "Done when each outcome's OLS table is in b11-s02 · model_tables.", "⏳ running · 🙋 t01 waits on you"),
        ("2 · 🧩 Tasks, step by step", "grid", STEPS,
         (("t01_outcome_a", ("✅ agreed", "✅ passed", "⏳ running", "🙋 waits", "⬜ not yet")),
          ("t02_outcome_b", ("✅ agreed", "✅ passed", "⏳ running", "⬜ not yet", "⬜ not yet")),
          ("t03_outcome_c", ("✅ agreed", "⬜ not yet", "⬜ not yet", "⬜ not yet", "⬜ not yet")))),
        ("3 · ⚙️ Its own Runs", "rows", (("⬜ not started", "run-plan-j21", "soft · plan the next outcome's Task", ("Open",), ""),)),
        ("rule",), WAITS)),
)
JOB_REPORT = (                         # s54: the MindMap, then the one type it makes; its finding across the Tasks
    ("MindMap", "How it is built: what it makes, its Tasks, their Runs.", (
        ("1 · 🧠 The mind map", "tree", JOB, (
            ("makes", "b11-s02 · model_tables", "the OLS tables, one per outcome", ()),
            ("", "t01_outcome_a", "outcome A's model, in every window", ("r01_years_16_19", "r02_years_16_23", "r03_years_16_23_robust")),
            ("", "t02_outcome_b", "outcome B's model, in every window", ("r01_years_16_19",)),
            ("", "t03_outcome_c", "outcome C's model, in every window", ("r01_years_16_19",)))),
        ("rule",), WAITS)),
    ("Display", "What it makes: one table across its Tasks, and the figure.", (
        ("1 · 📌 What it found", "big", "Outcome A rises with exposure; B and C are not read yet.", "b11-s02 · v2"),
        ("2 · 📊 The table, by Task", "table", ("", "outcome A · t01", "outcome B · t02", "outcome C · t03"),
         (("exposure", "x.xx (v2)", "planned", "planned"), ("age", "x.xx (v2)", "planned", "planned"), ("n", "x,xxx", "", ""))),
        ("3 · 📈 The figure", "picture", "each outcome's coefficient, side by side", ("Open",)),
        ("4 · 📦 The delivery", "lead", S02, "the OLS tables, one per outcome", "v2", TAGS),
        ("rule",), WAITS)),
)
BLOCK_WORK = (                         # s52-D01: where things stand lives here: the Jobs as a pipeline, every Task's steps
    ("Progress", "Where it stands, then each Job and the step each Task is on.", (
        ("1 · 📍 Where it stands", "big", "j21_ols_by_outcome waits on you: which window leads?", "done when every outcome has its OLS and IV table"),
        ("2 · 🧱 Jobs", "cardtabs", (("j01_cohort_table", "✅ done"), ("j21_ols_by_outcome", "🙋 waits on you"),
                                     ("j22_iv_by_outcome", "⬜ not started")), 1,
         (("Goal", "the OLS models, one Task per outcome"), ("Makes", "b11-s02 · model_tables · v2"),
          ("t01_outcome_a", "Read waits on you · Run running"), ("t02_outcome_b", "Run running · Build passed"),
          ("t03_outcome_c", "Plan agreed · Build not started")), ("Open",)),
        ("3 · ⚙️ Its own Runs", "rows", (("✅ answered", "r01_collect_cohort_rules", "collect · Cohort rules", ("Open",), ""),)),
        ("rule",), WAITS)),
)
VIEWS = {   # (level, section): (the line above the screens, the views, the open question)
    ("block", "report"): ("the MindMap, then one view per delivery type (s51-D01); a delivery opens from its tags (D02)",
                          BLOCK_REPORT, "? a type view: the deliveries\nas side tabs, or one card each"),
    ("block", "work"): ("one view: what waits on you, then each Job as a card tab, the step each Task is on, in words (s52-D01)",
                        BLOCK_WORK, "? a Job's Tasks: their steps\nin words, or as a grid"),
    ("block", "studio"): ("one view per group of the Block's _studio_groups.txt; each topic under where it sits",
                          BLOCK_STUDIO, "? the lead topic large,\nor every topic the same row"),
    ("job", "report"): ("the MindMap, then the one type this Job makes: one table across its Tasks", JOB_REPORT,
                        "? one table across the Tasks,\nor a table per Task"),
    ("job", "work"): ("one view: each Task against the five steps of a Task's life (haipipe-task ref/lifecycle.md)", JOB_WORK,
                      "? a step word opens that\nstep on the Task's page"),
    ("job", "studio"): ("the groups of the topics it shows: what it makes, its own, its Tasks'", JOB_STUDIO,
                        "? show the Block topic it\nmakes, or only its own"),
    ("task", "report"): ("the MindMap, then each step's results, read only: Plan, Build, Read (Run and Close are Work's)",
                         TASK_REPORT, "? Read first after the map,\nor in the life's order"),
    ("task", "work"): ("one view per step of a Task's life: plan ▶ build ▶ run ▶ read ▶ close (haipipe-task ref/lifecycle.md)",
                       TASK_WORK, "? one view per step,\nor one Runs view"),
    ("task", "studio"): ("the groups of the topics it shows; Ask the agent a helper", TASK_STUDIO,
                         "? start a topic here\nwith one click"),
}
PIECE = {
    ("block", "report"): ("the Block's Report: the map, and its deliveries by type",
                          ["the Report showed Status,\nFindings and Questions", "a delivery opened only\nfrom a Studio row",
                           "no view showed what\nthe Block hands over"]),
    ("block", "work"): ("the Block's Work: where it stands, each Job's steps",
                        ["where things stand sat\nin the Report", "a waiting form hid in\na Job's row",
                         "a Job row did not say\nwhat it makes"]),
    ("block", "studio"): ("the Block's Studio: its topics by group",
                          ["topics sat in studio/,\nout of sight", "a card's tags did not\nsay what they open",
                           "nothing said which\ntopic waits on you"]),
    ("job", "report"): ("a Job's Report: its map, one table across its Tasks",
                        ["a Job page repeated\nthe Block's views", "its delivery sat in\nthe Block's topic",
                         "no view said what\nthe Job hands over"]),
    ("job", "work"): ("a Job's Work: each Task against its five steps",
                      ["Tasks sat as plain rows", "the order was the\nfolders', not the plan's",
                       "a Run hid two\nclicks deep"]),
    ("job", "studio"): ("a Job's Studio: the topics it makes and holds",
                        ["a Job showed only\nits own topics", "the topic it makes\nsat at the Block",
                         "nothing linked the two"]),
    ("task", "report"): ("a Task's Report: its plan, code and results",
                         ["a Task's Report listed\nreceipts, not results", "the newest result was\nclicks away",
                          "a check's verdict\nhad no place"]),
    ("task", "work"): ("a Task's Work: one view per step, plan to close",
                       ["Runs sat as bare rows", "a built ticket did not\nsay you press Run",
                        "no prompt to plan,\nbuild or check"]),
    ("task", "studio"): ("a Task's Studio: what it makes, its own topics",
                         ["a Task's Studio showed\nthe Block's topics", "no line said which\npiece it makes",
                          "no talk-and-sketch\nprompt"]),
}
AGREED = {}                            # (level, section): {letter: sections}, the letters settled so far
MOCK = """<!doctype html><meta charset=utf-8><title>{letter} · {view}</title>
<!-- GENERATED by work_ui_cells.py from AGREED; the agreed screen of {nn} view {letter} -->
<style>body{{font:14px system-ui;margin:24px;max-width:820px;color:#1e1e1e;background:#fff}}h1{{font-size:22px;margin:0}}
h1 small{{color:#868e96;font-weight:400;margin-left:8px}}nav{{margin:12px 0 18px}}nav span{{display:inline-block;border:1px solid
#ced4da;border-radius:6px;padding:3px 9px;margin-right:6px;font-size:12px}}nav span.on{{border-color:#1864ab;background:#e7f5ff}}
section{{border:1px solid #dee2e6;border-radius:8px;padding:9px 14px;margin:8px 0}}section b{{font-size:13px}}</style>
<h1>{name}<small>{section}</small></h1><nav>{nav}</nav>{secs}"""


def slug(view):
    return re.sub(r"[^a-z0-9]+", "-", view.lower()).strip("-")


def cell(topic: Path):
    m = re.match(r"s(\d+)-(block|job|task)-ui-(report|work|studio)$", Path(topic).name)
    return m.group(1), m.group(2), m.group(3)


def screen_h(items):
    return 214 + max(tall(secs) for _, _, secs in items)


def screens(eid, x, y, items, level, section, gap=40):
    """Every view lettered A, B, C …, every screen the same size (the tallest view's), three a row (JL 261031)."""
    cols, h = min(3, len(items)), screen_h(items)
    views = tuple(v for v, _, _ in items)
    els = []
    for k, (view, caption, secs) in enumerate(items):
        sx, sy = x + (k % cols) * (W + gap), y + (k // cols) * (h + 40 + gap)
        els += text(f"{eid}{k}_L", sx, sy, f"{LETTERS[k]} · {view}", 22, TITLE)
        els += screen(f"{eid}{k}", sx, sy + 40, h, level, section, views, k, secs, caption)
    return els, y + ((len(items) + cols - 1) // cols) * (h + 40 + gap)


def flat(sec):
    """(title, one line) of a section, for the agreed screen file."""
    if sec[0] == "rule":
        return "", ""
    words = {"tree": lambda: " · ".join(b[1] for b in sec[3]), "sidetabs": lambda: " · ".join(h for h, _ in sec[2]),
             "cardtabs": lambda: " · ".join(t for t, _ in sec[2]), "asks": lambda: " · ".join(w for w, _ in sec[2]),
             "rows": lambda: " · ".join(r[1] for r in sec[2]), "trows": lambda: " · ".join(r[0] for r in sec[2]),
             "lead": lambda: f"{sec[2]} · {sec[3]}", "agent": lambda: " · ".join(sec[2])}.get(sec[1], lambda: str(sec[2]))()
    return sec[0], words


def write_agreed(topic, nn, level, section):
    """delivery/ui/<level>-<section>/<L>-<view>.html for each settled letter; the screen, placeholder words only."""
    items = VIEWS[(level, section)][1]
    names = [v for v, _, _ in items]
    for letter, secs in AGREED.get((level, section), {}).items():
        view = names[LETTERS.index(letter)]
        out = topic / "delivery" / "ui" / f"{level}-{section}" / f"{letter}-{slug(view)}.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        nav = "".join(f'<span class={"on" if v == view else "off"}>{v}</span>' for v in names)
        out.write_text(MOCK.format(letter=letter, view=view, nn=f"s{nn}", name=PAGE[level][0], section=VERB[section], nav=nav,
                                   secs="".join(f"<section><b>▾ {t}</b><br><small>{w}</small></section>"
                                                for t, w in map(flat, secs) if t)) + "\n", encoding="utf-8")


def build(topic: Path):
    topic = Path(topic).resolve()
    nn, level, section = cell(topic)
    piece, why = PIECE[(level, section)]
    lay, items, ask = VIEWS[(level, section)]
    names = [v for v, _, _ in items]
    last = LETTERS[len(names) - 1]
    write_agreed(topic, nn, level, section)
    ui = topic / "delivery" / "ui"
    pieces = [("page", f"ui/{level}-{section}/{L}-{slug(v)}.html", f"{L} · the {v} view",
               (ui / f"{level}-{section}" / f"{L}-{slug(v)}.html").exists()) for L, v in zip(LETTERS, names)]
    sk = topic / "delivery" / "skill" / f"{level}-{section}-views.md"
    pieces.append(("book", f"skill/{sk.name}", "the views' manual, for workbench-work", sk.exists()))
    spec = {"title": f"{level.capitalize()} UI · {VERB[section]}: {piece.split(': ', 1)[1]}",
            "why": {"question": f"why do we need s{nn}?", "notes": why,
                    "quote": "JL 261101: use the /haipipe-ui loop to check all the UIs and update them"},
            "what": {"head": f"② what s{nn} hands over: one screen, A to {last}", "icon": "page", "name": "delivery/ui/",
                     "type": "ui", "deck_why": f"stays in s{nn}'s delivery/deck/, so anyone gets it in a minute", "parts": pieces},
            "job": topic.parent.parent,
            "target": "servers/workbench/focus_page.py · workbench-work/SKILL.md",
            "missing": [(name, "not settled yet") for _, name, _, done in pieces if not done],
            "have": [(name, "agreed") for icon, name, _, done in pieces if done and icon == "page"]}

    def design():                                    # A, B, C … every view the same screen; no separate main sketch
        els = text("skA", 690, 280, f"A to {last} · {piece}, every view the same screen", 18, TITLE)
        els += text("lay", 690, 340, lay, 16, BODY)
        e, bottom = screens("sc", 690, 380, items, level, section)
        if (level, section) == ("task", "work"):            # a Run's pop-out, opened from any Run row (JL 261103)
            sx = 690 + 2 * (W + 40)
            els += text("popL", sx, bottom - (screen_h(items) + 120), "P · a Run's pop-out", 22, TITLE)
            pe, _ = popout("pop", sx, bottom - (screen_h(items) + 80))
            els += pe
        return els + e + sticky("askD", 1180, bottom + 20, 320, 76, ask, 15, -0.03, RED, RE)

    return five_parts.build(topic, spec, design, shift=(W + 40) * min(3, len(items)) - 300)


# ── a Run's pop-out (JL 261103: "when I click a run, it will show all the information from that run folder with a pop
# out window, so we can quickly understand what happened"): everything in runs/<run>/, read in place, over the page ───
RUN_POP = (
    ("1 · 📌 What happened", "big", "Outcome A is higher where exposure is higher.", "✅ complete · 10-27, 09:12 to 11:40 · pass p01"),
    ("2 · 📊 What it made · result/", "sidetabs", (("RUN-REPORT.md", "the report"), ("tables/coef.csv", "the table"),
                                                  ("figures/coef.png", "the figure"), ("metrics.json", "the numbers")),
     None, (("", "# r01_years_16_19 · the model, 2016 to 2019"), ("", "Headline: outcome A is higher where exposure is higher."),
            ("", "Rows: x,xxx cases · years 2016 to 2019"), ("", "Table: tables/coef.csv · Figure: figures/coef.png"),
            ("", "Open the file")), ""),
    ("3 · 🎫 How it ran · run.yaml, ticket, config", "kv", (("what it does", "makes the model, one window"),
                                                          ("reads", "cohort_table v3, 2016 to 2019"),
                                                          ("who", "you pressed Run · fit skill"),
                                                          ("ticket", "r01_years_16_19.sh  ·  Copy command"),
                                                          ("config", "config.yaml: window 2016 to 2019, the OLS model"),
                                                          ("receipt", "result/runtime.yaml"))),
    ("4 · 🔁 Passes · passes/", "rows", (("✅ complete", "p01-1027", "10-27 09:12 · log: wrote result/, gate passed, 11:40 done",
                                         ("Open log",), ""),)),
)


def popout(eid, x, y):
    """The Run's pop-out over the Task's Work: the page dimmed behind; a panel with the Run's name, Close, and its
    folder's parts as numbered sections, the thing it made first."""
    h = 120 + tall(RUN_POP)
    els = [_el("rectangle", eid + "_dim", x, y, W, h + 60, "#868e96", "#e9ecef", roundness={"type": 3})]
    els += text(eid + "_bg", x + 20, y + 10, "t01_outcome_a  Work  (the page, dimmed behind)", 11, BODY)
    px, py, pw = x + 30, y + 40, W - 60
    els += [_el("rectangle", eid + "_p", px, py, pw, h, INK, "#ffffff", roundness={"type": 3})]
    els += text(eid + "_t", px + 20, py + 14, "r01_years_16_19", 20, INK) + text(eid + "_tt", px + 220, py + 19, "Run", 14, BODY)
    els += _btns(eid + "_x", px + pw - 16, py + 14, ("Close",))
    els += text(eid + "_cap", px + 20, py + 50, "Everything in runs/r01_years_16_19/: what it made first, then how it ran.", 12, BODY)
    yy = py + 80
    for k, sec in enumerate(RUN_POP):
        els += sec_draw(f"{eid}r{k}", px + 20, yy, pw - 40, sec)
        yy += sec_h(sec)
    return els, h + 60


def letter_png(topic: Path, letter: str, out: Path, scale: float = 1.0) -> Path:
    """One letter's screen alone, for a Design loop review (haipipe-ui, stage 1): <out>.excalidraw and <out>.png."""
    import subprocess
    topic = Path(topic).resolve()
    _, level, section = cell(topic)
    items = VIEWS[(level, section)][1]
    if letter == "P":                                    # the Run's pop-out (s58)
        e, _ = popout("pop", 0, 40)
        els = text("L", 0, 0, "P · a Run's pop-out", 22, TITLE) + e
    else:
        k = LETTERS.index(letter)
        view, caption, secs = items[k]
        views = tuple(v for v, _, _ in items)
        els = text("L", 0, 0, f"{letter} · {view}", 22, TITLE) + screen("one", 0, 40, screen_h(items), level, section, views, k, secs, caption)
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    drawing = out.with_suffix(".excalidraw")
    five_parts.write(drawing, els)
    render = TOOLS / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts/render_png.py"
    subprocess.run(["uv", "run", "--no-project", "-q", "--with", "pillow", "python", str(render), str(drawing),
                    str(out.with_suffix(".png")), str(scale)], check=True, stdout=subprocess.DEVNULL)
    return out.with_suffix(".png")


if __name__ == "__main__":                               # python work_ui_cells.py <topic folder> <letter> <out>
    print(letter_png(Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])))
