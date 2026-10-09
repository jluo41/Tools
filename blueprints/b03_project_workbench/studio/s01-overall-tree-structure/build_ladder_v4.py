"""b03 ladder: s01-overall-tree-structure/s01-overall-tree-structure.excalidraw, frame 1 only
(frames 2-7 removed, JL 261007): each layer with its specials and its variants.

The variant trees below are defined here and drawn by s11-s13 and the theme Blocks' ladders, each into its own drawing.

One tree from Space down to Run, each layer one step down and to the right (JL 261006):

    <layer node> ──── special ── what it is            specials branch to the right, each described;
        │        ──── special Job ──▶ <child>/         the same level shares a column: a special Job sits
                                                       in the Job column, its child in the Task column;
                                                       studio/ and reports/ are special Jobs: each has
    [ definition │                    its tree         its own definition box, its child folder with a
      variants   │                                     file tree, and empty room to write
      room ]     │
        └─▶ <next layer node> ...           the last special, green, holds the next layer: a
                                            green arrow drops from it into the next node

Tools/ sits at the far right; its skills column, one box per layer, points right to left into
each layer's heading (SKILLS). Generic placeholders, no project content; "?" items are red.
A draft for the person to rearrange; canvas.write keeps whatever they move or add.

    python build_ladder_v4.py [out.excalidraw]
"""
import random
import re
import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_build"))   # shared studio helpers
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))  # canvas (haipipe-studio)
import canvas  # noqa: E402
import run_names  # noqa: E402  (each button's Run name, read off the server code)

random.seed(261008)
SANS, MONO = 6, 3
# the studio look (haipipe-studio, JL 261007 "Recolour all"): black, red = an open question, green = a change.
# GRAY, BLUE and TEAL keep their names for the builders that import them, all black now; "holds the next
# layer" is a bold black line, no longer green
INK, RED, GREEN = "#1e1e1e", "#e03131", "#2f9e44"
GRAY = BLUE = TEAL = INK
els = []
FRAME = [None]                  # elements drawn while a frame is open belong to it


def sp(name, desc, kids=None, job=None, holds=False):
    """A special: a plain file or folder (desc), one with children (kids), a special Job (job), or the
    one that holds the next layer (holds: green, with a green arrow down into the next node)."""
    return {"name": name, "desc": desc, "kids": kids or [], "job": job, "holds": holds}


LAYERS = [  # (layer, node, [specials], [variants])
    ("Space", "<space>/", [
        sp("code/", "shared library: its own submodule, on PYTHONPATH",
           kids=["haipipe/ hainn/ haiutils/   edit", "haifn/   generated, never edit", "scripts/   CLIs, builders"]),
        sp("_WorkSpace/", "data stores, outside git"),
        sp("examples*/", "holds the Projects", holds=True)], []),
    ("Project", "<Project>/", [
        sp("README.md", "human entry: mission, entry points"),
        sp("project.yaml", "id · profile · git_mode · state · mission"),
        sp("platforms/", "freestyle: owned code repos, no ladder"),
        sp("external/", "freestyle: pinned upstream, read-only"),
        sp("work/ discovery/ …", "holds the Themes, each singular, made on first use", holds=True)],
     ["research", "software", "hybrid"]),
    ("Theme", "<theme>/", [sp("_old/", "archived Blocks"), sp("bNN_<topic>/ …", "holds its Blocks", holds=True)],
     ["work", "discovery", "cowork", "paper", "insight", "design", "labeling"]),
    ("Block", "bNN_<topic>/", [
        sp("bNN_<topic>.md", "its face (was board.md), on screen Description: kind · spine · close · Questions"),
        sp("studio/", "", job={
            "define": "special Job, on screen the Idea Studio: the team's room, one folder per topic",
            "node": "sNN-<topic>/", "node_define": "one discussion topic: draw, script, chat",
            "tree": [("├── sNN-<topic>.md", "what is decided so far"),
                     ("├── <drawing>.excalidraw", "the scratch; your marks kept"),
                     ("├── build_<drawing>.py", "seeds the drawing (optional)"),
                     ("└── chat/", "Claude Code · Codex sessions, one file each")]}),
        sp("reports/", "", job={
            "define": "special Job, on screen the Audience Report: the audience's Questions, one folder each",
            "node": "qNN_<topic>/", "node_define": "one Question = a light Page",
            "tree": [("├── qNN_<topic>.md", "Answer · Evidence · Limits · Next"),
                     ("├── qNN_<topic>.excalidraw", "its one drawing"),
                     ("├── draft/", "free notes, the discussion"),
                     ("└── page.toml", "lets the workbench show it")]}),
        sp("related/", "on screen Description › Related: one table of related work, any kind (paper · repo · dataset · tool · project)"),
        sp("delivery/", "optional, on screen Delivery: what the Block hands out (exports, built reports)"),
        sp("runs/", "", job={
            "define": "its soft Runs, one folder each: run-<type>-<target>/ writes into one item above; "
                      "no hard Run, no evidence; on screen the Runs Space",
            "node": "README.md", "node_define": "the run types it has: tools write it, never by hand",
            "tree": [("run-question-<qNN>", "→ the face's Questions · haipipe-question-asking"),
                     ("run-draw-<sNN>", "→ studio/sNN-<topic>/ · workbench-studio"),
                     ("run-report-<qNN>", "→ reports/qNN_<topic>/ · haipipe-page-writing"),
                     ("run-check-<qNN>", "→ a verdict on reports/qNN · haipipe-page-check"),
                     ("run-delivery-<dNN>", "→ delivery/dNN-<…>/ · haipipe-page-delivery"),
                     ("each type: its Runs", "name · state · last pass, read from run.yaml")]}),
        sp("jNN_<job>/ …", "holds its work Jobs; on screen Work Details", holds=True)],
     ["work Block", "discovery Block", "cowork Block", "paper Board", "insight Block (DIKW)",
      "insight register board", "design Board", "labeling Block"]),
    ("Job", "jNN_<job>/", [
        sp("jNN_<job>.md", "its face: goal · state · next · task_groups"),
        sp("studio/", "optional: its drawings"),
        sp("reports/", "optional: its own Questions"),
        sp("src/", "code shared by its Tasks: marks a Job"),
        sp("sbatch/", "batch shared by its Tasks: marks a Job"),
        sp("delivery/", "optional: the Job's output"),
        sp("runs/", "", job={
            "define": "its soft Runs: plan, launch and review its Tasks; no evidence here",
            "node": "README.md", "node_define": "the run types it has: tools write it, never by hand",
            "tree": [("run-plan-tasks", "→ the face's task_groups · new tNN_ · haipipe-task-plan"),
                     ("run-launch-<group> ?", "→ sbatch/: its Tasks' hard Runs · haipipe-task-run ?"),
                     ("run-review-job", "→ the face: state · next · haipipe-task-review"),
                     ("run-draw-, -report-, …", "→ its optional studio/ · reports/ · delivery/")]}),
        sp("tNN_<task>/ …", "holds its Tasks", holds=True)],
     ["work Job", "discovery Job", "Page Job", "paper version", "cowork Job", "DIKW level", "design method",
      "labeling Job: one dataset, one label"]),
    ("Task", "tNN_<task>/", [
        sp("tNN_<task>.md", "its face: a Task is known by its name (tNN_…)"),
        sp("studio/", "optional: its drawings · chat/"),
        sp("reports/", "optional: its Page is usually its report"),
        sp("scripts/", "work Task: its worker code"),
        sp("delivery/", "builds: web · latex · word · slide"),
        sp("runs/", "holds its Runs, one folder each: hard and soft · README.md: its run types",
           holds=True)],
     ["work Task", "Page Task (a paper Section is one)", "discovery Task", "insight question", "design folder",
      "labeling Task"]),
    ("Run", "runs/<run>/", [
        sp("run.yaml", "the card: kind · type · scope · target · status · passes"),
        sp("ticket", "hard: rNN_<slug>.sh (runnable) · soft: run-<type>-<target>.md"),
        sp("config.yaml", "hard only: its frozen inputs"),
        sp("result/", "hard only: generated; heavy files → <ProjectResult>/…"),
        sp("passes/pNN-<MMDD>/", "the history: a rerun, or one more round on the target"),
        sp("where it lives", "hard: a work Task only · soft: any level · a Page: soft only")],
     ["hard: stays inside; evidence", "  work · discovery · insight · labeling",
      "soft: writes into its level", "  write · display · value · cite · build · draw",
      "a Page reads hard Results only"]),
]
DEFINE = {
    "Space": "the whole workspace: every Project, the shared code and the tools",
    "Project": "one research or software boundary",
    "Theme": "one kind of work, owned by one skill family",
    "Block": "one topic: a board, its Questions and its Jobs",
    "Job": "one line of work: Tasks that share one goal",
    "Task": "one bounded piece of work = a Page folder; dry (code on data) or wet (a procedure run by a person)",
    "Run": "one job in one folder; hard (makes evidence) or soft (writes into its level); many passes",
}
ON_SCREEN = {  # Level = the tab; its Spaces = the row below it (dashed = optional)
    "Block": "Block level · Spaces: Description · Idea Studio · Audience Report | Work Details | Runs · Delivery",
    "Job": "Job level, picked in Block › Work Details · Spaces: the same six as the Block",
    "Task": "Task level, picked in Job › Work Details · Spaces: the same six as the Block",
    "Run": "a row in its level's Runs view; opens a pop-out"}
SKILLS = {  # Tools/ at the far right; one skills box per layer, read right to left
    "Space": ["servers/space-home  (SPACE Home)", "workbench"],
    "Project": ["haipipe-project"],
    "Theme": ["haipipe-task", "haipipe-discovery", "haipipe-cowork", "haipipe-paper",
              "haipipe-insight", "haipipe-design", "haipipe-labeling"],
    "Block": ["haipipe-<family>  (owns bNN_<topic>.md)", "haipipe-question", "workbench-<family>",
              "excalidraw-report  (studio/)"],
    "Job": ["haipipe-task", "haipipe-cowork", "? one Job skill per Theme"],
    "Task": ["haipipe-task", "haipipe-page", "haipipe-page-workflow", "haipipe-discovery-inquiry"],
    "Run": ["haipipe-run  (hard and soft)", "haipipe-workflow"],
}
DX, NODE_W, NODE_H, SP_W, SP_H = 640, 320, 56, 240, 42
SP_GAP, KID_W, ROOM, LAYER_GAP = 40, 360, 110, 220          # wide spacing: room to scratch
SK_X, SK_W, TOOLS_X = 5600, 420, 6240                       # skills column and Tools/, far right
HOLD_X = 200                    # the green arrow drops from here in the holds box, clear of the headings
HOLDS = []                      # where the last layer's green arrow starts


# ── drawing helpers ──────────────────────────────────────────────────────────────────────────
def base(kind, x, y, w, h, stroke=INK, sw=1, dashed=False, rough=1):
    e = {"id": f"v{len(els)}", "type": kind, "x": x, "y": y, "width": w, "height": h, "angle": 0,
         "strokeColor": stroke, "backgroundColor": "transparent", "fillStyle": "solid", "strokeWidth": sw,
         "strokeStyle": "dashed" if dashed else "solid", "roughness": rough, "opacity": 100, "groupIds": [],
         "frameId": FRAME[0], "roundness": {"type": 3} if kind == "rectangle" else None,
         "seed": random.randint(1, 2**31 - 1), "version": 1, "versionNonce": random.randint(1, 2**31 - 1),
         "isDeleted": False, "boundElements": [], "updated": 1, "link": None, "locked": False}
    els.append(e)
    return e


def text(x, y, s, size=16, color=INK, font=SANS, link=None):
    lines = s.split("\n")
    e = base("text", x, y, max(len(l) for l in lines) * size * (0.6 if font == MONO else 0.55),
             len(lines) * size * 1.25, color, rough=0)
    e.update(text=s, originalText=s, fontSize=size, fontFamily=font, textAlign="left", verticalAlign="top",
             containerId=None, autoResize=True, lineHeight=1.25, link=link)


def path(pts, arrow=True, color=GRAY, dashed=False):
    x0, y0 = pts[0]
    rel = [[px - x0, py - y0] for px, py in pts]
    e = base("arrow" if arrow else "line", x0, y0, max(abs(a) for a, _ in rel) or 1,
             max(abs(b) for _, b in rel) or 1, color, 1.5, dashed)
    e.update(points=rel, lastCommittedPoint=None, startBinding=None, endBinding=None, startArrowhead=None,
             endArrowhead="arrow" if arrow else None)


def box(x, y, w, h, label, size=18, color=INK):
    base("rectangle", x, y, w, h, color, 1.5)
    text(x + 16, y + (h - size * 1.25) / 2, label, size, color, MONO)


def def_box(x, y, w, sections):
    """A gray box of labelled sections [(label, [lines])], then empty room to write; returns its bottom."""
    h = 14 + sum(20 + len(lines) * 21 + 12 for _, lines in sections) + ROOM
    base("rectangle", x, y, w, h, GRAY, 1)
    cy = y + 14
    for label, lines in sections:
        text(x + 16, cy, label, 13, GRAY)
        for k, ln in enumerate(lines):
            text(x + 16, cy + 20 + k * 21, ln, 15, RED if ln.startswith("?") else INK)
        cy += 20 + len(lines) * 21 + 12
    return y + h


def open_frame(name):
    """Start a frame; everything drawn until close_frame belongs to it and moves with it."""
    FRAME[0] = None
    fr = base("frame", 0, 0, 10, 10, GRAY, rough=0)
    fr["name"], fr["roundness"] = name, None          # a frame keeps its key name: other Blocks find frames by it
    FRAME[0] = fr["id"]
    return fr


