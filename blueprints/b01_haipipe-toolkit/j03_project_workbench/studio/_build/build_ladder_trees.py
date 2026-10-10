"""b03 ladder trees: studio/ladder-trees.excalidraw, one folder tree per level, a definition per line.

A prototype for the skill design: generic placeholders only, black and gray, no project
content. Each level (Project, Theme, Block, reports/qNN, Job, Task, Run) gets its name, a
one-line definition, its folder tree with a gray definition beside every entry, and its open
questions. The layout follows the Block's two branches: the top row runs Project -> Theme ->
Block -> reports/qNN (the audience's branch); the work branch drops down from the Block,
Job -> Task -> Run. Each level is a rounded sketch box holding its folder name; labelled arrows
join the boxes (red dashed = open), routed around the trees; open questions are red.

Replies to the person's red comments are drawn in blue beside the comment (REPLIES).

Sources: haipipe-project ref/project-structure.md, haipipe-task SKILL.md and ref/hierarchy.md,
haipipe-question SKILL.md, haipipe-run SKILL.md. "?" lines are open, not settled.

    python build_ladder_trees.py [out.excalidraw]
"""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))  # canvas (haipipe-studio)
import canvas

random.seed(261007)
SANS, MONO = 6, 3
INK, GRAY, RULE, RED, BLUE = "#1e1e1e", "#868e96", "#495057", "#e03131", "#1971c2"
els = []
FRAME = [None]                                       # elements drawn while set belong to that frame

