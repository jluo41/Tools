"""b11 s00 · Insight structure: s00-insight-structure.excalidraw: the thinking behind the insight ladder.

A design scratch (JL 261007: "please have s00 to put these thoughts into the draw with the tree and box"):
what an Insight Project looks like; the Prototype as its own work Block whose Jobs are Prototype
versions; the insight Board whose Jobs pin one Prototype version and one data version; the two clocks;
where a new release comes from and what triggers it; and a Questions frame (the Block's register,
read from board.md, with our idea beside each and your choice in a red box).

Placeholders only (<project>, bNN_<topic>, <d>v1); black only, red for what is open, green for a change. The canvas
writer (haipipe-studio scripts/canvas.py) keeps every mark a person adds through a rebuild.

    python build_s00_insight_structure.py [out.excalidraw]
"""
import random
import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
BLOCK = HERE.parents[1]                                   # b11_theme_insight/
sys.path.insert(0, str(HERE.parents[3] / "b01_haipipe-toolkit" / "j03_project_workbench" / "studio" / "_build"))
sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))  # canvas (haipipe-studio)
import canvas  # noqa: E402

random.seed(1)
HAND, MONO = 6, 3
INK, GRAY, RED, BLUE, GREEN = "#1e1e1e", "#1e1e1e", "#e03131", "#1e1e1e", "#2f9e44"   # black only (haipipe-studio 0.2.0)
els = []
FRAME = [None]


def base(kind, x, y, w, h, stroke=INK, bg="transparent", sw=2, dashed=False):
    e = {"id": f"t{len(els)}", "type": kind, "x": x, "y": y, "width": w, "height": h, "angle": 0,
         "strokeColor": stroke, "backgroundColor": bg, "fillStyle": "solid", "strokeWidth": sw,
         "strokeStyle": "dashed" if dashed else "solid", "roughness": 1, "opacity": 100, "groupIds": [],
         "frameId": FRAME[0], "roundness": {"type": 3} if kind == "rectangle" else None,
         "seed": random.randint(1, 2**31 - 1), "version": 1, "versionNonce": random.randint(1, 2**31 - 1),
         "isDeleted": False, "boundElements": [], "updated": 1, "link": None, "locked": False}
    els.append(e)
    return e


def text(x, y, s, size=22, color=INK, font=HAND, container=None):
    lines = s.split("\n")
    w = max(len(l) for l in lines) * size * (0.6 if font == MONO else 0.58)
    e = base("text", x, y, w, len(lines) * size * 1.25, color)
    e.update(text=s, originalText=s, fontSize=size, fontFamily=font, textAlign="left", verticalAlign="top",
             containerId=container, autoResize=True, lineHeight=1.25)
    return e


def box(x, y, w, h, stroke=INK, bg="transparent", dashed=False, sw=2):
    return base("rectangle", x, y, w, h, stroke, bg, sw, dashed)


def sticky(x, y, w, body, kind, size=18):
    """A note the person can rewrite: its text is bound to it; sized to its text."""
    lines = []
    for para in body.split("\n"):
        line = ""
        for word in para.split():
            if line and len(line) + 1 + len(word) > (w - 32) / (size * 0.58):
                lines.append(line)
                line = word
            else:
                line = f"{line} {word}" if line else word
        lines.append(line)
    h = 30 + len(lines) * size * 1.3
    r = box(x, y, w, h, RED if kind == "open" else INK, "transparent", sw=1)   # black only; a choice is open
    t = text(x + 16, y + 14, "\n".join(lines), size, INK, container=r["id"])
    r["boundElements"] = [{"type": "text", "id": t["id"]}]
    return y + h


def tree(x, y, rows, size=16, gap=430, title=None):
    """A folder tree: each row (path, its meaning); a meaning in red is open. Returns the bottom."""
    if title:
        text(x, y, title, 24)
        y += 44
    for i, (path, meaning) in enumerate(rows):
        text(x, y + i * size * 1.55, path, size, INK, MONO)
        if meaning:
            text(x + gap, y + i * size * 1.55 + 1, meaning, size - 1, RED if meaning.endswith("?") else GRAY)
    return y + len(rows) * size * 1.55


