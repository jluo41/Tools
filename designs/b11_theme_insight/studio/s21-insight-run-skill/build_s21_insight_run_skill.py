"""b11 s21 · Run and skill: s21-insight-run-skill.excalidraw, every insight Run type and the skills behind them.

JL 261007: "I am thinking we should have a s21-skills to show all the skills related to this … s21 should be
s21-run-skill, it should include both runs and skills"; then "you should follow this one" (b16's
s21-paper-run-skill). Drawn in black only (haipipe-studio's palette): lines-only tables, a decision in green and dated, red
only for work another owner must do. Seven frames, top to bottom:
  1. Runs by level: every run type a Space shows in s11 · s12 · s13, plus the Prototype Block's (no level drawing
     yet), where it stands today (a row of the workbench table, the base frame, the live theme only, drawn only),
     who does it, who checks it, its skill;
  2. one release and one data version, in order: open a version → ask · plan · script → sign → add a data version →
     add a Job → run the partitions → write and check the pages → read across Jobs → counsel and handoff, and back;
  3. the skills: each insight skill and the base skills it borrows: what it owns, the Runs that use it, how often
     it still writes an old name, what changes under plan C;
  3b. skill folders, before → after: today's tree read from disk, the proposed tree, and per file the change, what
     it does, why, and the plan phase that makes it;
  4. skill × Run: which skill each run type loads;
  5. Runs on disk: the Runs in the Project insight Blocks and register boards, by type and DIKW level (counts only;
     no Board, dataset or partition name is drawn);
  6. the skill update plan: six phases, each skill's change and the run types it gains.

Read from disk every build: the skills in skills/2_theme/insight; the level builders' SCREENS (imported, never
run); the workbench table (workbench-insight/ref/workbench-table.md, today's run types with agent, skill and
sign); the live insight theme (servers/workbench-insight: insight_theme.py, insight_views.py) and the base frame
(servers/workbench); the Runs in the Project insight folders (names only, counted by type). Typed, since they are
the proposal: the Prototype Block's run types, each skill's job and plan-C change, the owner and name of a run type
with no row yet, and the plan. canvas.write keeps every mark a person adds through a rebuild.

    python build_s21_insight_run_skill.py [out.excalidraw]
"""
import importlib.util
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True                    # importing the level builders leaves no __pycache__ behind
HERE = Path(__file__).resolve().parent
DESIGNS = HERE.parents[2]
B03 = DESIGNS / "b03_project_workbench" / "studio"
sys.path.insert(0, str(B03 / "s01-overall-tree-structure"))
sys.path.insert(0, str(B03 / "_build"))
sys.path.insert(0, str(HERE.parent / "_build"))     # the insight level builders' shared screens (insight_ui.py)
import build_ladder_v4 as L  # noqa: E402
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))  # canvas (haipipe-studio)
import canvas  # noqa: E402

SPACE = DESIGNS.parents[1]
TK = DESIGNS.parent / "plugins" / "haipipe-toolkit"
SKILLS = TK / "skills"
INSIGHT = SKILLS / "2_theme" / "insight"
TABLE = INSIGHT / "workbench-insight" / "ref" / "workbench-table.md"
LIVE = TK / "servers" / "workbench-insight"                           # the insight theme as it runs today
BASE = TK / "servers" / "workbench"                                   # the frame every theme shares
LEVELS = [("Block", "s11-block-level/build_s11_block_level.py"),
          ("Job", "s12-job-level/build_s12_job_level.py"),
          ("Task", "s13-task-level/build_s13_task_level.py")]
DATE = "261007"

# ── the typed part (proposal, 261007) ──────────────────────────────────────────────────────────
# the Prototype Block (work/bNN_<topic>_prototype/, s00): no level drawing yet, so its buttons are typed here
PROTOTYPE = [("Prototype", "Description › Proposals", "Take the proposals"),
             ("Prototype", "Work Details", "Open a version"),
             ("Prototype", "Work Details › a version", "Ask"),
             ("Prototype", "Work Details › a version", "Review the questions"),
             ("Prototype", "Work Details › a question", "Plan the evidence"),
             ("Prototype", "Work Details › a question", "Review the evidence plan"),
             ("Prototype", "Description › Partitions", "Set the cuts"),
             ("Prototype", "Work Details › a question", "Write the script"),
             ("Prototype", "Work Details › a question", "Review the script"),
             ("Prototype", "Idea Studio", "Draw the question map"),
             ("Prototype", "Delivery", "Sign a release"),
             ("Prototype", "Runs", "Carry a board over")]
# each insight skill: what it owns, and what changes under plan C ("?" = still to do, red)
SKILL_JOB = {
    "haipipe-insight": ("the door; the Block contract; its scripts (scaffold · run · carry over)",
                        "two Blocks (Prototype · Board); a Job = pN × vM; ref/insight-ladder.md + insight_ladder.py ?"),
    "haipipe-insight-workflow": ("Run Specs, GI gates, dispatch, the handoff record",
                                 "run cards by level × six Spaces; Sign a release; Run · Close a Job ?"),
    "workbench-insight": ("the served insight board and its workbench table",
                          "the theme is on the frame (insight_theme.py, insight_views.py); table from the cards ?"),
    "haipipe-insight-meta": ("the extract: what it holds (MT00)", "a data version: Add a data version ?"),
    "haipipe-insight-question": ("the question registers (MT01-MT04)",
                                 "questions live in a version Job; Take the proposals ?"),
    "haipipe-insight-data": ("what a Data answer may say", "the page of a D question in a Job"),
    "haipipe-insight-information": ("what an Information answer may say", "the page of an I question in a Job"),
    "haipipe-insight-knowledge": ("what a Knowledge answer may say; pool or split",
                                  "+ Compare with the previous Job; Check consistency ?"),
    "haipipe-insight-wisdom": ("the counsel and the Design handoff", "the handoff names its pair (pN × vM)"),
    "haipipe-insight-evidence-plan": ("a question's needs and work specs", "unchanged, in the version Job's question.md"),
    "haipipe-insight-check": ("check_block: every cell bound, fit, cited, current",
                              "+ Board readings: coverage · tracks; Close a Job ?"),
    "haipipe-insight-bind": ("answers.yaml for register boards",
                             "decided: no ladder Run uses it; kept for register boards until carried over"),
    "haipipe-page-insight": ("the task-side Insight Page and its RI Runs", "unchanged: its own route")}