TREES = {  # level: (token, definition, [(tree line, its definition)], [open questions])
    "Space": ("", "the whole workspace: every Project and the shared tools", [
        ("<space>/", ""),
        ("├── examples*/", "groups of Projects"),
        ("│   └── <Project>/", "a Project"),
        ("├── Tools/", "skills, agents, servers"),
        ("├── platforms/", "shared code repos"),
        ("└── _WorkSpace/", "data stores, outside git"),
    ], ["today: SPACE Home lists every Board, by Project", "? a Space workbench: Projects -> Themes -> Blocks"]),
    "Project": ("", "one durable research or software boundary", [
        ("examples*/<Project>/", ""),
        ("├── README.md", "human entry: mission, entry points"),
        ("├── project.yaml", "id · profile · git_mode · state · mission"),
        ("├── tasks/", "Theme: computational work"),
        ("├── discoveries/", "Theme: external evidence"),
        ("├── cowork/", "Theme: coordination"),
        ("├── papers/", "Theme: academic output"),
        ("├── insights/", "Theme: Prototype + Instances"),
        ("├── designs/", "Theme: Design boards"),
        ("├── platforms/", "freestyle: owned code repos, no ladder"),
        ("└── external/", "freestyle: pinned upstream, no ladder"),
    ], ["a Theme is made lazily, on first use", "? one word for these six: Theme · World · Family · Area"]),
    "Theme": ("", "one kind of work: a folder of Blocks, owned by one skill", [
        ("<theme>/", ""),
        ("├── bNN_<topic>/", "a Block"),
        ("├── bNN_<topic>/", "a Block"),
        ("└── _old/", "archived Blocks"),
    ], ["no files of its own", "? the same Block naming in every Theme",
        "? does a Theme have its own workbench"]),
    "Block": ("bNN", "one topic: a board with two branches", [
        ("bNN_<topic>/", ""),
        ("├── board.md", "kind · spine · close · Questions register"),
        ("├── studio/", "drawings the whole Block shares"),
        ("├── reports/", "branch 1: for the audience"),
        ("│   └── qNN_<topic>/", "one Question, its report"),
        ("└── jNN_<job>/", "branch 2: the work"),
    ], ["no code, config, Ticket or Result at its root", "address starts here: bNN",
        "? which Themes keep both branches"]),
    "reports/qNN": ("qNN", "one Question for the audience; its report Page answers it", [
        ("qNN_<topic>/", ""),                      # lines keep their slots: the person's marks point at them
        ("├── qNN_<topic>.md", "the report: discussion + results"),
        ("├── page.toml", "keep: lets the workbench show it"),
        ("├── draft/", "free notes: the discussion, first"),
        ("├── qNN_<topic>.excalidraw", "one question, one drawing"),
        ("·   no runs/", "Runs live in J-T-R"),
        ("·   no results/", "cites them by address"),
    ], ["takes its evidence from Job, Task or Run", "header: answers: QNN · answer-status",
        "no BJTR address, no Runs of its own", "history: git, not writing Runs",
        "? can it cite work from another Block"]),
    "Job": ("jNN", "one line of work: a group of Tasks", [
        ("jNN_<job>/", ""),
        ("├── src/", "code shared by two or more Tasks"),
        ("├── tNN_<task>/", "a Task"),
        ("├── tNN_<task>/", "a Task"),
        ("└── sbatch/", "batch shared by two or more Tasks"),
    ], ["? a Job page jNN_<job>.md (cowork has one)", "? a Job's result store", "? a View, or its own workbench"]),
    "Task": ("tNN", "one bounded piece of work = a Page folder", [
        ("tNN_<task>/", ""),
        ("├── tNN_<task>.md", "the Page, for the reader"),
        ("├── draft/", "Page plan and records"),
        ("├── workflow/", "Plan / Report receipts"),
        ("├── scripts/", "workers + config/rNN_<run>.yaml"),
        ("├── runs/", "Tickets, one per Run"),
        ("├── results/", "generated Results"),
        ("├── notebooks/", "executed notebooks (generated)"),
        ("└── studio/", "the Page's drawings"),
    ], ["two faces: the work and the Page", "? which entries every Theme's Task keeps"]),
    "Run": ("rNN", "one commission with a close rule: an identity, not a folder", [
        ("rNN_<run>", ""),
        ("scripts/config/rNN_<run>.yaml", "frozen inputs"),
        ("runs/rNN_<run>.sh", "Ticket: what to do"),
        ("results/rNN_<run>/", "Result, light"),
        ("├── runtime.yaml", "receipt: status · times · run: = stem"),
        ("├── metrics.json · fig_*.png", "what the Run found"),
        ("└── heavy.yaml", "pointer to heavy output"),
        ("notebooks/rNN_<run>.ipynb", "executed notebook"),
        ("<ProjectResult>/…/rNN_<run>/", "heavy, outside git"),
    ], ["address: bNNjNNtNNrNN", "? one Ticket form for every Theme (.sh, .md, .yaml)"]),
}
# where each tree sits: the audience's branch along the top, the work branch down from the Block
COLW, NAME_W, BOX_W, BOX_H = 640, 250, 330, 56
PLACE = {"Space": (-1, 0), "Project": (0, 0), "Theme": (1, 0), "Block": (2, 0), "reports/qNN": (3, 0),
         "Job": (2, 1), "Task": (3, 1), "Run": (4, 1)}
EDGES = [  # (from, to, label, open?)
    ("Space", "Project", "lists Projects", False),
    ("Project", "Theme", "one folder per Theme", False),
    ("Theme", "Block", "holds Blocks", False),
    ("Block", "reports/qNN", "branch 1: the audience", False),
    ("Block", "Job", "branch 2: the work", False),
    ("Job", "Task", "groups Tasks", False),
    ("Task", "Run", "commissions Runs", False),
    ("reports/qNN", "Run", "cites Runs as evidence", False),
]
ROW_Y, LINE_H = [170, 900], 26


def base(kind, x, y, w, h, stroke=INK, sw=1, dashed=False, rough=0):
    e = {"id": f"t{len(els)}", "type": kind, "x": x, "y": y, "width": w, "height": h, "angle": 0,
         "strokeColor": stroke, "backgroundColor": "transparent", "fillStyle": "solid", "strokeWidth": sw,
         "strokeStyle": "dashed" if dashed else "solid", "roughness": rough, "opacity": 100, "groupIds": [],
         "frameId": FRAME[0], "roundness": None, "seed": random.randint(1, 2**31 - 1), "version": 1,
         "versionNonce": random.randint(1, 2**31 - 1), "isDeleted": False, "boundElements": [], "updated": 1,
         "link": None, "locked": False}
    els.append(e)
    return e