def arrow(pts, color=INK, dashed=False, label=None, label_at=None):
    x, y = pts[0]
    rel = [[px - x, py - y] for px, py in pts]
    e = base("arrow", x, y, max(abs(p[0]) for p in rel) or 1, max(abs(p[1]) for p in rel) or 1, color,
             dashed=dashed)
    e.update(points=rel, lastCommittedPoint=None, startBinding=None, endBinding=None,
             startArrowhead=None, endArrowhead="arrow")
    if label:
        lx, ly = label_at or ((pts[0][0] + pts[-1][0]) / 2, (pts[0][1] + pts[-1][1]) / 2 - 30)
        text(lx, ly, label, 17, color)


# ── 1 · an Insight Project ───────────────────────────────────────────────────────────────────────
PROJECT = [("<project>/", ""),
           ("├── README.md · project.yaml", "the Project's face; themes: work · insights · designs"),
           ("├── work/", "the work theme"),
           ("│   └── bNN_<topic>_prototype/", "the Prototype: questions + code, versioned"),
           ("├── insights/", "the insight theme"),
           ("│   └── bNN_<topic>/", "the insight Board: data, Jobs, answers, handoff"),
           ("├── designs/   (optional)", "reads the Board's signed Wisdom handoff"),
           ("└── discoveries/   (optional)", "papers that suggest a method or a question"),
           ("<workspace>/<extracts>/", "the data versions, outside the Project: <d>v1 · <d>v2 …"),
           ("", "one Prototype Block serves one insight Board, or several ?")]

# ── 2 · the two Blocks: a box, its definition, its tree ─────────────────────────────────────────
PROTO = ("bNN_<topic>_prototype/", "work theme: the Prototype, made once per version, reviewed, signed", [
    ("├── board.md", "kind: prototype · serves: insights/bNN_<topic>"),
    ("├── proposals/", "the backlog: new · fix · retire, from the Board"),
    ("├── j01_p1/", "Job = Prototype version p1, frozen when closed"),
    ("│   ├── release.yaml", "every live question -> its Task (here or earlier)"),
    ("│   ├── partitions.md · thresholds.yaml", "the cuts, power floors, compare rule: plan"),
    ("│   ├── t01_D01_<q>/", "question.md · scripts/<name>.py · a test"),
    ("│   ├── t02_D02_<q>/ …", "grouped by level: D · I · K · W"),
    ("│   └── runs/", "soft: ask · plan · script · review · sign"),
    ("├── j02_p2/", "only new or changed Tasks, + release.yaml"),
    ("└── j03_p3/ …", "the next version, opened from proposals/")])
BOARD = ("bNN_<topic>/", "insight theme: one dataset, its versions, the answers", [
    ("├── board.md", "dataset: <d> · versions · accumulates ?"),
    ("│", "prototype: work/bNN_<topic>_prototype"),
    ("├── meta/status.md", "written only by the checker; the cuts live in the release"),
    ("├── reports/qNN_<topic>/", "the Block's own questions: D · I · K · W over the Jobs"),
    ("├── j01_p1_<d>v1/", "Job = Prototype p1 x data v1, frozen"),
    ("│   ├── j01_p1_<d>v1.md", "pins: j01_p1 (hash) · <d>v1"),
    ("│   └── t01_D01_<q>/", "the question on this pair: its page"),
    ("│   ├── t01_D01_<q>/runs/r01_full/ …", "hard: one per partition"),
    ("│   └── reports/vs-<prev>.md", "run-compare: new · held · changed · dropped"),
    ("├── j02_p1_<d>v2/", "data moved"),
    ("├── j03_p2_<d>v2/", "code moved"),
    ("└── delivery/", "the signed Wisdom handoff, latest Job")])

# ── 4 · where a new release comes from ──────────────────────────────────────────────────────────
TRIGGERS = [("a level is answered", "D answers raise I questions; I raise K; K raise W"),
            ("a check fails", "a script bug, a wrong spec -> fix"),
            ("an answer is weak", "underpowered, null, unstable across Jobs -> rework or retire"),
            ("new data, new fields", "a version adds columns -> new questions, or a new cut (a cut is plan)"),
            ("someone asks", "Design or a person needs a question answered"),
            ("a paper suggests it", "Discovery: a new method or a new question")]
FLOW = ["proposals/\nthe backlog", "open j0N_pN+1\n(a version Job)", "ask · plan · script\nreview (another agent)",
        "sign (a person)\nclose = frozen", "insight Board\nAdd a Job: pN+1 x latest"]