# old names a skill should no longer write as current under plan C (261007)
STALE = (r"answers\.yaml|Prototype \+ Instance|one Job per (?:DIKW )?level|j0[1-4]_(?:data|information|knowledge|"
         r"wisdom)|<dataset>_<partition>\.sh|\bMT0[1-4]\b")
OLDER = re.compile(r"older|still read|legacy|historical|was |were |carry_over|carry-over|carried|retired|readable|"
                   r"register board|before it", re.I)
# the base skills insight borrows, by what they do for it
BORROWS = [("the ladder: Board · Job · studio · report", ["haipipe-board", "haipipe-job", "haipipe-studio",
                                                          "haipipe-report"]),
           ("questions: asked, shaped and reviewed", ["haipipe-question", "haipipe-question-asking",
                                                      "haipipe-question-review"]),
           ("execution: the hard Runs, their tickets, Run names by Space", ["haipipe-task", "haipipe-run"]),
           ("pages: every answering page", ["haipipe-page", "haipipe-page-workflow", "haipipe-page-check"]),
           ("supporting", ["haipipe-discovery", "table-papers", "excalidraw-report"])]
# a run type the workbench table has no row for: its owner skill (decided 261007; the plan gives each its card)
OWNER = {"Add a data version": "haipipe-insight-meta", "Add a Job": "haipipe-insight",
         "Close a Job": "haipipe-insight-workflow", "Close the Job": "haipipe-insight-workflow",
         "Run the Job": "haipipe-insight-workflow", "Propose a cut": "haipipe-insight-question",
         "Propose questions": "haipipe-insight-question", "Take the proposals": "haipipe-insight-question",
         "Update the coverage": "haipipe-insight-check", "Draw a track": "haipipe-insight-check",
         "Check consistency": "haipipe-insight-knowledge", "Compare with j02": "haipipe-insight-knowledge",
         "Ask a Block question": "haipipe-question", "Write the report": "haipipe-report",
         "Write a report": "haipipe-insight-<level>", "Check a report": "haipipe-page-check",
         "Open a version": "haipipe-insight", "Set the cuts": "haipipe-insight", "Sign a release": "haipipe-insight-workflow",
         "Open the Prototype Block ↗": "the frame", "Open the release ↗": "the frame", "Add a topic": "the frame"}
# one name per Run, run-<type>-<target> (as b16's s21); a hard Run keeps rNN_<partition>
RUN_NAME = {"Take the proposals": "run-triage-proposals-p<N>", "Open a version": "run-open-version-p<N>",
            "Ask": "run-ask-<L><NN>", "Review the questions": "run-review-questions-p<N>",
            "Plan the evidence": "run-plan-evidence-<L><NN>", "Review the evidence plan": "run-review-plan-<L><NN>",
            "Set the cuts": "run-set-cuts-p<N>", "Write the script": "run-write-script-<L><NN>",
            "Review the script": "run-review-script-<L><NN>", "Draw the question map": "run-map-questions",
            "Sign a release": "run-sign-release-p<N>", "Carry a board over": "run-carry-<board>",
            "Add a data version": "run-add-version-<d>v<M>", "Add a Job": "run-add-<jNN>",
            "Close a Job": "run-close-<jNN>", "Close the Job": "run-close-<jNN>",
            "Propose a cut": "run-propose-cut-<slug>", "Update the coverage": "run-coverage",
            "Draw a track": "run-track-<q>", "Check consistency": "run-consistency-<jA>-<jB>",
            "Ask a Block question": "run-ask-<qNN>", ("Block", "Write the report"): "run-report-<qNN>",
            ("Block", "Check a report"): "run-check-<qNN>", "Add a topic": "run-draw-<sNN>",
            "Write the counsel": "run-write-counsel", "Draft the handoff": "run-draft-handoff",
            "Write a report": "run-write-<tNN>", ("Task", "Write the report"): "run-write-<tNN>",
            "Write the Knowledge report": "run-write-<tNN>", "Check a report": "run-check-<tNN>",
            "Pool or split": "run-pool-<tNN>", "Compare with j02": "run-compare-<jNN>",
            "Propose questions": "run-propose-<jNN>", "Run a partition": "rNN_<partition> (hard)",
            "Check alignment": "run-check-alignment-<tNN>", "Run the Job": "run-launch-<jNN>",
            "Add a method": "run-add-method-<slug>", "Add a paper": "run-add-paper-<slug>",
            "Open the Prototype Block ↗": "- (a link)", "Open the release ↗": "- (a link)"}
# today's table rows renamed on the ladder (old label → new label): a table row counts for its new button
RENAMED = {"Record the extract": "Add a data version", "Register a cut": "Set the cuts",
           "Write the Data report": "Write a report", "Write the Information report": "Write a report",
           "Review an answer": "Check a report"}
