"""s31 · Guide: s31-guide.excalidraw, a plain prototype in seven frames, in the style of
s04-studio-and-report (moved from b02's s02 when b02 merged into b03, 261007).

1 · Guide and the level tabs     what each is for, side by side
2 · From folder to Guide         the files a theme keeps, read by the loader, rendered as the Guide tab
3 · Guide on screen              the four Views, proposed: screen, on disk under each, pop-outs
4 · Guide today                  the same four Views as the server renders them now
5 · the logic tree               what a theme's Guide holds (lines) and how its files relate (labelled arrows)
6 · status                       each family's Guide, read off the code at build time
Questions                        what is still open

Black and gray lines, placeholders only; red marks what is open. Written through canvas.write, so
every mark a person adds survives a rebuild. The 261002 design and the first 261007 proposal are in
history/.

    python build_s31_guide.py [out.excalidraw]
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parents[3]
B03 = TOOLS / "blueprints" / "b03_project_workbench" / "studio"
sys.path.insert(0, str(B03 / "s01-overall-tree-structure"))
sys.path.insert(0, str(B03 / "_build"))
sys.path.insert(0, str(B03 / "s04-studio-and-report"))
import build_ladder_v4 as L  # noqa: E402  (the shared drawing helpers)
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))  # canvas (haipipe-studio)
import canvas  # noqa: E402
import studio_report_ui as UI  # noqa: E402  (the screen size and the pop-out window of b03 s04)

SERVERS = TOOLS / "plugins" / "haipipe-toolkit" / "servers"
sys.path.insert(0, str(SERVERS / "_host"))
from host_paths import bootstrap  # noqa: E402
bootstrap()
from live import guide_families as G  # noqa: E402

INK, GRAY, RED, MONO = L.INK, L.GRAY, L.RED, L.MONO
text, box, path, base = L.text, L.box, L.path, L.base
SIX = ("Description", "Idea Studio", "Audience Report", "Work Details", "Runs", "Delivery")
SW, SH, RW = UI.SW, UI.SH, UI.RW

COMPARE = [  # what · the Guide tab · a level tab (Block · Job · Task)
    ("job", "explain the family: what, how, why", "do the work of one folder"),
    ("holds", "4 Views, each in 3 folding sections: Block · Job · Task", "the six Spaces, filled from the folder"),
    ("shape", "cards: Space · step · drawing · paper", "rows, tables and drawings per Space"),
    ("reads", "the base's guide/levels.yaml + the theme's guide/, related/", "bNN_<topic>/ · jNN_/ · tNN_/ on disk"),
    ("words", "the base's card words; a theme overrides what differs", "its subspaces: the theme's words"),
    ("live", "each Space card's sub · runs, from the frame", "everything: read from disk per request"),
    ("the same in", "every Block of the theme; opens at your level", "one folder only"),
    ("who edits", "the theme's session: guide.yaml, method.md", "the Runs of that folder"),
    ("run types", "Add a method · Add a paper", "each Space's own"),
    ("on screen", "the first tab: Guide", "Block · Job ▾ · Task ▾"),
]
QUESTIONS = [
    "? levels.yaml: the base's home for the default card words (Block · Job · Task × the six Spaces)",
    "? folds: the tab you came from opens its level and folds the other two; remember a person's folds?",
    "? the page family (workbench/task-page): its own Guide, or the Task sections of each theme's Guide",
    "? a Method step whose 'where' is not one of the six Spaces: fail the tests, or warn on the page",
    "? RoadMap Draw per level: which drawings each theme lists first",
    "? b03's s11 · s12 · s13 (Block · Job · Task variants): draw their screens in this style",
]

def frame_compare(y0):
    fr = L.open_frame("1 · Guide and the level tabs")
    text(0, y0, "Guide and the level tabs: one explains, the others work", 34)
    text(0, y0 + 50, "Guide is the family's docs, the same in every Block, in Block · Job · Task sections; "
                     "the level tabs show one folder.", 20, GRAY)
    cols, widths = [0, 220, 960], [220, 740, 640]
    y = y0 + 110
    for i, head in enumerate(["", "Guide", "Block · Job · Task"]):
        text(cols[i] + 16, y + 14, head, 20, INK, MONO)
    for row in COMPARE:
        y += 56
        path([(0, y), (sum(widths), y)], arrow=False, color=GRAY)
        for i, cell in enumerate(row):
            text(cols[i] + 16, y + 16, cell, 18, GRAY if i == 0 else INK, MONO if "<" in cell or "/" in cell else L.SANS)
    y += 56
    path([(0, y), (sum(widths), y)], arrow=False, color=GRAY)
    for x in (cols[1], cols[2]):
        path([(x, y0 + 110), (x, y)], arrow=False, color=GRAY)
    L.close_frame(fr)
    return fr


def frame_flow(x0, y0):
    fr = L.open_frame("2 · From folder to Guide")
    text(x0, y0, "From folder to Guide: the base gives the shape and words, the theme its own, the frame the live parts", 34)
    text(x0, y0 + 50, "one renderer for every theme: 4 Views × 3 folding sections (Block · Job · Task), each a stack of cards",
         20, GRAY)
    W, H = 440, 64
    srcs = [("servers/workbench/guide/levels.yaml", "the base: card words, level × Space"),
            ("guide/guide.yaml", "description · skills · levels: · roadmap: · table"),
            ("guide/method.md + methods/", "## Block · ## Job · ## Task: steps · cards"),
            ("related/papers.md + papers/", "a row per paper, with its level · PDFs"),
            ("Tools/blueprints/bNN/studio/sNN-…", "the RoadMap drawings, named per level")]
    for k, (name, line) in enumerate(srcs):
        sy = y0 + 110 + k * 120
        box(x0, sy, W, H, name, 17)
        text(x0, sy + H + 6, line, 16, GRAY)
        path([(x0 + W + 8, sy + H / 2), (x0 + 650, y0 + 340)])
    loader = (x0 + 660, y0 + 308)
    box(*loader, 400, H, "guide_families.py", 18)
    text(loader[0], loader[1] + H + 8, "loads every guide.yaml;\nlevels: over the base's words", 16, GRAY)
    rend = (x0 + 1190, y0 + 308)
    box(*rend, 400, H, "workbench_guide.py", 18)
    text(rend[0], rend[1] + H + 8, "renders 4 Views × 3 folding\nsections, as cards", 16, GRAY)
    out = (x0 + 1720, y0 + 308)
    box(*out, 360, H, "the Guide tab", 18)
    text(out[0], out[1] + H + 8, "view only; opens at your level;\nRun types: Add a method · Add a paper", 16, GRAY)
    path([(loader[0] + 408, loader[1] + H / 2), (rend[0] - 8, rend[1] + H / 2)])
    path([(rend[0] + 408, rend[1] + H / 2), (out[0] - 8, out[1] + H / 2)])
    th = (x0, y0 + 110 + 5 * 120 + 20)
    box(*th, W, H, "<theme>_theme.py", 18)
    text(th[0], th[1] + H + 6, "Theme.spaces per level", 16, GRAY)
    fx = (x0 + 660, th[1])
    box(*fx, 400, H, "frame.py · spaces_for", 18)
    text(fx[0], fx[1] + H + 6, "the base, then the theme, per level", 16, GRAY)
    path([(th[0] + W + 8, th[1] + H / 2), (fx[0] - 8, fx[1] + H / 2)])
    path([(fx[0] + 408, fx[1] + H / 2), (rend[0] + 200, fx[1] + H / 2), (rend[0] + 200, rend[1] + H + 60)])
    text(rend[0] + 214, fx[1] - 40, "each Space card's sub · runs,\nlive: the Guide never drifts", 16, GRAY)
    L.close_frame(fr)
    return fr

TREE = {  # name -> (x, y, w, box text, the line under it): the logic tree of a theme's Guide
    # the base (s31-D06): the default card words, the one renderer, the frame
    "base": (0, 110, 320, "servers/workbench/", "the base, under every theme"),
    "levels": (420, 0, 340, "guide/levels.yaml", "the default card words: level × Space"),
    "render": (420, 110, 340, "workbench_guide.py", "one renderer: 4 Views · folds · cards"),
    "frame": (420, 220, 340, "frame.py", "spaces_for: each level's sub · runs"),
    # one theme
    "server": (0, 720, 320, "servers/workbench-<theme>/", "one theme"),
    "theme": (420, 400, 340, "<theme>_theme.py", "the theme on the frame"),
    "guide": (420, 640, 240, "guide/", "Description · Method · RoadMap Draw"),
    "related": (420, 960, 240, "related/", "Related Paper"),
    "yaml": (800, 500, 380, "guide.yaml", "description · skills · levels: · roadmap: · table"),
    "method": (800, 610, 380, "method.md", "## Block · ## Job · ## Task: the steps"),
    "cards": (800, 720, 380, "methods/<card>.md", "one method: what · where · tested"),
    "canvas": (800, 830, 380, "methods.excalidraw", "the methods canvas"),
    "papers": (800, 960, 380, "papers.md", "level · group · role · key · venue · doi · pdf"),
    "pdfs": (800, 1070, 380, "papers/<key>.pdf", "open-licensed only"),
    "table": (1480, 400, 420, "skills/…/ref/workbench-table.md", "run types · agent · skill"),
    "ladder": (1480, 560, 420, "bNN/studio/sNN-<topic>/", "the theme's drawings, listed per level"),
}
H = 52


def frame_tree(x0, y0):
    """The logic tree: what the base and a theme's Guide hold (plain lines), how their files relate
    (labelled arrows)."""
    fr = L.open_frame("5 · Guide: the logic tree")
    text(x0, y0, "The logic tree: what a theme's Guide holds, and how its files relate", 34)
    text(x0, y0 + 50, "plain line = holds  ·  arrow = a relationship, labelled  ·  red = open", 20, GRAY)
    oy = y0 + 150
    at = {k: (x0 + x, oy + y, w) for k, (x, y, w, _, _) in TREE.items()}
    for k, (x, y, w, name, line) in TREE.items():
        box(x0 + x, oy + y, w, H, name, 17)
        text(x0 + x, oy + y + H + 6, line, 15, GRAY)
    for parent, kids in [("base", ["levels", "render", "frame"]),
                         ("server", ["theme", "guide", "related"]), ("guide", ["yaml", "method", "cards", "canvas"]),
                         ("related", ["papers", "pdfs"])]:
        px, py, pw = at[parent]
        mx = px + pw + 40
        for k in kids:
            kx, ky, _ = at[k]
            path([(px + pw + 4, py + H / 2), (mx, py + H / 2), (mx, ky + H / 2), (kx - 4, ky + H / 2)],
                 arrow=False, color=INK)

    def rel(pts, label, where, color=GRAY, dashed=False):
        path([(x0 + a, oy + b) for a, b in pts], color=color, dashed=dashed)
        text(x0 + where[0], oy + where[1], label, 15, color)

    # how a Guide card is made: words from the base, overridden by the theme; sub · runs live from the frame
    rel([(764, 36), (800, 36), (800, 126), (764, 126)], "default words", (812, 66))
    rel([(764, 236), (790, 236), (790, 146), (764, 146)], "sub · runs, live", (800, 176))
    rel([(764, 426), (820, 426), (820, 256), (764, 256)], "fills its Spaces", (832, 320))
    rel([(990, 496), (990, 12), (764, 12)], "levels: overrides only\nthe words that differ", (1002, 250))
    # what the theme's files name and cite
    rel([(1184, 512), (1400, 512), (1400, 426), (1476, 426)], "table: names it", (1200, 470))
    rel([(1184, 540), (1440, 540), (1440, 586), (1476, 586)], "roadmap: names them, per level", (1200, 556))
    rel([(1184, 636), (1260, 636), (1260, 746), (1184, 746)], "a step cites\nits cards", (1270, 680))
    rel([(1184, 756), (1300, 756), (1300, 986), (1184, 986)], "a card cites\nits papers", (1310, 860))
    rel([(1184, 1000), (1240, 1000), (1240, 1096), (1184, 1096)], "pdf column", (1250, 1040))
    text(x0 + 420, oy + 80, "? levels.yaml: the base's home for the default words", 14, RED)
    text(x0, oy + 1190, "The same tree in every theme; workbench_guide.py reads each theme's guide/ and related/ "
                        "(the Page Task's own is workbench/task-page/).", 18, INK)
    L.close_frame(fr)
    return fr


GUIDE_VIEWS = ("Description", "Method", "RoadMap Draw", "Related Paper")
# (state, View) -> what the screen shows: [(kind, text)]; kind: h (heading), t (line), m (mono line),
# g (the Spaces-by-level grid), d (a drawing placeholder), s (a step table)
CONTENT = {
    ("today", "Description"): [
        ("h", "<Theme> Workbench"), ("t", "<one paragraph about the old board>"),
        ("h", "Scope Space"), ("t", "<its Views, one line>"), ("h", "Task Space"), ("t", "<one line>"),
        ("h", "Check Space"), ("t", "<one line>"), ("h", "Delivery Space"), ("t", "<one line>")],
    ("today", "Method"): [
        ("m", "▸ Method design (the canvas)"), ("s", "Scope › Questions"),
        ("m", "▸ 2–4 · each step in depth: cards, tests"), ("m", "▸ 5 · why it works")],
    ("today", "RoadMap Draw"): [
        ("m", "▸ Workbench design: the old board's UI drawing"), ("m", "▸ RoadMap: the Workbench Table, drawn"),
        ("m", "▸ Workbench Table (rows in the old Spaces)")],
    ("today", "Related Paper"): [
        ("t", "▸ <N> journals and publishers"), ("h", "<group A>"),
        ("m", "▸ <title> · <author> · <year> · <venue>  ↗"), ("t", "+ N more papers"), ("h", "<group B> …")],
}
LEVELS = ("Block", "Job", "Task")
# Proposed (JL 261007, s31-D05, s31-D06): every View keeps its tab; its body is a header line, then
# three sections, Block · Job · Task, top to bottom, each a heading (no box); its items stack as cards, one
# card shape per View, the same in every theme (a theme gives the words, never the shape):
#   Description    a Space card    <Space>  <what it is at this level>   sub · reads · runs
#   Method         a step card     <N · step>  <what happens>            where · methods · signs
#   RoadMap Draw   a drawing card  <drawing>  <what it shows>            the drawing, embedded ↗
#   Related Paper  a paper card    <title>  <author year · venue>        role · why here · ↗
# The words below are the base's defaults (what the vanilla frame does, frame.py); a theme overrides
# only the words that differ.
HEAD = {"Description": ("<theme> · what this family is for", "<one paragraph: who it serves, what it ends in>"),
        "Method": ("how it asks, plans and answers", "<one paragraph: the method, end to end>"),
        "RoadMap Draw": ("the theme's ladder, cut by level", "<one line: what the drawing shows>"),
        "Related Paper": ("the papers behind the method, by level", "<one line: how they were chosen>")}


def space_cards(level, face, kids, kid_runs, work):
    """The six Space cards of one level: (Space, what it is, sub · reads · runs)."""
    return [
        ("Description", f"the {level}'s face: its title and fields",
         f"sub: —   reads: {face}   runs: Update the description"),
        ("Idea Studio", "one row per studio topic; a click opens its drawing in place",
         "sub: —   reads: studio/sNN-<topic>/   runs: Add a topic · Redraw a topic"),
        ("Audience Report", "one row per Question: Question │ Work │ Report",
         "sub: All · <group>   reads: ## Questions · reports/qNN_<topic>/   runs: Ask a Question · Write the report"),
        ("Work Details", work, f"sub: —   reads: {kids}   runs: {kid_runs}"),
        ("Runs", f"the {level}'s Runs, grouped by type",
         "sub: All · <type>   reads: runs/<run>/run.yaml   runs: Run"),
        ("Delivery", f"what leaves the {level}", "sub: —   reads: delivery/   runs: Build the delivery"),
    ]


LEVEL_CONTENT = {
    ("Description", "Block"): [("t", "one topic: its Questions, its studio/ and reports/"),
                               ("c", space_cards("Block", "board.md", "jNN_<job>/", "Add a Job", "its Jobs")),
                               ("m", "skills   <skill> owns · <skill> works · <skill> shows")],
    ("Description", "Job"): [("t", "one line of work: a group of Tasks toward one end"),
                             ("c", space_cards("Job", "<job>.md", "tNN_<task>/", "Add a Task", "its Tasks")),
                             ("m", "skills   <skill> owns · <skill> works")],
    ("Description", "Task"): [("t", "one folder that is also a Page; it holds the Runs"),
                              ("c", space_cards("Task", "<task>.md", "<its own folders>", "Build the Task",
                                                "how the work is done: its own folders")),
                              ("m", "skills   <skill> owns · <skill> works · <skill> shows")],
    ("Method", "Block"): [("c", [
        ("1 · ask a Question", "raise it in the register; its report folder opens",
         "where: Audience Report   methods: <card> · <card>   signs: <who>"),
        ("2 · draw a topic", "think in the studio; a report cites its frames",
         "where: Idea Studio   methods: <card>   signs: <who>"),
        ("3 · write the report", "the answer and its evidence, one Page per Question",
         "where: Audience Report › Report   methods: <card>   signs: <who>")])],
    ("Method", "Job"): [("c", [
        ("1 · open a Job", "one line of work toward one end", "where: Work Details   methods: <card>   signs: <who>"),
        ("2 · group its Tasks", "each Task one folder, in order", "where: Work Details   methods: <card>   signs: <who>")])],
    ("Method", "Task"): [("c", [
        ("1 · plan", "scope and plan in its face", "where: Description › Plan   methods: <card>   signs: <who>"),
        ("2 · build", "the code and its review", "where: Work Details › Code   methods: <card>   signs: <who>"),
        ("3 · run", "a Run per execution, its Result beside it", "where: Runs   methods: <card>   signs: <who>"),
        ("4 · report", "what the Runs show", "where: Audience Report › Report   methods: <card>   signs: <who>")])],
    # drawing cards (JL 261007: "cards as well, in case there are multiple draw"): one per drawing,
    # closed by default; an open one shows its drawing inside the card, as an Idea Studio row does
    ("RoadMap Draw", "Block"): [("w", [("the ladder · Block layer", "what a Block holds and how it opens its Jobs",
                                        "source: Tools/blueprints/bNN_theme_<theme>/studio/sNN-<topic>/   built by: build_*.py   ↗ full size", True),
                                       ("the Block's screens", "the six Spaces on the Block tab", "source: Tools/blueprints/bNN_theme_<theme>/studio/sNN-<topic>/   built by: build_*.py   ↗ full size", False)])],
    ("RoadMap Draw", "Job"): [("w", [("the ladder · Job layer", "a Job, its Tasks, and where it shows", "source: Tools/blueprints/bNN_theme_<theme>/studio/sNN-<topic>/   built by: build_*.py   ↗ full size", True),
                                     ("the Job's screens", "the six Spaces on the Job tab", "source: Tools/blueprints/bNN_theme_<theme>/studio/sNN-<topic>/   built by: build_*.py   ↗ full size", False)])],
    ("RoadMap Draw", "Task"): [("w", [("the ladder · Task layer", "a Task, its Runs, and their Results", "source: Tools/blueprints/bNN_theme_<theme>/studio/sNN-<topic>/   built by: build_*.py   ↗ full size", True),
                                      ("a Run's life", "type → Spec → folder → passes → close", "source: Tools/blueprints/bNN_theme_<theme>/studio/sNN-<topic>/   built by: build_*.py   ↗ full size", False),
                                      ("the Task's screens", "the six Spaces on the Task tab", "source: Tools/blueprints/bNN_theme_<theme>/studio/sNN-<topic>/   built by: build_*.py   ↗ full size", False)])],
    ("Related Paper", "Block"): [("c", [
        ("<title>", "<author> <year> · <venue>", "role: classic   why here: <one line>   ↗ pdf · doi"),
        ("<title>", "<author> <year> · <venue>", "role: method   why here: <one line>   ↗ doi")])],
    ("Related Paper", "Job"): [("c", [
        ("<title>", "<author> <year> · <venue>", "role: evidence   why here: <one line>   ↗ doi")]),
                               ("t", "(a level with no paper yet says so)")],
    ("Related Paper", "Task"): [("c", [
        ("<title>", "<author> <year> · <venue>", "role: method   why here: <one line>   ↗ pdf · doi"),
        ("<title>", "<author> <year> · <venue>", "role: evidence   why here: <one line>   ↗ doi")])],
}
PANEL = {"proposed": ["Add a method", "Add a paper"], "today": ["Add a paper", "+ New Run"]}
# (state, View) -> on disk: (tree line, what on screen it feeds)
ON_DISK = {
    "Description": [
        ("servers/workbench/guide/levels.yaml", "the base: every Space card's words (proposed)"),
        ("servers/workbench-<theme>/", ""),
        ("├── <theme>_theme.py", "each card's sub · runs, read live (proposed)"),
        ("└── guide/guide.yaml", "the paragraph · skills · boundary"),
        ("    levels: Block · Job · Task", "only the card words that differ (proposed)"),
        ("skills/2_theme/<theme>/<skill>/SKILL.md", "each skill in the skills line")],
    "Method": [
        ("servers/workbench-<theme>/", ""),
        ("├── guide/", ""),
        ("│   ├── method.md", "the steps table; its 'where' column"),
        ("│   │   ## Block · ## Job · ## Task", "one steps table per section (proposed)"),
        ("│   ├── methods/<card>.md", "one card; ↗ opens it"),
        ("│   └── methods.excalidraw", "the canvas; ↗ full size"),
        ("└── related/papers.md", "a card's papers")],
    "RoadMap Draw": [
        ("servers/workbench-<theme>/guide/guide.yaml", "explain: which drawing"),
        ("    roadmap: Block · Job · Task", "a list of drawings per level, one card each (proposed)"),
        ("Tools/blueprints/bNN_theme_<theme>/studio/", ""),
        ("├── s01-<theme>-ladder/", "the drawing; one frame per level (proposed)"),
        ("└── s02-<theme>-workbench/", "the drawing (today: the old board)"),
        ("skills/…/workbench-<theme>/ref/workbench-table.md", "the Workbench Table and its drawing")],
    "Related Paper": [
        ("servers/workbench-<theme>/related/", ""),
        ("├── papers.md", "one row per paper: group · role · key ·"),
        ("│", "  venue · doi · why here · pdf"),
        ("│", "  + level: Block · Job · Task (proposed)"),
        ("└── papers/<key>.pdf", "the pdf ↗ (open-licensed only)")],
}
POPOUTS = [   # the windows a ↗ in the Guide opens
    ("By <method>  ·  a method card", ["What it does", "  <two lines>", "Where", "  step <n> · Work Details › <sub>",
                                       "Tested", "  N studies: <author><year> ↗ · <author><year> ↗"]),
    ("the methods canvas  ·  full size", ["[ guide/methods.excalidraw ]", "  view only here; edit it in its design Block"]),
    ("<author><year>  ·  the paper", ["[ related/papers/<key>.pdf ]", "  why here: <one line>   ·   doi ↗"]),
]


PH = [SH]                       # a proposed screen's height: its tallest View's content (measured)


def screen_h(state):
    return PH[0] if state == "proposed" else SH


def measure_proposed():
    """Lay out every proposed View once, keep the tallest, then drop what was drawn."""
    mark = len(L.els)
    PH[0] = max(SH, max(content_bottom(0, 0, v) for v in GUIDE_VIEWS) + 80)
    del L.els[mark:]


def content_bottom(x, y, view):
    cx, cy, cw = x + 24, y + 136 + 80, SW - RW - 48
    for lvl in LEVELS:
        cy = draw_items(cx - 10, cy + 52, cw + 20, LEVEL_CONTENT[(view, lvl)], lvl) + 24
    return cy - y


FOLDED_LINE = {  # what a folded level heading still says
    "Description": "6 Spaces · skills · folders",
    "Method": "N steps · N method cards",
    "RoadMap Draw": "N drawings",
    "Related Paper": "N papers",
}


def guide_screen(x, y, state, view, folded=()):
    """One workbench screen with the Guide tab open: the level tabs, the four Views, the content, the panel."""
    SH = screen_h(state)
    L.base("rectangle", x, y, SW, SH, INK, 1.5)
    tx = x + 24
    for tab in ["Guide", "Block", "Job ▾", "Task ▾"]:
        L.text(tx, y + 18, tab, 20, INK if tab == "Guide" else GRAY)
        if tab == "Guide":
            path([(tx, y + 48), (tx + len(tab) * 11, y + 48)], arrow=False, color=INK)
        tx += len(tab) * 11 + 46
    sx = x + 24
    for v in GUIDE_VIEWS:
        w = len(v) * 10 + 24
        if v == view:
            base("rectangle", sx - 8, y + 62, w, 36, INK, 1.5, rough=0)
        L.text(sx, y + 70, v, 18, INK if v == view else GRAY)
        sx += w + 14
    path([(x, y + 112), (x + SW, y + 112)], arrow=False, color=GRAY)
    path([(x + SW - RW, y + 112), (x + SW - RW, y + SH)], arrow=False, color=GRAY)
    rx = x + SW - RW + 20
    L.text(rx, y + 132, "Run types · Guide", 20)
    for i, r in enumerate(PANEL[state]):
        base("rectangle", rx, y + 176 + i * 54, RW - 40, 40, GRAY, 1, rough=0)
        L.text(rx + 12, y + 184 + i * 54, r, 17)
    L.text(rx, y + 176 + len(PANEL[state]) * 54 + 16, "recent: run-<type>-<target>\nclosed · p01", 15, GRAY, MONO)
    L.text(x + 24, y + SH - 40, "the family's docs (Tools), the same in every Block", 16, GRAY)
    cx, cy, cw = x + 24, y + 136, SW - RW - 48
    if state == "proposed":
        head, line = HEAD[view]
        L.text(cx, cy, head, 19, INK)
        L.text(cx + 10, cy + 34, line, 16, GRAY)
        cy += 80
        for lvl in LEVELS:              # one section per level: a fold, its cards under it, no box (JL 261007)
            if lvl in folded:           # folded: the heading and one line of what it holds
                L.text(cx, cy + 12, f"▸ {lvl}", 22, INK)
                L.text(cx + 120, cy + 16, FOLDED_LINE[view], 15, GRAY)
                cy += 60
                continue
            L.text(cx, cy + 12, f"▾ {lvl}", 22, INK)
            cy = draw_items(cx - 10, cy + 52, cw + 20, LEVEL_CONTENT[(view, lvl)], lvl) + 24
        return
    draw_items(cx, cy, cw, CONTENT[(state, view)])


def draw_items(cx, cy, cw, items, lvl=""):
    """Draw a View's lines from the top-left (cx, cy); returns where the next line goes."""
    for kind, s in items:
        if kind == "h":
            L.text(cx, cy, s, 19, INK); cy += 36
        elif kind == "t":
            L.text(cx + 10, cy, s, 16, GRAY); cy += 30
        elif kind == "m":
            L.text(cx + 10, cy, s, 16, INK, MONO); cy += 30
        elif kind == "d":
            base("rectangle", cx + 10, cy, cw - 20, 200, GRAY, 1, dashed=True, rough=0)
            L.text(cx + 30, cy + 90, s, 16, GRAY); cy += 216
        elif kind == "c":                                   # cards, stacked top to bottom
            for title, desc, line in s:
                base("rectangle", cx + 10, cy, cw - 20, 66, GRAY, 1, rough=0)
                L.text(cx + 26, cy + 10, title, 17, INK)
                L.text(cx + 26 + len(title) * 9.5 + 24, cy + 12, desc, 15, GRAY)
                L.text(cx + 26, cy + 38, line, 13, INK, MONO)
                cy += 76
        elif kind == "w":                                   # drawing cards: title, what it shows, the drawing
            for title, desc, line, opened in s:             # a card per drawing; open, it holds the drawing
                h = 66 + (190 if opened else 0)
                base("rectangle", cx + 10, cy, cw - 20, h, GRAY, 1, rough=0)
                head = ("▾ " if opened else "▸ ") + title
                L.text(cx + 26, cy + 10, head, 17, INK)
                L.text(cx + 26 + len(head) * 9.5 + 24, cy + 12, desc, 15, GRAY)
                L.text(cx + 26, cy + 38, line, 13, INK, MONO)
                if opened:                                  # the canvas fills the card: no box inside it
                    path([(cx + 26, cy + 66), (cx + cw - 26, cy + 66)], arrow=False, color=GRAY, dashed=True)
                    L.text(cx + 46, cy + 150, "[ the drawing, embedded, view only ]", 15, GRAY)
                cy += h + 10
        elif kind == "r":                                   # one level's row of the six Spaces
            w = (cw - 20) / 6
            for i, sp in enumerate(SIX):
                L.text(cx + 10 + i * w, cy, sp, 13, INK)
                base("rectangle", cx + 10 + i * w, cy + 22, w - 8, 28, GRAY, 1, rough=0)
                L.text(cx + 18 + i * w, cy + 28, "<sub> · <sub>", 12, GRAY, MONO)
            cy += 66
        elif kind == "g":                                   # Block · Job · Task × the six Spaces
            gx, w = cx + 90, (cw - 100) / 6
            for i, sp in enumerate(SIX):
                L.text(gx + i * w, cy, sp, 13, INK)
            for r, lvl in enumerate(("Block", "Job", "Task")):
                ry = cy + 24 + r * 34
                L.text(cx + 10, ry + 6, lvl, 15)
                for i in range(6):
                    base("rectangle", gx + i * w, ry, w - 8, 28, GRAY, 1, rough=0)
                    L.text(gx + i * w + 8, ry + 6, "<sub> · <sub>", 12, GRAY, MONO)
            cy += 24 + 3 * 34 + 16
        elif kind == "s":                                   # the steps table; s: the 'where' of each row
            rows = s if isinstance(s, tuple) else (s, s, s)
            cols = (0, 60, 300, 520, 820)
            for c, h in zip(cols, ("step", "what happens", "methods", "where in the workbench", "who signs")):
                L.text(cx + 10 + c, cy, h, 14, GRAY)
            path([(cx + 10, cy + 24), (cx + cw - 10, cy + 24)], arrow=False, color=GRAY)
            for r, where in enumerate(rows):
                does, _, space = where.partition(" › ") if " › " in where else ("<does>", "", where)
                for c, v in zip(cols, (f"{r + 1}", does, "<card> · <card>", space, "<who>")):
                    L.text(cx + 10 + c, cy + 34 + r * 28, v, 14, INK, MONO)
            cy += 34 + len(rows) * 28 + 16
    return cy