def text(x, y, s, size=16, color=INK, font=SANS):
    lines = s.split("\n")
    e = base("text", x, y, max(len(l) for l in lines) * size * (0.6 if font == MONO else 0.55),
             len(lines) * size * 1.25, color)
    e.update(text=s, originalText=s, fontSize=size, fontFamily=font, textAlign="left", verticalAlign="top",
             containerId=None, autoResize=True, lineHeight=1.25)


def arrow(pts, dashed=False, color=GRAY):
    """An arrow through the given points (an elbow when more than two)."""
    x0, y0 = pts[0]
    rel = [[px - x0, py - y0] for px, py in pts]
    e = base("arrow", x0, y0, max(abs(a) for a, _ in rel) or 1, max(abs(b) for _, b in rel) or 1, color, 1.5,
             dashed, 1)
    e.update(points=rel, lastCommittedPoint=None, startBinding=None, endBinding=None, startArrowhead=None,
             endArrowhead="arrow")


def box(x, y, label):
    e = base("rectangle", x, y, BOX_W, BOX_H, INK, 1.5, rough=1)
    e["roundness"] = {"type": 3}
    text(x + 18, y + 17, label, 18, INK, MONO)


REPLIES = [  # our answers to the person's red comments, in blue, beside the comment they answer
    ((430, 1165), "-> reply: yes, a Space workbench, one level above Project:\n"
                  "1  each Project folds open [-]\n"
                  "2  inside it, its Themes, each a row of Block cards\n"
                  "3  filter by Block kind: all · task · paper · discovery · design\n"
                  "4  a Block card opens that Block's workbench, /w/<block>\n\n"
                  "today: servers/space-home already finds every Board below the\n"
                  "root and groups them by Project (project.yaml), read-only.\n"
                  "missing: Themes inside a Project, the kind filter, the folds,\n"
                  "and Spaces with a Runs panel, so it is a Home, not a workbench.\n"
                  "drawn: the Space level, left of Project.\n\n"
                  "? Home grows into the Space workbench, or a new one beside it"),
    ((3080, 100), "-> reply: agreed. A report holds the discussion, not the work:\n"
                  "   qNN_<topic>.md           the report: Answer · Evidence · Limits · Next\n"
                  "   qNN_<topic>.excalidraw   one question, one drawing (replaces studio/)\n"
                  "   no runs/, no results/: it cites Job, Task or Run by address\n\n"
                  "updated: the qNN tree, line for line, so your marks still point right.\n"
                  "what this changes elsewhere:\n"
                  "   · haipipe-question puts a report's drawings in its studio/ (261004)\n"
                  "   · Page writing Runs (run-section-...) sit in reports/qNN/runs/ today\n\n"
                  "recommend: no writing Runs. The .md and the drawing are edited\n"
                  "directly and git keeps their history; only work that makes\n"
                  "evidence is a Run, and it lives in Job -> Task -> Run.\n"
                  "recommend: keep page.toml (the workbench needs it to show the\n"
                  "report)."),
    ((3720, 100), "-> a light Page: fixed skeleton, free prose (like the drawing)\n"
                  "1  draft/ takes in the discussion as free notes\n"
                  "2  the person, or an agent, folds them into the .md directly\n"
                  "3  four fixed headings; anything free goes under them\n"
                  "4  Evidence cites Job, Task or Run by address\n"
                  "5  a small check reads the shape: header lines + 4 headings\n"
                  "   (a check, not a Run; no versions, no realizes tags)"),
    ((3260, 1440), "-> reply: drawn below, one row per Theme, Job -> Task -> Run\n"
                   "under the trees above: each box says where it sits in that\n"
                   "Theme's workbench, each arrow the run that moves the work on,\n"
                   "and under Run every run type with its agent and skill.\n\n"
                   "what it shows: tasks/ and discoveries/ climb all three;\n"
                   "cowork/ stops at Job; papers/ has no Job level; insights/\n"
                   "runs live in the Instance; designs/ names Runs run-design-."),
]