# a decided skill that overrides today's table row (261007): no partition skill; a page's skill follows its level
SKILL_OVERRIDE = {"Set the cuts": "haipipe-insight", "Write a report": "haipipe-insight-<D·I·K> (its level)",
                  "Check a report": "haipipe-report"}
# a button the frame runs, and the skill the live theme names for it (insight_views.py SKILLS, with s11, 261007)
FRAME_SKILL = {"Add a topic": "haipipe-studio", "Open the release ↗": "haipipe-insight",
               "Open the Prototype Block ↗": "haipipe-insight"}
GUIDE_RUNS = {"Add a method", "Add a paper"}         # the Guide's own Runs panel (the shared frame), on every level

# 2 · one release and one data version, in order: (step, skill, note)
FLOW = [("open a version", "haipipe-insight", "j0N_pN/ from proposals/"),
        ("ask · plan · script", "-question · -evidence-plan", "a Task per question, reviewed"),
        ("sign the release", "-workflow", "a person signs pN"),
        ("add a data version", "-meta", "<d>v<M>, frozen"),
        ("add a Job", "haipipe-insight", "j0N_pN_<d>vM/"),
        ("run the partitions", "run_question.py", "hard rNN_<partition>"),
        ("write · check pages", "-data · -information · -knowledge", "one page per question"),
        ("read across Jobs", "-check · -knowledge", "coverage · tracks · consistency"),
        ("counsel · handoff", "-wisdom", "a person signs")]
# 6 · the skill update plan: (phase, skill, what it learns, run types it gains, done when)
PLAN = [("1 · contract", "haipipe-insight",
         "two special boards: Prototype (Jobs = releases), Board (Jobs = pN × vM); insight_ladder.py with its gates",
         "Open a version · Add a Job · Carry a board over (to both Blocks)", "a placeholder Project the server reads back"),
        ("2 · cards", "haipipe-insight-workflow",
         "run-cards.md by level × the six Spaces, one card per button; gates at their level",
         "a card for every run type in frame 1; the table's old rows placed or retired", "table-workbench --check"),
        ("2 · cards", "workbench-insight",
         "insight_views.py reads its run types from the cards; workbench-table.md regenerated from them",
         "every button names its skill, agent and sign", "workbench-insight and _host tests"),
        ("3 · Prototype", "haipipe-insight-question",
         "questions in a version Job; proposals/ (new · fix · retire · cut) and their triage; release.yaml",
         "Take the proposals · Ask · Propose questions · Propose a cut", "p2 cut from p1's proposals"),
        ("3 · Prototype", "haipipe-insight",
         "cuts in the release (partitions.md · thresholds.yaml); Sign a release closes the version",
         "Set the cuts · Sign a release", "a release signed and frozen"),
        ("4 · Board", "haipipe-insight-meta",
         "a dataset with dated versions in board.md; accumulates: yes · no", "Add a data version",
         "b52's extract as <d>v1"),
        ("4 · Board", "haipipe-insight-check",
         "readings across Jobs: coverage and tracks from the receipts; Close a Job checks and freezes",
         "Update the coverage · Draw a track · Close a Job", "check_block reads a Board"),
        ("5 · Job · Task", "haipipe-insight",
         "run_question.py writes runs/rNN_<partition>/ (run.yaml · result/ · passes/), pinned to pN × vM",
         "Run a partition · Run the Job", "b52 re-run as j01_p1_<d>v1"),
        ("5 · Job · Task", "haipipe-insight-knowledge",
         "Compare with the previous Job; Check consistency; pool or split on Cross",
         "Compare with j02 · Check consistency · Pool or split", "held · changed · dropped per question"),
        ("6 · old words", "all thirteen",
         "drop answers.yaml, MT0N, one Job per DIKW level, <dataset>_<partition>.sh as current (frame 3 counts)",
         "-", "0 old names; tests pass")]

