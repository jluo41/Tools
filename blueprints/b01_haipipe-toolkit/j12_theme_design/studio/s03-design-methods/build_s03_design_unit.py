"""s03 · the design unit as a plain catalog: s03-design-unit.excalidraw, a plain prototype.

The same content as s03-design-methods.excalidraw (the product picture in Guide › Method), drawn in
this folder's plain style so it can be written on (JL 261007: "could you draw it again? … add it here"):

1 · The catalog      one column per step of the design unit (see input, reason ideas, conduct process,
                     check output, check overall), its parts and the options for each part
2 · The methods      one row per method: the option it picks in each step, a part left out is open;
                     the Stage 2.5 arms, then an empty row and a notes column to write in
open ?               loose red notes

The steps and methods are read from design_unit_drawing.py beside it (its STEPS, SHARED and METHODS
blocks), so the two drawings never disagree. Lines only, black and gray, red for what is open. Written
through b03's canvas.write, so every mark a person adds survives a rebuild.

    python build_s03_design_unit.py [out.excalidraw]
"""
import ast
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
from design_ui import scratch_questions  # noqa: E402

INK, GRAY, RED = L.INK, L.GRAY, L.RED
text, path, base = L.text, L.path, L.base
wrap = lambda s, n: textwrap.wrap(s, n, break_on_hyphens=False) or [""]


def unit_data():
    """STEPS, SHARED and METHODS from design_unit_drawing.py, without running its drawing code."""
    src = (HERE / "design_unit_drawing.py").read_text(encoding="utf-8")
    keep = {"IN", "ID", "PR", "CK", "OV", "STEPS", "SHARED", "METHODS"}
    ns: dict = {}
    for node in ast.parse(src).body:
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id in keep or isinstance(t, ast.Tuple) and
                any(isinstance(x, ast.Name) and x.id in keep for x in t.elts) for t in node.targets):
            exec(compile(ast.Module([node], []), "design_unit_drawing.py", "exec"), ns)
    return ns["STEPS"], ns["METHODS"]


STEPS, METHODS = unit_data()
OPEN = [
    "? which of the five steps does a person sign, and which does an agent close?",
    "? N + 5 then keep N: who keeps, the planner or ⑤'s ranker?",
    "? an idea made from the model's own knowledge only: how is it reviewed at ④?",
    "? the rows are the Stage 2.5 arms: are these the methods we want to compare?",
]

# 1 · the catalog --------------------------------------------------------------------------------------
CW_, PAD, LINE = 380, 18, 22                  # a column's width, its inner margin, a line's advance


def column_cell(x, y, part, options):
    """A part: its name in gray, then its options, one per line; returns the y under it."""
    text(x + PAD, y, part, 14, GRAY)
    y += 22
    for o in options:
        for k, ln in enumerate(wrap(o, 40)):
            text(x + PAD + (14 if k else 0), y, ("· " if not k else "") + ln, 16)
            y += LINE
    return y + 10


def frame_catalog(y0):
    fr = L.open_frame("1 · The catalog")
    text(0, y0, "One design unit · the catalog: each step's parts and their options", 34)
    text(0, y0 + 50, "Read from design_unit_drawing.py at build time. ③ and ④ run once per idea; "
                     "⑤ ranks every design together.", 20, GRAY)
    top = y0 + 160                                 # room above the columns for the "for each idea" box
    xs = [i * (CW_ + 30) for i in range(len(STEPS))]
    bottom = top
    for x, (title, sub, band, _colours, parts) in zip(xs, STEPS):
        text(x + PAD, top + 14, title, 22)
        text(x + PAD, top + 46, sub, 14, GRAY)
        y = top + 78
        for ln in band.split("\n"):
            for w in wrap(ln, 44):
                text(x + PAD, y, w, 15, GRAY)
                y += 20
        y += 14
        path([(x, y), (x + CW_, y)], arrow=False, color=GRAY)
        y += 14
        for part, options in parts:
            y = column_cell(x, y, part, options)
            path([(x, y), (x + CW_, y)], arrow=False, color=GRAY)
            y += 14
        bottom = max(bottom, y)
    for x in xs:                                   # one box per step, all the same height
        base("rectangle", x, top, CW_, bottom - top, INK, 1.5)
    for a, b in zip(xs, xs[1:]):
        path([(a + CW_ + 4, top + 26), (b - 4, top + 26)])
    # ③ and ④ run once per idea: one dashed box around both
    base("rectangle", xs[2] - 12, top - 40, 2 * CW_ + 30 + 24, bottom - top + 54, GRAY, 1, dashed=True)
    text(xs[2], top - 34, "for each idea · ×N (or N + 5)", 15, GRAY)
    # the loop: what ⑤ gives back is the next unit's input
    ly = bottom + 50
    path([(xs[-1] + CW_ / 2, bottom + 4), (xs[-1] + CW_ / 2, ly), (xs[0] + CW_ / 2, ly), (xs[0] + CW_ / 2, bottom + 6)])
    text(xs[0] + CW_ / 2 + 20, ly + 12, "the loop: what the unit gave back (its designs, their checks, the ranking) "
                                        "is the next unit's input", 16, GRAY)
    L.close_frame(fr)
    return fr, xs


# 2 · the methods --------------------------------------------------------------------------------------
def frame_methods(x0, y0, xs):
    fr = L.open_frame("2 · The methods")
    text(x0, y0, "The methods · one row each, the option it picks in each step; a part left out is open", 30)
    NAME_W, NOTES_W = 300, 340
    cols = [x0 + NAME_W + x for x in xs]
    right = cols[-1] + CW_ + 30 + NOTES_W
    step_of = {p: si for si, st in enumerate(STEPS) for p, _ in st[4]}
    y = y0 + 70
    text(x0 + PAD, y + 12, "method", 16, GRAY)
    for c, st in zip(cols, STEPS):
        text(c + PAD, y + 12, st[0], 16, GRAY)
    text(cols[-1] + CW_ + 30 + PAD, y + 12, "notes", 16, GRAY)
    y += 46
    rows = [(name, sub, picks) for name, sub, _colour, picks, _explain in METHODS] + [("", "", [])]
    for name, sub, picks in rows:
        cells = [[] for _ in STEPS]
        for si, st in enumerate(STEPS):
            order = [p for p, _ in st[4]]
            for p, o in sorted((pk for pk in picks if step_of[pk[0]] == si), key=lambda pk: order.index(pk[0])):
                cells[si].append(f"{p}: {o}")
        h = max([len(c) for c in cells] + [2]) * LINE + 30
        path([(x0, y), (right, y)], arrow=False, color=GRAY)
        text(x0 + PAD, y + 14, name, 18)
        text(x0 + PAD, y + 40, sub, 14, GRAY)
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
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "parts" / "s03-design-unit.excalidraw"
    L.els.clear()
    L.FRAME[0] = None
    a, xs = frame_catalog(0)
    b = frame_methods(0, a["y"] + a["height"] + 300, xs)
    scratch_questions(0, b["y"] + b["height"] + 300, OPEN)
    canvas.write(out, list(L.els), Path(__file__).name)


if __name__ == "__main__":
    main()
