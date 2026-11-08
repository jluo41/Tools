"""The nine sNN of b13 j01 · The cowork pages, level by level: one per level (Block, Job, Task) and section (Report,
Work, Studio), each drawn in haipipe-studio's five parts (scripts/five_parts.py). Copied from b11's
insight_ui_cells.py and b17's work_ui_cells.py. Each sNN's builder is `build(Path(__file__).parent)`: its cell is
found by its folder name (s51-block-ui-report → block, report).

A cell's Design is its page's views, lettered A, B, C …, each drawn as the same full screen (haipipe-ui, "one view,
one screen"): the window, both rails as pale short lines, the path, the title-&-section, the view-button-list with this
view in orange, the goal-line (a Block's Purpose, a Job's Goal, a Task's Aim, its label small and a rule under it),
the view-caption, then the view's sections as numbered heading bars, closed (▸) as the live page starts them, each
with its state word on its right and, when it waits on the person, its waiting line under the bar; what a bar opens to
is drawn under it as what it is (side tabs, flush rows, a Job with its newest entries, a map). 🙋 Interaction is the
last section of every Report and Work view and holds that view's own forms; Work has the same views as Report, ⚙️
Process first when it has a step, then 📊 Results drawn by the same code. Studio is one view, Topics, at every level;
a page with no topic says so and offers Add a topic. The right rail ends Skills · Files.

Drawn 261108 from the live cowork pages (servers/workbench-cowork, as served on 261108; asked 261108: give the cowork
theme Block its UI drawings, the 3 × 3 the paper, work, labeling and insight Blocks have, drawn from the live cowork
pages): Block and Job MindMap · Status · Findings, a Task MindMap · Status. Findings holds the cowork parts no other
theme has: 👥 People, ✉️ Messages and ⏳ Next move. A Job and a Task have no ⚙️ Process today, so their Work is Results
only; where a step is plainly missing, it is drawn red, marked "proposal" (S(..., red=True), "redline"). Every new
screen carries its dated green ✎ notes under its letter, listed again under the screens (NOTES). The drawing is
written by five_parts.marks_writer, so a person's marks on the canvas stay.

The example is the theme's own public example, cowork/b01_example_data_request (a placeholder data request to a
partner office and the review board amendment it needs; every role, date and number is made up): a Block is one topic
coordinated with people; a Job is one line of work (j01 waits on them, j02 on us); a Task is one document written in
rounds. Tools is public, so nothing from a private Block is drawn.

    python cowork_ui_cells.py <topic folder> <letter> <out>     one letter's screen alone, for a review round
"""
import re
import sys
import textwrap
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = next(p for p in HERE.parents if (p / "plugins/haipipe-toolkit").is_dir())
sys.path.insert(0, str(TOOLS / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))
from five_parts import *  # noqa: E402,F401,F403  (the helpers and build())
from five_parts import _el  # noqa: E402
from canvas import change_note  # noqa: E402
import five_parts  # noqa: E402

VERB = {"report": "Report", "work": "Work", "studio": "Studio"}
LETTERS = "ABCDEFGH"
W, CW, X0 = 780, 640, 70             # a screen, its content column, where the column starts (the rails are short lines)
BLUE = "#1864ab"                     # the workbench's colour for the current thing
PALE = "#dee2e6"
RULE = "#e9ecef"

# ── the example: the theme's public cowork example, as the live pages show it ──────────────────────────────────────
SPACE = "<SPACE> / Tools / blueprints / Project-Ladder / cowork"
BLOCK, JOB, TJOB, TASK = ("b01_example_data_request", "j01_data_access_request", "j02_review_board_amendment",
                          "t01_data_use_plan")
PURPOSE = ("A placeholder request for a data extract from a partner office, and the review board amendment it needs; "
           "every role, date and number is made up.")
GOAL = "The partner office sends the extract with every field on the request's list."
AIM = "The data-use plan the review board reads with the amendment, written with the review board contact in rounds."
PAGE = {"block": (BLOCK, f"{SPACE} / {BLOCK}", ("PURPOSE", PURPOSE)),
        "job": (JOB, f"{SPACE} / {BLOCK} / {JOB}", ("GOAL", GOAL)),
        "task": (TASK, f"{SPACE} / {BLOCK} / {TJOB} / {TASK}", ("AIM", AIM))}
LEFT = {"block": (0, 5, 1), "job": (1, 4, 99), "task": (0, 2, 1)}   # this page's line, how many, the first child line
RIGHT = {"block": ("Report", "Work", "Studio", "Interactions", "Delivery", "Timeline", "Skills", "Files"),
         "job": ("Report", "Work", "Studio", "Interactions", "Delivery", "Skills", "Files"),   # no Timeline on a Job
         "task": ("Report", "Work", "Studio", "Interactions", "Delivery", "Timeline", "Skills", "Files")}


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
    for k, s in enumerate(RIGHT[level]):
        els += line(f"{eid}_r{k}", [(x + W - 40, y + 50 + 12 * k), (x + W - 16, y + 50 + 12 * k)],
                    OR if s == VERB[section] else PALE, 2)
    return els


def head(eid, x, y, name, section, views, on=0):
    """The title-&-section, then the view-button-list, the open view in orange."""
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
    for part_ in words.split(" / "):
        nxt = part_ if not cur else cur + " / " + part_
        if len(nxt) > width and cur:
            out.append(cur + " /")
            cur = part_
        else:
            cur = nxt
    return out + [cur]


def goal_lines(level):
    return textwrap.wrap(PAGE[level][2][1], 88)


def goal_h(level):
    """How much the goal-line adds under the view-button-list: its label, its lines, the rule."""
    return 26 + 18 * len(goal_lines(level))


WAITS = re.compile(r"waits?( for| on) you|waiting for you|needs your|your sign|your call|your agreement")


def waits_on_you(word):
    return word.startswith("🙋") or bool(WAITS.search(word))


def state_color(word):
    """A state word's colour, as live: orange only when it waits on the person; green done; blue running or next."""
    w = word.lstrip("🙋✅⏳⬜☑ ")
    if waits_on_you(word):
        return OR
    if word.startswith("✅") or w.startswith(("done", "agreed", "answered", "applied", "sent")):
        return GR
    if word.startswith("⏳") or w.startswith(("running", "next", "in progress")):
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


# ── a section's content, drawn as what it is ──────────────────────────────────────────────────────────────────────
def k_note(eid, x, y, w, words):
    """A small plain line: what a band's view repeats."""
    return text(eid, x + 2, y, words, 11, BODY)