LIGHT_PAGE = [  # header lines are haipipe-question's own; the four headings are its report divisions
    "# <the Question, as the audience asks it>",
    "answers: QNN",
    "answer-status: open | partial | answered",
    "results-read: <date the evidence was read>",
    "",
    "## Answer",
    "<two or three sentences>",
    "",
    "## Evidence",
    "- <what it shows>: bNNjNNtNNrNN or a path",
    "- the drawing: qNN_<topic>.excalidraw",
    "",
    "## Limits",
    "- <what this does not show>",
    "",
    "## Next",
    "- <the next question or work>",
]


def draw():
    text(0, 0, "Each level as a tree: what it holds, and what each part means", 40)
    text(0, 60, "Generic placeholders, from the haipipe-project, -task, -question and -run skills. "
                "Top row: the audience's branch. Down from the Block: the work. Red = open.", 18, GRAY)
    boxes = {}
    for lvl, (token, definition, tree, opens) in TREES.items():
        cx, row = PLACE[lvl]
        x, y = cx * COLW, ROW_Y[row]
        text(x, y, lvl + (f"   {token}" if token else ""), 26)
        box(x, y + 40, tree[0][0])
        boxes[lvl] = (x, y + 40)
        text(x, y + 40 + BOX_H + 12, definition, 16, GRAY)
        ty = y + 40 + BOX_H + 50
        name_w = max(NAME_W, max(len(l) for l, _ in tree[1:]) * 15 * 0.6 + 18)
        for line, meaning in tree[1:]:
            text(x, ty, line, 15, INK, MONO)
            if meaning:
                text(x + name_w, ty + 1, meaning, 14, GRAY)
            ty += LINE_H
        ty += 14
        for o in opens:
            text(x, ty, o, 15, RED if o.startswith("?") else GRAY)
            ty += 22
    for a, b, label, is_open in EDGES:
        (ax, ay), (bx, by) = boxes[a], boxes[b]
        color = RED if is_open else GRAY
        if ay == by:                                           # same row: box edge to box edge
            pts = [(ax + BOX_W + 6, ay + BOX_H / 2), (bx - 8, by + BOX_H / 2)]
            lx, ly = ax + BOX_W + 20, ay + BOX_H / 2 - 24
        elif bx == ax:                                         # straight down, along the left margin
            pts = [(ax - 6, ay + BOX_H / 2), (ax - 34, ay + BOX_H / 2), (ax - 34, by + BOX_H / 2), (bx - 8, by + BOX_H / 2)]
            lx, ly = ax - 30 - len(label) * 14 * 0.55 - 10, (ay + by) / 2
        else:                                                  # over the empty corner, then down
            mx = bx + BOX_W / 2
            pts = [(ax + BOX_W + 6, ay + BOX_H / 2), (mx, ay + BOX_H / 2), (mx, by - 8)]
            lx, ly = mx + 12, (ay + by) / 2
        arrow(pts, dashed=is_open, color=color)
        text(lx, ly, label, 14, color)
    for (x, y), body in REPLIES:
        text(x, y, body, 16, BLUE)
    sx, sy = 3720, 300
    text(sx, sy, "qNN_<topic>.md  ·  the light Page", 18, INK)
    for i, ln in enumerate(LIGHT_PAGE):
        if ln:                             # Excalidraw drops empty text, so draw none
            text(sx, sy + 34 + i * 19, ln, 14, INK if ln.startswith(("#", "answers", "answer-", "results")) else GRAY, MONO)
    draw_flows()
    draw_v2()


