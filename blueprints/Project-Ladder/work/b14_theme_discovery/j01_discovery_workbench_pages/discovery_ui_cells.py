"""The nine sNN of b14 j01 · The discovery pages, level by level: one per level (Block, Job, Task) and section (Report,
Work, Studio), each drawn in haipipe-studio's five parts (scripts/five_parts.py). Copied from b17's work_ui_cells.py
and b11's insight_ui_cells.py, so the discovery 3 × 3 reads as the paper's, labeling's, insight's and work's do. Each
sNN's builder is `build(Path(__file__).parent)`: its cell is found by its folder name (s51-block-ui-report → block,
report).

A cell's Design is its page's views, lettered A, B, C …, each drawn as the same full screen (haipipe-ui, "one view,
one screen"): the window, both rails as pale short lines, the path, the title-&-section, the view-button-list with this
view in orange, the goal-line (a Block's Purpose, a Job's Goal, a Task's Aim, each its label above), the view-caption,
then the view's sections as numbered heading bars, closed (▸) as the live page starts them, each with its state word on
its right and, when it waits on the person, its waiting line under the bar; what a bar opens to is drawn under it as
what it is (side tabs, a Job's rows folding to its Tasks and Runs, a map). 🙋 Interaction is the last section of every
Report and Work view and holds that view's own forms; Work has the same views as Report, ⚙️ Process first when it has a
step, then 📊 Results drawn by the same code. Studio is one view, Topics, flat rows. The right rail ends Skills · Files.

Drawn 261108 from the live discovery pages (servers/workbench-discovery/discovery_focus.py on the shared work page):
the Block and the Job read MindMap · Status · Findings, the Task MindMap · Status (a Task page has no Findings: its
Status holds the discovery parts). The discovery parts are 📚 Papers (a side tab per Paper Run: its Card, reading
depth, claim support, citation check; a Card whose verification line says NEEDS is the waiting line under the bar),
📖 Evidence Bib (a side tab per Task: its entries, where it was handed over, the BibTeX) and 🧾 Synthesis (a side tab
per Task that wrote its summary). Every screen is new, so each carries its dated green ✎ notes under its letter, listed
again under the screens (NOTES). A proposal the live page does not have yet is red, unnumbered, marked "proposal"
(S(..., red=True)). The drawing is written by five_parts.marks_writer, so a person's marks on the canvas stay.

The example is the theme's public example, discovery/b01_example_prior_work (three made-up papers, one inquiry Job,
one sub-question Task): a Block is one field of prior work; a Job one inquiry; a Task one sub-question; a hard Run one
paper. Tools is public, so every name is a placeholder.

    python discovery_ui_cells.py <topic folder> <letter> <out>     one letter's screen alone, for a review round
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
LETTERS = "ABCDEFGH"
W, CW, X0 = 780, 640, 70             # a screen, its content column, where the column starts (the rails are short lines)
CH = 0.62                            # the code font's width per size (quick_draw.WIDE)
BLUE = "#1864ab"                     # the workbench's colour for the current thing
PALE = "#dee2e6"

# ── the example: the theme's public discovery example, as the live pages show it ────────────────────────────────────
SPACE = "<SPACE> / Tools / blueprints / Project-Ladder / discovery"
BLOCK, JOB, TASK = "b01_example_prior_work", "j01_policy_effect_inquiry", "t01_policy_prior_work"
PAGE = {   # (name, path, goal-line label, goal-line), as served 261108
    "block": (BLOCK, f"{SPACE} / {BLOCK}", "PURPOSE",
              "What earlier work found about <a policy> and <an outcome>; three made-up papers\n"
              "read as numbered Runs, their Evidence Bib handed to the Paper-Example."),
    "job": (JOB, f"{SPACE} / {BLOCK} / {JOB}", "GOAL",
            "Read the earlier studies of <the policy> and its effect on <an outcome>,\none placeholder paper per Run."),
    "task": (TASK, f"{SPACE} / {BLOCK} / {JOB} / {TASK}", "AIM",
             "What did earlier work find about <the policy> and its effect on <an outcome>?")}
LEFT = {"block": (0, 4, 1), "job": (1, 5, 2), "task": (1, 3, 2)}   # this page's line, how many, the first child line
RIGHT = ("Report", "Work", "Studio", "Interactions", "Delivery", "Timeline", "Skills", "Files")   # as served 261108


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
    """The title-&-section, then the view-button-list, the open view in orange."""
    els = text(eid + "_t", x, y, name, 20, INK) + text(eid + "_s", x + CH * 20 * len(name) + 14, y + 4, VERB[section], 15, BODY)
    cx = x
    for k, v in enumerate(views):
        w = 14 + 8 * len(v)
        els += [_el("rectangle", f"{eid}_v{k}", cx, y + 36, w, 24, OR if k == on else ROOM,
                    "#fff4e6" if k == on else "#ffffff", roundness={"type": 3})] + text(f"{eid}_v{k}_t", cx + 7, y + 40, v, 12, INK)
        cx += w + 8
    return els


def crumb_lines(words, width=100):
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
    if word.startswith("✅") or w.startswith(("done", "agreed", "answered", "built", "ready", "written", "abstract read")):
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


# ── a section's content, drawn as what it is ──────────────────────────────────────────────────────────────────────
def k_note(eid, x, y, w, words):
    """A small plain line: what a band's view repeats."""
    return text(eid, x + 2, y, words, 11, BODY)


def k_waitline(eid, x, y, w, said, words):
    """The line above a Job's Status bars, as live: the yellow dot, "waiting on you", what waits."""
    els = [_el("ellipse", eid + "_d", x + 2, y + 2, 16, 16, OR, "#ffe8a3")]
    els += text(eid + "_s", x + 26, y, said, 14, INK)
    return els + text(eid + "_w", x + 26 + CH * 14 * len(said) + 6, y, "· " + words, 14, INK)


def k_todo(eid, x, y, w, items):
    """A Process step's to-do rows, as live: the act, its small line, its state word, its verb; a row that waits on
    you orange."""
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
        els += text(f"{eid}{k}_s", right - CH * 11 * len(state), ry + 14, state, 11, state_color(state))
    return els


