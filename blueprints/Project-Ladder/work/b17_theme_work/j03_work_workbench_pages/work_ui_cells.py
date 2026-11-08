"""The nine sNN of j03 · The work pages, level by level: one per level (Block, Job, Task) and section (Report, Work,
Studio), each drawn in haipipe-studio's five parts (scripts/five_parts.py). Copied from b16's paper_ui_cells.py and
b15's labeling_ui_cells.py (JL 261101: "plase read Theme_Paper and Theme_Labeling"; "use /haipipe-ui loop to check all
the UIs here and think about how to update them"). Each sNN's builder is `build(Path(__file__).parent)`: its cell is
found by its folder name (s51-block-ui-report → block, report).

A cell's Design is its page's views, lettered A, B, C …, each drawn as the same full screen (haipipe-ui 0.2.3, "one
view, one screen"): the window, both rails as pale short lines, the path, the title-&-section, the view-button-list
with this view in orange, the goal-line, the view-caption, then the view's sections as numbered heading bars, closed
(▸) as the live page starts them, what each opens to drawn under it as what it is (a map, side tabs, rows), and 🙋
Interaction the view's last section (261105). Each bar carries its state word on its right, and a bar that waits on the
person its waiting line under it (261106, ui_parts._section, focus_page.band_sec); each view's 🙋 holds its own forms
(focus_page.view_items) and the right rail ends Skills · Files (focus_page.render). A reviewed design no 261104 ask
overruled stays in red, a proposal; a changed screen carries its green ✎ notes, dated (NOTES).
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
RIGHT = ("Report", "Work", "Studio", "Interactions", "Delivery", "Related", "Timeline", "Skills", "Files")   # render's order (261106)
TAGS = "Slide · Draw · Mind map · Work · Delivery"               # the tags below an sNN (s51-D02)
FORM, ASK = "r04_collect_window_choice", "Which window leads the table?"
ASK_CL = "Cluster by state, or by physician?"          # j21's own form, about b11-s11 (r01_collect_clustering)
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


WAITS = re.compile(r"waits?( for| on) you|waiting for you|needs your|your sign|your call")   # ui_parts.waits_on_you


def state_color(word):
    w = word.lstrip("🙋✅⏳⬜ ")
    if word.startswith("🙋") or w.startswith("waits") or WAITS.search(w):
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
    """The map, as the live parts_mindmap draws it (261105): the root on the left, a branch per node (a Block's
    Questions, its topic groups, its bands of Jobs; a Job's Tasks; a Task's topics and Runs), its short name and one
    plain line; its children on the right: a Question's answer pill, a Task's goal ("finds out …") and topics, a Run's
    `says:` (261106: what each must find out, never the Run tree with its marks, which Status shows). Its nodes start
    closed: what one opens to is drawn on its right (Open all, Close all)."""
    rows = [branch_h(ch) for *_, ch in branches]
    tot = sum(r + 10 for r in rows) - 10
    ry = y + tot / 2 - 18
    els = [_el("rectangle", eid + "_r", x, ry, 120, 36, INK, "#ffffff", roundness={"type": 3})]
    els += text(eid + "_rt", x + 8, ry + 10, root, 11, INK)
    by = y
    for k, (pill, name, words, children) in enumerate(branches):
        bh = rows[k]
        cy = by + bh / 2
        els += line(f"{eid}{k}_l", [(x + 120, ry + 18), (x + 150, cy)], ROOM, 1)
        els += [_el("rectangle", f"{eid}{k}", x + 150, cy - 22, 230, 44, ROOM, "#ffffff", roundness={"type": 3})]
        nx = x + 160 + (6.2 * len(pill) + 8 if pill else 0)
        els += (text(f"{eid}{k}_p", x + 160, cy - 17, pill, 10, BODY) if pill else []) + text(f"{eid}{k}_n", nx, cy - 18, name, 12, TITLE)
        els += text(f"{eid}{k}_w", x + 160, cy + 3, words, 11, BODY) if words else []
        for j, cn in enumerate(children):
            chy = by + (bh - 30 * len(children)) / 2 + 30 * j + 2
            els += line(f"{eid}{k}_{j}_l", [(x + 380, cy), (x + 404, chy + 13)], ROOM, 1)
            els += [_el("rectangle", f"{eid}{k}_{j}", x + 404, chy, w - 404, 26, ROOM, "#ffffff", roundness={"type": 3})]
            els += text(f"{eid}{k}_{j}_n", x + 412, chy + 6, cn, 11, INK)
        by += bh + 10
    return els


def branch_h(children):
    """A branch's room: 30 a child, never less than its box (44), so a one-child branch does not overlap the next."""
    return max(46, 30 * len(children))


def tree_h(branches):
    return sum(branch_h(b[3]) + 10 for b in branches) - 10


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
    """Studio rows (JL 261029; live studio_html): picture, name, the one line it asks, its stage as one word, then its
    tags; a rolled-up topic says where it sits (haipipe-ui: `s22 · j02`); a topic whose form waits adds the flagged
    🙋 Interaction button, as live (261105)."""
    els = []
    for k, item in enumerate(items):
        label, words, stage, where, asks = (list(item) + ["", False])[:5]
        ry = y + 74 * k
        els += [_el("rectangle", f"{eid}{k}", x, ry, w, 66, ROOM, "#ffffff", roundness={"type": 3})]
        els += [_el("rectangle", f"{eid}{k}_p", x + 10, ry + 9, 76, 48, ROOM, GHOST)]
        els += text(f"{eid}{k}_a", x + 98, ry + 7, label, 11, TITLE) + text(f"{eid}{k}_w", x + 98, ry + 25, words, 12, INK)
        if where:
            els += text(f"{eid}{k}_at", x + 98 + 6.0 * len(label) + 8, ry + 7, f"· at {where}", 11, BODY)
        els += text(f"{eid}{k}_s", x + w - 70, ry + 25, stage, 11, state_color(stage))
        els += text(f"{eid}{k}_v", x + 98, ry + 45, TAGS, 10, BLUE)
        if asks:
            els += text(f"{eid}{k}_ix", x + 98 + 6.2 * len(TAGS) + 12, ry + 45, "· 🙋 Interaction", 10, OR)
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
        you = k == 1 and box[0].startswith(("🙋", "🧑"))     # 🧑 you work it; 🙋 is the Interaction's alone (261105)
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
            wait = c.startswith("🙋") or c.startswith("waits")
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


def _bar(eid, x, y, share, w=90):
    """A thin bar of how much is done, as live band_board draws one on a band's or a Job's row."""
    els = [_el("rectangle", eid, x, y, w, 6, "#e9ecef", "#e9ecef")]
    return els + ([_el("rectangle", eid + "_f", x, y, max(4, w * share), 6, GR if share >= 1 else BLUE,
                       GR if share >= 1 else "#74c0fc")] if share else [])


def k_fold(eid, x, y, w, items):
    """A folding tree as live fold_tree draws it: a line per Task (depth 1) or Run (depth 2), ▸ its name, its state word;
    on Work its output and its Interaction button (asked 261104: "each job each row, and we can collapse them out to
    see the tasks and runs")."""
    els = []
    for k, (depth, name, state, out, *verb) in enumerate(items):
        ky = y + 22 * k
        kx = x + 4 + 18 * (depth - 1)
        els += text(f"{eid}{k}_n", kx, ky, "▸ " + name, 11, TITLE if depth == 1 else INK)
        els += text(f"{eid}{k}_s", x + 214, ky, state, 11, state_color(state))
        if out:
            els += text(f"{eid}{k}_o", x + 316, ky, out, 11, BODY)
        if verb:
            els += _btns(f"{eid}{k}_b", x + w - 4, ky - 4, verb, OR if verb[0].startswith("🙋") else BLUE)
    return els