def k_state(eid, x, y, w, words):
    """A Job's state over its sections, as live (🟡 Active): one word, a size up."""
    return text(eid, x + 2, y, words, 15, TITLE)


def k_kv(eid, x, y, w, rows):
    """Label and value rows; a row with no label is a full line (the sentence a section opens with)."""
    els = []
    for k, (key, val) in enumerate(rows):
        if not key:
            els += text(f"{eid}{k}v", x + 4, y + 4 + 24 * k, val, 13, INK)
            continue
        els += text(f"{eid}{k}k", x + 4, y + 4 + 24 * k, key, 12, BLUE)
        els += text(f"{eid}{k}v", x + 150, y + 4 + 24 * k, val, 12, state_color(val) if val[:1] in "🙋✅⏳⬜" else INK)
    return els


def k_cols(eid, x, y, w, offs, rows, note=""):
    """Flush rows, as live: one row a line, a thin rule under each; the first cell small (a date, a mark, a state),
    the last right-aligned when the row has more cells than offsets (a kind: entry, email, meeting)."""
    els = []
    for i, r in enumerate(rows):
        ry = y + 24 * i
        for j, c in enumerate(r):
            if not c:
                continue
            last = j == len(r) - 1 and j >= len(offs)
            col = state_color(c) if c[:1] in "🙋✅⏳⬜☑" or last or j == 0 else INK
            if j == 0 and c[:1] not in "🙋✅⏳⬜":
                col = BODY
            cx = x + w - 6 - 5.8 * len(c) if last else x + offs[j]
            els += text(f"{eid}r{i}_{j}", cx, ry, c, 10 if (j == 0 or last) else 11, col)
        els += line(f"{eid}l{i}", [(x + offs[0], ry + 19), (x + w, ry + 19)], RULE, 1)
    return els + (text(eid + "_more", x + offs[0], y + 24 * len(rows) + 2, note, 10, BODY) if note else [])


def cols_h(rows, note=""):
    return 24 * len(rows) - 4 + (18 if note else 0)


def k_moves(eid, x, y, w, jobs):
    """Each Job under a who-has-the-move section, as live: its name, who has the move and since when on the right,
    its next move under it, then its newest Timeline entries as flush rows (date, what, kind)."""
    els, yy = [], y
    for k, (name, nxt, who, rows, more) in enumerate(jobs):
        els += text(f"{eid}{k}_n", x + 4, yy, "▾ " + name, 12, TITLE)
        els += text(f"{eid}{k}_w", x + w - 6 - 6.0 * len(who), yy + 1, who, 11, state_color(who))
        if nxt:
            els += text(f"{eid}{k}_x", x + 20, yy + 18, nxt, 11, BODY)
        els += k_cols(f"{eid}{k}_e", x, yy + (42 if nxt else 26), w, (20, 100), rows, more)
        yy += moves_h(((name, nxt, who, rows, more),)) + 10
    return els


def moves_h(jobs):
    return sum((42 if n else 26) + cols_h(r, m) + 10 for _, n, _, r, m in jobs) - 10


PANEL_H = {"kv": lambda p: 22 * len(p[1]), "table": lambda p: 30 + 20 * len(p[2]), "line": lambda p: 22,
           "form": lambda p: 22 * len(p[1]), "btn": lambda p: 30}


def tab_h(head_):
    return 38 + 13 * head_.count("\n")


def k_sidetabs(eid, x, y, w, items, panel):
    """Side tabs, as live: the list on the left, the first open (blue); on the right the open one to read, its parts
    in order (label and value rows, a line, a small table, a form, buttons)."""
    lw = 176
    els, iy = [], y
    for k, (head_, word) in enumerate(items):
        th = tab_h(head_)
        els += [_el("rectangle", f"{eid}{k}", x, iy, lw, th, BLUE if k == 0 else ROOM, "#e7f5ff" if k == 0 else "#ffffff",
                    roundness={"type": 3})]
        els += text(f"{eid}{k}_t", x + 8, iy + 4, head_, 11, BLUE if k == 0 else TITLE)
        els += text(f"{eid}{k}_w", x + 8, iy + th - 17, word, 10, state_color(word))
        iy += th + 6
    px, pw = x + lw + 12, w - lw - 12
    els += [_el("rectangle", eid + "_d", px, y, pw, sidetabs_h(items, panel) - 6, BLUE, "#ffffff", roundness={"type": 3})]
    keys = [k_ for p in panel if p[0] == "kv" for k_, _ in p[1] if k_.strip()]
    vx = px + 12 + (max(6.2 * len(k_) for k_ in keys) + 16 if keys else 0)   # the value column, past the longest label
    yy = y + 10
    for j, p in enumerate(panel):
        kind, pid = p[0], f"{eid}_p{j}"
        if kind == "kv":
            for k, (n_, words) in enumerate(p[1]):
                col = BLUE if words.endswith("↗") else state_color(words) if words[:1] in "🙋✅⏳⬜☐" else INK
                if n_.strip():
                    els += text(f"{pid}{k}k", px + 12, yy + 22 * k, n_, 11, BLUE)
                els += text(f"{pid}{k}v", vx if n_ else px + 12, yy + 22 * k, words, 11, col)
        elif kind == "table":                    # each column as wide as its words
            cols, rows = p[1], p[2]
            widths = [max([len(cols[c])] + [len(r[c]) for r in rows]) + 3 for c in range(len(cols))]
            unit = (pw - 24) / sum(widths)
            xs = [px + 12 + unit * sum(widths[:c]) for c in range(len(cols))]
            for c, col_ in enumerate(cols):
                els += text(f"{pid}h{c}", xs[c], yy, col_, 10, TITLE)
            for i, r in enumerate(rows):
                els += line(f"{pid}l{i}", [(px + 12, yy + 17 + 20 * i), (px + pw - 12, yy + 17 + 20 * i)], RULE, 1)
                for c, cell_ in enumerate(r):
                    els += text(f"{pid}r{i}_{c}", xs[c], yy + 21 + 20 * i, cell_, 10,
                                OR if "✎" in cell_ else BODY if c == 0 else INK)
        elif kind == "line":
            els += text(pid, px + 12, yy, p[1], 12 if j == 0 else 11, BLUE if p[1].endswith("↗") else TITLE)
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
    return max(sum(tab_h(h) + 6 for h, _ in items), 16 + sum(PANEL_H[p[0]](p) for p in panel)) + 6