def k_list(eid, x, y, w, items):
    """A section's rows as live lists them: a name, its word."""
    els = []
    for k, (name, note) in enumerate(items):
        els += text(f"{eid}{k}_n", x + 4, y + 24 * k, name, 12, TITLE)
        els += text(f"{eid}{k}_w", x + 300, y + 24 * k + 1, note, 11, state_color(note))
    return els


def k_runs(eid, x, y, w, items):
    """A Task's Runs as live lists them: the state word, the Run's name, what it returned."""
    els = []
    for k, (state, name, out) in enumerate(items):
        ry = y + 24 * k
        els += line(f"{eid}{k}_l", [(x, ry + 19), (x + w, ry + 19)], "#e9ecef", 1)
        els += text(f"{eid}{k}_s", x + 4, ry + 1, state, 11, state_color(state))
        els += text(f"{eid}{k}_n", x + 128, ry, name, 12, TITLE)
        els += text(f"{eid}{k}_o", x + 372, ry + 1, out, 11, BODY) if out else []
    return els


def _bar(eid, x, y, share, w=90):
    """A thin bar of how much is done, as live draws one on a band's or a Job's row."""
    els = [_el("rectangle", eid, x, y, w, 6, "#e9ecef", "#e9ecef")]
    return els + ([_el("rectangle", eid + "_f", x, y, max(4, w * share), 6, GR if share >= 1 else BLUE,
                       GR if share >= 1 else "#74c0fc")] if share else [])


def k_fold(eid, x, y, w, items):
    """A folding tree as live draws it: a line per Task (depth 1, ▸ it folds) or Run (depth 2), its state word, what it
    returned; a Task's row may carry its 🙋 Answer button."""
    els = []
    for k, (depth, name, state, out, *verb) in enumerate(items):
        ky = y + 22 * k
        kx = x + 4 + 18 * (depth - 1)
        els += text(f"{eid}{k}_n", kx, ky, ("▸ " if depth == 1 else "") + name, 11, TITLE if depth == 1 else INK)
        els += text(f"{eid}{k}_s", x + 236, ky, state, 11, state_color(state))
        if out:
            els += text(f"{eid}{k}_o", x + 364, ky, out, 11, BODY)
        if verb:
            els += _btns(f"{eid}{k}_b", x + w - 4, ky - 4, verb, OR if verb[0].startswith("🙋") else BLUE)
    return els


def k_jobrows(eid, x, y, w, rows):
    """A band's Jobs, one row each, closed (▸): its emoji, number and short name, its word left of its bar, the bar on
    the right edge, its 🙋 Answer button; what a row opens to, its Tasks and Runs, drawn under it behind a dashed line."""
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
            right -= btn_w(verb)
        els += text(f"{eid}{k}_s", right - CH * 11 * len(said), yy + 9, said, 11, BODY)
        yy += 36
        if kids:
            els += line(f"{eid}{k}_in", [(x + 6, yy - 4), (x + 6, yy + 22 * len(kids) - 4)], PALE, 1, dashed=True)
            els += k_fold(f"{eid}{k}_k", x + 14, yy, w - 14, kids)
            yy += 22 * len(kids) + 6
    return els


def jobrows_h(rows):
    return sum(36 + (22 * len(r[3]) + 6 if r[3] else 0) for r in rows) - 6


LW = 196                             # a side-tab list's width: "prior work on <the policy>" fits
PANEL_H = {"kv": lambda p: 22 * len(p[1]), "table": lambda p: 30 + 20 * len(p[2]), "line": lambda p: 22,
           "form": lambda p: 22 * len(p[1]), "btn": lambda p: 30}


def k_sidetabs(eid, x, y, w, items, panel):
    """Side tabs: the list on the left, the first open (blue); on the right the open one to read, its parts in order
    (a title line, kv lines, a small table, a form, buttons)."""
    els = []
    for k, (head_, word) in enumerate(items):
        iy = y + k * 44
        els += [_el("rectangle", f"{eid}{k}", x, iy, LW, 38, BLUE if k == 0 else ROOM, "#e7f5ff" if k == 0 else "#ffffff",
                    roundness={"type": 3})]
        els += text(f"{eid}{k}_t", x + 8, iy + 4, head_, 11, TITLE) + text(f"{eid}{k}_w", x + 8, iy + 21, word, 10, state_color(word))
    px, pw = x + LW + 12, w - LW - 12
    els += [_el("rectangle", eid + "_d", px, y, pw, sidetabs_h(items, panel) - 6, ROOM, "#ffffff", roundness={"type": 3})]
    yy = y + 10
    for j, p in enumerate(panel):
        kind, pid = p[0], f"{eid}_p{j}"
        if kind == "kv":
            for k, (n_, words) in enumerate(p[1]):
                els += text(f"{pid}{k}k", px + 12, yy + 22 * k, n_, 11, BODY)
                els += text(f"{pid}{k}v", px + (80 if n_ else 12), yy + 22 * k, words, 11,
                            BLUE if words.endswith("↗") else state_color(words) if words[:1] in "🙋✅⏳⬜✓" else INK)
        elif kind == "table":                    # each column as wide as its words
            cols, rows = p[1], p[2]
            wid = [max([len(cols[c])] + [len(r[c]) for r in rows]) + 2 for c in range(len(cols))]
            unit = min(CH * 10, (pw - 24) / sum(wid))
            xs = [px + 12 + unit * sum(wid[:c]) for c in range(len(cols))]
            for c, col in enumerate(cols):
                els += text(f"{pid}h{c}", xs[c], yy, col, 10, TITLE)
            for i, r in enumerate(rows):
                els += line(f"{pid}l{i}", [(px + 12, yy + 17 + 20 * i), (px + pw - 12, yy + 17 + 20 * i)], "#e9ecef", 1)
                for c, cell in enumerate(r):
                    els += text(f"{pid}r{i}_{c}", xs[c], yy + 21 + 20 * i, cell, 10, INK)
        elif kind == "line":
            els += text(pid, px + 12, yy, p[1], 11, BLUE if p[1].endswith("↗") else TITLE)
        elif kind == "form":                     # a form's questions and their choices, the person's pick ticked
            for k, (n_, words) in enumerate(p[1]):
                if n_ in ("A", "B", "C"):
                    els += [_el("ellipse", f"{pid}{k}o", px + 12, yy + 22 * k + 2, 11, 11, INK,
                                INK if "my pick" in words else "#ffffff")]
                    els += text(f"{pid}{k}t", px + 30, yy + 22 * k, f"{n_} · {words}", 11, INK)
                else:
                    els += text(f"{pid}{k}t", px + 12, yy + 22 * k, (f"{n_} · " if n_ else "") + words, 11, TITLE if n_ else BODY)
        elif kind == "btn":
            els += _btns(pid, px + pw - 12, yy, p[1], OR if p[1][0].startswith("Copy feedback") else BLUE)
        yy += PANEL_H[kind](p)
    return els