def k_jobrows(eid, x, y, w, rows):
    """A band's Jobs, one row each, closed (▸): its emoji, number and short name, its words left of its bar, the bar on
    the right edge (live band_board; asked 261104: "I prefer to me make it like the sections"); what a row opens to,
    its Tasks and Runs, drawn under it behind a dashed line; on Work a row adds its Interaction button."""
    els, yy = [], y
    for k, (name, said, share, kids, *verb) in enumerate(rows):
        els += [_el("rectangle", f"{eid}{k}", x, yy, w, 30, "#e9ecef", "#ffffff", roundness={"type": 3})]
        els += text(f"{eid}{k}_n", x + 10, yy + 8, "▸ " + name, 12, TITLE)
        right = x + w - 10
        if share is not None:
            els += _bar(f"{eid}{k}_bar", right - 80, yy + 12, share, 80)
            right -= 92
        if verb:
            els += _btns(f"{eid}{k}_v", right, yy + 3, verb, OR if verb[0].startswith("🙋") else BLUE)
            right -= sum(16 + 7.5 * len(v) + 8 for v in verb)
        els += text(f"{eid}{k}_s", right - 6.8 * len(said), yy + 9, said, 11, BODY)
        yy += 36
        if kids:
            els += line(f"{eid}{k}_in", [(x + 6, yy - 4), (x + 6, yy + 22 * len(kids) - 4)], PALE, 1, dashed=True)
            els += k_fold(f"{eid}{k}_k", x + 14, yy, w - 14, kids)
            yy += 22 * len(kids) + 6
    return els


def jobrows_h(rows):
    return sum(36 + (22 * len(r[3]) + 6 if r[3] else 0) for r in rows) - 6


def k_list(eid, x, y, w, items):
    """A Process step's rows, as live work_process lists them: a name, its small line."""
    els = []
    for k, (name, note) in enumerate(items):
        els += text(f"{eid}{k}_n", x + 4, y + 24 * k, name, 12, TITLE) + text(f"{eid}{k}_w", x + 240, y + 24 * k + 1, note, 11, BODY)
    return els


def k_note(eid, x, y, w, words):
    """A small plain line: a view's takeaways, a sub-heading, or what a band's view repeats."""
    return text(eid, x + 2, y, words, 11, BODY)


def k_verbs(eid, x, y, w, verbs):
    """Plain buttons on the left (the map's Open all, Close all)."""
    els, cx = [], x
    for k, v in enumerate(verbs):
        bw = 16 + 7.5 * len(v)
        els += [_el("rectangle", f"{eid}{k}", cx, y, bw, 22, ROOM, "#ffffff", roundness={"type": 3})]
        els += text(f"{eid}{k}_t", cx + 8, y + 4, v, 11, INK)
        cx += bw + 8
    return els


def _red(els):
    """A kept proposal's content: its edges red (261105: a reviewed design no 261104 ask overruled stays, red, open)."""
    for e in els:
        if e["type"] == "rectangle" and e["strokeColor"] in (ROOM, "#e9ecef", INK):
            e["strokeColor"] = RE
    return els


def k_red(eid, x, y, w, label, kind, *args):
    """A kept proposal with no heading bar (a lead card, Ask the agent): its name and "proposal" in red, then the thing,
    red-edged, behind a red dashed line."""
    h = KIND[kind][1](args)
    els = text(eid + "_l", x + 2, y, f"{label} · proposal", 12, RE)
    els += line(eid + "_in", [(x + 4, y + 20), (x + 4, y + 22 + h)], RE, 1, dashed=True)
    return els + _red(KIND[kind][0](eid + "_c", x + 14, y + 22, w - 14, *args))


def k_redline(eid, x, y, w, words):
    """A kept proposal that is only a heading (a Studio level group)."""
    return text(eid, x + 2, y, f"{words} · level group, proposal", 12, RE)


KIND = {"big": (k_big, lambda a: (56 if a[1] else 30) + 24 * a[0].count("\n")), "asks": (k_asks, lambda a: 48 * len(a[0]) - 8),
        "rows": (k_rows, lambda a: 60 * len(a[0]) - 8), "cardtabs": (k_cardtabs, lambda a: 74 + 24 * len(a[2])),
        "sidetabs": (k_sidetabs, lambda a: sidetabs_h(*a)), "tree": (k_tree, lambda a: tree_h(a[1])),
        "lead": (k_lead, lambda a: 104), "trows": (k_trows, lambda a: 74 * len(a[0]) - 8), "line": (k_line, lambda a: 20),
        "agent": (k_agent, lambda a: 70), "flow": (k_flow, lambda a: 84), "ask": (k_ask, lambda a: 36),
        "kv": (k_kv, lambda a: 24 * len(a[0])), "table": (k_table, lambda a: 24 * (len(a[1]) + 1) + 6),
        "checklist": (k_checklist, lambda a: 30 * len(a[0])), "picture": (k_picture, lambda a: 92),
        "grid": (k_grid, lambda a: grid_h(a[1])), "fork": (k_fork, lambda a: 72 * len(a[1]) - 10),
        "chain": (k_chain, lambda a: 62), "fold": (k_fold, lambda a: 22 * len(a[0]) - 4),
        "jobrows": (k_jobrows, lambda a: jobrows_h(a[0])), "list": (k_list, lambda a: 24 * len(a[0]) - 6),
        "note": (k_note, lambda a: 14 * (a[0].count("\n") + 1)), "verbs": (k_verbs, lambda a: 22),
        "red": (k_red, lambda a: 22 + KIND[a[1]][1](a[2:])), "redline": (k_redline, lambda a: 16)}


def S(title, word="", share=None, red=False, flag=False, wait=""):
    """A section's heading bar: closed (▸), as every section starts (asked 261104: "默认的话，大家都是合着的"); its state
    word and its thin bar on the right, as live (261106: "every closed bar shows a state word on its right"); red, a
    kept proposal, unnumbered (261105); flag, a 🙋 Interaction that waits for you (an orange edge, as live flags it);
    wait, the one thing that waits on the person, its line under the closed bar (261106: band_sec's band-wait)."""
    return {"t": title, "w": word, "s": share, "red": red, "flag": flag, "wait": wait}


WAIT_H = 22                          # a waiting line under a closed bar


def bar_of(head_):
    return head_ if isinstance(head_, dict) else S(head_ or "")


def sec_h(sec):
    if sec[0] == "rule":
        return 24
    if sec[0] in ("group", "next"):
        return 36 if sec[0] == "group" else 26
    b = bar_of(sec[0])
    has, wait = bool(b["t"]), WAIT_H if b.get("wait") else 0
    if sec[1] == "none":
        return 40 + wait
    return (40 if has else 0) + wait + KIND[sec[1]][1](sec[2:]) + (10 if sec[1] in ("flow",) and not has else 16)