WHEN = ["when to cut a release ?", "  a level's questions all signed", "  a batch of proposals agreed",
        "  on demand, by a person"]

# ── 5 · the Questions frame: the register, our ideas, the choices ───────────────────────────────
IDEAS = {"Q01": ("Board = data + Jobs + answers; the Prototype is its own work Block; Job = pN x vM; "
                 "Task = a question in the Job; Run = a partition.",
                 "Prototype in its own work Block, or inside the Board (s01 plan C)?"),
         "Q02": ("Versions are a second axis beside partitions: versions = Jobs, partitions = Runs; the cuts are defined in the release, so a new cut is a new release.",
                 "Versions accumulate (compare, never pool) or come in batches (may pool)?"),
         "Q03": ("Gates are chips on each question row; the checker is a Board Run.",
                 "Chips, or keep a Check Space?"),
         "Q04": ("Only the latest Job's Wisdom delivers; the signed handoff names its pair (pN x vM).",
                 "Does a handoff go stale when a newer Job lands?"),
         "Q05": ("Carry each register board over: a Prototype Block + an insight Board.",
                 "Carry over all now, or each when next worked on?")}
PROPOSED = ("(proposed) Q06", "How do the Prototype and the data versions evolve?",
            "Triggers -> proposals/ -> the next version Job -> sign -> the Board adds a Job; one clock per Job.",
            "Signed releases, cut per level, per batch, or on demand?")


# ── 6 · the logic tree (JL 261007: "add things like this: the logic tree"), the s04 way ─────────
# a box per folder (its name in monospace, a gray line under it); a plain line = holds; an arrow = a
# relationship, labelled; red dashed = open. Its own frame to the right, so nothing above moves.
LT_BOXES = {   # key: (column, y, name, what it is)
    "project": (0, 900, "<project>/", "an Insight Project"),
    "work": (1, 260, "work/", "the work theme"),
    "insights": (1, 1060, "insights/", "the insight theme"),
    "designs": (1, 1720, "designs/", "optional: reads the handoff"),
    "proto": (2, 260, "bNN_<topic>_prototype/", "the Prototype: questions + code"),
    "board": (2, 1060, "bNN_<topic>/", "one dataset, its versions, answers"),
    "proposals": (3, 60, "proposals/", "the backlog: new · fix · retire"),
    "version": (3, 380, "j0N_pN/", "a Prototype version, frozen when closed"),
    "boardmd": (3, 760, "board.md", "dataset: <d> · v1 · v2 … · accumulates ?"),
    "job": (3, 1060, "j0N_pN_<d>vM/", "a Job: version × data, frozen"),
    "reports": (3, 1380, "reports/qNN_<topic>/", "the Block's questions: D · I · K · W over the Jobs"),
    "delivery": (3, 1600, "delivery/", "the signed Wisdom handoff"),
    "cuts": (4, 150, "partitions.md · thresholds.yaml", "the cuts, power floors, compare rule: plan"),
    "release": (4, 300, "release.yaml", "every live question -> its Task"),
    "ptask": (4, 470, "tNN_<L><NN>_<q>/", "question.md · scripts/<name>.py"),
    "btask": (4, 1060, "tNN_<L><NN>_<q>/", "the question on this pair: its page"),
    "extract": (5, 760, "<d>vM  (an extract)", "outside the Project, by date"),
    "run": (5, 1060, "runs/rNN_<partition>/", "hard: result/ · passes/")}
LT_HOLDS = [("project", "work"), ("project", "insights"), ("project", "designs"), ("work", "proto"),
            ("insights", "board"), ("proto", "proposals"), ("proto", "version"), ("version", "cuts"), ("version", "release"),
            ("version", "ptask"), ("board", "boardmd"), ("board", "job"), ("board", "reports"),
            ("board", "delivery"), ("job", "btask"), ("btask", "run")]
LT_COLS = [0, 420, 900, 1480, 2060, 2640]
LT_H = 64