def k_todo(eid, x, y, w, items):
    """A Process step's to-do rows, as live: the act, its small line, its state word, its verb; a row that waits on
    you orange."""
    els = []
    for k, (name, small, state, verb) in enumerate(items):
        ry, you = y + 50 * k, waits_on_you(state)
        els += [_el("rectangle", f"{eid}{k}", x, ry, w, 44, OR if you else RULE, "#fff4e6" if you else "#ffffff",
                    roundness={"type": 3})]
        els += text(f"{eid}{k}_n", x + 12, ry + 6, name, 13, TITLE) + text(f"{eid}{k}_w", x + 12, ry + 25, small, 11, BODY)
        right = x + w - 10
        if verb:
            els += _btns(f"{eid}{k}_b", right, ry + 10, (verb,), OR if you else BLUE)
            right -= btn_w((verb,)) + 4
        els += text(f"{eid}{k}_s", right - 6.4 * len(state), ry + 14, state, 11, state_color(state))
    return els


def k_tree(eid, x, y, w, root, branches):
    """The map, as the live parts_mindmap draws it: the root on the left, a branch per node (its pill, its name, one
    plain line), its children on the right (Open all, Close all open and close them)."""
    rows = [branch_h(b) for b in branches]
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
        nl = 1 + bool(pill) + bool(words)                             # a pill above the name, a line under it
        els += [_el("rectangle", f"{eid}{k}", x + 160, cy - box_h(nl) / 2, 220, box_h(nl), INK, "#ffffff",
                    roundness={"type": 3})]
        ny = cy - 7 * nl - 1                                          # its lines centred in the box
        if pill:                                                      # the pill above the name, as live (job 1)
            els += text(f"{eid}{k}_p", x + 170, ny, pill, 10, BODY)
            ny += 14
        els += text(f"{eid}{k}_n", x + 170, ny, name, 12, TITLE)
        els += text(f"{eid}{k}_w", x + 170, ny + 15, words, 10, BODY) if words else []
        els += text(f"{eid}{k}_sh", x + 340, cy - box_h(nl) / 2 + 4, "▸ show", 9, BODY) if children else []
        for j, cn in enumerate(children):
            chy = by + (bh - 30 * len(children)) / 2 + 30 * j + 2
            els += line(f"{eid}{k}_{j}_l", [(x + 380, cy), (x + 404, chy + 13)], ROOM, 1)
            els += [_el("rectangle", f"{eid}{k}_{j}", x + 404, chy, w - 404, 26, ROOM, "#ffffff", roundness={"type": 3})]
            els += text(f"{eid}{k}_{j}_n", x + 412, chy + 6, cn, 11, INK)
        by += bh + 10
    return els


def box_h(nl):
    return max(44, 20 + 14 * nl)


def branch_h(branch):
    pill, _, words, children = branch
    return max(box_h(1 + bool(pill) + bool(words)) + 8, 50, 30 * len(children))


def tree_h(branches):
    return sum(branch_h(b) + 10 for b in branches) - 10


def k_verbs(eid, x, y, w, verbs):
    """Plain buttons on the left (the map's Open all, Close all)."""
    els, cx = [], x
    for k, v in enumerate(verbs):
        bw = 16 + 7.5 * len(v)
        els += [_el("rectangle", f"{eid}{k}", cx, y, bw, 22, ROOM, "#ffffff", roundness={"type": 3})]
        els += text(f"{eid}{k}_t", cx + 8, y + 4, v, 11, INK)
        cx += bw + 8
    return els


STUDIO_VERBS = ("Draw", "Mind map", "Work", "Delivery")


def k_trows(eid, x, y, w, items):
    """Studio rows as live: the topic's address small, its name, its stage and kind as pills, its one line, its verbs
    (a waiting form adds the orange 🙋 Interaction), its picture on the right."""
    els = []
    for k, (addr, name, stage, kind, words, verbs, asks) in enumerate(items):
        ry = y + 132 * k
        els += [_el("rectangle", f"{eid}{k}", x, ry, w, 124, ROOM, "#ffffff", roundness={"type": 3})]
        els += text(f"{eid}{k}_a", x + 14, ry + 10, addr, 10, BODY)
        els += text(f"{eid}{k}_n", x + 14, ry + 28, name, 14, TITLE)
        px = x + 14 + 0.62 * 14 * len(name) + 10
        for j, (pill, col) in enumerate(((stage, ROOM), (kind, BLUE))):
            pw = 14 + 6.6 * len(pill)
            els += [_el("rectangle", f"{eid}{k}_p{j}", px, ry + 28, pw, 18, col, "#ffffff", roundness={"type": 3})]
            els += text(f"{eid}{k}_p{j}t", px + 7, ry + 30, pill, 10, col)
            px += pw + 6
        els += text(f"{eid}{k}_w", x + 14, ry + 56, words, 12, INK)
        bx = x + 14
        for j, v in enumerate(verbs + (("🙋 Interaction",) if asks else ())):
            bw = 16 + 7.2 * len(v)
            you = v.startswith("🙋")
            els += [_el("rectangle", f"{eid}{k}_v{j}", bx, ry + 86, bw, 24, OR if you else ROOM, "#fff4e6" if you else "#ffffff",
                        roundness={"type": 3})] + text(f"{eid}{k}_v{j}t", bx + 8, ry + 91, v, 11, OR if you else INK)
            bx += bw + 6
        tx = x + w - 150
        els += [_el("rectangle", f"{eid}{k}_th", tx, ry + 30, 136, 80, ROOM, GHOST)]
        for j in range(3):
            els += [_el("rectangle", f"{eid}{k}_th{j}", tx + 12 + 40 * j, ry + 58 + 8 * (j % 2), 30, 18, ROOM, "#ffffff")]
            if j:
                els += line(f"{eid}{k}_tl{j}", [(tx + 12 + 40 * j - 10, ry + 67), (tx + 12 + 40 * j, ry + 67)], ROOM, 1)
    return els


def k_empty(eid, x, y, w, words, verb):
    """A page with no topic of its own: it says so, with Add a topic."""
    els = text(eid + "_w", x + 4, y, words, 13, INK)
    bw = 16 + 7.5 * len(verb)
    return els + [_el("rectangle", eid + "_b", x + 4, y + 28, bw, 26, ROOM, "#ffffff", roundness={"type": 3})] + \
        text(eid + "_bt", x + 12, y + 33, verb, 12, INK)


def _red(els):
    """A proposal's content: its edges red."""
    for e in els:
        if e["type"] == "rectangle" and e["strokeColor"] in (ROOM, RULE, INK, BLUE):
            e["strokeColor"] = RE
    return els