def sidetabs_h(items, panel):
    return max(44 * len(items), 16 + sum(PANEL_H[p[0]](p) for p in panel)) + 6


def k_tree(eid, x, y, w, root, branches):
    """The map, as the live parts_mindmap draws it: the root on the left, a branch per node, its small pill (job 1,
    task 1, ✎ drawing) above its name and one plain line; its children on the right (Open all, Close all open them)."""
    rows = [branch_h(ch) for *_, ch in branches]
    tot = sum(r + 10 for r in rows) - 10
    rh = 18 + 14 * (root.count("\n") + 1)
    ry = y + tot / 2 - rh / 2
    els = [_el("rectangle", eid + "_r", x, ry, 120, rh, INK, "#ffffff", roundness={"type": 3})]
    els += text(eid + "_rt", x + 8, ry + 9, root, 11, INK)
    by = y
    for k, (pill, name, words, children) in enumerate(branches):
        bh = rows[k]
        cy = by + bh / 2
        n = sum(1 for t in (pill, name, words) if t)
        ty = cy - 7 * n - 1
        els += line(f"{eid}{k}_l", [(x + 120, ry + rh / 2), (x + 140, cy)], ROOM, 1)
        els += [_el("rectangle", f"{eid}{k}", x + 140, cy - 27, 220, 54, INK, "#ffffff", roundness={"type": 3})]
        for j, (t_, size, col) in enumerate(((pill, 10, BODY), (name, 12, TITLE), (words, 11, BODY))):
            if t_:
                els += text(f"{eid}{k}_{j}t", x + 150, ty, t_, size, col)
                ty += 15
        if children:
            els += text(f"{eid}{k}_sh", x + 322, cy - 24, "▸ show", 9, BODY)
        for j, cn in enumerate(children):
            chy = by + (bh - 30 * len(children)) / 2 + 30 * j + 2
            els += line(f"{eid}{k}_{j}_l", [(x + 360, cy), (x + 380, chy + 13)], ROOM, 1)
            els += [_el("rectangle", f"{eid}{k}_{j}", x + 380, chy, w - 380, 26, ROOM, "#ffffff", roundness={"type": 3})]
            els += text(f"{eid}{k}_{j}_n", x + 388, chy + 6, cn, 11, state_color(cn) if cn[:1] in "🙋✅⬜" else INK)
        by += bh + 10
    return els


def branch_h(children):
    return max(56, 30 * len(children))


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


def k_trows(eid, x, y, w, items):
    """Studio rows as live: the topic's address small, its short name with its stage and kind as pills, its line, its
    verbs (a waiting form adds the orange 🙋 Interaction), its picture on the right."""
    els, ry = [], y
    for k, (addr, name, stage, kind, words, verbs, asks) in enumerate(items):
        h = trow_h(words)
        els += [_el("rectangle", f"{eid}{k}", x, ry, w, h, ROOM, "#ffffff", roundness={"type": 3})]
        els += text(f"{eid}{k}_a", x + 14, ry + 10, addr, 10, BODY)
        els += text(f"{eid}{k}_n", x + 14, ry + 26, name, 14, TITLE)
        px = x + 14 + CH * 14 * len(name) + 10
        for j, (pill, col) in enumerate(((stage, ROOM), (kind, BLUE))):
            pw = 14 + 6.6 * len(pill)
            els += [_el("rectangle", f"{eid}{k}_p{j}", px, ry + 27, pw, 18, col, "#ffffff", roundness={"type": 3})]
            els += text(f"{eid}{k}_p{j}t", px + 7, ry + 29, pill, 10, col)
            px += pw + 6
        els += text(f"{eid}{k}_w", x + 14, ry + 52, words, 12, INK)
        bx, by = x + 14, ry + h - 30
        for j, v in enumerate(verbs + (("🙋 Interaction",) if asks else ())):
            bw = 16 + 7.2 * len(v)
            you = v.startswith("🙋")
            els += [_el("rectangle", f"{eid}{k}_v{j}", bx, by, bw, 24, OR if you else ROOM, "#fff4e6" if you else "#ffffff",
                        roundness={"type": 3})] + text(f"{eid}{k}_v{j}t", bx + 8, by + 5, v, 11, OR if you else INK)
            bx += bw + 6
        tx = x + w - 134                                 # the topic's drawing, small: three boxes and their arrows
        els += [_el("rectangle", f"{eid}{k}_th", tx, ry + 12, 120, h - 24, ROOM, GHOST)]
        els += line(f"{eid}{k}_thl", [(tx + 8, ry + 24), (tx + 60, ry + 24)], ROOM, 1)
        for j in range(3):
            bx_ = tx + 8 + 38 * j
            els += [_el("rectangle", f"{eid}{k}_th{j}", bx_, ry + 34 + 10 * (j % 2), 28, 22, ROOM, "#ffffff")]
            if j:
                els += arrow(f"{eid}{k}_ta{j}", [(bx_ - 9, ry + 45), (bx_ - 1, ry + 45)], ROOM)
        ry += h + 8
    return els


def trow_h(words):
    return 104 + 16 * words.count("\n")


def _red(els):
    """A proposal's content: its edges red (a proposal the live page does not have yet)."""
    for e in els:
        if e["type"] == "rectangle" and e["strokeColor"] in (ROOM, "#e9ecef", INK, BLUE, OR):
            e["strokeColor"] = RE
    return els


