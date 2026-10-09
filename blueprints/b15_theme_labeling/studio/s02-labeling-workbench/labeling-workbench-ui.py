"""Build labeling-workbench-ui.excalidraw, the Labeling workbench design drawing (Guide › RoadMap Draw).

The drawing is generated: change this file, then run it (never edit the .excalidraw by hand):

    python3 blueprints/b15_theme_labeling/studio/s02-labeling-workbench/labeling-workbench-ui.py   (from Tools/)

It follows the Insight workbench drawing (blueprints/b11_theme_insight/studio/s02-insight-workbench/):
same sizes, colours and grammar, four named frames.

1 · Spaces, runs and skills   the four working Spaces, their Views, the Run types of each View
                              in step order with their agent and skill, read from
                              workbench-labeling/ref/workbench-table.md; unbuilt ones grey.
2 · The workbench             each Space as the page shows it: the header, the Space row, its
                              View tabs, the Space's brief, one View's content, the Runs panel.
3 · Every View                all twelve Views, block by block, and the steps each one lists.
4 · Where things live         what each Space reads, the one write door, and the rules.

The Space and View names come from labeling.py's SPACES and the Run types from the Workbench
Table, so a renamed View or a new Run type redraws on the next run. The example job in
Part 2 is made up; the drawing names no real job, item or person.
"""
import ast
import json
import random
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "labeling-workbench-ui.excalidraw"
TOOLKIT = HERE.parents[3] / "plugins" / "haipipe-toolkit"   # moved to b15_theme_labeling (261007)
SKILL = TOOLKIT / "skills" / "2_theme" / "labeling" / "workbench-labeling"
MAPPING = TOOLKIT / "skills" / "2_theme" / "labeling" / "haipipe-labeling-building" / "ref" / "ref-space-mapping.md"
random.seed(261003)
NOW = 0  # a fixed stamp keeps the generated file stable between runs
E = []

BLUE, GREEN, INK, MUTED, RULE, PANEL, ORANGE = "#1864ab", "#2b8a3e", "#1e1e1e", "#495057", "#ced4da", "#f8f9fa", "#e8590c"


# ---- drawing pieces (the Insight drawing's grammar) ----------------------------------------
def base(id_, type_, x, y, w, h, stroke=INK, bg="transparent", dashed=False, rounded=True):
    return {"id": id_, "type": type_, "x": x, "y": y, "width": w, "height": h, "angle": 0,
            "strokeColor": stroke, "backgroundColor": bg, "fillStyle": "solid", "strokeWidth": 2,
            "strokeStyle": "dashed" if dashed else "solid", "roughness": 0, "opacity": 100,
            "groupIds": [], "frameId": None, "roundness": {"type": 3} if rounded else None,
            "seed": random.randint(1, 2**31 - 1), "version": 1,
            "versionNonce": random.randint(1, 2**31 - 1), "isDeleted": False,
            "boundElements": [], "updated": NOW, "link": None, "locked": False}


def text(id_, x, y, s, size=16, color=INK, mono=False):
    lines = s.split("\n")
    w = max(len(l) for l in lines) * size * (0.6 if mono else 0.56)
    e = base(id_, "text", x, y, w, len(lines) * size * 1.25, stroke=color, rounded=False)
    e.update(text=s, originalText=s, fontSize=size, fontFamily=3 if mono else 8,
             textAlign="left", verticalAlign="top", containerId=None, autoResize=True, lineHeight=1.25)
    E.append(e)
    return e


def rect(id_, x, y, w, h, stroke=INK, bg="transparent", dashed=False):
    E.append(base(id_, "rectangle", x, y, w, h, stroke, bg, dashed))
    return E[-1]