def k_redline(eid, x, y, w, words):
    """A proposal that is only a line."""
    return text(eid, x + 2, y, f"{words} · proposal", 12, RE)


KIND = {"note": (k_note, lambda a: 14 * (a[0].count("\n") + 1)), "state": (k_state, lambda a: 20),
        "kv": (k_kv, lambda a: 24 * len(a[0])), "cols": (k_cols, lambda a: cols_h(a[1], a[2] if len(a) > 2 else "")),
        "moves": (k_moves, lambda a: moves_h(a[0])), "sidetabs": (k_sidetabs, lambda a: sidetabs_h(*a)),
        "todo": (k_todo, lambda a: 50 * len(a[0]) - 6), "tree": (k_tree, lambda a: tree_h(a[1])),
        "verbs": (k_verbs, lambda a: 22), "trows": (k_trows, lambda a: 132 * len(a[0]) - 8),
        "empty": (k_empty, lambda a: 56), "redline": (k_redline, lambda a: 16)}


def S(title, word="", red=False, flag=False, wait=""):
    """A section's heading bar: closed (▸), as every section starts; its state word on the right, as live; red, a
    proposal; flag, a 🙋 Interaction that waits for you (an orange edge); wait, the one thing that waits on the person,
    its line under the closed bar (live fd-wait)."""
    return {"t": title, "w": word, "red": red, "flag": flag, "wait": wait}


WAIT_H = 22                          # a waiting line under a closed bar


def bar_of(head_):
    return head_ if isinstance(head_, dict) else S(head_ or "")


def sec_h(sec):
    if sec[0] == "group":
        return 36
    b = bar_of(sec[0])
    has, wait = bool(b["t"]), WAIT_H if b.get("wait") else 0
    if sec[1] == "none":
        return 40 + wait
    return (40 if has else 0) + wait + KIND[sec[1]][1](sec[2:]) + 16


def sec_draw(eid, x, y, w, sec):
    """A numbered heading bar, closed (▸) as live starts every section; what it opens to drawn under it, behind a
    dashed line ("none": the bar alone, as on Work, whose Results repeat the Report's); a band heading (⚙️ Process,
    📊 Results)."""
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
    view-button-list with this view in orange, the goal-line, the view-caption and its sections."""
    name, path, (label, _) = PAGE[level]
    els = window(eid + "w", x, y, W, h, f"/_board/workbench?layout=focus&path=…/{name}&section={section}")
    els += rails(eid + "rl", x, y, level, section)
    cx = x + X0
    lines = crumb_lines(path)
    for k, ln in enumerate(lines):
        els += text(f"{eid}_crumb{k}", cx, y + 40 + 14 * k, ln, 10, BODY)
    top = y + 46 + 14 * len(lines)
    els += head(eid + "h", cx, top, name, section, views, on)
    gl = goal_lines(level)                           # the goal-line, as live: its label small, its words, a rule
    els += text(eid + "_goalk", cx, top + 70, label, 9, BODY)
    for k, words in enumerate(gl):
        els += text(f"{eid}_goal{k}", cx, top + 84 + 18 * k, words, 13, INK)
    els += line(eid + "_goall", [(cx, top + 88 + 18 * len(gl)), (cx + CW, top + 88 + 18 * len(gl))], PALE, 1)
    top += goal_h(level)
    if caption:
        els += text(eid + "_cap", cx, top + 76, caption, 12, BODY)
    yy = top + 106 if caption else top + 76
    for k, sec in enumerate(secs):
        els += sec_draw(f"{eid}r{k}", cx, yy, CW, sec)
        yy += sec_h(sec)
    return els


# ── the views (view, its view-caption, its sections in page order) ─────────────────────────────────────────────────
G_PROC, G_RES = ("group", "⚙️ Process"), ("group", "📊 Results")
MAP_CAP = "How it is built, as a map: its parts, and what each must find out."

# ── the forms, and which view's 🙋 holds each (as live, 261108): a form is (its tab, the form's questions as side
# tabs, the open question's panel, its waiting line, the bar's word, its tab's word)
RETENTION = ("Retention period", (("Q1 · Retention period", "waiting"), ("Q2 · Who signs", "waiting")),
             (("line", "Retention period"),
              ("kv", (("", "Q1 · Retention period   ·   Q2 · Who signs"),)),
              ("form", (("Q1", "Which retention period goes into v3?"),
                        ("A", "Two years after the study closes · my pick"),
                        ("B", "One year after the study closes"))),
              ("kv", (("", "asked by Data-use plan, written in rounds"), ("", "about Data-use plan rounds"))),
              ("btn", ("Copy feedback",))),
             "🙋 Retention period: Q1 · Retention period", "2 wait for you", "waiting for you")
DECISIONS = ("Plan decisions", (("Q1 · Four sections", "✅ applied · my own decision"),),
             (("line", "Plan decisions"), ("form", (("Q1", "<the question, as asked>"), ("", "✓ my own decision")))),
             "", "answered", "answered")
IX_OF = {("block", "Findings"): (RETENTION, DECISIONS), ("task", "Status"): (RETENTION, DECISIONS)}


def ix(level, view, n=0):
    """🙋 Interaction, the view's last section, holding this view's own forms: its state word, its first waiting
    question under the closed bar; a side tab per form (or per question, when it holds one) and the open one's form
    on the right; "nothing yet" when the view has none."""
    title = (f"{n} · " if n else "") + "🙋 Interaction"
    forms = IX_OF.get((level, view), ())
    if not forms:
        return (S(title, "nothing yet"), "none")
    first = forms[0]
    tabs = first[1] if len(forms) == 1 else tuple((f[0], f[5]) for f in forms)
    return (S(title, first[4], flag=bool(first[3]), wait=first[3]), "sidetabs", tabs, first[2])


def closing(secs, level, view):
    """The view's sections, then its 🙋 Interaction numbered after the last band's numbered sections (unnumbered when
    that band has none, as live)."""
    last = max([i for i, s in enumerate(secs) if s[0] == "group"], default=-1)
    nums = [int(m.group(1)) for s in secs[last + 1:] if s[0] != "group"
            for m in [re.match(r"(\d+) · ", bar_of(s[0])["t"])] if m]
    return tuple(secs) + (ix(level, view, max(nums) + 1 if nums else 0),)


def same(letter, view):
    """Work's 📊 Results repeat the Report's view, drawn by the same code: its bars drawn closed here."""
    return ("", "note", f"the Report's {letter} · {view}, drawn by the same code")


def bars(secs):
    """A Report view's sections as Work repeats them: its state line, then each numbered section as a closed bar."""
    return tuple(s if s[1] == "state" else (s[0], "none") for s in secs
                 if s[0] != "group" and (bar_of(s[0])["t"] or s[1] == "state"))


