"""The nine sNN of j01 · The paper pages, level by level: one per level (Board, version, Section) and section (Report,
Work, Studio), each drawn in haipipe-studio's five parts (scripts/five_parts.py), as b17-s04. Each sNN's builder is
`build(Path(__file__).parent)`: its cell is found by its folder name (s32-board-ui-report → board, report).

A cell's Design is its page's views, lettered A, B, C …, each drawn as the same full screen (window, title and section
word, view buttons with that view in orange, its sections as heading bars with what each holds under it), three a row,
the open question in red under them (JL 261031: "could you make each of them to be the same size and format"). A view
is settled one round at a time; a settled view's screen is written to delivery/ui/ (AGREED). Names are placeholders: the
papers are unpublished and Tools is public. The draft step names come from draft_steps.STEPS on every build (JL 261031:
"I think it should be 3 x 3").

261105: each view is drawn as the live page draws it (servers/workbench-paper; workbench-task-draft/focus_draft.py;
focus_page.py). Every section bar starts closed (▸); under it, what it shows once opened. 🙋 Interaction is every
Report and Work view's last section (interaction_section.view_section), so Work's ⚙️ Process has no 🙋 step. A screen
that changed carries a green ✎ note per change under its letter, each with its date; the old notes stay.

261106: each closed bar carries its state word on its right, and a section that waits on the person its one waiting
line under the bar (ui_parts._section: `word`, `waits`); the words come from the same rules as the live page (a to-do
list's word is read from its rows' states, ui_parts.todo_word), with counts that match what the screen draws. 🙋
Interaction holds the view's own items only. Skills is a right-rail section, between Timeline and Files (focus_page.
render). A version's Report is MindMap, then Work's six views, results only (paper_version.version_report_views); the
evidence and submission Jobs' own pages (paper_jobs.py) are drawn under "Other Jobs" in the version cells, one row a
Job, their letters after the version's. A Job's MindMap shows each Task with its goal leaf, "finds out …".
"""
import random
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = next(p for p in HERE.parents if (p / "plugins/haipipe-toolkit").is_dir())
sys.path.insert(0, str(TOOLS / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))
from five_parts import *  # noqa: E402,F401,F403  (the helpers and build())
from five_parts import _el  # noqa: E402
from canvas import change_note  # noqa: E402
from quick_draw import WIDE  # noqa: E402  (a character's width per font size, to set a word flush right)
import five_parts  # noqa: E402

_ds = (TOOLS / "plugins/haipipe-toolkit/servers/workbench/workbench-task-draft/draft_steps.py").read_text(encoding="utf-8")
STEPS = [s for s in re.search(r"^STEPS = \((.*?)\)$", _ds, re.M).group(1).replace('"', "").split(", ") if s[:1].isdigit()]
VERB = {"report": "Report", "work": "Work", "studio": "Studio"}          # no verb after the section word (b10-s33-D06)
LIST = ("Idea", "Story", "Data + Paper Plan", "Support blocks", "Evidence", "Displays", "Writing")   # the Board's views (board_read.BOARD_VIEWS, 261105)
PAGE = {"board": ("Paper-Example", "…/paper/Paper-Example"),
        "version": ("j11_writing_v1130_venue", "…/Paper-Example/j11_writing_v1130_venue"),
        "section": ("t00_summary", "…/j11_writing_v1130_venue/t00_summary")}


# ── the screen's parts, drawn plainly ───────────────────────────────────────────────────────────────────────────
def window(eid, x, y, w, h, url):
    els = [_el("rectangle", eid, x, y, w, h, INK, "#ffffff", roundness={"type": 3})]
    els += line(eid + "_bar", [(x, y + 28), (x + w, y + 28)], ROOM, 1)
    return els + [_el("ellipse", f"{eid}_d{k}", x + 10 + k * 14, y + 9, 9, 9, ROOM, ROOM) for k in range(3)] + \
        text(eid + "_url", x + 60, y + 7, url, 12, BODY)


def head(eid, x, y, name, section, views, on=0, words=None):
    """The title-&-section, then the view-button-list, the open view in orange; a draft step's button carries its state
    word small after its name, as the page draws it (focus_page: `<span class=vw>`; `words`: {view: (label, word)})."""
    els = text(eid + "_t", x, y, name, 20, INK) + text(eid + "_s", x + 12 * len(name) + 20, y + 4, VERB[section], 15, ROOM)
    cx = x
    tight = not words and sum(12 + 8 * len(v) for v in views) + 8 * (len(views) - 1) > 570   # seven views: smaller, to fit
    for k, v in enumerate(views):
        label, word = (words or {}).get(v, (v, ""))
        w = (10 + 6.5 * len(label) + 8 + 5.5 * len(word)) if word else (8 + 6.4 * len(label)) if tight else 12 + 8 * len(label)
        els += [_el("rectangle", f"{eid}_v{k}", cx, y + 38, w, 24, OR if k == on else ROOM,
                    "#fff4e6" if k == on else "#ffffff", roundness={"type": 3})] + \
            text(f"{eid}_v{k}_t", cx + (4 if tight else 6), y + (44 if tight else 42), label, 10 if tight else 12, INK)
        if word:
            els += text(f"{eid}_v{k}_w", cx + 12 + 6.5 * len(label), y + 44, word, 10, BODY)
        cx += w + 8
    return els


def topic_row(eid, x, y, w, addr, words, stage):
    """A Studio topic as the page draws it: its name and stage, its line, Draw · Mind map, its picture on the right."""
    els = [_el("rectangle", eid, x, y, w, 68, ROOM, "#ffffff", roundness={"type": 3})]
    els += text(eid + "_a", x + 12, y + 8, addr, 13, TITLE) + text(eid + "_s", x + 22 + 7.5 * len(addr), y + 9, stage, 11, GR)
    els += text(eid + "_w", x + 12, y + 25, words, 11, BODY) + buttons(eid + "_v", x + 12, y + 42, ("Draw", "Mind map"))
    return els + [_el("rectangle", eid + "_p", x + w - 150, y + 6, 140, 56, ROOM, "#f1f3f5")]


# ── the nine cells: Idea's words, the delivery piece, the two sketches and their open questions ───────────────────
def secbar(eid, x, y, w, title, words):
    """A section as the page draws it now: a boxed heading bar that folds, closed at first, its content below it."""
    return ([_el("rectangle", eid, x, y, w, 30, ROOM, "#ffffff", roundness={"type": 3})]
            + text(eid + "_t", x + 12, y + 7, "▸ " + title, 13, TITLE) + text(eid + "_w", x + 12, y + 38, words, 11, BODY))


LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"   # one letter per screen; the Board's seven use A to G (261105); a version cell's
                                         # Other Jobs go on after its own views (261106)


def slug(view):
    return re.sub(r"[^a-z0-9]+", "-", view.lower()).strip("-")


BLUE = "#1864ab"                     # the workbench's colour for the current thing (frame.py :root)


def buttons(eid, x, y, verbs, color=INK):
    """Verb buttons, styled like Answer: a word in a small rounded box."""
    els, bx = [], x
    for k, v in enumerate(verbs):
        bw = 14 + 7.5 * len(v)
        els += [_el("rectangle", f"{eid}{k}", bx, y, bw, 24, ROOM, "#ffffff", roundness={"type": 3})] + \
            text(f"{eid}{k}_t", bx + 7, y + 5, v, 11, color)
        bx += bw + 6
    return els


def lead(eid, x, y, w, label, words, stage):
    """The view's main point, first and largest: a blue edge, its label, the sentence big, the picture beside it."""
    els = [_el("rectangle", eid, x, y, w, 124, ROOM, "#ffffff", roundness={"type": 3}),
           _el("rectangle", eid + "_e", x, y, 8, 124, BLUE, BLUE)]
    els += text(eid + "_l", x + 22, y + 12, label, 12, BLUE) + text(eid + "_s", x + w - 290, y + 12, stage, 12, GR)
    els += text(eid + "_w", x + 22, y + 34, words, 19, INK)
    els += [_el("rectangle", eid + "_p", x + w - 203, y + 12, 189, 74, ROOM, "#f1f3f5")]
    return els + buttons(eid + "_b", x + w - 203, y + 92, ("Slides", "Draw", "Mind map"))


def ask(eid, x, y, w, words, verb):
    els = [_el("rectangle", eid, x, y, w, 38, OR, "#fff4e6", roundness={"type": 3})]
    els += text(eid + "_t", x + 14, y + 10, words, 13, INK)
    return els + [_el("rectangle", eid + "_b", x + w - 96, y + 6, 82, 26, OR, "#ffffff", roundness={"type": 3})] + \
        text(eid + "_bt", x + w - 84, y + 11, verb, 12, OR)


def tiles(eid, x, y, w, items):
    tw = (w - 16 * (len(items) - 1)) / len(items)
    els = []
    for k, (t, words) in enumerate(items):
        tx = x + k * (tw + 16)
        els += [_el("rectangle", f"{eid}{k}", tx, y, tw, 84, ROOM, "#ffffff", roundness={"type": 3})]
        els += text(f"{eid}{k}_t", tx + 12, y + 10, t, 13, TITLE) + text(f"{eid}{k}_w", tx + 12, y + 34, words, 12, INK)
    return els


def chain(eid, x, y, w, title, steps, verb):
    """A sequence as boxes and arrows, each box with its role word above its name; the verb button on the right."""
    els = text(eid + "_t", x, y, title, 14, TITLE) + buttons(eid + "_v", x + w - 104, y - 4, (verb,))
    bw = 150
    for k, (role, name) in enumerate(steps):
        bx = x + k * (bw + 46)
        els += text(f"{eid}{k}_r", bx + 2, y + 30, role, 10, BLUE if k == 0 else BODY)
        els += [_el("rectangle", f"{eid}{k}", bx, y + 46, bw, 40, BLUE if k == 0 else ROOM, "#e7f5ff" if k == 0 else "#ffffff",
                    roundness={"type": 3})] + text(f"{eid}{k}_w", bx + 12, y + 58, name, 12, INK)
        if k:
            els += arrow(f"{eid}{k}_a", [(bx - 40, y + 66), (bx - 6, y + 66)], ROOM)
    return els


def more(eid, x, y, w, items):
    """Everything else, open, small, one line each: its name, then its line."""
    els = []
    for k, (n, words) in enumerate(items):
        els += line(f"{eid}{k}_l", [(x, y + k * 28), (x + w, y + k * 28)], "#e9ecef", 1) + \
            text(f"{eid}{k}", x + 8, y + k * 28 + 7, n, 12, INK) + text(f"{eid}{k}_w", x + 150, y + k * 28 + 7, words, 11, BODY)
    return els


def big(eid, x, y, w, words, stage):
    """The view's main point, under its bar: one large sentence, and its state word when it has one (no edge, JL 261031;
    the Direction shows no stage word, s32-D33)."""
    return text(eid + "_w", x + 4, y + 2, words, 19, INK) + (text(eid + "_s", x + 4, y + 36, stage, 12, GR) if stage else [])


def picture(eid, x, y, w, name):
    """The topic's picture, its name under it, and its verbs; the mind map has its own place (A: its own helper,
    B: section 6), so it is not a button here (b16 s32 A r01, B r04)."""
    return [_el("rectangle", eid + "_p", x, y, 189, 74, ROOM, "#f1f3f5")] + text(eid + "_n", x, y + 78, name, 11, BODY) + \
        buttons(eid + "_b", x + 204, y + 50, ("Slides", "Draw"))


def chain_only(eid, x, y, w, steps, verb=None):
    els = chain(eid, x, y - 37, w, "", steps, verb or "")[1:]
    return els if verb else [e for e in els if not e["id"].startswith(eid + "_v")]


def one_line(eid, x, y, w, words):
    return text(eid, x + 4, y, words, 12, BODY)


def cardtabs(eid, x, y, w, items, detail):
    """Tiles that act as a view-button-list (JL 261031: "for each RQ, when we click it, will it show the results
    below? ... treat them as the view button list"): one open at a time, the first open (orange in the drawing),
    the open one's detail in a panel under the tiles."""
    tw = (w - 16 * (len(items) - 1)) / len(items)
    els = []
    for k, (t, words) in enumerate(items):
        tx = x + k * (tw + 16)
        els += [_el("rectangle", f"{eid}{k}", tx, y, tw, 64, OR if k == 0 else ROOM, "#fff4e6" if k == 0 else "#ffffff",
                    roundness={"type": 3})]
        els += text(f"{eid}{k}_t", tx + 12, y + 8, t, 13, TITLE) + text(f"{eid}{k}_w", tx + 12, y + 32, words, 12, INK)
    py = y + 76
    els += [_el("rectangle", eid + "_d", x, py, w, 18 + 26 * len(detail), OR, "#ffffff", roundness={"type": 3})]
    for k, (name, words) in enumerate(detail):
        els += text(f"{eid}_d{k}", x + 14, py + 10 + k * 26, name, 12, TITLE) + \
            text(f"{eid}_d{k}_w", x + 140, py + 10 + k * 26, words, 12, INK)
    return els


