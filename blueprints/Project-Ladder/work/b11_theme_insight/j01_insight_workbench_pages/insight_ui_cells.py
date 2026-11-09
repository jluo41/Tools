"""The nine sNN of b11 j01 · The insight pages, level by level: one per level (Board, Job, Task) and section (Report,
Work, Studio), each drawn in haipipe-studio's five parts (scripts/five_parts.py). Each sNN's builder is
`build(Path(__file__).parent)`: its cell is found by its folder name (s51-block-ui-report → block, report).

A cell's Design is its page's views, lettered A, B, C …, each drawn as the same full screen (haipipe-ui, "one view,
one screen"): the window, both rails as pale short lines, the path, the title-&-section, the view-button-list with this
view in orange, the goal-line (a Task's Aim; a Board and a Job have none), the view-caption, then the view's sections as
numbered heading bars, closed (▸) as the live page starts them, each with its state word on its right and, when it
waits on the person, its waiting line under the bar; what a bar opens to is drawn under it as what it is (side tabs, a
dot row per DIKW level, a grid of dots, a map). 🙋 Interaction is the last section of every Report and Work view and
holds that view's own forms; Work has the same views as Report, ⚙️ Process first, then 📊 Results drawn by the same
code. No view starts with a "Waits on you" section. Studio exists at every level; a page with no topic says so and
offers Add a topic. The right rail ends Skills · Files.

Redrawn 261106 to the live, aligned insight pages (servers/workbench-insight; asked 261106: "use your picks" on the
Board, Job and Task Report walks, and Studio at every level): Board Answers · Questions · Jobs · Data · Handoff ·
MindMap; Job Overall · Grid · vs previous · MindMap (vs previous hidden on a first Job); Task Answer · By cut · Across
Jobs · Plan · MindMap. A changed screen carries its dated green ✎ notes under its letter, listed again under the
screens (NOTES). A reviewed design no later ask overruled stays, red, marked "proposal" (S(..., red=True), "red",
"redline"). The drawing is written by five_parts.marks_writer, so a person's marks on the canvas stay.

The example is the theme's own public example, Insight-Example (made-up rows, arm A and arm B, three groups): a Board is
one dataset and its data freezes; a Job is one analysis plan on one data freeze; a Task is one question (X, D, I, K or
W level); a hard Run is one cut. Tools is public, so nothing from a private Board is drawn.

    python insight_ui_cells.py <topic folder> <letter> <out>     one letter's screen alone, for a review round
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
from quick_draw import box  # noqa: E402
import five_parts  # noqa: E402

VERB = {"report": "Report", "work": "Work", "studio": "Studio"}
LETTERS = "ABCDEFGH"
W, CW, X0 = 780, 640, 70             # a screen, its content column, where the column starts (the rails are short lines)
BLUE = "#1864ab"                     # the workbench's colour for the current thing
PALE = "#dee2e6"

# ── the example: the theme's public Insight-Example, as the live pages show it ──────────────────────────────────────
SPACE = "<SPACE> / Tools / blueprints / Project-Ladder / insight"
BOARD, JOB, TASK = "Insight-Example", "j02_code-v1-example-questions_data-v2", "t03_I01_outcome-by-arm"
PAGE = {"block": (BOARD, f"{SPACE} / {BOARD}", ""),
        "job": (JOB, f"{SPACE} / {BOARD} / {JOB}", ""),
        "task": (TASK, f"{SPACE} / {BOARD} / {JOB} / {TASK}", "Aim  ·  I01")}       # only a Task has a goal-line
LEFT = {"block": (0, 4, 1), "job": (2, 12, 3), "task": (3, 9, 99)}   # this page's line, how many, the first child line
RIGHT = ("Report", "Work", "Studio", "Interactions", "Delivery", "Timeline", "Skills", "Files")   # as served 261106
J1, J2 = "j01_code-v1-example-questions_data-v1", JOB


# ── the screen's parts, one name each (haipipe-ui: path, title-&-section, view-button-list, goal-line, view-caption,
# content, left-rail, right-rail) ─────────────────────────────────────────────────────────────────────────────────
def window(eid, x, y, w, h, url):
    els = [_el("rectangle", eid, x, y, w, h, INK, "#ffffff", roundness={"type": 3})]
    els += line(eid + "_bar", [(x, y + 28), (x + w, y + 28)], ROOM, 1)
    return els + [_el("ellipse", f"{eid}_d{k}", x + 10 + k * 14, y + 9, 9, 9, ROOM, ROOM) for k in range(3)] + \
        text(eid + "_url", x + 60, y + 7, url, 12, BODY)


def rails(eid, x, y, level, section):
    """Both rails hide until hovered: pale short lines, no words; the open page or section darker."""
    here, n, child = LEFT[level]
    els = []
    for k in range(n):
        els += line(f"{eid}_l{k}", [(x + 16 + (6 if k >= child else 0), y + 50 + 12 * k), (x + 40, y + 50 + 12 * k)],
                    INK if k == here else PALE, 2)
    for k, s in enumerate(RIGHT):
        els += line(f"{eid}_r{k}", [(x + W - 40, y + 50 + 12 * k), (x + W - 16, y + 50 + 12 * k)],
                    OR if s == VERB[section] else PALE, 2)
    return els


def head(eid, x, y, name, section, views, on=0):
    """The title-&-section (a long folder name a size smaller), then the view-button-list, the open view in orange."""
    size = 20 if len(name) <= 30 else 15
    els = text(eid + "_t", x, y, name, size, INK) + text(eid + "_s", x + 0.62 * size * len(name) + 14, y + 4, VERB[section], 15, BODY)
    cx = x
    for k, v in enumerate(views):
        w = 14 + 8 * len(v)
        els += [_el("rectangle", f"{eid}_v{k}", cx, y + 36, w, 24, OR if k == on else ROOM,
                    "#fff4e6" if k == on else "#ffffff", roundness={"type": 3})] + text(f"{eid}_v{k}_t", cx + 7, y + 40, v, 12, INK)
        cx += w + 8
    return els


def crumb_lines(words, width=118):
    """The path, wrapped on its separators so no folder name is cut."""
    out, cur = [], ""
    for part in words.split(" / "):
        nxt = part if not cur else cur + " / " + part
        if len(nxt) > width and cur:
            out.append(cur + " /")
            cur = part
        else:
            cur = nxt
    return out + [cur]


WAITS = re.compile(r"waits?( for| on) you|waiting for you|needs your|your sign|your call")


def waits_on_you(word):
    return word.startswith("🙋") or bool(WAITS.search(word))


def state_color(word):
    """A state word's colour, as live: orange only when it waits on the person; green done; blue running or next."""
    w = word.lstrip("🙋✅⏳⬜ ")
    if waits_on_you(word):
        return OR
    if word.startswith("✅") or w.startswith(("done", "agreed", "answered", "checked", "signed", "ok", "closed")):
        return GR
    if word.startswith("⏳") or w.startswith(("running", "next")):
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


def btn_w(verbs):
    return sum(16 + 7.5 * len(v) + 8 for v in verbs)


def chip(eid, x, y, words, color=BLUE):
    """An id as the live page links it (X01, D02, j02): a small outlined chip."""
    w = 12 + 7 * len(words)
    return [_el("rectangle", eid, x, y, w, 20, color, "#ffffff", roundness={"type": 3})] + text(eid + "_t", x + 6, y + 3, words, 11, color)


def dotmark(eid, x, y, mark, r=11):
    """A cell's dot, as the live grid draws it: ● ran or written, ◐ drafted, ○ planned or to write, ◌ running,
    ✕ refused or failed, — not asked."""
    if mark == "—":
        return line(eid, [(x, y + r / 2), (x + r, y + r / 2)], ROOM, 1)
    if mark == "✕":
        return text(eid, x, y - 2, "✕", 11, RE)
    stroke, fill, dash = {"●": (INK, INK, False), "◐": (INK, "#adb5bd", False), "○": (INK, "#ffffff", False),
                          "◌": (BLUE, "#ffffff", True)}[mark]
    return [_el("ellipse", eid, x, y, r, r, stroke, fill, strokeStyle="dashed" if dash else "solid")]


# ── a section's content, drawn as what it is ──────────────────────────────────────────────────────────────────────
def k_big(eid, x, y, w, words, state):
    """The view's main point: one large sentence, its state or small line under it."""
    sy = y + 30 + 24 * words.count("\n")
    return text(eid + "_w", x + 4, y, words, 19, INK) + (text(eid + "_s", x + 4, sy, state, 12, state_color(state)) if state else [])


def k_line(eid, x, y, w, words):
    return text(eid, x + 4, y, words, 12, INK)


def k_note(eid, x, y, w, words):
    """A small plain line: a sub-heading, a key, or what a band's view repeats."""
    return text(eid, x + 2, y, words, 11, BODY)


def k_kv(eid, x, y, w, rows):
    els = []
    for k, (key, val) in enumerate(rows):
        els += text(f"{eid}{k}k", x + 4, y + 4 + 24 * k, key, 12, BODY)
        els += text(f"{eid}{k}v", x + 130, y + 4 + 24 * k, val, 12, state_color(val) if val[:1] in "🙋✅⏳⬜" else INK)
    return els


def k_table(eid, x, y, w, head_, rows, foot=""):
    """A small table, as the file reads; each column as wide as its words; a state cell keeps its word and colour; its
    foot, a small line under it."""
    n = len(head_)
    widths = [max([len(head_[j])] + [len(r[j]) for r in rows if j < len(r)]) + 3 for j in range(n)]   # sized to its words
    unit = (w - 16) / sum(widths)
    xs = [x + 8 + unit * sum(widths[:j]) for j in range(n)]
    els = [_el("rectangle", eid, x, y, w, 24 * (len(rows) + 1) + 6, ROOM, "#ffffff", roundness={"type": 3})]
    for j, c in enumerate(head_):
        els += text(f"{eid}h{j}", xs[j], y + 6, c, 11, TITLE)
    for i, r in enumerate(rows):
        els += line(f"{eid}l{i}", [(x, y + 26 + 24 * i), (x + w, y + 26 + 24 * i)], "#e9ecef", 1)
        for j, c in enumerate(r):
            col = state_color(c) if c[:1] in "🙋✅⏳⬜" else (BLUE if c.endswith("↗") or c.startswith("+ ") else INK)
            els += text(f"{eid}r{i}_{j}", xs[j], y + 31 + 24 * i, c, 11, col)
    return els + (text(eid + "_foot", x + 4, y + 24 * (len(rows) + 1) + 14, foot, 11, BODY) if foot else [])


def k_todo(eid, x, y, w, items):
    """A Process step's to-do rows, as live pb-todo: the act, its small line, its state word, its verb; a row that
    waits on you orange."""
    els = []
    for k, (name, small, state, verb) in enumerate(items):
        ry, you = y + 50 * k, waits_on_you(state)
        els += [_el("rectangle", f"{eid}{k}", x, ry, w, 44, OR if you else "#e9ecef", "#fff4e6" if you else "#ffffff",
                    roundness={"type": 3})]
        els += text(f"{eid}{k}_n", x + 12, ry + 6, name, 13, TITLE) + text(f"{eid}{k}_w", x + 12, ry + 25, small, 11, BODY)
        right = x + w - 10
        if verb:
            els += _btns(f"{eid}{k}_b", right, ry + 10, (verb,), OR if you else BLUE)
            right -= btn_w((verb,)) + 4
        els += text(f"{eid}{k}_s", right - 6.4 * len(state), ry + 14, state, 11, state_color(state))
    return els


def k_answers(eid, x, y, w, items):
    """The answers, one line each: an id chip, the line."""
    els = []
    for k, (qid, words) in enumerate(items):
        els += chip(f"{eid}{k}_c", x + 4, y + 26 * k, qid) + text(f"{eid}{k}_w", x + 58, y + 26 * k + 3, words, 12, INK)
    return els


