"""b03 ladder grid: studio/ladder-grid.excalidraw, levels across, Themes down, lines only.

Columns are the Block, its two branches (reports/ for the Questions, the audience's side; the
Jobs for the work), then Task and Run, plus a notes column; rows are the Themes, with a
first row that defines each level and an empty last row. The table is drawn with plain lines,
black and gray, no fills. Each Theme cell is read from disk: how many folders fill that level
(those on a path to a runs/ folder, three levels below the Theme), their naming shapes, one
real example, and a gray reading; the Run cell adds results/ pairing and run: = stem counts.
Each cell says in gray whether its names follow the level ("fits") or not ("other names").

Shared canvas: s- elements at version 1 are redrawn; anything a person added or moved is kept.

    python build_ladder_grid.py [out.excalidraw]
"""
import json
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))  # canvas (haipipe-studio)
import canvas
import disk_facts as F

random.seed(261006)
SANS, MONO = 6, 3                                    # Excalidraw fonts: Nunito, Cascadia
INK, GRAY, RULE = "#1e1e1e", "#868e96", "#495057"
els = []
FRAME = [None]                                       # elements drawn while set belong to that frame

LEVELS = ["Block", "Job", "Task", "Run"]                 # the work ladder, by depth below the Theme
COLUMNS = ["Block", "reports", "Job", "Task", "Run"]
EXPECT = {"Block": "bNN_<slug>", "reports": "qNN_<slug>", "Job": "jNN_<slug>", "Task": "tNN_<slug>",
          "Run": "rNN_<slug>"}
COLS = [("", 260), ("Block  bNN", 470), ("reports/  qNN", 420), ("Job  jNN", 470), ("Task  tNN", 470),
        ("Run  rNN", 470), ("notes", 420)]
BRANCH = "reports"                                   # the Questions branch: not a Job, never counted as one
DEFINE = {
    "Block": "bNN_<topic>/\none topic: board.md (kind, spine, close,\nQuestions register) and two branches:\nreports/ for the audience, Jobs for the work",
    "reports": "reports/qNN_<topic>/\none Question each, for the audience:\nits report Page says what the work found;\nit reads Runs, it does not do the work",
    "Job": "jNN_<job>/\none line of work inside the Block:\nTasks that share a goal, an input\nor a dataset version",
    "Task": "tNN_<task>/  = a Page folder\none bounded piece of work and its\nPage tNN_<task>.md; holds scripts/,\nruns/ and results/",
    "Run": "runs/rNN_<slug>.*  +  results/<same>/\none commission with a close rule:\nTicket, Result and runtime.yaml\nshare one stem; run: = stem",
}
OWNER = {"Block": "haipipe-board", "reports": "haipipe-question · haipipe-page", "Job": "the Theme's own skill",
         "Task": "haipipe-task · haipipe-page", "Run": "haipipe-run"}
COWORK = {"Block": "bNN_<topic>/ by rule\nboard-kind: cowork-block", "reports": "reports/qNN_<topic>/ by rule", "Job": "jNN_<job>/ by rule\njNN_<job>.md + Timeline.md",
          "Task": "none by rule\n\"no tNN level in cowork\"", "Run": "none by rule\ncode runs in a Task Block"}
READING = {  # how the names on disk read against the definition; a reading, not a rule
    ("discoveries", "Block"): "P01_ / S01_ boards too",
    ("papers", "Job"): "a manuscript or Story part",
    ("papers", "Task"): "a Section or Story Page",
    ("insights", "Job"): "a DIKW level, or a partition",
    ("insights", "Task"): "one question folder",
    ("insights", "Run"): "contract says riNN_<slug>",
    ("designs", "Job"): "a numbered stage of the board",
    ("designs", "Task"): "one Design Folder",
    ("designs", "Run"): "contract says rdNN_<op>_<slug>",
}
NOTES = {
    "definition": "depth already lines up: every Theme\nwith Runs keeps runs/ three folders\nbelow the Theme",
    "tasks": "the reference ladder",
    "discoveries": "same ladder; some Blocks named\nP01_ / S01_ instead of bNN_",
    "cowork": "stops at Job by rule",
    "papers": "same depth, own names;\nRun names run-<kind>-…",
    "insights": "Instance uses DIKW levels for Job,\nthe InsightBoard uses partitions;\nruns named by partition (full.sh)",
    "designs": "same depth, own names;\nRun names run-design-<op>-…",
}
HEAD_H, DEF_H, ROW_H = 60, 190, 235