KIND = {"note": (k_note, lambda a: 14 * (a[0].count("\n") + 1)), "waitline": (k_waitline, lambda a: 24),
        "todo": (k_todo, lambda a: 50 * len(a[0]) - 6), "list": (k_list, lambda a: 24 * len(a[0]) - 6),
        "runs": (k_runs, lambda a: 24 * len(a[0])), "fold": (k_fold, lambda a: 22 * len(a[0]) - 4),
        "jobrows": (k_jobrows, lambda a: jobrows_h(a[0])), "sidetabs": (k_sidetabs, lambda a: sidetabs_h(*a)),
        "tree": (k_tree, lambda a: tree_h(a[1])), "verbs": (k_verbs, lambda a: 22),
        "trows": (k_trows, lambda a: sum(trow_h(r[4]) + 8 for r in a[0]) - 8)}


def S(title, word="", share=None, red=False, flag=False, wait=""):
    """A section's heading bar: closed (▸), as every section starts; its state word and its thin bar on the right, as
    live; red, a proposal, unnumbered; flag, a 🙋 Interaction that waits for you (an orange edge); wait, the one thing
    that waits on the person, its line under the closed bar (live band-wait)."""
    return {"t": title, "w": word, "s": share, "red": red, "flag": flag, "wait": wait}


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
    dashed line ("none": the bar alone, as on Work, whose Results repeat the Report's); a group heading (⚙️ Process,
    📊 Results)."""
    if sec[0] == "group":
        return text(eid, x, y + 6, sec[1], 16, INK) + line(eid + "_l", [(x + 130, y + 18), (x + w, y + 18)], PALE, 1)
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
        els += text(eid + "_w", right - CH * 11 * len(word), y + 8, word, 11, RE if b["red"] else state_color(word))
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


def goal_h(level):
    return 46 + 17 * PAGE[level][3].count("\n")


def screen(eid, x, y, h, level, section, views, on, secs, caption):
    """One view as the full page: window, both rails, then in the content column the path, the title-&-section, the
    view-button-list, the goal-line (its label above, a rule under), the view-caption and its sections."""
    name, path, label, goal = PAGE[level]
    els = window(eid + "w", x, y, W, h, f"/_board/workbench?layout=focus&path=…/{name}&section={section}")
    els += rails(eid + "rl", x, y, level, section)
    cx = x + X0
    lines = crumb_lines(path)
    for k, ln in enumerate(lines):
        els += text(f"{eid}_crumb{k}", cx, y + 40 + 14 * k, ln, 10, BODY)
    top = y + 46 + 14 * len(lines)
    els += head(eid + "h", cx, top, name, section, views, on)
    els += text(eid + "_gl", cx, top + 70, label, 10, BODY) + text(eid + "_goal", cx, top + 86, goal, 13, INK)
    gy = top + 86 + 17 * (goal.count("\n") + 1) + 6
    els += line(eid + "_goall", [(cx, gy), (cx + CW, gy)], PALE, 1)
    top += goal_h(level)
    els += text(eid + "_cap", cx, top + 76, caption, 12, BODY) if caption else []
    yy = top + 106 if caption else top + 80
    for k, sec in enumerate(secs):
        els += sec_draw(f"{eid}r{k}", cx, yy, CW, sec)
        yy += sec_h(sec)
    return els


# ── the views (view, its view-caption, its sections in page order) ─────────────────────────────────────────────────
G_PROC, G_RES = ("group", "⚙️ Process"), ("group", "📊 Results")
MAP_CAP = "How it is built, as a map: its parts, and what each must find out."
FIND_CAP = "What it has found so far, and what it hands over."
OPEN_CLOSE = ("", "verbs", ("Open all", "Close all"))

# ── the forms, and which view's 🙋 holds each (as live, 261108: a Block's Findings holds the forms below it, a Job's
# and a Task's Status): a form is (its tab, its questions as side tabs, the open form's panel, its waiting line, its word)
ORDER = ("Citation check order", (("Q1 · First check", "waiting"), ("Q2 · After the check", "waiting")),
         (("line", "Citation check order"),
          ("form", (("Q1", "Which citation does a person check first?"),
                    ("A", "r03 (@example2022two), the one marked NEEDS · my pick"),
                    ("B", "r01 (@example2024policy), the one cited first"),
                    ("Q2", "Close the Task right after the check?"),
                    ("A", "Yes, and rebuild the Evidence Bib first · my pick"),
                    ("B", "No, read r03's full text before closing"))),
          ("kv", (("asked by", "prior work on <the policy>"), ("about", "Which paper to check first · s03"))),
          ("btn", ("Copy feedback",))),
         "🙋 Citation check order: Q1 · First check", "2 wait for you")
RULES = ("Citation check rules", (("Q1 · Verification line", "my own decision"),),
         (("line", "Citation check rules"),
          ("form", (("Q1", "A Card's verification line says when a person checks it"), ("", "✓ my own decision"))),
          ("kv", (("asked by", "prior work on <the policy>"), ("about", "How the example papers are read · s01")))),
         "", "answered")
IX_OF = {("block", "Findings"): (ORDER, RULES), ("job", "Status"): (ORDER, RULES), ("task", "Status"): (ORDER, RULES)}


def ix(level, view, n=0):
    """🙋 Interaction, the view's last section, holding this view's own forms: its state word, its first waiting
    question under the closed bar; a side tab per form (one form: per question) and the open one's form on the right;
    "nothing yet" when the view has none."""
    title = (f"{n} · " if n else "") + "🙋 Interaction"
    forms = IX_OF.get((level, view), ())
    if not forms:
        return (S(title, "nothing yet"), "none")
    first = forms[0]
    tabs = first[1] if len(forms) == 1 else tuple((f[0], f[4]) for f in forms)
    return (S(title, first[4], flag=bool(first[3]), wait=first[3]), "sidetabs", tabs, first[2])


def closing(secs, level, view):
    """The view's sections, then its 🙋 Interaction numbered after the last band's numbered sections (unnumbered when
    that band has none, as live)."""
    last = max([i for i, s in enumerate(secs) if s[0] == "group"], default=-1)
    nums = [int(m.group(1)) for s in secs[last + 1:] if s[0] != "group"
            for m in [re.match(r"(\d+) · ", bar_of(s[0])["t"])] if m]
    return tuple(secs) + (ix(level, view, max(nums) + 1 if nums else 0),)


def same(letter, view):
    """Work's 📊 Results repeat the Report's view, drawn by the same code: its bars drawn closed here, the content
    is the Report's letter."""
    return ("", "note", f"the Report's {letter} · {view}, drawn by the same code")