def button(id_, x, y, w, h, label, sel=False, size=17, dashed=False, muted=False):
    stroke = MUTED if muted else (BLUE if sel else INK)
    r = rect(id_, x, y, w, h, stroke, "#e7f5ff" if sel else "transparent", dashed)
    tw, th = len(label) * size * 0.56, size * 1.25
    t = base(id_ + "-text", "text", x + (w - tw) / 2, y + (h - th) / 2, tw, th, stroke=stroke, rounded=False)
    t.update(text=label, originalText=label, fontSize=size, fontFamily=8, textAlign="center",
             verticalAlign="middle", containerId=id_, autoResize=True, lineHeight=1.25)
    r["boundElements"] = [{"id": id_ + "-text", "type": "text"}]
    E.append(t)


def line(id_, x, y, w, color=RULE):
    e = base(id_, "line", x, y, w, 0, stroke=color, rounded=False)
    e.update(points=[[0, 0], [w, 0]], lastCommittedPoint=None, startBinding=None, endBinding=None,
             startArrowhead=None, endArrowhead=None)
    E.append(e)


def arrow(id_, x, y, points, color):
    e = base(id_, "arrow", x, y, max(abs(p[0]) for p in points), max(abs(p[1]) for p in points),
             stroke=color, rounded=False)
    e.update(points=points, lastCommittedPoint=None, startBinding=None, endBinding=None,
             startArrowhead=None, endArrowhead="arrow", elbowed=False)
    E.append(e)


def chips(key, x, y, labels, sel, size=16, h=40):
    """A row of buttons, each as wide as its label (Space row, View tabs)."""
    for n, label in enumerate(labels):
        w = max(80, int(len(label) * size * 0.56) + 30)
        button(f"{key}-{n}", x, y, w, h, label, sel=n == sel, size=size)
        x += w + 8
    return x


def kv(key, x, y, rows, lw=170, w=520, size=13):
    """Label/value rows as a two-column table with a shaded label cell."""
    h = 28
    for n, (k, v) in enumerate(rows):
        rect(f"{key}-k{n}", x, y + n * h, lw, h, RULE, PANEL)
        rect(f"{key}-v{n}", x + lw, y + n * h, w - lw, h, RULE)
        text(f"{key}-kt{n}", x + 8, y + n * h + 7, k, size - 1, MUTED)
        text(f"{key}-vt{n}", x + lw + 8, y + n * h + 7, v, size)
    return y + len(rows) * h


def wrap(cell, width, size):
    """Break a cell's words so each line fits `width` pixels at `size`."""
    limit = max(4, int((width - 12) / (size * 0.56)))
    lines, cur = [], ""
    for word in cell.split():
        if cur and len(cur) + 1 + len(word) > limit:
            lines.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}".strip()
    return "\n".join(lines + [cur])


def grid(key, x, y, head, rows, widths, size=12):
    """A table: a shaded header row, then rows; `widths` per column; long cells wrap."""
    for r, cells in enumerate([head] + rows):
        wrapped = [wrap(cell, widths[c], size) for c, cell in enumerate(cells)]
        h = 12 + max(t.count("\n") + 1 for t in wrapped) * size * 1.25
        cx = x
        for c, cell in enumerate(wrapped):
            rect(f"{key}-r{r}c{c}", cx, y, widths[c], h, RULE, PANEL if r == 0 else "transparent")
            text(f"{key}-t{r}c{c}", cx + 6, y + 6, cell, size - (1 if r == 0 else 0), MUTED if r == 0 else INK)
            cx += widths[c]
        y += h
    return y


def brief(key, x, y, facts):
    """A Space's brief: label over value, left to right."""
    for n, (k, v) in enumerate(facts):
        text(f"{key}-bk{n}", x, y, k.upper(), 11, MUTED)
        text(f"{key}-bv{n}", x, y + 16, v, 15, GREEN if v in ("confirmed", "valid", "frozen") else INK)
        x += max(len(k) * 11 * 0.6, len(v) * 15 * 0.56) + 30