def on_disk(x, y, view, state):
    L.text(x, y, "on disk", 22)
    for i, (line, meaning) in enumerate(ON_DISK[view]):
        old = (state == "proposed" and "today" in meaning) or (state == "today" and "proposed" in meaning)
        L.text(x, y + 44 + i * 28, line, 16, GRAY if old else INK, MONO)
        if meaning:
            L.text(x + 620, y + 45 + i * 28, meaning, 15, GRAY)


def frame_screens(x0, y, state, name, title, note):
    fr = L.open_frame(name)
    text(x0, y, title, 34)
    text(x0, y + 50, note, 20, GRAY)
    for i, view in enumerate(GUIDE_VIEWS):
        x = x0 + i * (SW + 120)
        text(x, y + 110, f"Guide › {view}", 24)
        guide_screen(x, y + 150, state, view)
        on_disk(x, y + 150 + screen_h(state) + 50, view, state)
    if state == "proposed":
        x = x0 + 4 * (SW + 120)
        text(x, y + 110, "Guide › Description, from the Block tab: Job and Task folded", 24)
        guide_screen(x, y + 150, state, "Description", folded=("Job", "Task"))
        text(x, y + 150 + screen_h(state) + 50, "each level heading folds (▾ open · ▸ folded); a click toggles it;\n"
             "the tab you came from opens its level, the other two start folded (proposed)", 16, GRAY)
        px, py = x0 + 5 * (SW + 120), y + 150
        text(px, py - 40, "pop-out, from any View's ↗", 24)
        for t, lines in POPOUTS:
            h = 72 + sum(168 if l.startswith("[") else 28 for l in lines) + 20
            UI.window(px, py, UI.PW, h, t, lines)
            py += h + 40
    L.close_frame(fr)
    return fr