def cardtabchain(eid, x, y, w, steps, detail):
    """A sequence whose boxes act as a view-button-list (JL 261031: "the journal can serve the same, like each
    journal you can describe the information about that journal"): role word above each box, arrows between, the
    first open, the open box's detail in a panel under the chain."""
    bw, els = 150, []
    for k, (role, name) in enumerate(steps):
        bx = x + k * (bw + 46)
        els += text(f"{eid}{k}_r", bx + 2, y, role, 10, OR if k == 0 else BODY)
        els += [_el("rectangle", f"{eid}{k}", bx, y + 16, bw, 40, OR if k == 0 else ROOM, "#fff4e6" if k == 0 else "#ffffff",
                    roundness={"type": 3})] + text(f"{eid}{k}_w", bx + 12, y + 28, name, 12, INK)
        if k:
            els += arrow(f"{eid}{k}_a", [(bx - 40, y + 36), (bx - 6, y + 36)], ROOM)
    py = y + 68
    els += [_el("rectangle", eid + "_d", x, py, w, 18 + 26 * len(detail), OR, "#ffffff", roundness={"type": 3})]
    for k, (name, words) in enumerate(detail):
        els += text(f"{eid}_d{k}", x + 14, py + 10 + k * 26, name, 12, TITLE) + \
            text(f"{eid}_d{k}_w", x + 160, py + 10 + k * 26, words, 12, INK)
    return els


def narrative(eid, x, y, w, root, branches):
    """The Section narrative drawn as its mind map (JL 261031: "the mindmap is actually the narrative"): the paper
    in the middle-left, a branch per Section in reader order, each with what it says; the full map opens by button."""
    n = len(branches)
    ry = y + (n * 32 - 32) / 2
    els = [_el("rectangle", eid + "_r", x, ry, 110, 32, TITLE, "#e7f5ff", roundness={"type": 3})] + \
        text(eid + "_rt", x + 14, ry + 8, root, 12, INK)
    for k, (name, words) in enumerate(branches):
        by = y + k * 32
        els += line(f"{eid}{k}_l", [(x + 110, ry + 16), (x + 170, by + 14)], ROOM, 1)
        els += [_el("rectangle", f"{eid}{k}", x + 170, by, 130, 28, ROOM, "#ffffff", roundness={"type": 3})]
        els += text(f"{eid}{k}_n", x + 180, by + 6, name, 12, TITLE) + text(f"{eid}{k}_w", x + 316, by + 6, words, 12, INK)
    return els + buttons(eid + "_b", x + w - 82, y + n * 32 - 26, ("Mind map",))


def mapcanvas(eid, x, y, w, root, branches):
    """A mind map on its canvas, worked on where it is read (board_results._canvas; JL 261102: "I think we should have
    the mindmap canvas to work on"): a frame, the map inside it, no button."""
    els = [_el("rectangle", eid + "_f", x, y, w, 32 * len(branches) + 16, ROOM, "#ffffff", roundness={"type": 3})]
    return els + [e for e in narrative(eid, x + 12, y + 8, w - 24, root, branches) if not e["id"].startswith(eid + "_b")]


def goalmap(eid, x, y, w, root, kids):
    """A Job's MindMap as the page draws it (focus_page.parts_mindmap, 261106): the Job on the left, a box per Task (its
    number small, its title), and beside each its goal leaf, `finds out` and what it must find out; never the Run tree,
    which Status shows. `kids`: (number, title, goal)."""
    rh, n = 44, len(kids)
    els = [_el("rectangle", eid + "_f", x, y, w, rh * n + 20, ROOM, "#ffffff", roundness={"type": 3})]
    ry = y + 10 + (rh * n - rh) / 2
    els += [_el("rectangle", eid + "_r", x + 12, ry, 130, 38, TITLE, "#e7f5ff", roundness={"type": 3})] + \
        text(eid + "_rt", x + 22, ry + 11, root, 11, INK)
    for k, (num, title, goal) in enumerate(kids):
        by = y + 10 + k * rh
        els += line(f"{eid}{k}_l", [(x + 142, ry + 19), (x + 176, by + 19)], ROOM, 1)
        els += [_el("rectangle", f"{eid}{k}", x + 176, by, 140, 38, ROOM, "#ffffff", roundness={"type": 3})]
        els += text(f"{eid}{k}_n", x + 184, by + 3, num, 9, BODY) + text(f"{eid}{k}_t", x + 184, by + 18, title, 11, INK)
        els += line(f"{eid}{k}_g", [(x + 316, by + 19), (x + 330, by + 19)], ROOM, 1)
        els += [_el("rectangle", f"{eid}{k}_p", x + 330, by + 10, 58, 18, BLUE, "#e7f5ff", roundness={"type": 3})] + \
            text(f"{eid}{k}_pt", x + 335, by + 13, "finds out", 9, BLUE)
        els += text(f"{eid}{k}_w", x + 394, by + 12, goal, 10, INK)
    return els


def studio_panel(eid, x, y, w, name):
    """A topic's 🎨 Studio as the page draws it (board_results._studio_panel): Open in Studio · Slides · Draw, then its
    mind map, worked on in place, and its picture beside it."""
    els = buttons(eid + "_b", x, y, ("Open in Studio", "Slides", "Draw"))
    els += [_el("rectangle", eid + "_m", x, y + 32, w - 205, 92, ROOM, "#ffffff", roundness={"type": 3})]
    els += text(eid + "_mt", x + 10, y + 36, "its mind map, worked on in place", 10, BODY)
    rx, ry = x + 14, y + 68
    els += [_el("rectangle", eid + "_r", rx, ry, 96, 26, TITLE, "#e7f5ff", roundness={"type": 3})] + \
        text(eid + "_rt", rx + 8, ry + 6, name, 10, INK)
    for k in range(3):
        by = y + 54 + k * 22
        els += line(f"{eid}_l{k}", [(rx + 96, ry + 13), (rx + 140, by + 9)], ROOM, 1)
        els += [_el("rectangle", f"{eid}_n{k}", rx + 140, by, 120, 18, ROOM, "#ffffff", roundness={"type": 3})] + \
            text(f"{eid}_n{k}_t", rx + 146, by + 3, "<a branch>", 9, BODY)
    return els + [_el("rectangle", eid + "_p", x + w - 189, y + 32, 189, 92, ROOM, "#f1f3f5")] + \
        text(eid + "_pt", x + w - 176, y + 70, "its picture", 10, BODY)


def drawing(eid, x, y, w, name):
    """A Board topic shown as its drawing only (board_results._topic_canvas; JL 261102: "we might want to have this to
    be a excalidraw only"): Draw, then the picture."""
    return buttons(eid + "_b", x, y, ("Draw",)) + [_el("rectangle", eid + "_p", x, y + 30, 189, 74, ROOM, "#f1f3f5")] + \
        text(eid + "_n", x + 204, y + 60, name, 11, BODY)


def prompt_box(eid, x, y, w, title, prompt, run):
    """The step's Copy prompt box (draft_steps' Prompt box; focus_draft.studio_top shows the Studio step's, 261105): its
    title and Copy prompt, the prompt, a box for your notes, and the session it runs in."""
    els = [_el("rectangle", eid, x, y, w, 158, ROOM, "#ffffff", roundness={"type": 3})]
    els += text(eid + "_t", x + 12, y + 10, title, 13, TITLE) + buttons(eid + "_c", x + w - 104, y + 6, ("Copy prompt",))
    els += [_el("rectangle", eid + "_g", x + 12, y + 38, w - 24, 50, "#e9ecef", "#f1f3f5")] + text(eid + "_p", x + 20, y + 44, prompt, 10, INK)
    els += text(eid + "_nl", x + 12, y + 102, "your notes", 10, BODY)
    els += [_el("rectangle", eid + "_n", x + 100, y + 96, w - 112, 24, ROOM, "#ffffff", roundness={"type": 3})]
    return els + text(eid + "_r", x + 12, y + 132, run, 10, BODY)


def note(eid, x, y, w, words):
    """A line the page shows only sometimes, said where it would stand."""
    return text(eid, x + 4, y + 4, words, 11, BODY)


def flowmap(eid, x, y, w, cols):
    """How the data come together (JL 261101: "show the mind map of how these data are collected together"): a column
    each for the data, the linking, the tables and the questions, a line from each box to the next column."""
    cw, bh, gap = (w - 3 * 24) / 4, 22, 6
    els = []
    for c, (head, boxes) in enumerate(cols):
        cx = x + c * (cw + 24)
        els += text(f"{eid}{c}_h", cx, y, head, 11, TITLE)
        for k, name in enumerate(boxes):
            by = y + 18 + k * (bh + gap)
            els += [_el("rectangle", f"{eid}{c}_{k}", cx, by, cw, bh, TITLE if c == 3 else ROOM, "#ffffff", roundness={"type": 3})]
            els += text(f"{eid}{c}_{k}_t", cx + 6, by + 4, name, 10, INK)
            if c:
                pk = min(k, len(cols[c - 1][1]) - 1)
                py = y + 18 + pk * (bh + gap) + bh / 2
                els += line(f"{eid}{c}_{k}_l", [(cx - 24, py), (cx, by + bh / 2)], ROOM, 1)
    return els


def ftree(eid, x, y, w, rows):
    """A folder tree, one line per folder: its name, then its line, an elbow from its parent; ▾ open, ▸ shut, a Run
    its receipt's mark (board_results.explore_view: Blocks open, Jobs shut, each Task folding to its Runs)."""
    els = []
    for k, (depth, name, words) in enumerate(rows):
        ry, rx = y + k * 22, x + depth * 22
        if depth:
            els += line(f"{eid}{k}_l", [(rx - 14, ry - 12), (rx - 14, ry + 8), (rx - 3, ry + 8)], ROOM, 1)
        els += text(f"{eid}{k}", rx, ry, name, 11, TITLE if depth > 1 else BODY)
        if words:
            els += text(f"{eid}{k}_w", rx + 7 * len(name) + 10, ry, words, 10, BODY)
    return els


def sidetabs(eid, x, y, w, items, detail):
    """Side tabs (JL 261101: "in the left there is a panel, and we can read the content quickly"): the items as a list on
    the left, the first open; the open one's content to read on the right."""
    lw = 110                                     # narrow, so the reading panel gets the room (JL 261101)
    els = []
    for k, (head, words) in enumerate(items):
        iy = y + k * 40
        els += [_el("rectangle", f"{eid}{k}", x, iy, lw, 34, OR if k == 0 else "#ffffff", "#fff4e6" if k == 0 else "#ffffff", roundness={"type": 3})]
        els += text(f"{eid}{k}_t", x + 8, iy + 3, head, 11, TITLE) + text(f"{eid}{k}_w", x + 8, iy + 18, words, 9, BODY)
    ph = 18 + 24 * len(detail)
    els += [_el("rectangle", eid + "_d", x + lw + 14, y, w - lw - 14, max(ph, 40 * len(items)), OR, "#ffffff", roundness={"type": 3})]
    for k, (name, words) in enumerate(detail):
        els += text(f"{eid}_d{k}", x + lw + 26, y + 10 + k * 24, name, 10, TITLE) + text(f"{eid}_d{k}_w", x + lw + 110, y + 10 + k * 24, words, 10, INK)
    return els


def gtabs(eid, x, y, w, groups, detail):
    """Side tabs in groups (board_results._grouped_tabs: Displays' Main, Supplement, Others; Related's `bears on`): each
    group's name small over its items, the first item open; the open one's content on the right."""
    lw, els, iy, first = 110, [], y, True
    for g, (name, items) in enumerate(groups):
        els += text(f"{eid}g{g}", x + 2, iy + 2, name, 10, BODY)
        iy += 20
        for k, (head, words) in enumerate(items):
            els += [_el("rectangle", f"{eid}{g}_{k}", x, iy, lw, 34, OR if first else "#ffffff", "#fff4e6" if first else "#ffffff",
                        roundness={"type": 3})]
            els += text(f"{eid}{g}_{k}_t", x + 8, iy + 3, head, 11, TITLE) + text(f"{eid}{g}_{k}_w", x + 8, iy + 18, words, 9, BODY)
            first, iy = False, iy + 40
    els += [_el("rectangle", eid + "_d", x + lw + 14, y, w - lw - 14, max(18 + 24 * len(detail), iy - y), OR, "#ffffff",
                roundness={"type": 3})]
    for k, (name, words) in enumerate(detail):
        els += text(f"{eid}_d{k}", x + lw + 26, y + 10 + k * 24, name, 10, TITLE) + text(f"{eid}_d{k}_w", x + lw + 110, y + 10 + k * 24, words, 10, INK)
    return els