# ---- the facts the drawing reads ------------------------------------------------------------
def presenter_spaces():
    """[(Space, [View, ...]), ...] from labeling.py's SPACES."""
    tree = ast.parse((TOOLKIT / "servers" / "workbench-labeling" / "labeling.py").read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "SPACES":
            return [(name, [label for _, label in views]) for _, name, views in ast.literal_eval(node.value)]
    raise SystemExit("labeling.py has no SPACES")


def md_table(text_, heading):
    """The first table under `## heading`: rows keyed by lower-case header."""
    m = re.search(r"^## %s\s*$" % re.escape(heading), text_, re.M)
    lines = []
    for l in text_[m.end():].split("\n## ", 1)[0].splitlines():
        if l.startswith("|"):
            lines.append(l)
        elif lines:
            break
    head = [c.strip().lower() for c in lines[0].strip("|").split("|")]
    return [dict(zip(head, (c.strip() for c in l.strip("|").split("|")))) for l in lines[2:]]


SPACES = presenter_spaces()
# The Workbench Table through table-workbench's own reader, so --check and this drawing see the same rows.
sys.path.insert(0, str(TOOLKIT / "skills" / "0_utils" / "table-workbench" / "ref"))
from render_workbench_table import read_table  # noqa: E402
TABLE = read_table(SKILL / "ref" / "workbench-table.md")
MAP_TEXT = MAPPING.read_text(encoding="utf-8")
UNBUILT = {r["in words"] for r in md_table(MAP_TEXT, "Workflow map") if r["started by"] == "not built yet"}
ASKS = {r["space"].strip("* "): r["first question"] for r in md_table(MAP_TEXT, "Space roster")}
WRITES = {r["in words"]: r["writes to"].replace("`", "") for r in md_table(MAP_TEXT, "Workflow map")}
for r in md_table(MAP_TEXT, "Corpus Preparation Run Types"):
    WRITES[r["in words"]] = r["writes to"]

FW, GAP = 1176, 32
X = [48 + i * (FW + GAP) for i in range(4)]
WIDE = 4 * FW + 3 * GAP

# ---- title -----------------------------------------------------------------------------------
text("title", 48, 24, "Labeling Workbench · design", 34)
text("subtitle", 48, 74, "One labeling job on one Page: labels whose meaning one person decides. Four working Spaces, "
     "input → process → checks → output, each with its content on the left and its Runs panel on the right.", 18, MUTED)
rect("hdr-box", 48, 118, WIDE, 64, BLUE, "#e7f5ff")
text("hdr-text", 72, 128, "Header  🏷 <the job's question>  ·  all labeling jobs  ·  band: phase · round n: x of y "
     "labeled · guideline G_nn · HOLD or no HOLD", 19, BLUE)
text("hdr-rule", 72, 154, "Guide comes first on the Space row, then Data · Labeling · Quality · Delivery. Each Space "
     "opens with its brief; every View ends with \"Steps in this view\". The board level lists every job.", 15, MUTED)
F1 = len(E)

# ---- 1 · Spaces, Views, runs in order, and the skill of each run ----------------------------
P1 = 222
text("p1-title", 48, P1, "1 · Spaces, Views, Run types in order, and the skill and agent of each", 28)
page_rows = [r for r in TABLE if r["Level"] == "page"]
cols = []
for space, views in SPACES:
    subs = []
    for view in views:
        runs = [r for r in page_rows if r["Space"] == space and r["View"] == view and r["Run type"] != "none"]
        subs.append((view, runs))
    cols.append((space, subs))


def col_height(subs):
    y = 140
    for _v, runs in subs:
        y += max(56, sum(74 for _ in runs) + 12)
    return y + 70


BH = max(col_height(subs) for _s, subs in cols)
for i, (space, subs) in enumerate(cols):
    x0, y0 = X[i], P1 + 56
    rect(f"m{i}-box", x0, y0, FW, BH)
    text(f"m{i}-title", x0 + 24, y0 + 22, f"{space} Space", 28)
    text(f"m{i}-asks", x0 + 24, y0 + 62, wrap(ASKS.get(space, ""), FW - 48, 15), 15, BLUE)
    line(f"m{i}-rule", x0 + 24, y0 + 112, FW - 48)
    y, n = y0 + 130, 0
    for v, (view, runs) in enumerate(subs):
        button(f"m{i}-v{v}", x0 + 24, y, 200, 40, view, size=17)
        ry = y
        if not runs:
            text(f"m{i}-v{v}-none", x0 + 248, ry + 8, "(no Run type: a view)", 17, MUTED)
            ry += 44
        for k, r in enumerate(runs):
            n += 1
            unbuilt = r["Run type"] in UNBUILT
            color = MUTED if unbuilt else INK
            text(f"m{i}-v{v}-r{k}", x0 + 248, ry + 4, f"{n:>2}  {r['Run type']}" + ("   · not built yet" if unbuilt else ""),
                 17, color)
            signs = "" if r["Person signs"] == "none" else f" · you sign {r['Person signs']}"
            t = text(f"m{i}-v{v}-s{k}", x0 + 290, ry + 28,
                     wrap(f"{r['Skill']} · {r['Agent'].replace(' (new)', '*')}{signs}", FW - 320, 13 * 1.08),
                     13, MUTED if unbuilt else GREEN, mono=True)
            ry += 34 + t["height"]
        y = max(y + 56, ry + 12)
    text(f"m{i}-hands", x0 + 24, y0 + BH - 44, {
        "Data": "hands on: a contract and a checked corpus → Labeling",
        "Labeling": "hands on: confirmed meanings, judged rounds, a guideline → Quality, Delivery",
        "Quality": "hands on: a selected model and an audit → Delivery",
        "Delivery": "hands on: the frozen handoff and the final labels → the reader"}.get(space, ""), 15, MUTED)
for i in range(3):
    arrow(f"m-link{i}", X[i] + FW + 2, P1 + 56 + 40, [[0, 0], [GAP - 4, 0]], BLUE)
guide_runs = [r for r in TABLE if r["Space"] == "Guide" and r["Run type"] != "none"]
text("m-rules", 48, P1 + 56 + BH + 24,
     "Drawn from workbench-labeling/ref/workbench-table.md (generated from ref-space-mapping.md). The number is the "
     "step order inside the Space; grey rows have no worker yet; * marks a planned agent.\n"
     "The agent prepares a Run and calls the engine's checked writer; the person never does a Run and signs only what is "
     "theirs. Guide, shared by every workbench: "
     + " · ".join(f'{r["View"]} → {r["Run type"]} ({r["Skill"]})' for r in guide_runs) + ".", 16)
F2 = len(E)

# ---- 2 · each Space as the workbench shows it -----------------------------------------------
P2 = P1 + 56 + BH + 120
text("p2-title", 48, P2, "2 · Each Space as the page shows it: View tabs, brief, content on the left, Runs on the right", 28)
Y0, FH = P2 + 56, 900


def space(key, i, name, facts, sel_view, draw, types, sel_type, run, notes):
    x0 = X[i]
    names = [s for s, _ in SPACES]
    views = dict(SPACES)[name]
    rect(f"{key}-space", x0, Y0, FW, FH)
    text(f"{key}-title", x0 + 24, Y0 + 24, f"{name} Space", 30)
    line(f"{key}-rule", x0 + 24, Y0 + 62, FW - 48)
    chips(f"{key}-tab", x0 + 24, Y0 + 76, ["Guide"] + names, names.index(name) + 1, size=18, h=46)
    rect(f"{key}-box", x0 + 24, Y0 + 140, 744, 720, RULE)
    chips(f"{key}-view", x0 + 44, Y0 + 156, views, views.index(sel_view), size=15, h=36)
    line(f"{key}-vrule", x0 + 44, Y0 + 204, 704)
    brief(f"{key}-brief", x0 + 44, Y0 + 216, facts)
    line(f"{key}-brule", x0 + 44, Y0 + 266, 704)
    draw(key, x0 + 44, Y0 + 282)
    rx, ry = x0 + 792, Y0 + 140
    rect(f"{key}-runs", rx, ry, 360, 720, bg=PANEL)
    text(f"{key}-runs-title", rx + 16, ry + 16, "▸ Runs   (starts folded: ◂ Runs)", 17)
    yy = ry + 56
    for n, label in enumerate(types):
        button(f"{key}-type-{n}", rx + 16, yy, 328, 34, label, sel=n == sel_type, size=13,
               dashed=label.startswith("+"))
        yy += 42
    dy = yy + 10
    rect(f"{key}-detail", rx + 16, dy, 328, 330, bg="#ffffff")
    text(f"{key}-run-name", rx + 28, dy + 12, run["name"], 13, INK, mono=True)
    text(f"{key}-state", rx + 28, dy + 36, run["state"], 13, GREEN)
    if run.get("action"):
        button(f"{key}-act", rx + 252, dy + 34, 80, 26, run["action"], size=12)
    text(f"{key}-skill", rx + 28, dy + 66, "Run Type skills\n" + run["skill"], 12, GREEN, mono=True)
    text(f"{key}-prompt", rx + 28, dy + 116, "▸ Prompt" + ("   Copy" if run.get("action") else "   (record only)"), 14)
    text(f"{key}-process-label", rx + 28, dy + 150, "Running process", 14)
    text(f"{key}-process", rx + 28, dy + 172, run["process"], 12, MUTED)
    text(f"{key}-results-label", rx + 28, dy + 214, "Results", 14)
    text(f"{key}-results", rx + 28, dy + 236, run["results"], 12, BLUE, mono=True)
    text(f"{key}-notes", x0 + 24, Y0 + FH + 16, notes, 15, MUTED)


def steps_table(key, x, y, rows):
    return grid(key, x, y, ["Step", "Run type", "Writes", "On this job"], rows, [52, 250, 230, 172], 12)


def data_content(key, x, y):
    text(f"{key}-h1", x, y, "The job", 17)
    y = kv(f"{key}-job", x, y + 26, [("job", "example"), ("target", "unsafe_response"),
                                     ("labels decided by", "one person · one person decides every label"),
                                     ("test kept by", "the custodian"), ("created", "by Run run-labeling-corpus-contract-…"),
                                     ("contract check", "valid")], w=700)
    text(f"{key}-h2", x, y + 12, "Labels", 17)
    y = kv(f"{key}-lab", x, y + 38, [("labels", "high · low · none"), ("regions", "H · L · N · HL · LN · HN · HLN"),
                                     ("how sure", "low · medium · high")], w=700)
    text(f"{key}-h3", x, y + 12, "Data   ·   What you see after you lock an answer", 15, MUTED)
    text(f"{key}-h4", x, y + 44, "Steps in this view", 17)
    steps_table(f"{key}-st", x, y + 70, [["1", "Set up the job", "gates/p0-contract/receipt.json", "done · run-…"]])


def labeling_content(key, x, y):
    text(f"{key}-h1", x, y, "All rounds", 17)
    y = grid(f"{key}-all", x, y + 26, ["Round", "State", "Labeled", "Changed after reveal", "How drawn", "Guideline"],
             [["round 1", "all labeled", "20 of 20", "3", "uniform-random · seed", "G_00"],
              ["round 2", "labeling", "8 of 20", "1", "disagreement-focused", "G_01"]], [80, 100, 80, 160, 190, 94])
    text(f"{key}-h2", x, y + 10, "How the final labels fall   (counts only)", 15)
    y = grid(f"{key}-fall", x, y + 34, ["Round", "high", "low", "none", "All"],
             [["round 1", "4", "9", "7", "20"]], [120, 100, 100, 100, 100])
    rect(f"{key}-round", x, y + 14, 704, 176, BLUE)
    text(f"{key}-round-h", x + 14, y + 26, "▾ Round 2   8 of 20 labeled   you are labeling · started …", 15)
    kv(f"{key}-rk", x + 14, y + 54, [("how drawn", "from the items to label, seed"), ("guideline", "G_01")], w=676)
    grid(f"{key}-items", x + 14, y + 118, ["#", "Item", "Text (only items already shown)", "Group", "State"],
         [["#1", "item …", "the reply as shown in the chat", "G3", "LOW"]], [40, 80, 340, 70, 146])
    text(f"{key}-h4", x, y + 208, "Steps in this view", 17)
    steps_table(f"{key}-st", x, y + 234, [["7", "Draw one round", "rounds/round_NN/", "done · run-…"],
                                          ["9", "You label one round", "…/sessions/events.jsonl", "in progress · run-…"],
                                          ["11", "Measure one completed set", "…/metrics.json", "not built yet"]])


def quality_content(key, x, y):
    text(f"{key}-h1", x, y, "(no result yet: evaluation/ does not exist)", 15, MUTED)
    text(f"{key}-h4", x, y + 34, "Steps in this view", 17)
    yy = steps_table(f"{key}-st", x, y + 60, [["15", "Have one registered model predict the test", "evaluation/predictions/", "not built yet"],
                                              ["16", "Score one closed set of predictions", "evaluation/scorecards/", "not built yet"],
                                              ["17", "Select from the complete scorecard set", "evaluation/summary.md", "not built yet"]])
    text(f"{key}-later", x, yy + 20, "Once it exists: one row per scored model, the selected one marked.", 14, ORANGE)


def delivery_content(key, x, y):
    text(f"{key}-h1", x, y, "(no result yet: production/ does not exist)", 15, MUTED)
    text(f"{key}-h4", x, y + 34, "Steps in this view", 17)
    steps_table(f"{key}-st", x, y + 60, [["18", "Check one frozen production plan", "…/preflight.json", "not built yet"],
                                         ["19", "Label one frozen corpus shard", "production/run_<n>/", "not built yet"],
                                         ["20", "Route risky items to review", "…/risk_queue.jsonl", "not built yet"],
                                         ["21", "You label one risk queue", "…/human_final.jsonl", "not built yet"],
                                         ["22", "Reconcile reviewed items", "…/run_report.md", "not built yet"]])


space("data", 0, "Data", [("items", "350"), ("to label", "300"), ("held back", "50"), ("contract", "valid"),
                          ("embedding builds", "1")], "Contract", data_content,
      ["Set up the job  1", "+ New Run"], 0,
      {"name": "run-labeling-corpus-contract-…", "state": "done", "skill": "haipipe-labeling-contract",
       "process": "created … · the meaning still had to\nbe confirmed then", "results": "results/run-labeling-corpus-contract-…/"},
      "Preparation → Raw corpus · Items to label (20 at a time) · Steps   Embedding → model · item to vector · map · groups · build record")
space("labeling", 1, "Labeling", [("meanings (G0)", "confirmed"), ("meaning changes", "1"), ("rounds", "2"),
                                  ("open round", "round 2 · 8 of 20"), ("labeled", "28"), ("guideline", "G_01")],
      "Rounds", labeling_content, ["Draw one round  2", "You label one round  2", "+ New Run"], 1,
      {"name": "run-labeling-human-calibration-…", "state": "in progress", "action": "Resume",
       "skill": "haipipe-labeling-rounds", "process": "started … · you are labeling",
       "results": "results/run-labeling-human-\ncalibration-…/"},
      "Definition → label definitions · discussion · Meaning (G0) · meaning history   Guideline → versions · the current text")
space("quality", 2, "Quality", [("held-back test", "50 items · sealed, not locked"), ("models scored", "none"),
                                ("audits", "none")], "Evaluation", quality_content, ["(no Run type can start yet)"], 0,
      {"name": "No runs yet.", "state": "", "skill": "haipipe-labeling-evaluation", "process": "", "results": ""},
      "Test → held-back test items (items, how drawn, keeper, state, locked)   Audit → its steps until an audit exists")
space("delivery", 3, "Delivery", [("handoff", "not frozen"), ("production runs", "none"), ("final labels", "not released")],
      "Scan", delivery_content, ["(no Run type can start yet)"], 0,
      {"name": "No runs yet.", "state": "", "skill": "haipipe-labeling-scan", "process": "", "results": ""},
      "Handoff → the frozen handoff · its steps   Final labels → the released labels · their steps")
F3 = len(E)

# ---- 3 · every View, block by block ---------------------------------------------------------
P3 = Y0 + FH + 110
text("p3-title", 48, P3, "3 · Every View, block by block (each ends with \"Steps in this view\")", 28)
BLOCKS = {
    "Preparation": ["Raw corpus: source · folder · one row is · one item is ·\n  raw column → item field · other columns · built",
                    "Items to label: one item is · counts · text and\n  context fields · kept together across the test",
                    "Show items: 20 at a time, each fetch logged",
                    "before a job: Page folder needed, or Corpus\n  Preparation (n of 5 steps, the accepted package)"],
    "Contract": ["The job: job · target · question · labels decided by ·\n  test kept by · created · by Run · contract check",
                 "Labels: labels · kind · regions · how sure",
                 "Data: source · items · to label · held back · embedding",
                 "Imported labels (when an outside rating set came)",
                 "What you see after you lock an answer"],
    "Embedding": ["Embedding model: builds · Run a new embedding",
                  "From item to vector · Worked example (made up)",
                  "Map: 2D or 3D · color by group or label · pick a dot",
                  "Groups: k-means · typical items on request, logged",
                  "Build record: run · model · files · rebuild command"],
    "Definition": ["Label definitions: question · confirmed · each label's\n  meaning · in-between cases (`not defined yet`)",
                   "Discussion: each label before and after · still open",
                   "Meaning (G0): confirmed ✓, or Confirm, or the reason not",
                   "Meaning history: each revision · when · by · labels changed"],
    "Rounds": ["Start round 1 (when no round is open)",
               "All rounds: state · labeled · changed after reveal ·\n  how drawn · guideline",
               "How the final labels fall: counts per label",
               "One box per round: its card, then the items it drew\n  (text only for items already shown)"],
    "Guideline": ["Versions: version · status · from · made by · used by ·\n  current marked",
                  "Guideline G_nn: the text (question, classes,\n  regions, uncertainty)"],
    "Test": ["Held-back test items: items · how drawn · keeper ·\n  state · locked for scoring"],
    "Evaluation": ["blank until evaluation/ exists, then the registry"],
    "Audit": ["blank until an audit exists, then the audits"],
    "Handoff": ["blank until handoff/label-v1.yaml exists, then its status"],
    "Scan": ["blank until production/ exists, then its runs"],
    "Final labels": ["blank until corpus/final/D_star.jsonl exists"],
}
VH = 330
for i, (space_name, views) in enumerate(SPACES):
    for v, view in enumerate(views):
        x0, y0 = X[i], P3 + 56 + v * (VH + 24)
        rect(f"v{i}{v}-box", x0, y0, FW, VH)
        button(f"v{i}{v}-name", x0 + 20, y0 + 18, 240, 40, f"{space_name} › {view}", sel=True, size=16)
        yy = y0 + 76
        for b, block in enumerate(BLOCKS.get(view, [])):
            t = text(f"v{i}{v}-b{b}", x0 + 30, yy, "• " + block, 15)
            yy += t["height"] + 8
        runs = [r for r in page_rows if r["Space"] == space_name and r["View"] == view and r["Run type"] != "none"]
        sx = x0 + 640
        text(f"v{i}{v}-steps", sx, y0 + 26, "Steps in this view", 17)
        sy = y0 + 58
        for k, r in enumerate(runs):
            unbuilt = r["Run type"] in UNBUILT
            text(f"v{i}{v}-s{k}", sx, sy, ("○ " if unbuilt else "● ") + r["Run type"][:44], 14, MUTED if unbuilt else INK)
            text(f"v{i}{v}-w{k}", sx + 22, sy + 19, WRITES.get(r["Run type"], "")[:58], 11, MUTED, mono=True)
            sy += 42
        if not runs:
            text(f"v{i}{v}-s-none", sx, sy, "none", 14, MUTED)
text("v-legend", 48, P3 + 56 + 3 * (VH + 24) + 4,
     "● a Run type with a worker today   ○ not built yet (its row says so on the page). On the page the state is this job's: "
     "done or in progress with its Run, not started, or not built yet.", 16, MUTED)
F4 = len(E)

# ---- 4 · where things live ------------------------------------------------------------------
P4 = P3 + 56 + 3 * (VH + 24) + 80
text("p4-title", 48, P4, "4 · Where things live: what each Space reads, the one write door, the rules", 28)
READS = {
    "Data": "config.yaml · corpus/source.yaml\ncorpus/manifest.json · corpus/items.jsonl (on request)\n"
            "preparation-owner.yaml · preparation-ref.yaml\ngates/p0-contract/ · cache/embeddings/<version>/",
    "Labeling": "config.yaml labels and meanings\ngates/g0/ · gates/meaning-revisions/\n"
                "rounds/round_NN/ (card, batch, events)\npolicy/current · policy/versions/<G>/",
    "Quality": "test/sealed/status.json\ntest/final/lock.json\nevaluation/ · audit/final_<n>/",
    "Delivery": "handoff/label-v1.yaml\nproduction/run_<n>/\ncorpus/final/D_star.jsonl",
}
for i, (space_name, _v) in enumerate(SPACES):
    x0, y0 = X[i], P4 + 56
    rect(f"r{i}-box", x0, y0, FW, 210, "#9c36b5", dashed=True)
    text(f"r{i}-title", x0 + 24, y0 + 18, f"{space_name} reads", 22, "#9c36b5")
    text(f"r{i}-files", x0 + 24, y0 + 58, READS[space_name], 16, INK, mono=True)
y0 = P4 + 56 + 240
rect("door-box", 48, y0, 2 * FW + GAP, 230, ORANGE)
text("door-title", 72, y0 + 18, "The one write door · POST /_board/labeling/act", 22, ORANGE)
text("door-text", 72, y0 + 58,
     "confirm_meaning (G0) · release_round · open_item · first · final · build_embedding\n"
     "reads: embedding_status · embedding_item · group_examples · embedding_item_text · item_page\n"
     "Each action goes through the engine (job.py, calibration.py), which re-checks the configured person,\n"
     "HOLD, G0, the event order and the sealed test on every call. Every other button only copies a prompt.", 16)
rect("rules-box", 48 + 2 * (FW + GAP), y0, 2 * FW + GAP, 230, INK)
text("rules-title", 72 + 2 * (FW + GAP), y0 + 18, "Rules the page keeps", 22)
text("rules-text", 72 + 2 * (FW + GAP), y0 + 58,
     "1. Item text appears only in Labeling › Rounds, and only for items already shown.\n"
     "2. A file observed on disk is never shown as a passed gate.\n"
     "3. The person is the only source of gold: a model's agreement never makes a label true.\n"
     "4. Held-back test items are never shown, counted from, or drawn into a round.\n"
     "5. The page stores nothing: it reads the job's files on every open.", 16)
F5 = len(E)


# ---- frames ---------------------------------------------------------------------------------
def bounds(e):
    if e.get("points"):
        xs, ys = [e["x"] + p[0] for p in e["points"]], [e["y"] + p[1] for p in e["points"]]
        return min(xs), min(ys), max(xs), max(ys)
    return e["x"], e["y"], e["x"] + e["width"], e["y"] + e["height"]


def frame(id_, name, start, end, pad=40):
    """A named frame around E[start:end]; its name is the address Guide can open."""
    box = [bounds(e) for e in E[start:end]]
    f = base(id_, "frame", min(b[0] for b in box) - pad, min(b[1] for b in box) - pad,
             max(b[2] for b in box) - min(b[0] for b in box) + 2 * pad,
             max(b[3] for b in box) - min(b[1] for b in box) + 2 * pad, rounded=False)
    f["name"] = name
    for e in E[start:end]:
        e["frameId"] = id_
    return f


E += [frame("frame-skills", "Spaces, runs and skills", F1, F2),
      frame("frame-workbench", "The workbench", F2, F3),
      frame("frame-views", "Every View", F3, F4),
      frame("frame-folders", "Where things live", F4, F5)]

OUT.write_text(json.dumps({"type": "excalidraw", "version": 2, "source": "haipipe-workbench-labeling-ui",
                           "elements": E, "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None},
                           "files": {}}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"Wrote {OUT.name}: {len(E)} elements")