# ── helpers ────────────────────────────────────────────────────────────────────────────────
def base(kind, x, y, w, h, stroke=INK, sw=1):
    e = {"id": f"s-{len(els)}", "type": kind, "x": x, "y": y, "width": w, "height": h, "angle": 0,
         "strokeColor": stroke, "backgroundColor": "transparent", "fillStyle": "solid", "strokeWidth": sw,
         "strokeStyle": "solid", "roughness": 0, "opacity": 100, "groupIds": [],
         "roundness": None, "seed": random.randint(1, 2**31 - 1), "version": 1, "frameId": FRAME[0],
         "versionNonce": random.randint(1, 2**31 - 1), "isDeleted": False, "boundElements": [], "updated": 1,
         "link": None, "locked": False}
    els.append(e)
    return e


def text(x, y, s, size=18, color=INK, font=SANS):
    lines = s.split("\n")
    e = base("text", x, y, max(len(l) for l in lines) * size * (0.6 if font == MONO else 0.55),
             len(lines) * size * 1.25, color)
    e.update(text=s, originalText=s, fontSize=size, fontFamily=font, textAlign="left", verticalAlign="top",
             containerId=None, autoResize=True, lineHeight=1.25)


def line(x1, y1, x2, y2, sw=1):
    e = base("line", x1, y1, abs(x2 - x1), abs(y2 - y1), RULE, sw)
    e.update(points=[[0, 0], [x2 - x1, y2 - y1]], lastCommittedPoint=None, startBinding=None, endBinding=None,
             startArrowhead=None, endArrowhead=None)


def clip(s, n):
    return s if len(s) <= n else s[: n - 1] + "…"


# ── reading the disk, one Theme at a time ──────────────────────────────────────────────────
def shape(name):
    """The naming shape of a folder or ticket: digits become NN, the free text becomes <slug>."""
    stem, ext = name.rsplit(".", 1) if "." in name else (name, "")
    m = re.match(r"^(\D*?)(\d+)([_-])", stem)
    if m:
        s = f"{m.group(1)}NN{m.group(3)}<slug>"
    else:
        m = re.match(r"^([A-Za-z]+)([_-])", stem)
        s = f"{m.group(1)}{m.group(2)}<slug>" if m else stem
    return s + (f".{ext}" if ext else "")


def theme_facts(th):
    level, depths, examples = defaultdict(set), Counter(), {}
    tickets, beside, receipts, match, projects = Counter(), 0, 0, 0, 0
    for pr in F.projects():
        root = pr / th
        if not root.is_dir():
            continue
        projects += 1
        level["Block"] |= {(pr.name, b.name) for b in F.subdirs(root)}
        for b in F.subdirs(root):
            level["reports"] |= {(pr.name, b.name, q.name) for q in F.subdirs(b / BRANCH)}
        for runs in sorted(root.rglob("runs")):
            if F.SKIP & set(runs.parts) or not runs.is_dir():
                continue
            parts = runs.parent.relative_to(root).parts
            if len(parts) > 1 and parts[1] == BRANCH:     # a report Page's own writing Runs
                continue
            depths[len(parts)] += 1
            for i, p in enumerate(parts[:3]):
                level[LEVELS[i]].add((pr.name,) + parts[: i + 1])
            for t in runs.iterdir():
                if t.is_file() and not t.name.startswith(("_", ".")):
                    tickets[shape(t.name)] += 1
                    examples.setdefault("Run", t.name)
                    beside += (runs.parent / "results" / t.stem).is_dir()
            for rt in runs.parent.glob("results/*/runtime.yaml"):
                receipts += 1
                m = re.search(r"^run:\s*(\S+)", rt.read_text(errors="ignore"), re.M)
                match += bool(m and m.group(1).strip("\"'") == rt.parent.name)
    for r in ("Block", "reports", "Job", "Task"):
        if level[r]:
            examples[r] = sorted(level[r])[0][-1]
    return dict(projects=projects, level=level, depths=depths, examples=examples, tickets=tickets,
                beside=beside, receipts=receipts, match=match)