def k_levels(eid, x, y, w, levels):
    """Questions grouped by DIKW level, each group folding (asked 261102): the open one lists its questions, an id chip
    and one line each; the others closed, their word on the right."""
    els, yy = [], y
    for i, (name, word, rows) in enumerate(levels):
        els += text(f"{eid}{i}_n", x + 4, yy + 2, ("▾ " if rows else "▸ ") + name, 12, TITLE)
        els += text(f"{eid}{i}_s", x + 170, yy + 3, word, 11, state_color(word))
        els += line(f"{eid}{i}_l", [(x, yy + 22), (x + w, yy + 22)], "#e9ecef", 1)
        yy += 28
        for k, (qid, words) in enumerate(rows or ()):
            els += chip(f"{eid}{i}_{k}c", x + 22, yy, qid) + text(f"{eid}{i}_{k}w", x + 76, yy + 3, words, 11, INK)
            yy += 24
    return els


def levels_h(levels):
    return sum(28 + 24 * len(r or ()) for _, _, r in levels)


def k_jobdots(eid, x, y, w, key, rows):
    """Each Job as one row: its id, its plan × freeze, a dot per DIKW level (X D I K W), how much is written (asked
    261106: "a dot row per DIKW level, as Questions")."""
    els = text(eid + "_key", x + 4, y, key, 11, BODY)
    for k, (jid, words, dots, said) in enumerate(rows):
        ry = y + 22 + 50 * k
        els += [_el("rectangle", f"{eid}{k}", x, ry, w, 44, "#e9ecef", "#ffffff", roundness={"type": 3})]
        els += chip(f"{eid}{k}_c", x + 10, ry + 12, jid)
        els += text(f"{eid}{k}_w", x + 60, ry + 5, words, 11, BODY)
        for i, (lv, m) in enumerate(zip("XDIKW", dots)):
            dx = x + 60 + 30 * i
            els += text(f"{eid}{k}_{i}L", dx, ry + 23, lv, 10, BODY) + dotmark(f"{eid}{k}_{i}d", dx + 10, ry + 25, m)
        els += text(f"{eid}{k}_s", x + w - 10 - 6.4 * len(said), ry + 14, said, 11, state_color(said))
    return els


DG_COLS = (("question", 150), ("Full", 52), ("First", 52), ("Second", 52), ("Third", 52), ("Cross", 52), ("page", 120),
           ("check", 70))


def k_dotgrid(eid, x, y, w, key, levels):
    """Questions × cuts, one dot a cell, folded by DIKW level (asked 261106: "one dot, folded by DIKW level"): the open
    level shows its rows, a column per cut, then the page and its check."""
    els = text(eid + "_key", x + 4, y, key, 11, BODY)
    xs, cx = [], x + 4
    for _, cw in DG_COLS:
        xs.append(cx)
        cx += cw
    yy = y + 22
    for i, (name, word, rows) in enumerate(levels):
        els += text(f"{eid}{i}_n", x + 4, yy + 2, ("▾ " if rows else "▸ ") + name, 12, TITLE)
        els += text(f"{eid}{i}_s", x + 170, yy + 3, word, 11, state_color(word))
        els += line(f"{eid}{i}_l", [(x, yy + 22), (x + w, yy + 22)], "#e9ecef", 1)
        yy += 28
        if not rows:
            continue
        for j, (c, _) in enumerate(DG_COLS):
            els += text(f"{eid}{i}h{j}", xs[j] + (8 if j else 18), yy, c, 10, TITLE)
        yy += 20
        for r, (q, cells, page, check) in enumerate(rows):
            els += text(f"{eid}{i}_{r}q", xs[0] + 18, yy + 2, q, 11, BLUE)
            for j, m in enumerate(cells):
                els += dotmark(f"{eid}{i}_{r}_{j}", xs[j + 1] + 18, yy + 3, m)
            els += text(f"{eid}{i}_{r}p", xs[6] + 8, yy + 2, page, 10, BLUE if page.endswith("↗") else BODY)
            els += text(f"{eid}{i}_{r}k", xs[7] + 8, yy + 2, check, 10, state_color(check))
            yy += 22
    return els


def dotgrid_h(levels):
    return 22 + sum(28 + (20 + 22 * len(r) if r else 0) for _, _, r in levels)


def k_tiles(eid, x, y, w, items):
    """A card of key numbers: each number large, its label small under it."""
    tw = (w - 8 * (len(items) - 1)) / len(items)
    els = []
    for k, (big_, small) in enumerate(items):
        tx = x + k * (tw + 8)
        els += [_el("rectangle", f"{eid}{k}", tx, y, tw, 48, ROOM, "#ffffff", roundness={"type": 3})]
        els += text(f"{eid}{k}_t", tx + 8, y + 6, big_, 14, INK) + text(f"{eid}{k}_w", tx + 8, y + 28, small, 10, BODY)
    return els


def k_fig(eid, x, y, w, caption, n=3):
    """A small figure: a few bars so it reads as a chart, its caption beside it."""
    els = [_el("rectangle", eid, x, y, 150, 62, ROOM, "#ffffff")]
    for k in range(n):
        bh = (22, 44, 34, 50)[k % 4]
        els += [_el("rectangle", f"{eid}_b{k}", x + 20 + 40 * k, y + 54 - bh, 22, bh, "#74c0fc", "#a5d8ff")]
    return els + text(eid + "_c", x + 162, y + 6, caption, 11, INK)


PANEL_H = {"kv": lambda p: 22 * len(p[1]), "table": lambda p: 30 + 20 * len(p[2]), "tiles": lambda p: 58,
           "fig": lambda p: 70, "line": lambda p: 20, "form": lambda p: 22 * len(p[1]), "btn": lambda p: 30}


def k_sidetabs(eid, x, y, w, items, panel):
    """Side tabs: the list on the left, the first open (blue); on the right the open one to read, its parts in order
    (kv lines, a small table, a card of numbers, a figure, a form, buttons)."""
    lw = 170
    els = []
    for k, (head_, word) in enumerate(items):
        iy = y + k * 44
        els += [_el("rectangle", f"{eid}{k}", x, iy, lw, 38, BLUE if k == 0 else ROOM, "#e7f5ff" if k == 0 else "#ffffff",
                    roundness={"type": 3})]
        els += text(f"{eid}{k}_t", x + 8, iy + 4, head_, 11, TITLE) + text(f"{eid}{k}_w", x + 8, iy + 21, word, 10, state_color(word))
    px, pw = x + lw + 12, w - lw - 12
    els += [_el("rectangle", eid + "_d", px, y, pw, sidetabs_h(items, panel) - 6, ROOM, "#ffffff", roundness={"type": 3})]
    yy = y + 10
    for j, p in enumerate(panel):
        kind, pid = p[0], f"{eid}_p{j}"
        if kind == "kv":
            for k, (n_, words) in enumerate(p[1]):
                els += text(f"{pid}{k}k", px + 12, yy + 22 * k, n_, 11, BODY)
                els += text(f"{pid}{k}v", px + (80 if n_ else 12), yy + 22 * k, words, 11,
                            BLUE if words.endswith("↗") else state_color(words) if words[:1] in "🙋✅⏳⬜✓" else INK)
        elif kind == "table":
            cols, rows = p[1], p[2]
            wts = [0.4, 2.6] + [1.0] * (len(cols) - 2) if cols[0] == "#" else [1.0] * len(cols)   # an id column narrow
            unit = (pw - 24) / sum(wts)
            xs = [px + 12 + unit * sum(wts[:c]) for c in range(len(cols))]
            for c, col in enumerate(cols):
                els += text(f"{pid}h{c}", xs[c], yy, col, 10, TITLE)
            for i, r in enumerate(rows):
                els += line(f"{pid}l{i}", [(px + 12, yy + 17 + 20 * i), (px + pw - 12, yy + 17 + 20 * i)], "#e9ecef", 1)
                for c, cell in enumerate(r):
                    els += text(f"{pid}r{i}_{c}", xs[c], yy + 21 + 20 * i, cell, 10,
                                state_color(cell) if cell[:1] in "✅⏳⬜🙋" else INK)
        elif kind == "tiles":
            els += k_tiles(pid, px + 12, yy, pw - 24, p[1])
        elif kind == "fig":
            els += k_fig(pid, px + 12, yy, pw - 24, p[1])
        elif kind == "line":
            els += text(pid, px + 12, yy, p[1], 11, BLUE if p[1].endswith("↗") else TITLE)
        elif kind == "form":                     # a form's question and its choices, the person's pick ticked
            for k, (n_, words) in enumerate(p[1]):
                if n_ in ("A", "B", "C"):
                    els += [_el("ellipse", f"{pid}{k}o", px + 12, yy + 22 * k + 2, 11, 11, INK,
                                INK if "my pick" in words else "#ffffff")]
                    els += text(f"{pid}{k}t", px + 30, yy + 22 * k, f"{n_} · {words}", 11, INK)
                else:
                    els += text(f"{pid}{k}t", px + 12, yy + 22 * k, words, 11, TITLE if n_ else BODY)
        elif kind == "btn":
            els += _btns(pid, px + pw - 12, yy, p[1], OR if p[1][0].startswith("Copy feedback") else BLUE)
        yy += PANEL_H[kind](p)
    return els


def sidetabs_h(items, panel):
    return max(44 * len(items), 16 + sum(PANEL_H[p[0]](p) for p in panel)) + 6


def k_canvas(eid, x, y, w):
    """The question canvas, small: the find bar, Executive on top, then a column per level, Data → Wisdom, a line a
    citation; one question pinned (I01): what it rests on solid, what uses it dashed, the rest faded; its panel right
    (as s51's B sketch, asked 261102)."""
    els = text(eid + "_bar", x + 4, y, "find …    ☐ Only linked   ▢ page written   ▢ drafted   ▢ not yet", 11, BODY)
    cw_, ch_ = 82, 24
    pos = {}
    els += [_el("rectangle", eid + "_X", x, y + 22, 430, 40, ROOM, "#e7f0fb", roundness={"type": 3})]
    els += text(eid + "_Xt", x + 8, y + 26, "EXECUTIVE", 9, BODY)
    for k, q in enumerate(("X01", "X02")):
        pos[q] = (x + 110 + k * 150, y + 30)
    cols = (("DATA", ("D01", "D02")), ("INFORMATION", ("I01", "I02")), ("KNOWLEDGE", ("K01", "K02")), ("WISDOM", ("W01",)))
    for c, (name, qs) in enumerate(cols):
        cx = x + c * 110
        els += [_el("rectangle", f"{eid}_c{c}", cx, y + 74, 98, 100, ROOM, GHOST, roundness={"type": 3})]
        els += text(f"{eid}_c{c}t", cx + 6, y + 78, name, 9, BODY)
        for i, q in enumerate(qs):
            pos[q] = (cx + 8, y + 96 + i * 36)
    lit = {"I01", "D01", "K01", "X01", "W01"}
    for q, (qx, qy) in pos.items():
        on = q in lit
        els += [_el("rectangle", f"{eid}_q{q}", qx, qy, cw_, ch_, INK if on else "#ced4da", "#ffffff",
                    roundness={"type": 3}, strokeWidth=3 if q == "I01" else 1)]
        els += text(f"{eid}_q{q}t", qx + 8, qy + 5, q, 11, INK if on else ROOM)
    cites = (("I01", "D01", "solid"), ("K01", "I01", "dashed"), ("X01", "I01", "dashed"), ("W01", "K01", "dashed"),
             ("I02", "D01", "faded"), ("K02", "I02", "faded"), ("X02", "K01", "faded"), ("D02", "D01", "skip"))
    for a, b, how in cites:
        if how == "skip":
            continue
        (ax, ay), (bx, by) = pos[a], pos[b]
        if a[0] == "X":
            pts = [(ax + cw_ / 2, ay + ch_), (bx + cw_ / 2, by)]
        else:
            pts = [(bx + cw_, by + ch_ / 2), (ax, ay + ch_ / 2)]
        if how == "faded":
            els += line(f"{eid}_e{a}{b}", pts, "#dee2e6", 1)
        else:
            els += arrow(f"{eid}_e{a}{b}", pts, INK, dashed=how == "dashed", width=1)
    px = x + 450
    els += [_el("rectangle", eid + "_P", px, y + 22, w - 450, 152, ROOM, "#ffffff", roundness={"type": 3})]
    for k, (words, size, col) in enumerate((("I01 · outcome by arm", 12, TITLE), ("page: written · open its Task ↗", 10, BLUE),
                                             ("Rests on", 10, BODY), ("D01", 11, INK), ("Used by", 10, BODY),
                                             ("K01 · X01", 11, INK), ("Ask about it · Propose", 10, BLUE))):
        els += text(f"{eid}_P{k}", px + 10, y + 30 + 20 * k, words, size, col)
    return els