def close_frame(fr, pad=80):
    """Fit the frame around its children; returns its bottom."""
    xs, ys = [], []
    for e in els:
        if e.get("frameId") != fr["id"]:
            continue
        if e.get("points"):                            # lines and arrows: measure their real points
            xs += [e["x"] + px for px, _ in e["points"]]
            ys += [e["y"] + py for _, py in e["points"]]
        else:
            xs += [e["x"], e["x"] + e["width"]]
            ys += [e["y"], e["y"] + e["height"]]
    x0, y0, x1, y1 = min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad
    fr.update(x=x0, y=y0, width=x1 - x0, height=y1 - y0)
    FRAME[0] = None
    return y1


# ── one special, drawn from its box at (sx, sy); returns its bottom ─────────────────────────────
def draw_special(s, sx, sy, child_x=None):
    """child_x: for a special Job, the x of the column one level down (its child sits there)."""
    color = RED if s["name"].endswith("?") else INK
    box(sx, sy, SP_W, SP_H, s["name"], 15, color)
    if s["holds"]:                                     # the one that holds the next layer: a bold box
        els[-2]["strokeWidth"] = 3
    if s["holds"]:
        HOLDS.append((sx + HOLD_X, sy + SP_H))
    bottom = sy + SP_H
    cx = child_x
    if s["kids"]:                                      # a folder with children: stacked to its right
        for j, kid in enumerate(s["kids"]):
            ky = sy + j * (SP_H + 12)
            path([(sx + SP_W + 6, sy + SP_H / 2), (sx + SP_W + 70, sy + SP_H / 2),
                  (sx + SP_W + 70, ky + SP_H / 2), (cx - 8, ky + SP_H / 2)])
            box(cx, ky, KID_W, SP_H, kid, 15, GRAY if "generated" in kid else INK)
        if any("generated" in k for k in s["kids"]):
            text(cx + KID_W + 20, sy + SP_H + 16, "written by builders in a Task's scripts/;\n"
                 "change the builder, then rebuild", 14, GRAY)
        text(sx, sy + SP_H + 8, s["desc"], 14, GRAY)
        bottom = max(sy + SP_H + 30, sy + len(s["kids"]) * (SP_H + 12))
    elif s["job"]:                                     # a special Job: definition box, then its child
        j = s["job"]
        db = def_box(sx, sy + SP_H + 14, SP_W + 60, [("definition", textwrap.wrap(j["define"], 36))])
        path([(sx + SP_W + 6, sy + SP_H / 2), (cx - 8, sy + SP_H / 2)])
        box(cx, sy, KID_W, SP_H, j["node"], 15)
        text(cx, sy + SP_H + 10, j["node_define"], 14, GRAY)
        ty = sy + SP_H + 38
        for line, meaning in j["tree"]:
            text(cx, ty, line, 15, INK, MONO)
            text(cx + 270, ty + 1, meaning, 14, RED if line.endswith("?") else GRAY)
            ty += 24
        bottom = max(db, ty + ROOM)
    else:                                              # a plain file or folder: described beside it
        text(sx + SP_W + 18, sy + 12, s["desc"], 14, GRAY)
    return bottom


def draw():
    draw_ladder("1 · The ladder", "The ladder: each layer, its specials, its variants",
                "A layer's node keeps its folder pattern; its specials branch to the right, each described; "
                "studio/ and reports/ are special Jobs; the box under a node holds its definition and variants; "
                "the next layer steps down and right. Red = open.", LAYERS, DEFINE, ON_SCREEN, SKILLS)


def draw_ladder(name, title, subtitle, layers, define, shown, owners, y0=0, shown_label="on screen",
                top=("Tools/", "skills, agents, servers")):
    """One ladder, drawn as s01's frame 1: a node per layer, one step down and right; its specials branch
    right; a box under each node (definition, what shows, variants); the owners in a column far right.
    Returns the frame."""
    ladder = open_frame(name)
    text(0, y0, title, 40)
    text(0, y0 + 58, subtitle, 18, GRAY)
    y, prev, tools = y0 + 170, None, None
    for i, (layer, node, specials, variants) in enumerate(layers):
        x = i * DX
        text(x, y, layer, 24)
        ny = y + 38
        box(x, ny, NODE_W, NODE_H, node)
        mid = ny + NODE_H / 2
        if HOLDS:                                      # the bold link: where this layer comes from
            hx, hy = HOLDS.pop()
            path([(hx, hy + 6), (hx, ny - 8)], color=INK)
            els[-1]["strokeWidth"] = 3
        if prev:                                       # from the layer above: down its left side, then right
            px, pmid = prev
            path([(px - 6, pmid), (px - 40, pmid), (px - 40, mid), (x - 8, mid)])
        # specials: the first one level with the node, each on its own branch from the node's middle
        # a special Job is one level down, so it sits in the next layer's column, and its child one
        # further, in the column after: the same level shares a column (JL 261006)
        # one column grid, top to bottom (上下对齐): a layer's node in column i, its specials in
        # column i+1 (above the next layer's node), anything one level further in column i+2
        sx, sy = (i + 1) * DX, ny + (NODE_H - SP_H) / 2
        bottom = ny + NODE_H
        for s in specials:
            path([(x + NODE_W + 6, mid), (x + NODE_W + 160, mid), (x + NODE_W + 160, sy + SP_H / 2),
                  (sx - 8, sy + SP_H / 2)], arrow=False)
            sb = draw_special(s, sx, sy, child_x=(i + 2) * DX)
            bottom = max(bottom, sb)
            sy = sb + SP_GAP
        # the box under the node: its definition, its variants, room to write
        sections = [("definition", textwrap.wrap(define[layer], 34))]
        if layer in shown:
            sections.append((shown_label, textwrap.wrap(shown[layer], 34)))
        if variants:
            sections.append(("variants", variants))
        bottom = max(bottom, def_box(x, ny + NODE_H + 24, NODE_W, sections))
        # Tools/ (a special of the Space) at the far right, and this layer's skills to its left
        if i == 0:
            box(TOOLS_X, ny, SP_W, SP_H, top[0], 15)
            text(TOOLS_X, ny - 30, top[1], 14, GRAY)
            path([(x + NODE_W / 2, ny - 6), (x + NODE_W / 2, y0 + 140), (TOOLS_X + SP_W / 2, y0 + 140),
                  (TOOLS_X + SP_W / 2, ny - 6)], arrow=False, dashed=True)
            tools = ny + SP_H / 2
        names = owners.get(layer, [])
        if names:
            sky = y if i else bottom + 20                 # the Space: below everything in its row
            sh = 24 + len(names) * 22
            base("rectangle", SK_X, sky, SK_W, sh, INK, 1.5)
            for k, n in enumerate(names):
                text(SK_X + 16, sky + 12 + k * 22, n, 15, RED if n.startswith("?") else INK, MONO)
            trunk = SK_X + SK_W + 50
            path([(TOOLS_X - 6, tools), (trunk, tools), (trunk, sky + 18), (SK_X + SK_W + 8, sky + 18)])
            hx = x + len(layer) * 24 * 0.62 + 28           # stop clear of the heading's text
            if i:
                path([(SK_X - 6, sky + 18), (hx, y + 14)], dashed=True)
            else:
                path([(SK_X - 6, sky + 18), (x + NODE_W + 8, sky + 18)], dashed=True)
                bottom = sky + sh
        prev = (x, mid)
        y = bottom + LAYER_GAP
    close_frame(ladder)
    return ladder
    # frames 2-7 are gone from this drawing (JL 261007); s11-s13 and the theme ladders draw the variant trees below