# ── per Theme: Job -> Task -> Run as a workflow, under the trees, with workbench place and runs ──
# From each family's ref/workbench-table.md (Level · Space › View · Run type · Agent · Skill).
# Names drop the "haipipe-" prefix. A row: (theme, its workbench, [Job, Task, Run boxes],
# [Job->Task label, Task->Run label], [run type — agent · skill], open question)
FLOWS = [
    ("tasks/", "board /w/<block>: Scope · Task · Check · Delivery",
     [("jNN_<job>/", "board › Task › a View per Job"), ("tNN_<task>/", "board › Task · Check › Tasks"),
      ("rNN_<run>.sh", "results/ under the Task")],
     ["Plan · Build a Task", "Run a Task"],
     ["Plan a Task — task-creator-agent · task-plan (new)", "Build the Task — task-creator-agent · task-plan (new)",
      "Run a Task — task-orchestrator-agent · task-run (new)", "Report the Run — task-creator-agent · task-plan (new)",
      "Check a Task — task-reviewer-agent · task-audit (new)"], ""),
    ("discoveries/", "board: Scope · Work · Check",
     [("jNN_<inquiry>/", "board › Work › Tasks"), ("tNN_<task>/", "board › Work › Tasks"),
      ("rNN_<paper>.sh", "one paper or source per Run")],
     ["Synthesize a Task", "Read a paper"],
     ["Find papers — discovery-search-worker-agent · discovery-search",
      "Read a paper — discovery-creator-agent · discovery-review",
      "Review a Run — discovery-reviewer-agent · discovery-review",
      "Verify a citation — discovery-reviewer-agent · discovery-search"], ""),
    ("cowork/", "board: Scope · Work · Check",
     [("jNN_<job>/ + .md", "board › Work › Jobs"), ("no Task", "by rule"), ("no Run", "writes the Job's files")],
     ["", ""],
     ["Open · Update a job — cowork-agent (new) · cowork", "Draft an email — cowork-agent (new) · writing",
      "Write meeting notes — cowork-agent (new) · cowork"], "? are these Runs with no Run level"),
    ("papers/", "board: Ideation · Story · Sections · Delivery",
     [("<part>/  Ba- Bb-", "? no Job level in the skill"), ("<Section Page>/", "board › Sections · page workbench"),
      ("run-section-…", "Draft · Evidence · Delivery")],
     ["?", "Draft runs · Evidence runs"],
     ["Draft runs — page-writing-agent · paper-section", "Evidence runs — page-evidence-agent · page-evidence",
      "Page check — page-check-agent · page-check"], "? Task and Discovery runs go to tasks/ and discoveries/"),
    ("insights/", "board: Scope · Prototype · Insight · Check · Delivery",
     [("<level>/  1-Data…4-Wisdom", "board › Prototype › D · I · K · W"), ("<q>/  a question", "Prototype · Insight › each partition"),
      ("<partition> run", "in the Instance, not the Task")],
     ["Plan the evidence", "Run a partition"],
     ["Plan the evidence — insight-agent · insight-evidence-plan", "Write the script — task-creator-agent · insight",
      "Run a partition — task-orchestrator-agent · insight", "Check alignment — insight-reviewer-agent · insight-check"],
     "? should the Run sit under its question folder"),
    ("designs/", "board: Design Tasks · page: Design Task · Item · Delivery",
     [("<stage>/  2-Design", "board › Design Tasks › Task list"), ("Design-NN-<slug>/", "page workbench: Task · Item"),
      ("run-design-<op>-…", "results/ under the Design")],
     ["Add design tasks", "Commission · Generate"],
     ["Commission — designer-agent · design-commission (new)", "Generate — designer-agent · design-unit",
      "Verify — design-reviewer-agent (new) · design-unit"], "? contract says rdNN_<op>_<slug>"),
]
FLOW_Y, FLOW_H = 2240, 330


def draw_flows():
    x_theme, cols = COLW * 1, [COLW * 2, COLW * 3, COLW * 4]          # under Theme, Job, Task, Run
    text(x_theme, FLOW_Y - 90, "Each Theme down Job -> Task -> Run: where it sits in its workbench, what runs it", 30)
    text(x_theme, FLOW_Y - 46, "From each family's ref/workbench-table.md. Under Run: run type — agent · skill "
                               "(names without haipipe-). Red = open.", 16, GRAY)
    for k, (theme, bench, boxes, labels, runs, open_q) in enumerate(FLOWS):
        y = FLOW_Y + k * FLOW_H
        box(x_theme, y, theme)
        text(x_theme, y + BOX_H + 10, bench, 14, GRAY)
        if open_q:
            text(x_theme, y + BOX_H + 34, open_q, 14, RED)
        arrow([(x_theme + BOX_W + 6, y + BOX_H / 2), (cols[0] - 8, y + BOX_H / 2)])
        for i, ((label, where), x) in enumerate(zip(boxes, cols)):
            absent = label.startswith("no ")
            b = base("rectangle", x, y, BOX_W, BOX_H, GRAY if absent else INK, 1.5, absent, 1)
            b["roundness"] = {"type": 3}
            text(x + 18, y + 17, label, 18, GRAY if absent else INK, MONO)
            text(x, y + BOX_H + 10, where, 14, RED if where.startswith("?") else GRAY)
            if i < 2:
                lab = labels[i]
                arrow([(x + BOX_W + 6, y + BOX_H / 2), (cols[i + 1] - 8, y + BOX_H / 2)],
                      dashed=lab.startswith("?") or absent, color=RED if lab.startswith("?") else GRAY)
                if lab:
                    text(x + BOX_W + 16, y + BOX_H / 2 - 22, lab, 13, RED if lab.startswith("?") else GRAY)
        rx = cols[2] if not boxes[2][0].startswith("no ") else cols[0]
        for j, r in enumerate(runs):
            text(rx, y + BOX_H + 36 + 19 * j, r, 13, INK)