# 3b · skill folders, before → after (proposal, 261007): (after path or "" to retire, change, what, why, phase)
FOLDERS = {
    "haipipe-insight/SKILL.md": ("haipipe-insight/SKILL.md", "rewrite",
        "routes Prototype Block · Board · Job · Task", "today: one Block, a Job per DIKW level", "1"),
    "haipipe-insight/ref/block-contract.md": ("haipipe-insight/ref/block-contract.md", "edit",
        "marked the older layout; its question file and script stay current", "Insight Blocks made before it are read", "1"),
    "haipipe-insight/ref/scaffold_block.py": ("haipipe-insight/ref/scaffold_block.py", "keep",
        "tickets for the older Insight Block", "b52-style Blocks, until carried into a release", "6"),
    "haipipe-insight/ref/run_question.py": ("haipipe-insight/scripts/run_question.py", "move",
        "writes runs/rNN_<partition>/ with result/ and passes/", "scripts sit in scripts/; the Run contract", "5"),
    "haipipe-insight/ref/carry_over.py": ("haipipe-insight/scripts/carry_over/carry_over.py", "move",
        "a register board → a Prototype + a Board, once", "a carry-over, not how insight is made", "6"),
    "haipipe-insight/ref/question_map.py": ("haipipe-insight/scripts/question_map.py", "move",
        "draws a version Job's questions", "scripts sit in scripts/", "3"),
    "haipipe-insight/ref/partition.md": ("haipipe-insight/ref/partition.md", "edit",
        "cuts live in the release; a Board only proposes one", "s11: a cut is part of the plan", "3"),
    "haipipe-insight/ref/board-contract.md": ("haipipe-insight/ref/board-contract.md", "keep",
        "the register boards' law, until carried over", "older boards are still read", "6"),
    "haipipe-insight-workflow/SKILL.md": ("haipipe-insight-workflow/SKILL.md", "rewrite",
        "gates and Runs by level", "Runs hang on the register's cells", "2"),
    "haipipe-insight-workflow/ref/run-workflow.md": ("haipipe-insight-workflow/ref/run-workflow.md", "edit",
        "routes between levels and between the two Blocks", "routes between registers", "2"),
    "workbench-insight/SKILL.md": ("workbench-insight/SKILL.md", "rewrite",
        "the theme on the shared frame", "it describes the old five-Space page", "2"),
    "workbench-insight/ref/workbench-table.md": ("workbench-insight/ref/workbench-table.md", "regenerate",
        "written from the run cards", "it must match the cards (table-workbench)", "2"),
    "workbench-insight/ref/insight-board.md": ("workbench-insight/ref/old-page.md", "rename",
        "the retired page: what its renderers show", "insight_theme.py still draws register boards with it", "2"),
    "folder-kinds/haipipe-insight-question/SKILL.md": ("folder-kinds/haipipe-insight-question/SKILL.md", "rewrite",
        "questions in a version Job; proposals/ triage", "the four registers MT01-MT04", "3"),
    "folder-kinds/haipipe-insight-meta/SKILL.md": ("folder-kinds/haipipe-insight-meta/SKILL.md", "edit",
        "a dataset and its dated versions", "one extract per board", "4"),
    "haipipe-insight-check/SKILL.md": ("haipipe-insight-check/SKILL.md", "edit",
        "+ Board readings; Close a Job", "readings are Runs at the Board (s11)", "4"),
    "haipipe-insight-check/ref/check_block.py": ("haipipe-insight-check/ref/check_block.py", "edit",
        "reads a Board: Jobs pin pN × vM; coverage", "today it reads one Block's cells", "4"),
    "folder-kinds/haipipe-insight-knowledge/SKILL.md": ("folder-kinds/haipipe-insight-knowledge/SKILL.md", "edit",
        "compare Jobs; consistency; pool or split", "held · changed across versions (s12)", "5"),
    "haipipe-insight-bind/SKILL.md": ("haipipe-insight-bind/SKILL.md", "keep",
        "answers.yaml, for register boards only", "decided: no ladder Run binds; retire with the last register board", "6")}
NEW_FILES = [
    ("haipipe-insight/ref/insight-ladder.md", "two special boards; a Job = pN × vM; cuts in the release; 12 rules",
     "one contract per theme, named like design-ladder.md", "1"),
    ("haipipe-insight/scripts/insight_ladder.py", "scaffold prototype · version · question · board · data · job · run",
     "a scaffold for every level, as design and paper; job writes through open_job.py", "1"),
    ("haipipe-insight/tests/test_insight_ladder.py", "the scaffold makes each level; the server reads it back",
     "the contract has teeth", "1"),
    ("haipipe-insight-workflow/ref/run-cards.md", "one card per button, by level × six Spaces",
     "every button names its skill, agent and sign", "2"),
    ("haipipe-insight/ref/release.md", "release.yaml · proposals/ · cuts · signing",
     "a Prototype version is the unit of change", "3")]
PHASES_DONE = {"1"}                                   # phase 1 done 261008 (haipipe-insight 3.0.0)

CHANGES = {
    "runs": ["new drawing, in b16's s21-paper-run-skill shape (JL 261007: \"you should follow this one\")",
             "black only (haipipe-studio 0.2.0 palette): the gray text and lines are black; red stays for open ?, green for changes",
             "the Prototype Block's run types are typed here: no level drawing shows that Block yet",
             "decided: a run type with no table row gets its owner skill and its run-<type>-<target> name here; "
             "phase 2 gives each its card",
             "decided (with s11): a cut is set in the release (Set the cuts); the Board only proposes one",
             "a Board's report is haipipe-report's (b03 261007: Question │ Work │ Report; haipipe-question keeps the asking)",
             "aligned with the live theme's skills: map (s11): Check a report = haipipe-report; Add a topic = haipipe-studio; "
             "the Open … links = haipipe-insight",
             "a frame button keeps the frame's Run name (haipipe-run ref/run-types-by-space.md): run-add-<jNN> (was "
             "run-add-job-p<N>-<d>v<M>) · run-ask-<qNN> · run-check-<qNN> · run-draw-<sNN> (was run-add-topic-<sNN>)"],
    "flow": ["new frame: one release on one data version, in order; proposals loop back to the next version"],
    "skills": ["decided: haipipe-insight-bind has no ladder Run; kept for register boards until the last is carried over",
               "decided: no new haipipe-insight-partition skill; cuts belong to haipipe-insight's release (ref/partition.md)",
               "decided: new Board and Prototype runs go to the skill whose folder they write (frame 1's skill column)"],
    "matrix": ["new frame: which skill each run type loads; x ? = decided owner, no card yet"],
    "disk": ["counts only: no Board, dataset or partition name is drawn",
             "today's hard tickets are <dataset>_<partition>.sh beside results/: plan C makes them runs/rNN_<partition>/"],
    "folders": ["new frame: the skill folders before → after, each change with its why",
                "shaped like the design and paper skills: ref/insight-ladder.md + scripts/insight_ladder.py"],
    "plan": ["new frame: the skill update plan; phases run in order, the contract and the cards first",
             "261008 phase 1 done: haipipe-insight 3.0.0 (ref/insight-ladder.md · scripts/insight_ladder.py · 5 tests); "
             "it takes in s11's real build (tasks/Prototype-bNN-<Topic>, insights/Insight-<name>, open_job.py)",
             "261008 decided: one clock per Job · a release per triaged batch · a kept question reruns on a "
             "code-moved Job (the compare checks its tables' sha256)",
             "? the real release p1 runs unsigned: a person signs it (state closed, signed ✅ <YYMMDD>)"]}