def sec_draw(eid, x, y, w, sec):
    """A numbered heading bar (JL 261031: "each section to be the [heading bar] ... seems to be ordered"), closed (▸)
    as live starts every section (asked 261104); what it opens to drawn under it, behind a dashed line ("none": the
    bar alone, as on Work, whose Results repeat the Report's); a group heading (⚙️ Process, 📊 Results) and the next
    step's link, as b15 draws them."""
    if sec[0] == "rule":
        return line(eid, [(x, y + 8), (x + w, y + 8)], ROOM, 1, dashed=True)
    if sec[0] == "group":
        return text(eid, x, y + 6, sec[1], 16, INK) + line(eid + "_l", [(x + 130, y + 18), (x + w, y + 18)], "#dee2e6", 1)
    if sec[0] == "next":
        return text(eid, x + w - 8.5 * len(sec[1]) - 70, y + 4, f"next: {sec[1]} →", 13, BLUE)
    b = bar_of(sec[0])
    if not b["t"]:
        return KIND[sec[1]][0](eid + "_c", x, y, w, *sec[2:])
    stroke, fill, ink = (RE, "#fff5f5", RE) if b["red"] else (OR, "#fff4e6", TITLE) if b["flag"] else (ROOM, "#ffffff", TITLE)
    els = [_el("rectangle", eid, x, y, w, 30, stroke, fill, roundness={"type": 3})]
    els += text(eid + "_t", x + 12, y + 7, "▸ " + b["t"], 13, ink)
    right = x + w - 12
    if b["s"] is not None:
        els += _bar(eid + "_bar", right - 90, y + 12, b["s"])
        right -= 102
    word = "proposal" if b["red"] else b["w"]
    if word:
        els += text(eid + "_w", right - 6.8 * len(word), y + 8, word, 11, RE if b["red"] else state_color(word))
    if b.get("wait"):                                # under the closed bar, outside the fold (hidden once opened)
        els += text(eid + "_wait", x + 4, y + 35, b["wait"], 12, OR)
        y += WAIT_H
    if sec[1] == "none":
        return els
    h = KIND[sec[1]][1](sec[2:])
    els += line(eid + "_in", [(x + 6, y + 36), (x + 6, y + 40 + h)], RE if b["red"] else PALE, 1, dashed=True)
    inner = KIND[sec[1]][0](eid + "_c", x + 18, y + 40, w - 18, *sec[2:])
    return els + (_red(inner) if b["red"] else inner)


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
# Redrawn 261105 to follow the live work pages where the person asked for that change on 261104 (haipipe-ui 0.4.x;
# focus_page.render, work_views, work_process, band_board, findings_board, parts_mindmap): Work has the same views as
# Report, ⚙️ Process before 📊 Results; every section starts closed (▸), what it opens to drawn under its bar behind a
# dashed line; 🙋 Interaction is a view's last section, numbered after its band's, never a Process step. A reviewed
# design no 261104 ask overruled stays, red, unnumbered, marked "proposal" (S(..., red=True), "red", "redline"). The
# earlier screens (261101) stay in git and in each topic's review/.
# Redrawn 261106 as the live pages changed: every bar its state word, the waiting line under one that waits on you; each
# view's 🙋 its own forms; the skills left Process for the right rail's Skills (work_process: "who does it: the rail's
# Skills section, once per page, not a step in every view"), so a view with nothing to do has no ⚙️ Process; a Job's
# map draws each Task with its goal, a Task's map each Run with its `says:`.
G_PROC, G_RES = ("group", "⚙️ Process"), ("group", "📊 Results")
STEPS = ("Plan", "Build", "Run", "Read", "Close")   # a Task's life (haipipe-task ref/lifecycle.md)

# ── the forms, and which view's 🙋 holds each (focus_page.view_items, 261106). On a Block or a Job: Findings takes the
# forms at a Question's work, Status the forms below the page, MindMap the rest (the page's own, about its topics). On
# the Task's target: the step its answer changes (the window choice changes Read's headline), MindMap the rest.
# A form: (its title, its open form on the right, its waiting line, the bar's state word)
WINDOW = ("Window choice", (("Q1", ASK), ("A", "2016 to 2019, my pick"), ("B", "2016 to 2023"),
                            ("Q2", "Add the robust window?"), ("", "Note (optional)")),
          "🙋 Window choice: Q1 · Which window leads", "2 wait for you")
CLUSTER = ("Clustering", (("Q1", ASK_CL), ("A", "By state, my pick"), ("B", "By physician"), ("", "Note (optional)")),
           "🙋 Clustering: Q1 · By state or by physician", "1 waits for you")
RULES = ("Cohort rules", (("Q1", "Keep the cases with no year?"), ("A", "Yes, keep them: your pick"),
                          ("", "applied in b11-s01 · cohort_table")), "", "answered")
IX_OF = {   # (level, view): its 🙋's forms, each with its tab's word (where it was asked)
    ("block", "MindMap"): ((RULES, "✅ answered · b11"),),
    ("block", "Status"): ((CLUSTER, "🙋 waits · j21_ols_by_outcome"),),
    ("block", "Findings"): ((WINDOW, "🙋 waits · t01_outcome_a"),),
    ("job", "MindMap"): ((CLUSTER, "🙋 waits · j21_ols_by_outcome"),),
    ("job", "Status"): ((WINDOW, "🙋 waits · t01_outcome_a"),),
    ("task", "Read"): ((WINDOW, "🙋 waits on you"),),
}


def ix(level, view, n=0):
    """🙋 Interaction, the view's last section (decided 261105: it shows once, never a Process step), holding this view's
    own forms (261106: "a view's bottom section shows that view's own items, and the rail shows everything at this page
    and below"): its state word, its first waiting question under the closed bar (interaction_section.state_word), a
    side tab per form and the first one's form on the right; "nothing yet" when the view has none (view_section)."""
    title = (f"{n} · " if n else "") + "🙋 Interaction"
    rows = IX_OF.get((level, view), ())
    if not rows:
        return (S(title, "nothing yet"), "none")
    (_, form, wait, word), _ = rows[0]
    return (S(title, word, flag=bool(wait), wait=wait), "sidetabs", tuple((f[0], w) for f, w in rows), None, form,
            "Copy feedback" if wait else "")


def closing(secs, level, view):
    """The view's sections, then its 🙋 Interaction numbered after the last band's numbered sections, unnumbered when
    that band has none (live interaction_section.next_number); a step's next link after it."""
    last = max([i for i, s in enumerate(secs) if s[0] == "group"], default=-1)
    nums = [int(m.group(1)) for s in secs[last + 1:] if s[0] not in ("rule", "group", "next")
            for m in [re.match(r"(\d+) · ", bar_of(s[0])["t"])] if m]
    return (tuple(s for s in secs if s[0] != "next") + (ix(level, view, max(nums) + 1 if nums else 0),)
            + tuple(s for s in secs if s[0] == "next"))


def same(letter, view, extra=""):
    """Work's 📊 Results repeat the Report's view, drawn by the same code (asked 261104: "it should have the same view
    to the report"); its bars are drawn closed and empty here, the content is the Report's letter."""
    return ("", "note", f"the Report's {letter} · {view}, drawn by the same code" + (f";\n{extra}" if extra else ""))


def bars(secs):
    """A view's numbered sections as closed bars alone, each with its word and waiting line (its Results, drawn in the
    Report's cell)."""
    return tuple((s[0], "none") for s in secs if s[0] not in ("rule", "group", "next") and bar_of(s[0])["t"])


MAP_CAP = "How it is built, as a map: its parts, and what each must find out."
STATUS_CAP = "Where its Jobs, Tasks and sNN stand."
WAIT_B = "🙋 outcomes B and C: its answer waits for your agreement"   # findings_board's waiting line

# ── the Block (s51 Report, s52 Work, s53 Studio) ─────────────────────────────────────────────────────────────────────
BLOCK_MAP = (("", "verbs", ("Open all", "Close all")), ("", "tree", BLOCK, (
    ("", "Questions", "each with its answer's state", ("✅ outcome A and exposure", "🙋 outcomes B and C: your call",
                                                       "⬜ IV and OLS agree?")),
    ("", "Data", "its topics in the Data group", ("b11-s01 · cohort_table", "b11-s04 · codebook")),
    ("", "Display", "its topics in the Display group", ("b11-s02 · model_tables", "b11-s03 · iv_tables")),
    ("j0N", "📋 tables", "its Jobs, each opening to its Tasks", ("j01_cohort_table",)),
    ("j2N", "📈 models", "its Jobs, each opening to its Tasks", ("j21_ols_by_outcome", "j22_iv_by_outcome")))))