def rows(eid, x, y, w, items):
    """Short rows, a name then its words (skills, steps, where each stands)."""
    els = []
    for k, (name, words) in enumerate(items):
        els += text(f"{eid}_{k}n", x + 4, y + k * 24, name, 12, TITLE) + (text(f"{eid}_{k}w", x + 220, y + k * 24, words, 12, BODY) if words else [])
    return els


# ── a bar's state word and its waiting line, by the live page's rules (ui_parts.waits_on_you, todo_word; 261106) ─────
WAITS_WORDS = ("wait for you", "waits for you", "waiting for you", "waits for your", "needs your", "your sign", "your call")
DONE_WORDS = ("done", "checked", "answered", "drawn", "ready", "applied", "decided")


def waits_on_you(word):
    return any(w in (word or "").lower() for w in WAITS_WORDS)


def todo_word(rows):
    """(state word, waiting line) of to-do rows (words, state, verb), as ui_parts.todo_word: how many wait for you and the
    first of them, else done, running, N open, or how many are done."""
    states = [(s or "").lower() for _, s, _ in rows]
    if not states:
        return "nothing yet", ""
    you = [r for r, s in zip(rows, states) if waits_on_you(s) or s.startswith("waiting")]
    if you:
        return f'{len(you)} wait{"s" if len(you) == 1 else ""} for you', f"🙋 {you[0][0]}"
    done = sum(any(w in s for w in DONE_WORDS) for s in states)
    if done == len(states):
        return "done", ""
    if any("running" in s or "in progress" in s for s in states):
        return "running", ""
    if all(s == "open" for s in states):
        return f"{len(states)} open", ""
    return f"{done} of {len(states)} done", ""


def bar_words(sec):
    """A section's (state word, waiting line): its own when it names them (`("sec", title, inner, word[, waits])`), else
    a to-do list's, read from its rows; else none."""
    if len(sec) > 3:
        return sec[3], (sec[4] if len(sec) > 4 else "")
    if sec[2][0] == "todo":
        return todo_word(sec[2][1])
    return "", ""


TODO_PILL = {"Needs your judgment": (OR, "#fff4e6"), "waiting for you": (OR, "#fff4e6"), "sign": (OR, "#fff4e6"),
             "running": (BLUE, "#e7f5ff"), "done": (GR, "#ebfbee"), "Answered": (GR, "#ebfbee"), "ready": (GR, "#ebfbee"),
             "answered": (GR, "#ebfbee")}


def todo(eid, x, y, w, items):
    """One full-width row per thing to do: its words, its state a coloured pill, its verb (b15 s58 C2)."""
    els = []
    for k, (words, state, verb) in enumerate(items):
        ry = y + 40 * k
        els += [_el("rectangle", f"{eid}{k}", x, ry, w, 34, ROOM, "#ffffff", roundness={"type": 3})]
        els += text(f"{eid}{k}_w", x + 12, ry + 9, words, 13, INK)
        stroke, fill = TODO_PILL.get(state, (ROOM, "#f8f9fa"))
        pw = 16 + 6.5 * len(state)
        verbs = tuple(verb.split(" · ")) if verb else ()
        bw = sum(20 + 7.5 * len(v) for v in verbs)
        px = x + w - 12 - (bw + 8 if verb else 0) - pw
        els += [_el("rectangle", f"{eid}{k}_p", px, ry + 7, pw, 20, stroke, fill, roundness={"type": 3})]
        els += text(f"{eid}{k}_pt", px + 8, ry + 10, state, 10, INK)
        if verb:
            els += buttons(f"{eid}{k}_b", x + w - 12 - bw, ry + 5, verbs)
    return els


def paras(eid, x, y, w, items):
    """A draft's text as the page lays it out: each paragraph its id and name, then its sentences as grey lines with
    their S numbers (JL 261101: "show the scratch of the layout here")."""
    els, yy, s_no = [], y, 0
    for k, (head, n) in enumerate(items):
        els += text(f"{eid}{k}_h", x + 4, yy, head, 12, TITLE)
        for j in range(n):
            lw = w - 60 - (j * 37) % 120
            s_no += 1                              # sentences count straight through the Section: S1, S2, S3 …
            els += text(f"{eid}{k}_s{j}", x + 4, yy + 22 + j * 18, f"S{s_no}", 9, BODY)
            els += [_el("rectangle", f"{eid}{k}_l{j}", x + 30, yy + 26 + j * 18, lw, 6, ROOM, "#e9ecef")]
        yy += 30 + 18 * n
    return els


def split(eid, x, y, w, items, right, by_s):
    """The text in two panels, as the draft page lays it out (rv-split: JL 261101, "it is the left part, and the right
    part"): the paragraphs and their sentences on the left; on the right, under its title, what belongs to each
    sentence, level with it: your editor row (Write), its evidence card (Evidence), its note (Revise)."""
    lw = (w - 16) * 0.55
    els = paras(eid + "_l", x, y + 22, lw, items)
    rx, rw = x + lw + 16, w - lw - 16
    els += [_el("rectangle", eid + "_rb", rx, y, rw, SIZE["paras"](("paras", items)) + 22, ROOM, "#ffffff", roundness={"type": 3})]
    els += text(eid + "_rt", rx + 10, y + 4, right, 11, TITLE)
    yy, s_no = y + 22, 0
    for k, (head, n) in enumerate(items):
        for j in range(n):
            s_no += 1
            sy = yy + 22 + j * 18
            what = by_s.get(s_no) if isinstance(by_s, dict) else (f"S{s_no} · <your words>" if by_s == "editor" else None)
            if what:
                label, state = (what, "") if isinstance(what, str) else what
                els += [_el("rectangle", f"{eid}_r{s_no}", rx + 8, sy - 3, rw - 16, 15, OR if state else ROOM,
                            "#fff4e6" if state else "#ffffff", roundness={"type": 3})]
                els += text(f"{eid}_r{s_no}_t", rx + 14, sy - 2, label + (f"  · {state}" if state else ""), 9, INK)
        yy += 30 + 18 * n
    return els


def chips(eid, x, y, w, items):
    """A Section a row, its five step words as chips, each opening that step (paper_version.section_row, s36-D01)."""
    els = []
    for k, (name, words) in enumerate(items):
        ry = y + 34 * k
        els += text(f"{eid}{k}_n", x + 4, ry + 6, name, 11, TITLE)
        cx = x + 130
        for j, wd in enumerate(words):
            cw = 14 + 5.6 * len(wd)
            you = wd.endswith(("sign", "asked"))
            els += [_el("rectangle", f"{eid}{k}_c{j}", cx, ry, cw, 24, OR if you else ROOM, "#fff4e6" if you else "#ffffff",
                        roundness={"type": 3})] + text(f"{eid}{k}_c{j}_t", cx + 7, ry + 5, wd, 10, INK)
            cx += cw + 5
    return els


def editor(eid, x, y, w, label):
    """An editor the person types in: a framed box, faint lines, its label."""
    els = [_el("rectangle", eid, x, y, w, 70, ROOM, "#ffffff", roundness={"type": 3})] + text(eid + "_t", x + 10, y + 6, label, 11, BODY)
    for j in range(3):
        els += [_el("rectangle", f"{eid}_l{j}", x + 10, y + 28 + j * 13, w - 60 - j * 70, 4, ROOM, "#f1f3f5")]
    return els


def band(eid, x, y, w, name, why=""):
    """A view's part, ⚙️ Process or 📊 Results: its name and a thin rule after it, as b15 s58 and the live page draw it
    (servers/workbench/ui_parts.py PROCESS, RESULTS; JL 261101: one look in every theme)."""
    return text(eid + "_n", x, y + 6, name, 16, INK) + line(eid + "_r", [(x + 120, y + 16), (x + w, y + 16)], ROOM, 1)


UNDER = {"chips": (chips, 0), "split": (split, 0), "paras": (paras, 0), "editor": (editor, 76), "todo": (todo, 4 * 40 + 2), "rows": (rows, 3 * 24 + 4), "big": (big, 64), "sidetabs": (sidetabs, 18 + 24 * 4 + 6), "ftree": (ftree, 9 * 22 + 6), "flowmap": (flowmap, 18 + 5 * 28 + 6), "narrative": (narrative, 4 * 32 + 6), "cardtabchain": (cardtabchain, 68 + 18 + 26 * 4 + 6), "cardtabs": (cardtabs, 76 + 18 + 26 * 4 + 6), "tiles": (tiles, 96), "chain": (chain_only, 70), "ask": (ask, 50), "picture": (picture, 100),
         "line": (one_line, 26), "canvas": (mapcanvas, 0), "studio": (studio_panel, 128), "drawing": (drawing, 110), "gtabs": (gtabs, 0),
         "goalmap": (goalmap, 0)}


def sec_block(eid, x, y, w, title, inner, word="", waits=""):
    """A section as the page draws it: a boxed heading bar that folds, numbered in reading order, closed at first (▸,
    JL 261104: "this should be closed at the begining"); its state word on the bar's right, in the waiting colour when it
    waits on you, and that one waiting line under the closed bar (ui_parts._section, 261106); under them, what it shows
    once opened (JL 261031: "each section to be the [heading bar] ... seems to be ordered")."""
    word, waits = bar_words(("sec", title, inner) + ((word, waits) if word or waits else ()))
    els = [_el("rectangle", eid, x, y, w, 30, ROOM, "#ffffff", roundness={"type": 3})] + \
        text(eid + "_t", x + 12, y + 7, "▸ " + title, 13, TITLE)
    if word:
        els += text(eid + "_sw", x + w - 12 - len(word) * 11 * WIDE, y + 9, word, 11, OR if waits_on_you(word) else BODY)
    top = y + 42
    if waits:
        size = 11 if len(waits) * 11 * WIDE <= w - 40 else 10
        els += text(eid + "_wl", x + 30, y + 36, waits, size, OR)
        top += 20
    return els + UNDER[inner[0]][0](eid + "_c", x, top, w, *inner[1:])


BLOCK = {"band": (band, 40), "lead": (lead, 140), "ask": (ask, 52), "tiles": (tiles, 100), "chain": (chain, 106),
         "note": (note, 28), "prompt": (prompt_box, 172)}


SIZE = {"todo": lambda inner: 40 * len(inner[1]) + 2, "rows": lambda inner: 24 * len(inner[1]) + 4,
        "paras": lambda inner: sum(30 + 18 * n for _, n in inner[1]),
        "split": lambda inner: sum(30 + 18 * n for _, n in inner[1]) + 26,
        "chips": lambda inner: 34 * len(inner[1]), "line": lambda inner: 26 if inner[1] else 0,
        "big": lambda inner: 64 if inner[2] else 40,
        "sidetabs": lambda inner: max(18 + 24 * len(inner[2]), 40 * len(inner[1])) + 6,
        "gtabs": lambda inner: max(18 + 24 * len(inner[2]), sum(20 + 40 * len(g[1]) for g in inner[1])) + 6,
        "ftree": lambda inner: 22 * len(inner[1]) + 6, "narrative": lambda inner: 32 * len(inner[2]) + 6,
        "canvas": lambda inner: 32 * len(inner[2]) + 22, "goalmap": lambda inner: 44 * len(inner[2]) + 26}


def inner_h(inner):
    return SIZE[inner[0]](inner) if inner[0] in SIZE else UNDER[inner[0]][1]


def block_h(sec):
    if sec[0] == "sec":
        return 42 + (20 if bar_words(sec)[1] else 0) + inner_h(sec[2]) + 14
    if sec[0] == "body":                     # a view's content with no bar of its own (the frame's Job and Task views)
        return inner_h(sec[1]) + 14
    if sec[0] == "rule":
        return 24
    if sec[0] == "more":
        return 28 * len(sec[1]) + 16
    if sec[0] in BLOCK:
        return BLOCK[sec[0]][1]
    return 76 if len(sec) == 3 else 58