def bars(secs):
    """A Report view's sections as Work repeats them: its waiting line, then each numbered section as a closed bar."""
    return tuple(s if s[1] == "waitline" else (s[0], "none") for s in secs
                 if s[0] != "group" and (bar_of(s[0])["t"] or s[1] == "waitline"))


def report(level, items):
    return tuple((v, cap, closing(secs, level, v)) for v, cap, secs in items)


def work(level, report_items, process):
    """Each Work view: ⚙️ Process when it has a step (a proposal alone stands without the heading), then 📊 Results,
    the Report's view by the same code."""
    out = []
    for k, (v, _, secs) in enumerate(report_items):
        cap, proc = process[v]
        pre = () if not proc else proc if all(bar_of(s[0])["red"] for s in proc) else (G_PROC,) + proc
        out.append((v, cap, closing(pre + (G_RES, same(LETTERS[k], v)) + bars(secs), level, v)))
    return tuple(out)


# ── the discovery parts, as discovery_focus draws them, the same at every level ─────────────────────────────────────
PAPER_TABS = (("Example 2024 · policy", "abstract read"), ("Example 2021 · one", "abstract read"),
              ("Example 2022 · two", "waits for you"))


def paper_panel(task_row):
    """The open paper's Card: its title, what it found, how it was read and checked, where it is reused; at a Block
    and a Job the Task it sits in."""
    kv = (("", "<the policy> raised <an outcome> the year after it began"), ("cite", "@example2024policy"),
          ("venue", "Example Journal (2024)"), ("read", "abstract read · claim supported"),
          ("check", "✅ title, authors and year agree"), ("signed", "not yet"),
          ("reuse", "the introduction's first sentence"))
    kv += (("task", "prior work on <the policy>"),) if task_row else ()
    return (("line", "<A policy> and <a service>: a placeholder study"), ("kv", kv),
            ("line", "Open the Run ↗ · Card ↗ · BibTeX ↗ · Source ↗"))


PAPER_WAIT = "🙋 Example 2022 · two: its verification waits for you"
BIB_PANEL = (("line", "t01_policy_prior_work.bib ↗ · handed over: v1, a draft"),
             ("table", ("key", "title", "Run"), (("@example2021one", "<An outcome> in one setting", "r02"),
                                                 ("@example2022two", "<An outcome> in a second setting", "r03"),
                                                 ("@example2024policy", "<A policy> and <a service>", "r01"))),
             ("line", "▸ The BibTeX"))
SYN_PANEL = (("line", "summary.md ↗"),
             ("kv", (("found", "two papers: <the policy> raised <an outcome>"), (" ", "in one setting; the third adds a setting only"),
                     ("agree", "<an outcome> rose after <the policy> began"), ("open", "r03's setting: its citation check waits"),
                     ("none did", "split it by <a characteristic>: j02's question"),
                     ("", "every paper here is made up"))))
DELIVERY_PANEL = (("kv", (("", "t01_policy_prior_work-v1.bib · a draft"),
                          ("", "from j01_policy_effect_inquiry/t01_policy_prior_work/bib"))),)
TASK_TAB = "prior work on <the policy>"


def papers(n, task_row=True):
    return (S(f"{n} · 📚 Papers", "1 waits for you", wait=PAPER_WAIT), "sidetabs", PAPER_TABS, paper_panel(task_row))


def bib(n):
    return (S(f"{n} · 📖 Evidence Bib", "built"), "sidetabs", ((TASK_TAB, "built"),), BIB_PANEL)


def synthesis(n, word):
    return (S(f"{n} · 🧾 Synthesis", word), "sidetabs", ((TASK_TAB, "topic summary"),), SYN_PANEL)


def delivery_(n):
    return (S(f"{n} · 📦 Delivery", "ready"), "sidetabs", (("Evidence Bib", "ready"),), DELIVERY_PANEL)


def topic_row(nn, asks=None):
    """A Studio topic's row, as live: s01 at the Block, s02 at the Job, s03 at the Task."""
    return {"s01": ("b01-s01:example_prior_work @", "example_reading", "shaping", "skill",
                    "A placeholder topic: the path from a paper to the Bib\na paper cites, and where a person checks a citation.",
                    ("Draw", "Mind map", "Delivery", "Interaction"), False),
            "s02": ("b01.j01-s02:example_prior_work.policy_effect_inquiry @", "inquiry_scope", "agreed", "skill",
                    "A placeholder topic: one inquiry, one question,\none rule for what enters.",
                    ("Draw", "Mind map", "Work", "Delivery"), False),
            "s03": ("b01.j01.t01-s03:example_prior_work.policy_effect_inquiry.policy_prior_work @", "check_order",
                    "explore", "skill", "A placeholder topic: one paper's citation waits for a person;",
                    ("Draw", "Mind map", "Work", "Delivery"), True)}[nn]


# ── the Block (s51 Report, s52 Work, s53 Studio) ─────────────────────────────────────────────────────────────────────
BLOCK_MAP = (OPEN_CLOSE, ("", "tree", "b01_example_\nprior_work", (
    ("", "Questions", "each with its answer's state", ("✅ the earlier effect: agreed", "🙋 the setting: your call",
                                                       "⬜ the subgroup: no answer yet")),
    ("✎ drawing", "How the papers are read", "s01 · example_reading", ()),
    ("job 1", "what earlier work found", "about <the policy>", ("t01 · prior work on <the policy>",)),
    ("job 2", "whether the effect differs", "by <a characteristic>", ("t01 · prior work, <the subgroup>",)))))
J01_KIDS = ((1, "t01_policy_prior_work", "🙋 waiting on you", ""),
            (2, "r01_example2024_policy", "✅ done", "<the policy> raised <an outcome>"),
            (2, "r02_example2021_one", "✅ done", "it rose again a second year"),
            (2, "r03_example2022_two", "✅ done", "metadata only: a second setting"),
            (2, "r04_collect_example_check_order", "🙋 waiting for you", ""),
            (2, "r05_collect_example_check_rules", "✅ done", ""),
            (2, "run-deliver-bib", "✅ done", "3 papers in the Bib; 1 check waits"))