# ── frame v2 · a Block holds only Jobs: studio, questions and work (JL 261006) ───────────────
# The person's own arrangement of the canvas stays as it is; v2 is drawn fresh in its own frame.
V2_X, V2_Y = 5600, 0
V2_TOP = [  # (heading, box, definition, [(line, meaning)], [open]); a tree lists only the level's own
            # files: its children are the next box, never a line here (JL 261006)
    ("Space", "<space>/", "the whole workspace", [
        ("├── Tools/", "skills, agents, servers"), ("└── _WorkSpace/", "data, outside git")],
     ["Projects sit in examples*/"]),
    ("Project", "<Project>/", "one research or software boundary", [
        ("├── README.md", "human entry"), ("├── project.yaml", "id · profile · state"),
        ("└── platforms/ external/", "freestyle, no ladder")], []),
    ("Theme", "<theme>/", "one kind of work, one skill family", [
        ("└── _old/", "archived Blocks")], ["? Theme · Family · Area"]),
    ("Block   bNN", "bNN_<topic>/", "one topic: a board and its Jobs", [
        ("└── board.md", "kind · spine · close · Questions")],
     ["its Jobs are its subfolders: next level", "? reserved names, or numbered (j00_people style)"]),
]
V2_ROWS = [  # (row, [(box, definition, [(line, meaning)], absent?) for Job, Task, Run], [arrow labels])
    ("studio", [
        ("studio/", "special Job: the Block's drawings", [], False),
        ("<name>.excalidraw", "one drawing, edited on the canvas", [
            ("_build/<name>.py", "optional seed script"), ("person's marks", "always kept")], False),
        ("no Run", "drawn, not run", [], True)],
     ["holds drawings", ""]),
    ("questions", [
        ("reports/", "special Job: the audience's Questions", [], False),
        ("qNN_<topic>/", "one Question = a light Page", [
            ("├── qNN_<topic>.md", "Answer · Evidence · Limits · Next"),
            ("├── qNN_<topic>.excalidraw", "its one drawing"),
            ("├── draft/", "free notes, the discussion"),
            ("└── page.toml", "lets the workbench show it")], False),
        ("no Run", "history is git", [], True)],
     ["one per Question", ""]),
    ("work", [
        ("jNN_<job>/", "a work Job: Tasks with one goal", [
            ("├── jNN_<job>.md", "? its face: goal, state, next"),
            ("├── src/", "code shared by Tasks"), ("└── sbatch/", "shared batch")], False),
        ("tNN_<task>/", "one bounded piece of work = a Page", [
            ("├── tNN_<task>.md", "the Page"), ("├── scripts/", "workers + config"),
            ("├── runs/", "Tickets"), ("├── results/", "Results"), ("├── notebooks/", "executed notebooks"),
            ("└── studio/   plugin", "optional: chat/ · draw/")], False),
        ("rNN_<run>", "one commission, one identity", [
            ("config/rNN_<run>.yaml", "frozen inputs"), ("runs/rNN_<run>.sh", "Ticket"),
            ("results/rNN_<run>/", "Result + runtime.yaml"), ("<ProjectResult>/…", "heavy, outside git")], False)],
     ["groups Tasks", "commissions Runs"]),
    ("page", [
        ("jNN_<job>/", "any Job that holds Pages", [], False),
        ("tNN_<task>/", "a Task whose Page leads: a writing Page", [
            ("├── tNN_<task>.md", "Opening · Content, the reader's"),
            ("├── page.toml", "registers the Page"),
            ("├── draft/", "the plan <stem>-draft-v<G>.<S>.md"),
            ("│   ├── <stem>-evidence-items.md", "Citations · Displays · Values"),
            ("│   ├── records/", "context · feedback · log"),
            ("│   └── previous/", "superseded plans"),
            ("├── workflow/", "machine receipts"),
            ("├── runs/ · results/", "Page Runs and their Results"),
            ("├── delivery/", "web · latex · word · slide"),
            ("└── studio/   plugin", "chat/ · draw/: the person's room")], False),
        ("run-<kind>-<MMDD>-<slug>", "a Page Run: plan, write, evidence", [
            ("run-structure-…", "the plan"), ("run-section-…", "a writing session"),
            ("re-<kind>-NN_<slug>", "one Evidence Item"), ("run-delivery-<lane>", "one build per lane")], False)],
     ["holds Pages", "Page Runs"]),
    ("paper", [
        ("Ba-<desk>-Main/", "a paper part: Story · Main · Appendix · Round", [], False),
        ("S-<desk>-<Section>/", "one Section = a Page", [
            ("├── S-<desk>-<Section>.md", "the Section's text"),
            ("├── draft/", "plan + evidence items"),
            ("├── runs/ · results/", "writing and evidence Runs"),
            ("├── delivery/latex/", "its LaTeX fragment"),
            ("└── studio/   plugin", "chat/ · draw/: logic tree"),
            ("evidence comes from", "tasks/ · discoveries/ Results")], False),
        ("run-section-<MMDD>-<slug>", "a writing session on one Section", [
            ("run-structure-…", "the Section's plan"), ("re-<kind>-NN_<slug>", "one Evidence Item"),
            ("run-delivery-<lane>", "its build")], False)],
     ["holds Sections", "writing Runs"]),
]