def screen(eid, x, y, h, level, section, views, on, secs, page=None):
    """One view as the full screen of the big sketch: the window, the title and section word, the view buttons with
    this one in orange, then its content: a section is a heading bar with what it holds under it (title, inner[, its
    state word[, its waiting line]]); a body is content with no bar; a topic is a box with its picture, name, line and
    stage (name, words, stage). `page`: (name, path, crumb, goal) of another page at this level (an Other Job)."""
    name, path, crumb, goal = page or (*PAGE[level], CRUMB[level], GOAL[level])
    els = window(eid + "w", x, y, 700, h, f"…&path={path}&section={section}")
    els += text(eid + "_cr", x + 40, y + 38, crumb, 10, ROOM)
    els += head(eid + "h", x + 40, y + 56, name, section, views, on, BUTTON.get((level, section)))
    els += text(eid + "_go", x + 40, y + 126, goal, 11, BODY)
    cap = CAPTION.get((level, section, views[on]), "")
    els += text(eid + "_ca", x + 40, y + 146, cap, 11, INK) if cap else []
    for k in range(4):                                            # left-rail: pale page lines
        els += line(f"{eid}_lr{k}", [(x + 10, y + 180 + k * 22), (x + 28, y + 180 + k * 22)], ROOM, 1)
    for k, r in enumerate(RAIL):                                  # right-rail: the sections, this one marked
        els += text(f"{eid}_rr{k}", x + 622, y + 180 + k * 22, r, 9, OR if r.lower() == section else ROOM)
    yy = y + 172
    for k, sec in enumerate(secs):
        if sec[0] == "sec":
            els += sec_block(f"{eid}r{k}", x + 40, yy, 570, *sec[1:])
        elif sec[0] == "body":
            els += UNDER[sec[1][0]][0](f"{eid}r{k}", x + 40, yy, 570, *sec[1][1:])
        elif sec[0] == "rule":
            els += line(f"{eid}r{k}", [(x + 40, yy + 8), (x + 610, yy + 8)], ROOM, 1, dashed=True)
        elif sec[0] == "more":
            els += more(f"{eid}r{k}", x + 40, yy, 570, sec[1])
        elif sec[0] in BLOCK:
            els += BLOCK[sec[0]][0](f"{eid}r{k}", x + 40, yy, 570, *sec[1:])
        elif len(sec) == 3:
            els += topic_row(f"{eid}r{k}", x + 40, yy, 570, *sec)
        else:
            els += secbar(f"{eid}r{k}", x + 40, yy, 570, *sec)
        yy += block_h(sec)
    return els


def tall(secs):
    return sum(block_h(sec) for sec in secs)


def notes_of(value):
    """A screen's green notes, oldest first: a plain string is a legacy note, dated 261031 (the date every note had
    before 261105); a list holds each note, a string (legacy) or a (date, words) pair."""
    if not value:
        return []
    if isinstance(value, str):
        return [("261031", value)]
    return [("261031", n) if isinstance(n, str) else tuple(n) for n in value]