# ── variant trees: what each Block, Job and Task variant's folder holds ────────────────────────
# Read off real folders on disk where one exists, otherwise each family's contract; "?" = open.
BLOCK_TREES = [
    ("work Block", "bNN_<topic>/", [
        ("├── bNN_<topic>.md", "Description: its face (was board.md)"),
        ("├── studio/", "Idea Studio: the team's room"),
        ("│   ├── sNN-<topic>/", "one discussion topic"),
        ("│   │   ├── sNN-<topic>.md", "what is decided so far"),
        ("│   │   ├── <drawing>.excalidraw", "the scratch; marks kept"),
        ("│   │   ├── build_<drawing>.py", "seeds the drawing"),
        ("│   │   └── chat/", "one file per session"),
        ("│   └── _build/", "helpers the topics share"),
        ("├── reports/", "Audience Report: the Questions"),
        ("│   └── qNN_<topic>/", "md · excalidraw · page.toml"),
        ("├── related/", "Description › Related"),
        ("│   ├── related.md", "one table: kind · item · link · why here"),
        ("│   └── <key>.pdf", "only under an open license"),
        ("├── delivery/", "optional: exports, built reports"),
        ("├── runs/", "Runs: the Block's own soft Runs"),
        ("│   ├── README.md", "the run types it has (tools write it)"),
        ("│   ├── run-draw-<sNN>/", "→ studio/sNN-<topic>/"),
        ("│   ├── run-report-<qNN>/", "→ reports/qNN_<topic>/"),
        ("│   ├── run-delivery-<dNN>/", "→ delivery/dNN-<…>/"),
        ("│   └── (each: run.yaml · .md · passes/)", ""),
        ("└── jNN_<job>/ …", "Work Details: its Jobs")]),
    ("discovery Block", "bNN_<topic>/", [   # the same folder as a work Block (JL 261006)
        ("├── bNN_<topic>.md", "Description: its face (was board.md)"),
        ("├── studio/", "Idea Studio: the team's room"),
        ("│   ├── sNN-<topic>/", "one discussion topic"),
        ("│   │   ├── sNN-<topic>.md", "what is decided so far"),
        ("│   │   ├── <drawing>.excalidraw", "the scratch; marks kept"),
        ("│   │   ├── build_<drawing>.py", "seeds the drawing"),
        ("│   │   └── chat/", "one file per session"),
        ("│   └── _build/", "helpers the topics share"),
        ("├── reports/", "Audience Report: the Questions"),
        ("│   └── qNN_<topic>/", "md · excalidraw · page.toml"),
        ("├── related/", "Description › Related"),
        ("│   ├── related.md", "one table: kind · item · link · why here"),
        ("│   └── <key>.pdf", "only under an open license"),
        ("├── delivery/", "optional: <block>.bib · reports"),
        ("├── runs/", "Runs: the Block's own soft Runs"),
        ("│   ├── README.md", "the run types it has (tools write it)"),
        ("│   ├── run-draw-<sNN>/", "→ studio/sNN-<topic>/"),
        ("│   ├── run-report-<qNN>/", "→ reports/qNN_<topic>/"),
        ("│   ├── run-delivery-bib/", "→ delivery/<block>.bib"),
        ("│   └── (each: run.yaml · .md · passes/)", ""),
        ("└── jNN_<inquiry>/ …", "Work Details: one inquiry per Job")]),
    ("cowork Block", "bNN_<topic>/", [
        ("├── bNN_<topic>.md", "its face: state · spine · close"),
        ("├── studio/sNN-<topic>/ …", "topics: draw · build · chat"),
        ("├── reports/qNN_<topic>/ …", "its Questions"),
        ("├── delivery/", "optional: exports, built reports"),
        ("├── runs/ (soft)", "README · run-status- · run-draw- · run-report-"),
        ("├── j00_people/ ?", "Description › People: a Job, or people.md?"),
        ("├── jNN_<job>/ …", "Work Details: one line of work each"),
        ("└── _old/", "replaced material")]),
    ("paper Board", "Paper-<Name>/", [
        ("├── bNN_<topic>.md", "the paper's face (was board.md)"),
        ("├── studio/sNN-<topic>/ …", "topics: draw · build · chat"),
        ("├── reports/qNN_<topic>/ …", "answers: RQ<n>"),
        ("├── related/", "Description › Related: one table"),
        ("├── venues/<venue>/", "Description › Venue: one folder per venue"),
        ("│   ├── call.md", "dates · limits · format · review rules"),
        ("│   └── kit/", "the author template, as the venue ships it"),
        ("├── delivery/ ?", "the built paper: here, or in each version's Job?"),
        ("│   ├── paper-build.toml", "order · venue · names"),
        ("│   ├── assemble.sh", "the build"),
        ("│   └── latex/ · word/", "master · DOCX"),
        ("├── runs/ (soft)", "README · run-story- · run-check- · run-delivery-"),
        ("├── j01_v1_<venue>/ ?", "a paper version = a Job"),
        ("├── j02_v2_<revision>/", "the next version"),
        ("├── jNN_grant_<funder>/ ?", "a grant from the same story: a Job"),
        ("└── jNN_slides_<talk>/ ?", "a talk's slides: a Job")]),
    ("insight Block (DIKW)", "bNN_<topic>_dikw/", [
        ("├── bNN_<topic>_dikw.md", "its face: the question register"),
        ("├── studio/sNN-<topic>/ …", "topics: draw · build · chat"),
        ("├── reports/qNN_<topic>/ …", "its Questions"),
        ("├── delivery/", "optional: Wisdom counsel · Handoff"),
        ("├── runs/ (soft)", "README · run-extract- · run-cut- · run-map- · …"),
        ("├── j01_data/", "DIKW level D: what was observed"),
        ("├── j02_information/", "DIKW level I: rates, contrasts"),
        ("├── j03_knowledge/", "DIKW level K: claims"),
        ("├── j04_wisdom/", "DIKW level W: counsel, handoff"),
        ("one script per question; Runs = dataset × partition", ""),
        ("on screen: the Block's Spaces; Work Details = the DIKW levels", ""),
        ("a DIKW level opens its own Job tab (was Prototype › Data)", ""),
        ("Meta (counts per DIKW level) stays on the Block ?", "")]),
    ("insight register board", "<Dataset>-InsightBoard/", [
        ("├── board.md", "the register (older layout)"),
        ("├── 0-MT-meta/", "the board's meta"),
        ("└── N-<partition>/ …", "one per partition"),
        ("carry over to a DIKW Block, or keep?", ""),
        ("its Instances = Jobs? partitions = Jobs?", ""),
        ("one workbench for both layouts?", "")]),
    ("design Board", "B00_DesignBoard-<name>/", [
        ("├── B00_DesignBoard-<name>.md", "its face: the Design Tasks"),
        ("├── design-goal.md", "the goal every design keeps"),
        ("├── design-theory.md", "the theory behind them"),
        ("├── studio/sNN-<topic>/ …", "topics: draw · build · chat"),
        ("├── delivery/", "optional: passed designs · test plan"),
        ("├── runs/ (soft)", "README · run-brief- · run-rules- · run-testplan-"),
        ("├── 0-BR-brief/", "stage 0: the brief"),
        ("├── 1-P-principle/", "stage 1: principles"),
        ("├── 2-Design/", "stage 2: the Design folders"),
        ("└── _archive/", "replaced material")]),
    ("labeling Block", "bNN_<topic>/", [   # b15 Q01 (261007): the labels of one topic, one Job per dataset × label
        ("├── bNN_<topic>.md", "Description: its face (was board.md)"),
        ("├── schema.yaml ?", "disk today: here · contract: per Job (b15 Q03)"),
        ("├── studio/sNN-<topic>/ …", "topics: draw · build · chat"),
        ("├── reports/qNN_<topic>/ …", "its Questions"),
        ("├── delivery/", "optional: final labels, exported"),
        ("├── runs/ (soft)", "README · run-setup-<job> · run-delivery-<dNN>"),
        ("├── jNN_<dataset>_<label>/ …", "one dataset, one label: build it"),
        ("└── jNN_<dataset2>_<label>/ …", "scan only: reads a handoff"),
        ("today: tasks/bNN_<label>/j01_building_corpus/ ?", "move = JL's call")]),
]
JOB_TREES = [
    ("work Job", "jNN_<job>/", [
        ("├── jNN_<job>.md ?", "its face: goal, state, next"),
        ("├── src/", "code shared by its Tasks"),
        ("├── sbatch/", "batch shared by its Tasks"),
        ("├── studio/", "optional: drawings (.excalidraw)"),
        ("├── runs/", "soft Runs only: no evidence at a Job"),
        ("│   ├── README.md", "the run types it has (tools write it)"),
        ("│   ├── run-plan-tasks/", "→ the face's task_groups · new tNN_"),
        ("│   └── run-launch-<group>/ ?", "sbatch/ → its Tasks' hard Runs"),
        ("└── tNN_<task>/ …", "its work Tasks")]),
    ("discovery Job", "jNN_<inquiry>/", [   # one inquiry, the Block's six Spaces (b14 Q01, 261007)
        ("├── jNN_<inquiry>.md ?", "Description: the inquiry (today: job: in each discovery.yaml)"),
        ("├── studio/", "optional: drawings (.excalidraw)"),
        ("├── delivery/", "optional: jNN_<inquiry>.bib, merged from its Tasks"),
        ("├── runs/", "Runs: soft only, no evidence at a Job"),
        ("│   ├── README.md", "the run types it has (tools write it)"),
        ("│   ├── run-plan-tasks/", "→ the face's sub-questions · new tNN_"),
        ("│   ├── run-delivery-bib/", "→ delivery/jNN_<inquiry>.bib"),
        ("│   └── (each: run.yaml · .md · passes/)", ""),
        ("└── tNN_<task>/ …", "Work Details: one sub-question each"),
        ("    each one discovery_type", "map · reading · verdict · landscape …"),
        ("no reports/: Audience Report = its Tasks' answers", ""),
        ("a synthesis across its Tasks: a Task of its own ?", ""),
        ("on screen: its Job tab, the Block's six Spaces", "")]),
    ("Page Job", "jNN_<job>/", [
        ("├── src/", "shared code, if any"),
        ("├── studio/", "optional: drawings (.excalidraw)"),
        ("├── runs/ (soft)", "README · run-plan-tasks"),
        ("└── tNN_<task>/ …", "its Page Tasks")]),
    ("paper version", "jNN_v<N>_<venue>/", [
        ("├── jNN_v<N>.md", "the version: venue · date · state"),
        ("├── studio/", "optional: drawings (.excalidraw)"),
        ("├── S-<desk>-<N>-<Section>/ …", "Main Sections: Page Tasks (group Main)"),
        ("├── S-<desk>-A<N>-<Section>/ …", "Appendix Sections: Page Tasks (group Appendix)"),
        ("├── tNN_cover_letter/ ?", "a Page Task (group Letters)"),
        ("├── tNN_rebuttal/ ?", "the reply to reviews: a Page Task"),
        ("├── story/ ?", "this version's Story"),
        ("├── delivery/", "this version, built"),
        ("├── runs/ (soft)", "README · run-narrative- · run-check-"),
        ("└── reviews → next version's Job ?", "")]),
    ("cowork Job", "jNN_<job>/", [   # one line of work; its items are rows, not Tasks (b13 Q01, 261007)
        ("├── jNN_<job>.md", "Description: state · waiting-on · since · next"),
        ("├── Timeline.md", "Work Details › Timeline: what happened when"),
        ("├── CHECKLIST.md", "Work Details › Checklist: what is left"),
        ("├── emails/ · meetings/", "Work Details: one row per file, not Tasks"),
        ("├── materials/", "Description › Files: what the Job uses"),
        ("├── design/ ?", "drawings → studio/, notes → materials/?"),
        ("├── studio/", "optional: drawings (.excalidraw)"),
        ("├── delivery/ ?", "what it sent and decided (b13 Q03)"),
        ("├── runs/ (soft)", "README · run-email-<thread> · run-notes-<meeting>"),
        ("└── tNN_<doc>/ ?", "only a document written in rounds: a Page Task"),
        ("on screen: its Job tab, the Block's six Spaces", ""),
        ("no hard Runs: code work is a work Task, cited", "")]),
    ("DIKW level", "j01_data/", [
        ("├── level.md", "what this DIKW level asks"),
        ("├── src/", "code its questions share"),
        ("├── studio/", "optional: drawings (.excalidraw)"),
        ("├── runs/ (soft)", "README · run-plan-evidence · run-review-questions"),
        ("└── tNN_<question>/ …", "one Task per question"),
        ("j02_information/ · j03_knowledge/", "· j04_wisdom/: the same"),
        ("on screen: its Job tab, the Block's six Spaces", ""),
        ("today: a View of Block › Prototype", ""),
        ("its rows in each partition's Insight table", "")]),
    ("design method", "jNN_<goal>_by-<method>/", [   # one goal x one method -> N designs (JL 261007)
        ("├── jNN_<goal>_by-<method>.md", "Description: the goal, its rules, N"),
        ("├── method.md", "the method card, frozen: ① see ② do ③ check"),
        ("├── studio/", "optional: drawings (.excalidraw)"),
        ("├── reports/qNN_<topic>/ ?", "Audience Report: what its N designs show"),
        ("├── delivery/", "passed designs, word for word · csv"),
        ("├── runs/", "README · run-commission- · rNN_generate_<N>/"),
        ("└── tNN_d<NN>_<slug>/ …", "Work Details: one design item each"),
        ("the same goal by another method", "= a sibling Job: compare them"),
        ("today: 2-Design-M<NN>-<method>/", "a method holds every goal; a goal is a Task"),
        ("on screen: its Job tab, the Block's six Spaces", "")]),
    ("labeling Job", "jNN_<dataset>_<label>/", [   # b15 Q01 (261007): one dataset × one label, four steps
        ("├── jNN_<dataset>_<label>.md", "Description: dataset · label · human"),
        ("├── schema.yaml", "the label, by version (b15 Q03)"),
        ("├── src/", "code its step Tasks share"),
        ("├── studio/", "optional: drawings (.excalidraw)"),
        ("├── runs/ (soft)", "README · run-setup-job · run-plan-tasks"),
        ("├── delivery/ ?", "from below: handoff · final labels"),
        ("├── t01_<dataset>_items/", "prepare: items, fenced (work Task)"),
        ("├── t02_<dataset>_keys/", "keys: its own labels, kept blind"),
        ("├── t03_<dataset>_labeling/", "label: the labeling Task"),
        ("└── t04_<dataset>_scoring/", "score: our labels vs the keys"),
        ("on screen: its Job tab, the Block's six Spaces", ""),
        ("today: no Job screen; the Task's page", "reaches up (Preparation · External gold)")]),
]
TASK_TREES = [
    ("work Task", "tNN_<task>/", [
        ("├── tNN_<task>.md", "the Page"),
        ("├── CODE_REVIEW.md", "the code review"),
        ("├── scripts/<worker>.py", "the code"),
        ("├── runs/", "its Runs: hard (the work = evidence)"),
        ("│   ├── README.md", "the run types it has (tools write it)"),
        ("│   └── rNN_<slug>/", "one hard Run"),
        ("│       ├── run.yaml", "the card"),
        ("│       ├── rNN_<slug>.sh", "the ticket"),
        ("│       ├── config.yaml", "frozen inputs"),
        ("│       ├── result/", "generated: metrics · tables · figures"),
        ("│       │   └── heavy.yaml", "→ <ProjectResult>/…"),
        ("│       └── passes/pNN-<MMDD>/", "log · runtime.yaml (the receipt)"),
        ("├── notebooks/rNN_<run>.ipynb", "executed, generated"),
        ("├── workflow/", "plan.yaml · report.yaml"),
        ("└── studio/ · sbatch/", "optional plugins")]),
    ("Page Task", "tNN_<task>/", [   # from haipipe-page's Folder contract; a paper Section is one
        ("├── tNN_<task>.md", "the Page: Opening · Content"),
        ("├── page.toml", "registers the Page"),
        ("├── <stem>.bib", "its verified citations (run-citation-)"),
        ("├── draft/", "the human's process"),
        ("│   ├── <stem>-draft-v<G>.<S>.md", "the one current plan"),
        ("│   ├── <stem>-evidence-items.md", "Citations · Displays · Values"),
        ("│   ├── records/", "context · feedback · log"),
        ("│   └── previous/", "superseded plans"),
        ("├── workflow/", "the machine's receipts"),
        ("├── displays/<fig>/", "recipe/ (plot script) · assets/ (figure)"),
        ("├── runs/", "soft Runs only: no new facts here"),
        ("│   ├── README.md", "the run types it has"),
        ("│   ├── run-structure-<target>/", "the plan"),
        ("│   ├── run-section- · run-paragraph-", "writing"),
        ("│   ├── run-revise- · run-scratch-", "edits · rough thinking"),
        ("│   ├── run-display-<fig>/", "plots a hard Result → displays/"),
        ("│   ├── run-value- · run-citation-", "quote a hard Result"),
        ("│   ├── run-delivery-<lane>/", "builds delivery/<lane>/"),
        ("│   └── (each: run.yaml · .md · passes/)", ""),
        ("├── delivery/", "built, never edited"),
        ("│   └── web/ latex/ word/ slide/", "one per lane"),
        ("└── studio/", "the person's room"),
        ("    ├── chat/", "sessions kept"),
        ("    └── draw/", "one scene per owner"),
        ("a paper Section is a Page Task: S-<desk>-<N>-<…>/", "inside a version Job (JL 261006)"),
        ("its .tex: delivery/latex/S-<…>.tex", "the fragment the paper pulls in")]),
    ("discovery Task", "tNN_<task>/", [   # a Page that makes facts: hard Paper Runs + its Page's soft Runs (b14 Q01)
        ("├── tNN_<task>.md", "the Task Page: the article, its synthesis"),
        ("├── discovery.yaml", "its contract: question · type · admission rule"),
        ("├── summary | verdict | landscape.md", "optional typed record, by discovery_type"),
        ("├── draft/", "the Page's process: plan · evidence items"),
        ("│   ├── evidence/bibex/tNN_<task>.bib", "the Evidence Bib, derived from its Results"),
        ("│   └── records/search/ ?", "screened candidates (today results/search/)"),
        ("├── workflow/", "D1 + Page receipts"),
        ("├── scripts/", "optional: a reusable instrument"),
        ("├── studio/", "optional: drawings (.excalidraw)"),
        ("├── delivery/", "optional: the article, built (web)"),
        ("└── runs/", "hard Paper Runs + the Page's soft Runs"),
        ("    ├── README.md", "the run types it has"),
        ("    ├── rNN_<author><year>_<subject>/", "hard: one Subject (one paper)"),
        ("    │   ├── run.yaml · rNN_<…>.sh", "the card · the ticket"),
        ("    │   ├── result/", "generated"),
        ("    │   │   ├── rNN_<…>.md", "the Result Card"),
        ("    │   │   ├── facts.md · abstract.md", "what the source says"),
        ("    │   │   ├── rNN_<…>.bib", "one BibTeX entry"),
        ("    │   │   └── source-access.json", "how it was read"),
        ("    │   └── passes/pNN-<MMDD>/ ?", "log · runtime.yaml (today result/runtime.yaml)"),
        ("    ├── run-structure- · run-section-", "soft: write the Page"),
        ("    ├── run-citation-<rNN>/", "soft: cite its own Result in the Page"),
        ("    └── run-check-<task>/", "soft: CHECK closes the Task"),
        ("today: runs/rNN.sh + results/rNN/ ?", "one move, by script (s01-D15)")]),
    ("insight question", "tNN_<question>/", [
        ("├── tNN_<question>.md", "the answering Page"),
        ("├── question.md", "the question itself"),
        ("├── draft/", "plan · evidence items · records/"),
        ("├── scripts/<script>.py", "its one script"),
        ("├── studio/", "optional: drawings (.excalidraw)"),
        ("├── runs/", "hard and soft"),
        ("│   ├── README.md", "the run types it has"),
        ("│   ├── <dataset>_<partition>/", "hard: one per dataset × partition"),
        ("│   │   └── run.yaml · .sh · result/ · passes/", ""),
        ("│   ├── rNN_ name for these ?", ""),
        ("│   └── run-check- · run-revise-", "soft: Page checks and edits"),
        ("└── reports/<dataset>_<partition>/", "the generated report")]),
    ("design folder", "Design-NN-<slug>/", [   # one design task, its candidates
        ("├── Design-NN-<slug>.md", "the design task"),
        ("├── draft/", "the human's process"),
        ("│   ├── <stem>-design-items.md", "one card per design"),
        ("│   └── feedback/", "notes on each generation"),
        ("├── scripts/", "helpers"),
        ("├── studio/", "optional: drawings (.excalidraw)"),
        ("└── runs/", "three kinds of Run"),
        ("    ├── README.md", "the run types it has"),
        ("    ├── run-commission-<target>/", "soft: release or hold, a decision"),
        ("    │   └── decision.yaml", "the person's decision"),
        ("    ├── rNN_generate_<slug>/", "hard: the candidate stays inside"),
        ("    │   └── result/ content · checks", "the design, checked"),
        ("    └── rNN_verify_<slug>/", "hard: an independent check"),
        ("        └── result/ review.md · checks", "the verdict")]),
    ("labeling Task", "tNN_<dataset>_labeling/", [   # b15 Q01 (261007): the Job's label step, one engine job
        ("├── tNN_<…>.md", "the labeling Page (page-type: labeling)"),
        ("├── labeling/", "the engine's lane: canonical records"),
        ("│   ├── config · corpus/ · policy/", "Building: the contract, G_t"),
        ("│   ├── rounds/round_NN/ · gold/", "Building: calibration, D_cal"),
        ("│   ├── handoff/label-v<N>.yaml", "the one crossing (signed)"),
        ("│   └── test/ · evaluation/ · production/ · audit/", "Scanning: T*, scorecards, D*"),
        ("├── studio/", "optional: drawings (.excalidraw)"),
        ("├── delivery/ ?", "exports for readers: final labels"),
        ("└── runs/", "hard: one per operation"),
        ("    ├── README.md", "the 26 run types, Building · Scanning"),
        ("    └── rNN_<operation>_<target>/", "one Run (was run-labeling-<op>-<MMDD>-…)"),
        ("        ├── run.yaml · rNN_<…>.yaml", "the card · the ticket (runner)"),
        ("        ├── result/result.yaml ?", "pointers into labeling/: hard or soft?"),
        ("        └── passes/pNN-<MMDD>/", "a resumed human session = a pass"),
        ("prepare · keys · score Tasks", "= work Tasks (the work Task row)"),
        ("(data: the LabelingStore,", "outside git)")]),
]