def ranked(shapes):
    return sorted(shapes.items(), key=lambda kv: (-kv[1], kv[0]))      # ties in a fixed order


def fits(shapes, lvl):
    top, n = ranked(shapes)[0]
    return top.startswith(EXPECT[lvl]) and n >= 0.9 * sum(shapes.values())


# ── the table ──────────────────────────────────────────────────────────────────────────────
def draw():
    text(0, 0, "The ladder: levels across, Themes down", 40)
    text(0, 60, "Project = README.md + project.yaml; a Theme is a folder in it.  Each Theme cell is read from disk: "
                "how many fill the level, their naming shapes, one example.  Gray = a reading, not a rule.", 18, GRAY)
    X0, Y0 = 0, 120
    xs = [X0]
    for _, w in COLS:
        xs.append(xs[-1] + w)
    rows = ["definition"] + F.THEMES + [""]
    ys = [Y0, Y0 + HEAD_H, Y0 + HEAD_H + DEF_H]
    for _ in rows[1:]:
        ys.append(ys[-1] + ROW_H)
    for i, y in enumerate(ys):
        line(xs[0], y, xs[-1], y, 2 if i in (0, 1, 2, len(ys) - 1) else 1)
    for i, x in enumerate(xs):
        line(x, ys[0], x, ys[-1], 2 if i in (0, 1, len(xs) - 1) else 1)
    for (name, _), x in zip(COLS, xs):
        text(x + 16, Y0 + 16, name, 24)

    # definition row
    y = ys[1]
    text(X0 + 16, y + 14, "definition", 22)
    for i, r in enumerate(COLUMNS):
        x = xs[i + 1] + 16
        first, rest = DEFINE[r].split("\n", 1)
        text(x, y + 14, first, 16, INK, MONO)
        text(x, y + 44, rest, 17, INK)
        text(x, y + DEF_H - 34, OWNER[r], 15, GRAY)
    text(xs[-2] + 16, y + 14, NOTES["definition"], 17, GRAY)

    # one row per Theme
    for k, th in enumerate(F.THEMES):
        y = ys[k + 2]
        f = theme_facts(th)
        d = f["depths"]
        text(X0 + 16, y + 14, f"{th}/", 24, INK, MONO)
        info = f"{f['projects']} projects\n{sum(d.values())} runs/ folders"
        if d:
            main = d.most_common(1)[0][0]
            info += f"\nruns/ at depth {main}"
            other = {k2: v for k2, v in d.items() if k2 != main}
            if other:
                info += "\nalso " + ", ".join(f"depth {k2}: {v}" for k2, v in sorted(other.items()))
        text(X0 + 16, y + 54, info, 16, GRAY)
        text(xs[-2] + 16, y + 14, NOTES[th], 17, GRAY)
        for i, r in enumerate(COLUMNS):
            x = xs[i + 1] + 16
            if th == "cowork":
                text(x, y + 14, COWORK[r], 17, GRAY)
                continue
            shapes = f["tickets"] if r == "Run" else Counter(shape(p[-1]) for p in f["level"][r])
            total = sum(shapes.values())
            if not total:
                text(x, y + 14, "nothing on disk", 17, GRAY)
                continue
            word = {"Block": "Blocks", "reports": "Questions", "Job": "Jobs", "Task": "Tasks", "Run": "tickets"}[r]
            text(x, y + 12, f"{total} {word}", 20, INK)
            text(xs[i + 2] - 130, y + 16, "fits" if fits(shapes, r) else "other names", 15, GRAY)
            for j, (s, n) in enumerate(ranked(shapes)[:3]):
                text(x, y + 46 + 24 * j, clip(f"{n:>4}  {s}", 40), 15, INK, MONO)
            text(x, y + 122, clip(f"e.g. {f['examples'].get(r, '')}", 46), 14, GRAY, MONO)
            note = READING.get((th, r), "")
            if r == "Run":
                note = f"results/ beside: {f['beside']} of {total}\nrun: = stem: {f['match']} of {f['receipts']}" + \
                       (f"\n{note}" if note else "")
            if note:
                text(x, y + 146, note, 15, GRAY)
    draw_workbench(xs, ys[-1] + 140)


