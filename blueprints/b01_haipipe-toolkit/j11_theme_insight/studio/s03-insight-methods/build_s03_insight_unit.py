"""s03 · the Insight unit as a catalog: s03-insight-unit.excalidraw, a plain prototype.

The same picture as the Design workbench's design-unit catalog (servers/workbench-design/studio/
design_unit_drawing.py), drawn for one Insight question (JL 261007: "what is draw again? could you
draw it again? and put it here"):

1 · The catalog      one column per step of guide/method.md's six steps; in each, its parts and the
                     options for each part (the method cards at steps 1, 3 and 5, the tests at their
                     step, read at build time)
2 · The methods      one row per method: the option it picks in each step, a part left out is open;
                     examples by DIKW level, then an empty row and a notes column to write in
open ?               loose red notes

Lines only, black and gray, red for what is open. Written through b03's canvas.write, so every mark a
person adds survives a rebuild.

    python build_s03_insight_unit.py [out.excalidraw]
"""
import re
import sys
import textwrap
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parents[4]
B03 = TOOLS / "blueprints" / "b01_haipipe-toolkit" / "j03_project_workbench" / "studio"
sys.path.insert(0, str(B03 / "s01-overall-tree-structure"))
sys.path.insert(0, str(B03 / "_build"))
sys.path.insert(0, str(HERE.parent / "_build"))
import build_ladder_v4 as L  # noqa: E402  (the drawing helpers)
sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))  # canvas (haipipe-studio)
import canvas  # noqa: E402
from insight_ui import CARDS, FAMS, scratch_questions  # noqa: E402  (the cards, as the level topics read them)

INK, GRAY, RED, SANS = L.INK, L.GRAY, L.RED, L.SANS
text, path, base = L.text, L.path, L.base
GUIDE = TOOLS / "plugins" / "haipipe-toolkit" / "servers" / "workbench-insight" / "guide"
read = lambda p: p.read_text(encoding="utf-8", errors="ignore") if p.is_file() else ""
wrap = lambda s, n: textwrap.wrap(s, n, break_on_hyphens=False) or [""]
cards = lambda fam: [c["name"].replace("By ", "by ") for c in CARDS[fam]]


def tests_at(step):
    """The tests guide/method.md places at a step: 'T4 Spec', … from its test table."""
    out = []
    for line in read(GUIDE / "method.md").splitlines():
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) >= 3 and re.match(r"T\d ", c[0]) and re.search(rf"step {step}\b", c[2]):
            out.append(c[0])
    return out


ASK, ANSWER, READ = (f[0] for f in FAMS)
LEVELS = ["Data", "Information", "Knowledge", "Wisdom"]

# the six steps: (title, board, what never varies, [(part, options)]) ----------------------------------
STEPS = [
    ("1 Ask the question", "Prototype", "one ask, why now, what would answer it", [
        ("DIKW level", LEVELS),
        ("Asking method", cards(ASK)),
        ("Signed by", ["a person"])]),
    ("2 Plan and agree", "Prototype", "plan: partition · unit · measure · grouping · uncertainty · rivals · output", [
        ("Written", ["before any data is read"]),
        ("Agreed by", ["a different agent"]),
        ("Tests", tests_at(2))]),
    ("3 Run each partition", "Instance", "the Prototype's script, a tracked copy, unchanged", [
        ("Answering method", cards(ANSWER)),
        ("Runs on", ["each partition", "the pooled extract", "a held-out partition"]),
        ("Maker", ["the script", "an agent with code"])]),
    ("4 Check the run", "Instance", "against its plan", [
        ("Checker", ["an agent that did not write the run"]),
        ("Returns", ["OK", "GAP", "STALE", "UNBOUND", "UNPLANNED"]),
        ("Tests", tests_at(4))]),
    ("5 Write the page", "Instance", "one page per question, a section per partition", [
        ("Reading method", cards(READ)),
        ("Checker", ["an agent that did not write the page"]),
        ("Tests", tests_at(5))]),
    ("6 Hand off", "Instance", "only what leaves the board", [
        ("To", ["the next DIKW level", "Design (a Wisdom answer)", "the next extract"]),
        ("Signed by", ["a person"]),
        ("Tests", tests_at(6))]),
]

# the methods: (name, what it is, {part key: option}); keys are "<step> <part>" -------------------------
METHODS = [
    ("a Data question", "what was observed, no reading", {
        "1 DIKW level": "Data", "1 Asking method": "by level", "3 Answering method": "by exploring",
        "3 Runs on": "each partition", "6 To": "the next DIKW level"}),
    ("an Information contrast", "a rate or a difference", {
        "1 DIKW level": "Information", "1 Asking method": "by estimand", "3 Answering method": "by hypothesis test",
        "3 Runs on": "each partition", "5 Reading method": "by heterogeneity", "6 To": "the next DIKW level"}),
    ("a Knowledge claim", "why it happens, with rivals", {
        "1 DIKW level": "Knowledge", "1 Asking method": "by question type", "3 Answering method": "by model comparison",
        "3 Runs on": "a held-out partition", "5 Reading method": "by multiverse", "6 To": "the next DIKW level"}),
    ("a Wisdom counsel", "what to do, for Design", {
        "1 DIKW level": "Wisdom", "1 Asking method": "by goal-question-metric", "5 Reading method": "by sensemaking",
        "6 To": "Design (a Wisdom answer)"}),
    ("the same protocol, next extract", "every question again", {
        "1 Asking method": "by protocol reuse", "3 Runs on": "each partition", "6 To": "the next extract"}),
]
OPEN = [
    "? which method a question used is recorded nowhere: give question.md a field per family",
    "? steps 2, 4 and 6 have rules, not methods: is a choice ever made there?",
    "? an answering run by an agent with code: the same as an Instance script, or its own method?",
    "? the rows are examples by DIKW level: are these the methods we want to compare?",
]