# the variant frames in four groups, two columns (JL 261007): the biggest, work · paper, top left;
# discovery · cowork under it; insight · design on the right; labeling under them
VARIANT_GROUPS = [
    ("work · paper", 0, ["work Block", "paper Board", "work Job", "Page Job", "paper version", "work Task",
                         "Page Task"]),
    ("discovery · cowork", 0, ["discovery Block", "cowork Block", "discovery Job", "cowork Job", "discovery Task"]),
    ("insight · design", 1, ["insight Block (DIKW)", "insight register board", "design Board", "DIKW level",
                             "design method", "insight question", "design folder"]),
    ("labeling", 1, ["labeling Block", "labeling Job", "labeling Task"]),
]


def arrange_groups(top, groups=VARIANT_GROUPS, frame_gap=200, group_gap=400, col_gap=600):
    """Move each variant's frame into its group: a group is a stack of frames under its heading,
    and the groups stack in their column. A frame not in any group joins the first column's end."""
    frames = {e["name"]: e for e in els if e["type"] == "frame"}
    left = min(f["x"] for f in frames.values())
    placed = {v for _, _, vs in groups for v in vs}
    rest = [n for n in frames if n not in placed]
    plan = groups + ([("other", 0, rest)] if rest else [])
    x = left
    for col in sorted({c for _, c, _ in plan}):
        y, right = top, x
        for name, c, variants in plan:
            members = [frames[v] for v in variants if v in frames]
            if c != col or not members:
                continue
            text(x + 40, y, name, 34)
            y += 80
            for fr in members:
                dx, dy = x - fr["x"], y - fr["y"]
                for e in els:
                    if e is fr or e.get("frameId") == fr["id"]:
                        e["x"] += dx
                        e["y"] += dy
                y += fr["height"] + frame_gap
                right = max(right, fr["x"] + fr["width"])
            y += group_gap - frame_gap
        x = right + col_gap


def draw_trees(title, subtitle, trees, y0, frame_each=False, views=None, block=None, groups=False):
    """One row per variant, top to bottom: its folder -> what the folder holds -> on screen.
    frame_each: each variant's row is its own frame, named after the variant (a topic drawing).
    groups: then arrange the frames in VARIANT_GROUPS, two columns (needs frame_each).
    views(x, y, variant) -> bottom: draws the screens column instead of the default one.
    block: the rows are Block variants (column heads, blockers); default: trees is BLOCK_TREES."""
    block = trees is BLOCK_TREES if block is None else block
    text(0, y0, title, 30)
    text(0, y0 + 46, subtitle, 16, GRAY)
    TX = 450                                           # the tree column
    name_w = max(250, max(len(l) for _, _, t in trees for l, _ in t) * 14 * 0.6 + 16)
    mean_w = max(len(m) for _, _, t in trees for _, m in t) * 13 * 0.55
    tree_w = name_w + mean_w + 40
    SX = TX + tree_w + 50                              # the skills, one column for every row
    WX = SX + SKW + 30                                 # the screen sketch, one column for every row
    def heads(hy):                                     # the column heads
        text(TX, hy, "what the folder holds", 14, INK)
        text(SX, hy, "skills: owns · works · shows", 14, BLUE)
        if block:                                      # one screen per view of the Block tab
            for i, v in enumerate(BLOCK_VIEW_NAMES):
                text(WX + i * (UI_W + VIEW_GAP), hy, COLUMN_HEAD.get(v, f"Block › {v}"), 14, TEAL)
        else:
            text(WX, hy, "UI scratch: where it shows", 14, TEAL)

    if not frame_each:
        heads(y0 + 112)
    y = y0 + 160
    for variant, folder, tree in trees:
        fr = open_frame(variant) if frame_each else None
        if frame_each:                                 # each frame carries its own heads (JL 261006)
            heads(y - 34)
        text(0, y, variant, 22)
        box(0, y + 34, NODE_W, SP_H, folder, 15)
        ty = y + 34 + 14
        for line, meaning in tree:
            red = line.rstrip().endswith("?")
            text(TX + 12, ty, line, 14, RED if red else INK, MONO)
            if meaning:
                text(TX + 12 + name_w, ty + 1, meaning, 13, RED if red else GRAY)
            ty += 22
        tree_bottom = ty + ROOM
        base("rectangle", TX, y + 34, tree_w, tree_bottom - (y + 34), GRAY, 1)
        path([(NODE_W + 6, y + 34 + SP_H / 2), (TX - 8, y + 34 + SP_H / 2)])
        sk_bottom = draw_skills(SX, y + 40, variant)
        if views:
            ui_bottom = views(WX, y + 10, variant)
        elif variant in BLOCK_FAMILY:
            ui_bottom = block_views(WX, y + 10, variant)
        else:
            ui_bottom = wireframe(WX, y + 10, UI_WHERE[variant]) if variant in UI_WHERE else y
        if block:                                      # the blockers: one block per group of Spaces
            block_dividers(WX, y - 50, ui_bottom + 10)
        y = max(tree_bottom, sk_bottom, ui_bottom, y + 34 + SP_H + 60)
        if frame_each:                                 # the frames stand apart: a wide gap, no rule
            close_frame(fr, pad=40)
            y += 200
        else:
            y += 90
            path([(0, y - 45), (WX + UI_W + 40, y - 45)], arrow=False, color=INK)
    if frame_each and groups:
        arrange_groups(y0 + 160)


# ── under the Run layer: every run type, one column per Theme, read from the workbench tables ──
PLUGINS = Path(__file__).resolve().parents[4] / "plugins"
TK = "haipipe-toolkit/skills"
# Task variant -> its workbench table -> the Spaces whose runs act on one Task, minus Block-level runs
TASK_RUNS = [
    ("work Task", "tNN_<task>/", f"{TK}/2_theme/work/workbench-work", {"Task", "Check"},
     {"Plan the report", "Write the report", "Check a report"}, "rNN_<noun>_<qualifier>.sh",
     "Task workbench · /w/<block>"),
    ("Page Task", "tNN_<task>/", f"{TK}/1_base/page/workbench-page", {"Draft", "Evidence", "Delivery"},
     set(), "soft only: run-<type>-<target>", "Page workbench · one Page"),
    ("paper Section", "S-<desk>-<Section>/", f"{TK}/2_theme/paper/workbench-paper", {"Sections"},
     set(), "soft only: run-section-<target> · run-delivery-latex", "Paper workbench · /w/<paper>"),
    ("discovery Task", "tNN_<task>/", f"{TK}/2_theme/discovery/workbench-discovery", {"Work", "Check"},
     {"Write the report", "Check a report"}, "rNN_<author><year>_<subject>.sh", "Discovery workbench · /w/<block>"),
    ("insight question", "tNN_<question>/", f"{TK}/2_theme/insight/workbench-insight",
     {"Prototype", "Insight", "Check"}, {"Carry a board over", "Register a cut", "Draw the question map"},
     "<dataset>_<partition>.sh · run-check-…", "Insight workbench · /w/<block>"),
    ("design folder", "Design-NN-<slug>/", f"{TK}/2_theme/design/workbench-design",
     {"Design Task", "Design Item", "Delivery"}, set(), "run-commission- (soft) · rNN_generate_ · rNN_verify_",
     "Design workbench · page level"),
    ("labeling Task", "tNN_<task>/", "haipipe-toolkit/skills/2_theme/labeling/workbench-labeling",
     {"Data", "Labeling", "Quality", "Delivery"}, set(), "rNN_<operation>_<target>/ (today run-labeling-…)",
     "Labeling workbench · the labeling Task"),
]


def ui_tree(table):
    """The workbench's own layout: [(level, Space, [(subspace, [rows with a run])])], in table order."""
    tree = []
    path_ = PLUGINS / table / "ref/workbench-table.md"
    if not path_.exists():                   # the skills moved into groups (1_base/, 2_theme/): find it by name
        path_ = next((PLUGINS / table).parent.parent.glob(f"**/{Path(table).name}/ref/workbench-table.md"))
    for line in path_.read_text().splitlines():
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) < 6 or c[0] not in ("board", "page"):
            continue
        if not tree or tree[-1][:2] != (c[0], c[1]):
            tree.append((c[0], c[1], []))
        views = tree[-1][2]                  # a subspace listed twice in the table is one subspace
        view = c[2]
        if " · " in view and len(view) > 22:
            view = "·".join(w.strip()[0] for w in view.split(" · "))
        if view not in [v for v, _ in views]:
            views.append((view, []))
        rs = next(r for v, r in views if v == view)
        if c[3] not in ("none", "") and c[3] not in [r["Run"] for r in rs]:
            rs.append(dict(Level=c[0], Space=c[1], View=view, Run=c[3], Agent=c[4], Skill=c[5]))
    return tree