def logic_tree(x0, y0):
    fr = base("frame", x0 - 60, y0 - 60, 10, 10, GRAY)
    fr["name"], fr["roundness"] = "Logic tree: an Insight Project", None
    FRAME[0] = fr["id"]
    text(x0, y0, "The logic tree: what an Insight Project holds, and how its Prototype and its Board relate", 30)
    text(x0, y0 + 48, "plain line = holds · arrow = a relationship, labelled · red dashed = open", 18, GRAY)
    top = y0 + 140
    at = {}
    for key, (col, y, name, what) in LT_BOXES.items():
        x, yy = x0 + LT_COLS[col], top + y
        w = len(name) * 17 * 0.6 + 40
        box(x, yy, w, LT_H)
        text(x + 20, yy + 20, name, 17, INK, MONO)
        text(x, yy + LT_H + 8, what, 15, RED if what.endswith("?") else GRAY)
        at[key] = (x, yy, w)

    def right(k):
        x, y, w = at[k]
        return x + w, y + LT_H / 2

    def left(k):
        x, y, w = at[k]
        return x, y + LT_H / 2

    for parent, child in LT_HOLDS:                  # an elbow: out of the parent, down, into the child
        (sx, sy), (ex, ey) = right(parent), left(child)
        mx = ex - 40
        line = base("line", sx, sy, 1, 1, INK, sw=1.5)
        rel = [[0, 0], [mx - sx, 0], [mx - sx, ey - sy], [ex - sx, ey - sy]]
        line.update(points=rel, width=max(abs(a) for a, _ in rel) or 1, height=max(abs(b) for _, b in rel) or 1,
                    lastCommittedPoint=None, startBinding=None, endBinding=None, startArrowhead=None, endArrowhead=None)

    def mid(k, side):                               # a box's top or bottom middle
        x, y, w = at[k]
        return x + w / 2, (y if side == "top" else y + LT_H)

    # the Board's Job uses one version; its Task runs that version's script
    jxl, jyl, jw = at["job"]                        # up the clear channel right of the Job boxes
    vxl, vyl, vw = at["version"]
    lane = x0 + LT_COLS[3] + 360
    arrow([(jxl + jw, jyl + 16), (lane, jyl + 16), (lane, vyl + LT_H - 10), (vxl + vw, vyl + LT_H - 10)], INK,
          label="uses pN\n(path + hash),\nnever copies", label_at=(lane + 14, jyl - 260))
    (bx, by), (tx, ty) = mid("btask", "top"), mid("ptask", "bottom")
    arrow([(bx + 40, by), (tx + 40, ty + 30)], INK, label="runs its script", label_at=(bx + 60, by - 300))
    # the data version is pinned by the Job
    ex, ey, ew = at["extract"]
    arrow([(ex, ey + LT_H / 2), (ex - 120, ey + LT_H / 2), (ex - 120, at["job"][1] - 40),
           (at["job"][0] + 40, at["job"][1] - 40), (at["job"][0] + 40, at["job"][1])], INK,
          label="pins vM", label_at=(ex - 110, ey + LT_H + 30))
    # each Job's pages feed the answers across Jobs
    (rx, ry) = mid("reports", "top")
    arrow([(at["job"][0] + 60, at["job"][1] + LT_H + 30), (at["job"][0] + 60, ry)], INK,
          label="its pages, compared", label_at=(at["job"][0] + 80, at["job"][1] + LT_H + 120))
    # the answers send proposals back: around the right side, up to the backlog
    rr = right("reports")
    pr = right("proposals")
    far = x0 + LT_COLS[5] + 560
    arrow([rr, (far, rr[1]), (far, pr[1]), pr], INK, label="proposals: new · fix · retire",
          label_at=(far - 330, pr[1] - 40))
    # the backlog opens the next version: when is still open
    px, py = mid("proposals", "bottom")
    arrow([(px, py + 30), (px, at["version"][1])], RED, dashed=True,
          label="? opens the next version:\nper DIKW level, per batch, or on demand", label_at=(px - 470, py + 44))
    # the handoff leaves for Design
    dx, dy, dw = at["delivery"]
    gx, gy, gw = at["designs"]
    arrow([(dx, dy + LT_H / 2), (dx - 60, dy + LT_H / 2), (dx - 60, gy + LT_H / 2), (gx + gw, gy + LT_H / 2)], INK,
          label="reads the signed handoff", label_at=(gx + gw + 20, gy + LT_H / 2 + 14))
    text(x0, top + 1880, "one clock per Job ?  a new Prototype version or a new data version makes a new Job, never both",
         19, RED)
    FRAME[0] = None
    kids = [e for e in els if e.get("frameId") == fr["id"]]
    xs = [e["x"] + px for e in kids for px, _ in (e.get("points") or [[e["width"], 0]])]
    ys = [e["y"] + py for e in kids for _, py in (e.get("points") or [[0, e["height"]]])]
    fr.update(width=max(xs) - fr["x"] + 60, height=max(ys) - fr["y"] + 60)