# 1 · the catalog --------------------------------------------------------------------------------------
CW_, PAD, LINE = 380, 18, 22                  # a column's width, its inner margin, a line's advance


def column_cell(x, y, part, options, color=INK):
    """A part: its name in gray, then its options, one per line; returns the y under it."""
    text(x + PAD, y, part, 14, GRAY)
    y += 22
    for o in options:
        for k, ln in enumerate(wrap(o, 40)):
            text(x + PAD + (14 if k else 0), y, ("· " if not k else "") + ln, 16, color)
            y += LINE
    return y + 10


def frame_catalog(y0):
    fr = L.open_frame("1 · The catalog")
    text(0, y0, "One Insight question · the catalog: each step's parts and their options", 34)
    text(0, y0 + 50, "Read from guide/method.md and the method cards at build time. Steps 1-2 are written once, "
                     "in the Prototype; steps 3-6 run on every dataset, in its Instance.", 20, GRAY)
    top = y0 + 110
    xs = [i * (CW_ + 30) for i in range(len(STEPS))]
    bottom = top
    for x, (title, board, fixed, parts) in zip(xs, STEPS):
        text(x + PAD, top + 14, title, 22)
        text(x + PAD, top + 46, board, 14, GRAY)
        y = top + 78
        for ln in wrap(fixed, 44):
            text(x + PAD, y, ln, 15, GRAY)
            y += 20
        y += 14
        path([(x, y), (x + CW_, y)], arrow=False, color=GRAY)
        y += 14
        for part, options in parts:
            y = column_cell(x, y, part, options or ["none"], RED if not options else INK)
            path([(x, y), (x + CW_, y)], arrow=False, color=GRAY)
            y += 14
        bottom = max(bottom, y)
    for x in xs:                                   # one box per step, all the same height
        base("rectangle", x, top, CW_, bottom - top, INK, 1.5)
    for a, b in zip(xs, xs[1:]):
        path([(a + CW_ + 4, top + 26), (b - 4, top + 26)])
    # the loop: what step 6 hands off is the next question's input
    ly = bottom + 50
    path([(xs[-1] + CW_ / 2, bottom + 4), (xs[-1] + CW_ / 2, ly), (xs[0] + CW_ / 2, ly), (xs[0] + CW_ / 2, bottom + 6)])
    text(xs[0] + CW_ / 2 + 20, ly + 12, "the loop: a handed-off answer is the next question's input "
                                        "(the next DIKW level up, Design, or the next extract)", 16, GRAY)
    L.close_frame(fr)
    return fr, xs


# 2 · the methods --------------------------------------------------------------------------------------
def frame_methods(x0, y0, xs):
    fr = L.open_frame("2 · The methods")
    text(x0, y0, "The methods · one row each, the option it picks in each step; a part left out is open", 30)
    NAME_W, NOTES_W = 300, 340
    cols = [x0 + NAME_W + x for x in xs]                  # the step columns, as in the catalog
    right = cols[-1] + CW_ + 30 + NOTES_W
    y = y0 + 70
    text(x0 + PAD, y + 12, "method", 16, GRAY)
    for c, (title, *_rest) in zip(cols, STEPS):
        text(c + PAD, y + 12, title, 16, GRAY)
    text(cols[-1] + CW_ + 30 + PAD, y + 12, "notes", 16, GRAY)
    y += 46
    rows = METHODS + [("", "", {})]                       # an empty row to write a method of one's own
    for name, what, picks in rows:
        cells = []
        for si, (_t, _b, _f, parts) in enumerate(STEPS, start=1):
            cells.append([f"{p}: {picks[f'{si} {p}']}" for p, _o in parts if f"{si} {p}" in picks])
        h = max([len(c) for c in cells] + [2]) * LINE + 30
        path([(x0, y), (right, y)], arrow=False, color=GRAY)
        text(x0 + PAD, y + 14, name, 18)
        text(x0 + PAD, y + 40, what, 14, GRAY)
        for c, items in zip(cols, cells):
            for k, s in enumerate(items):
                text(c + PAD, y + 14 + k * LINE, s, 15)
        y += h
    path([(x0, y), (right, y)], arrow=False, color=GRAY)
    for c in [x0, *cols, cols[-1] + CW_ + 30, right]:
        path([(c, y0 + 70), (c, y)], arrow=False, color=GRAY)
    L.close_frame(fr)
    return fr


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s03-insight-unit.excalidraw"
    L.els.clear()
    L.FRAME[0] = None
    a, xs = frame_catalog(0)
    b = frame_methods(0, a["y"] + a["height"] + 300, xs)
    scratch_questions(0, b["y"] + b["height"] + 300, OPEN)
    canvas.write(out, list(L.els), Path(__file__).name)


if __name__ == "__main__":
    main()