# ── the skills of each variant: who owns its folder, who works in it, who shows it ──────────────
VARIANT_SKILLS = {
    # Blocks
    "work Block": [("owns", ["haipipe-task", "haipipe-question  (reports/)", "excalidraw-report  (studio/)"]),
                   ("shows", ["workbench-work"])],
    "discovery Block": [("owns", ["haipipe-discovery", "haipipe-question  (reports/)"]),
                        ("shows", ["workbench-discovery"])],
    "cowork Block": [("owns", ["haipipe-cowork", "haipipe-question  (reports/)"]),
                     ("shows", ["workbench-cowork"])],
    "paper Board": [("owns", ["haipipe-paper"]),
                    ("works", ["haipipe-paper-workflow", "haipipe-paper-ideation", "haipipe-paper-story"]),
                    ("shows", ["workbench-paper"])],
    "insight Block (DIKW)": [("owns", ["haipipe-insight"]), ("works", ["haipipe-insight-workflow",
                                                                      "haipipe-insight-meta"]),
                             ("shows", ["workbench-insight"])],
    "insight register board": [("owns", ["haipipe-insight", "haipipe-insight-question"]),
                               ("shows", ["workbench-insight"])],
    "design Board": [("owns", ["haipipe-design", "haipipe-design-brief"]),
                     ("works", ["haipipe-design-workflow", "haipipe-design-goal"]),
                     ("shows", ["workbench-design"])],
    "labeling Block": [("owns", ["haipipe-labeling", "haipipe-question  (reports/)"]),
                       ("works", ["haipipe-labeling-workflow  (which Job is next)"]),
                       ("shows", ["workbench-labeling"])],
    # Jobs
    "work Job": [("owns", ["haipipe-task"]), ("works", ["haipipe-task-for-<type>"]),
                 ("shows", ["workbench-work"])],
    "discovery Job": [("owns", ["haipipe-discovery", "haipipe-discovery-inquiry"]),
                      ("shows", ["workbench-discovery"])],
    "Page Job": [("owns", ["haipipe-task", "haipipe-task-for-page"]), ("shows", ["workbench-work"])],
    "paper version": [("owns", ["haipipe-paper"]), ("works", ["haipipe-paper-section", "haipipe-paper-assemble"]),
                   ("shows", ["workbench-paper"])],
    "cowork Job": [("owns", ["haipipe-cowork"]), ("shows", ["workbench-cowork"])],
    "DIKW level": [("owns", ["haipipe-insight"]), ("works", ["haipipe-insight-data · -information",
                                                           "haipipe-insight-knowledge · -wisdom"]),
                  ("shows", ["workbench-insight"])],
    "design method": [("owns", ["haipipe-design"]), ("works", ["haipipe-design-unit", "haipipe-design-workflow"]),
                     ("shows", ["workbench-design"])],
    "labeling Job": [("owns", ["haipipe-labeling", "haipipe-labeling-contract  (schema)"]),
                     ("works", ["haipipe-labeling-preparation  (prepare)", "haipipe-task  (keys · score)"]),
                     ("shows", ["workbench-labeling"])],
    # Tasks
    "work Task": [("owns", ["haipipe-task", "haipipe-folder"]), ("works", ["haipipe-task-for-<type>", "haipipe-run"]),
                  ("shows", ["workbench-work"])],
    "Page Task": [("owns", ["haipipe-page", "haipipe-folder", "haipipe-paper-section  (a Section)"]),
                  ("works", ["haipipe-page-workflow", "haipipe-run"]),
                  ("shows", ["workbench-page  (a Section opens here)", "workbench-studio  (studio/)"])],
    "paper Section": [("owns", ["haipipe-paper-section", "haipipe-page"]),
                      ("works", ["haipipe-page-workflow", "haipipe-run"]), ("shows", ["workbench-paper"])],
    "discovery Task": [("owns", ["haipipe-discovery-inquiry"]),
                       ("works", ["haipipe-discovery-search · -review", "haipipe-discovery-synthesize",
                                  "haipipe-page-workflow  (its Page)", "haipipe-run"]),
                       ("shows", ["workbench-discovery"])],
    "insight question": [("owns", ["haipipe-insight-question"]),
                         ("works", ["haipipe-insight-evidence-plan", "haipipe-insight-check", "haipipe-run"]),
                         ("shows", ["workbench-insight"])],
    "design folder": [("owns", ["haipipe-design"]), ("works", ["haipipe-design-unit", "haipipe-design-workflow",
                                                             "haipipe-run"]),
                      ("shows", ["workbench-design"])],
    "labeling Task": [("owns", ["haipipe-labeling"]),
                      ("works", ["haipipe-labeling-workflow", "haipipe-labeling-building  (step order: ref/)", "haipipe-labeling-scanning",
                                 "haipipe-labeling-<view> × 12", "haipipe-run"]),
                      ("shows", ["workbench-labeling"])],
}
SKW = 330                                              # the skills column's width


def draw_skills(x, y, variant):
    """owns / works / shows, each with its skills in monospace; returns the bottom."""
    for role, names in VARIANT_SKILLS.get(variant, []):
        text(x, y, role, 12, GRAY)
        y += 18
        for n in names:
            text(x + 12, y, n, 13, RED if n.endswith("?") else BLUE, MONO)
            y += 19
        y += 6
    return y


# ── UI scratch: a plain, high-level wireframe of the workbench screen where a folder shows ─────
UI_TABLES = {"task": f"{TK}/2_theme/work/workbench-work", "discovery": f"{TK}/2_theme/discovery/workbench-discovery",
             "cowork": f"{TK}/2_theme/cowork/workbench-cowork", "paper": f"{TK}/2_theme/paper/workbench-paper",
             "insight": f"{TK}/2_theme/insight/workbench-insight", "design": f"{TK}/2_theme/design/workbench-design",
             "page": f"{TK}/1_base/page/workbench-page",
             "labeling": "haipipe-toolkit/skills/2_theme/labeling/workbench-labeling"}
# The Block workbench, proposed (JL 261006, frames 6-7): Level = the tab (Guide · Block · Job · Task);
# Space = the row below it; Subspace = the third row, an item (sNN · qNN · dNN) or a group.
# The tabs are the ladder; each shows ONE folder of its level, picked from the list one tab up. Every
# level: what it is · Studio (optional drawings) | its children | Runs · Delivery. The children list
# (Jobs, a Job's Tasks) has a third row of buttons, its groups; a Task's Runs are one plain list.
# No Check Space (JL 261006): what waits shows on each row (Block › Jobs opens each Job to its Tasks),
# a check is a Run, and a release check sits in Delivery. Insight keeps today's Check (its gates).
LEVEL_TABS = ["Guide", "Block", "Job ▾", "Task ▾"]
# The Block tab's Spaces, one per part of its folder (JL 261006): Description (its face, its
# resources, its related papers) · Idea Studio (studio/) · Audience Report (reports/) | Work Details
# (its Jobs with their Tasks) | Runs (its own runs/, third row: their run types) · Delivery
# (delivery/); Runs and Delivery are optional. Every family keeps them; its own views go in the
# third row. Insight puts today's Insight workbench views there
# (workbench-insight 0.16.0): Scope → Description, RoadMap Draw → Idea Studio, Insight (by
# partition) → Audience Report, Prototype (by DIKW level) → Work Details; today's Check is left out.
BLOCK_SPACES = ["Description", "|", "Idea Studio", "Audience Report", "|", "Work Details", "|", "~Runs",
                "~Delivery"]
INSIGHT_VIEWS = {"Description": ["Dataset", "Partitions", "Questions"],
                 "Audience Report": ["Full", "<cut>", "<cut>", "Cross"],
                 "Work Details": [], "Delivery": ["Handoff"]}   # Work Details: the four DIKW levels, each a Job (JL 261006)
JOB_CHILDREN = {"task": ["Tasks"], "discovery": ["Tasks"], "cowork": ["Timeline", "Emails", "Meetings"],
                "insight": ["Questions"], "paper": ["Sections"], "design": ["Design folders"],
                "labeling": ["Tasks"]}
# A DIKW level is a Job (JL 261006: "they are in the board level, do you think in the job level"): its tab
# takes the Block's six Spaces; today's Prototype › Data view becomes its Work Details (its questions).
JOB_SPACES_DIKW = ["Description", "|", "~Idea Studio", "Audience Report", "|", "Work Details", "|", "Runs",
                   "~Delivery"]
# A design Job is one goal done by one method, returning N designs (JL 261007: "a design method + design
# goal + N design items as a job"); each design is a Task. Delivery is not optional: step 5, Release.
JOB_SPACES_DESIGN = ["Description", "|", "~Idea Studio", "Audience Report", "|", "Work Details", "|", "Runs",
                     "Delivery"]
# A discovery Job is one inquiry (b14 Q01, 261007): the Block's six Spaces; Work Details = its sub-question
# Tasks, Audience Report = their answers (a view, no reports/), Delivery (optional) = its merged Bib.
JOB_SPACES_DISCOVERY = ["Description", "|", "~Idea Studio", "Audience Report", "|", "Work Details", "|", "Runs",
                        "~Delivery"]
# A cowork Job is one line of work (b13 Q01, 261007): the Block's six Spaces; its emails, meetings and
# checklist steps are rows of Work Details, not Tasks. Audience Report and Delivery are optional.
JOB_SPACES_COWORK = ["Description", "|", "~Idea Studio", "~Audience Report", "|", "Work Details", "|", "Runs",
                     "~Delivery"]
# A labeling Job is one dataset × one label (b15 Q01, 261007): its tab takes the six Spaces; its Tasks are the
# four steps (prepare · keys · label · score); Delivery rolls up the label Task's handoff and final labels.
JOB_SPACES_LABELING = ["Description", "|", "~Idea Studio", "Audience Report", "|", "Work Details", "|", "Runs",
                       "Delivery"]
# A Task's six Spaces (JL 261006): Description | Idea Studio · Audience Report | Work Details |
# Runs · Delivery, as on the Block tab. A variant's parts are not Spaces: they are groups in a third row
# (a Page's Table · Reading in Audience Report, its Draft-… · Evidence-… in Work Details, its Runs by
# type; see level_views.REPORT_GROUPS, WORK_GROUPS); Description's groups come from TASK_DESCRIPTION.
TASK_DESCRIPTION = {"work Task": ["Scope", "Plan"], "Page Task": ["Scope", "Plan", "Requirement", "Records"], "labeling Task": ["Scope", "Contract", "Records"],
                    "discovery Task": ["Scope", "Admission", "Records"]}                     # default: Scope · Plan · Records
TASK_PARTS = {"work Task": [], "Page Task": ["Draft", "Evidence"], "paper Section": ["Draft", "Evidence"],
              "discovery Task": ["Papers", "Intake", "Draft"], "insight question": ["Partitions"],
              "design folder": ["Design Task", "Design Item"], "labeling Task": []}
JOB_GROUPS = {"task": ["All", "j0N", "j1N", "j5N"], "discovery": ["All", "j0N", "j1N"],
              "cowork": ["All", "open", "waiting", "done"], "insight": ["All"], "paper": ["All", "main", "appendix", "grants", "slides"],
              "design": ["All", "Internal", "External", "Goal Only"], "labeling": ["All", "<label>", "<label>"]}
TASK_GROUPS = {"task": ["All", "t0N", "t1N"], "discovery": ["All", "t0N", "t1N"], "insight": ["All", "t0N", "t1N"],
               "paper": ["All", "Main", "Appendix", "Letters"], "design": ["All", "t0N"],
               "labeling": ["All", "prepare", "keys", "label", "score"]}
LEVEL_RUNS = {"Block": ["Update the Block status", "Ask a Question", "+ Add topic", "Open a Job"],
              "Job": ["Update the Job", "Plan its Tasks", "Add a Task", "Review the Job"]}


def level_subs(family, tab, variant=None):
    """The Spaces of a Level, in one order: face · items | children | Runs · Delivery ("~" = optional)."""
    if tab == "Guide":                                 # the family's docs (Tools), as today
        return ["Description", "Method", "RoadMap Draw", "Related Paper"]
    if tab == "Block":                                 # five Spaces, every family (JL 261006)
        return BLOCK_SPACES
    if tab == "Job" and family == "insight":           # a DIKW level: the six Spaces (JL 261006)
        return JOB_SPACES_DIKW
    if tab == "Job" and family == "design":            # goal × method → N designs: the six Spaces (JL 261007)
        return JOB_SPACES_DESIGN
    if tab == "Job" and family == "discovery":         # one inquiry: the six Spaces (b14 Q01, 261007)
        return JOB_SPACES_DISCOVERY
    if tab == "Job" and family == "labeling":          # dataset × label: the six Spaces (b15 Q01, 261007)
        return JOB_SPACES_LABELING
    if tab == "Job" and family == "cowork":            # one line of work: the six Spaces (b13 Q01, 261007)
        return JOB_SPACES_COWORK
    if tab == "Job":
        return ["Overview", "~Studio", "~Reports", "|"] + JOB_CHILDREN[family] + ["|", "Runs", "~Delivery"]
    return ["Description", "|", "~Idea Studio", "~Audience Report", "|", "Work Details", "|", "Runs", "Delivery"]


GROUP_ROWS = {"Description": ["Scope", "Resources", "Related"],   # the Block's face and what it uses
              # no Idea Studio row (JL 261006): one drawing after another, each named for what it draws
              "Audience Report": ["All", "<group A>", "<group B>"],   # the questions' groups
              "Reports": ["All", "<group A>", "<group B>"],
              "Delivery": ["All", "Report", "Export"],                 # delivery types
              "Draft": ["Table", "Reading", "Scratch", "Revise"],       # views of one Page
              "Evidence": ["Citations", "Displays", "Values"]}


# a family's own groups for a Block Space (JL 261006, paper: today's Ideation, Story and Delivery views)
FAMILY_GROUPS = {("cowork", "Description"): ["Scope", "People", "Resources", "Related"],
                 # paper: where it goes, second like cowork's People (JL 261006: "the venue resources here?")
                 ("paper", "Description"): ["Scope", "Venue", "Resources", "Related"],
                 ("paper", "Audience Report"):["Ideation", "Spine", "Design", "Narrative",
                                                "High-level logic + Low-level work", "Related Questions"],
                 # the paper's Sections by group, then its evidence (b16, 261007)
                 ("paper", "Work Details"): ["Main", "Appendix", "Evidence"],
                 ("paper", "Delivery"): ["LaTeX", "Word", "Cover letter", "Rounds"]}


def subspace_row(family, tab, space):
    """The third row: a group of the open Space's items (or a view); None = no row. Never one item:
    the items are the rows of the content, stacked top to bottom."""
    if tab == "Guide":                                                  # the family's docs: no third row
        return None
    if family == "insight" and tab == "Block" and space in INSIGHT_VIEWS:
        return INSIGHT_VIEWS[space]                                     # today's Insight views
    if tab == "Block" and (family, space) in FAMILY_GROUPS:
        return FAMILY_GROUPS[(family, space)]
    if tab == "Block" and space == "Work Details":                      # its Jobs' groups
        return JOB_GROUPS.get(family)
    if tab == "Block" and space == "Runs":                              # its Runs, by run type (JL 261006)
        return ["All"] + (VIEW_FAMILY.get(family, {}).get("Runs") or VIEW_DEFAULT["Runs"])[1]
    if space == "Jobs":
        return JOB_GROUPS.get(family)
    if tab == "Job" and space in JOB_CHILDREN[family]:
        return TASK_GROUPS.get(family)
    return GROUP_ROWS.get(space)