def _abs(v):
    p = Path(str(v))
    return p if p.is_absolute() else (TOOLS / p if (TOOLS / p).exists() else TOOLS.parent / p)


def _has(path, pattern):
    try:
        return bool(re.search(pattern, Path(path).read_text(encoding="utf-8")))
    except OSError:
        return False


def _all_levels(path):
    """method.md has a step table per level: a heading naming each level, as the Guide's parser reads
    it (workbench_guide.level_steps: `## Task …`, a whole bold line `**Job · …**`, or an underlined line)."""
    return all(_has(path, rf"(?m)^(?:#+\s*{lvl}\b.*|\*\*{lvl}\b[^*]*\*\*|{lvl}\b.*\n-{{3,}})$") for lvl in LEVELS)


def _level_column(papers):
    """papers.md's table has a `level` column: its header row (the first table line) names it."""
    head = next((l for l in papers.read_text(encoding="utf-8").splitlines() if l.startswith("|")), "")
    return any(c.strip().lower() == "level" for c in head.split("|"))


def status_rows():
    """One row per family: what its Guide has today of the card Guide (s31-D05 to D08)."""
    themes = {p.parent.name: p.name for p in SERVERS.glob("workbench-*/*_theme.py")}
    for fam, e in G.FAMILIES.items():
        home = _abs(e.get("guide_home") or "").resolve()
        folder = home.parent.relative_to(SERVERS.resolve()).as_posix() if home.name == "guide" else "?"
        theme = themes.get(folder, "not yet") if folder.startswith("workbench-") else "the base"
        name = folder.split("-", 1)[1] if folder.startswith("workbench-") else ""
        key = fam if not name or fam == name else f"{fam} → {name}?"
        yaml = home / "guide.yaml"
        levels = "yes" if _has(yaml, r"(?m)^levels:") else "not yet"
        roadmap = "yes" if _has(yaml, r"(?m)^roadmap:") else "not yet"
        md = e.get("method_doc")
        method = ("—" if not md or not _abs(md).is_file() else "yes" if _all_levels(_abs(md)) else "not yet")
        where = "—"
        if md and _abs(md).is_file():
            spaces = {w.split("›")[0].strip() for line in _abs(md).read_text(encoding="utf-8").splitlines()
                      if line.startswith("|") for w in line.split("|") if "›" in w}
            bad = sorted(sp for sp in spaces if sp and sp not in SIX)
            where = "frame" if spaces and not bad else ("old: " + " · ".join(bad[:3]) if bad else "—")
        papers = home.parent / "related" / "papers.md"
        plevel = "—" if not papers.is_file() else ("yes" if _level_column(papers) else "not yet")
        yield key, folder, theme, levels, method, where, roadmap, plevel