def report(level, items):
    return tuple((v, cap, closing(secs, level, v)) for v, cap, secs in items)


def work(level, report_items, process):
    """Each Work view: ⚙️ Process when it has a step, then 📊 Results, the Report's view by the same code."""
    out = []
    for k, (v, rcap, secs) in enumerate(report_items):
        proc = process.get(v, ())
        body = ((G_PROC,) + proc if proc else ()) + (G_RES, same(LETTERS[k], v)) + bars(secs)
        out.append((v, rcap, closing(body, level, v)))
    return tuple(out)


# ── the Block (s51 Report, s52 Work, s53 Studio) ─────────────────────────────────────────────────────────────────────
J1N, J2N, J3N = "Data access request to the partner office", "Review board amendment", "Kickoff meeting with the partner office"
J2_ROWS = (("2026-11-06", "Amendment to the review board · draft ✎", "email"),
           ("2026-11-05", "the review board contact: submit once the retention period is set", "entry"),
           ("2026-11-04", "sent v2, every comment answered", "entry"),
           ("2026-11-02", "Call with the review board contact", "meeting"))
J1_ROWS = (("2026-10-28", "the data owner: the extract follows the approved amendment", "entry"),
           ("2026-10-28", "Reply from the data owner", "email"),
           ("2026-10-24", "Intro call with the data owner", "meeting"),
           ("2026-10-20", "Data access request", "delivery"))
J3_ROWS = (("2026-10-15", "Kickoff notes", "email"), ("2026-10-14", "Kickoff with the partner office", "meeting"),
           ("2026-10-07", "sent the invite through the partner coordinator", "entry"))
NEEDS = (("What the partner\noffice needs", "answered"), ("The retention period", "proposed, waiting for you"))
NEEDS_PANEL = (("line", "What the partner office needs   ·   answered"),
               ("kv", (("", "What does the partner office need from us before it"), ("", "sends the extract?"),
                       ("answer", "a signed data-use plan and the request form"), (" ", "with its field list; the extract follows"),
                       (" ", "once the review board approves the amendment"),
                       ("its work", "Data access request: twelve fields, by month,"),
                       (" ", "no row-level data; its date is theirs to give"))),
               ("line", "Read full report ↗"))
BLOCKERS = (("What could hold up\nthe extract", "no answer yet"),)
BLOCKERS_PANEL = (("line", "What could hold up the extract   ·   no answer yet"),
                  ("kv", (("", "What could still hold up the extract once the"), ("", "amendment is approved?"),
                          ("its work", "Data access request: the extract follows"), (" ", "the approved amendment (j02)"))))
PEOPLE_ALL = (("Project lead", "Our team"), ("Data owner", "has the move"), ("Review board contact", "Review board"),
              ("Data analyst", "Our team"), ("Partner coordinator", "Partner office"))
PEOPLE_PANEL = (("kv", (("Side", "Our team"), ("Role here", "leads the request and signs each send"),
                        ("Owns", "the Block, the request and every send"), ("Reach", "the project channel"),
                        ("Ask them about", "priorities, a send to sign"))),
                ("line", "Open the people page ↗"))
MESSAGES = (("Emails", "newest 2026-11-06"), ("Meetings", "newest 2026-11-02"), ("Drafts", "waits for you to send"))
MESSAGES_PANEL = (("table", ("date", "message", "Job"),
                   (("11-06", "Amendment to the review board ✎", "Review board amendment"),
                    ("10-30", "Comments on v1", "Review board amendment"),
                    ("10-28", "Reply from the data owner", "Data access request"),
                    ("10-15", "Kickoff notes", "Kickoff meeting"))),)
NEXT = (("Review board\namendment", "ours · 3 days"), ("Data access request\nto the partner office", "Data owner · 11 days"))
NEXT_PANEL = (("line", "pick the retention period, then send the amendment draft"),
              ("kv", (("Has the move", "us"), ("Since", "2026-11-05 · 3 days"), ("Ticket", "RB-0001"))),
              ("line", "Steps still open"),
              ("kv", (("☐ 3", "Pick the retention period"), ("☐ 4", "Send the amendment with the plan"),
                      ("☐ 5", "Forward the approval to the data owner"))),
              ("line", "Open the Job ↗"))
DELIVERY = (("Data-use plan v2", "sent"), ("Data access request", "sent"))
DELIVERY_PANEL = (("kv", (("Date", "2026-11-04"), ("From", "j02_review_board_amendment/t01_data_use_plan"),
                          ("To", "Review board contact"), ("Cc", "Project lead"), ("Subject", "Re: Data-use plan v1, now v2"),
                          ("State", "sent"), ("Attachments", "data-use-plan-v2.txt"))),
                  ("line", "Open the copy page ↗ · Read the draft ↗"))
BLOCK_MAP = (("", "verbs", ("Open all", "Close all")), ("", "tree", "b01_example_\ndata_request", (
    ("", "Questions", "", ("✅ What the partner office needs", "🙋 The retention period", "⬜ What could hold up the extract")),
    ("job 0", "People", "", ()),
    ("job 1", "Data access request", "to the partner office", ()),
    ("job 2", "Review board amendment", "", ("Task 1 · Data-use plan, in rounds",)),
    ("job 3", "Kickoff meeting", "with the partner office", ()))))