BLOCK_STATUS = (
    (S("1 · 🧱 Jobs", "not run", 0.0), "jobrows", (("🧱 j01 · what earlier work found", "not run", 0.0, J01_KIDS, "🙋 Answer"),
                                                  ("🧱 j02 · whether the effect differs", "not run", 0.0,
                                                   ((1, "t01_subgroup_prior_work", "⬜ planned", ""),)))),
    (S("2 · 🎨 Studio", "1 shaping, 1 agreed, 1 exploring"), "list",
     (("How the example papers are read", "shaping"), ("What the policy inquiry admits", "agreed"),
      ("Which paper to check first", "exploring"))))
BLOCK_FINDINGS = (
    (S("1 · ❓ Prior work", "waits for you", wait="🙋 The setting: its answer waits for your agreement"), "sidetabs",
     (("The earlier effect", "answered"), ("The setting", "proposed, waiting for you")),
     (("line", "The earlier effect · answered · Read full report ↗"),
      ("kv", (("asks", "what did earlier work find about <the policy>?"),
              ("answer", "two papers: <the policy> raised <an outcome>"), (" ", "in one setting; a third, metadata only"),
              ("found by", "prior work on <the policy> ↗"))))),
    (S("2 · ❓ Subgroups", "no answer yet"), "sidetabs", (("The subgroup", "no answer yet"),),
     (("line", "The subgroup · no answer yet"),
      ("kv", (("asks", "did any earlier work look at the effect"), (" ", "by <a characteristic>?"),
              ("found by", "prior work on <the subgroup>: no paper yet"))))),
    papers(3), bib(4), synthesis(5, "1 of 2 written"), delivery_(6))
BLOCK_R = (
    ("MindMap", MAP_CAP, BLOCK_MAP),
    ("Status", "Where its Jobs, Tasks and Studio topics stand.", BLOCK_STATUS),
    ("Findings", FIND_CAP, BLOCK_FINDINGS),
)
BLOCK_REPORT = report("block", BLOCK_R)
BLOCK_WORK = work("block", BLOCK_R, {
    "MindMap": (MAP_CAP, ()),                     # nothing to do on the map: no ⚙️ Process
    "Status": ("Where its Jobs, Tasks and Studio topics stand.", (
        (S("1 · 🚧 Next steps", "2 to do"), "todo",
         (("prior work on <the policy>", "in what earlier work found about <the policy>", "🙋 waiting on you", "Open"),
          ("prior work on <the subgroup>", "in whether the effect differs by <a characteristic>", "planned", "Open"))),)),
    "Findings": (FIND_CAP, (
        (S("1 · ✍️ Answers to write or agree", "1 waits for you", wait="🙋 The setting: its answer waits for your agreement"),
         "todo", (("The setting", "proposed: in which settings was the effect measured?", "🙋 waiting for you", "Agree"),
                  ("The subgroup", "no answer yet: no paper is admitted", "no answer yet", "Write"))),)),
})
BLOCK_STUDIO = (("Topics", "", (("", "trows", (topic_row("s01"), topic_row("s02"), topic_row("s03"))),)),)

# ── the Job (s54 Report, s55 Work, s56 Studio) ───────────────────────────────────────────────────────────────────────
JOB_MAP = (OPEN_CLOSE, ("", "tree", "j01_policy_\neffect_inquiry", (
    ("task 1", "prior work on <the policy>", "", ("finds out what earlier work found",)),)))
JOB_STATUS = (
    ("", "waitline", "waiting on you", "one paper's citation to check"),
    (S("1 · 🧱 Tasks", "0 of 1 done", 0.0), "fold",
     ((1, "prior work on <the policy>", "🙋 waiting on you", "3 papers, 1 check waits", "🙋 Answer"),) + J01_KIDS[1:]))
JOB_FINDINGS = (
    (S("1 · 📌 Headlines", "1 of 1 returned"), "sidetabs", ((TASK_TAB, "waiting on you"),),
     (("kv", (("", "two papers find <the policy> raised <an outcome>"),
              ("", "in one setting; the third adds a setting, no finding"))),
      ("line", "Open t01_policy_prior_work ↗"),
      ("kv", (("", "run-deliver-bib ↗ · headline.txt · facts.json"),)))),
    papers(2), bib(3), synthesis(4, "written"), delivery_(5))
JOB_R = (
    ("MindMap", MAP_CAP, JOB_MAP),
    ("Status", "Where its Tasks stand, each with its newest result.", JOB_STATUS),
    ("Findings", FIND_CAP, JOB_FINDINGS),
)
JOB_REPORT = report("job", JOB_R)
JOB_WORK = work("job", JOB_R, {
    "MindMap": (MAP_CAP, ()),
    "Status": ("Where its Tasks stand, each with its newest result.", (
        (S("1 · 🚧 Next steps", "1 to do"), "todo",
         (("r04_collect_example_check_order", "in prior work on <the policy>", "🙋 waiting for you", "Open"),)),)),
    "Findings": (FIND_CAP, ()),                   # no question to answer at a Job: no ⚙️ Process, as live
})
JOB_STUDIO = (("Topics", "", (("", "trows", (topic_row("s02"), topic_row("s03"))),)),)

# ── the Task (s57 Report, s58 Work, s59 Studio) ──────────────────────────────────────────────────────────────────────
TASK_MAP = (OPEN_CLOSE, ("", "tree", "t01_policy_\nprior_work", (
    ("", "Runs", "each with what it says", ("r01 · a paper, from its abstract", "r02 · a second, from its abstract",
                                             "r03 · a third, metadata only", "r04 · Citation check order",
                                             "r05 · Citation check rules", "run-deliver-bib · Evidence Bib")),)))