# ── 7 · run types by level (JL 261007: "we might want to propose more run-types") ───────────────
RUN_TYPES = [   # (level, hard, soft); a red line is proposed and open
    ("Prototype Block", "—", "run-propose · run-open-release-pN"),
    ("  a version Job", "—", "run-define-cuts (cuts, thresholds, compare rule) · run-sign-release (a person) · run-close-release"),
    ("  a question Task", "—", "run-ask · run-plan · run-review-plan · run-script · run-review-script"),
    ("insight Board", "—", "run-add-version-vM · run-add-job-pN-vM · run-check-board · run-read-<reading> · run-handoff"),
    ("  a Job (pN x vM)", "—", "run-launch · run-power (n, power per cut, before outcomes) · run-compare-<prev> · run-close"),
    ("  a question Task", "rNN_<partition> · rNN_cross", "run-write · run-check · run-sign (W: a person signs)")]
ORDER = ("a Job's order:  Add a Job -> run-launch -> run-power -> per Task: rNN_<partition> -> rNN_cross -> run-write "
         "-> run-check -> run-compare-<prev> -> run-close (frozen)")


def run_types(x0, y0):
    fr = base("frame", x0 - 60, y0 - 60, 10, 10, GRAY)
    fr["name"], fr["roundness"] = "Run types by level", None
    FRAME[0] = fr["id"]
    text(x0, y0, "Run types by level: hard writes a result/, soft writes into its level's own folders", 30)
    cols = [0, 330, 760]
    y = y0 + 70
    for h, c in zip(("level", "hard", "soft"), cols):
        text(x0 + c, y, h, 18, GRAY)
    y += 36
    for level, hard, soft in RUN_TYPES:
        line = base("line", x0, y - 6, 2400, 1, GRAY, sw=1)
        line.update(points=[[0, 0], [2400, 0]], lastCommittedPoint=None, startBinding=None, endBinding=None,
                    startArrowhead=None, endArrowhead=None)
        text(x0, y + 4, level, 18)
        text(x0 + cols[1], y + 6, hard, 16, INK, MONO)
        text(x0 + cols[2], y + 6, soft, 16, INK, MONO)
        y += 52
    text(x0, y + 20, ORDER, 17, INK)
    text(x0, y + 60, "? held = same direction and the intervals overlap (D: counts within a tolerance): "
                     "a rule in the release, set before any outcome", 18, RED)
    text(x0, y + 96, "? new question (first asked in this release) is not a new finding", 18, RED)
    FRAME[0] = None
    kids = [e for e in els if e.get("frameId") == fr["id"]]
    xs = [e["x"] + px for e in kids for px, _ in (e.get("points") or [[e["width"], 0]])]
    ys = [e["y"] + py for e in kids for _, py in (e.get("points") or [[0, e["height"]]])]
    fr.update(width=max(xs) - fr["x"] + 60, height=max(ys) - fr["y"] + 60)


