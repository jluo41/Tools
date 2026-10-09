"""b17 s01 · work ladder: s01-work-ladder.excalidraw: every work row in one drawing, Block down to Run.

First frame, "work ladder · Q01": this Block's answer to Q01 (261007), drawn here and argued in
reports/q01_work_ladder/: each level's folder and its six Spaces in one grid, where each of today's
Task workbench views goes, the run types each level's runs/README.md lists, and the open points in red.
Then the work rows of b03's s06 (Blocks), s07 (Jobs) and s08 (Tasks), together (JL 261007), drawn from
the shared definitions (b03's studio/s01-overall-tree-structure/); edit those rows there. canvas.write
keeps every mark a person adds.

    python build_s01_work_ladder.py [out.excalidraw]
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
B03 = HERE.parents[3] / "b01_haipipe-toolkit" / "j03_project_workbench" / "studio"      # the shared definitions and canvas.write live in b03
sys.path.insert(0, str(B03 / "s01-overall-tree-structure"))
sys.path.insert(0, str(B03 / "_build"))
import build_ladder_v4 as L  # noqa: E402
sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))  # canvas (haipipe-studio)
import canvas  # noqa: E402
import level_views as LV  # noqa: E402
import theme_ladder  # noqa: E402

# ── the answer: one row per level, one column per Space ("?" = open, red) ──────────────────────
SPACES = ["Description", "Idea Studio", "Audience Report", "Work Details", "Runs", "Delivery", "Run types panel"]
# the blockers (b03 s01-D23): solid lines at the edges and before Description | Idea Studio · Audience Report |
# Work Details | Runs · Delivery | the panel; dashed inside a group
BLOCKERS = {0, 1, 2, 4, 5, 7, 8}
GRID = [
    ("Block", "bNN_<topic>/", [
        "bNN_<topic>.md   (was board.md)", "studio/sNN-<topic>/", "reports/qNN_<topic>/", "related/related.md",
        "runs/  soft only + README.md", "delivery/  optional", "jNN_<job>/ …"], [
        ["the face: spine · close ·", "the Question register", "third row:", "Scope · Resources · Related"],
        ["one drawing after another,", "no third row", "s01-question-map: generated", "from the register, view only"],
        ["one row per Question:", "Question │ Work │ Report", "Work = j · t · r it reads", "third row: the question",
         "groups (register group:)"],
        ["Jobs ▾, each open to its Tasks", "a row: Plan · Build · Run ·", "Report chips, waits, stale",
         "third row: the Job series", "j0N · j1N · j5N …"],
        ["its own soft Runs:", "run-draw- · run-report-", "run-check-qNN · run-delivery-", "☐ from below: its Tasks'",
         "hard Runs; third row = types"],
        ["optional (dashed)", "its own: built reports", "from below: released", "reports of its Tasks"],
        ["Ask a Question", "Review the questions", "Add a resource · Draw", "Draw the question map",
         "Write · Check · Build the report"]]),
    ("Job", "jNN_<job>/", [
        "jNN_<job>.md   (today: diagram/)", "src/ · sbatch/ · CODE_REVIEW.md", "studio/  optional",
        "runs/  soft only + README.md", "delivery/  optional", "tNN_<task>/ …"], [
        ["the face: goal · state · next", "task_groups: t0N · t1N", "? third row:", "? Scope · Shared code"],
        ["optional (dashed)", "diagram/*.excalidraw", "→ studio/s01-<topic>/"],
        ["? no reports/ at a Job:", "? the Block's Question rows", "? this Job's Tasks feed (a filter)"],
        ["its Tasks: Plan · Build ·", "Run · Report chips", "third row: task groups", "pick a Task → the Task tab"],
        ["its own soft Runs:", "run-plan-tasks", "run-review-src", "run-launch-<group> (sbatch/)", "☐ from below"],
        ["optional (dashed)", "an export its Tasks share", "from below"],
        ["Plan its Tasks", "Review the shared code", "Launch a group", "Update the Job"]]),
    ("Task", "tNN_<task>/", [
        "tNN_<task>.md   the Task Page", "scripts/<worker>.py · CODE_REVIEW.md", "runs/  hard rNN_ + soft run-",
        "notebooks/rNN_<run>.ipynb  generated", "workflow/  plan.yaml · report.yaml", "studio/ · sbatch/  optional",
        "delivery/  optional"], [
        ["its Page: goal · plan", "inputs → worker → Runs", "close: what it must find", "third row: Scope · Plan"],
        ["optional (dashed)", "e.g. the analysis flow"],
        ["Question │ Work │ Report,", "this Task's Questions only", "third row: Draft · Report",
         "? Report = the Block's qNN", "? Page, not a Task Page"],
        ["how the work is done", "third row:", "Code · Review · Notebooks"],
        ["hard rNN_<slug>/ (evidence)", "soft run-build- · run-report-", "· run-check-<task>",
         "third row: All · run · build", "· report · check"],
        ["no third row: cards", "Reports · Exports", "(today's style)"],
        ["Plan a Task · Review the plan", "Build the Task", "Review the Task code", "Run a Task (hard)",
         "Report the Run · Check a Task"]]),
    ("Run", "runs/rNN_<slug>/", [
        "run.yaml   the card", "rNN_<slug>.sh   the ticket", "config.yaml   frozen inputs",
        "result/   generated · heavy.yaml", "passes/pNN-<MMDD>/  log · runtime.yaml", "(today: runs/rNN.sh",
        " + results/rNN/)"], [
        ["no tab: a pop-out from", "Task › Runs (or Block › Runs,", "from below)", "card · ticket · config"],
        ["—"],
        ["result/ preview:", "metrics · tables · figures"],
        ["passes: one per execution", "of the same ticket", "new inputs = a new rNN"],
        ["a soft Run: run-<type>-<target>/", "run.yaml · .md · passes/", "writes into its scope's items"],
        ["—  (a Result is light;", "heavy → ProjectResult)"],
        ["Rerun (a new pass)", "Open the Result", "? dry: code on data", "? wet: a protocol, a signed receipt"]]),
]
# today's Task workbench (board level) → where each view goes
MOVES = [("Guide › its 4 views", "Guide, unchanged"),
         ("Scope › Block", "Block › Description › Scope"),
         ("Scope › Questions", "Block › Audience Report (the rows); the register stays in the face"),
         ("Scope › Resources", "Block › Description › Resources"),
         ("Scope › RoadMap Draw", "Block › Idea Studio (the question map: a generated topic)"),
         ("Task › <group A> · <group B>", "Block › Audience Report, its third row"),
         ("Task › a row's Task Work tree", "Block › Work Details (Jobs ▾ Tasks)"),
         ("Task › Not under a Question", "Work Details: a Task with no Question chip"),
         ("Task › Plan · Build · Run · Report buttons", "the Task tab's Run types"),
         ("Check › Runs", "Block › Runs, ☐ from below"),
         ("Check › Tasks", "state chips on Work Details rows; Check a Task = run-check-<task>"),
         ("Check › Reports", "run-check-qNN in Block › Runs; the release check in Delivery"),
         ("Delivery › Reports", "Block › Delivery"),
         ("a Task's 'Task Page' link (pop-out)", "the Task tab"),
         ("(no Job screen today)", "the Job tab")]
OPEN = ["1  the frame gives every level the six Spaces, the Job too (b02, 261007); open: what work fills",
        "   at Job beyond vanilla (Scope · Shared code)? b03's work Job row still draws Overview · Studio · Reports",
        "2  Job › Audience Report: a filter of the Block's Questions, no reports/ at a Job?",
        "3  Task › Audience Report: the Block's qNN Page, or a Task Page of its own? (Q03)",
        "   today some Tasks keep a Page in workflow/ (qNN_<topic>.md · page.toml)",
        "4  a Task's draft/records/ and workflow/: kept, or folded into runs/ and the face? (Q02)",
        "5  notebooks/rNN_<run>.ipynb: stays in the Task, or moves into runs/rNN_<slug>/?",
        "6  Page Job and Page Task are not work rows: no work Block on disk has one;",
        "   a Page Task is the base's Task level (servers/workbench/task). Drop them here?",
        "7  the Job series j0N · j1N · j5N: read from the face (job_groups:), never hard-coded?",
        "8  a Run opens as a pop-out, not a fifth tab?",
        "9  a wet Task (a protocol run by a person): ticket + signed receipt in the same runs/rNN_/?"]
COL_W = [330, 260, 280, 290, 290, 330, 290, 300]   # level · folder, then the six Spaces, then the panel
LH = 20


def cell(x, y, lines, size=14, font=L.SANS):
    for k, s in enumerate(lines):
        L.text(x + 12, y + 10 + k * LH, s.lstrip("? ") if s.startswith("?") else s, size,
               L.RED if s.startswith("?") else L.INK, font)


def grid(x, y):
    """The ladder: a row per level, its folder on the left, a column per Space; returns its bottom."""
    xs = [x]
    for w in COL_W:
        xs.append(xs[-1] + w)
    L.text(x + 12, y + 10, "level · folder", 15, L.GRAY)
    for i, name in enumerate(SPACES):
        L.text(xs[i + 1] + 12, y + 10, name, 15, L.INK)
    top, ry = y, y + 40
    L.path([(x, ry), (xs[-1], ry)], arrow=False, color=L.INK)
    for level, folder, tree, spaces in GRID:
        h = max(len(tree) + 2, *(len(c) for c in spaces)) * LH + 24
        L.text(x + 12, ry + 10, level, 18, L.INK)
        L.text(x + 90, ry + 12, folder, 14, L.INK, L.MONO)
        cell(x, ry + 30, tree, 12, L.MONO)
        for i, c in enumerate(spaces):
            cell(xs[i + 1], ry, c)
        ry += h
        L.path([(x, ry), (xs[-1], ry)], arrow=False, color=L.GRAY)
    for i, cx in enumerate(xs):
        heavy = i in BLOCKERS
        L.path([(cx, top), (cx, ry)], arrow=False, color=L.INK if heavy else L.GRAY, dashed=not heavy)
    return ry


def answer(y=0):
    fr = L.open_frame("work ladder · Q01")
    L.text(0, y, "Q01 · How does work climb the ladder?  proposed answer, open until JL settles it", 30)
    L.text(0, y + 46, "Each level of the work Theme: its folder (left) and its six Spaces, the same at every level "
                      "(b03 s01-D20, D22); the Run types panel on the right lists the buttons. Red = open.", 16, L.GRAY)
    bot = grid(0, y + 100)
    ty = bot + 80
    L.text(0, ty, "today's Task workbench (board level) → where each view goes", 20, L.INK)
    for k, (a, b) in enumerate(MOVES):
        L.text(0, ty + 40 + k * 26, a, 15, L.GRAY)
        L.text(390, ty + 40 + k * 26, "→  " + b, 15, L.INK)
    ox = 1500
    L.text(ox, ty, "open", 20, L.RED)
    for k, s in enumerate(OPEN):
        L.text(ox, ty + 40 + k * 26, s, 15, L.RED)
    qy = ty + 40 + len(OPEN) * 26 + 40
    L.text(ox, qy, "this Block's questions", 18, L.INK)
    for k, (qid, title) in enumerate(theme_ladder.questions(HERE.parents[1] / "board.md")):
        L.text(ox, qy + 34 + k * 26, f"{qid}  {title}", 15, L.RED if qid != "Q01" else L.INK)
    L.close_frame(fr, pad=40)
    return theme_ladder.bottom()


def draw(out):
    L.els.clear()
    L.FRAME[0] = None
    y = answer() + 260
    for title, trees, fam, level, block in [("Board level", L.BLOCK_TREES, L.BLOCK_FAMILY, "Block", True),
                                            ("Job level", L.JOB_TREES, LV.JOB_FAMILY, "Job", False),
                                            ("Task level", L.TASK_TREES, LV.TASK_FAMILY, "Task", False)]:
        rows = [t for t in trees if fam.get(t[0]) == "task"]
        if rows:
            L.draw_trees(f"work · {title}", theme_ladder.SUB, rows, y, frame_each=True, views=LV.rows(level),
                         block=block)
            y = theme_ladder.bottom() + 260
    canvas.write(out, list(L.els), "build_s01_work_ladder.py")


if __name__ == "__main__":
    draw(Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s01-work-ladder.excalidraw")