def task_runs(variant):
    """The run buttons of one Task variant, from its workbench table."""
    for v, _, table, spaces, skip, _, _ in TASK_RUNS:
        if v == variant:
            names = []
            for _, sp_name, views in ui_tree(table):
                for _, rs in views:
                    names += [r["Run"] for r in rs if sp_name in spaces and r["Run"] not in skip and r["Run"] not in names]
            return names
    return []


UI_W, UI_H = 560, 280
# variant -> (family, tab, Task variant, open subspace, open group, body: card|rows|runs, highlighted, caption)
UI_WHERE = {
    # Blocks: the Block tab, opened on Scope
    "work Block": ("task", "Block", None, "Scope", None, "card", "the topics this Block covers",
                   "the Block tab; Scope says what it covers"),
    "discovery Block": ("discovery", "Block", None, "Scope", None, "card", "the topics this Block covers",
                        "the Block tab"),
    "cowork Block": ("cowork", "Block", None, "Scope", None, "card", "status · what we coordinate", "the Block tab"),
    "paper Board": ("paper", "Block", None, "Scope", None, "card", "the paper's spine",
                    "the Block tab; its Jobs are the versions"),
    "insight Block (DIKW)": ("insight", "Block", None, "Scope", None, "card", "dataset · partitions",
                             "the Block tab; its Jobs are the 4 DIKW levels"),
    "insight register board": ("insight", "Block", None, "Prototype", "Meta", "card", "0-MT-meta · MT01-MT04",
                               "same tabs, older board on disk"),
    "design Board": ("design", "Block", None, "Scope", None, "card", "what this Board designs", "the Block tab"),
    "labeling Block": ("labeling", "Block", None, "Scope", None, "card", "the labels this Block builds",
                       "the Block tab"),
    # Jobs: one row in Block › Jobs, under its group; pick it → the Job tab
    "work Job": ("task", "Block", None, "Jobs", "j1N", "rows", "jNN_<job>", "a row in Block › Jobs; pick → Job tab"),
    "discovery Job": ("discovery", "Block", None, "Jobs", "All", "rows", "jNN_<inquiry>", "a row in Block › Jobs"),
    "Page Job": ("task", "Block", None, "Jobs", "j1N", "rows", "jNN_<job>", "a row; its Tasks are Pages"),
    "paper version": ("paper", "Block", None, "Jobs", "current", "rows", "jNN_v<N>_<venue>",
                      "a version = a row in Block › Jobs"),
    "cowork Job": ("cowork", "Block", None, "Jobs", "open", "rows", "jNN_<job>", "a row in Block › Jobs"),
    "DIKW level": ("insight", "Block", None, "Prototype", "Data", "rows", "Question N",
                  "a DIKW level = one view (Data) of Block › Prototype"),
    "design method": ("design", "Block", None, "Jobs", "Internal", "rows", "jNN_<goal>_by-insight",
                      "goal × method = a row, grouped by method family"),
    "labeling Job": ("labeling", "Block", None, "Jobs", "All", "rows", "jNN_<dataset>_<label>",
                     "a row, grouped by label; pick → its Job tab"),
    # Tasks: one row in Job › <its children>, under its group; pick it → the Task tab
    "work Task": ("task", "Job", None, "Tasks", "t0N", "rows", "tNN_<task>", "a row in Job › Tasks; pick → Task tab"),
    "Page Task": ("task", "Job", None, "Tasks", "t0N", "rows", "tNN_<task>", "a row; its Task tab = the Page"),
    "paper Section": ("paper", "Job", None, "Sections", "Main", "rows", "S-<desk>-<Section>",
                      "a row in Job › Sections, group Main"),
    "discovery Task": ("discovery", "Job", None, "Tasks", "All", "rows", "tNN_<task>", "a row in Job › Tasks"),
    "insight question": ("insight", "Block", None, "Insight", "Full", "rows", "Question N <question>",
                         "a row in Insight › Full; page and runs open in pop-outs"),
    "design folder": ("design", "Job", None, "Design folders", "All", "rows", "Design-NN-<slug>",
                      "a row; its Task tab = the design page"),
    "labeling Task": ("labeling", "Job", None, "Tasks", "label", "rows", "tNN_<dataset>_labeling",
                      "a row in Job › Tasks; its tab = today's labeling page"),
}


def short(s, n):
    return s if len(s) <= n else s[:n - 1] + "…"


def mini_map(x, y, w, h):
    """A drawing embedded in a list row, view only: a Section's map (excalidraw-section) in small, its
    paragraphs left to right, each with its evidence card."""
    base("rectangle", x, y, w, h, GRAY, 1)
    base("rectangle", x + 4, y + h / 2 - 3, 8, 6, INK, 1)                  # the Section
    for k in range(3):                                                      # its paragraphs, each a row
        ry = y + 3 + k * (h - 6) / 2
        path([(x + 12, y + h / 2), (x + 20, ry)], arrow=False, color=GRAY)
        path([(x + 20, ry), (x + w - 16, ry)], arrow=False, color=GRAY)
        base("rectangle", x + w - 13, ry - 2, 9, 4, INK, 1)                # its evidence card


# the files behind a Space, for the Disk part of the panel (JL 261008: "Disk and Runs in the same panel")
FACE = {"Guide": "SKILL.md · ref/", "Block": "bNN_<topic>.md", "Job": "jNN_<job>.md", "Task": "tNN_<task>.md"}
SPACE_DISK = {"Description": "related/", "Idea Studio": "studio/sNN-<topic>/", "Audience Report": "reports/qNN_<q>/",
              "Work Details": {"Block": "jNN_<job>/", "Job": "tNN_<task>/", "Task": "scripts/ · draft/"},
              "Runs": "runs/<run>/", "Delivery": "delivery/dNN-<name>/", "Overview": "src/ · sbatch/"}