# ── frame 2 · the workbench on the ladder: same columns, so the two tables line up ─────────
WB_ROWS = [  # (concept, what it is, then one cell per column: Block, reports, Job, Task, Run, notes)
    ("Workbench", "one screen that opens\none ladder level",
     ["board workbench\n/w/<block>", "a report is a Page:\nits page workbench?", "none: a View\ninside the board?",
      "page workbench\non one Page folder", "none: Runs show\nin a Runs panel", "Level = board or page"]),
    ("Space", "a stage on that screen\nGuide → setup → work\n→ Delivery",
     ["Guide · Scope · Task\n· Check · Delivery", "Scope asks them,\nDelivery holds answers", "inside the Task Space",
      "the Page's own Spaces", "—", ""]),
    ("View", "a tab inside a Space",
     ["Block · Questions ·\nResources · RoadMap Draw", "one row per qNN", "one View per Job\n(register group)?",
      "?", "a run card", ""]),
    ("Run type", "one button in a Space's\nRuns panel = one Run Spec",
     ["Ask a Question\nDraw the question map", "Write the report", "Plan · Build a Task", "Run a Task\nReport the Run",
      "the Run's type", "one press allocates\none Run"]),
    ("Run", "the bottom level: one\ncommission, one Result",
     ["Block-level writes?", "reports/qNN/runs/\n(writing Runs)", "?", "tNN/runs/ + results/", "runs/<run> +\nresults/<run>/",
      ""]),
    ("Agent", "who does the run;\nnever a person",
     ["a Block agent (new)", "page agents:\nplan · write · check", "task creator", "task orchestrator ·\ncreator · reviewer",
      "the Ticket's worker", "make and judge\nare two agents"]),
    ("Skill", "how the agent does it:\none small skill per View",
     ["question-asking", "haipipe-page", "task-plan (new)", "task-run (new)", "haipipe-run", "a -workflow skill\nroutes, never a row"]),
    ("Person signs", "the decision the person\nowns, or none",
     ["the question", "release of the report?", "none", "none", "the close rule?", ""]),
    ("Folder", "where the run writes",
     ["board.md · studio/", "reports/qNN_<topic>/", "jNN_<job>/", "tNN_<task>/", "runs/ + results/", ""]),
]
WB_H = 112


def draw_workbench(xs, y0):
    width = xs[-1] - xs[0]
    ys = [y0 + 110, y0 + 110 + HEAD_H] + [y0 + 110 + HEAD_H + (i + 1) * WB_H for i in range(len(WB_ROWS))]
    FRAME[0] = None
    fr = base("frame", xs[0] - 30, y0, width + 60, ys[-1] - y0 + 40, RULE)
    fr["name"] = "Workbench on the ladder"
    FRAME[0] = fr["id"]
    text(xs[0], y0 + 24, "The workbench on the ladder: same columns, concepts down", 34)
    text(xs[0], y0 + 72, "Space · View · Run type · Run · Agent · Skill · Person signs · Folder (table-workbench), "
                         "placed at the level each one lives on.  Gray = a reading from the workbench tables; ? = open.",
         17, GRAY)
    for i, y in enumerate(ys):
        line(xs[0], y, xs[-1], y, 2 if i in (0, 1, len(ys) - 1) else 1)
    for i, x in enumerate(xs):
        line(x, ys[0], x, ys[-1], 2 if i in (0, 1, len(xs) - 1) else 1)
    for (name, _), x in zip(COLS, xs):
        text(x + 16, ys[0] + 16, name or "concept", 24)
    for r, (concept, what, cells) in enumerate(WB_ROWS):
        y = ys[r + 1]
        text(xs[0] + 16, y + 12, concept, 21)
        text(xs[0] + 16, y + 42, what, 14, GRAY)
        for c, val in enumerate(cells):
            if val:
                text(xs[c + 1] + 16, y + 14, val, 16, GRAY)
    FRAME[0] = None


if __name__ == "__main__":
    draw()
    canvas.write(Path(sys.argv[1]) if len(sys.argv) > 1 else F.BLOCK / "studio/ladder-grid.excalidraw", els,
                 "build_ladder_grid.py")