LEVEL_PATTERN = [
    "level   its face            its drawing             its extras                      its children",
    "Block   board.md            studio/ (its topics)    reports/: Questions, audience   jNN_<job>/",
    "Job     jNN_<job>.md ?      none                    src/ · sbatch/: shared by Tasks tNN_<task>/",
    "Task    tNN_<task>.md       studio/ plugin, if any  scripts/: workers + config      rNN_<run>",
    "",
    "drawings live only in a studio/ (the Block's topics, or a Task's plugin) and in reports/qNN/",
    "",
    "Questions stay at the Block: a Job feeds them through the register's work: line,",
    "so it needs no reports/ of its own.",
    "",
    "plugins: optional folders that add a room without changing what a folder is",
    "   studio/  chat/ · draw/   on a Block (its topics) or on one Task or Page",
    "   sbatch/  batch jobs      on a Job (shared) or on one Task",
    "   delivery/ builds         on a Page, or on a paper's Block (the whole paper)",
]


def v2_node(x, y, heading, label, definition, tree, opens, absent=False):
    if heading:
        text(x, y, heading, 26)
    by = y + 40
    b = base("rectangle", x, by, BOX_W, BOX_H, GRAY if absent else INK, 1.5, absent, 1)
    b["roundness"] = {"type": 3}
    text(x + 18, by + 17, label, 18, GRAY if absent else INK, MONO)
    text(x, by + BOX_H + 12, definition, 16, GRAY)
    ty = by + BOX_H + 46
    name_w = max(220, max([len(l) for l, _ in tree] or [0]) * 15 * 0.6 + 18)
    for line, meaning in tree:
        text(x, ty, line, 15, INK, MONO)
        text(x + name_w, ty + 1, meaning, 14, RED if meaning.startswith("?") else GRAY)
        ty += LINE_H
    for o in opens:
        text(x, ty + 8, o, 15, RED if o.startswith("?") else GRAY)
        ty += 22
    return by                                                     # the box's top