J21_KIDS = ((1, "t01_outcome_a", "⏳ running", ""), (2, "r01_years_16_19", "✅ done", ""), (2, "r02_years_16_23", "⏳ running", ""),
            (2, "r03_years_16_23_robust", "⬜ planned", ""), (1, "t02_outcome_b", "⏳ running", ""), (1, "t03_outcome_c", "⬜ planned", ""))
BLOCK_STATUS = (                       # live band_board: a closed section per band, a row per Job (s51-D10)
    (S("1 · 📋 tables", "done", 1.0), "jobrows", (("📋 j01 · cohort table", "done · 2 Tasks", 1.0, ()),)),
    (S("2 · 📈 models", "partly", 0.3), "jobrows", (("📈 j21 · ols by outcome", "partly · 3 Tasks · 40%", 0.4, J21_KIDS),
                                                   ("📈 j22 · iv by outcome", "not run · 1 Task", 0.0, ()))),
    ("", "note", "Studio  ▸ its topics: 3 explore · 2 shaping · 1 agreed"))
BLOCK_FINDINGS = (                     # live findings_board: closed numbered sections, side tabs (asked 261104)
    ("", "note", "Takeaways: outcome A rises with exposure in every window read so far."),
    (S("1 · 🔢 Values", "all current"), "sidetabs", (("outcome A by window", "j21 · tables.json"), ("cohort by year", "j01 · tables.json")),
     (("", "2016 to 2019", "2016 to 2023"), (("exposure", "x.xx", "x.xx"), ("n", "x,xxx", "x,xxx"))),
     (("", "Open j21_ols_by_outcome"),), ""),
    (S("2 · Outcomes", "waits for you", wait=WAIT_B), "sidetabs",
     (("outcome A and exposure", "answered"), ("outcomes B and C", "waits for you")), None,
     (("asks", "does outcome A rise with exposure?"), ("answer", "yes, in every window read so far"),
      ("t01", "r01: outcome A rises with exposure")), ""),
    (S("3 · Instruments", "no answer yet"), "sidetabs", (("IV and OLS agree?", "no answer yet"),), None,
     (("asks", "do the IV models agree with the OLS?"), ("answer", "none yet: j22 has not run")), ""),
    (S("4 · 🌐 Service", "live"), "sidetabs", (("cohort explorer", "a live page"),), None,
     (("", "the site itself, working, in a frame"), ("", "Own tab ↗")), ""),
    (S("5 · 🧠 Maps", "built 10-30"), "sidetabs", (("cohort_table", "its columns"), ("codebook", "its fields")), None,
     (("", "the map, its nodes closed · Enlarge map ↗"),), ""),
    (S("6 · 📦 Delivery", "ready"), "sidetabs", (("Models", "ready"), ("Data", "ready"), ("Website", "nothing yet")), None,
     (("model/", "ols_by_outcome.pkl · j21_ols_by_outcome"),), ""))
BLOCK_REPORT = (
    ("MindMap", MAP_CAP, closing(BLOCK_MAP, "block", "MindMap")),
    ("Status", STATUS_CAP, closing(BLOCK_STATUS, "block", "Status")),
    ("Findings", "What it has found so far, and what it hands over.", closing(BLOCK_FINDINGS, "block", "Findings")),
)
BLOCK_WORK = (                         # live work_views: Process (when it has a step), then the Report's view (asked 261104)
    ("MindMap", MAP_CAP, closing((G_RES, same("A", "MindMap")), "block", "MindMap")),
    ("Status", STATUS_CAP, closing((
        (S("📍 Where it stands", red=True), "big", "j21_ols_by_outcome waits on you:\nwhich window leads?",
         "done when every outcome has its OLS and IV table"),
        G_PROC,
        (S("1 · 🚧 Jobs not finished", "1 of 3 done"), "list", (("j21_ols_by_outcome", "partly · 3 Tasks · 40%"),
                                                                ("j22_iv_by_outcome", "not run · 1 Task"))),
        (S("⚙️ Its own Runs", red=True), "rows", (("✅ answered", "r01_collect_cohort_rules", "collect · Cohort rules", ("Open",), ""),)),
        G_RES, same("B", "Status", "Work adds each Task's output and its Interaction button"),
        (S("1 · 📋 tables", "done", 1.0), "none"),
        (S("2 · 📈 models", "partly", 0.3), "jobrows", (
            ("📈 j21 · ols by outcome", "partly · 40%", 0.4, ((1, "t01_outcome_a", "⏳ running", "r01: outcome A rises"),
                                                             (1, "t02_outcome_b", "⏳ running", "r01: running"),
                                                             (1, "t03_outcome_c", "⬜ planned", "")), "🙋 Interaction"),
            ("📈 j22 · iv by outcome", "not run", 0.0, ())))), "block", "Status")),
    ("Findings", "What it has found so far, and what it hands over.", closing((
        G_PROC, (S("1 · ✍️ Answers to write or agree", "1 waits for you", wait=WAIT_B), "list",
                 (("outcomes B and C", "proposed, waiting for you"), ("IV and OLS agree?", "no answer yet"))),
        G_RES, same("C", "Findings")) + bars(BLOCK_FINDINGS), "block", "Findings")),
)
BLOCK_STUDIO = (                       # live studio_html: flat rows; the lead card and level groups stay proposals (s53)
    ("Data", "The topics in the Data group, at the Block and below.", (
        ("", "red", "💡 Lead topic", "lead", S01, "keep the cases with no year?", "agreed", TAGS),
        ("", "redline", "🧩 At the Block"),
        ("", "trows", ((S01, "keep the cases with no year?", "agreed"), (S04, "one codebook, or one per year?", "explore"))))),
    ("Display", "The topics in the Display group, at the Block and below.", (
        ("", "red", "💡 Lead topic", "lead", S02, ASK, "🙋 waits on you", TAGS),
        ("", "redline", "🧩 At the Block"),
        ("", "trows", ((S02, ASK, "shaping", "", True), (S03, "which instrument?", "explore"))),
        ("", "redline", "🧩 At j21_ols_by_outcome"),
        ("", "trows", ((S11, "cluster by state, or by physician?", "shaping", "j21", True),
                       (S21, "add the age control?", "explore", "t01_outcome_a"))))),
)

# ── the Job (s54 Report, s55 Work, s56 Studio) ───────────────────────────────────────────────────────────────────────
JOB_MAP = (("", "verbs", ("Open all", "Close all")), ("", "tree", JOB, (   # each Task with its goal, no Runs (261106)
    ("", "b11-s11 · ols_model_design", "cluster by state, or by physician?", ()),
    ("t01", "outcome A's model", "in every window", ("finds out: does A rise with exposure", "b11-s21 · outcome_a_controls")),
    ("t02", "outcome B's model", "in every window", ("finds out: does B rise with exposure",)),
    ("t03", "outcome C's model", "in every window", ("finds out: does C rise with exposure",)))))