# ── helpers, as b16's s21 draws them ──────────────────────────────────────────────────────────
def table(x, y, cols, rows, size=15, row_h=34, mono=("folder", "skill")):
    """A lines-only table: a header, then one row each; a cell ending in "?" is red. Returns its bottom."""
    w = sum(cw for _, cw in cols)
    cx = x
    for name, cw in cols:
        L.text(cx + 8, y + 8, name, size - 1, L.INK)
        cx += cw
    L.path([(x, y + row_h), (x + w, y + row_h)], arrow=False, color=L.INK)
    for i, row in enumerate(rows):
        ry = y + row_h * (i + 1)
        cx = x
        for (name, cw), cell in zip(cols, row):
            font = L.MONO if name in mono else L.SANS
            L.text(cx + 8, ry + 8, cell, size, L.RED if cell.endswith("?") else L.INK, font)
            cx += cw
        L.path([(x, ry + row_h), (x + w, ry + row_h)], arrow=False, color=L.INK)
    return y + row_h * (len(rows) + 1)


def notes(x, y, lines):
    """Work another owner must do in red ("?"), then what was decided or changed, in green and dated."""
    for k, n in enumerate(lines):
        if n.startswith("?"):
            L.text(x, y + k * 26, n, 16, L.RED)
        else:                                         # a note may carry its own date: "261008 …"
            dated = re.match(r"^(\d{6}) (.*)$", n)
            L.text(x, y + k * 26, f"✎ {dated.group(1)}  {dated.group(2)}" if dated else f"✎ {DATE}  {n}", 16, L.GREEN)
    return y + len(lines) * 26


def bottom():
    return max(e["y"] + e.get("height", 0) for e in L.els)


# ── facts, read from disk ──────────────────────────────────────────────────────────────────────
def callers(name):
    """Files in the toolkit outside 2_theme/insight that name a skill."""
    out = subprocess.run(["grep", "-rlIw", "--exclude-dir=.git", "--exclude-dir=_legacy", "--exclude-dir=venue",
                          "--exclude=CHANGELOG.md", name, str(TK)], capture_output=True, text=True).stdout.split()
    return [o for o in out if not o.startswith(str(INSIGHT))]


def stale(d):
    """How many lines of a skill's docs still write a plan-C-retired name as if current."""
    n = 0
    for f in d.rglob("*.md"):
        if f.name == "CHANGELOG.md":
            continue
        lines, older = f.read_text(encoding="utf-8", errors="ignore").splitlines(), False
        for i, line in enumerate(lines):
            nxt = lines[i + 1] if i + 1 < len(lines) else ""
            if line.startswith("#") or (line.strip() and re.fullmatch(r"[-=]{3,}", nxt.strip())):
                older = bool(OLDER.search(line))
            if re.search(STALE, line) and not older and not OLDER.search(line) and not (i and OLDER.search(lines[i - 1])):
                n += 1
    return n


def find_skill(name):
    return next((p for p in SKILLS.rglob(name) if (p / "SKILL.md").is_file()), None)


def insight_skills():
    return sorted((p for p in INSIGHT.rglob("SKILL.md")), key=lambda p: p.parent.name)


def table_rows():
    """Today's run types, from the workbench table: {run type: {space, agent, skill, signs, folder}}."""
    out = {}
    for line in TABLE.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 8 or cells[0] in ("Level", "") or set(cells[0]) <= {"-", ":"} or cells[3] == "none":
            continue
        out[cells[3]] = {"space": f"{cells[1]} › {cells[2]}", "agent": cells[4], "skill": cells[5],
                         "signs": cells[6], "folder": cells[7]}
    return out


def agent_exists(name):
    return any(TK.rglob(name.split()[0] + ".md"))


def thirds(t):
    """The views a screen has open: its third row, or its rows (Partition: … · Reading: …)."""
    if not t:
        return []
    rows = t if isinstance(t[0], list) else [t]
    return [lb for row in rows for lb, on in row if on and not str(lb).endswith(":") and lb != "All"]


def designed():
    """Every run type a screen shows in s11 · s12 · s13, then the Prototype Block's: [(level, where, label)]."""
    out = []
    for level, rel in LEVELS:
        spec = importlib.util.spec_from_file_location(f"s21_{level}", HERE.parent / rel)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)                       # the builders draw only under __main__
        for e in m.SCREENS:                              # (space, third row(s), run types, recent, body, files)
            on = [v for v in thirds(e[1]) if not v.startswith("<partition")]
            out += [(level, e[0] + (f" › {' · '.join(on)}" if on else ""), r) for r in e[2]]
    out = PROTOTYPE + out
    seen, uniq = set(), []
    for lv, where, r in out:
        key = (lv, where, r)
        if key not in seen:
            seen.add(key)
            uniq.append(key)
    return uniq


def said(label, code):
    """A button label written as a string in the code."""
    return re.search(r"[\"']" + re.escape(label) + r"[\"' ]", code) is not None