def draw_v2():
    X, Y = V2_X, V2_Y
    FRAME[0] = None
    fr = base("frame", X - 60, Y - 60, 7 * COLW + 300, 3560, RULE)
    fr["name"] = "The ladder v2: a Block holds only Jobs"
    FRAME[0] = fr["id"]
    text(X, Y, "The ladder, v2: a Block holds only Jobs (studio, questions, work)", 40)
    text(X, Y + 58, "Special Jobs have reserved names and no Runs; cowork's j00_people is one already. "
                    "Generic placeholders. Red = open.", 18, GRAY)
    tops = []
    for i, (h, label, definition, tree, opens) in enumerate(V2_TOP):
        tops.append(v2_node(X + i * COLW, Y + 170, h, label, definition, tree, opens))
    for i in range(len(tops) - 1):
        lab = ["lists Projects", "one folder per Theme", "holds Blocks"][i]
        ax, by = X + i * COLW, tops[i]
        arrow([(ax + BOX_W + 6, by + BOX_H / 2), (ax + COLW - 8, by + BOX_H / 2)])
        text(ax + BOX_W + 18, by + BOX_H / 2 - 24, lab, 14, GRAY)
    # the Block's three branches, one row each, down a trunk on the Block's left
    bx, bby = X + 3 * COLW, tops[3]
    cols = [bx + COLW, bx + 2 * COLW, bx + 3 * COLW]               # one step right: Jobs are subfolders
    row_y = [Y + 720, Y + 1180, Y + 1680, Y + 2260, Y + 2880]
    for c, name in zip(cols, ["Job level   jNN", "Task level   tNN", "Run level   rNN"]):
        text(c, row_y[0] - 70, name, 22, GRAY)
    run_box = None
    for r, ((row, nodes, labels), ry) in enumerate(zip(V2_ROWS, row_y)):
        trunk_x = bx - 30                                          # down the Block's left edge, then right
        arrow([(bx - 6, bby + BOX_H - 12), (trunk_x, bby + BOX_H - 12), (trunk_x, ry + 40 + BOX_H / 2),
               (cols[0] - 8, ry + 40 + BOX_H / 2)])
        text(trunk_x + 16, ry + 40 + BOX_H / 2 - 24, row, 15, GRAY)
        boxes = []
        for c, (label, definition, tree, absent) in zip(cols, nodes):
            boxes.append(v2_node(c, ry, "", label, definition, tree, [], absent))
        for i in range(2):
            absent = nodes[i + 1][3]
            arrow([(cols[i] + BOX_W + 6, boxes[i] + BOX_H / 2), (cols[i + 1] - 8, boxes[i + 1] + BOX_H / 2)],
                  dashed=absent)
            if labels[i]:
                text(cols[i] + BOX_W + 18, boxes[i] + BOX_H / 2 - 24, labels[i], 14, GRAY)
        if row == "work":
            run_box = boxes[2]
        if row == "questions":
            q_box = boxes[1]
    # a Question cites the work's Runs: around the right of the Run column
    rx = cols[2] + BOX_W + 50
    arrow([(cols[1] + BOX_W + 6, q_box + BOX_H + 6), (rx, q_box + BOX_H + 6), (rx, run_box + BOX_H / 2),
           (cols[2] + BOX_W + 8, run_box + BOX_H / 2)], dashed=True, color=RED)
    text(rx + 12, (q_box + run_box) / 2, "cites as evidence\n(a Job, Task or Run)", 14, RED)
    text(bx, Y + 3420, "? keep the folder names studio/ and reports/, or number them like j00_people",
         16, RED)
    # the same three at every level: a face, what its children share, its children
    text(X, Y + 1560, "the same three at every folder level", 22)
    for i, ln in enumerate(LEVEL_PATTERN):
        text(X, Y + 1604 + i * 22, ln, 15, INK if i == 0 else GRAY, MONO)
    FRAME[0] = None


if __name__ == "__main__":
    draw()
    canvas.write(Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / "ladder-trees.excalidraw",
                 els, "build_ladder_trees.py", redraw_frames=("The ladder v2: a Block holds only Jobs",))