JOB_STATUS = (("", "note", "Tasks"), ("", "fold", J21_KIDS), ("", "note", "Studio  ▸ its topics: 1 shaping · 1 explore"))
JOB_GRID = (S("🧩 Tasks, step by step", red=True), "grid", STEPS,
            (("t01_outcome_a", ("✅ agreed", "✅ passed", "⏳ running", "waits on you", "⬜ not yet")),
             ("t02_outcome_b", ("✅ agreed", "✅ passed", "⏳ running", "⬜ not yet", "⬜ not yet")),
             ("t03_outcome_c", ("✅ agreed", "⬜ not yet", "⬜ not yet", "⬜ not yet", "⬜ not yet"))))
JOB_FINDINGS = (                       # live: its takeaways; the Display's table and figure stay proposals (s54)
    ("", "note", "Takeaways: outcome A rises with exposure; B and C are not read yet."),
    (S("📊 The table, by Task", red=True), "table", ("", "outcome A · t01", "outcome B · t02", "outcome C · t03"),
     (("exposure", "x.xx (v2)", "planned", "planned"), ("age", "x.xx (v2)", "planned", "planned"), ("n", "x,xxx", "", ""))),
    (S("📈 The figure", red=True), "picture", "each outcome's coefficient, side by side", ("Open",)))
FIND_CAP = "What it has found so far, in the answers' own words, and what waits for you."
JOB_REPORT = (
    ("MindMap", MAP_CAP, closing(JOB_MAP, "job", "MindMap")),
    ("Status", STATUS_CAP, closing(JOB_STATUS, "job", "Status")),
    ("Findings", FIND_CAP, closing(JOB_FINDINGS, "job", "Findings")),
)
JOB_WORK = (
    ("MindMap", MAP_CAP, closing((G_RES, same("A", "MindMap")), "job", "MindMap")),
    ("Status", STATUS_CAP, closing((
        G_PROC, (S("1 · 🚧 Tasks not finished", "0 of 3 done"), "list", (("t01_outcome_a", "running"), ("t02_outcome_b", "running"),
                                                                       ("t03_outcome_c", "planned"))),
        G_RES, same("B", "Status", "Work adds each Task's output and its Interaction button"),
        ("", "note", "Tasks"),
        ("", "fold", ((1, "t01_outcome_a", "⏳ running", "r01: outcome A rises", "🙋 Interaction"),
                      (1, "t02_outcome_b", "⏳ running", "r01: running"), (1, "t03_outcome_c", "⬜ planned", ""))),
        JOB_GRID), "job", "Status")),
    ("Findings", FIND_CAP, closing((G_RES, same("C", "Findings"))   # no Questions to answer: no ⚙️ Process
                                   + tuple((s[0], "none") for s in JOB_FINDINGS[1:]), "job", "Findings")),
)
JOB_STUDIO = (                         # live rows; "This Job makes" and the level groups stay proposals (s56)
    ("Display", "The topics in the Display group: what this Job makes, its own, then its Tasks'.", (
        ("", "red", "🎯 This Job makes", "lead", S02, ASK, "🙋 waits on you", TAGS),
        ("", "redline", "🧩 Its own"),
        ("", "trows", ((S11, "cluster by state, or by physician?", "shaping", "", True),)),
        ("", "redline", "🧩 Its Tasks'"),
        ("", "trows", ((S21, "add the age control?", "explore", "t01_outcome_a"),)))),
)

# ── the Task (s57 Report, s58 Work, s59 Studio): the target, built after the person's look (the live Task page is
# MindMap · Status today). Six views on both: A MindMap, then the five steps of a Task's life (haipipe-task
# ref/lifecycle.md: plan ▶ build ▶ run ▶ read ▶ close); Report shows each step's results, Work adds ⚙️ Process first
# (decided 261105). The step sections are the reviewed 261101 designs, drawn closed, each bar its word (261106) ─────
TASK_MAP = (("", "verbs", ("Open all", "Close all")), ("", "tree", TASK, (   # each Run with its says:, no marks (261106)
    ("", "b11-s21 · outcome_a_controls", "add the age control?", ()),
    ("", "Runs", "each with what it says", ("r01 · the model, 2016 to 2019", "r02 · the model, 2016 to 2023",
                                            "r03 · 2016 to 2023, robust errors", "r04 · Window choice",
                                            "r05 · the Table Card", "r06 · the coefficient plot")))))
TASK_RESULTS = {                       # each step's 📊 Results: the Report's view, and Work's after its Process
    "Plan": ("What it set out to make, who makes it, where it lands.", (
        (S("1 · 🎯 Done when", "agreed"), "big", "Every window's model has its table, and it is read.", "✅ agreed, 10-26"),
        (S("2 · 🔗 What it makes", "1 of 3 made"), "flow", ("cohort_table", "v3, made by j01_cohort_table", ""),
         ("🤖 scripts/fit_ols.py", "r01 to r03, one Run a window", ""), ("Three window models", "r01 v2 · r02, r03 planned", "")),
        (S("3 · 📦 Where it lands", "v2 landed"), "kv", (("b11-s02", "model_tables: outcome A's table, v2"),)))),
    "Build": ("The code its Runs run, and its review: the thing to read.", (   # the thing, not its steps (s57 C r05)
        (S("1 · 🔎 Code review", "pass"), "big", "scripts/fit_ols.py passed review against the Task's goal.", "✅ pass, 10-26"),
        ("", "rows", (("✅ pass", "CODE_REVIEW.md", "checked against the Task's goal · open issues: none", ("Open",), ""),)),
        (S("2 · 📄 The code", "reviewed"), "sidetabs", (("scripts/fit_ols.py", "the worker"), ("config.yaml", "r01_years_16_19"),
                                                       ("r01_years_16_19.sh", "the ticket")),
         None, (("1", "def fit(window):"), ("2", "    rows = read_table(cohort_table, years=window)"),
                ("3", "    model = ols(outcome_a ~ exposure + age + year)"), ("4", "    write_table(model, result/tables/)"),
                ("", "Open the file")), ""))),
    "Run": ("Each Run with its status and what it made; a Run opens in its pop-out.", (   # new 261105
        (S("1 · 🧾 Its Runs", "1 of 5 done"), "rows", (
            ("✅ done", "r01_years_16_19", "made tables/coef.csv and figures/coef.png", ("Open",), "coef.png"),
            ("⏳ running", "r02_years_16_23", "started 10-31 08:05 · nothing made yet", ("Open",), ""),
            ("⬜ planned", "r03_years_16_23_robust", "built, not run yet", ("Open",), ""),
            ("⬜ planned", "r05_describe_table", "the Table Card, once r01 to r03 are done", ("Open",), ""),
            ("⬜ planned", "r06_figures_coef", "the coefficient plot", ("Open",), ""))),
        (S("2 · 🔁 Passes", "1 failed, kept"), "line", "r02 failed once on 10-29; that pass stays in passes/p01-1029"))),
    "Read": ("What it found: the headline, the table, the figure.", (
        (S("1 · 📌 Headline", "draft"), "big", "Outcome A is higher where exposure is higher.", "draft until r04 is answered · r01_years_16_19"),
        ("", "ask", "✍️ your read: mark r01 read once you have read it", "Mark read", "gate"),
        (S("2 · 📊 Table Card · r05_describe_table", "planned"), "table", ("", "estimate", "95% CI", "n"),
         (("exposure", "x.xx", "x.xx to x.xx", "x,xxx"), ("age", "x.xx", "x.xx to x.xx", ""), ("year", "x.xx", "x.xx to x.xx", ""))),
        (S("3 · 📈 Coefficient plot · r06_figures_coef", "planned"), "picture", "the coefficients, window by window", ("Open",)))),
    "Close": ("Where the close stands, read only: what it still needs.", (   # new on Report 261105, read only
        (S("1 · 🚧 Where the close stands", "not yet"), "big", "Not closed yet: Runs to finish,\nyour answer and your read.", "⬜ not yet"),
        (S("2 · 📋 What the close needs", "1 waits for you", wait="🙋 which window leads: waits on your answer"), "checklist", (
            ("which window leads", "waits on your answer"), ("r01_years_16_19 read by you", "⬜ not yet"),
            ("r02_years_16_23 done", "⏳ running"), ("r03_years_16_23_robust done", "⬜ planned"),
            ("r05_describe_table, r06_figures_coef", "⬜ planned"),
            ("each Result gate passed", "✅ yes, r01"), ("each receipt current", "✅ yes"))),
        (S("3 · 🎯 What it ticks", "not yet"), "kv", (("j21_ols_by_outcome", "⬜ not yet: outcome A's table in b11-s02 · model_tables"),)))),
}
TASK_PROCESS = {                       # each step's ⚙️ Process (b15's shape: In → who works → Out, your part); the
    "MindMap": (),                     # map has none since its skills went to the rail (261106)
    "Plan": ((S("1 · 🧭 Plan the Runs", "agreed"), "flow", ("j21's Deliverables item", "outcome A's table in b11-s02", "goal: and close:"),
              ("🤖 Agent", "run-plan-t01", "one Run per window"), ("Planned Run cards", "status: planned", "r01 to r03, r05, r06")),
             ("", "ask", "✅ you agreed the plan on 10-26", "", "done")),
    "Build": ((S("1 · 🔧 Build the code", "passed"), "flow", ("Planned Run cards", "r01 to r03", ""),
               ("🤖 The fit skill's creator", "run-build-t01", ""), ("Worker · config · ticket", "scripts/fit_ols.py", "one config, one ticket a Run")),
              ("", "ask", "✅ the reviewer passed the code before any Run (Gate 1)", "Open review", "done")),
    "Run": ((S("1 · 🏃 Run the tickets", "running"), "flow", ("Ticket + config", "r03_years_16_23_robust.sh", ""),
             ("🧑 You press Run", "a long Run waits for you", "AGENTS rule 2"), ("The receipt", "result/runtime.yaml", "running ▶ complete")),
            ("", "ask", "r03_years_16_23_robust is built: press Run on the server", "Copy command", "gate")),
    "Read": ((S("1 · 📖 Read the results", "draft"), "flow", ("result/ files", "r01: tables/, metrics.json", ""),
              ("🤖 Describe and figures Runs", "r05_describe_table", "r06_figures_coef"), ("Headline · Table Card · figure", "", "")),),
    "Close": ((S("1 · 🏁 Check the close", "not yet"), "flow", ("Every receipt", "and the close: line", ""), ("🤖 Agent", "run-check-t01", ""),
               ("close: not yet", "then the Job's item ticks", "")),),
}
WORK_CAP = {"Plan": "Plan: the Job's item, the goal and close, a card per Run.",
            "Build": "Build: the worker, each Run's config and ticket, then the review.",
            "Run": "Run: each ticket pressed, its receipt from running to complete.",
            "Read": "Read: the headline, its table and figure; your answer waits in 🙋 Interaction.",
            "Close": "Close: every receipt against the close line; then the Job's item ticks."}