def k_figthumbs(eid, x, y, w, words, caption, thumbs, link):
    """The answer, then the page's first figure large and the others as thumbnails (asked 261106: "the page's first
    figure, others as thumbnails")."""
    els = text(eid + "_w", x + 4, y, words, 15, INK)
    fy = y + 26 + 20 * (words.count("\n") + 1)
    els += [_el("rectangle", eid + "_f", x, fy, 330, 130, ROOM, "#ffffff")]
    for k, (lab, bh) in enumerate((("arm A", 50), ("arm B", 80))):
        bx = x + 70 + 120 * k
        els += [_el("rectangle", f"{eid}_fb{k}", bx, fy + 110 - bh, 60, bh, "#74c0fc", "#a5d8ff")]
        els += line(f"{eid}_fe{k}", [(bx + 30, fy + 100 - bh), (bx + 30, fy + 120 - bh)], INK, 1)
        els += text(f"{eid}_fl{k}", bx + 10, fy + 114, lab, 9, BODY)
    els += text(eid + "_fc", x + 344, fy + 8, caption, 12, INK)
    els += text(eid + "_fn", x + 344, fy + 30, "a click opens it large", 10, BODY)
    ty = fy + 142
    tw = (w - 8 * (len(thumbs) - 1)) / len(thumbs)
    for k, lab in enumerate(thumbs):
        tx = x + k * (tw + 8)
        els += [_el("rectangle", f"{eid}_t{k}", tx, ty, tw, 44, ROOM, "#ffffff")]
        for j in range(2):
            bh = (14, 26)[j] if k % 2 == 0 else (24, 10)[j]
            els += [_el("rectangle", f"{eid}_t{k}b{j}", tx + 18 + 26 * j, ty + 38 - bh, 14, bh, "#74c0fc", "#a5d8ff")]
        els += text(f"{eid}_t{k}l", tx + 2, ty + 48, lab, 9, BODY)
    return els + text(eid + "_lk", x + 4, ty + 68, link, 11, BLUE)


def figthumbs_h(words):
    return 26 + 20 * (words.count("\n") + 1) + 142 + 86


def k_tree(eid, x, y, w, root, branches):
    """The map, as the live parts_mindmap draws it: the root on the left, a branch per node, its short name and one
    plain line; its children on the right (Open all, Close all open and close them)."""
    rows = [branch_h(ch) for *_, ch in branches]
    tot = sum(r + 10 for r in rows) - 10
    rh = 18 + 14 * (root.count("\n") + 1)
    ry = y + tot / 2 - rh / 2
    els = [_el("rectangle", eid + "_r", x, ry, 130, rh, INK, "#ffffff", roundness={"type": 3})]
    els += text(eid + "_rt", x + 8, ry + 9, root, 11, INK)
    by = y
    for k, (pill, name, words, children) in enumerate(branches):
        bh = rows[k]
        cy = by + bh / 2
        els += line(f"{eid}{k}_l", [(x + 130, ry + rh / 2), (x + 160, cy)], ROOM, 1)
        els += [_el("rectangle", f"{eid}{k}", x + 160, cy - 22, 220, 44, ROOM, "#ffffff", roundness={"type": 3})]
        nx, ny = x + 170 + (6.2 * len(pill) + 8 if pill else 0), cy - (18 if words else 8)   # a name alone sits centred
        els += (text(f"{eid}{k}_p", x + 170, ny + 1, pill, 10, BODY) if pill else []) + text(f"{eid}{k}_n", nx, ny, name, 12, TITLE)
        els += text(f"{eid}{k}_w", x + 170, cy + 3, words, 11, BODY) if words else []
        for j, cn in enumerate(children):
            chy = by + (bh - 30 * len(children)) / 2 + 30 * j + 2
            els += line(f"{eid}{k}_{j}_l", [(x + 380, cy), (x + 404, chy + 13)], ROOM, 1)
            els += [_el("rectangle", f"{eid}{k}_{j}", x + 404, chy, w - 404, 26, ROOM, "#ffffff", roundness={"type": 3})]
            els += text(f"{eid}{k}_{j}_n", x + 412, chy + 6, cn, 11, INK)
        by += bh + 10
    return els


def branch_h(children):
    return max(46, 30 * len(children))


def tree_h(branches):
    return sum(branch_h(b[3]) + 10 for b in branches) - 10


def k_verbs(eid, x, y, w, verbs):
    """Plain buttons on the left (the map's Open all, Close all)."""
    els, cx = [], x
    for k, v in enumerate(verbs):
        bw = 16 + 7.5 * len(v)
        els += [_el("rectangle", f"{eid}{k}", cx, y, bw, 22, ROOM, "#ffffff", roundness={"type": 3})]
        els += text(f"{eid}{k}_t", cx + 8, y + 4, v, 11, INK)
        cx += bw + 8
    return els


def k_chain(eid, x, y, w, steps):
    """A sequence as boxes and arrows, a word above each: which Job came first, which clock each moved."""
    bw = (w - 30 * (len(steps) - 1)) / len(steps)
    els = []
    for k, (role, name) in enumerate(steps):
        bx = x + k * (bw + 30)
        els += text(f"{eid}{k}_r", bx + 2, y, role, 10, BODY)
        els += [_el("rectangle", f"{eid}{k}", bx, y + 16, bw, 40, ROOM, "#ffffff", roundness={"type": 3})]
        els += text(f"{eid}{k}_w", bx + 10, y + 28, name, 12, INK)
        if k:
            els += arrow(f"{eid}{k}_a", [(bx - 27, y + 36), (bx - 4, y + 36)], ROOM)
    return els


STUDIO_VERBS = ("Draw", "Mind map", "Work", "Delivery")


def k_trows(eid, x, y, w, items):
    """Studio rows as live: the topic's name, its stage and its kind as pills, its one line, its verbs (a waiting form
    adds the orange 🙋 Interaction), its picture on the right."""
    els = []
    for k, (name, stage, kind, words, verbs, asks) in enumerate(items):
        ry = y + 112 * k
        els += [_el("rectangle", f"{eid}{k}", x, ry, w, 104, ROOM, "#ffffff", roundness={"type": 3})]
        els += text(f"{eid}{k}_n", x + 14, ry + 12, name, 14, TITLE)
        px = x + 14 + 0.62 * 14 * len(name) + 10
        for j, (pill, col) in enumerate(((stage, ROOM), (kind, BLUE))):
            pw = 14 + 6.6 * len(pill)
            els += [_el("rectangle", f"{eid}{k}_p{j}", px, ry + 12, pw, 18, col, "#ffffff", roundness={"type": 3})]
            els += text(f"{eid}{k}_p{j}t", px + 7, ry + 14, pill, 10, col)
            px += pw + 6
        els += text(f"{eid}{k}_w", x + 14, ry + 40, words, 12, INK)
        bx = x + 14
        for j, v in enumerate(verbs + (("🙋 Interaction",) if asks else ())):
            bw = 16 + 7.2 * len(v)
            you = v.startswith("🙋")
            els += [_el("rectangle", f"{eid}{k}_v{j}", bx, ry + 68, bw, 24, OR if you else ROOM, "#fff4e6" if you else "#ffffff",
                        roundness={"type": 3})] + text(f"{eid}{k}_v{j}t", bx + 8, ry + 73, v, 11, OR if you else INK)
            bx += bw + 6
        tx = x + w - 150
        els += [_el("rectangle", f"{eid}{k}_th", tx, ry + 12, 136, 80, ROOM, GHOST)]
        for j in range(3):
            els += [_el("rectangle", f"{eid}{k}_th{j}", tx + 12 + 40 * j, ry + 40 + 8 * (j % 2), 30, 18, ROOM, "#ffffff")]
            if j:
                els += line(f"{eid}{k}_tl{j}", [(tx + 12 + 40 * j - 10, ry + 49), (tx + 12 + 40 * j, ry + 49)], ROOM, 1)
    return els


def k_empty(eid, x, y, w, words, verb):
    """A page with no topic of its own (asked 261106: "Studio says none yet, with Add a topic")."""
    els = text(eid + "_w", x + 4, y, words, 13, INK)
    bw = 16 + 7.5 * len(verb)
    return els + [_el("rectangle", eid + "_b", x + 4, y + 28, bw, 26, BLUE, "#ffffff", roundness={"type": 3})] + \
        text(eid + "_bt", x + 12, y + 33, verb, 12, BLUE)


def k_agent(eid, x, y, w, verbs):
    """Ask the agent: one notes box, then its Copy prompt buttons."""
    els = [_el("rectangle", eid, x, y, w, 36, ROOM, "#ffffff", roundness={"type": 3}, strokeStyle="dashed")]
    els += text(eid + "_t", x + 12, y + 10, "your notes, copied with the prompt", 12, BODY)
    return els + _btns(eid + "_b", x + w, y + 46, verbs)


def _red(els):
    """A kept proposal's content: its edges red (a reviewed design no later ask overruled stays, red, open)."""
    for e in els:
        if e["type"] == "rectangle" and e["strokeColor"] in (ROOM, "#e9ecef", INK, BLUE):
            e["strokeColor"] = RE
    return els


def k_red(eid, x, y, w, label, kind, *args):
    """A kept proposal with no heading bar: its name and "proposal" in red, then the thing, red-edged, behind a red
    dashed line."""
    h = KIND[kind][1](args)
    els = text(eid + "_l", x + 2, y, f"{label} · proposal", 12, RE)
    els += line(eid + "_in", [(x + 4, y + 20), (x + 4, y + 22 + h)], RE, 1, dashed=True)
    return els + _red(KIND[kind][0](eid + "_c", x + 14, y + 22, w - 14, *args))


def k_redline(eid, x, y, w, words):
    """A kept proposal that is only a line."""
    return text(eid, x + 2, y, f"{words} · proposal", 12, RE)


KIND = {"big": (k_big, lambda a: (56 if a[1] else 30) + 24 * a[0].count("\n")), "line": (k_line, lambda a: 20),
        "note": (k_note, lambda a: 14 * (a[0].count("\n") + 1)), "kv": (k_kv, lambda a: 24 * len(a[0])),
        "table": (k_table, lambda a: 24 * (len(a[1]) + 1) + 6 + (24 if len(a) > 2 and a[2] else 0)), "todo": (k_todo, lambda a: 50 * len(a[0]) - 6),
        "answers": (k_answers, lambda a: 26 * len(a[0]) - 6), "levels": (k_levels, lambda a: levels_h(a[0])),
        "jobdots": (k_jobdots, lambda a: 22 + 50 * len(a[1]) - 6), "dotgrid": (k_dotgrid, lambda a: dotgrid_h(a[1])),
        "tiles": (k_tiles, lambda a: 48), "sidetabs": (k_sidetabs, lambda a: sidetabs_h(*a)),
        "canvas": (k_canvas, lambda a: 176), "figthumbs": (k_figthumbs, lambda a: figthumbs_h(a[0])),
        "tree": (k_tree, lambda a: tree_h(a[1])), "verbs": (k_verbs, lambda a: 22), "chain": (k_chain, lambda a: 56),
        "trows": (k_trows, lambda a: 112 * len(a[0]) - 8), "empty": (k_empty, lambda a: 56),
        "agent": (k_agent, lambda a: 70), "red": (k_red, lambda a: 22 + KIND[a[1]][1](a[2:])),
        "redline": (k_redline, lambda a: 16)}