def register():
    """The Block's questions, from board.md's `## Questions` yaml."""
    m = re.search(r"(?ms)^## Questions\s*\n```yaml\n(.*?)```", (BLOCK / "board.md").read_text(encoding="utf-8"))
    return yaml.safe_load(m.group(1))["questions"] if m else []


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s00-insight-structure.excalidraw"
    text(0, 0, "Insight structure: a Prototype that evolves, a Board that runs it on data that grows", 40)
    text(0, 62, "Design scratch: placeholders only. Red = open. Draw anywhere; your marks stay through a rebuild.",
         20, GRAY)

    # 1 · the Project
    text(0, 160, "An Insight Project", 30)
    tree(0, 220, PROJECT, gap=470)

    # 2 · the two Blocks
    for k, (name, define, rows) in enumerate((PROTO, BOARD)):
        x = 1300 + k * 1250
        box(x, 160, 520, 70)
        text(x + 20, 178, name, 22, INK, MONO)
        text(x, 248, define, 18, GRAY)
        tree(x, 300, [(name, "")] + rows, gap=430)
    # the Board's Job uses a version, never copies; the Board sends proposals back
    row = lambda i: 300 + i * 16 * 1.55 + 10                 # the middle of tree line i
    arrow([(2540, row(4)), (2210, row(2))], INK, label="proposals: new · fix · retire", label_at=(2250, row(2) - 52))
    arrow([(2540, row(5)), (2210, row(3))], INK, label="uses p1 (path + hash), never copies", label_at=(2230, row(5) + 16))

    # 3 · the two clocks
    cy = 900
    text(0, cy, "Two clocks; a Job pins one of each and is frozen once closed", 30)
    text(0, cy + 60, "Prototype", 22)
    text(240, cy + 62, "p1  ->  p2 (+ I questions, a script fixed)  ->  p3 (a question retired, its successor)  …",
         18, INK, MONO)
    text(0, cy + 110, "data", 22)
    text(240, cy + 112, "<d>v1  ->  <d>v2  ->  <d>v3  …", 18, INK, MONO)
    chain = [("j01_p1_<d>v1", "start"), ("j02_p1_<d>v2", "data moved"), ("j03_p2_<d>v2", "code moved"),
             ("j04_p2_<d>v3", "data moved")]
    x = 0
    for k, (job, moved) in enumerate(chain):
        box(x, cy + 180, 470, 100)
        text(x + 20, cy + 196, job, 20, INK, MONO)
        text(x + 20, cy + 236, moved, 18, GRAY)
        if k < len(chain) - 1:
            arrow([(x + 480, cy + 230), (x + 590, cy + 230)])
        x += 600
    text(0, cy + 310, "one clock per Job ?  then a change in an answer has one cause: new data, or new code", 20, RED)
    text(0, cy + 350, "backfill (new code on old data) is just one more Job: j0N_p2_<d>v1", 18, GRAY)

    # 4 · where a new release comes from
    ty = cy + 470
    text(0, ty, "Where a new release comes from: what triggers the evolving", 30)
    for i, (what, why) in enumerate(TRIGGERS):
        box(0, ty + 60 + i * 74, 300, 56, GRAY, sw=1)
        text(16, ty + 74 + i * 74, what, 19)
        text(320, ty + 76 + i * 74, why, 17, GRAY)
        arrow([(900, ty + 88 + i * 74), (1040, ty + 260)], GRAY)
    fx = 1060
    for k, step in enumerate(FLOW):
        box(fx, ty + 220, 300, 90, RED if "sign" in step else INK)
        text(fx + 18, ty + 236, step, 18, RED if "sign" in step else INK)
        if k < len(FLOW) - 1:
            arrow([(fx + 305, ty + 265), (fx + 375, ty + 265)])
        fx += 380
    text(1060, ty + 340, "new data needs no release: a new extract lands -> the Board adds a Job pN x vM+1", 18, GRAY)
    for i, line in enumerate(WHEN):
        text(1060, ty + 400 + i * 30, line, 19 if i == 0 else 17, RED)

    # 5 · Questions frame: one row per question; the ask, our idea, your choice (red: open)
    qy = ty + 640
    fr = base("frame", -40, qy - 40, 10, 10, GRAY)
    fr["name"], fr["roundness"] = "Questions", None
    FRAME[0] = fr["id"]
    text(0, qy, "Questions: the Block's register, our idea, your choice (red)", 30)
    text(0, qy + 40, "✎ 261007 black only (haipipe-studio 0.2.0): the ideas, once blue, are black; the choices, once pink, "
                     "are red boxes", 16, GREEN)
    rows = [(q["id"], q["title"]) + IDEAS.get(q["id"], ("", "")) for q in register()]
    rows.append(PROPOSED)
    y = qy + 90
    for qid, title, idea, choice in rows:
        bottom = sticky(0, y, 520, f"{qid} · {title}", "ask")
        if idea:
            bottom = max(bottom, sticky(560, y, 640, idea, "idea"))
        if choice:
            bottom = max(bottom, sticky(1240, y, 560, choice, "open"))
        y = bottom + 30
    FRAME[0] = None
    kids = [e for e in els if e.get("frameId") == fr["id"]]
    fr.update(x=-40, y=qy - 40, width=max(e["x"] + e["width"] for e in kids) + 80 + 40,
              height=max(e["y"] + e["height"] for e in kids) - qy + 80)
    logic_tree(3500, 0)
    run_types(3500, max(e["y"] + e["height"] for e in els if e["type"] == "frame") + 260)
    canvas.write(out, list(els), "build_s00_insight_structure.py")


if __name__ == "__main__":
    main()