TASK_VIEWS = ("MindMap",) + STEPS


def task_report(k, view):
    if view == "MindMap":
        return view, MAP_CAP, closing(TASK_MAP, "task", view)
    cap, res = TASK_RESULTS[view]
    return view, cap, closing(res, "task", view)


def task_work(k, view):
    res = () if view == "MindMap" else TASK_RESULTS[view][1]
    nxt = (("next", f"{LETTERS[k + 1]} · {TASK_VIEWS[k + 1]}"),) if k + 1 < len(TASK_VIEWS) else ()
    proc = ((G_PROC,) + TASK_PROCESS[view]) if TASK_PROCESS[view] else ()   # nothing to do: no ⚙️ Process (work_views)
    secs = proc + (G_RES, same(LETTERS[k], view)) + bars(res) + nxt
    return view, WORK_CAP.get(view, MAP_CAP), closing(secs, "task", view)


TASK_REPORT = tuple(task_report(k, v) for k, v in enumerate(TASK_VIEWS))
TASK_WORK = tuple(task_work(k, v) for k, v in enumerate(TASK_VIEWS))
TASK_STUDIO = (                        # live rows; "This Task makes" and Ask the agent stay proposals (s59)
    ("Display", "The topics in the Display group: what this Task makes, then its own.", (
        ("", "red", "🎯 This Task makes", "lead", S02, "its piece: outcome A's table, v2", "🙋 waits on you", TAGS),
        ("", "trows", ((S21, "add the age control?", "explore"),)),
        ("", "red", "✍️ Ask the agent", "agent", ("Copy prompt: talk and sketch", "Copy prompt: start a topic")))),
)
CLOSED = ("every section starts closed (▸), its state word on its right, a waiting line under one that waits on you; "
          "what it opens to is drawn under its bar, behind a dashed line")