BLOCK_R = (
    ("MindMap", MAP_CAP, BLOCK_MAP),
    ("Status", "Each Job by who has the move: us, them, or done; then the Studio topics.", (
        (S("1 · 🙋 Waiting on us", "1 waits for you",
           wait="🙋 Review board amendment: pick the retention period, then send the amendment draft"), "moves",
         ((J2N, "pick the retention period, then send the amendment draft", "us · 3 days", J2_ROWS, "… 4 more, back to 2026-10-30"),)),
        (S("2 · ⏳ Waiting on them", "longest 11 days"), "moves",
         ((J1N, "chase the extract date if there is no word by 2026-11-12", "Data owner · 11 days", J1_ROWS[:3],
           "… 3 more, back to 2026-10-14"),)),
        (S("3 · ✅ Done", "done"), "moves", ((J3N, "", "since 2026-10-15", J3_ROWS, ""),)),
        (S("4 · 🎨 Studio", "1 shaping"), "cols", (4, 4), (("", "Data-use plan rounds", "shaping"),)))),
    ("Findings", "What it has found so far, and what it hands over.", (
        (S("1 · ❓ Needs", "waits for you", wait="🙋 The retention period: its answer waits for your agreement"),
         "sidetabs", NEEDS, NEEDS_PANEL),
        (S("2 · ❓ Blockers", "no answer yet"), "sidetabs", BLOCKERS, BLOCKERS_PANEL),
        (S("3 · 👥 People", "1 has the move"), "sidetabs", PEOPLE_ALL, PEOPLE_PANEL),
        (S("4 · ✉️ Messages", "1 draft waits for you",
           wait="🙋 a draft waits for you to send: Amendment to the review board"), "sidetabs", MESSAGES, MESSAGES_PANEL),
        (S("5 · ⏳ Next move", "1 waits for you · 1 on them",
           wait="🙋 Review board amendment: ours since 2026-11-05, pick the retention period, then send the draft"),
         "sidetabs", NEXT, NEXT_PANEL),
        (S("6 · 📦 Delivery", "sent"), "sidetabs", DELIVERY, DELIVERY_PANEL))),
)
BLOCK_REPORT = report("block", BLOCK_R)
BLOCK_WORK = work("block", BLOCK_R, {
    "Status": ((S("1 · 🚧 Next steps", "1 in progress"), "todo",
                ((J2N + " › Data-use plan, written in rounds", "the Task in progress", "in progress", "Open"),)),),
    "Findings": ((S("1 · ✍️ Answers to write or agree", "1 waits for you",
                    wait="🙋 The retention period: its answer waits for your agreement"), "todo",
                  (("The retention period", "Which retention period does the plan ask for?", "🙋 waiting for you", "Agree"),
                   ("What could hold up the extract", "What could still hold it up once approved?", "no answer yet", "Write"))),),
})
TOPIC_ROW = ("b01.j02.t01-s01:example_data_request.review_board_amendment.data_use_plan @", "data_use_plan_rounds",
             "shaping", "draft", "A placeholder walk through one document written in rounds.", STUDIO_VERBS, True)
SHORT = "the row's name in the short form: b01-s01:example_data_request @ data_use_plan_rounds"
BLOCK_STUDIO = (
    ("Topics", "", (
        ("", "trows", (TOPIC_ROW,)),
        ("", "redline", SHORT))),
)

# ── the Job (s54 Report, s55 Work, s56 Studio) ───────────────────────────────────────────────────────────────────────
JOB_MAP = (("", "verbs", ("Open all", "Close all")), ("", "tree", "j01_data_access_\nrequest", (
    ("", "🗓️ What happened", "", ("10-28 · reply from the data owner", "10-24 · intro call, data owner",
                                  "10-20 · sent the request", "… 3 more")),
    ("", "⏳ Who has the move", "", ("Data owner · since 10-28 · 11 days",)),
    ("", "➡️ Next", "", ("chase the extract date by 11-12",)),
    ("", "☐ Steps still open", "", ("Get the extract date", "Receive the extract, check fields")))))
JOB_ROWS = J1_ROWS[:1] + (("2026-10-28", "Reply from the data owner", "email"),
                          ("2026-10-24", "intro call with the data owner", "entry"),
                          ("2026-10-24", "Intro call with the data owner", "meeting"),
                          ("2026-10-20", "sent the request with the field list", "entry"),
                          ("2026-10-20", "Data access request", "delivery"),
                          ("2026-10-14", "the kickoff agreed what the request asks for (j03)", "entry"))
STEPS = (("☑ 1", "Fill in the request form", ""), ("☑ 2", "Send the request with the field list", ""),
         ("☑ 3", "Walk the fields with the data owner", ""), ("☐ 4", "Get the extract date", "open"),
         ("☐ 5", "Receive the extract and check every field", "open"))
JOB_R = (
    ("MindMap", "This Job as a map: what happened, who has the move, and what is left.", JOB_MAP),
    ("Status", "Who has the move, since when, and what happened so far.", (
        ("", "state", "🟡 Active"),
        (S("1 · ⏳ Waiting on them", "Data owner · 11 days"), "kv",
         (("Has the move", "Data owner"), ("Since", "2026-10-28 · 11 days"),
          ("Next", "chase the extract date if there is no word by 2026-11-12"), ("Ticket", "REQ-0001"),
          ("State", "🟡 ACTIVE"))),
        (S("2 · 🗓️ Timeline", "newest 2026-10-28"), "cols", (4, 84), JOB_ROWS),
        (S("3 · ☑️ Steps", "3 of 5 done"), "cols", (4, 84), STEPS))),
    ("Findings", "What it has found so far, and what it hands over.", (
        (S("1 · 👥 People", "1 has the move"), "sidetabs",
         (("Project lead", "Our team"), ("Data owner", "has the move"), ("Data analyst", "Our team")), PEOPLE_PANEL),
        (S("2 · ✉️ Messages", "newest 2026-10-28"), "sidetabs",
         (("Emails", "newest 2026-10-28"), ("Meetings", "newest 2026-10-24"), ("Drafts", "none to send")),
         (("table", ("date", "message"), (("10-28", "Reply from the data owner"),)),)),
        (S("3 · 📦 Delivery", "sent"), "sidetabs", (("Data access request", "sent"),),
         (("kv", (("Date", "2026-10-20"), ("From", "j01_data_access_request"), ("To", "Data owner (partner office)"),
                  ("Cc", "Project lead"), ("Subject", "Data access request (placeholder extract)"), ("State", "sent"),
                  ("Attachments", "requested-fields.csv"))),
          ("line", "Open the copy page ↗ · Read the draft ↗"))))),
)
JOB_REPORT = report("job", JOB_R)
JOB_WORK = work("job", JOB_R, {      # no ⚙️ Process on a Job today; the next move as a step is a proposal
    "Status": ((S("1 · ➡️ The next move", red=True), "todo",
                (("Chase the extract date", "with the data owner, if there is no word by 2026-11-12", "on them · 11 days",
                  "Copy prompt"),)),),
})
JOB_STUDIO = (
    ("Topics", "", (
        ("", "empty", "No Studio topic here yet.", "Add a topic"),)),
)

# ── the Task (s57 Report, s58 Work, s59 Studio) ──────────────────────────────────────────────────────────────────────
TASK_MAP = (("", "verbs", ("Open all", "Close all")), ("", "tree", "t01_data_use_\nplan", (
    ("", "Runs", "", ("Run 1 · Retention period", "Run 2 · Plan decisions", "run-write-data_use_plan · write")),)))