def S(title, word="", red=False, flag=False, wait=""):
    """A section's heading bar: closed (▸), as every section starts; its state word on the right, as live; red, a kept
    proposal, unnumbered; flag, a 🙋 Interaction that waits for you (an orange edge); wait, the one thing that waits on
    the person, its line under the closed bar (live fd-wait)."""
    return {"t": title, "w": word, "red": red, "flag": flag, "wait": wait}


WAIT_H = 22                          # a waiting line under a closed bar


def bar_of(head_):
    return head_ if isinstance(head_, dict) else S(head_ or "")


def sec_h(sec):
    if sec[0] == "rule":
        return 24
    if sec[0] == "group":
        return 36
    b = bar_of(sec[0])
    has, wait = bool(b["t"]), WAIT_H if b.get("wait") else 0
    if sec[1] == "none":
        return 40 + wait
    return (40 if has else 0) + wait + KIND[sec[1]][1](sec[2:]) + 16


def sec_draw(eid, x, y, w, sec):
    """A numbered heading bar, closed (▸) as live starts every section; what it opens to drawn under it, behind a
    dashed line ("none": the bar alone, as on Work, whose Results repeat the Report's); a group heading (⚙️ Process,
    📊 Results)."""
    if sec[0] == "rule":
        return line(eid, [(x, y + 8), (x + w, y + 8)], ROOM, 1, dashed=True)
    if sec[0] == "group":
        return text(eid, x, y + 6, sec[1], 16, INK) + line(eid + "_l", [(x + 130, y + 18), (x + w, y + 18)], PALE, 1)
    b = bar_of(sec[0])
    if not b["t"]:
        return KIND[sec[1]][0](eid + "_c", x, y, w, *sec[2:])
    stroke, fill, ink = (RE, "#fff5f5", RE) if b["red"] else (OR, "#fff4e6", TITLE) if b["flag"] else (ROOM, "#ffffff", TITLE)
    els = [_el("rectangle", eid, x, y, w, 30, stroke, fill, roundness={"type": 3})]
    els += text(eid + "_t", x + 12, y + 7, "▸ " + b["t"], 13, ink)
    word = "proposal" if b["red"] else b["w"]
    if word:
        els += text(eid + "_w", x + w - 12 - 6.8 * len(word), y + 8, word, 11, RE if b["red"] else state_color(word))
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
    view-button-list with this view in orange, the goal-line (a Task's only), the view-caption and its sections."""
    name, path, goal = PAGE[level]
    els = window(eid + "w", x, y, W, h, f"/_board/workbench?layout=focus&path=…/{name}&section={section}")
    els += rails(eid + "rl", x, y, level, section)
    cx = x + X0
    lines = crumb_lines(path)
    for k, ln in enumerate(lines):
        els += text(f"{eid}_crumb{k}", cx, y + 40 + 14 * k, ln, 10, BODY)
    top = y + 46 + 14 * len(lines)
    els += head(eid + "h", cx, top, name, section, views, on)
    if goal:                                         # a Task's Aim, as live: its label small, the id under a rule
        els += text(eid + "_goal", cx, top + 72, goal, 13, INK)
        els += line(eid + "_goall", [(cx, top + 94), (cx + CW, top + 94)], PALE, 1)
        top += 30
    els += text(eid + "_cap", cx, top + 76, caption, 12, BODY)
    yy = top + 106 if caption else top + 76
    for k, sec in enumerate(secs):
        els += sec_draw(f"{eid}r{k}", cx, yy, CW, sec)
        yy += sec_h(sec)
    return els


# ── the views (view, its view-caption, its sections in page order) ─────────────────────────────────────────────────
G_PROC, G_RES = ("group", "⚙️ Process"), ("group", "📊 Results")
MAP_CAP = "How it is built, as a map: its parts, and what each must find out."

# ── the forms, and which view's 🙋 holds each (as live, 261106): a form is (its tab, the form's questions as side tabs,
# the open question's panel, its waiting line, the bar's word)
POOL = ("Pooling on freeze two", (("Q1 · Counsel scope", "waiting"), ("Q2 · Small group", "waiting")),
        (("line", "Pooling on freeze two"),
         ("form", (("Q1", "Should W01's counsel on freeze two speak for both groups?"),
                   ("A", "Yes: one counsel for the first and second groups · my pick"),
                   ("B", "Not yet: wait for K02's replication over the window"))),
         ("kv", (("", "asked by t05_K01_gap-holds · about s02-why-answers-moved"),)), ("btn", ("Copy feedback",))),
        "🙋 Pooling on freeze two: Q1 · Counsel scope", "2 wait for you")
SCOPE = ("The example's scope", (("Q1 · Second Job partly done", "my own decision"), ("Q2 · Signs by date", "my own decision")),
         (("line", "The example's scope"), ("form", (("Q1", "<the question, as asked>"), ("", "✓ my own decision"))),
          ("kv", (("", "asked by t06_W01_next-round · about s02-why-answers-moved"),))), "", "answered")
IX_OF = {("block", "Jobs"): (POOL,), ("block", "Handoff"): (SCOPE,), ("job", "Grid"): (POOL, SCOPE)}


def ix(level, view, n=0):
    """🙋 Interaction, the view's last section, holding this view's own forms: its state word, its first waiting
    question under the closed bar; a side tab per question (or per form, when it holds several) and the open one's form
    on the right; "nothing yet" when the view has none."""
    title = (f"{n} · " if n else "") + "🙋 Interaction"
    forms = IX_OF.get((level, view), ())
    if not forms:
        return (S(title, "nothing yet"), "none")
    first = forms[0]
    tabs = first[1] if len(forms) == 1 else tuple((f[0], f[4]) for f in forms)
    word = first[4]
    return (S(title, word, flag=bool(first[3]), wait=first[3]), "sidetabs", tabs, first[2])


def closing(secs, level, view):
    """The view's sections, then its 🙋 Interaction numbered after the last band's numbered sections (unnumbered when
    that band has none, as live)."""
    last = max([i for i, s in enumerate(secs) if s[0] == "group"], default=-1)
    nums = [int(m.group(1)) for s in secs[last + 1:] if s[0] not in ("rule", "group")
            for m in [re.match(r"(\d+) · ", bar_of(s[0])["t"])] if m]
    return tuple(secs) + (ix(level, view, max(nums) + 1 if nums else 0),)


def same(letter, view):
    """Work's 📊 Results repeat the Report's view, drawn by the same code: its bars drawn closed here, the content
    is the Report's letter."""
    return ("", "note", f"the Report's {letter} · {view}, drawn by the same code")


def bars(secs):
    """A Report view's sections as Work repeats them: its big line, then each numbered section as a closed bar."""
    return tuple(s if s[1] == "big" else (s[0], "none") for s in secs
                 if s[0] not in ("rule", "group") and (bar_of(s[0])["t"] or s[1] == "big"))


def report(level, items):
    return tuple((v, cap, closing(secs, level, v)) for v, cap, secs in items)


def work(level, report_items, process):
    """Each Work view: ⚙️ Process when it has a step, then 📊 Results, the Report's view by the same code."""
    out = []
    for k, (v, _, secs) in enumerate(report_items):
        cap, proc = process[v]
        body = ((G_PROC,) + proc if proc else ()) + (G_RES, same(LETTERS[k], v)) + bars(secs)
        out.append((v, cap, closing(body, level, v)))
    return tuple(out)


# ── the Board (s51 Report, s52 Work, s53 Studio) ─────────────────────────────────────────────────────────────────────
A_ONE = "Arm B's outcome rate is about 15 points above arm A's"
A_TWO = "It cannot speak for group_3, and covers only 16 days"
OVERALL = (("X01 · what we found", "answered · checked"), ("X02 · what data cannot say", "answered"))
OVERALL_PANEL = (("line", "What did the example find, in one line?"), ("kv", (("", A_ONE + "."),
                                                                             ("how sure", "firm on the whole population; the two groups pool"))),
                 ("fig", "Arm B's outcome rate is the higher one\nfrom I01 · t03"),
                 ("kv", (("", "the page, all cuts ↗"), ("check", "✅ 261106 · another agent"))))
FOUND = (("Data", "2 of 2 answered"), ("Information", "2 of 2 answered"), ("Knowledge", "1 of 2 answered"),
         ("Wisdom", "1 of 1 answered"))
FOUND_PANEL = (("kv", (("may say", "counts, what was seen"),)),
               ("line", "D01 ✅  What does the example extract hold?"),
               ("kv", (("", "960 rows and 5 columns over 16 days; nothing missing"), ("", "answered on 2 of 2 Jobs · r01_full ↗"))),
               ("line", "D02 ✅  Are the arms and groups the size we expect?"),
               ("kv", (("", "the arms close to even in every cut"), ("", "answered on 2 of 2 Jobs · r01_full ↗"))))
LEVELS_Q = (("Executive", "2 of 2 answered", (("X01", "what did the example find? · " + A_ONE),
                                              ("X02", "what can this data not say? · " + A_TWO))),
            ("Data", "2 of 2 answered", None), ("Information", "0 of 2 answered", None),
            ("Knowledge", "1 of 2 answered", None), ("Wisdom", "1 of 1 answered", None))
LEVELS_T = (("Executive", "2 of 2 written", (("X01", "what we found · cites the answers below it · page answered"),
                                            ("X02", "what data cannot say · page answered"))),
            ("Data", "2 of 2 written", None), ("Information", "0 of 2 written", None),
            ("Knowledge", "1 of 1 written", None), ("Wisdom", "0 of 1 written", None))
BLOCK_MAP = (("", "verbs", ("Open all", "Close all")), ("", "tree", BOARD, (
    ("✎", "How the questions build", "s01-question-map, a drawing", ()),
    ("Job 1", "j01 · plan 1 × freeze 1", "its Tasks, each its question", ("Task 1 · D01", "Task 3 · I01", "Task 5 · K01",
                                                                         "Task 7 · X01", "… 8 Tasks")),
    ("Job 2", "j02 · plan 1 × freeze 2", "its Tasks, each its question", ("Task 1 · D01", "Task 3 · I01", "… 8 Tasks")))))
BLOCK_R = (
    ("Answers", "The answers in one line each, the plans × data freezes, the newest Overall Report, and what each "
                "question found.", (
        ("", "big", "What this dataset says, Job by Job", ""),
        (S("1 · ⚓ The answers, one line each", "2 of 2 answered"), "answers", (("X01", A_ONE), ("X02", A_TWO))),
        (S("2 · 🧷 Analysis plans × data freezes", "1 open"), "table",
         ("analysis plan \\ data freeze", "freeze 1 · first ten days", "freeze 2 · all sixteen days"),
         (("plan 1 · example questions · ✅ signed", "j01 · closed · 8 of 8 written", "j02 · open · 6 of 8 written"),
          ("plan 2 · example follow-up · not signed", "+ Add a Job", "+ Add a Job"))),
        (S("3 · 📄 The Overall Report", "2 of 2 written"), "sidetabs", OVERALL, OVERALL_PANEL),
        (S("4 · 🔎 What each question found", "6 of 7 answered"), "sidetabs", FOUND, FOUND_PANEL))),
    ("Questions", "How the questions build on each other, each question and its answer, then every plan's questions.", (
        (S("1 · 🕸 How the questions build on each other", "plan not signed yet"), "canvas"),
        (S("2 · 💬 Each question and its answer", "6 of 9 answered"), "levels", LEVELS_Q),
        (S("3 · ❓ The questions, plan by plan", "1 proposal open"), "sidetabs",
         (("analysis plan 2 · follow-up", "not signed yet"), ("analysis plan 1 · questions", "signed 261106"), ("proposals", "1 open")),
         (("kv", (("", "Executive may say: the plain answer a leader asks for"),)),
          ("table", ("#", "question", "in this plan"), (("X01", "what did the example find?", "kept"),
                                                        ("D01", "what does the extract hold?", "kept"),
                                                        ("K02", "does the gap hold over the window?", "new"))))),
        (S("4 · 🧭 The Board's own questions", "1 of 1 answered"), "kv",
         (("Knowledge", "1 asked · may say: one claim, how sure, its rivals"),
          ("Q01", "Does the arm gap hold from data freeze 1 to data freeze 2? ↗"),
          ("", "run-report-q01 ✅ done · reads the Jobs' answers · the report ↗"))))),
    ("Jobs", "Each Job by DIKW level, the newest Job's Tasks, and the one clock each Job moved.", (
        (S("1 · 🧷 Each Job", "1 open"), "jobdots", "●  page written     ◐  drafted     ○  to write",
         (("j02", "analysis plan 1 × data freeze 2 · all sixteen days", "●●○●○", "5 of 8 written · open"),
          ("j01", "analysis plan 1 × data freeze 1 · first ten days", "●●●●●", "8 of 8 written · closed"))),
        (S("2 · 📂 The newest Job, j02 · its Tasks", "5 of 8 written"), "levels", LEVELS_T),
        (S("3 · ⏱ What each Job moved", "one clock each"), "chain", (("j01", "the first Job"), ("j02", "the data · from j01"))))),
    ("Data", "Each data freeze's key numbers and files, then the cuts every question runs on.", (
        (S("1 · 🗄 Data freezes", "newest first"), "sidetabs",
         (("data freeze 2 · all sixteen days", "frozen 261106"), ("data freeze 1 · first ten days", "frozen 261106")),
         (("tiles", (("960", "rows"), ("5", "columns"), ("16 days", "dates"), ("261106", "frozen"), ("j02", "Jobs on it"))),
          ("line", "cohort_summary.txt · data_dictionary.csv · manifest.json ↗"),
          ("kv", (("", "a few rows, 3 of 960, identifying columns left out"),)),
          ("table", ("date", "arm", "group", "outcome"), (("01-05", "B", "group_1", "1"), ("01-09", "A", "group_1", "1"),
                                                          ("01-11", "B", "group_1", "0"))))),
        (S("2 · ✂️ Cuts", "power floor 20 pp"), "table", ("cut", "where", "why"),
         (("full", "every row", "every row"), ("first", "group = group_1", "the largest group, on its own"),
          ("second", "group = group_2", "the second group, on its own"), ("cross", "first against second", "do they differ?"),
          ("third", "group = group_3", "too thin to answer")),
         "rows per freeze, full · first · second · third:   v1  600 · 350 · 210 · 40     v2  960 · 541 · 351 · 68"))),
    ("Handoff", "What the handoff will say, its draft, and what was handed to Design.", (
        ("", "big", "A handoff waits for a person's sign", ""),
        (S("1 · 🧠 What the handoff will say", "0 of 1 written"), "answers",
         (("W01", "what should the next round keep or change? · its page is still to write"),)),
        (S("2 · 🤝 The handoff draft", "a draft, not signed"), "kv",
         (("pair", "analysis plan 1 × data freeze 2"), ("counsel", "0 of 1 Wisdom answers written"), ("draft", "handoff-W01.md ↗"))),
        (S("3 · 📦 Handoffs", "none signed yet"), "table", ("counsel", "from Job", "signed"), (("W01 ↗", "j01", "—"),)))),
    ("MindMap", MAP_CAP, BLOCK_MAP),
)
BLOCK_REPORT = report("block", BLOCK_R)
BLOCK_WORK = work("block", BLOCK_R, {
    "Answers": ("The Overall Report to write, then the Report's Answers.", (
        (S("1 · ✍️ The Overall Report", "done"), "todo",
         (("Write the Overall Report for j02", "in the Job, from the answers below it", "✅ done", ""),)),)),
    "Questions": ("Your sign on the next plan, the proposals, new questions, then the questions to ask about.", (
        (S("1 · 📋 The next analysis plan", "2 wait for you", wait="🙋 Sign the plan analysis plan 2 · example follow-up: in the Prototype"),
         "todo", (("Sign the plan analysis plan 2", "in the Prototype", "🙋 waiting for you", "Open in the Prototype"),
                  ("Triage the open proposals", "into one batch for the next plan", "🙋 waiting for you", "Open the proposals"))),
        (S("2 · ❓ New questions", "2 ready"), "todo",
         (("Propose questions", "the gaps and weak answers, as proposals for the next plan", "ready", "Copy prompt"),
          ("Ask a Board question", "a question over the Jobs' answers", "ready", "Copy prompt"))))),
    "Jobs": ("Each Job's steps and a new Job, then the Report's Jobs.", (
        (S("1 · 🪜 Each Job, its steps", "j02 next: run"), "table", ("Job", "Runs", "pages", "checks", "close"),
         (("j02 · plan 1 × freeze 2", "next", "to do", "to do", "to do"),
          ("j01 · plan 1 × freeze 1", "✅ done", "✅ done", "✅ done", "✅ done"))),
        (S("2 · ➕ A new Job", "ready"), "todo",
         (("Add a Job", "a signed analysis plan × a data freeze, one clock moved", "ready", "Copy prompt"),)))),
    "Data": ("A new freeze or cut, then the freezes and cuts.", (
        (S("1 · 🗄 Freezes and cuts", "2 ready"), "todo",
         (("Add a data freeze", "a new extract, frozen, its rows counted per cut", "ready", "Copy prompt"),
          ("Propose a cut to the next plan", "a cut is plan, fixed before any outcome", "ready", "Copy prompt"))),)),
    "Handoff": ("The counsel, the draft and your sign, then the Report's Handoff.", (
        (S("1 · 🤝 The handoff", "1 waits for you", wait="🙋 Sign the handoff W01: Design reads only a signed handoff"), "todo",
         (("Write the counsel", "from the latest Job's Wisdom answers", "✅ done", ""),
          ("Sign the handoff W01", "Design reads only a signed handoff", "🙋 waiting for you", "Read the draft ↗"))),)),
    "MindMap": (MAP_CAP, ()),                     # nothing to do on the map: no ⚙️ Process
})
BLOCK_STUDIO = (                       # live studio rows; the groups by Tag and Ask the agent stay proposals (s53)
    ("Topics", "", (
        ("", "trows", (("s01-question-map", "explore", "display", "the example's questions as one map: a box per question",
                        ("Draw", "Mind map", "Delivery"), False),
                       ("s03-first-job-settled", "explore", "display", "j01 ran plan 1 on data freeze 1 and closed checked.",
                        STUDIO_VERBS, False),
                       ("s02-why-answers-moved", "explore", "display", "j02 runs the same analysis plan on data freeze 2.",
                        STUDIO_VERBS, True))),
        ("", "redline", "🏷 Groups by Tag: Map · Why it moved · Cut ideas · Story for Design, each row says where"),
        ("", "red", "✍️ Ask the agent", "agent", ("Copy prompt: talk and sketch",)))),
)

# ── the Job (s54 Report, s55 Work, s56 Studio) ───────────────────────────────────────────────────────────────────────
DG_KEY = "●  ran     ○  planned     ◌  running     ✕  refused or failed     —  not asked"
JOB_MAP = (("", "verbs", ("Open all", "Close all")), ("", "tree", "j02_prototype-p1-\nexample-questions_\ndata-data-v2", (
    ("", "Executive", "", ("X01 · What did the example find?", "X02 · What can this data not say?")),
    ("", "Data", "", ("D01 · What does the extract hold?", "D02 · Are the arms the size we expect?")),
    ("", "Information", "", ("I01 · How often in each arm?", "I02 · Does the rate move by day?")),
    ("", "Knowledge", "", ("K01 · Is the gap the same in both groups?",)),
    ("", "Wisdom", "", ("W01 · What should the next round keep?",)))))
JOB_R = (
    ("Overall", "The Overall Report, written last, and the pair this Job runs.", (
        ("", "big", "Overall Report · analysis plan 1 × data freeze 2", "moved: the data, from j01"),
        (S("1 · 📄 Overall Report", "2 of 2 written"), "sidetabs", OVERALL, OVERALL_PANEL),
        (S("2 · 🧷 This Job", "open"), "kv", (("plan", "analysis plan 1 · example questions"),
                                             ("freeze", "data freeze 2 · all sixteen days"), ("state", "open"),
                                             ("moved", "the data"), ("Job before", J1))))),
    ("Grid", "Every question × cut, by DIKW level: one dot a cell.", (
        ("", "big", "5 of 8 questions answered", "still to write: I01, I02, W01"),
        (S("1 · 🔲 Questions × cuts", "5 of 8 answered"), "dotgrid", DG_KEY, (
            ("Data", "2 of 2 answered", (("D01 extract-shape", "●————", "t01_D01 ↗", "checked"),
                                         ("D02 arm-balance", "●●●●—", "t02_D02 ↗", "checked"))),
            ("Information", "0 of 2 answered", (("I01 outcome-by-arm", "●●●○—", "waits on runs", "—"),
                                                ("I02 outcome-by-day", "●————", "↩ rewrite", "—"))),
            ("Knowledge", "1 of 1 answered", None), ("Wisdom", "0 of 1 answered", None),
            ("Executive", "2 of 2 answered", None))))),
    ("vs previous", "This Job against the one before: what changed.", (
        ("", "big", "Against j01: only the data moved", "so a changed answer has one cause"),
        (S("1 · 🔁 Per question", "4 changed"), "sidetabs",
         (("Executive", "1 changed"), ("Data", "1 changed"), ("Information", "1 changed"), ("Knowledge", "1 changed"),
          ("Wisdom", "not comparable")),
         (("tiles", (("2", "held"), ("4", "changed"), ("0 · 0", "new · dropped"), ("2", "not comparable"))),
          ("kv", (("may say", "the plain answer a leader asks for"),)),
          ("line", "X01  held · data moved (v1 → v2): the same finding on more rows"),
          ("kv", (("previous", "Arm B about 19 points above arm A …"), ("this", "Arm B about 15 points above arm A …"))),
          ("line", "X02  changed · data moved: it reports K01's verdict, which moved"),
          ("kv", (("", "vs-j01.md ↗, as the Job's run-compare wrote it"),)))))),
    ("MindMap", MAP_CAP, JOB_MAP),
)
JOB_REPORT = report("job", JOB_R)
JOB_WORK = work("job", JOB_R, {
    "Overall": ("Your sign and the close, the Overall Report to write, then the Report's Overall.", (
        (S("1 · 🔏 The plan and the close", "waits on the runs, the pages, the checks"), "todo",
         (("Sign the plan analysis plan 1", "signed in the Prototype", "✅ done 261106", ""),
          ("Close the Job", "once every page is checked", "waits on the checks", "Close"))),
        (S("2 · ✍️ Write the Overall Report", "done"), "todo",
         (("Write the Overall Report", "each Executive question's page from the answers below it", "✅ done", ""),)))),
    "Grid": ("The next act in each cell, then the grid, each cell its next verb.", (
        (S("1 · 🧮 Next in each cell", "1 to run"), "todo",
         (("Launch all", "one Run per question × cut, from the plan's thresholds", "1 to run", "Copy prompt"),
          ("Write all", "the next DIKW level first: I · Information", "3 to write", "Copy prompt"),
          ("Check all", "alignment and CHECK, by another agent", "2 to check", "Copy prompt"))),
        ("", "note", "⏳ running now · run-write-t06 ↗"))),
    "vs previous": ("Compare and propose, then each question against the Job before.", (
        (S("1 · 🔁 Compare, then propose", "done"), "todo",
         (("Compare with j01", "run-compare-j02 · every answer against j01", "✅ done", ""),
          ("Propose questions", "run-propose-j02 · each change or gap to the proposals", "✅ done", ""))),)),
    "MindMap": (MAP_CAP, ()),
})
JOB_STUDIO = (
    ("Topics", "", (
        ("", "trows", (("s02-why-answers-moved", "explore", "display", "j02 runs the same analysis plan on data freeze 2.",
                        STUDIO_VERBS, True),)),
        ("", "red", "✍️ Ask the agent", "agent", ("Copy prompt: talk and sketch",)))),
)

# ── the Task (s57 Report, s58 Work, s59 Studio) ──────────────────────────────────────────────────────────────────────
T_ONE = "Arm B's outcome rate is 15 points above arm A's on the whole extract,\nand B leads in every cut that could be read."
TASK_MAP = (("", "verbs", ("Open all", "Close all")), ("", "tree", "t03_I01_\noutcome-by-arm", (
    ("", "Runs", "one a cut, then the page", ("Run 1 · r01_full · the full cut", "Run 2 · the first group",
                                              "Run 3 · the second group", "Run 5 · r05_third · planned",
                                              "run-write-t03 · write the page")),)))
TASK_R = (
    ("Answer", "The answer, its evidence, how sure it is and what it rests on.", (
        (S("1 · ⚓ The answer", "partial"), "figthumbs", T_ONE, "rates by arm · full",
         ("gap · full", "rates · first", "gap · first", "rates · second", "gap · second"), "t03_I01_outcome-by-arm ↗"),
        (S("2 · 🎯 How sure", "not checked yet"), "kv",
         (("how sure", "Wilson intervals per arm; the gap's interval excludes zero on full"),
          ("rests on", "full ↗ · first ↗ · second ↗"))))),
    ("By cut", "Each cut this question runs on: its Run, its power, page and check.", (
        (S("1 · 🔲 Cut × step", "3 of 4 ran"), "table", ("cut", "Run", "power", "page", "check"),
         (("full", "✅ ok", "enough · sees 9 points", "to write", "to check"),
          ("first", "✅ ok", "enough · sees 12 points", "to write", "to check"),
          ("second", "✅ ok", "enough · sees 15 points", "to write", "to check"),
          ("third", "⏳ planned", "—", "—", "—"))),
        (S("2 · 📈 The full result", "ok"), "kv",
         (("", "Arm B 47% against arm A 32%: a gap of 15 points"), ("the numbers", "r01_full ↗ · 960 rows"))))),
    ("Across Jobs", "This question in every Job of the Board.", (
        (S("1 · 🔁 This question in each Job", "in 2 Jobs"), "table", ("Job", "answer", "status"),
         (("j01 · plan 1 × freeze 1", "B about 19 points above A", "✅ first"),
          ("j02 · plan 1 × freeze 2", "B about 15 points above A", "⏳ partial"))),)),
    ("Plan", "What the plan needs from this question, agreed before any Run.", (
        (S("1 · 📋 Needs", "agreed"), "kv",
         (("question", "how often does the outcome happen in each arm?"),
          ("need", "each arm's outcome rate, its 95% interval · rates_by_arm.csv"),
          ("", "the gap, B minus A, in points, its interval · gap.csv"),
          ("steps", "🧮 Compute"), ("may say", "rates and contrasts, never \"because\""), ("agreed", "✅ 261106"))),)),
    ("MindMap", MAP_CAP, TASK_MAP),
)
TASK_REPORT = report("task", TASK_R)
TASK_WORK = work("task", TASK_R, {
    "Answer": ("The chain of roles, one verb live on the next link, then the answer.", (
        (S("1 · 🔗 The chain", "next: run every cut"), "todo",
         (("Plan the evidence", "writer · in the Prototype, before any Run", "✅ done", ""),
          ("Agree the plan", "checker · another agent agrees the needs", "✅ done", ""),
          ("Run every cut", "the scripts · one Run per cut, from the plan", "ready", "Copy prompt"),
          ("Write the page", "writer · from the Runs' results", "to do", ""),
          ("Check the page", "checker · in a fresh context", "to do", ""),
          ("Check the alignment", "checker · each cell against its question", "to do", ""))),)),
    "By cut": ("The next act on each cut, then each cut's Run, power, page and check.", (
        (S("1 · 🔲 Next on each cut", "ready"), "todo", (("Run the third cut", "r05_third", "ready", "Copy prompt"),)),
        (S("2 · ✂️ A new cut", "ready"), "todo",
         (("Propose a cut to the next plan", "a cut is plan, fixed before any outcome", "ready", "Copy prompt"),)))),
    "Across Jobs": ("Track this question across the Jobs, then its answer in each.", (
        (S("1 · 🔁 Track", "ready"), "todo", (("Track I01 across the Jobs", "its answer Job by Job", "ready", "Copy prompt"),)),)),
    "Plan": ("The plan's steps, then what it needs.", (
        (S("1 · 📋 The plan", "done"), "todo", (("Plan the evidence", "in the Prototype, before any Run", "✅ done", ""),
                                               ("Agree the plan", "another agent", "✅ done 261106", ""))),)),
    "MindMap": (MAP_CAP, ()),
})
TASK_STUDIO = (
    ("Topics", "", (
        ("", "empty", "No Studio topic here yet.", "Add a topic"),
        ("", "red", "✍️ Ask the agent", "agent", ("Copy prompt: talk and sketch",)))),
)

CLOSED = ("every section starts closed (▸), its state word on its right, a waiting line under one that waits on you; "
          "what it opens to is drawn under its bar, behind a dashed line")
OWN = "🙋 Interaction is every view's last section and holds its own forms; no view starts with a Waits-on-you section"
RAIL = "the right rail: Report · Work · Studio · Interactions · Delivery · Timeline · Skills · Files, as served 261106"
VIEWS = {   # (level, section): (the line above the screens, the views, the open question)
    ("block", "report"): ("Answers · Questions · Jobs · Data · Handoff · MindMap, as the live page draws them (261106); " + CLOSED + ";\n"
                          + OWN + "; " + RAIL, BLOCK_REPORT, "? agree A to F: they\nfollow the live page"),
    ("block", "work"): ("the same views as Report: ⚙️ Process when it has a step, then 📊 Results by the same code; " + CLOSED + ";\n"
                        + OWN + "; " + RAIL, BLOCK_WORK, "? Process before Results\non every view, as live"),
    ("block", "studio"): ("one view, Topics: the Board's topics and its Jobs', flat rows as live; red: the groups by Tag and Ask the\n"
                          "agent, reviewed designs no later ask overruled, kept as proposals; " + RAIL, BLOCK_STUDIO,
                          "? groups by Tag and\nAsk the agent (red)"),
    ("job", "report"): ("Overall · Grid · vs previous · MindMap (vs previous hidden on a first Job), as live; " + CLOSED + ";\n"
                        + OWN + "; " + RAIL, JOB_REPORT, "? agree A to D: they\nfollow the live page"),
    ("job", "work"): ("the same views as Report: ⚙️ Process when it has a step, then 📊 Results by the same code; " + CLOSED + ";\n"
                      + OWN + "; " + RAIL, JOB_WORK, "? Close stays greyed\nuntil every check"),
    ("job", "studio"): ("one view, Topics: this Job's own topics, flat rows as live; red: Ask the agent, kept as a proposal;\n" + RAIL,
                        JOB_STUDIO, "? Ask the agent\nhere too (red)"),
    ("task", "report"): ("Answer · By cut · Across Jobs · Plan · MindMap, read only, as live; its goal-line the question's Aim; " + CLOSED
                         + ";\n" + OWN + "; " + RAIL, TASK_REPORT, "? agree A to E: they\nfollow the live page"),
    ("task", "work"): ("the same views as Report: ⚙️ Process when it has a step, then 📊 Results by the same code; " + CLOSED + ";\n"
                       + OWN + "; " + RAIL, TASK_WORK, "? the chain as rows,\nits roles in each line"),
    ("task", "studio"): ("one view, Topics: a Task with no topic says so, with Add a topic (asked 261106); red: Ask the agent, kept;\n"
                         + RAIL, TASK_STUDIO, "? Ask the agent\nbeside Add a topic (red)"),
}
# what changed on each letter's screen: its green ✎ notes under its letter, dated, and listed under the screens
D6 = "261106"
NOTES = {
    ("block", "report"): {"A": [(D6, "new first: the answers, one line each"), (D6, "Overall Report: side tabs, one question open"),
                                (D6, "each level's findings as a side tab"), (D6, "no Waits-on-you; 🙋 Interaction last")],
                          "B": [(D6, "canvas, then each question and its answer"), (D6, "the plans as side tabs, proposals a tab"),
                                (D6, "each bar its state word")],
                          "C": [(D6, "Each Job: a dot row per DIKW level"), (D6, "the newest Job · its Tasks, by level"),
                                (D6, "🙋 holds Pooling on freeze two: 2 wait")],
                          "D": [(D6, "each freeze a card of key numbers"), (D6, "its files one click away, a few rows"),
                                (D6, "cuts with their power floor")],
                          "E": [(D6, "a line per Wisdom draft, then the draft"), (D6, "the signed handoffs; 🙋 answered")],
                          "F": [(D6, "new: MindMap, the drawing and each Job"), (D6, "🙋 Interaction, unnumbered")]},
    ("block", "work"): {"A": [(D6, "no Waits-on-you section first"), (D6, "⚙️ the Overall Report: done"),
                              (D6, "📊 Results = the Report's A")],
                        "B": [(D6, "the next plan: 2 wait, its line under"), (D6, "❓ New questions: Copy prompt")],
                        "C": [(D6, "🪜 each Job's steps: j02 next: run"), (D6, "➕ a new Job; 🙋 2 wait for you")],
                        "D": [(D6, "🗄 a new freeze or cut: 2 ready")],
                        "E": [(D6, "🤝 sign the handoff W01: waits for you")],
                        "F": [(D6, "new: MindMap, Results only, no Process")]},
    ("block", "studio"): {"A": [(D6, "one view, Topics: flat rows as live"), (D6, "a row: stage, kind, its line, its verbs"),
                                (D6, "s02's row: 🙋 Interaction, its form waits"), (D6, "red: groups by Tag, Ask the agent")]},
    ("job", "report"): {"A": [(D6, "Overall Report: side tabs, one question open"), (D6, "This Job: plan, freeze, what moved")],
                        "B": [(D6, "one dot a cell, folded by DIKW level"), (D6, "page and check columns; 🙋 2 wait")],
                        "C": [(D6, "per question, a side tab per level"), (D6, "shown from the second Job on")],
                        "D": [(D6, "new: MindMap, Tasks by DIKW level"), (D6, "each leaf the Task's question")]},
    ("job", "work"): {"A": [(D6, "🔏 your sign and the close, in Process"), (D6, "no Waits-on-you section first")],
                      "B": [(D6, "🧮 launch, write, check all; 🙋 2 wait")],
                      "C": [(D6, "🔁 compare, then propose: done")],
                      "D": [(D6, "new: MindMap, Results only")]},
    ("job", "studio"): {"A": [(D6, "one view, Topics: this Job's s02, as live"), (D6, "red: Ask the agent, kept")]},
    ("task", "report"): {"A": [(D6, "goal-line: Aim · I01"), (D6, "the first figure large, the others small"),
                               (D6, "how sure and what it rests on")],
                         "B": [(D6, "a power column per cut"), (D6, "the full result, its numbers")],
                         "C": [(D6, "the answer in each Job, its status")],
                         "D": [(D6, "needs: need, steps, may say, agreed")],
                         "E": [(D6, "new: MindMap, a Run per cut")]},
    ("task", "work"): {"A": [(D6, "🔗 the chain of roles: run every cut next"), (D6, "no Waits-on-you section first")],
                       "B": [(D6, "🔲 the third cut to run, ✂️ a new cut")],
                       "C": [(D6, "🔁 Track: ready")],
                       "D": [(D6, "📋 the plan: done")],
                       "E": [(D6, "new: MindMap, Results only")]},
    ("task", "studio"): {"A": [(D6, "no topic here yet: Add a topic"), (D6, "red: Ask the agent, kept")]},
}
PIECE = {   # the why notes: what the live focus page showed when the cell was opened (261101)
    ("block", "report"): ("the Board's Report: its answers, questions, Jobs, data, handoff, map",
                          ["Report shows only\nMindMap and Status", "no answer is shown\non the Board",
                           "the answers live on the\nold insight-board page"]),
    ("block", "work"): ("the Board's Work: Process, then the Report's views",
                        ["each Job says \"no\nstate recorded\"", "no button signs a plan\nor closes a Job",
                         "proposals have no\nplace on screen"]),
    ("block", "studio"): ("the Board's Studio: its topics",
                          ["no Studio section on\nthe focus page", "the Board has no\nstudio/ folder", "topics sit only\nin b11"]),
    ("job", "report"): ("a Job's Report: the Overall Report, the grid, what changed, its map",
                        ["Tasks are listed flat,\nt01 to t20", "no question × cut\ngrid", "the Overall Report\nis not shown"]),
    ("job", "work"): ("a Job's Work: Process, then the Report's views",
                      ["every Task says \"no\nstate recorded\"", "no sign or close\nbutton", "what moved is only\nin the Job's face"]),
    ("job", "studio"): ("a Job's Studio: its own topics",
                        ["no Studio section", "no topic names\na Job", "no talk-and-sketch\nprompt here"]),
    ("task", "report"): ("a Task's Report: the answer, each cut, other Jobs, the plan, its map",
                         ["Report lists Runs:\nr01_full, run-write", "the answer sits in the\nface, never shown",
                          "gates hid in the old\nCheck Space"]),
    ("task", "work"): ("a Task's Work: Process, then the Report's views",
                       ["Runs show ok or\nplanned, no verbs", "the evidence plan\nhas no place", "no chain shows\nwhat comes next"]),
    ("task", "studio"): ("a Task's Studio: its own topics, or none yet",
                         ["Studio was not\na section", "no topic names\nthe Task", "the prompt had\nno home"]),
}
TARGET = {"block": "servers/workbench-insight/insight_theme.py · workbench-insight/SKILL.md",
          "job": "servers/workbench-insight/insight_theme.py · workbench-insight/SKILL.md",
          "task": "servers/workbench-insight/insight_views.py · workbench-insight/SKILL.md"}

AGREED = {}                            # (level, section): {letter: sections}, the letters settled so far; none yet
MOCK = """<!doctype html><meta charset=utf-8><title>{letter} · {view}</title>
<!-- GENERATED by insight_ui_cells.py from AGREED; the agreed screen of {nn} view {letter} -->
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


def screen_h(items, level):
    return 214 + (30 if PAGE[level][2] else 0) + max(tall(secs) for _, _, secs in items)


NOTE_H = 20                          # one green note's line under a letter


def notes_top(notes, letters):
    """Where the screens start under their letters: the letter, then the most notes any of them carries."""
    return 40 + NOTE_H * max([len(notes.get(L, ())) for L in letters] + [0])


def letter_notes(eid, x, y, notes):
    """A letter's green ✎ notes, one a line under it, each with its own date (canvas.change_note)."""
    return [change_note(x + 4, y + 34 + NOTE_H * j, what, date, None, 14) for j, (date, what) in enumerate(notes)]


def screens(eid, x, y, items, level, section, notes=None, gap=40):
    """Every view lettered A, B, C …, every screen the same size (the tallest view's), three a row; a letter whose
    screen changed carries its green ✎ notes under its name, dated."""
    notes = notes or {}
    cols, h = min(3, len(items)), screen_h(items, level)
    views = tuple(v for v, _, _ in items)
    top = notes_top(notes, LETTERS[:len(items)])
    els = []
    for k, (view, caption, secs) in enumerate(items):
        sx, sy = x + (k % cols) * (W + gap), y + (k // cols) * (h + top + gap)
        els += text(f"{eid}{k}_L", sx, sy, f"{LETTERS[k]} · {view}", 22, TITLE)
        els += letter_notes(f"{eid}{k}_n", sx, sy, notes.get(LETTERS[k], ()))
        els += screen(f"{eid}{k}", sx, sy + top, h, level, section, views, k, secs, caption)
    return els, y + ((len(items) + cols - 1) // cols) * (h + top + gap)


def flat(sec):
    """(title, one line) of a section, for the agreed screen file."""
    if sec[0] in ("rule", "group"):
        return (sec[1], "") if sec[0] == "group" else ("", "")
    if sec[1] in ("none", "red", "redline"):
        return bar_of(sec[0])["t"] or (sec[2] if sec[1] != "none" else ""), "proposal" if sec[1] != "none" else ""
    words = {"tree": lambda: " · ".join(b[1] for b in sec[3]), "sidetabs": lambda: " · ".join(h for h, _ in sec[2]),
             "todo": lambda: " · ".join(r[0] for r in sec[2]), "trows": lambda: " · ".join(r[0] for r in sec[2]),
             "answers": lambda: " · ".join(i for i, _ in sec[2]), "levels": lambda: " · ".join(n for n, _, _ in sec[2]),
             "verbs": lambda: " · ".join(sec[2])}.get(sec[1], lambda: str(sec[2]))()
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


# ── s51's two sketches, kept from round 3 (asked 261102): the plan × freeze matrix, and the question canvas ─────────
MX_PLANS = ("analysis plan 1\nfirst ladder", "analysis plan 2\nadds events")
MX_FREEZES = ("data freeze 1\nfirst window", "data freeze 2\nwhole record", "data freeze 3\nnew rows")
MX_JOBS = {(0, 0): ("j01", "closed", 40, 40, "XDIKW"), (0, 1): ("j02", "closed", 40, 40, "XDIKW"),
           (1, 1): ("j03", "open · a preview", 31, 44, "DIK")}       # (id, state, pages written, pages, levels done)


def matrix_sketch(x, y):
    """A · Answers holds the matrix (drawn by hand on s51: plans down, freezes across; "more active, and vivid"): one
    cell a Job, alive: its pages as a bar, its levels X D I K W as a strip, the newest marked; arrows between Jobs say
    which clock moved; the next Job is the empty cell, outlined. -> (els, bottom)."""
    RW, CWD, CHT, HH = 300, 440, 170, 100
    els = text("mxH", x, y, "A · Answers holds the matrix: analysis plans down, data freezes across", 34, TITLE)
    els += text("mxS", x, y + 52, "one cell is one Job, alive: how far it got, which levels are answered, which clock it moved", 20, BODY)
    els += [change_note(x + 1600, y + 6, "the plan × freeze matrix first, as drawn by hand on s51; each cell alive", "261102", None)]
    top, left = y + 130, x + RW
    for k, words in enumerate(MX_FREEZES):
        els += text(f"mxF{k}", left + k * CWD + 24, top + 20, words, 22, TITLE)
    for r, words in enumerate(MX_PLANS):
        els += text(f"mxP{r}", x + 10, top + HH + r * CHT + 50, words, 22, TITLE)
    els += line("mxAx", [(left - 10, top + HH - 8), (left + 3 * CWD + 10, top + HH - 8)], INK, 4)
    els += line("mxAy", [(left - 10, top + HH - 8), (left - 10, top + HH + 2 * CHT + 10)], INK, 4)
    cell_ = {}
    for r in range(2):
        for k in range(3):
            cx, cy, w, h = left + k * CWD + 12, top + HH + r * CHT + 10, CWD - 40, CHT - 30
            cell_[(r, k)] = (cx, cy, w, h)
            job = MX_JOBS.get((r, k))
            if not job:
                nxt = (r, k) == (1, 2)
                els += box(f"mxC{r}{k}", cx, cy, w, h, "+ Add a Job\nanalysis plan 2 × data freeze 3" if nxt else
                           ("+ Add a Job" if k == 2 else "not run"), "plain", 18, dashed=True)
                els[-2]["backgroundColor"], els[-2]["strokeWidth"] = "#ffffff", 3 if nxt else 1
                continue
            jid, state, done, of, lv = job
            els += box(f"mxC{r}{k}", cx, cy, w, h, "", "plain")
            els[-1]["strokeWidth"] = 4 if state.startswith("open") else 2
            els += text(f"mxC{r}{k}_j", cx + 20, cy + 14, f"{jid} · {state}", 22, TITLE)
            bw = w - 40                                                    # pages written, as a bar
            els += box(f"mxC{r}{k}_bar", cx + 20, cy + 56, bw, 16, "", "plain")
            els[-1]["backgroundColor"] = "#ffffff"
            els += box(f"mxC{r}{k}_fill", cx + 20, cy + 56, bw * done / of, 16, "", "plain")
            els[-1]["backgroundColor"], els[-1]["fillStyle"] = "#1e3a5f", "solid"
            els += text(f"mxC{r}{k}_n", cx + 20, cy + 78, f"{done} of {of} pages written", 16, BODY)
            for i, L in enumerate("XDIKW"):                                # the levels strip
                els += box(f"mxC{r}{k}_l{L}", cx + 20 + i * 44, cy + 104, 38, 26, L, "plain", 15)
                if L in lv:
                    els[-2]["backgroundColor"], els[-2]["fillStyle"], els[-1]["strokeColor"] = "#1e3a5f", "solid", "#ffffff"
                else:
                    els[-2]["backgroundColor"] = "#ffffff"
            if state.startswith("open"):
                els += sticky("mxNew", cx + w - 40, cy + h - 6, 150, 44, "newest", 18, 0.06)
    (ax, ay, aw, ah), (bx, by, bw_, bh) = cell_[(0, 0)], cell_[(0, 1)]
    els += arrow("mxM1", [(ax + aw + 4, ay + 40), (bx - 4, by + 40)], INK, "moved the data", width=3, at=(ax + aw - 50, ay - 50))
    (cx_, cy_, cw_, ch_) = cell_[(1, 1)]
    els += arrow("mxM2", [(bx + bw_ / 2, by + bh + 4), (cx_ + cw_ / 2, cy_ - 4)], INK, "moved the code", width=3,
                 at=(bx + bw_ / 2 + 16, by + bh + 2))
    (nx, ny, nw, nh) = cell_[(1, 2)]
    els += arrow("mxNext", [(cx_ + cw_ + 4, cy_ + ch_ / 2), (nx - 4, ny + nh / 2)], INK, "next", width=3, dashed=True,
                 at=(cx_ + cw_ + 2, cy_ + ch_ / 2 - 30))
    end = top + HH + 2 * CHT + 20
    els += arrow("mxData", [(left + 20, end + 30), (left + 3 * CWD - 40, end + 30)], INK, "a new data freeze: the data clock",
                 width=3, at=(left + 3 * CWD / 2 - 180, end + 44))
    els += arrow("mxCode", [(left + 3 * CWD + 40, top + HH + 10), (left + 3 * CWD + 40, top + HH + 2 * CHT - 10)], INK,
                 "a new plan:\nthe code clock", width=3, at=(left + 3 * CWD + 60, top + HH + CHT - 30))
    notes = ("click a cell: that Job's Overall Report", "hover a level: its questions, written or not")
    for k, words in enumerate(notes):
        els += sticky(f"mxN{k}", left + 3 * CWD + 380, top + 120 + k * 120, 380, 80, words, 17, (-0.02, 0.02)[k])
    els += text("mxUnder", x, end + 100, "on the same view: ⚓ the answers one line each, 📄 the Overall Report as side tabs, "
                "🔎 what each question found", 20, BODY)
    els += [change_note(x, end + 136, "live 261106: the answers come first, the matrix is section 2, as a table", "261106", None)]
    return els, end + 190


QC_X = ("X01\noverall", "X02\nbest-time", "X03\nwho-differs", "X04\nlimits")
QC_COLS = (("DATA", ("D01\nextract-and-clock", "D02\ngaps", "D03\nmeal-log", "D04\ndevices")),
           ("INFORMATION", ("I01\nglucose-control", "I03\nhour-curve", "I02\ntime-in-range", "I05\nmeals", "I06\nevent-locked")),
           ("KNOWLEDGE", ("K01\ncontrol-and-timing", "K02\nawake-asleep", "K05\npooling", "K03\nmeal-response", "K04\nevent-effect")),
           ("WISDOM", ("W01\nfirst-focus", "W02\nnext-focus")))
QC_CITES = {"X01": ("D01", "I01", "K01"), "X02": ("K01", "I03"), "X03": ("K02", "K05"), "X04": ("D02", "K05"),
            "W01": ("K01", "K03"), "W02": ("K04", "K02"), "K01": ("I01", "I03"), "K02": ("I02", "I03"),
            "K03": ("I05", "D03"), "K04": ("I06",), "K05": ("K02", "I02"), "I01": ("D01",), "I02": ("D01", "D02"),
            "I03": ("D01",), "I05": ("D03",), "I06": ("D03", "D04")}
QC_PIN = "K01"


def _down(q, seen=None):
    seen = set() if seen is None else seen
    for c in QC_CITES.get(q, ()):
        if c not in seen:
            seen.add(c)
            _down(c, seen)
    return seen


def _up(q):
    out, todo = set(), [q]
    while todo:
        k = todo.pop()
        for a, cs in QC_CITES.items():
            if k in cs and a not in out:
                out.add(a)
                todo.append(a)
    return out


def canvas_sketch(x, y):
    """The question canvas as the page draws it, K01 pinned (asked 261102: "should we start from the Executive, and the
    Data, and then I, K, W"): Executive as a row on top; under it a column per level, Data → Information → Knowledge →
    Wisdom, so the evidence builds left to right. What K01 rests on in solid lines, what uses it dashed, every other
    card faded; its panel on the right; how to use it in notes. -> (els, bottom)."""
    CWD, CHT, GY, COLW, GAP = 250, 64, 18, 290, 110
    down, up = _down(QC_PIN), _up(QC_PIN)
    lit = lambda q: q == QC_PIN or q in down or q in up
    els = text("qcH", x, y, "B · Questions opens on a canvas: Executive first, then the evidence, Data → Wisdom", 34, TITLE)
    els += text("qcS", x, y + 52, "one card a question; one line a citation in its evidence plan; it builds left to right", 20, BODY)
    els += [change_note(x + 1700, y + 6, "Executive on top, then D → I → K → W left to right", "261102", None)]
    bar_y = y + 100
    els += box("qcFind", x, bar_y, 300, 44, "find  K01, timing …", "plain", 16)
    els += text("qcOnly", x + 330, bar_y + 10, "☐ Only linked     ▢ page written   ▢ drafted   ▢ not yet", 16, BODY)
    pos = {}
    width = 4 * COLW + 3 * GAP
    xt = bar_y + 80                                                      # the Executive row
    els += box("qcBX", x, xt, width, CHT + 70, "", "plain")
    els[-1]["backgroundColor"], els[-1]["fillStyle"], els[-1]["strokeWidth"] = "#e7f0fb", "solid", 2
    els += text("qcBXt", x + 20, xt + 14, "EXECUTIVE · what a leader reads first", 18, TITLE)

    def card(q, words, cx, cy):
        pos[q] = (cx, cy)
        out = box(f"qcC{q}", cx, cy, CWD, CHT, words, "plain", 17)
        out[0]["strokeWidth"] = 5 if q == QC_PIN else 3 if lit(q) else 1
        if not lit(q):
            out[0]["strokeColor"], out[0]["backgroundColor"], out[1]["strokeColor"] = "#ced4da", "#ffffff", "#adb5bd"
        return out
    step = (width - 40) / len(QC_X)
    for k, words in enumerate(QC_X):
        els += card(words.split("\n")[0], words, x + 20 + k * step, xt + 48)
    ct = xt + CHT + 110
    bottom = ct
    for c, (name, cards) in enumerate(QC_COLS):
        cx = x + c * (COLW + GAP)
        h = 60 + len(cards) * (CHT + GY)
        els += box(f"qcB{c}", cx, ct, COLW, h, "", "plain")
        els[-1]["backgroundColor"], els[-1]["fillStyle"], els[-1]["strokeWidth"] = "#f1f3f5", "solid", 1
        els += text(f"qcBt{c}", cx + 18, ct + 16, f"{name} · {len(cards)}", 18, BODY)
        for i, words in enumerate(cards):
            els += card(words.split("\n")[0], words, cx + 20, ct + 50 + i * (CHT + GY))
        if c < 3:
            els += arrow(f"qcFlow{c}", [(cx + COLW + 18, ct + 24), (cx + COLW + GAP - 18, ct + 24)], INK, width=4)
        bottom = max(bottom, ct + h)
    for a, cs in QC_CITES.items():
        for c in cs:
            (ax, ay), (bx, by) = pos[a], pos[c]
            if a[0] == "X":
                p0, p1 = (ax + CWD / 2, ay + CHT), (bx + CWD / 2, by)
            elif a[0] == c[0]:
                p0, p1 = (ax + CWD, ay + CHT / 2), (bx + CWD, by + CHT / 2)
            else:
                p0, p1 = (bx + CWD, by + CHT / 2), (ax, ay + CHT / 2)        # from the evidence to what it builds
            pts = [p0, (p0[0] + 40, (p0[1] + p1[1]) / 2), p1] if a[0] == c[0] else [p0, p1]
            if a == QC_PIN or (a in down and c in down):
                els += arrow(f"qcE{a}{c}", pts, INK, width=3)
            elif (c == QC_PIN or c in up) and a in up:
                els += arrow(f"qcE{a}{c}", pts, INK, width=3, dashed=True)
            else:
                els += line(f"qcE{a}{c}", pts, "#dee2e6", 1)
    px, py = x + width + 80, bar_y + 80                                   # the pinned question's panel
    els += box("qcP", px, py, 560, 330, "", "plain")
    els[-1]["strokeWidth"] = 2
    els += text("qcPt", px + 24, py + 20, "K01 · control-and-timing", 24, TITLE)
    els += text("qcPq", px + 24, py + 62, "does control depend on the hour of the day?", 18, INK)
    els += text("qcPs", px + 24, py + 96, "page: written  ·  open its Task ↗", 16, BODY)
    els += text("qcPr", px + 24, py + 140, "Rests on  (to its left)", 18, TITLE)
    els += text("qcPc1", px + 24, py + 172, "( I01 )  ( I03 )  ( D01 )", 18, INK)
    els += text("qcPu", px + 24, py + 220, "Used by  (to its right, and above)", 18, TITLE)
    els += text("qcPc2", px + 24, py + 252, "( W01 )  ( X01 )  ( X02 )", 18, INK)
    notes = ("hover a card: solid lines, what it rests on,\nall the way down; dashed, what uses it",
             "click pins it; click a chip to walk\nto that question",
             "a link ending #q=K01 opens it pinned",
             "every other card fades; the questions with\nno line hide under Only linked")
    for k, words in enumerate(notes):
        els += sticky(f"qcN{k}", px + 280, py + 420 + k * 120, 520, 92, words, 17, (-0.02, 0.015, -0.01, 0.02)[k])
    return els, max(bottom, py + 420 + 4 * 120) + 40


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
    pieces.append(("book", f"skill/{sk.name}", "the views' manual, for workbench-insight", sk.exists()))
    spec = {"title": f"{level.capitalize()} UI · {VERB[section]}: {piece.split(': ', 1)[1]}",
            "why": {"question": f"why do we need s{nn}?", "notes": why,
                    "quote": "asked 261106: match each screen to the live, aligned insight pages"},
            "what": {"head": f"② what s{nn} hands over: one screen, A to {last}", "icon": "page", "name": "delivery/ui/",
                     "type": "ui", "deck_why": f"stays in s{nn}'s delivery/deck/, so anyone gets it in a minute", "parts": pieces},
            "job": topic.parent.parent,
            "target": TARGET[level],
            "missing": [(name, "not settled yet") for _, name, _, done in pieces if not done],
            "have": [(name, "agreed") for icon, name, _, done in pieces if done and icon == "page"]}
    notes = NOTES.get((level, section), {})

    def design():                                    # A, B, C … every view the same screen; s51 keeps its two sketches
        els = text("skA", 690, 280, f"A to {last} · {piece}, every view the same screen", 18, TITLE)
        els += text("lay", 690, 330, lay, 16, BODY)
        y = 356 + 20 * (lay.count("\n") + 1)
        if (level, section) == ("block", "report"):   # round 3's matrix and canvas, kept; then the screens
            mx, y = matrix_sketch(690, y)
            els += mx
            qc, y = canvas_sketch(690, y + 60)
            els += qc
            els += text("rowH", 690, y + 30, f"A to {last} · every view of the Board's Report, as served 261106", 26, TITLE)
            y += 90
        e, bottom = screens("sc", 690, y, items, level, section, notes)
        listed = [(L, d, w) for L in LETTERS for d, w in notes.get(L, ())]   # every changed screen's notes, in one place
        els += text("chgH", 690, bottom + 10, "What changed", 16, TITLE) if listed else []
        for j, (L, d, w) in enumerate(listed):
            els += [change_note(690, bottom + 40 + 22 * j, f"{L}: {w}", d, None, 14)]
        return els + e + sticky("askD", 1480, bottom + 60, 320, 76, ask, 15, -0.03, RED, RE)

    return five_parts.build(topic, spec, design, shift=(W + 40) * min(3, len(items)) - 300 + (240 if len(items) == 1 else 0),
                            writer=five_parts.marks_writer)   # the person's canvas marks stay


def letter_png(topic: Path, letter: str, out: Path, scale: float = 1.0, drawing: Path = None) -> Path:
    """One letter's screen alone, for a Design loop review (haipipe-ui, stage 1): <out>.png, drawn from
    <out>.excalidraw (or `drawing`)."""
    import subprocess
    topic = Path(topic).resolve()
    _, level, section = cell(topic)
    items = VIEWS[(level, section)][1]
    k = LETTERS.index(letter)
    view, caption, secs = items[k]
    views = tuple(v for v, _, _ in items)
    els = text("L", 0, 0, f"{letter} · {view}", 22, TITLE) + screen("one", 0, 40, screen_h(items, level), level, section,
                                                                     views, k, secs, caption)
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    drawing = Path(drawing) if drawing else out.with_suffix(".excalidraw")
    drawing.parent.mkdir(parents=True, exist_ok=True)
    five_parts.write(drawing, els)
    render = TOOLS / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts/render_png.py"
    subprocess.run(["uv", "run", "--no-project", "-q", "--with", "pillow", "python", str(render), str(drawing),
                    str(out.with_suffix(".png")), str(scale)], check=True, stdout=subprocess.DEVNULL)
    return out.with_suffix(".png")


if __name__ == "__main__":                               # python insight_ui_cells.py <topic folder> <letter> <out>
    print(letter_png(Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])))