OWN = "each view's 🙋 Interaction holds its own forms; the right rail ends Skills · Files, as live (261106)"
RAIL_ONLY = "the right rail ends Skills · Files, as live (261106)"
VIEWS = {   # (level, section): (the line above the screens, the views, the open question)
    ("block", "report"): ("MindMap · Status · Findings, as the live page draws them (asked 261104); " + CLOSED + ";\n" + OWN,
                          BLOCK_REPORT, "? agree A to C: they\nfollow the live page"),
    ("block", "work"): ("the same views as Report (asked 261104): ⚙️ Process when it has a step, then 📊 Results by the same code;\n"
                        "red: a reviewed design no ask overruled, kept as a proposal; " + CLOSED + ";\n" + OWN,
                        BLOCK_WORK, "? keep 📍 Where it stands\nand its own Runs (red)"),
    ("block", "studio"): ("one view per group of the Block's _studio_groups.txt, flat rows as live;\n"
                          "red: the lead card and the level groups, kept as proposals; " + RAIL_ONLY,
                          BLOCK_STUDIO, "? the lead topic large,\nand level groups (red)"),
    ("job", "report"): ("MindMap · Status · Findings (when it has questions or takeaways), as live;\n"
                        "red: one table across the Tasks and the figure, kept as proposals; " + CLOSED + ";\n" + OWN, JOB_REPORT,
                        "? one table across\nthe Tasks (red)"),
    ("job", "work"): ("the same views as Report (asked 261104): ⚙️ Process when it has a step, then 📊 Results by the same code;\n"
                      "red: the Tasks × steps grid, kept as a proposal; " + CLOSED + ";\n" + OWN, JOB_WORK,
                      "? the Tasks × steps\ngrid (red)"),
    ("job", "studio"): ("the groups of the topics it shows, flat rows as live;\nred: This Job makes and the level groups, "
                        "kept as proposals; " + RAIL_ONLY, JOB_STUDIO, "? show the Block topic\nit makes first (red)"),
    ("task", "report"): ("the target, built after your look (the live Task page is MindMap · Status today):\n"
                         "the MindMap, then each step's results, read only: Plan, Build, Run, Read, Close; " + CLOSED + ";\n"
                         + OWN + "; a form shows in the step its answer changes",
                         TASK_REPORT, "? build the six views\nas drawn"),
    ("task", "work"): ("the target, built after your look (the live Task page is MindMap · Status today): the same six\n"
                       "views, ⚙️ Process before 📊 Results; P, a Run's pop-out, opens from any Run row; " + CLOSED + ";\n"
                       + OWN + "; a form shows in the step its answer changes",
                       TASK_WORK, "? step buttons carry\ntheir state words"),
    ("task", "studio"): ("the groups of the topics it shows, flat rows as live;\nred: This Task makes and Ask the agent, kept as proposals; "
                         + RAIL_ONLY, TASK_STUDIO, "? This Task makes and\nAsk the agent (red)"),
}
# what changed on each letter's screen: its green ✎ notes under its letter, dated, and listed under the screens
# (canvas.change_note); the 261105 redraw's notes stay beside the 261106 ones
D5, D6 = "261105", "261106"
NOTES = {
    ("block", "report"): {"A": [(D5, "map as live: answer pills, Jobs under bands"), (D5, "🙋 Interaction its last section, closed"),
                                (D6, "rail: Skills · 🙋 holds the Block's own form"), (D6, "outcomes B and C: 🙋 your call")],
                          "B": [(D5, "new: Status, a closed section per band, as live"), (D5, "was B · Data: folded into C's 📦 Delivery"),
                                (D6, "rail: Skills · 🙋 holds the forms below: Clustering")],
                          "C": [(D5, "new: Findings as live: closed side-tab sections"), (D5, "was C · Display: folded into its 📦 Delivery"),
                                (D6, "rail: Skills · each bar its state word"), (D6, "Outcomes waits for you: its question under it"),
                                (D6, "🙋 holds the Questions' forms: Window choice")]},
    ("block", "work"): {"A": [(D5, "new: ⚙️ Process, then the Report's MindMap"),
                              (D6, "rail: Skills; Process left with its skills step"), (D6, "🙋 holds the Block's own form")],
                        "B": [(D5, "Status replaces A · Progress (asked 261104)"), (D5, "red: Where it stands, its own Runs, kept"),
                              (D6, "rail: Skills; Process: no skills step"), (D6, "each bar its word; 🙋 holds the forms below")],
                        "C": [(D5, "new: ⚙️ Process, then the Report's Findings"),
                              (D6, "rail: Skills; Process: no skills step"), (D6, "Answers: 1 waits for you, its question under it"),
                              (D6, "🙋 holds the Questions' forms")]},
    ("block", "studio"): {"A": [(D5, "rows as live"), (D5, "red: the lead card and level groups, kept"), (D6, "right rail: Skills, as live")],
                          "B": [(D5, "rows as live, 🙋 on the waiting row"), (D5, "red: the lead card and level groups, kept"),
                                (D6, "right rail: Skills · s11's row: 🙋, its form waits")]},
    ("job", "report"): {"A": [(D5, "map as live: its Tasks, their Runs marked"),
                              (D6, "map: each Task with what it finds out, no Runs"), (D6, "rail: Skills · 🙋 holds the Job's own form")],
                        "B": [(D5, "new: Status, its Tasks opening to their Runs"),
                              (D6, "Runs read ✅ done · ⏳ running · ⬜ planned"), (D6, "rail: Skills · 🙋 holds the forms below")],
                        "C": [(D5, "was B · Display: Findings, its takeaways, as live"), (D5, "red: the table by Task and the figure, kept"),
                              (D6, "rail: Skills · 🙋 nothing yet: no Questions")]},
    ("job", "work"): {"A": [(D5, "new: ⚙️ Process, then the Report's MindMap"),
                            (D6, "rail: Skills; Process left with its skills step"), (D6, "🙋 holds the Job's own form")],
                      "B": [(D5, "Status replaces A · Progress (asked 261104)"), (D5, "red: the Tasks × steps grid, kept"),
                            (D6, "rail: Skills; Process: no skills step"), (D6, "each bar its word; 🙋 holds the forms below")],
                      "C": [(D5, "new: ⚙️ Process, then the Report's Findings"),
                            (D6, "rail: Skills; no Process: no Questions to answer"), (D6, "🙋 nothing yet")]},
    ("job", "studio"): {"A": [(D5, "rows as live"), (D5, "red: This Job makes and level groups, kept"),
                              (D6, "right rail: Skills · s11's row: 🙋, its form waits")]},
    ("task", "report"): {"A": [(D5, "map as live: its topic, its Runs marked"),
                               (D6, "map: each Run with what it says, no marks"), (D6, "rail: Skills · 🙋 nothing yet here")],
                         "B": [(D5, "drawn closed; 🙋 Interaction its last section"), (D6, "rail: Skills · each bar its state word")],
                         "C": [(D5, "drawn closed; 🙋 Interaction its last section"), (D6, "rail: Skills · each bar its state word")],
                         "D": [(D5, "new: each Run, its status and output;"), (D5, "Open pops the Run out (P on s58)"),
                               (D6, "rail: Skills · each bar its state word"), (D6, "Runs read ✅ done · ⏳ running · ⬜ planned")],
                         "E": [(D5, "was D · Read; drawn closed"), (D5, "🙋 Interaction its last section"),
                               (D6, "rail: Skills · each bar its state word"), (D6, "🙋 holds Window choice: its answer is Read's")],
                         "F": [(D5, "new: the close checklist's state, read only"), (D6, "rail: Skills · each bar its state word"),
                               (D6, "close needs: 1 waits for you, under its bar")]},
    ("task", "work"): {"A": [(D5, "new: ⚙️ Process, then the Report's MindMap"),
                             (D6, "rail: Skills; Process left with its skills step"), (D6, "🙋 nothing yet here")],
                       "B": [(D5, "was A · Plan; 📊 Results = the Report's B"), (D6, "rail: Skills · each bar its state word")],
                       "C": [(D5, "was B · Build; 📊 Results = the Report's C"), (D6, "rail: Skills · each bar its state word")],
                       "D": [(D5, "was C · Run; 📊 Results = the Report's D"), (D5, "press Run: a plain row, not 🙋"),
                             (D6, "rail: Skills · each bar its state word")],
                       "E": [(D5, "was D · Read; its 🙋 ask moved into"), (D5, "🙋 Interaction, the view's last section"),
                             (D6, "rail: Skills · each bar its state word"), (D6, "🙋 holds Window choice: its answer is Read's")],
                       "F": [(D5, "was E · Close; 📊 Results = the Report's F"), (D6, "rail: Skills · each bar its state word"),
                             (D6, "close needs: 1 waits for you, under its bar")],
                       "P": [(D6, "each bar its state word")]},
    ("task", "studio"): {"A": [(D5, "rows as live; the 🙋 helper left (Studio has none)"), (D5, "red: This Task makes, Ask the agent, kept"),
                               (D6, "right rail: Skills, as live")]},
}
PIECE = {
    ("block", "report"): ("the Block's Report: its map, its Status, its Findings",
                          ["the Report showed Status,\nFindings and Questions", "a delivery opened only\nfrom a Studio row",
                           "no view showed what\nthe Block hands over"]),
    ("block", "work"): ("the Block's Work: Process, then the Report's views",
                        ["where things stand sat\nin the Report", "a waiting form hid in\na Job's row",
                         "a Job row did not say\nwhat it makes"]),
    ("block", "studio"): ("the Block's Studio: its topics by group",
                          ["topics sat in studio/,\nout of sight", "a card's tags did not\nsay what they open",
                           "nothing said which\ntopic waits on you"]),
    ("job", "report"): ("a Job's Report: its map, its Status, its Findings",
                        ["a Job page repeated\nthe Block's views", "its delivery sat in\nthe Block's topic",
                         "no view said what\nthe Job hands over"]),
    ("job", "work"): ("a Job's Work: Process, then the Report's views",
                      ["Tasks sat as plain rows", "the order was the\nfolders', not the plan's",
                       "a Run hid two\nclicks deep"]),
    ("job", "studio"): ("a Job's Studio: the topics it makes and holds",
                        ["a Job showed only\nits own topics", "the topic it makes\nsat at the Block",
                         "nothing linked the two"]),
    ("task", "report"): ("a Task's Report: its map, then each step's results",
                         ["a Task's Report listed\nreceipts, not results", "the newest result was\nclicks away",
                          "a check's verdict\nhad no place"]),
    ("task", "work"): ("a Task's Work: its map, then each step, Process first",
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


NOTE_H = 20                          # one green note's line under a letter


def notes_top(notes, letters):
    """Where the screens start under their letters: the letter, then the most notes any of them carries."""
    return 40 + NOTE_H * max([len(notes.get(L, ())) for L in letters] + [0])


def letter_notes(eid, x, y, notes):
    """A letter's green ✎ notes, one a line under it, each with its own date (canvas.change_note)."""
    return [change_note(x + 4, y + 34 + NOTE_H * j, what, date, None, 14) for j, (date, what) in enumerate(notes)]


def screens(eid, x, y, items, level, section, notes=None, gap=40, top=None):
    """Every view lettered A, B, C …, every screen the same size (the tallest view's), three a row (JL 261031); a
    letter whose screen changed carries its green ✎ notes under its name, dated (as the paper's cells)."""
    notes = notes or {}
    cols, h = min(3, len(items)), screen_h(items)
    views = tuple(v for v, _, _ in items)
    top = top or notes_top(notes, LETTERS[:len(items)])
    els = []
    for k, (view, caption, secs) in enumerate(items):
        sx, sy = x + (k % cols) * (W + gap), y + (k // cols) * (h + top + gap)
        els += text(f"{eid}{k}_L", sx, sy, f"{LETTERS[k]} · {view}", 22, TITLE)
        els += letter_notes(f"{eid}{k}_n", sx, sy, notes.get(LETTERS[k], ()))
        els += screen(f"{eid}{k}", sx, sy + top, h, level, section, views, k, secs, caption)
    return els, y + ((len(items) + cols - 1) // cols) * (h + top + gap)


def flat(sec):
    """(title, one line) of a section, for the agreed screen file."""
    if sec[0] in ("rule", "group", "next"):
        return (sec[1], "") if sec[0] == "group" else ("", "")
    if sec[1] in ("none", "red", "redline"):
        return bar_of(sec[0])["t"] or (sec[2] if sec[1] != "none" else ""), "proposal" if sec[1] != "none" else ""
    words = {"tree": lambda: " · ".join(b[1] for b in sec[3]), "sidetabs": lambda: " · ".join(h for h, _ in sec[2]),
             "cardtabs": lambda: " · ".join(t for t, _ in sec[2]), "asks": lambda: " · ".join(w for w, _ in sec[2]),
             "rows": lambda: " · ".join(r[1] for r in sec[2]), "trows": lambda: " · ".join(r[0] for r in sec[2]),
             "jobrows": lambda: " · ".join(r[0] for r in sec[2]), "fold": lambda: " · ".join(r[1] for r in sec[2]),
             "list": lambda: " · ".join(n for n, _ in sec[2]), "verbs": lambda: " · ".join(sec[2]),
             "lead": lambda: f"{sec[2]} · {sec[3]}", "agent": lambda: " · ".join(sec[2])}.get(sec[1], lambda: str(sec[2]))()
    return bar_of(sec[0])["t"], words


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

    notes = NOTES.get((level, section), {})
    pop = (level, section) == ("task", "work")           # a Run's pop-out beside the six steps (JL 261103)

    def design():                                    # A, B, C … every view the same screen; no separate main sketch
        els = text("skA", 690, 280, f"A to {last} · {piece}, every view the same screen", 18, TITLE)
        els += text("lay", 690, 330, lay, 16, BODY)
        top = 356 + 20 * (lay.count("\n") + 1)
        ntop = notes_top(notes, LETTERS[:len(names)] + ("P" if pop else ""))
        e, bottom = screens("sc", 690, top, items, level, section, notes, top=ntop)
        if pop:                                          # P to the right of A to C, opened from any Run row (D's)
            sx = 690 + 3 * (W + 40)
            els += text("popL", sx, top, "P · a Run's pop-out", 22, TITLE) + letter_notes("popN", sx, top, notes.get("P", ()))
            pe, _ = popout("pop", sx, top + ntop)
            els += pe
        # the title-frame list: every changed screen's notes, in one place under the screens (green, each its date)
        listed = [(L, d, w) for L in LETTERS + "P" for d, w in notes.get(L, ())]
        els += text("chgH", 690, bottom + 10, "What changed", 16, TITLE) if listed else []
        for j, (L, d, w) in enumerate(listed):
            els += [change_note(690, bottom + 40 + 22 * j, f"{L}: {w}", d, None, 14)]
        return els + e + sticky("askD", 1480, bottom + 60, 320, 76, ask, 15, -0.03, RED, RE)

    return five_parts.build(topic, spec, design, shift=(W + 40) * (min(3, len(items)) + pop) - 300 + 160 * pop,
                            writer=five_parts.marks_writer)   # the person's canvas marks stay (261105)


# ── a Run's pop-out (JL 261103: "when I click a run, it will show all the information from that run folder with a pop
# out window, so we can quickly understand what happened"): everything in runs/<run>/, read in place, over the page ───
RUN_POP = (
    (S("1 · 📌 What happened", "done"), "big", "Outcome A is higher where exposure is higher.", "✅ done · 10-27, 09:12 to 11:40 · pass p01"),
    (S("2 · 📊 What it made · result/", "4 files"), "sidetabs", (("RUN-REPORT.md", "the report"), ("tables/coef.csv", "the table"),
                                                  ("figures/coef.png", "the figure"), ("metrics.json", "the numbers")),
     None, (("", "# r01_years_16_19 · the model, 2016 to 2019"), ("", "Headline: outcome A is higher where exposure is higher."),
            ("", "Rows: x,xxx cases · years 2016 to 2019"), ("", "Table: tables/coef.csv · Figure: figures/coef.png"),
            ("", "Open the file")), ""),
    (S("3 · 🎫 How it ran · run.yaml, ticket, config", "receipt current"), "kv", (("what it does", "makes the model, one window"),
                                                          ("reads", "cohort_table v3, 2016 to 2019"),
                                                          ("who", "you pressed Run · fit skill"),
                                                          ("ticket", "r01_years_16_19.sh  ·  Copy command"),
                                                          ("config", "config.yaml: window 2016 to 2019, the OLS model"),
                                                          ("receipt", "result/runtime.yaml"))),
    (S("4 · 🔁 Passes · passes/", "1 pass, done"), "rows", (("✅ done", "p01-1027", "10-27 09:12 · log: wrote result/, gate passed, 11:40 done",
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


def letter_png(topic: Path, letter: str, out: Path, scale: float = 1.0, drawing: Path = None) -> Path:
    """One letter's screen alone, for a Design loop review (haipipe-ui, stage 1) or a look Run's option picture:
    <out>.png, drawn from <out>.excalidraw (or `drawing`, so a Run folder keeps only its picture)."""
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
    drawing = Path(drawing) if drawing else out.with_suffix(".excalidraw")
    drawing.parent.mkdir(parents=True, exist_ok=True)
    five_parts.write(drawing, els)
    render = TOOLS / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts/render_png.py"
    subprocess.run(["uv", "run", "--no-project", "-q", "--with", "pillow", "python", str(render), str(drawing),
                    str(out.with_suffix(".png")), str(scale)], check=True, stdout=subprocess.DEVNULL)
    return out.with_suffix(".png")


if __name__ == "__main__":                               # python work_ui_cells.py <topic folder> <letter> <out>
    print(letter_png(Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])))