TASK_STATUS = (
    papers(1, task_row=False), bib(2), synthesis(3, "written"),
    (S("4 · 🧪 Runs", "5 of 6 done · 1 waiting"), "runs",
     (("✅ done", "r01_example2024_policy", "<the policy> raised <an outcome>"),
      ("✅ done", "r02_example2021_one", "it rose again a second year"),
      ("✅ done", "r03_example2022_two", "metadata only: a second setting"),
      ("🙋 waiting for you", "r04_collect_example_check_order", ""),
      ("✅ done", "r05_collect_example_check_rules", ""),
      ("✅ done", "run-deliver-bib", "3 papers in the Bib; 1 check waits"))))
TASK_R = (
    ("MindMap", MAP_CAP, TASK_MAP),
    ("Status", "What its newest Run returned, and where its Runs stand.", TASK_STATUS),
)
TASK_REPORT = report("task", TASK_R)
TASK_WORK = work("task", TASK_R, {
    "MindMap": (MAP_CAP, ()),
    "Status": ("What its newest Run returned, and where its Runs stand.", (   # live has no ⚙️ Process: a proposal
        (S("⚙️ Process · 🚧 Next steps", red=True), "todo",
         (("r04_collect_example_check_order", "check r03's citation first, then close the Task", "🙋 waiting for you", "Open"),)),)),
})
TASK_STUDIO = (("Topics", "", (("", "trows", (topic_row("s03"),)),)),)

CLOSED = ("every section starts closed (▸), its state word on its right, a waiting line under one that waits on you; "
          "what it opens to is drawn under its bar, behind a dashed line")
OWN = "🙋 Interaction is every view's last section and holds its own forms"
RAIL = "the right rail: Report · Work · Studio · Interactions · Delivery · Timeline · Skills · Files, as served 261108"
PARTS = "📚 Papers a side tab a paper, 📖 Evidence Bib its entries then the BibTeX, 🧾 Synthesis the topic summary"
RAIL2 = "the right rail: Report · Work · Studio · Interactions · Delivery · Timeline ·\nSkills · Files, as served 261108"   # one screen wide
VIEWS = {   # (level, section): (the line above the screens, the views, the open question)
    ("block", "report"): ("MindMap · Status · Findings, as the live discovery page draws them (261108); Findings: one ❓ section per question\n"
                          "group, then " + PARTS + ", 📦 Delivery;\n" + CLOSED + ";\n" + OWN + "; " + RAIL,
                          BLOCK_REPORT, "? agree A to C: they\nfollow the live page"),
    ("block", "work"): ("the same views as Report: ⚙️ Process when it has a step (B 🚧 Next steps, C ✍️ Answers to write or agree),\n"
                        "then 📊 Results by the same code; " + CLOSED + ";\n" + OWN + "; " + RAIL, BLOCK_WORK,
                        "? A has no ⚙️ Process:\nnothing to do on a map"),
    ("block", "studio"): ("one view, Topics: the Block's topic and its Job's and Task's, flat rows as live:\n"
                          "the address, the short name, its stage and kind, its line, its verbs, its picture;\n"
                          "no 🙋 Interaction section on Studio; " + RAIL2,
                          BLOCK_STUDIO, "? one flat list, or rows\ngrouped by level"),
    ("job", "report"): ("MindMap · Status · Findings, as live (261108); Status: the waiting line, then each Task opening to its Runs;\n"
                        "Findings: 📌 Headlines, then " + PARTS + ", 📦 Delivery;\n" + CLOSED + ";\n" + OWN + "; " + RAIL,
                        JOB_REPORT, "? C's Papers waits, its\n🙋 says nothing yet"),
    ("job", "work"): ("the same views as Report: ⚙️ Process when it has a step (B 🚧 Next steps), then 📊 Results by the same code;\n"
                      "C has no Process (no question to answer at a Job); " + CLOSED + ";\n" + OWN + "; " + RAIL, JOB_WORK,
                      "? a check step in C's\nProcess too"),
    ("job", "studio"): ("one view, Topics: the Job's own topic and its Task's, flat rows as live;\n" + RAIL2, JOB_STUDIO,
                        "? the short address:\nb01-s02 @ inquiry_scope"),
    ("task", "report"): ("MindMap · Status, as live (261108): a Task page has no Findings, so its Status holds " + PARTS + ",\n"
                         "then 🧪 Runs; its goal-line the question's Aim;\n" + CLOSED + ";\n" + OWN + ";\n" + RAIL,
                         TASK_REPORT, "? split Status into\nStatus and Findings"),
    ("task", "work"): ("the same views as Report, 📊 Results by the same code; live has no ⚙️ Process on a Task: red, 🚧 Next steps,\n"
                       "as the Block and the Job have it, a proposal;\n" + CLOSED + ";\n" + OWN + ";\n" + RAIL, TASK_WORK,
                       "? 🚧 Next steps on a\nTask's Work (red)"),
    ("task", "studio"): ("one view, Topics: the Task's own topic, its form waiting (the orange 🙋 Interaction);\n" + RAIL2, TASK_STUDIO,
                         "? agree A: it follows\nthe live page"),
}
# what changed on each letter's screen: every screen is new (261108), each with its dated green ✎ notes
D8 = "261108"
NOTES = {
    ("block", "report"): {"A": [(D8, "new: the live Block map"), (D8, "questions with their answer's state"),
                                (D8, "a branch a Job, its Task under it")],
                          "B": [(D8, "new: Status, 🧱 Jobs fold to Tasks and Runs"), (D8, "🎨 Studio: each topic's stage")],
                          "C": [(D8, "new: Findings, a ❓ section a question group"), (D8, "📚 Papers, 📖 Evidence Bib, 🧾 Synthesis"),
                                (D8, "🙋 holds both citation-check forms")]},
    ("block", "work"): {"A": [(D8, "new: 📊 Results only, no Process")],
                        "B": [(D8, "new: ⚙️ 🚧 Next steps, a row a Task"), (D8, "📊 Results = the Report's B")],
                        "C": [(D8, "new: ⚙️ ✍️ Answers to write or agree"), (D8, "the setting waits: Agree")]},
    ("block", "studio"): {"A": [(D8, "new: one view, Topics, flat rows"), (D8, "s01, s02, s03: Block, Job and Task"),
                                (D8, "s03's row: 🙋 Interaction, its form waits")]},
    ("job", "report"): {"A": [(D8, "new: the Job's map, its Task")],
                        "B": [(D8, "new: Status, the waiting line on top"), (D8, "🧱 Tasks fold to their Runs; 🙋 2 wait")],
                        "C": [(D8, "new: Findings, 📌 Headlines first"), (D8, "📚 Papers, 📖 Evidence Bib, 🧾 Synthesis")]},
    ("job", "work"): {"A": [(D8, "new: 📊 Results only, no Process")],
                      "B": [(D8, "new: ⚙️ 🚧 Next steps: the check Run")],
                      "C": [(D8, "new: 📊 Results only, as live")]},
    ("job", "studio"): {"A": [(D8, "new: one view, Topics: s02 and s03"), (D8, "s03's row: 🙋 Interaction, its form waits")]},
    ("task", "report"): {"A": [(D8, "new: the Task's map, a Run a leaf"), (D8, "goal-line: the question's Aim")],
                         "B": [(D8, "new: Status holds the discovery parts"), (D8, "🧪 Runs: 5 of 6 done · 1 waiting"),
                               (D8, "🙋 holds both citation-check forms")]},
    ("task", "work"): {"A": [(D8, "new: 📊 Results only, no Process")],
                       "B": [(D8, "new: 📊 Results = the Report's B"), (D8, "red: 🚧 Next steps, a proposal")]},
    ("task", "studio"): {"A": [(D8, "new: one view, Topics: s03"), (D8, "its form waits: 🙋 Interaction")]},
}
PIECE = {   # the why notes: what b14 had before this Job (261108)
    ("block", "report"): ("the Block's Report: its map, its Status, its Findings",
                          ["b14 drew no screen of\nthe live Block page", "papers, Bib and synthesis\nnow sit in Findings",
                           "the old four Spaces\n(s02) are retired"]),
    ("block", "work"): ("the Block's Work: Process, then the Report's views",
                        ["Work's steps were in\nthe old Scope Space", "what waits on you had\nno place of its own",
                         "the other themes draw\ntheir Work: b14 did not"]),
    ("block", "studio"): ("the Block's Studio: its topics, at every level",
                          ["s01 to s03 sat in\nthree folders", "no screen showed which\ntopic waits on you",
                           "the old page had\nno Studio"]),
    ("job", "report"): ("a Job's Report: its map, its Status, its Findings",
                        ["the old page had no\nJob level at all", "a Job's headline was\nnowhere on screen",
                         "papers sat only on\nthe Block"]),
    ("job", "work"): ("a Job's Work: Process, then the Report's views",
                      ["a waiting check Run\nhid in the Task", "no Next steps at\nthe Job", "the old Check Space\nheld the Runs"]),
    ("job", "studio"): ("a Job's Studio: its own topic and its Task's",
                        ["no Studio at the Job", "s02 had no screen", "the address prints\nthe whole path"]),
    ("task", "report"): ("a Task's Report: its map, then its Status",
                         ["the Task page had\nno discovery parts", "a NEEDS check was\nonly on its Card",
                          "the Bib sat in\nthe old Delivery"]),
    ("task", "work"): ("a Task's Work: the Report's views, and a proposal",
                       ["a Task's Work has\nno Next steps", "the waiting check\nsits in Runs only",
                        "Block and Job have\na Process: the Task not"]),
    ("task", "studio"): ("a Task's Studio: its own topic",
                         ["s03 had no screen", "its waiting form showed\nonly in its folder", "the old page had\nno Studio"]),
}
TARGET = {"report": "servers/workbench-discovery/discovery_focus.py · workbench-discovery/SKILL.md",
          "work": "servers/workbench-discovery/discovery_focus.py · workbench-discovery/SKILL.md",
          "studio": "servers/workbench/focus_page.py · workbench-discovery/SKILL.md"}