def run_rows():
    """Frame 1's rows per level, each run type with where it stands today; the tally per level."""
    rows_today = table_rows()
    by_new = {}
    for old, row in rows_today.items():
        by_new.setdefault(RENAMED.get(old, old), row)
    live = "\n".join(p.read_text(encoding="utf-8") for p in LIVE.glob("insight_*.py"))
    base = "\n".join(p.read_text(encoding="utf-8") for p in BASE.glob("*.py"))
    by_level, tally, used, merged = {}, {}, set(), {}
    for lv, where, label in designed():
        c = by_new.get(label)
        owner = OWNER.get(label, "?").replace("<level>", "<D·I·K>")
        name = RUN_NAME.get((lv, label)) or RUN_NAME.get(label) or "-"
        if c:
            used.add(label)
            st, skill, agent, signs = "table", SKILL_OVERRIDE.get(label, c["skill"]), c["agent"], c["signs"]
            agent = agent if "(new)" in agent or agent_exists(agent) else agent + " (no file) ?"
            skill = skill.replace(" (new)", " (new) ?")
        elif owner == "the frame":
            st, skill, agent, signs = "base", FRAME_SKILL.get(label, "the frame"), "-", "-"
        else:
            st = "live ?" if said(label, live) else "drawn ?"
            skill, agent, signs = f"{owner} ?", "?", "?"
        row = merged.get((lv, name))
        if row is None:
            merged[(lv, name)] = row = [name, label, where, st, agent, signs, skill]
            by_level.setdefault(lv, []).append(row)
        else:
            row[1] = row[1] if label in row[1].split(" · ") else f"{row[1]} · {label}"
            row[2] = row[2] if where in row[2].split(" · ") else f"{row[2]} · {where}"
    for lv, rows in by_level.items():
        tally[lv] = Counter(r[3].rstrip(" ?") for r in rows)
    left = [(old, r) for old, r in rows_today.items() if RENAMED.get(old, old) not in used]
    return by_level, tally, left


# Runs on disk: the Project insight folders (an Insight Block in tasks/, a register board in insights/)
def insight_runs():
    """Every Run stem in a Project insight folder, typed, with its DIKW level; names never leave this function."""
    folders = [p for p in SPACE.glob("examples-*/*/tasks/b5*_dikw") if p.is_dir()]
    folders += [p for p in SPACE.glob("examples-*/*/insights/*-InsightBoard") if p.is_dir()]
    folders += [p for p in SPACE.glob("examples-*/*/insights/Insight-*") if p.is_dir()]       # plan C Boards (261008)
    folders += [p for p in SPACE.glob("examples-*/*/tasks/Prototype-*") if p.is_dir()]      # plan C Prototypes
    found = []
    for f in folders:
        for d in f.rglob("runs"):
            if not d.is_dir() or {"_old", "_legacy"} & set(d.parts):
                continue
            task = next((m.group(1) for part in d.relative_to(f).parts
                         for m in [re.match(r"^t\d+_([DIKW])\d\d_", part)] if m), "")
            lvl = {"D": "data", "I": "information", "K": "knowledge", "W": "wisdom"}.get(task) or next(
                (w for w in ("data", "information", "knowledge", "wisdom", "meta") if
                 any(w in part for part in d.relative_to(f).parts)), "board")
            for r in d.iterdir():
                stem = re.sub(r"\.(md|sh|yaml)$", "", r.name)
                if stem.startswith("run-"):
                    kind = "run-" + stem.split("-")[1] + "-…"
                elif re.match(r"^r\d", stem):
                    kind = "rNN_<partition>"
                elif r.suffix == ".sh" and "_" in stem:
                    kind = "<dataset>_<partition>.sh"
                else:
                    continue
                found.append((kind, lvl))
    return found, len(folders)


def insight_files():
    """Every file in 2_theme/insight today; CHANGELOGs, caches and tests left out."""
    out = []
    for f in sorted(INSIGHT.rglob("*")):
        rel = f.relative_to(INSIGHT)
        if f.is_file() and f.name != "CHANGELOG.md" and not {"__pycache__", ".git"} & set(rel.parts):
            out.append(rel.as_posix())
    return sorted(out, key=lambda p: p.split("/"))


def tree(paths, tag=lambda p: ""):
    lines, seen = [], set()
    for p in paths:
        parts = p.rstrip("/").split("/")
        for k in range(len(parts)):
            key = "/".join(parts[:k + 1])
            if key in seen:
                continue
            seen.add(key)
            leaf = k == len(parts) - 1
            name = parts[k] + ("/" if not leaf or p.endswith("/") else "")
            lines.append(("    " * k + name + ("   " + tag(p) if leaf and tag(p) else ""), p if leaf else None))
    return lines


def draw_tree(x, y, title, lines, color):
    L.text(x, y, title, 20)
    for k, (line, p) in enumerate(lines):
        L.text(x, y + 40 + k * 22, line, 14, color(p) if p else L.INK, L.MONO)
    return y + 40 + len(lines) * 22