TASK_R = (
    ("MindMap", MAP_CAP, TASK_MAP),
    ("Status", "Each round of the document, who has the move now, and its Runs.", (
        (S("1 · 📝 Rounds", "round 2 · waiting"), "sidetabs",
         (("v1 to the review\nboard contact", "done"), ("v2 answers the six\ncomments", "waiting")),
         (("kv", (("", "Four sections; the retention period left to set."), ("", "Six comments came back on 2026-10-30."))),
          ("line", "data_use_plan_v1.md"), ("line", "Open run-write-data_use_plan ↗"))),
        (S("2 · 🙋 Waiting on us", "waits for you · 3 days",
           wait="🙋 the next move is ours: pick the retention period (the waiting form), then write v3"), "kv",
         (("", "pick the retention period (the waiting form), then write v3"), ("Has the move", "us"),
          ("Since", "2026-11-05"))),
        (S("3 · 🧪 Runs", "1 of 3 done · 2 waiting"), "cols", (4, 120),
         (("🙋 waiting for you", "r01_collect_retention_period"), ("✅ done", "r02_collect_data_use_plan"),
          ("🙋 waiting for you", "run-write-data_use_plan · v2 answers all six comments on v1"))))),
)
TASK_REPORT = report("task", TASK_R)
TASK_WORK = work("task", TASK_R, {   # no ⚙️ Process on a Task today; writing v3 as a step is a proposal
    "Status": ((S("1 · ✍️ Write v3", red=True), "todo",
                (("Write v3 of the data-use plan", "once the retention period form is answered", "waits on the form",
                  "Copy prompt"),)),),
})
TASK_STUDIO = (
    ("Topics", "", (
        ("", "trows", (TOPIC_ROW,)),
        ("", "redline", SHORT))),
)

CLOSED = ("every section starts closed (▸), its state word on its right, a waiting line under one that waits on you; "
          "what it opens to is drawn under its bar, behind a dashed line")
OWN = "🙋 Interaction is every view's last section and holds its own forms"


def rail(level):
    return "the right rail: " + " · ".join(RIGHT[level]) + (" (no Timeline on a Job)" if level == "job" else "") + \
        ", as served 261108"


VIEWS = {   # (level, section): (the line above the screens, the views, the open question)
    ("block", "report"): ("MindMap · Status · Findings, as the live page draws them (261108); " + CLOSED + ";\n" + OWN
                          + "; " + rail("block"), BLOCK_REPORT, "? agree A to C: they\nfollow the live page"),
    ("block", "work"): ("the same views as Report: ⚙️ Process when it has a step, then 📊 Results by the same code; " + CLOSED
                        + ";\n" + OWN + "; " + rail("block"), BLOCK_WORK, "? Process before Results\non Status and Findings"),
    ("block", "studio"): ("one view, Topics: the Block's topics and its Jobs' and Tasks', flat rows as live; red: the row's name\n"
                          "in the short form, a proposal; " + rail("block"), BLOCK_STUDIO, "? the short name for\na topic row (red)"),
    ("job", "report"): ("MindMap · Status · Findings, as live (j01 waits on the data owner); " + CLOSED + ";\n" + OWN + "; "
                        + rail("job"), JOB_REPORT, "? agree A to C: they\nfollow the live page"),
    ("job", "work"): ("the same views as Report, 📊 Results only (a Job has no ⚙️ Process today); red: the next move as a\n"
                      "step, a proposal; " + OWN + "; " + rail("job"), JOB_WORK, "? a Process step for\nthe next move (red)"),
    ("job", "studio"): ("one view, Topics: a Job with no topic says so, with Add a topic, as live;\n" + rail("job"),
                        JOB_STUDIO, "? Add a topic is\nenough here"),
    ("task", "report"): ("MindMap · Status, read only, as live (no Findings on a Task); its goal-line the Task's Aim; " + CLOSED
                         + ";\n" + OWN + "; " + rail("task"), TASK_REPORT, "? agree A and B: they\nfollow the live page"),
    ("task", "work"): ("the same views as Report, 📊 Results only (a Task has no ⚙️ Process today); red: writing v3 as a\n"
                       "step, a proposal; " + OWN + "; " + rail("task"), TASK_WORK, "? a Process step to\nwrite v3 (red)"),
    ("task", "studio"): ("one view, Topics: the Task's own topic, s01, the row the Block shows too; red: the short name;\n"
                         + rail("task"), TASK_STUDIO, "? the short name for\na topic row (red)"),
}
# what is new on each letter's screen: its green ✎ notes under its letter, dated, and listed under the screens
D8 = "261108"
NOTES = {
    ("block", "report"): {"A": [(D8, "new: drawn from the live page"), (D8, "the map: Questions, then job 0 to job 3"),
                                (D8, "🙋 Interaction last: nothing yet")],
                          "B": [(D8, "each Job by who has the move"), (D8, "🙋 Waiting on us: its waiting line"),
                                (D8, "a Job's newest entries under it")],
                          "C": [(D8, "Needs, Blockers: a tab per question"), (D8, "👥 People · ✉️ Messages · ⏳ Next move"),
                                (D8, "🙋 two forms: 2 wait for you")]},
    ("block", "work"): {"A": [(D8, "📊 Results only: the Report's map")],
                        "B": [(D8, "⚙️ 🚧 Next steps: the Task in progress"), (D8, "📊 Results = the Report's B")],
                        "C": [(D8, "⚙️ ✍️ answers to write or agree"), (D8, "Agree and Write, one verb a row"),
                              (D8, "📊 Results = the Report's C")]},
    ("block", "studio"): {"A": [(D8, "one view, Topics: the Task's s01 row"), (D8, "its 🙋 Interaction: a form waits"),
                                (D8, "red: the row's name, short form")]},
    ("job", "report"): {"A": [(D8, "the map: happened, move, next, open")],
                        "B": [(D8, "🟡 Active, then who has the move"), (D8, "🗓️ Timeline, ☑️ Steps 3 of 5")],
                        "C": [(D8, "👥 People: the three on this Job"), (D8, "✉️ Messages, 📦 Delivery: sent")]},
    ("job", "work"): {"A": [(D8, "📊 Results only, as live")],
                      "B": [(D8, "no ⚙️ Process today: Results only"), (D8, "red: the next move as a step")],
                      "C": [(D8, "📊 Results only, as live")]},
    ("job", "studio"): {"A": [(D8, "no topic here yet: Add a topic")]},
    ("task", "report"): {"A": [(D8, "the map: its three Runs")],
                         "B": [(D8, "📝 Rounds: a tab per round"), (D8, "🙋 Waiting on us: 3 days"),
                               (D8, "🧪 Runs; 🙋 two forms wait")]},
    ("task", "work"): {"A": [(D8, "📊 Results only, as live")],
                       "B": [(D8, "no ⚙️ Process today: Results only"), (D8, "red: write v3 as a step")]},
    ("task", "studio"): {"A": [(D8, "one view, Topics: s01's row"), (D8, "red: the row's name, short form")]},
}
PIECE = {   # the why notes: what the live focus page showed when the cell was drawn (261108)
    ("block", "report"): ("the Block's Report: its map, who has each move, what it found",
                          ["no drawing yet of the\nlive cowork pages", "four themes have\ntheir 3 × 3 already",
                           "Findings holds six\nsections, closed"]),
    ("block", "work"): ("the Block's Work: Process, then the Report's views",
                        ["Process only on Status\nand Findings", "Agree and Write sit\nin Findings' Process",
                         "the map has no step"]),
    ("block", "studio"): ("the Block's Studio: its topics and its Tasks'",
                          ["one topic, s01, lives\nin j02's Task", "its name prints\nthe whole path",
                           "its form waits:\n🙋 Interaction"]),
    ("job", "report"): ("a Job's Report: its map, who has the move, what it found",
                        ["j01 waits on the\ndata owner, 11 days", "Status: Timeline and\nSteps, 3 of 5",
                         "Findings: People,\nMessages, Delivery"]),
    ("job", "work"): ("a Job's Work: the Report's views, Results only",
                      ["no Process band\non a Job today", "the next move has\nno verb", "Work repeats\nthe Report"]),
    ("job", "studio"): ("a Job's Studio: its own topics, or none yet",
                        ["j01 has no topic", "Add a topic is\nthe only verb", "a Job's rail has\nno Timeline"]),
    ("task", "report"): ("a Task's Report: its map, each round, its Runs",
                         ["Status: Rounds, Waiting\non us, Runs", "no Findings view\non a Task", "two forms wait\nfor you"]),
    ("task", "work"): ("a Task's Work: the Report's views, Results only",
                       ["no Process band\non a Task today", "v3 waits on a form,\nno verb to write it",
                        "Work repeats\nthe Report"]),
    ("task", "studio"): ("a Task's Studio: its own topic",
                         ["s01 lives here:\nthe rounds drawn", "the same row shows\non the Block", "its form waits"]),
}
TARGET = {"block": "servers/workbench-cowork/cowork_theme.py · workbench-cowork/SKILL.md",
          "job": "servers/workbench-cowork/cowork_theme.py · workbench-cowork/SKILL.md",
          "task": "servers/workbench-cowork/cowork_theme.py · workbench-cowork/SKILL.md"}