def screens(eid, x, y, items, level, section, changed=None, gap=40, proposed=(), first=0, page=None):
    """Every view lettered A, B, C …, every screen the same size (the tallest view's), three a row (JL 261031: each
    view "the same size and format" as the big sketch). A view is (name, its sections[, the buttons its screen shows],
    when a screen's buttons differ, as a Section Studio's Topics); a view in `proposed` is drawn under a red letter,
    not built. Each screen's green notes stand under its letter, one a line, in their order. `first`: the first
    screen's letter (an Other Job's row goes on from the page's own); `page`: that Job's (name, path, crumb, goal)."""
    cols = min(3, len(items))
    h = 192 + max(tall(it[1]) for it in items)
    views = tuple(it[0] for it in items)
    notes = [notes_of((changed or {}).get(LETTERS[first + k])) for k in range(len(items))]
    top = 40 + 24 * max(len(n) for n in notes)                 # the letter, its notes, then the screen
    els = []
    for k, item in enumerate(items):
        view, secs = item[0], item[1]
        nav = item[2] if len(item) > 2 else views
        sx, sy = x + (k % cols) * (700 + gap), y + (k // cols) * (h + top + gap)
        red = view in proposed
        els += text(f"{eid}{k}_L", sx, sy, f"{LETTERS[first + k]} · {view}" + ("   (proposed, not built)" if red else ""), 22,
                    RE if red else TITLE)
        for j, (date, words) in enumerate(notes[k]):
            els += [change_note(sx, sy + 34 + 24 * j, words, date, None)]
        els += screen(f"{eid}{k}", sx, sy + top, h, level, section, nav, nav.index(view), secs, page)
    return els, y + ((len(items) + cols - 1) // cols) * (h + top + gap)


# ── the Board's views, as board_views.py draws them (261105) ─────────────────────────────────────────────────────
# Each view's sections in page order, each with what it holds under its bar (JL 261031: each view "the same size and
# format" as the big sketch). Titles are the bars the live page draws (board_results.py); words are placeholders, never
# paper text. A helper (the drawing) stands after the dashed rule; 🙋 Interaction is added last (_ix).
STUDIO = ("studio", "<the topic>")
IX_DETAIL = (("", "<the question and its choices: pick one>"), ("", "‹ Back     Next ›     Copy feedback"),   # the form on
             ("", "<who asked · about what · who applies it>"))                                          # the right
IXW = ("sidetabs", (("Q1 · <a question>", "waiting for you"), ("Q2 · <a question>", "waiting for you")), IX_DETAIL)
IXA = ("sidetabs", (("Q1 · <a question>", "✓ <your pick>"), ("Q2 · <a question>", "✓ <your pick>")), IX_DETAIL)
# 🙋 Interaction holds the view's own items (JL 261106: "a view's bottom section shows that view's own items"), so its
# state is the view's: questions waiting (the word counts them, the first shows under the bar), all answered, or none
IX = {"wait": (IXW, "2 wait for you", "🙋 <the form's title>: Q1 · <its first question>"),
      "answered": (IXA, "answered", ""),
      "none": (("line", "Nothing asked yet."), "nothing yet", "")}
REPORT_ONLY = (
    ("Idea", (("sec", "🎨 Studio", STUDIO, "agreed"),                           # the many directions (s32-D44, D45)
              ("sec", "1 · 🔀 Directions", ("sidetabs", (("<direction 1>", "✅ selected"), ("<direction 2>", "second"),
                                                         ("<direction 3>", "lost")),
                                            (("Direction", "<the direction, in full>"), ("Verdict", "<selected, second, fallback, lost …>"),
                                             ("Reason", "<why, in one line>"), ("Decided", "<who and when>"))), "one chosen"),
              ("sec", "2 · 🎓 Theory", ("sidetabs", (("<direction 1>", "<its theory>"), ("<direction 2>", "<its theory>")),
                                        (("Theory", "<the theory the direction rests on>"),
                                         ("", "empty, it says how to fill it; flagged for an IS venue"))), "written"),
              ("note", "no Story yet: 🧭 Direction comes first, and 📚 Related after Theory"))),
    ("Story", (("sec", "🎨 Studio", STUDIO, "shaping"),                         # the one chosen (s32-D44, D45, D30)
               ("sec", "1 · 🧭 Direction", ("big", "<the direction chosen, in one plain sentence>", ""), "agreed"),
               ("sec", "2 · 💡 Pitch", ("big", "<what the paper finds, for whom, in one plain sentence>", ""), "shaping"),
               ("sec", "3 · 🎓 Theory", ("line", "<the theory the chosen direction rests on>"), "written"),
               ("sec", "4 · ❓ Research Questions", ("sidetabs", (("RQ1", "<its question>"), ("RQ2", "<its question>"),
                                                                 ("RQ3", "<its question>")),
                                                    (("Hypothesis", "<what we expect, and why>"),
                                                     ("Claim", "<what an answer lets the paper say>"),
                                                     ("Tested by", "<its Runs and displays>"),
                                                     ("Answer so far", "<the finding, or what it waits on>"))), "2 of 3 open"),
               ("sec", "5 · ⚖️ Stakes and evidence", ("sidetabs", (("Stakes", "why it matters"), ("Evidence basis", "what it can claim")),
                                                      (("", "<why it matters, and to whom>"), ("", "<what it can claim, and what it cannot>"))),
                "both written"),
               ("sec", "6 · 📚 Related", ("gtabs", (("<what it bears on>", (("★ <closest paper>", "<author year · venue>"),
                                                                           ("<a paper>", "<author year · venue>"))),
                                                    ("<what else it bears on>", (("<a paper>", "<author year · venue>"),))),
                                          (("", "<its title> · <why it is here>"), ("", "Pop out"), ("", "<its PDF, read here>"))),
                "every paper to read here"),
               ("sec", "7 · 🏛️ Venues", ("sidetabs", (("target", "<journal>"), ("fallback 1", "<journal>"), ("fallback 2", "<journal>")),
                                          (("Desk rules", "<deadline · word limit · format>"), ("Review and scope", "<how it reviews, what it takes>"),
                                           ("Related papers", "<its closest papers>"), ("Fit", "<why this paper belongs here>"))),
                "target <journal>"),
               ("sec", "8 · 🧠 Story by Section", ("narrative", "<paper>", (("Introduction", "<what it says>"), ("Methods", "<what it says>"),
                                                                            ("Results", "<what it says>"), ("Discussion", "<what it says>"))),
                "shaping"))),
    ("Data + Paper Plan", (("sec", "1 · 🗄️ Data flow", ("canvas", "<the data flow>", (("The data", "<claims · traits · dates>"),
                                                                                       ("The linking", "<visits · physician · state>"),
                                                                                       ("The tables", "<a visit table · others>"),
                                                                                       ("The questions", "<each Board Question>"))),
                            "shaping"),
                           ("sec", "2 · 📝 Paper flow", ("canvas", "<the paper flow>", (("Sections", "<in reader order>"),
                                                                                         ("Displays", "<Figure 1 · Table 1>"),
                                                                                         ("To the send", "<date · step · who>"))),
                            "shaping"),
                           ("sec", "3 · 🗺️ Roadmaps", ("sidetabs", (("Discovery roadmap", "still to read"), ("Task roadmap", "still to run")),
                                                       (("", "<each question · what it must read>"), ("", "<each Run still to make · its state>"))),
                            "1 of 4 done"),
                           ("rule",),                                          # the helpers, after the dashed rule
                           ("sec", "🖼️ The drawing · Data flow", ("picture", "<the data-flow topic>"), "drawn <date>"),
                           ("sec", "🖼️ The drawing · Paper flow", ("picture", "<the paper-flow topic>"), "drawn <date>"))),
    ("Support blocks", (("sec", "1 · 🧪 Work", ("ftree", ((0, "▾ Project-Example/", ""), (1, "▾ work/", ""),     # one tree per
                                                         (2, "▾ bNN_<block>/", "<what it builds>"),         # Project, only what
                                                         (3, "▾ jNN_<job>/", "main analysis · <its goal>"),  # this paper uses
                                                         (4, "▾ tNN_<task>/", "<its aim>"),                  # (JL 261101); Jobs
                                                         (5, "✅ rNN_<run>", "<its headline>"),               # fold, each Task to
                                                         (5, "⬜ rNN_<run>", "no receipt yet"),               # its Runs (JL 261102)
                                                         (3, "▸ jNN_<job>/", "<its goal>"),
                                                         (0, "▸ Project-Example-B/", ""))), "2 Blocks"),
                        ("sec", "2 · 🔎 Discovery", ("ftree", ((0, "▾ Project-Example/", ""), (1, "▾ discovery/", ""),
                                                              (2, "▾ b01_<question>/", "<what it reads>"),
                                                              (3, "▸ j01_<topic>/", "<its question>"))), "1 Block"))),
    ("Evidence", (("sec", "1 · 🔢 Values", ("sidetabs", (("Sample", "<what it waits on>"), ("<policy>", "<…>"), ("Timing", "<…>")),   # side tabs:
                                                       (("1.", "<Section sentence · the number>"), ("", "source: <Run · file>"),   # list left,
                                                        ("2.", "<Section sentence · the number>"), ("", "source: <Run · file>"))),  # read right
                   "all current"),
                  ("sec", "2 · 📚 Citations", ("sidetabs", (("<topic A>", "<N checked>"), ("<topic B>", "<…>"), ("Methods", "<…>")),
                                                           (("<paper key>", "<its Sections> · ✅ checked"), ("<paper key>", "<its Sections> · ✅ checked"))),
                   "2 of 2 verified"))),
    # Displays, its own view after Evidence (JL 261101: "put the display outside of the Evidence, and put it after the
    # Evidence and before the Writing, to highlight it"): the plan's drawing, each display by group, then the venue's examples
    ("Displays", (("sec", "1 · 📐 Plan", ("drawing", "<the display plan, its drawing>"), "shaping"),
                  ("sec", "2 · 🖼️ Displays", ("gtabs", (("Main", (("Figure 1 (Display A)", "📈 Figure · <what it shows>"),
                                                                 ("Table 1 (Display B)", "📊 Table · <who is in it>"))),
                                                        ("Supplement", (("eFigure 1 (Display C)", "📈 Figure · <a check>"),)),
                                                        ("Others", (("<a draft display>", "not placed yet"),))),
                                              (("", "Open all displays as one PDF · Open the display Job"),
                                               ("", "<preview.pdf: page 1 as the paper prints it>"), ("", "<then how it was made>"))),
                   "3 of 3 drawn"),
                  ("sec", "3 · 🔍 Examples", ("drawing", "<the venue's published displays, one canvas>"), "drawn"))),
    ("Writing", (("sec", "1 · ✍️ j11_writing_v1130_venue", ("sidetabs", (("Summary", "Plan: waits for your sign"),
                                                                       ("Methods", "Write: next"), ("Results", "Evidence: waits for your answer")),
                                                        (("", "Open the version · Open the Section"), ("BACKGROUND", "<the Section's text, to read>"),
                                                         ("METHODS", "<its paragraph>"), ("FINDINGS", "<its paragraph>"))),
                  "2 wait for you", "🙋 Summary: Plan: waits for your sign"),                 # board_results.sections_word
                 ("sec", "2 · 📄 The assembled paper", ("sidetabs", (("The paper", "draft · <when>"), ("The paper · Word", "draft · <when>"),
                                                                   ("Earlier round", "<when it was sent>")),          # each output
                                                      (("", "⤢ Pop out  (the whole paper over the page)"),            # read right;
                                                       ("", "<the PDF itself, page by page>"),                        # pops out
                                                       ("", "Open the PDF · Open the Word file"))), "draft"),         # (JL 261101)
                 ("sec", "3 · 📮 Ready for the portal", ("todo", (("1 · <a portal slot> · <its file>", "ready", "Open"),
                                                                 ("2 · <a portal slot>", "no file yet", ""))), "1 of 2 ready"))),
)
BOARD_IX = {"Idea": "none", "Story": "wait", "Data + Paper Plan": "answered", "Support blocks": "none", "Evidence": "none",
            "Displays": "none", "Writing": "none"}                # each view's own 🙋, as the Paper-Example's live page has it


def _nums(secs):
    return [int(m.group(1)) for s in secs if s[0] == "sec" for m in [re.match(r"(\d+) · ", s[1])] if m]


def _ix(secs, state="none"):
    """🙋 Interaction, the view's last section on every Report and Work view (s32-D38, D41): numbered after the last
    band's numbered sections, unnumbered when they carry none (interaction_section.next_number); its word and waiting
    line are the view's own items' (interaction_section.state_word, 261106)."""
    bands = [k for k, s in enumerate(secs) if s[0] == "band"]
    n = max(_nums(secs[bands[-1]:] if bands else secs), default=0)
    return ("sec", (f"{n + 1} · " if n else "") + "🙋 Interaction", *IX[state])


# Work's ⚙️ Process, as board_process.process_html draws it today: 📌 Open points, one list of the lines the parts'
# faces mark waiting and their Open rows (261105: Idea read "🚧 Open", Story "📌 Open points"; one list now), then the
# view's own steps; a title names the step, never a count (s33-D08). Who does it is the rail's Skills section, once per
# page, no longer a step in every view (JL 261105: "a new tab in the right rail, named 'SKILL'"; drawn 261106)
PROCESS = {
    "Idea": (("📌 Open points", ("todo", (("<an open point of the topic>", "open", ""),))),),
    "Story": (("📌 Open points", ("todo", (("<a line the face marks waiting for you>", "waiting for you", ""),
                                          ("<an open point of the topic>", "open", "")))),),
    "Data + Paper Plan": (("🧭 Plan", ("todo", (("🗂️ Design the dataset", "use /haipipe-paper-plan", "Open · Copy prompt"),   # the plan
                                               ("📈 Design the regressions", "use /haipipe-task", "Open · Copy prompt"),       # center
                                               ("⚙️ Make them run", "use /haipipe-run", "Open · Copy prompt"),                # (s33-D07)
                                               ("🖼️ Plan the displays", "use /haipipe-paper-plan", "Open · Copy prompt"),
                                               ("🔎 Plan the reading", "use /haipipe-discovery", "Open · Copy prompt"))),
                           "runs in <the Board's session>"),
                          ("⚙️ Runs to do", ("todo", (("<a Run to do> · <what it gives>", "waiting for you", "Open"),
                                                     ("<a Run to do>", "running", "Open"), ("<a Run to do>", "done", "Open")))),
                          ("🗓️ Next steps to the send", ("todo", (("<date> · <step> · <who>", "waiting for you", ""),
                                                                ("<date> · <step> · <who>", "not started", ""))))),
    "Support blocks": (),
    "Evidence": (("📋 Where each stands", ("todo", (("Values · <a value group>", "done", "Open"),
                                                   ("Values · the whole-paper check", "not started", "Open"),
                                                   ("Citations · <a claim group>", "done", "Open")))),),
    "Displays": (("🖼️ Where each display stands", ("todo", (("Figure 1 (Display A) · 📈 Figure", "done", "Open"),
                                                           ("Table 1 (Display B) · 📊 Table", "done", "Open"),
                                                           ("eFigure 1 (Display C) · 📈 Figure", "done", "Open")))),),
    "Writing": (("🪜 Sections to finish", ("todo", (("Summary · next: Plan", "waiting for you", "Open Plan"),
                                                   ("Methods · next: Evidence", "running", "Open Evidence"),
                                                   ("Results · next: Write", "not started", "Open Write")))),)}


def _work(view, secs):
    """A Board Work view (board_views.banded, work): ⚙️ Process, numbered from 1, when the view has steps, then 📊
    Results, the Report's sections drawn by the same code (JL 261101: "the results should be consistent to the report"),
    its helpers, then 🙋 Interaction."""
    steps = PROCESS[view]
    body = ((("band", "⚙️ Process", ""),) + tuple(("sec", f"{k} · {t}", *rest) for k, (t, *rest) in enumerate(steps, 1))
            if steps else ()) + (("band", "📊 Results", ""),) + secs
    return body + (_ix(body, BOARD_IX[view]),)


REPORT_SECTIONS = tuple((v, secs + (_ix(secs, BOARD_IX[v]),)) for v, secs in REPORT_ONLY)   # the Report: its sections only (s32-D27)
WORK_SECTIONS = tuple((v, _work(v, secs)) for v, secs in REPORT_ONLY)
LAYERS = "① plan: A to C   ·   ② explore: D   ·   ③ evidence: E, F   ·   ④ writing: G"


# a view's caption, as the live page writes it under the Purpose, Goal or Aim (focus_page.VIEW_WORDS, focus_draft.CAPTIONS);
# the frame's MindMap shows one; the paper's own views (a Board's, a version's, an Other Job's) show none today
CAPTION = {("version", "report", "MindMap"): "How it is built, as a map: its parts, and what each must find out.",
           ("section", "report", "MindMap"): "The content as a map: each part, then what it holds.",
           ("section", "report", "Text"): "Each sentence beside its evidence, its changes and the review's notes.",
           ("section", "report", "Status"): "Where each step stands, and what waits for you.",
           ("section", "work", "Plan"): "The plan: its paragraphs and their points, before the sentences.",
           ("section", "work", "Write"): "The text, and your own sentences typed beside it.",
           ("section", "work", "Evidence"): "The text beside the evidence for each sentence, and what is still open.",
           ("section", "work", "Display"): "The Tables and Figures the text calls, each beside its sentence.",
           ("section", "work", "Revise"): "The text beside its review cards: accept or reject each change.",
           ("section", "work", "Runs"): "Every Run of this Task."}
CRUMB = {"board": "SPACE › Project-Example › paper › Paper-Example", "version": "… › Paper-Example › j11_writing_v1130_venue",
         "section": "… › j11_writing_v1130_venue › t00_summary"}
GOAL = {"board": "Purpose: one paper, from its idea to its send", "version": "Goal: this send, ready by its date",
        "section": "Aim: this Section, as the venue asks"}
RAIL = ("Report", "Work", "Studio", "Interactions", "Delivery", "Related", "Timeline", "Skills", "Files")   # Skills before Files (focus_page.render, 261106)
# a draft step's button: its number and name, then its state word small (focus_draft.WORK; focus_page `<span class=vw>`)
BUTTON = {("section", "work"): {"Plan": ("1 · Plan", "sign"), "Write": ("2 · Write", "next"), "Evidence": ("3 · Evidence", "later"),
                                "Display": ("4 · Display", "later"), "Revise": ("5 · Revise", "later")}}


# ── the Studio cells: the buttons are the topics' Tags, in the order first seen, then Other (focus_page.render) ──────
STUDIO_GROUPS = (                    # a paper Board's topics by their Tags (s34-D01; _studio_groups.txt is no longer read)
    ("Ideation", (("s01-ideation", "the directions, and which one was chosen", "shaping"),)),
    ("Story", (("s02-story-<desk>-<idea>", "the paper's questions and claims", "agreed"),)),
    ("Plan", (("s03-paper-dataflow", "how the data becomes each answer", "shaping"),
              ("s04-paper-workflow", "Sections in reader order, to the send", "shaping"),
              ("s05-paper-checklist", "one line per thing the paper needs", "shaping"),
              ("s06-paper-displays", "which display carries each answer", "shaping"))),
    ("Other", (("s10-related-work-<venue>", "the closest papers, mapped", "shaping"),)),   # topics with no Tag
)
SECTIONS = (("t00_summary", "Summary"), ("t01_introduction", "Introduction"), ("t02_methods", "Methods"), ("t03_results", "Results"))
PROMPT_V = ("prompt", "✍️ Prompt · Studio · talk and sketch",
            "/haipipe-studio <the Board> a new topic: talk with me about this send\nand sketch it on the canvas; write no text yet.",
            "Run this in the Claude session \"<the Board>: <the version>\"; start it if it is not running.")
PROMPT_S = ("prompt", "✍️ Prompt · Studio · talk and sketch",
            "/haipipe-studio <the Board> a new topic: talk with me about <the Section>'s argument and sketch it\n"
            "on the canvas; write no text yet; what we settle goes into the Task's §1.",
            "Run this in the Claude session \"<the Board>: <the Section>\"; start it if it is not running.")
VERSION_STUDIO = (                   # its own topics by their Tags; the Board's topics and a Copy prompt row stay proposed (s37)
    ("Telling", (("s20-j01-telling", "how this version tells the story", "explore"),), ("Telling", "Review")),
    ("Review", (("s21-j01-round1", "round 1 comments, grouped", "shaping"),), ("Telling", "Review")),
    ("Board", (PROMPT_V, ("s02-story-<desk>-<idea>", "the paper's questions and claims", "agreed"),
               ("s04-paper-workflow", "Sections in reader order, to the send", "shaping")), ("Telling", "Review", "Board")),
)
SECTION_STUDIO = (                   # the step's Copy prompt box on top (focus_draft.studio_top, 261105), then its topics;
    ("Topics", (PROMPT_S, ("note", "No Studio topic names t00_summary yet.")), ("Topics",)),   # no topic: one Topics button
    ("Story", (PROMPT_S, ("s02-story-<desk>-<idea>", "the paper's questions and claims", "agreed")), ("Story", "Plan")),
)


# ── a version (a writing Job) and a Section (a draft Task), as the frame and paper_version.py draw them (261106) ──────
def _num(secs):
    return tuple(("sec", f"{k} · {t}", *rest) for k, (t, *rest) in enumerate(secs, 1))


def _lvl(process, results, ix="none"):
    """A Work view in its two parts, each numbered from 1; a part with nothing in it does not show; 🙋 Interaction last.
    A part's entry is (title, inner[, its state word[, its waiting line]])."""
    P = (("band", "⚙️ Process", ""),) + _num(process) if process else ()
    R = (("band", "📊 Results", ""),) + _num(results) if results else ()
    return P + R + (_ix(P + R, ix),)


def _res(results, ix="none"):
    """A Report view of a paper Job: its Results alone, numbered, no band (board_views.banded; 261106), then 🙋."""
    R = _num(results)
    return R + (_ix(R, ix),)


def _body(*inner, ix="none"):
    """A frame view (MindMap, Status, Text …): its content with no bar of its own, then 🙋 Interaction."""
    body = tuple(("body", x) for x in inner)
    return body + (_ix(body, ix),)


STEPW = lambda *w: tuple(f"{n} {x}" for n, x in zip(("Plan", "Write", "Evidence", "Display", "Revise"), w))
# each Section's text to read, a side tab per Section with its next step (board_results.section_tabs: the Board's
# Writing and a version's Draft views draw the same tabs, 261106); one state on every tab says nothing, so it drops
READ = (("", "Open the Section"), ("C1.P1", "<its sentences, to read>"), ("C1.P2", "<its sentences, to read>"))
TEXT_MAIN = ("📝 Text", ("sidetabs", (("Summary", "Plan: waits for your sign"), ("Introduction", "Evidence: waits for your answer"),
                                     ("Methods", "Write: next")), READ), "3 of 3 written")
TEXT_APPX = ("📝 Text", ("sidetabs", (("Appendix", ""),), READ), "1 of 1 written")
V_WORK = {   # paper_version.version_work_views: each view ⚙️ Process then 📊 Results (261106)
    "Draft-Main": ((("🪜 Sections", ("chips", (("t00_summary", STEPW("sign", "done", "next", "optional", "later")),
                                                ("t01_introduction", STEPW("done", "done", "asked", "optional", "next")),
                                                ("t02_methods", STEPW("done", "next", "later", "next", "later")))),
                     "2 wait for you", "🙋 Summary: Plan: waits for your sign"),), (TEXT_MAIN,)),   # board_results.sections_word
    "Draft-Appendix": ((("🪜 Sections", ("chips", (("t21_appendix", STEPW("done", "next", "later", "next", "later")),)), "0 of 1 done"),),
                       (TEXT_APPX,)),
    "Display-Main": ((("🖼️ Where each display stands", ("todo", (("Figure 1 · <its label>", "done", "Open"),
                                                                ("Table 1 · <its label>", "done", "Open")))),),
                     (("🖼️ Displays", ("rows", (("t01_figure-1", "Figure 1 · <its label> · drawn"),
                                                ("t02_table-1", "Table 1 · <its label> · drawn"))), "2 of 2 drawn"),)),
    "Display-Appendix": ((("🖼️ Where each display stands", ("todo", (("eFigure 1 · <its label>", "done", "Open"),))),),
                         (("🖼️ Displays", ("rows", (("t51_efigure-1", "eFigure 1 · <its label> · drawn"),)), "1 of 1 drawn"),)),
    "Values": ((("📋 Where each stands", ("todo", (("<a value group>", "done", "Open"), ("the Values tabs", "done", "Open"),
                                                  ("the whole-paper check", "not started", "Open")))),),
               (("🔢 Values", ("rows", (("t01_values-<group>", "<a value group> · filled"), ("t02_values-tabs", "the Values tabs · filled"),
                                       ("t99_values-check", "the whole-paper check · not run yet"))), "2 of 3 filled"),)),
    "Citations": ((("📋 Where each stands", ("todo", (("<a claim group>", "done", "Open"), ("the whole-paper check", "not started", "Open")))),),
                  (("📚 Citations", ("rows", (("t01_cite-<group>", "<a claim group> · 2 keys: 2 verified"),
                                             ("t99_cite-check", "the whole-paper check · not run yet"))), "2 of 2 verified"),)),
}
VERSION_WORK = tuple((v, _lvl(p_, r, "wait")) for v, (p_, r) in V_WORK.items())
# a version's Report: MindMap, then Work's six views, results only (paper_version.version_report_views; JL 261106: "a
# paper version's Report gets the same six views as its Work, showing results only"); the MindMap shows each Section
# with what it finds out (focus_page.parts_mindmap)
VERSION_KIDS = tuple((t.split("_")[0], n, "<what this Section must say>") for t, n in SECTIONS) + \
    (("t31", "Cover letter", "<why this paper, for this venue>"),)
VERSION_REPORT = (("MindMap", _body(("goalmap", "<the version>", VERSION_KIDS), ix="wait")),) + \
    tuple((v, _res(r, "wait")) for v, (_, r) in V_WORK.items())

# ── the evidence and submission Jobs on their own pages (paper_jobs.py, 261106), drawn as the version's Other Jobs ──
# Report: MindMap first, then each view's Results alone; Work: each view ⚙️ Process then 📊 Results. The Results are the
# Board's own pieces, so the pages agree: the Board's Displays, Values and Citations sections, drawn by the same tuples.
BOARD = dict(REPORT_ONLY)
B_SEC = lambda view, k: BOARD[view][k][2:]                    # (inner, word[, waits]) of a Board section
PLAN_STEP = ("🧭 Plan the displays", ("todo", (("🖼️ Plan the displays", "use /haipipe-paper-plan", "Open · Copy prompt"),)),
             "runs in <the Board's session>")
CHECK_RUN = ("⚙️ The check's Run", ("todo", (("Run the whole-paper check · <its headline>", "done", "Open"),)))
OTHER_JOBS = (   # (the Job's kind, its page (name, path, crumb, goal), its MindMap's Tasks, {view: (Process, Results)})
    ("display", ("j01_evidence_display", "…/Paper-Example/j01_evidence_display", "… › Paper-Example › j01_evidence_display",
                 "Goal: displays: one Task per figure or table, main then appendix"),
     (("t01", "Figure 1", "<what it shows>"), ("t02", "Table 1", "<who is in it>"), ("t51", "eFigure 1", "<the check it makes>")),
     {"Plan": ((PLAN_STEP,), (("📐 Plan", *B_SEC("Displays", 0)),)),
      "Displays": ((("🖼️ Where each display stands", ("todo", (("Figure 1 · 📈 Figure", "done", "Open"), ("Table 1 · 📊 Table", "done", "Open"),
                                                              ("eFigure 1 · 📈 Figure", "done", "Open")))),),
                   (("🖼️ Displays", *B_SEC("Displays", 1)),)),
      "Examples": ((), (("🔍 Examples", *B_SEC("Displays", 2)),))}),
    ("value", ("j02_evidence_value", "…/Paper-Example/j02_evidence_value", "… › Paper-Example › j02_evidence_value",
               "Goal: values: one Task per group of printed numbers, each read from a returned Result"),
     (("t01", "<a value group>", "<the numbers it reads>"), ("t02", "the Values tabs", "<the raw tables from the Runs>"),
      ("t99", "the whole-paper check", "every printed number at once")),
     {"Values": ((("📋 Where each stands", ("todo", (("<a value group>", "done", "Open"), ("the Values tabs", "done", "Open")))),),
                 (("🔢 Values", *B_SEC("Evidence", 0)),)),
      "Check": ((CHECK_RUN,), (("🔎 Check", ("rows", (("9 values", "6 match · 3 differ"), ("S3 · <a printed number>", "✅ matches <Run · file>"),
                                                    ("S5 · <another>", "❗ differs: <the Run's number>"))), "6 of 9 match"),))}),
    ("citation", ("j03_evidence_cite", "…/Paper-Example/j03_evidence_cite", "… › Paper-Example › j03_evidence_cite",
                  "Goal: citations: one Task per claim group, each from verified CITE Results"),
     (("t01", "<a claim group>", "<the papers that back it>"), ("t99", "the whole-paper check", "every citation at once")),
     {"Citations": ((("📋 Where each stands", ("todo", (("<a claim group>", "done", "Open"),))),),
                    (("📚 Citations", *B_SEC("Evidence", 1)),)),
      "Check": ((CHECK_RUN,), (("🔎 Check", ("rows", (("2 keys", "2 verified"), ("<paper key>", "card ✅ · record ✅ · verified"),
                                                    ("<paper key>", "card ✅ · record ✅ · verified"))), "2 of 2 verified"),))}),
    ("submission", ("j21_submission_v1130_venue", "…/Paper-Example/j21_submission_v1130_venue",
                    "… › Paper-Example › j21_submission_v1130_venue",
                    "Goal: everything the portal asks beside the manuscript, ready to review and paste"),
     (("t01", "Cover letter", "the letter the portal takes"), ("t02", "Portal walk", "every field the portal asks"),
      ("t03", "Portal fill", "one page to review before the portal")),
     {"Cover letter": ((("✍️ The letter Section", ("todo", (("j11_writing_v1130_venue · t31_cover-letter · next: Plan", "waiting for you",
                                                            "Open"),)),
                         "1 waits for you", "🙋 j11_writing_v1130_venue · t31_cover-letter: next: Plan"),),
                       (("✉️ Cover letter", ("paras", (("Open the letter PDF · Open the Section", 0), ("Dear Editor", 2),
                                                        ("<why this paper, for this venue>", 2))), "1 of 1 written"),)),
      "Portal": ((("🧭 Walk and fill", ("todo", (("Portal walk", "done", "Open"), ("Portal fill", "not started", "Open")))),),
                 (("📮 Portal", ("todo", (("1 · <a portal slot> · <its file>", "ready", "Open"), ("2 · <a portal slot>", "no file yet", ""),
                                         ("The fill page · every field to check and paste", "waits for you", "⤢ Pop out"))),
                   "waits for you", "🙋 Check every field on the fill page, then press Submit in the portal yourself"),))}),
)


def other_jobs(section):
    """The Other Jobs' rows for a version cell: (kind, page, its views), Report's MindMap first."""
    out = []
    for kind, page, kids, views in OTHER_JOBS:
        if section == "report":
            items = (("MindMap", _body(("goalmap", page[0], kids))),) + tuple((v, _res(r)) for v, (_, r) in views.items())
        else:
            items = tuple((v, _lvl(p_, r)) for v, (p_, r) in views.items())
        out.append((kind, page, items))
    return out


# Each step as the draft workbench shows it today (focus_draft.step_html): ⚙️ Process 📌 Where this step stands (a Run
# running, its ask, its sign: only a step that waits, runs or is signed), 🤖 Ask the agent (Plan, Write, Revise), 📥
# Input, 🏃 Runs of this step, each only with content, each bar with the step's state word; 📊 Results, the step's own
# cards, by the names and words draft_steps gives them; then 🙋 Interaction.
STRUCT = ("narrative", "<Section>", (("C1.P1", "<point 1> · <point 2>"), ("C1.P2", "<point 3> · <point 4>"),
                                    ("C1.P3", "<point 5>"), ("C1.P4", "<point 6> · <point 7>")))
PARAS = (("C1.P1 · Background", 2), ("C1.P2 · Methods", 3), ("C1.P3 · Findings", 2))
TEXT = ("paras", PARAS)
TEXT_WRITE = ("split", PARAS, "✍️ Write it yourself", "editor")                     # draft_steps._text_and_editor
TEXT_EVIDENCE = ("split", PARAS, "🔎 Its evidence", {3: ("VALUE <the number>", "checked"), 5: ("CITE <the source>", "owed"),
                                                     6: ("DISPLAY Figure 1", "drawn")})  # draft_steps ev-split
# Revise as the page lays it out (draft_steps._revise, _text_and_cards): the text on the left, a + beside each sentence
# for your comment; on the right the pass's cards in reading order, filtered by chips (Comments · Logic · Edits ·
# Evidence): an Edit card with ✓ Accept ✗ Reject ✎ Edit, your Comment and its reply, a Logic score per sentence
TEXT_REVISE = ("split", PARAS, "🃏 Revise cards · Pass 2\n[Comments] [Logic] [Edits] [Evidence]",
               {2: ("Edit · <Why · Original → Expected>", "✓ Accept ✗ Reject ✎ Edit"), 4: ("Comment · <your note>", "AI replied"),
                6: ("Logic · S6 · logic 7/10 · read 8/10", "")})
TEXT_READ = ("split", PARAS, "Its evidence, read only", {3: "VALUE <the number> · checked", 5: "CITE <the source> · owed",
                                                         6: "DISPLAY Figure 1 · drawn"})   # focus_draft.text_html: read, never decided
STEP_CARDS = {   # each card by the name draft_steps gives it, drawn as a scratch of its layout (JL 261101), with its word;
    # the Revise pass's report, marks, rules and older versions carry no word on the live page, so none here (261106)
    "Plan": (("📐 §1 Structure · v0.1", STRUCT, "waits for your sign"),
             ("Scratch · your notes, a paragraph each", ("editor", "<your note on C1.P1>"), "yours to edit"),
             ("📚 Examples", ("rows", (("<an example paper>", "what to copy from it"), ("<another>", "its opening move"))), "drawn"),
             ("🧭 The Section's contract, from its Story", ("rows", (("Answers", "RQ1, RQ2"), ("Claims", "C1, C2"), ("Words", "<its budget>"))),
              "7 of 7 set"),
             ("📏 Requirement and Rubric", ("rows", (("<a venue rule>", "must"), ("<a rubric point>", "scored /10"))), "set"),
             ("🗂 Records", ("rows", (("<context record>", "<date>"), ("<plan record>", "<date>"))), "2 kept")),
    "Write": (("📚 Examples", ("rows", (("<an example paper>", "its paragraph shape"),)), "drawn"),     # Examples first, as live
              ("✍️ The text · v0.1", TEXT_WRITE, "no marks open")),
    "Evidence": (("🔎 The text and its Evidence · v0.1", TEXT_EVIDENCE, "2 of 3 found"),
                 ("❓ Open points", ("rows", (("OPEN 1 · S7", "<a value with no Run> · to find"),)), "1 open"),
                 ("✍ Asks, for you to tick", ("todo", (("S3 · VALUE · <the number it quotes>", "waiting for you", "Tick"),
                                                      ("S5 · CITE · <the source>", "done", "Open"))), "1 waits for you"),
                 ("❗ What does not resolve", ("todo", (("S7 · <a value with no Run>", "not started", "Open"),)), "1 to fix")),
    "Display": (("🖼 The text and its displays · v0.1", ("picture", "<Figure 1, beside the sentence that calls it>"), "1 of 1 made"),),
    "Revise": (("📋 Revise Review Report · Pass 2", ("rows", (("Mechanics", "MEETS · 8/10 · Fix: <the smallest fix>"),
                                                               ("Function", "NEEDS WORK · 6/10 · Fix: <the smallest fix>"),
                                                               ("Evidence", "MEETS · 8/10"), ("Readability", "MEETS · 9/10"),
                                                               ("Coherence · Anti-AI · Venue", "<each, the same way>"))), ""),
               ("✍️ The text and its Revise cards · v0.2", TEXT_REVISE, "1 comment open"),
               ("💬 Your marks from the canvas", ("rows", (("<a red mark on the drawing>", "its words"),)), ""),
               ("📜 Revise rules · how a pass runs, and the author's rulings", ("rows", (("R1", "<a rule>"), ("R2", "<your ruling>"))), ""),
               ("🕘 Older versions", ("rows", (("draft-v0.1", "previous/"),)), "")),
}
SECTION_REPORT = (                   # MindMap · Text · Status, opening on Text (focus_draft.report_views); cards read only
    ("MindMap", _body(("canvas", "<the Section>", (("C1.P1", "<point 1> · <point 2>"), ("C1.P2", "<point 3> · <point 4>"),
                                                   ("C1.P3", "<point 5>"))))),
    # the text is one bar now, the step's own card read flat (focus_draft.text_html, 261106)
    ("Text", (("sec", "🔎 The text and its Evidence · v0.1", TEXT_READ, "2 of 3 found"),
              _ix((), "none"))),
    ("Status", _body(("todo", tuple((f"{s} · {what}", w, "Go") for s, what, w in (
        ("Studio", "optional", "optional"), ("1 · Plan", "waits for your sign", "sign"), ("2 · Write", "comes next", "next"),
        ("3 · Evidence", "later", "later"), ("4 · Display", "optional", "optional"), ("5 · Revise", "later", "later"),
        ("Delivery", "later", "later")))))),
)
SAID = {"Plan": "waits for your sign", "Write": "comes next", "Evidence": "later", "Display": "later", "Revise": "later"}   # BUTTON's
INPUT = {"Plan": "2 of 5 missing", "Write": "1 of 5 missing", "Evidence": "3 of 5 missing", "Display": "2 of 5 missing",   # words, as
         "Revise": "1 of 5 missing"}                                                                                      # STATUS_WHAT


def _step(name):
    if name == "Runs":                         # the base page's list of the Task's Runs: no bands
        return _body(("todo", (("<a Run of this Section>", "done", "Open"), ("<a Run of this Section>", "running", "Open"))))
    said, proc = SAID[name], []
    if name == "Plan":                         # the one step that waits on you here: its ask, under the closed bar too
        proc.append(("📌 Where this step stands", ("todo", (("The plan: waits for your sign", "waiting for you", "Open the draft"),)),
                     said, "🙋 The plan: waits for your sign: ✅ on approved: in the draft"))
    if name in ("Plan", "Write", "Revise"):
        proc.append(("🤖 Ask the agent", ("rows", (("Copy prompt", "the step's prompt, with your notes"),)), said))
    proc += [("📥 Input", ("line", "the table of what the step reads"), INPUT[name]),
             ("🏃 Runs of this step", ("rows", (("<a Run>", "its type · its status"),)), "1 of 1 done")]
    return _lvl(proc, STEP_CARDS[name])


SECTION_WORK = tuple((v, _step(v)) for v in tuple(STEP_CARDS) + ("Runs",))
assert [v for v, _ in SECTION_WORK][:-1] == [x.split(" · ")[1] for x in STEPS], "draft_steps.STEPS changed"


# ── each cell: the line above its screens, its views, its open question (None: none), its green notes, its proposals ──
CLOSED = ("261105", "every bar starts closed; 🙋 Interaction is the last section")
NO_IX_STEP = ("261105", "Process has no 🙋 step now; 🙋 Interaction is the last section")
WORDS = ("261106", "Skills on the rail; each bar's state word, what waits under it")     # every Report and Work screen
OWN_IX = ("261106", "🙋 Interaction: this view's own items only")
RAIL_SKILLS = ("261106", "Skills on the right rail, before Files")                       # every Studio screen
NO_SKILLS = ("261106", "Process: 🧰 Skills moved to the rail")


def every(notes, n, *more):
    """The green notes of n screens, A on, each with `more` added after its own."""
    return {LETTERS[k]: list(notes.get(LETTERS[k], [])) + list(more) for k in range(n)}


def other_notes(section, first):
    """Each Other Job screen's note: new on 261106."""
    out, k = {}, first
    for kind, _, items in other_jobs(section):
        for v, _ in items:
            out[LETTERS[k]] = [("261106", f"new: the {kind} Job's own page"), WORDS]
            k += 1
    return out


VIEWS = {   # (level, section): (the line above the screens, the views, the open question, green notes[, proposed views])
    ("board", "report"): (LAYERS + "\nevery bar starts closed (▸), its state word on its right and what waits on you under it; under them, what it shows "
                          "once opened;\n🙋 Interaction, each view's last section, holds that view's own items; Skills is a right-rail section",
                          REPORT_SECTIONS, None,
                          every({"A": ["A: RESULTS · PROCESS bands", ("261105", "its own view: Studio, Directions, Theory; no Hand-off"), CLOSED],
                                 "B": [("261105", "its own view: Studio first; Theory and Related added"), CLOSED],
                                 "C": [("261105", "one view: two mind-map canvases, then Roadmaps"), CLOSED],
                                 "D": [("261105", "the trees fold, and show each Task's Runs"), CLOSED],
                                 "E": [CLOSED],
                                 "F": [("261105", "the plan's drawing, the displays by group, Examples"), CLOSED],
                                 "G": [("261105", "adds Ready for the portal"), CLOSED]}, 7, WORDS, OWN_IX)),
    ("board", "work"): ("the same views and letters as Report; each: ⚙️ Process (📌 Open points, one list of the lines a face marks waiting and the\n"
                        "Open rows; the view's own steps), then 📊 Results (the Report's sections), then 🙋 Interaction; who does it is the rail's Skills",
                        WORK_SECTIONS, "? a new review round on A to G\n(Process changed 261105, 261106)",
                        every({"A": ["A: PROCESS · RESULTS bands (proposed)", ("261105", "Process: 📌 Open points, 🚧 Open, 🧰 Skills"), NO_IX_STEP,
                                     ("261106", "Process: one 📌 Open points; 🧰 Skills moved to the rail")],
                               "B": [("261105", "Process: 📌 Open points, 🚧 Open, 🧰 Skills"), NO_IX_STEP,
                                     ("261106", "Process: one 📌 Open points; 🧰 Skills moved to the rail")],
                               "C": [("261105", "Process: 🧭 Plan, Runs to do, Next steps, 🧰 Skills"), NO_IX_STEP, NO_SKILLS],
                               "D": [("261105", "Process: 🧰 Skills that do it only"), NO_IX_STEP,
                                     ("261106", "no Process: its 🧰 Skills moved to the rail")],
                               "E": [NO_IX_STEP, NO_SKILLS], "F": [NO_IX_STEP, NO_SKILLS], "G": [NO_IX_STEP, NO_SKILLS]}, 7, WORDS, OWN_IX)),
    ("board", "studio"): ("the buttons are the topics' Tags, in the order first seen, then Other for the topics with none", STUDIO_GROUPS,
                          None, every({"A": [("261105", "buttons: the topics' Tags, then Other")],
                                       "C": [("261105", "Plan holds the checklist and the display plan too")],
                                       "D": [("261105", "Other: the topics with no Tag")]}, 4, RAIL_SKILLS)),
    ("version", "report"): ("MindMap (each Section with what it finds out), then the same six views as Work, its 📊 Results alone, numbered, no band; then\n"
                            "🙋 Interaction; Values and Citations show once the paper has their Tasks. Other Jobs, below: the evidence and submission Jobs' pages",
                            VERSION_REPORT, None,
                            {"A": ["A: both parts, content as today (proposed)", ("261105", "as live: the map, then 🙋 Interaction; no bands"),
                                   ("261106", "replaces MindMap · Status · Findings and the regroup proposal"),
                                   ("261106", "the map: each Section and what it finds out"), WORDS],
                             **{L: [("261106", f"new: Work's {v}, results only" + (": each Section's text, side tabs" if v.startswith("Draft") else "")),
                                    WORDS] for L, (v, _) in zip(LETTERS[1:], VERSION_REPORT[1:])},
                             **other_notes("report", len(VERSION_REPORT))}),
    ("version", "work"): ("each view: ⚙️ Process (Draft: 🪜 Sections, each with its five step words; the others: where each stands), then 📊 Results\n"
                          "(Draft: each Section's text in side tabs; the others: their items), then 🙋 Interaction. Other Jobs, below: the evidence and submission Jobs' pages",
                          VERSION_WORK, None,
                          {**every({"A": ["A: content as today (proposed)", NO_IX_STEP, ("261106", "📊 Results: each Section's text in side tabs")],
                                    "B": [NO_IX_STEP, ("261106", "📊 Results: each Section's text in side tabs")],
                                    "C": [("261105", "no Process band: 📊 Results, then 🙋 Interaction"),
                                          ("261106", "⚙️ Process: where each stands, then 📊 Results")],
                                    "D": [("261105", "no Process band: 📊 Results, then 🙋 Interaction"),
                                          ("261106", "⚙️ Process: where each stands, then 📊 Results")],
                                    "E": [("261105", "no Process band: 📊 Results, then 🙋 Interaction"),
                                          ("261106", "⚙️ Process: where each stands, then 📊 Results")],
                                    "F": [("261105", "no Process band: 📊 Results, then 🙋 Interaction"),
                                          ("261106", "⚙️ Process: where each stands, then 📊 Results")]}, 6, WORDS),
                           **other_notes("work", len(VERSION_WORK))}),
    ("version", "studio"): ("the buttons are the Tags of the topics that name this version (Studio shows once one does);\n"
                            "C, the Board's topics under a Copy prompt row, is proposed, not built", VERSION_STUDIO,
                            "? add the Board's topics as a group,\nand a Copy prompt row on top",
                            every({"A": [("261105", "buttons: the Tags of the topics that name it")],
                                   "C": [("261105", "the Board group and Copy prompt: still a proposal")]}, 3, RAIL_SKILLS), ("Board",)),
    ("section", "report"): ("MindMap · Text · Status, opening on Text; each its content, then 🙋 Interaction (no bands); Text is one bar,\n"
                            "its state word on its right; Skills is a right-rail section", SECTION_REPORT,
                            "? regroup each view: 📊 Results,\nthen ⚙️ Process (proposed 261101)",
                            every({"A": [("261105", "as live: the map, then 🙋 Interaction")],
                                   "B": ["B: content as today (proposed)", ("261105", "as live: the text with its cards read only, then 🙋 Interaction"),
                                         ("261106", "the text is one bar: 🔎 The text and its Evidence")],
                                   "C": [("261105", "as live: each step's row and Go, then 🙋 Interaction")]}, 3, WORDS, OWN_IX)),
    ("section", "work"): ("buttons 1 · Plan … 5 · Revise, each with its state word (4 · Display only when the Section has a display), then Runs; each step:\n"
                          "⚙️ Process (📌 Where this step stands only when it waits, runs or is signed; 🤖 Ask the agent; 📥 Input; 🏃 Runs of this step),\n"
                          "📊 Results, 🙋 Interaction; each bar its state word, the step's own on Process",
                          SECTION_WORK, "? the same sections, regrouped\n(proposed 261101)",
                          every({"A": ["A: content as today (proposed)", ("261105", "📌 Where this step stands replaces the 🙋 step"), CLOSED],
                                 "B": [("261105", "📌 Where this step stands replaces the 🙋 step"), CLOSED,
                                       ("261106", "no 📌: the step does not wait; Examples first")],
                                 "C": [("261105", "📌 Where this step stands replaces the 🙋 step"), CLOSED,
                                       ("261106", "no 📌 or 🤖; ❓ Open points added")],
                                 "D": [("261105", "shows only when the Section has a display"), CLOSED, ("261106", "no 📌 or 🤖")],
                                 "E": [("261105", "📌 Where this step stands replaces the 🙋 step"), CLOSED,
                                       ("261106", "no 📌: the step does not wait")],
                                 "F": [("261105", "as live: the Runs, then 🙋 Interaction; no bands")]}, 6, WORDS, OWN_IX)),
    ("section", "studio"): ("the step's Copy prompt box on top, then the topics that name this Section;\n"
                            "the buttons are their Tags (B), else one Topics button (A)", SECTION_STUDIO,
                            "? start a topic from here\nwith one click",
                            every({"A": [("261105", "the Studio step's Copy prompt box now shows on top")],
                                   "B": [("261105", "buttons: the Tags of the topics that name it")]}, 2, RAIL_SKILLS)),
}
PIECE = {
    ("board", "report"): ("the Board's Report: the paper's four layers as views",
                          ["a Board opened on steps,\nnot on what it found", "answers sat in report\nfolders, unread", "no one line said\nhow far it has got"]),
    ("board", "work"): ("the Board's Work: the same views, each layer's work",
                        ["versions sat as a\ndropdown, not rows", "no row said which\nversion waits", "the old frame drew\nthree rows of tabs"]),
    ("board", "studio"): ("the Board's Studio: the paper's topics, by Tag",
                          ["Story and Ideation hid\nin old Spaces", "topics were one long\nlist, no groups", "a row said too much"]),
    ("version", "report"): ("a version's Report: the paper as the reader gets it",
                            ["a version hid which\nSection waits on me", "no whole manuscript\nto read", "status lived in chips"]),
    ("version", "work"): ("a version's Work: its Sections and their steps",
                          ["seven tabs per Section\nin a card", "no word said which\nstep waits", "a click went to\nthe old page"]),
    ("version", "studio"): ("a version's Studio: the topics that name it",
                            ["a send's telling had\nno place of its own", "review rounds sat\nin the Board", "no talk-and-sketch\nprompt here"]),
    ("section", "report"): ("a Section's Report: sentences beside their cards",
                            ["Findings said No\ntakeaways recorded", "the text read as\none block", "no evidence beside\nthe sentence"]),
    ("section", "work"): ("a Section's Work: the draft Task page",
                          ["the steps were old\npages in iframes", "cards inside cards,\nfold arrows", "no verb said what\nto do next"]),
    ("section", "studio"): ("a Section's Studio: always on the right-rail",
                            ["Studio sat as a\nWork button", "no topic named the\nSection: it vanished", "the prompt was\na long box"]),
}


# the letters settled so far: all seven of the Board's Report (s32-D24; redrawn as live 261105)
AGREED = {("board", "report"): {LETTERS[k]: secs for k, (_, secs) in enumerate(REPORT_SECTIONS)}}
MOCK = """<!doctype html><meta charset=utf-8><title>{letter} · {view}</title>
<!-- GENERATED by paper_ui_cells.py from AGREED; the agreed screen of {nn} view {letter} -->
<style>body{{font:14px system-ui;margin:24px;max-width:820px;color:#1e1e1e;background:#fff}}h1{{font-size:22px;margin:0}}
h1 small{{color:#868e96;font-weight:400;margin-left:8px}}nav{{margin:12px 0 18px}}nav span{{display:inline-block;border:1px solid
#ced4da;border-radius:6px;padding:3px 9px;margin-right:6px;font-size:12px}}nav span.on{{border-color:#e8590c;background:#fff4e6}}
section{{border:1px solid #dee2e6;border-radius:8px;padding:9px 14px;margin:8px 0}}section b{{font-size:13px}}
section i{{float:right;font-style:normal;font-size:12px;color:#868e96}}section i.you,section em{{color:#b35c00}}
section em{{display:block;font-style:normal;font-size:13px}}</style>
<h1>Paper-Example<small>{section}</small></h1><nav>{nav}</nav>{secs}"""


def write_agreed(topic, nn, level, section):
    """delivery/ui/<level>-<section>/<L>-<view>.html for each settled letter; the screen, placeholder words only. A letter
    file not in the current set (a view renamed or relettered) is removed, so the folder holds this build's files only."""
    names = [it[0] for it in VIEWS[(level, section)][1]]
    agreed = AGREED.get((level, section), {})
    folder = topic / "delivery" / "ui" / f"{level}-{section}"
    written = set()
    for letter, secs in agreed.items():
        view = names[LETTERS.index(letter)]
        out = folder / f"{letter}-{slug(view)}.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        nav = "".join(f'<span class={"on" if v == view else "off"}>{v}</span>' for v in names)
        out.write_text(MOCK.format(letter=letter, view=view, nn=f"s{nn}", section=VERB[section], nav=nav,
                                   secs="".join(agreed_sec(sec) for sec in secs if flat(sec)[0])) + "\n", encoding="utf-8")
        written.add(out.name)
    if agreed and folder.is_dir():
        for stale in sorted(folder.glob("[A-Z]-*.html")):
            if stale.name not in written:
                print(f"removed stale {stale.relative_to(topic)}")
                stale.unlink()


def agreed_sec(sec):
    """One section of the agreed screen file: its bar (title, then its state word on the right), its waiting line, then
    what it holds, in one line."""
    t, w = flat(sec)
    word, waits = bar_words(sec) if sec[0] == "sec" else ("", "")
    return (f"<section><b>▸ {t}</b>" + (f'<i{" class=you" if waits_on_you(word) else ""}>{word}</i>' if word else "")
            + (f"<em>{waits}</em>" if waits else "") + f"<br><small>{w}</small></section>")


def flat(sec):
    """(title, one line) of a section in either form, for the agreed screen file."""
    if sec[0] in ("rule", "note"):
        return "", ""
    if sec[0] == "band":
        return sec[1], sec[2]
    if sec[0] == "body":
        return flat(("sec", "", sec[1]))
    if sec[0] != "sec":
        return sec[0], sec[1]
    inner = sec[2]
    words = {"tiles": lambda: " · ".join(t for t, _ in inner[1]), "cardtabs": lambda: " · ".join(t for t, _ in inner[1]),
             "cardtabchain": lambda: " → ".join(n for _, n in inner[1]),
             "narrative": lambda: " · ".join(n for n, _ in inner[2]),
             "goalmap": lambda: " · ".join(f"{t}: finds out {g}" for _, t, g in inner[2]),
             "canvas": lambda: "its mind map, worked on in place: " + " · ".join(n for n, _ in inner[2]),
             "studio": lambda: "Open in Studio · Slides · Draw; its mind map, worked on in place; its picture",
             "flowmap": lambda: " → ".join(h for h, _ in inner[1]),
             "ftree": lambda: " · ".join(n for d, n, _ in inner[1] if d == 2),
             "sidetabs": lambda: " · ".join(h for h, _ in inner[1]), "chain": lambda: " → ".join(n for _, n in inner[1]),
             "gtabs": lambda: " · ".join(f"{g}: " + ", ".join(h for h, _ in items) for g, items in inner[1]),
             "picture": lambda: "Slides · Draw", "drawing": lambda: "Draw · " + inner[1],
             "todo": lambda: " · ".join(f"{w} ({st})" for w, st, _ in inner[1]),
             "rows": lambda: " · ".join(n for n, _ in inner[1])}.get(inner[0], lambda: inner[1])()
    return sec[1], words.replace("\n", " ")


def build(topic: Path):
    topic = Path(topic).resolve()
    m = re.match(r"s(\d+)-(board|version|section)-ui-(report|work|studio)$", topic.name)
    nn, level, section = m.group(1), m.group(2), m.group(3)
    piece, why = PIECE[(level, section)]
    lay, items, ask, changed, *more_ = VIEWS[(level, section)]
    proposed = more_[0] if more_ else ()
    others = other_jobs(section) if level == "version" and section != "studio" else []   # the Other Jobs, after the
    names = [it[0] for it in items]                                                       # version's own views (261106)
    labels = [f"the {v} view" for v in names] + [f"the {kind} Job's {v} view" for kind, _, its in others for v, _ in its]
    last = LETTERS[len(labels) - 1]
    write_agreed(topic, nn, level, section)
    ui = topic / "delivery" / "ui"
    part = f"ui/{level}-{section}"
    lettered = True                                  # every cell: one lettered screen per view (JL 261031)
    pieces = [("page", f"{part}/{L}-{slug(v)}.html", f"{L} · {lab}", (ui / f"{level}-{section}" / f"{L}-{slug(v)}.html").exists())
              for L, v, lab in zip(LETTERS, names + [v for _, _, its in others for v, _ in its], labels)]
    sk = topic / "delivery" / "skill" / f"{level}-{section}-views.md"
    pieces.append(("book", f"skill/{sk.name}", "the views' manual, for workbench-paper", sk.exists()))
    spec = {"title": f"{level.capitalize()} UI · {VERB[section]}: {piece.split(': ', 1)[1]}",
            "why": {"question": f"why do we need s{nn}?", "notes": why,
                    "quote": "JL 261031: 3 x 3, Board, version, Section × Report, Work, Studio"},
            "what": {"head": f"② what s{nn} hands over: one screen", "icon": "page", "name": "delivery/ui/", "type": "ui",
                     "deck_why": f"stays in s{nn}'s delivery/deck/, so anyone gets it in a minute",
                     "parts": pieces},
            "job": topic.parent.parent,
            "target": {"board": "servers/workbench-paper/ (the Board page)", "version": "servers/workbench-paper/ (a version page)",
                       "section": "workbench-task-draft/focus_draft.py (b32 s42)"}[level],
            "missing": [(name, "not settled yet") for _, name, _, done in pieces if not done and lettered]
                       or ([] if (ui / f"{level}-{section}").exists() else [(part, "the agreed screen, not drawn yet")])}
    if lettered:
        spec["have"] = [(name, "agreed") for icon, name, _, done in pieces if done and icon == "page"]
        spec["what"]["head"] = f"② what s{nn} hands over: one screen, A to {last}"
        spec["target"] = "servers/workbench-paper/ · workbench-paper/SKILL.md"

    def design():                                    # A, B, C … every view the same screen; no separate main sketch
        els = text("skA", 690, 280, f"A to {last} · {piece}, every view the same screen", 18, TITLE)
        els += text("lay", 690, 340, lay, 16, BODY)
        e, bottom = screens("sc", 690, 380 + 22 * lay.count("\n"), items, level, section, changed, proposed=proposed)
        if others:                                   # the evidence and submission Jobs' own pages, one row a Job (261106)
            k = len(items)
            e += text("oj", 690, bottom + 10, f"Other Jobs · {LETTERS[k]} to {last}: the evidence and submission Jobs' own pages "
                      "(paper_jobs.py), one row a Job", 22, TITLE)
            bottom += 70
            for g, (kind, page, its) in enumerate(others):
                e += text(f"oj{g}", 690, bottom, f"{kind} Job · {page[0]}: " + " · ".join(v for v, _ in its), 16, BODY)
                ge, bottom = screens(f"oj{g}s", 690, bottom + 34, its, level, section, changed, first=k, page=page)
                e += ge
                k += len(its)
        # the open question in red; a cell with none open draws no sticky (s34-D01 settled its question, 261105)
        return els + e + (sticky("askD", 1180, bottom + 20, 320, 76, ask, 15, -0.03, RED, RE) if ask else [])

    random.seed(topic.name)                          # quick_draw's element seeds come from `random`: a rebuild of the
    return five_parts.build(topic, spec, design, shift=2300 - 925 * (3 - min(3, len(items))),   # same cell writes the same file
                            writer=five_parts.marks_writer)   # the person's canvas marks stay (261105)