# ── the drawing ────────────────────────────────────────────────────────────────────────────────
def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s21-insight-run-skill.excalidraw"
    L.els.clear()
    L.FRAME[0] = None
    by_level, tally, left = run_rows()
    levels = ("Prototype", "Block", "Job", "Task")

    # 1 · Runs by level
    fr = L.open_frame("Runs by level")
    L.text(0, 0, "Insight Runs, level by level", 30)
    L.text(0, 46, "the Prototype Block (typed: no level drawing yet), then every Run a Space's buttons make in s11 · s12 · "
                  "s13, one row per Run, named run-<type>-<target> · today: table = a row of workbench-table.md names its "
                  "skill, agent and sign · base = the shared frame · live = the insight theme shows the button, no row "
                  "says who runs it · drawn = only in the drawing · red ? = no card yet", 16, L.INK)
    cols = [("Run", 400), ("button", 330), ("shows in", 470), ("today", 90), ("who does it", 330),
            ("who checks", 200), ("skill", 330)]
    y = 110
    for level in levels:
        t = tally[level]
        L.text(0, y, level, 20)
        L.text(0, y + 30, "\n".join(f"{t[k]} {k}" for k in ("table", "base", "live", "drawn") if t[k]), 14, L.INK)
        y = table(130, y - 4, cols, by_level[level], mono=("Run", "skill")) + 30
    L.text(0, y + 10, "today's table rows no level screen shows", 20)
    rows = [[old, r["space"], r["skill"], "decided: kept, the Guide's own Runs panel on every tab" if old in GUIDE_RUNS
             else "place it in a Space or retire it ?"] for old, r in left]
    y = table(130, y + 46, [("run type", 300), ("today's Space › view", 380), ("skill", 300), ("decided", 460)],
              rows) + 40
    runnable = {lv: (t["table"] + t["base"]) * 100 // max(1, sum(t.values())) for lv, t in tally.items()}
    L.text(0, y, "runnable today (a table row or the frame): " + " · ".join(f"{lv} {p}%" for lv, p in runnable.items()),
           18)
    notes(0, y + 50, ["? the Prototype Block has no level drawing: a session drawing it (as s11 · s12 · s13) should "
                      "show these buttons"] + CHANGES["runs"])
    L.close_frame(fr, pad=40)

    # 2 · one release and one data version, in order
    y = bottom() + 200
    fr = L.open_frame("one Job, in order")
    L.text(0, y, "One release on one data version, in order: each step and its skill", 30)
    fx, fy = 0, y + 170
    for k, (step, skill, note) in enumerate(FLOW):
        L.base("rectangle", fx, fy, 260, 64, L.INK, 1.5)
        L.text(fx + 16, fy + 18, step, 20)
        L.text(fx, fy + 80, skill, 14, L.INK, L.MONO)
        L.text(fx, fy + 104, note, 14, L.INK)
        if k < len(FLOW) - 1:
            L.path([(fx + 268, fy + 32), (fx + 332, fy + 32)], color=L.INK)
        fx += 340
    lx, ox = 7 * 340 + 130, 130                        # read across Jobs → proposals → the next version
    L.path([(lx, fy - 4), (lx, fy - 50), (ox, fy - 50), (ox, fy - 4)], color=L.INK, dashed=True)
    L.text(ox + 40, fy - 80, "proposals (new · fix · retire · a cut) go to the Prototype's proposals/ and open the "
                             "next version; new data alone makes a new Job, no release", 14, L.INK)
    L.text(0, fy + 150, "a person signs each release and the handoff; an agent that did not write them reviews the "
                        "questions, the plans, the scripts and every page", 16, L.INK)
    notes(0, fy + 190, CHANGES["flow"])
    L.close_frame(fr, pad=40)

    # 3 · the skills
    y = bottom() + 200
    fr = L.open_frame("the skills")
    L.text(0, y, "The skills behind the Runs", 30)
    L.text(0, y + 46, "skills/2_theme/insight/ · callers = files elsewhere in the toolkit that name it · old = lines that "
                      "still write answers.yaml, MT0N, one Job per DIKW level or <dataset>_<partition>.sh as current", 16,
           L.INK)
    uses, rows_by_skill = Counter(), {}
    for rows in by_level.values():
        for r in rows:
            sk = r[6].rstrip(" ?")
            uses[sk] += 1
            rows_by_skill.setdefault(sk, []).append(r[0])
    rows = []
    for f in insight_skills():
        d = f.parent
        s = f.read_text(encoding="utf-8")
        v = re.search(r'version: "?([\d.]+)', s)
        owns, plan_c = SKILL_JOB.get(d.name, ("?", "?"))
        dik = d.name in ("haipipe-insight-data", "haipipe-insight-information", "haipipe-insight-knowledge")
        names = sorted(set(n for k, v2 in rows_by_skill.items()
                           if k == d.name or (dik and k == "haipipe-insight-<D·I·K>") for n in v2))
        joined = " · ".join(names)
        rows.append([d.name, "v" + (v.group(1) if v else "?"), str(len(callers(d.name))), owns,
                     (joined[:58] + (" …" if len(joined) > 58 else "")) or "-", str(stale(d)), plan_c])
    y2 = table(0, y + 100, [("skill", 320), ("version", 90), ("callers", 80), ("owns", 520),
                            ("Runs that use it", 560), ("old", 60), ("under plan C", 640)], rows)
    rows = []
    for group, names in BORROWS:
        for n in names:
            p = find_skill(n)
            rows.append([n, group if n == names[0] else "", p.parent.relative_to(SKILLS).as_posix() + "/" if p
                         else "not found ?", str(uses.get(n, 0) or "-")])
    y2 = table(0, y2 + 60, [("skill", 320), ("borrowed for", 440), ("where", 400), ("Runs", 80)], rows)
    agents = sorted({r[4].split(" (")[0] for rows in by_level.values() for r in rows if r[4] not in ("-", "?")})
    y2 = table(0, y2 + 60, [("agent", 420), ("on disk", 200)],
               [[a, "yes" if agent_exists(a) else "missing ?"] for a in agents], mono=("agent",))
    notes(0, y2 + 30, CHANGES["skills"])
    L.close_frame(fr, pad=40)

    # 3b · skill folders, before → after
    y = bottom() + 200
    fr = L.open_frame("skill folders: before → after")
    L.text(0, y, "The skill folders, before → after: what changes, and why", 30)
    L.text(0, y + 46, "skills/2_theme/insight/ · before = today, read from disk · after = the plan · a file with no row "
                      "is kept as it is · state = to do until its phase runs", 16, L.INK)
    before = insight_files()
    missing = [p for p in FOLDERS if p not in before]
    after = sorted({FOLDERS[p][0] if p in FOLDERS else p for p in before} - {""} | {p for p, *_ in NEW_FILES},
                   key=lambda p: p.split("/"))
    verb_of = {FOLDERS[p][0]: FOLDERS[p][1] for p in FOLDERS if FOLDERS[p][0]}
    verb_of.update({p: "new" for p, *_ in NEW_FILES})
    yb = draw_tree(0, y + 110, "before · today", tree(before, lambda p: FOLDERS[p][1] if p in FOLDERS else ""),
                   lambda p: L.INK)
    ya = draw_tree(1100, y + 110, "after · proposed", tree(after, lambda p: verb_of.get(p, "")),
                   lambda p: L.INK)
    L.path([(900, y + 200), (1040, y + 200)], color=L.INK)
    rows = [[p, FOLDERS[p][0] or "-", FOLDERS[p][1], FOLDERS[p][2], FOLDERS[p][3], FOLDERS[p][4],
             "done" if FOLDERS[p][4] in PHASES_DONE else "to do"] for p in FOLDERS if p in before]
    rows += [["-", p, "new", what, why, ph, "done" if ph in PHASES_DONE else "to do"] for p, what, why, ph in NEW_FILES]
    rows.sort(key=lambda r: r[5])
    yt = table(0, max(yb, ya) + 80, [("before", 520), ("after", 520), ("change", 110), ("what", 480),
                                      ("why", 480), ("phase", 70), ("state", 90)], rows, size=14,
               mono=("before", "after"))
    keep = len([p for p in before if p not in FOLDERS])
    notes(0, yt + 30, [f"kept as they are: {keep} files (no change word beside them in either tree)"] +
          [f"? named here but not on disk: {p}" for p in missing] + CHANGES["folders"])
    L.close_frame(fr, pad=40)

    # 4 · skill x Run
    y = bottom() + 200
    fr = L.open_frame("skill x Run")
    L.text(0, y, "Which skill each Run loads", 30)
    L.text(0, y + 46, "x = today's table names the skill · x ? = decided owner, no card yet", 16, L.INK)
    names = ["haipipe-insight", "-workflow", "-question", "-evidence-plan", "-meta", "-<D·I·K>", "-knowledge",
             "-wisdom", "-check"]
    full = ["haipipe-insight"] + ["haipipe-insight" + n for n in names[1:]]
    cols = [("Run", 520)] + [(n, 130) for n in names] + [("other", 300)]
    rows = []
    for lv in levels:
        for r in by_level[lv]:
            sk = r[6].rstrip(" ?").replace(" (new)", "").replace(" (its level)", "")
            mark = "x ?" if r[6].endswith("?") else "x"
            hit = [mark if sk == f or (f.endswith("<D·I·K>") and sk in ("haipipe-insight-data",
                                                                          "haipipe-insight-information",
                                                                          "haipipe-insight-<D·I·K>"))
                   else "" for f in full]
            rows.append([f"{lv} · {r[0]}"] + hit + ["" if any(hit) else (sk + (" ?" if mark != "x" else ""))])
    table(0, y + 90, cols, rows, mono=("Run",))
    notes(0, bottom() + 30, CHANGES["matrix"])
    L.close_frame(fr, pad=40)

    # 5 · Runs on disk
    y = bottom() + 200
    fr = L.open_frame("Runs on disk")
    found, n_folders = insight_runs()
    L.text(0, y, f"The Runs in the {n_folders} Project insight folders today", 30)
    L.text(0, y + 46, "run type · DIKW level · count; counts only, no Board, dataset or partition is named", 16, L.INK)
    by_type = Counter(found)
    rows = [[t, lvl, str(k) + (" ?" if t.endswith(".sh") else "")]
            for (t, lvl), k in sorted(by_type.items(), key=lambda x: (-x[1], x[0]))]
    yb = table(0, y + 100, [("run type", 320), ("DIKW level", 160), ("count", 90)], rows, mono=("run type",))
    yn = table(800, y + 100, [("family", 220), ("name", 470), ("note", 470)], [
        ["a partition (hard)", "rNN_<partition>/", "one per cut, in a question's Task; result/ · passes/"],
        ["a question's page", "run-write-<tNN> · run-check-<tNN>", "the Page's own Runs"],
        ["a Job", "run-launch-<jNN> · run-compare-<jNN> · run-close-<jNN>", "soft, in the Job's runs/"],
        ["a Board reading", "run-coverage · run-track-<q> · run-consistency-<jA>-<jB>", "soft, in the Board's runs/"],
        ["the Prototype", "run-open-version-p<N> · run-sign-release-p<N>", "soft, in the Prototype Block"],
        ["old, still read", "<dataset>_<partition>.sh beside results/", "today's tickets; re-cut by phase 5"]],
        mono=("name",))
    notes(0, max(yb, yn) + 30, CHANGES["disk"])
    L.close_frame(fr, pad=40)

    # 6 · the skill update plan
    y = bottom() + 200
    fr = L.open_frame("skill update plan")
    L.text(0, y, "The skill update plan: every button above gets an owner", 30)
    L.text(0, y + 46, "phases in the order they unblock each other: the contract and the cards first, so each later "
                      "skill has a folder to write and a card to answer", 16, L.INK)
    yp = table(0, y + 100, [("phase", 160), ("skill", 300), ("what it learns", 860), ("run types it gains", 620),
                            ("done when", 320)],
              [[f"{p[0]} ✓" if p[0].split(" ")[0] in PHASES_DONE else p[0], *p[1:]] for p in PLAN])
    notes(0, yp + 30, CHANGES["plan"])
    L.close_frame(fr, pad=40)
    off = canvas.off_palette(L.els)
    if off:
        print(f"{len(off)} elements outside the studio palette (black, red, green)")
    canvas.write(out, list(L.els), "build_s21_insight_run_skill.py")


if __name__ == "__main__":
    main()