def disk_runs(px, py, bottom, tab, space, runs):
    """The right panel as the frame draws it (JL 261008): Disk, the files behind the Space, one row each;
    then Runs, one row per button, named by the Run it makes (run-<type>-<target>, haipipe-run rule 6)
    with its words small under it. A button with no Run name yet stays in its words, red: open."""
    text(px, py, "Disk · Runs", 12, INK)
    where = SPACE_DISK.get(space, "")
    where = where.get(tab, "") if isinstance(where, dict) else where
    rows = [FACE.get(tab, "")] + ([where] if where and tab != "Guide" else [])
    yy = py + 20
    for r in rows:
        text(px, yy, "▫ " + short(r, 26), 10, GRAY, MONO)
        yy += 15
    text(px, yy + 3, "Runs", 11, INK)
    yy += 21
    fit = max(1, int((bottom - yy - 18) // 26))
    for r in runs[:fit]:
        name = run_names.name_of(r)
        known = run_names.named(r)
        text(px, yy, short(name if known else r + " ?", 27), 10, INK if known else RED, MONO if known else SANS)
        if known:
            text(px + 8, yy + 12, short(r.lstrip("+ "), 30), 8, GRAY)
        yy += 26
    if len(runs) > fit:
        text(px, yy - 4, f"+{len(runs) - fit} more", 10, GRAY)


QUESTION = re.compile(r"^(?:q(\d\d)|Question (\d+))(?: RQ\d)? (.+)$")


def question_of(cell):
    """(number, the rest) when a cell is a Question: "q01 <question>" or "Question 1 <question>"."""
    m = QUESTION.match(cell) if isinstance(cell, str) else None
    return (int(m.group(1) or m.group(2)), m.group(3)) if m else None


def question_cell(x, y, cell, w):
    """The Question cell as the frame draws it (s32, JL 261008): a label pill "Question N" with its state
    dot, then the short name (slug), and under them one concise sentence; no tags."""
    n, rest = question_of(cell)
    label = f"Question {n}"
    pw = len(label) * 5.6 + 22
    base("rectangle", x, y - 2, pw, 15, INK, 1, rough=0)
    text(x + 5, y, label, 9, INK)
    base("ellipse", x + pw - 11, y + 2, 6, 6, INK, 1, rough=0)["backgroundColor"] = INK   # the state dot
    text(x + pw + 6, y - 1, short("<slug>" if rest.startswith("<") else rest, max(6, int((w - pw) / 6.2))), 10,
         INK, MONO)
    text(x, y + 15, short("<one concise sentence: what it asks>", max(8, int(w / 5.2))), 9, GRAY)


# what today's decisions changed in every screen of s11 · s12 · s13 (JL 261008), listed once per drawing
CHANGES_261008 = ["✎ 261008 the right panel is Disk · Runs: the files behind the Space, then one row per Run button,",
                  "    named by the Run it makes (run-<type>-<target>), its words small under it; red ? = no Run name yet",
                  "✎ 261008 a Question cell: the label \"Question N\" with its state dot, the slug, one concise sentence; no tags",
                  "✎ 261008 an optional Space tab is a solid line, not dashed"]


def changes(lines, x=0, y=-300):
    """The dated green list of what changed in this drawing, above its title."""
    for k, ln in enumerate(lines):
        text(x, y + k * 30, ln, 20, GREEN)


def wireframe(x, y, spec, lines=None, runs=None, pick=None, header=None, groups=None, wrap=False):
    """Proposed: the level tabs, the level's subspaces below, the open list's groups below again, the
    content, the Run types panel. body "lines" draws the given content lines. Returns its bottom.
    wrap: a third row too long for one line goes on to a second one instead of ending in "…"."""
    family, tab, variant, open_sub, open_group, body, mark, caption = spec
    red = caption.endswith("?")
    text(x, y, header or f"on screen (proposed) · {family} · {tab} tab", 13, TEAL)
    y += 24
    base("rectangle", x, y, UI_W, UI_H, GRAY, 1)
    RUNS = 190

    def tabs(names, open_name, ty, h, size, gap, x0=x + 10, wrap=False):
        tx = x0
        for n in names:
            if n == "|":
                tx += 10
                continue
            optional = n.startswith("~")                 # an optional Space: a dashed tab
            n = n.lstrip("~")
            w = len(n) * size * 0.58 + 14
            if tx + w > x + UI_W - 10 and wrap:          # on to the next line
                tx, ty = x0, ty + h + 4
            elif tx + w > x + UI_W - 10:
                text(tx, ty + 3, "…", size, GRAY)
                break
            on = n == open_name
            base("rectangle", tx, ty, w, h, TEAL if on else GRAY, 1.5 if on else 1)   # optional: solid too (JL 261008)
            text(tx + 7, ty + (h - size * 1.25) / 2, n, size, TEAL if on else GRAY)
            tx += w + gap
        return ty

    tabs(LEVEL_TABS, tab + (" ▾" if tab in ("Job", "Task") else ""), y + 8, 24, 12, 6)       # the levels
    path([(x, y + 38), (x + UI_W, y + 38)], arrow=False, color=GRAY)
    tabs(level_subs(family, tab, variant), open_sub, y + 44, 20, 11, 4)                      # its parts
    path([(x, y + 70), (x + UI_W, y + 70)], arrow=False, color=GRAY)
    groups = subspace_row(family, tab, open_sub) if groups is None else groups   # [] = no third row
    top = y + 70
    if groups:                                                                    # its Subspaces
        gsize = 10 if sum(len(n) * 10 * 0.58 + 18 for n in groups) + 24 <= UI_W - 10 else 9   # a long row: smaller
        last = tabs(groups, open_group or groups[0], y + 76, 18, gsize, 4, x + 24, wrap)
        top = last + 24
        path([(x, top), (x + UI_W, top)], arrow=False, color=GRAY)
    path([(x + UI_W - RUNS, top), (x + UI_W - RUNS, y + UI_H)], arrow=False, color=GRAY)
    runs = runs or LEVEL_RUNS.get(tab) or task_runs(variant)
    disk_runs(x + UI_W - RUNS + 10, top + 8, y + UI_H, tab, open_sub, runs)
    bx, by, bw = x + 12, top + 10, UI_W - RUNS - 24          # the content, as placeholders
    hl = RED if red else TEAL
    if body == "studio":                                     # topics stacked; the open one is its drawing
        ty = by
        for k, (name, kind, meta) in enumerate(lines):
            if k == 0:
                text(bx, ty, "▾ " + " · ".join(s for s in (name, kind, meta) if s), 11, TEAL, MONO)
                cy = ty + 18
                base("rectangle", bx, cy, bw, 76, GRAY, 1)        # the live Excalidraw canvas
                for rx, ry_, rw, rh in [(14, 12, 74, 24), (128, 34, 84, 24), (250, 12, 74, 24)]:
                    base("rectangle", bx + rx, cy + ry_, rw, rh, INK, 1)
                path([(bx + 88, cy + 24), (bx + 128, cy + 44)], color=GRAY)
                path([(bx + 212, cy + 44), (bx + 250, cy + 26)], color=GRAY)
                text(bx + 8, cy + 60, "the drawing, live · marks kept", 10, GRAY)
                text(bx, cy + 82, "chat ▸ 3 sessions (Claude Code · Codex)", 11, GRAY)
                ty = cy + 104
            else:
                text(bx, ty, "▸ " + " · ".join(s for s in (name, kind, meta) if s), 11, GRAY, MONO)
                ty += 18
        if caption:
            text(x, y + UI_H + 10, caption, 13, RED if red else GRAY)
        return y + UI_H + 34
    if body == "preview":                                    # one Run opened: a preview of what it made
        name, kind, meta = lines[0]
        text(bx, by, f"▾ {name} · {kind} · {meta}", 11, TEAL, MONO)
        cy = by + 18
        base("rectangle", bx, cy, bw, 84, GRAY, 1)            # the result, as it looks
        for k in range(4):
            path([(bx + 12, cy + 14 + k * 13), (bx + bw - 150 - k * 30, cy + 14 + k * 13)], arrow=False, color=GRAY)
        base("rectangle", bx + bw - 120, cy + 10, 104, 58, GRAY, 1)      # a figure in it
        text(bx + 8, cy + 68, lines[1], 10, GRAY)
        for k, ln in enumerate(lines[2:]):
            text(bx, cy + 94 + k * 18, ln, 11, GRAY)
        if caption:
            text(x, y + UI_H + 10, caption, 13, RED if red else GRAY)
        return y + UI_H + 34
    if body in ("qwr", "table"):                             # rows under column heads; qwr = Question │ Work │ Report
        heads, rows = (("Question", "Work", "Report"), lines) if body == "qwr" else (lines[0], lines[1:])
        fracs = {3: [0.43, 0.32, 0.25], 4: [0.33, 0.30, 0.14, 0.23]}[len(heads)]
        xs, acc = [], bx
        for f_ in fracs:
            xs.append(acc)
            acc += bw * f_
        for cx_, head in zip(xs, heads):
            text(cx_ + 2, by, head, 12, INK)
        path([(bx, by + 18), (bx + bw, by + 18)], arrow=False, color=GRAY)
        qcell = any(question_of(r[0]) for r in rows)          # a Question row: label · slug · sentence (JL 261008)
        step = 36 if qcell else 26
        for k, row in enumerate(rows):
            ry_ = by + 26 + k * step
            if k == pick:
                base("rectangle", bx - 4, ry_ - 4, bw + 8, step - 4, TEAL, 1.5)
            for j, (cx_, cell, f_) in enumerate(zip(xs, row, fracs)):
                if j == 0 and question_of(cell):
                    question_cell(cx_ + 2, ry_, cell, bw * f_ - 8)
                    continue
                text(cx_ + 2, ry_, short(cell, max(6, int(bw * f_ / 6.8))), 11, TEAL if k == pick else GRAY,
                     MONO if cell[:1] in "qjtQ<" else SANS)
        for cx_ in xs[1:]:
            path([(cx_ - 4, by), (cx_ - 4, by + 26 + len(rows) * step)], arrow=False, color=INK)
        if caption:
            text(x, y + UI_H + 10, caption, 13, RED if red else GRAY)
        return y + UI_H + 34
    if body == "lines":                                      # a view filled with its content
        for k, ln in enumerate(lines):
            ly = by + k * 24
            if ln.endswith(" ▢"):                            # the row's own drawing, embedded (JL 261006)
                ln = ln[:-2]
                mini_map(bx + bw - 64, ly - 3, 60, 18)
            head = k == 0 or ln in ("its own", "from below")
            if k == pick:
                base("rectangle", bx - 4, ly - 4, bw + 8, 22, TEAL, 1.5)
            mono = not head and ("<" in ln or ln.startswith(("j0", "j1", "Q0", "QD", "QI", "QK", "RQ", "s0", "q0",
                                                             "▸ ", "▾ ", "    ", "d0")))   # indented: a child
            text(bx + (0 if head else 6), ly, ln, 12, TEAL if k == pick else INK if head else GRAY,
                 MONO if mono else SANS)
        if caption:
            text(x, y + UI_H + 10, caption, 13, RED if red else GRAY)
        return y + UI_H + 34
    if body == "card":
        base("rectangle", bx, by, bw, 60, hl, 1.5)
        text(bx + 10, by + 8, mark, 12, hl)
        for k in range(3):
            path([(bx + 10, by + 34 + k * 8), (bx + bw - 30 - k * 60, by + 34 + k * 8)], arrow=False, color=GRAY)
        for k in range(3):
            path([(bx, by + 80 + k * 22), (bx + bw - k * 70, by + 80 + k * 22)], arrow=False, color=GRAY)
    else:                                                    # rows: a list, one highlighted; runs: every Run
        n = 6 if body == "runs" else 5
        text(bx + 4, by, "every Run, newest first" if body == "runs" else f"{open_group or 'All'}", 11, GRAY)
        for k in range(n):
            ry = by + 20 + k * 20
            if k == 1:
                base("rectangle", bx, ry - 3, bw, 18, hl, 1.5)
                text(bx + 6, ry - 1, mark, 11, hl)
            else:
                path([(bx + 6, ry + 6), (bx + bw - 20, ry + 6)], arrow=False, color=GRAY)
    text(x, y + UI_H + 10, caption, 13, RED if red else GRAY)
    return y + UI_H + 34


# ── frame 2: every view of the Block tab, filled per family (placeholders, no project data) ────────
# frame 2: one screen per view of the Block tab: (column, Space, view); a family may leave a column out
BLOCK_COLUMNS = [("Guide", "Guide", None), ("Scope", "Description", "Scope"), ("People", "Description", "People"),
                 ("Resources", "Description", "Resources"), ("Related", "Description", "Related"),
                 ("Studio", "Idea Studio", None), ("Reports", "Audience Report", None),
                 ("Jobs", "Work Details", None), ("Runs", "Runs", None),
                 ("Preview", "Runs", None), ("Delivery", "Delivery", None)]
BLOCK_VIEW_NAMES = [c for c, _, _ in BLOCK_COLUMNS]
COLUMN_HEAD = {"Guide": "Guide · its own tab: the family's docs, as today",
               "Scope": "Block › Description › Scope (insight: Dataset)",
               "People": "Description › People (cowork) · Venue (paper)",
               "Resources": "Description › Resources", "Related": "Description › Related",
               "Studio": "Block › Idea Studio: one drawing after another (insight: RoadMap Draw)",
               "Reports": "Block › Audience Report (insight: Insight, by partition)",
               "Jobs": "Block › Work Details: Jobs, each open to its Tasks (insight: the 4 DIKW levels)",
               "Runs": "Block › Runs (optional): its own Runs; third row: their run types",
               "Preview": "Block › Runs › the picked Run: a preview of its result",
               "Delivery": "Block › Delivery (optional: a work Block's may be empty)"}
# insight fills the columns with today's views: column → (Space, view, content key)
FAMILY_COLUMNS = {"insight": {"Scope": ("Description", "Dataset", "Scope"),
                              "Studio": ("Idea Studio", None, "Prototype›RoadMap Draw"),
                              "Reports": ("Audience Report", "Full", "Insight"),
                              "Jobs": ("Work Details", None, "Levels"),
                              "Runs": ("Runs", None, "Runs"), "Preview": ("Runs", None, "Preview"),
                              "Delivery": ("Delivery", "Handoff", "Delivery")}}
# a note under a screen: what changed and what is open ("?" = open, in red)
FAMILY_CAPTIONS = {("paper", "Jobs"): "▢ = the Section's map (excalidraw-section), embedded, view only",
                   ("insight", "Jobs"):"was Prototype › Data · Information …: now each DIKW level's Job tab",
                   ("insight-reg", "Jobs"): "carry over: each register → a DIKW level Job ?",
                   # discovery (b14 Q01, 261007): where today's Discovery Views went
                   ("discovery", "Scope"): "was Scope › Block (its state, spine, close)",
                   ("discovery", "Studio"): "was Scope › RoadMap Draw",
                   ("discovery", "Reports"): "was Scope › Questions, Work › Questions, Check › Reports",
                   ("discovery", "Jobs"): "was Work › Tasks; its Papers moved into each Task",
                   ("discovery", "Runs"): "was Check › Runs: each level lists its own Runs",
                   ("discovery", "Delivery"): "was Delivery › Reports and BibTeX"}
VIEW_GAP = 50
BLOCK_FAMILY = {"work Block": "task", "discovery Block": "discovery", "cowork Block": "cowork",
                "paper Board": "paper", "insight Block (DIKW)": "insight", "insight register board": "insight-reg",
                "design Board": "design", "labeling Block": "labeling"}
KIND = {"task": "task-block", "discovery": "discovery-block", "cowork": "cowork-block", "paper": "paper-board",
        "insight": "insight-block", "insight-reg": "insight-board", "design": "design-board",
        "labeling": "labeling-block"}
# view -> (content lines, Runs buttons, highlighted line); the first line is the view's heading
VIEW_DEFAULT = {
    "Related": (["related/related.md: one row each, any kind", "★ paper  <author><year>  <short title>  doi  q01",
                 "  repo  <name>  <url>  to read", "  dataset · tool · project: the same row",
                 "pdf: only open-licensed, in related/", "a deep read: a discovery Task's Run, result/"],
                ["Add an item", "Find related work", "Check the list"]),
    "Guide": (["the family's docs (Tools), the same in every Block", "Description: what this family is for",
               "Method: how it asks, plans and answers", "RoadMap Draw: the workbench's own drawing",
               "Related Paper: <author><year> · …"], ["Add a method", "Add a paper"]),
    "Scope": (["bNN_<topic>.md", "kind: {kind}", "spine: the one line this Block answers", "covers: <topic> · <topic> · …",
               "excluded: <what it leaves to others>", "close: when it is done"],
              ["Update the Block status", "Edit the spine"]),
    "Resources": (["what the Block uses", "data: <store>/<asset>   read only", "code: code/<package>/…",
                   "links: <dashboard> · <doc>", "owner · reviewer"], ["Add a resource"]),
    "Studio": ([("s01-<topic>", "", "decided 4 · open 3"), ("s02-<topic>", "", "1 chat"),
                ("s03-question-map", "", "generated, view only")], ["+ Add topic", "Draw", "Keep this chat"]),
    "Reports": ([("q01 <question>", "j11 › t02 › r03", "answered"), ("q02 <question>", "j12 › t01", "draft"),
                 ("q03 <question>", "—", "asked")], ["Ask a Question", "Structure the report", "Draw the report",
                                                    "Check a report"], 0),
    "Jobs": (["Job · Task        Tasks  feeds  state   waits", "▾ j11_<job>       3/5    Q01    half    t02",
              "    t01_<task>                  done", "    t02_<task>                  check   2 days",
              "▸ j12_<job>       0/2    Q02    stale   30 days", "▸ j13_<job>       5/5    Q03    done"],
             ["Open a Job", "Update a Job"], 1),
    "Runs": ([("Run", "type", "writes", "state"), ("run-draw-s01", "Draw", "s01", "open · p03"),
              ("run-report-q02", "Write the report", "q02", "closed · p02"),
              ("run-check-q02", "Check a report", "q02", "waiting"),
              ("run-delivery-d01", "Build the report", "d01", "closed · p01")],
             ["Ask a Question", "Draw", "Write the report", "Check a report", "Build the report"], 1),
    "Delivery": (["its own: empty (optional for a work Block)", "from below", "j11 · t02     Report   released",
                  "j12 · t01     Report   web · LaTeX"], ["Build a delivery", "Release"]),
}
VIEW_FAMILY = {
    "task": {"Resources": (["what the Block uses", "data: _WorkSpace/<stage>Store/<asset>",
                            "code: code/<package>/ · haifn builders", "heavy: _WorkSpace/ProjectResult/…",
                            "owner · reviewer"], ["Add a resource"])},
    "discovery": {
        "Resources": (["where it searches", "channels: PubMed · arXiv · Semantic Scholar", "access: open · library proxy",
                       "seed papers: <author><year> · …"], ["Add a resource", "Add a paper"]),
        "Reports": ([("q01 <question>", "j01 › t01 · t02 · 10 papers", "answered"),
                     ("q02 <question>", "j02 › t01 · 4 papers", "draft"), ("q03 <question>", "—", "asked")],
                    ["Ask a Question", "Write the report", "Check a report"], 0),
        "Jobs": (["Job · Task           Tasks  papers  state", "▾ j01_<inquiry>      4/6    10      half",
                  "    t01_<sub-question>       6       done", "    t03_<sub-question>       2       check",
                  "▸ j02_<inquiry>      2/2    4       done", "pick a Job or a Task → its tab"],
                 ["Open a Job"], 1),
        "Runs": ([("Run", "type", "writes", "state"), ("run-draw-s01", "Draw", "s01", "open · p02"),
                  ("run-report-q01", "Write the report", "q01", "closed · p01"),
                  ("run-check-q01", "Check a report", "q01", "waiting"),
                  ("run-delivery-bib", "Export BibTeX", "d02", "closed · p04")],
                 ["Ask a Question", "Draw", "Write the report", "Verify a citation", "Check a report"], 1),
        "Delivery": (["dNN            type     what", "d01-<report>   Report   q01 · web",
                      "d02-<bib>      Export   <block>.bib · 42 entries", "from below",
                      "j01 · t03      Report   synthesis released"], ["Build a delivery", "Export BibTeX"])},
    "cowork": {
        "People": (["person      role       waiting on   since", "<person>    owner      —            —",
                    "<person>    reviewer   draft v2     3 days", "<person>    data       extract      1 week"],
                   ["Add a person"]),
        "Resources": (["what the Block uses", "threads: <thread>.md · …", "shared: <drive>/<folder>",
                       "meetings: notes/ · calendar"], ["Add a resource"]),
        "Jobs": (["Job        state     waiting on   next", "j11_<job>  open      <person>     send v2",
                  "j12_<job>  waiting   <person>     —", "j13_<job>  done      —            —",
                  "pick a Job → the Job tab"], ["Open a job", "Update a job"], 1),
        "Runs": ([("Run", "type", "writes", "state"), ("run-status-face", "Update the Block status", "face", "closed · p05"),
                  ("run-draw-s01", "Draw", "s01", "open · p01"),
                  ("run-report-q01", "Write the report", "q01", "closed · p02")],
                 ["Update the Block status", "Add a person", "Draw", "Write the report", "Check a report"], 0),
        "Delivery": (["dNN            type     what", "d01-<report>   Report   sent to <person>",
                      "from below", "j13_<job>      done"], ["Check a report"])},
    "paper": {
        "Scope": (["bNN_<topic>.md", "kind: paper-board", "claim: the one sentence the paper argues",
                   "venue: <venue> · deadline <date>", "authors: <a> · <b>", "close: accepted"], ["Update the Block status"]),
        "Venue": (["venues/: one folder per venue it writes for", "▾ <venue>   j02_v2   deadline <date>   open",
                   "    call.md: dates · limits · format · rules", "    kit/: the venue's author template",
                   "▸ <venue>   j01_v1   rejected: reviews → Rounds"], ["Add a venue", "Check the rules"], 1),
        "Resources": (["what the paper uses", "results: work/ · discovery/", "the venue's template: in Venue"],
                      ["Add a resource"]),
        "Related": (["related.md: the paper's related work", "★ paper  <author><year>  <short title>  S-2",
                     "  repo  <name>  <url>  to read", "reference.bib: built from its papers at Delivery",
                     "a deep read: a discovery Task's Run, result/"],
                    ["Add an item", "Find related work", "Check the list"]),
        "Studio": ([("s01-paper-flow", "", "the paper's flow, drawn"), ("s02-ideas", "", "one idea after another"),
                    ("s03-spine", "", "the story, drawn"), ("s04-figures", "", "the figure plan")],
                   ["Generate ideas", "Select idea", "Story revise", "Draw"]),
        "Reports": ([("q01 RQ1 <question>", "j02_v2 › S-Main-3", "answered"), ("q02 RQ2 <question>", "j02_v2 › S-Main-5", "draft"),
                     ("q03 RQ3 <question>", "—", "asked")], ["Ask a Question", "Draw the report"], 0),
        "Jobs": (["Version · Task             Tasks   state", "▸ j01_v1_<venue>           8/8     submitted",
                  "▾ j02_v2_<revision>        3/11    drafting", "    S-<desk>-1-<Section>           done ▢",
                  "    S-<desk>-2-<Section>           check ▢", "    tNN_cover_letter               draft",
                  "    tNN_rebuttal                   new"], ["Open a Job"], 2),
        "Runs": ([("Run", "type", "writes", "state"), ("run-story-spine", "Story revise", "face", "open · p06"),
                  ("run-claim-<claim>", "Claim review", "claims", "closed · p02"),
                  ("run-check-submit", "Check", "G4 · G5", "waiting"),
                  ("run-delivery-latex", "Build", "d01", "closed · p04")],
                 ["Story revise", "Claim review", "Check", "Build"], 2),
        "Delivery": (["dNN         group         made by", "d01-latex   LaTeX         run-delivery-latex",
                      "d02-word    Word          run-delivery-word", "d03-letter  Cover letter  j02 › tNN letter",
                      "d04-round1  Rounds        j02 › tNN rebuttal", "each one made by calling the Block's Runs"], ["Build", "Check"])},
    "insight": {   # today's Insight workbench, aligned: Scope · Prototype · Insight · Check · Delivery
        "Scope": (["dataset: <dataset> ▾ · one at a time", "the extract: rows · fields · <date>",
                   "meta/meta.md: what it is, no values", "Partitions: Full · <cut> · <cut> · Cross",
                   "Questions: 12 live · the Ask box"], ["Record the extract", "Ask"]),
        "Prototype": (["Data: the DIKW level's opening question · level.md", "▾ Question 1  <short question>",
                       "    chips: full · <cut> · script · signed", "▸ Question 2  <short question>",
                       "▸ Question 3  <short question>", "retired questions, folded"],
                      ["Carry a board over", "Register a cut", "Review the questions", "Plan the evidence",
                       "Review the evidence plan", "Write the script", "Review the script"]),
        "Levels": (["Level · Job        asked  needs  script  signed", "▾ j01_data        5      8      5       3",
                   "    t01_<question>   full · <cut>   ok", "    t02_<question>   full           open",
                   "▸ j02_information 4      6      3       1", "▸ j03_knowledge   3      4      1       0",
                   "▸ j04_wisdom      1      2      0       0"], ["Open a DIKW level", "Ask a Question"], 1),
        "Runs": ([("Run", "type", "writes", "state"), ("run-extract-<dataset>", "Record the extract", "meta/", "closed · p01"),
                  ("run-cut-<cut>", "Register a cut", "meta/", "closed · p02"),
                  ("run-map-questions", "Draw the question map", "studio/", "open · p03"),
                  ("run-carry-<board>", "Carry a board over", "j0N · tNN", "waiting")],
                 ["Record the extract", "Register a cut", "Draw the question map", "Carry a board over"], 2),
        "Prototype›RoadMap Draw": ([("question-map", "", "generated"),
                                    ("<drawing>", "", "Edit drawing"), ("<drawing>", "", "folded")],
                                   ["Draw the question map"]),
        "Insight": ([("Logic", "Work", "Report"), ("Question 1 <question>", "E1 → full · ok", "page <id>"),
                     ("Question 2 <question>", "E1 → full · ok", "page <id>"),
                     ("Question 4 <question>", "E2 → not bound", "No answer")],
                    ["Run a partition", "Write the Data report", "Write the Information report",
                     "Write the Knowledge report", "Check alignment", "Pool or split"], 0),
        "Check": (["the picked question's seven gates", "G1 asked · G2 planned · G3 run: open",
                   "Checks: cli/check.py", "Runtime: the workflow index", "a gate closes with its owner, not here"],
                  ["Review an answer"]),
        "Delivery": (["the signed Wisdom answers", "W01 <counsel>   signed: —   eligible: no",
                      "eligibility from owner receipts", "never granted here"],
                     ["Write the counsel", "Draft the handoff"])},
    "design": {
        "Scope": (["bNN_<topic>.md", "kind: design-board", "application: <app> · venue: <venue>",
                   "who: <audience> · their job", "authorizes: <N> design tasks", "close: every design verified"],
                  ["Update the Block status"]),
        "Resources": (["what the Board uses", "theories: Guide › Related Paper", "rules: 1-P-principle/ P01 · P02",
                       "insight handoff: <W-NN>"], ["Add a theory", "Add a resource"]),
        "Jobs": (["Job: goal × method          N    state", "▾ j01_<who>_by-insight      10   verify",
                  "    t01_d01_<slug>                passed", "    t02_d02_<slug>                revise",
                  "▸ j02_<who>_by-tailoring    10   passed", "▸ j03_<who>_by-precedent    —    new",
                  "pick a Job or a design → its tab"], ["Add a goal × method", "Open a Job"], 1),
        "Runs": ([("Run", "type", "writes", "state"), ("run-brief-tasks", "Add design tasks", "face", "closed · p02"),
                  ("run-rules-shared", "Set shared rules", "goal", "closed · p01"),
                  ("run-testplan-d02", "Plan the test", "d02", "open · p01")],
                 ["Add design tasks", "Set shared rules", "Add a method", "Plan the test"], 2),
        "Delivery": (["dNN            type     what", "d01-<designs>  Export   passed designs · designs.csv",
                      "d02-<plan>     Report   test plan · draft", "from below",
                      "Design-01      passed Verify"], ["Plan the test", "Passed review"])},
    "labeling": {
        "Scope": (["bNN_<topic>.md", "kind: labeling-block", "labels: <label> · <label>", "datasets: <dataset> · <dataset>",
                   "schema: per Job ? (b15 Q03)", "close: final labels audited"], ["Update the Block status"]),
        "Resources": (["what the Block uses", "LabelingStore/<dataset>/  (outside git)", "guideline: v<N> · gold: G<t>",
                       "models: registered weak executors"], ["Add a resource"]),
        "Jobs": (["Job · Task                 side      state", "▾ j01_<dataset>_<label>    Building  round 4",
                  "    t01_<dataset>_items             done", "    t03_<dataset>_labeling          G0 ✓ · round 4",
                  "▸ j02_<dataset2>_<label>   Scanning  reads j01's handoff",
                  "pick a Job or a Task → its tab"], ["Set up a Job"], 1),
        "Runs": ([("Run", "type", "writes", "state"), ("run-setup-j02", "Set up a Job", "j02", "closed · p01"),
                  ("run-delivery-d01", "Publish final labels", "d01", "open · p02")],
                 ["Set up a Job", "Ask a Question", "Publish final labels"], 1),
        "Delivery": (["dNN            type     what", "d01-<labels>   Export   final labels · <dataset>",
                      "from below", "j01 · t03      Handoff  label-v1 · signed",
                      "j01 · t04      Report   scored vs the keys"], ["Publish final labels"])},
}
VIEW_FAMILY["insight-reg"] = dict(VIEW_FAMILY["insight"])
VIEW_FAMILY["insight-reg"]["Scope"] = (["board.md (older) = the register", "kind: insight-board",
                                        "dataset: <Dataset> · one board per extract", "carry over, or keep ?"],
                                       ["Record the extract", "Ask"])
VIEW_FAMILY["insight-reg"]["Levels"] = (["0-MT-meta/ = its design", "MT01-MT04: the registers, D · I · K · W",
                                        "N-<partition>/: one folder per partition", "no DIKW level Jobs: carry over to get them"],
                                       ["Carry a board over"])
VIEW_FAMILY["insight-reg"]["Prototype"] = (["0-MT-meta/ = its design", "MT01-MT04: the question registers",
                                            "→ carry over to an Insight Block ?"], ["Carry a board over"])
VIEW_FAMILY["insight-reg"]["Insight"] = ([("Logic", "Work", "Report"), ("Question 1 <question>", "1-full/ ok", "page <id>"),
                                          ("Question 2 <question>", "2-<cut>/ ok", "page <id>"),
                                          ("carry over ?", "—", "—")], ["Run a partition"], None)


def block_dividers(x0, top, bottom):
    """The blockers (JL 261006): a line down the row before each group of Spaces, the same groups as
    the bars in the Spaces row: Guide | Description | Idea Studio · Audience Report | Work Details |
    Runs · Delivery."""
    groups, cur = [["Guide"]], []
    for s in BLOCK_SPACES:
        if s == "|":
            groups.append(cur)
            cur = []
        else:
            cur.append(s.lstrip("~"))
    groups.append(cur)
    group_of = {s: k for k, g in enumerate(groups) for s in g}
    last = None
    for i, (_, space, _) in enumerate(BLOCK_COLUMNS):
        if group_of.get(space, last) != last:
            gx = x0 + i * (UI_W + VIEW_GAP) - VIEW_GAP / 2
            path([(gx, top), (gx, bottom)], arrow=False, color=INK)
            last = group_of[space]


# (family key, column) -> (its third row, the open group): a drawing's own variant may set one (b11's
# "DIKW on the board" option opens Work Details on its DIKW levels)
BLOCK_ROWS = {}


def block_views(x, y, variant):
    """One screen per view of the Block tab, left to right; returns the bottom."""
    fam = BLOCK_FAMILY[variant]
    family = "insight" if fam.startswith("insight") else fam   # insight-reg, and b11's options
    cols = FAMILY_COLUMNS.get(family)
    bottom = y
    for i, (col, space, view) in enumerate(BLOCK_COLUMNS):
        tab, key = "Block", col
        if col == "Guide":                             # the Guide tab first, above today's Guide (JL 261006)
            tab, space = "Guide", "Description"
        elif cols is not None:                         # insight: today's views, each under the column doing that job
            if col not in cols:
                continue
            space, view, key = cols[col]
        elif col == "People" and fam == "paper":       # paper: this slot is its Venue (JL 261006)
            view = key = "Venue"
        elif col == "People" and fam != "cowork":
            continue                                   # only cowork has People
        if col == "Preview":                           # the picked Run, opened: what it made (JL 261006)
            rows, _, pick = VIEW_FAMILY.get(fam, {}).get("Runs") or VIEW_DEFAULT["Runs"]
            name, kind, writes, state = rows[1 + pick]
            lines = [(name, kind, state), f"what it made: {writes}, as it reads after its last pass",
                     "passes: p01 · p02, compare any two", "files: the ticket .md · run.yaml · passes/"]
            sp_ = (family, tab, None, space, kind, "preview", "", "")
            bottom = max(bottom, wireframe(x + i * (UI_W + VIEW_GAP), y, sp_, lines=lines,
                                           runs=["Open the result", "Run it again (a pass)", "Compare passes"],
                                           header=f"{variant} · {tab} › {space} › {name}"))
            continue
        spec = VIEW_FAMILY.get(fam, {}).get(key) or VIEW_DEFAULT[key]
        lines, runs = spec[0], spec[1]
        hl = spec[2] if len(spec) > 2 else None
        lines = [ln.replace("{kind}", KIND[fam]) if isinstance(ln, str) else ln for ln in lines]
        groups = JOB_GROUPS.get(family) or [None]
        open_group = view or (("j1N" if "j1N" in groups else groups[min(1, len(groups) - 1)])
                              if key == "Jobs" else None)
        body = {"Studio": "studio", "Reports": "qwr", "Prototype›RoadMap Draw": "studio",
                "Insight": "table", "Runs": "table"}.get(key, "lines")
        row = BLOCK_ROWS.get((fam, col))
        if row:
            open_group, view = row[1], row[1]
        sp_ = (family, tab, None, space, open_group, body, "", FAMILY_CAPTIONS.get((fam, col), ""))
        head = f"{variant} · {tab} › {space}" + (f" › {view}" if view else "")
        bottom = max(bottom, wireframe(x + i * (UI_W + VIEW_GAP), y, sp_, lines=lines, runs=runs, pick=hl,
                                       header=head, groups=row[0] if row else None))
    return bottom


if __name__ == "__main__":
    draw()
    canvas.write(Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent / "s01-overall-tree-structure.excalidraw",
                 els, "build_ladder_v4.py")