def frame_status(x0, y0):
    fr = L.open_frame("6 · status")
    text(x0, y0, "Status: what each family's Guide has of the card Guide, read off the code", 34)
    text(x0, y0 + 50, "a column per part the cards need (s31-D05 to D08); red = not yet. Rebuilt from the code, "
                      "so it fills in as each theme moves.", 20, GRAY)
    cols = (0, 230, 560, 790, 980, 1200, 1620, 1820)
    y = y0 + 110
    for x, h in zip(cols, ("family", "folder", "theme file", "levels:", "method.md\nby level",
                           "Method 'where'", "roadmap:", "papers.md\nlevel")):
        text(x0 + x, y, h, 18)
    y += 22
    path([(x0, y + 32), (x0 + 2000, y + 32)], arrow=False, color=INK)
    for k, row in enumerate(status_rows()):
        for x, c in zip(cols, row):
            text(x0 + x, y + 46 + k * 30, str(c), 15,
                 RED if str(c).startswith(("old", "not yet")) or "?" in str(c) else INK, MONO)
    L.close_frame(fr)
    return fr


def frame_questions(x0, y0):
    fr = L.open_frame("Questions")
    text(x0, y0, "Questions", 30)
    for i, q in enumerate(QUESTIONS):
        text(x0, y0 + 60 + i * 40, q, 18, RED)
    L.close_frame(fr)
    return fr


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s31-guide.excalidraw"
    L.els.clear()
    L.FRAME[0] = None
    measure_proposed()
    a = frame_compare(0)
    b = frame_flow(a["x"] + a["width"] + 300, 0)
    c = frame_screens(0, max(a["y"] + a["height"], b["y"] + b["height"]) + 300, "proposed",
                      "3 · Guide on screen", "Guide at every View",
                      "one screen per View, each split in three sections: Block · Job · Task (JL 261007); "
                      "on disk under each, what feeds it. The same in every Block.")
    d = frame_screens(0, c["y"] + c["height"] + 300, "today", "4 · Guide today", "Guide today",
                      "as the server renders it now (the work family, in placeholders): its words describe the old board.")
    q = frame_questions(0, d["y"] + d["height"] + 300)
    t = frame_tree(q["x"] + q["width"] + 300, q["y"])
    frame_status(t["x"] + t["width"] + 300, q["y"])
    canvas.write(out, list(L.els), "build_s31_guide.py")


if __name__ == "__main__":
    main()