AGREED = {}                            # (level, section): {letter: sections}, the letters settled so far; none yet
MOCK = """<!doctype html><meta charset=utf-8><title>{letter} · {view}</title>
<!-- GENERATED by discovery_ui_cells.py from AGREED; the agreed screen of {nn} view {letter} -->
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
    lines = len(crumb_lines(PAGE[level][1]))
    return 200 + 14 * lines + goal_h(level) + max(tall(secs) for _, _, secs in items)


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
    if sec[1] == "none":
        return bar_of(sec[0])["t"], ""
    words = {"tree": lambda: " · ".join(b[1] for b in sec[3]), "sidetabs": lambda: " · ".join(h for h, _ in sec[2]),
             "todo": lambda: " · ".join(r[0] for r in sec[2]), "trows": lambda: " · ".join(r[1] for r in sec[2]),
             "jobrows": lambda: " · ".join(r[0] for r in sec[2]), "fold": lambda: " · ".join(r[1] for r in sec[2]),
             "runs": lambda: " · ".join(r[1] for r in sec[2]), "list": lambda: " · ".join(n for n, _ in sec[2]),
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
    pieces.append(("book", f"skill/{sk.name}", "the views' manual, for workbench-discovery", sk.exists()))
    spec = {"title": f"{level.capitalize()} UI · {VERB[section]}: {piece.split(': ', 1)[1]}",
            "why": {"question": f"why do we need s{nn}?", "notes": why,
                    "quote": "asked 261108: draw the discovery 3 × 3 from the live discovery pages"},
            "what": {"head": f"② what s{nn} hands over: one screen, A to {last}", "icon": "page", "name": "delivery/ui/",
                     "type": "ui", "deck_why": f"stays in s{nn}'s delivery/deck/, so anyone gets it in a minute", "parts": pieces},
            "job": topic.parent.parent,
            "target": TARGET[section],
            "missing": [(name, "not settled yet") for _, name, _, done in pieces if not done],
            "have": [(name, "agreed") for icon, name, _, done in pieces if done and icon == "page"]}
    notes = NOTES.get((level, section), {})

    def design():                                    # A, B, C … every view the same screen
        els = text("skA", 690, 280, f"A to {last} · {piece}, every view the same screen", 18, TITLE)
        els += text("lay", 690, 330, lay, 16, BODY)
        y = 356 + 20 * (lay.count("\n") + 1)
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


if __name__ == "__main__":                               # python discovery_ui_cells.py <topic folder> <letter> <out>
    print(letter_png(Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])))