AGREED = {}                            # (level, section): {letter: sections}, the letters settled so far; none yet
MOCK = """<!doctype html><meta charset=utf-8><title>{letter} · {view}</title>
<!-- GENERATED by cowork_ui_cells.py from AGREED; the agreed screen of {nn} view {letter} -->
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
    return 214 + goal_h(level) + max(tall(secs) for _, _, secs in items)


NOTE_H = 20                          # one green note's line under a letter


def notes_top(notes, letters):
    """Where the screens start under their letters: the letter, then the most notes any of them carries."""
    return 40 + NOTE_H * max([len(notes.get(L, ())) for L in letters] + [0])


def letter_notes(eid, x, y, notes):
    """A letter's green ✎ notes, one a line under it, each with its own date (canvas.change_note)."""
    return [change_note(x + 4, y + 34 + NOTE_H * j, what, date, None, 14) for j, (date, what) in enumerate(notes)]


def screens(eid, x, y, items, level, section, notes=None, gap=40):
    """Every view lettered A, B, C …, every screen the same size (the tallest view's), three a row; each letter
    carries its green ✎ notes under its name, dated."""
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
    if sec[0] == "group":
        return sec[1], ""
    if sec[1] in ("none", "redline"):
        return bar_of(sec[0])["t"] or (sec[2] if sec[1] != "none" else ""), "proposal" if sec[1] != "none" else ""
    words = {"tree": lambda: " · ".join(b[1] for b in sec[3]), "sidetabs": lambda: " · ".join(h for h, _ in sec[2]),
             "todo": lambda: " · ".join(r[0] for r in sec[2]), "trows": lambda: " · ".join(r[1] for r in sec[2]),
             "moves": lambda: " · ".join(j[0] for j in sec[2]), "verbs": lambda: " · ".join(sec[2])
             }.get(sec[1], lambda: str(sec[2]))()
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
    span = f"A to {last}" if len(names) > 1 else "A"
    write_agreed(topic, nn, level, section)
    ui = topic / "delivery" / "ui"
    pieces = [("page", f"ui/{level}-{section}/{L}-{slug(v)}.html", f"{L} · the {v} view",
               (ui / f"{level}-{section}" / f"{L}-{slug(v)}.html").exists()) for L, v in zip(LETTERS, names)]
    sk = topic / "delivery" / "skill" / f"{level}-{section}-views.md"
    pieces.append(("book", f"skill/{sk.name}", "the views' manual, for workbench-cowork", sk.exists()))
    spec = {"title": f"{level.capitalize()} UI · {VERB[section]}: {piece.split(': ', 1)[1]}",
            "why": {"question": f"why do we need s{nn}?", "notes": why,
                    "quote": "asked 261108: the cowork 3 × 3, drawn from the live cowork pages"},
            "what": {"head": f"② what s{nn} hands over: one screen, {span}", "icon": "page", "name": "delivery/ui/",
                     "type": "ui", "deck_why": f"stays in s{nn}'s delivery/deck/, so anyone gets it in a minute", "parts": pieces},
            "job": topic.parent.parent,
            "target": TARGET[level],
            "missing": [(name, "not settled yet") for _, name, _, done in pieces if not done],
            "have": [(name, "agreed") for icon, name, _, done in pieces if done and icon == "page"]}
    notes = NOTES.get((level, section), {})

    def design():                                    # A, B, C … every view the same screen
        els = text("skA", 690, 280, f"{span} · {piece}, every view the same screen", 18, TITLE)
        els += text("lay", 690, 330, lay, 16, BODY)
        y = 356 + 20 * (lay.count("\n") + 1)
        e, bottom = screens("sc", 690, y, items, level, section, notes)
        listed = [(L, d, w) for L in LETTERS for d, w in notes.get(L, ())]   # every new screen's notes, in one place
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


if __name__ == "__main__":                               # python cowork_ui_cells.py <topic folder> <letter> <out>
    print(letter_png(Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])))
