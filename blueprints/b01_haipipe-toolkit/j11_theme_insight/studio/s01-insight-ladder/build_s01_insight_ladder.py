"""b11 s01 · Insight ladder: s01-insight-ladder.excalidraw: plan A and plan B in the workbench UI.

The insight rows of b03's s11-block-variants (Blocks), s12-job-variants (Jobs) and s13-task-variants (Tasks), each frame named for its level
(JL 261007), with the two plans side by side: A · DIKW on the board (a DIKW level is a group of Board ›
Work Details, no Job tab) and B · DIKW in the Jobs (a DIKW level is a Job with the Block's six Spaces).
Each frame: the folder, its skills, then the proposed screens with today's beneath them.

Cleaned 261007 (JL: "could you reorganize this?", "make it clean and use the red color to show the
one I should pay attention"; then "where is my original workbench UI?", "I want to see the plan A and
plan B how to fit the workbench UI"): the UI screens stay as drawn; a short Decide frame goes first
(the ladder and the open points ① to ⑦ with my answers); frames sit 300 apart, so no title runs into
the frame above; the Board rows drop their three empty Description columns (People · Venue,
Resources, Related: nothing for insight); a "differs:" line (today against proposed) is gray; red is
left only on the open points, each tagged with its number.

The trees, skills and screens of B and of the Task level come from b03's
studio/s01-overall-tree-structure/build_ladder_v4.py and level_views.py; option A and the cleanup are
this drawing's own. The canvas writer keeps every mark a person adds through a rebuild.

    python build_s01_insight_ladder.py [out.excalidraw]
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
B03 = HERE.parents[3] / "b01_haipipe-toolkit" / "j03_project_workbench" / "studio"      # the shared definitions and the canvas writer
sys.path.insert(0, str(B03 / "s01-overall-tree-structure"))
sys.path.insert(0, str(B03 / "_build"))
import build_ladder_v4 as L  # noqa: E402  (the shared trees and drawing helpers)
sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))  # canvas (haipipe-studio)
import canvas  # noqa: E402
import level_views as LV  # noqa: E402  (proposed screens per Space, and today's beside them)

SUB = "Read off real folders where one exists, otherwise the family's contract; red ? = open."
B_BLOCK = "insight Block (DIKW)"
A_BLOCK = "insight Block (DIKW on the board)"


def define_option_a():
    tree = [t for t in L.BLOCK_TREES if t[0] == B_BLOCK][0][2]
    keep = [ln for ln in tree if not ln[0].startswith(("on screen", "a DIKW level opens", "Meta (counts"))]
    keep += [("on screen: Work Details › D · I · K · W = the questions", ""),
             ("a DIKW level folder = a group, no Job tab ?", ""),
             ("DIKW level Runs (review, plan) show in Block › Runs", "")]
    L.BLOCK_FAMILY[A_BLOCK] = "insight-a"
    L.KIND["insight-a"] = L.KIND["insight"]
    L.VARIANT_SKILLS[A_BLOCK] = L.VARIANT_SKILLS[B_BLOCK]
    LV.TODAY[A_BLOCK] = LV.TODAY[B_BLOCK]
    views = dict(L.VIEW_FAMILY["insight"])
    views["Levels"] = (["Question · need      partitions   script", "▾ t01_<question>      full · <cut>  ok",
                       "    E1 compute: <spec>  bound", "    E2 cite: <source>   open",
                       "▸ t02_<question>      full          ok", "▸ t03_<question>      —             —",
                       "pick a question → the Task tab"],
                      ["Ask a Question", "Review the questions", "Plan the evidence", "Write the script"], 1)
    views["Runs"] = ([("Run", "type", "writes", "state"), ("run-cut-<cut>", "Register a cut", "meta/", "closed · p02"),
                      ("run-review-questions-d", "Review the questions", "j01", "closed · p01"),
                      ("run-plan-evidence-t01", "Plan the evidence", "t01", "open · p02"),
                      ("run-map-questions", "Draw the question map", "studio/", "open · p03")],
                     ["Register a cut", "Review the questions", "Plan the evidence", "Draw the question map"], 2)
    L.VIEW_FAMILY["insight-a"] = views
    L.BLOCK_ROWS[("insight-a", "Jobs")] = (["Meta", "Data", "Information", "Knowledge", "Wisdom"], "Data")
    L.FAMILY_CAPTIONS[("insight-a", "Jobs")] = "A: a DIKW level is a group here, as today's Prototype; a question opens its Task tab"
    L.FAMILY_CAPTIONS[("insight-a", "Runs")] = "A: the DIKW levels' design Runs mix with the Block's own ?"
    return (A_BLOCK, "bNN_<topic>_dikw/", keep)


A_JOB = "DIKW level, plan A"                            # option A's DIKW level: no tab; where each part shows
A_JOB_VIEWS = {
    "Description": (["no Job tab under plan A", "level.md: a line above its questions,", "  in Board › Work Details › Data",
                     "Meta's counts for this DIKW level:", "  in Board › Description"], ["Update the DIKW level"]),
    "Idea Studio": ([("question-map, the Block's, whole", "", "generated"), ("no slice per DIKW level", "", "—")],
                    ["Draw the question map"]),
    "Audience Report": ([("Logic", "Work", "Report"), ("Question 1 <question>", "E1 → full · ok", "page <id>"),
                         ("Question 2 <question>", "E1 → full · ok", "page <id>"),
                         ("Question 3 <question>", "E2 → not bound", "No answer")],
                        ["Write the Data report", "Check alignment"], 0),
    "Work Details": (["Board › Work Details › Data", "▾ D01 <question>      full · <cut>  ok",
                      "    E1 compute: <spec>  bound", "    E2 cite: <source>   open",
                      "▸ D02 <question>      full          ok", "▸ D03 <question>      —             —",
                      "pick a question → the Task tab"],
                     ["Ask a Question", "Review the questions", "Plan the evidence", "Write the script"], 1),
    "Runs": ([("Run", "type", "writes", "state"), ("run-cut-<cut>", "Register a cut", "meta/", "closed · p02"),
              ("run-review-questions-d", "Review the questions", "j01", "closed · p01"),
              ("run-plan-evidence-t01", "Plan the evidence", "t01", "open · p02"),
              ("run-map-questions", "Draw the question map", "studio/", "open · p03")],
             ["Register a cut", "Review the questions", "Plan the evidence"], 2),
    "Delivery": (["no Job tab under plan A", "the DIKW level's answers: Board ›", "  Audience Report, filtered",
                  "W: Board › Delivery › Handoff"], ["Write the counsel", "Draft the handoff"])}
A_JOB_ROWS = {"Description": ["Level"], "Idea Studio": [], "Audience Report": ["Full", "<cut>", "Cross"],
              "Work Details": ["Data", "Information", "Knowledge", "Wisdom"],
              "Runs": ["All", "cut", "review", "plan", "map"], "Delivery": []}
A_JOB_NOTES = {"Description": "A: lives on the Board, above the DIKW level's questions",
               "Idea Studio": "A: the Block's map only",
               "Audience Report": "A: Board › Audience Report, filtered to this DIKW level",
               "Work Details": "A: Board › Work Details › Data, one level up",
               "Runs": "A: in Board › Runs, mixed with the Block's own ?",
               "Delivery": "A: only Board › Delivery; the DIKW level hands up"}


def define_job_a():
    """Register option A's DIKW level beside B's, for this drawing only: B's tree and today's row, A's screens."""
    tree = [ln for ln in [t for t in L.JOB_TREES if t[0] == "DIKW level"][0][2] if not ln[0].startswith("on screen")]
    tree.insert(len(tree) - 2, ("on screen: no Job tab; a group of Board › Work Details ?", ""))
    for mod in (L, LV):                              # every table that knows the B DIKW level learns the A DIKW level
        for v in list(vars(mod).values()):
            if isinstance(v, dict) and "DIKW level" in v and A_JOB not in v:
                v[A_JOB] = v["DIKW level"]
    original = LV.proposed

    def proposed(x, y, variant, level):              # A's screens, rows and notes only while A is drawn
        if variant != A_JOB:
            return original(x, y, variant, level)
        keep = (LV.JOB_FAMILY_VIEWS["insight"], LV.DIKW_ROWS, LV.DIKW_NOTES)
        LV.JOB_FAMILY_VIEWS["insight"], LV.DIKW_ROWS, LV.DIKW_NOTES = A_JOB_VIEWS, A_JOB_ROWS, A_JOB_NOTES
        try:
            return original(x, y, variant, level)
        finally:
            LV.JOB_FAMILY_VIEWS["insight"], LV.DIKW_ROWS, LV.DIKW_NOTES = keep
    LV.proposed = proposed
    return (A_JOB, "j01_data/", tree)


FRAMES = {A_BLOCK: "Board level · A: DIKW on the board",
          B_BLOCK: "Board level · B: DIKW in the Jobs",
          "insight register board": "Board level · the older register board",
          A_JOB: "Job level · A: no Job tab; where a level's parts show",
          "DIKW level": "Job level · B: a DIKW level is a Job",
          "insight question": "Task level · a question (A and B alike)"}


def bottom():
    return max(e["y"] + e.get("height", 0) for e in L.els)


def rename_frames():
    for e in L.els:
        if e["type"] == "frame" and e.get("name") in FRAMES:
            e["name"] = FRAMES[e["name"]]
        elif e["type"] == "text" and e.get("fontSize") == 22 and e.get("text") in FRAMES:
            e["text"] = e["originalText"] = FRAMES[e["text"]]



# ── the open points (red, numbered), shown first in the Decide frame ─────────────────────────────
OPEN = [("①", "Plan C: a Job = one Prototype release × one data version? (A and B, below, are the earlier options)",
         "Yes: the Board holds the Prototype (made once, DIKW as groups) and the dataset; each Job runs one release on "
         "one version; a Task is a question in that Job; a Run is one partition."),
        ("②", "Is each Prototype release signed by a person (p1, p2, …)?",
         "Yes, as a handoff is signed today: the set of live questions and their scripts that a Job may run."),
        ("③", "One clock per Job: only the release or only the data version moves between neighbouring Jobs?",
         "Yes, so a change in an answer has one cause: new data, or new code. Backfill (new code on old data) "
         "is then just one more Job."),
        ("④", "Versions: does the data accumulate (0807 holds 0801) or come in batches?",
         "Accumulate: compare versions, never pool them. Batches: may pool, or test as a replication. "
         "One field in board.md says which."),
        ("⑤", "Pages: one page per question per Job, plus a Board answer across Jobs?",
         "Yes: the Job's page answers on its pair; Board › Audience Report says whether it held across Jobs."),
        ("⑥", "Today's Check (a question's gates): where does it go?",
         "Chips on each question row: bound · fit · cited · current; the checker is a Board Run."),
        ("⑦", "Delivery: does only Wisdom deliver?",
         "Yes: the signed handoff, from the latest Job. D · I · K hand their answers up as cite needs."),
        ("⑧", "The older register boards: carry over or keep?",
         "Carry each over (carry_over.py, word for word) when next worked on; read-only until then.")]

LADDER = [("Board", "b5N_<topic>_dikw/", "the Prototype (made once) + the dataset"),
          ("Job", "j03_p2_<dataset>0807/", "one release × one data version"),
          ("Task", "t01_D01_<question>/", "one question in that Job: its page"),
          ("Run", "runs/r01_full/", "one partition: hard")]


# a red note on an earlier-option screen, and the open point it belongs to (its number is added to the note)
TAGS = {"a DIKW level folder = a group, no Job tab": "①", "A: the DIKW levels' design Runs mix": "①",
        "the Job tab is skipped": "①", "A: in Board › Runs, mixed": "①", "on screen: no Job tab": "①",
        "only j04_wisdom delivers": "⑦", "this DIKW level's part of the question map": "①",
        "Meta (counts per DIKW level) stays": "①", "carry over to a DIKW Block": "⑧", "its Instances = Jobs?": "⑧",
        "one workbench for both layouts?": "⑧", "carry over: each register": "⑧", "│   ├── rNN_ name for these": "①"}
EMPTY = (2900, 4700)          # a Board row's empty Description columns: People · Venue, Resources, Related
FRAME_GAP = 300               # room for a frame's name above it
DECIDE = "Decide · plan C, and the open points"


def decide():
    """The first frame: the ladder of plan C, and the open points with my answers."""
    fr = L.open_frame(DECIDE)
    L.text(0, 0, "Insight ladder: plan C, the Prototype and its Jobs", 30)
    L.text(0, 46, "Plan C first (the screens and how it evolves), then the earlier options A and B. "
                  "Red waits on you; gray is today's workbench.", 16, L.GRAY)
    x = 0
    for k, (level, folder, holds) in enumerate(LADDER):
        L.base("rectangle", x, 100, 420, 96, L.INK, 1.5)
        L.text(x + 18, 112, level, 20)
        L.text(x + 18, 142, folder, 15, L.INK, L.MONO)
        L.text(x + 18, 168, holds, 13, L.GRAY)
        if k < len(LADDER) - 1:
            L.path([(x + 425, 148), (x + 495, 148)])
        x += 500
    ty = 250
    L.text(0, ty, "open points, with my answer", 22, L.RED)
    for tag, ask, answer in OPEN:
        ty += 64 if ty > 250 else 44
        L.text(0, ty, f"{tag}  {ask}", 17, L.RED)
        L.text(36, ty + 26, "→ " + answer, 15, L.INK)
    L.close_frame(fr, pad=60)


# ── plan C on the base: the s02 way (one real screen per level, its folders beneath, a Run pop-out) ──
sys.path.insert(0, str(B03 / "s02-workbench-shared"))
import build_s02_workbench_shared as S2  # noqa: E402  (chrome, runs_panel, on_disk: the base's look)
UI = S2.UI
INK, GRAY, RED, TEAL, MONO = L.INK, L.GRAY, L.RED, L.TEAL, L.MONO
TABS = ["Guide", "Board", "Job · j03_p2_0807 ▾", "Task · D01 ▾"]


def cells(x, y, heads, rows, cols):
    """A table like the base's, one colour per cell: a cell is text or (text, colour)."""
    for h, c in zip(heads, cols):
        L.text(x + c + 10, y, h, 16, GRAY)
    for i, row in enumerate(rows):
        ry = y + 30 + i * 62
        L.base("rectangle", x, ry, UI.SW - UI.RW - 48, 52, GRAY, 1, rough=0)
        for c in cols[1:]:
            L.path([(x + c, ry), (x + c, ry + 52)], arrow=False, color=GRAY)
        for cell, c in zip(row, cols):
            t, col = cell if isinstance(cell, tuple) else (cell, INK)
            L.text(x + c + 10, ry + 16, t, 16, col, MONO if c == 0 else L.SANS)


C_SCREENS = [   # (title, tab on, Space, third row, heads, cols, rows, run buttons, recent, on disk)
    ("Board › Work Details: the Prototype", 1, "Work Details",
     ["Data", "Information", "Knowledge", "Wisdom", "Meta", "Releases", "Jobs"],
     ["Question", "needs · script · signed", "release"], [0, 380, 760],
     [("D01 <question> ↗", "✓ · ✓ · ✓", "p1"), ("D02 <question> ↗", "✓ · ✓ fixed · ✓", "p2"),
      ("D07 <question> ↗", ("✓ · ✓ · not yet", RED), ("next release ②", RED)), ("D03 <question>", ("retired → D07", GRAY), "p1")],
     ["Ask a question", "Plan the evidence", "Write the script", "Sign a release"], "run-sign-release-p2   p01 closed",
     [("b5N_<topic>_dikw/", ""), ("├── board.md", "dataset: <name> · versions · accumulates ④"),
      ("├── meta/", "partitions · thresholds · status (the checker)"),
      ("├── prototype/", "made once; DIKW as groups"),
      ("│   ├── data/D01_<question>/", "question.md · scripts/<name>.py"),
      ("│   ├── information/ … wisdom/", "the same, one folder per question"),
      ("│   └── releases.yaml", "p1 · p2: the signed sets ②"),
      ("├── runs/", "soft: ask · plan · script · sign · add a version"),
      ("└── j01_p1_<d>0801/ …", "the Jobs (Work Details › Jobs)"),
      ("insight_theme.py", "servers/workbench-insight/: level names, third rows")]),
    ("Board › Audience Report: across the Jobs", 1, "Audience Report", ["Across Jobs", "Full", "<cut>", "Cross"],
     ["Question", "j01 p1×0801 · j02 p1×0807", "j03 p2×0807"], [0, 380, 760],
     [("D01 <question>", "ok · ok", "ok · held"), ("D02 <question>", ("stale · stale (old script)", GRAY), "ok · new script"),
      ("I01 <question>", ("— · —  (new in p2)", GRAY), "ok"), ("D03 <question>", "ok · ok", ("retired", GRAY))],
     ["Write the answer across Jobs ⑤", "Compare two Jobs"], "run-compare-j02-j03 p01",
     [("reports/qNN_<topic>/", "the Board's answers across Jobs ⑤"),
      ("each Run's run.yaml", "question id · script hash · release · version"),
      ("meta/status.md", "this table, written only by the checker"),
      ("", "compare two Jobs only when one clock moved ③")]),
    ("Job › Work Details: one release × one version", 2, "Work Details", ["Full", "<cut>", "Cross"],
     ["Question (Logic)", "Work: its runs", "Report"], [0, 380, 760],
     [("t01_D01_<question> ↗", "r01_full ok · r02_<cut> ok", "page ✓"),
      ("t02_D02_<question> ↗", "r01_full ok · r02_<cut> —", "page draft"),
      ("t05_I01_<question> ↗", "r01_full ok", ("no answer", GRAY))],
     ["Run the Job", "Write the pages", "Close the Job"], "run-launch-j03   p01 running",
     [("j03_p2_<d>0807/", ""), ("├── j03_p2_<d>0807.md", "the band: release p2 · version 0807 · frozen when closed"),
      ("├── t01_D01_<question>/ …", "one Task per live question of p2"),
      ("└── runs/", "soft: run-launch-j03 · run-close-j03"),
      ("", "a new release or a new version → a new Job ③")]),
    ("Task › Runs: one question in that Job", 3, "Runs", ["All", "hard", "soft"],
     ["Run", "kind · partition", "status · passes"], [0, 380, 760],
     [("r01_full ↗", "hard · full", "closed · 1"), ("r02_<cut> ↗", "hard · <cut>", "closed · 1"),
      ("run-write-page", "soft · the page", "open · 1"), ("run-check-page", "soft · check ⑥", "—")],
     ["Run a partition", "Write the page", "Check the page"], "r02_<cut>   p01 closed",
     [("t01_D01_<question>/", ""), ("├── t01_D01_<question>.md", "the page: the short answer, a part per partition ⑤"),
      ("├── question → prototype/…/D01/", "read from the Prototype, never copied"),
      ("└── runs/r01_full/", "run.yaml · ticket · config · result/ · passes/"),
      ("", "result/report.md (generated): the page cites it")])]


def plan_c(x0, y0):
    """Plan C on screen: Board (twice), Job, Task, then a Run's pop-out; each with its folders beneath."""
    fr = L.open_frame("Plan C · insight on the base, at each level")
    L.text(x0, y0, "Plan C on screen: the Board holds the Prototype; a Job runs one release on one data version", 34)
    L.text(x0, y0 + 50, "Each screen is the base frame with the insight theme on it; a row's ↗ opens the level below, "
                        "or a Run's pop-out. The folders it reads are beneath it.", 20, GRAY)
    for i, (title, on, space, third, heads, cols, rows, buttons, recent, disk) in enumerate(C_SCREENS):
        x, y = x0 + i * (UI.SW + 120), y0 + 150
        L.text(x, y0 + 110, title, 24)
        S2.chrome(x, y, TABS, on, space, third)
        cells(x + 24, y + 190, heads, rows, cols)
        S2.runs_panel(x, y, buttons, recent)
        S2.on_disk(x, y + UI.SH + 50, disk)
    px = x0 + len(C_SCREENS) * (UI.SW + 120)
    L.text(px, y0 + 110, "pop-out, from a Run row's ↗", 24)
    UI.window(px, y0 + 150, UI.PW, 600, "r01_full  ·  the Run", [
        "run.yaml: hard · partition full · target t01_D01", "pins: question D01 · script a3f9",
        "      release p2 · data <dataset>0807", "passes: p01 1008 ok",
        "[ result/ preview: metrics · the first figure ]", "  result/report.md (generated) → the page cites it",
        "  open the folder · Rerun · Check"])
    L.close_frame(fr, pad=60)


def evolve(x0, y0):
    """How plan C evolves: two clocks, the chain of Jobs, and the loop that makes the next release."""
    fr = L.open_frame("Plan C · how it evolves")
    L.text(x0, y0, "How it evolves: two clocks, one Job per step", 34)
    L.text(x0, y0 + 50, "The Prototype and the data both grow; a Job pins one of each and is frozen once closed.", 20, GRAY)
    ty = y0 + 130
    L.text(x0, ty, "Prototype", 22)
    L.text(x0 + 220, ty + 2, "p1: D01–D05   →   p2: + I01–I04, D02's script fixed   →   p3: D03 retired → D07  …", 18,
           INK, MONO)
    L.text(x0, ty + 50, "data", 22)
    L.text(x0 + 220, ty + 52, "<d>0801   →   <d>0807   →   <d>0815  …", 18, INK, MONO)
    chain = [("j01_p1_<d>0801", "start"), ("j02_p1_<d>0807", "data moved"), ("j03_p2_<d>0807", "code moved"),
             ("j04_p2_<d>0815", "data moved")]
    cy, x = ty + 140, x0
    for k, (job, moved) in enumerate(chain):
        L.base("rectangle", x, cy, 520, 110, INK, 1.5)
        L.text(x + 20, cy + 18, job, 20, INK, MONO)
        L.text(x + 20, cy + 62, moved, 18, GRAY if k == 0 else TEAL)
        if k < len(chain) - 1:
            L.path([(x + 530, cy + 55), (x + 640, cy + 55)])
        x += 650
    L.text(x0, cy + 150, "one clock per Job ③: a change in an answer has one cause, the new data or the new code", 18, RED)
    ly = cy + 230
    loop = ["a Job answers every live question on its pair", "its answers raise new questions, fix scripts, retire weak ones",
            "a person signs the next release ②", "the next Job runs it, or new data arrives: the loop starts again"]
    L.text(x0, ly, "the loop", 22)
    for k, line in enumerate(loop):
        L.text(x0 + 40, ly + 44 + k * 34, f"{k + 1}. {line}", 18, RED if "②" in line else INK)
    L.close_frame(fr, pad=60)


def tidy():
    """Gray the today-differs lines, number the red notes, drop the empty columns, space the frames."""
    frames = [e for e in L.els if e["type"] == "frame"]
    for e in L.els:
        if e["type"] != "text" or e.get("strokeColor") != L.RED:
            continue
        if e["text"].startswith("differs:"):
            e["strokeColor"] = L.GRAY
            continue
        tag = next((t for k, t in TAGS.items() if e["text"].startswith(k)), None)
        if tag and tag not in e["text"]:
            e["text"] = e["originalText"] = e["text"] + " " + tag
            e["width"] += 20
    for fr in frames:
        if not fr["name"].startswith("Board level ·"):
            continue
        kids = [e for e in L.els if e.get("frameId") == fr["id"]]
        drop = [e for e in kids if EMPTY[0] <= e["x"] < EMPTY[1]]
        for e in drop:
            L.els.remove(e)
        for e in kids:
            if e not in drop and e["x"] >= EMPTY[1]:
                e["x"] -= EMPTY[1] - EMPTY[0]
        fr["width"] -= EMPTY[1] - EMPTY[0]


# the grid (JL 261007: "Board a column, job a column and then task a column"): a row per plan
GRID = {"Board level · A: DIKW on the board": (0, 0), "Job level · A: no Job tab; where a level's parts show": (1, 0),
        "Task level · a question (A and B alike)": (2, 0),
        "Board level · B: DIKW in the Jobs": (0, 1), "Job level · B: a DIKW level is a Job": (1, 1),
        "Board level · the older register board": (0, 2)}
COL_GAP, ROW_GAP = 600, 300


def layout():
    """Place each frame, with the section titles drawn just above it, in its grid cell under Decide."""
    frames = {e["name"]: e for e in L.els if e["type"] == "frame"}
    loose = [e for e in L.els if not e.get("frameId") and e["type"] != "frame"]
    for e in loose:                                  # a section title belongs to the frame just below it
        e["_owner"] = min((f for f in frames.values() if f["y"] >= e["y"]), key=lambda f: f["y"])["name"]

    def move(f, dx, dy):
        for e in L.els:
            if e is f or e.get("frameId") == f["id"] or e.get("_owner") == f["name"]:
                e["x"] += dx
                e["y"] += dy

    def span(f):                                     # the frame and its titles: left, top, right, bottom
        parts = [f] + [e for e in loose if e["_owner"] == f["name"]]
        return (min(e["x"] for e in parts), min(e["y"] for e in parts),
                max(e["x"] + e["width"] for e in parts), max(e["y"] + e["height"] for e in parts))

    cells = {name: rc for name, rc in GRID.items() if name in frames}
    widths = [max(span(frames[n])[2] - span(frames[n])[0] for n, (c, _) in cells.items() if c == col) for col in range(3)]
    col_x = [0, widths[0] + COL_GAP, widths[0] + widths[1] + 2 * COL_GAP]
    above = [f for n, f in frames.items() if n not in GRID]      # Decide and plan C stay where they are
    y = max(f["y"] + f["height"] for f in above) + ROW_GAP + 600   # room for the heading, heads and titles
    heads = []
    for row in range(3):
        names = [n for n, (_, r) in cells.items() if r == row]
        for n in names:
            l = span(frames[n])[0]
            move(frames[n], col_x[cells[n][0]] - l, y - frames[n]["y"])      # frame tops line up in a row
        if row == 0:
            heads = [(col_x[c], y - 330, h) for c, h in enumerate(("Board", "Job", "Task"))]
        y = max(span(frames[n])[3] for n in names) + ROW_GAP + 150
    if heads:                                        # the earlier options' heading, above the column heads
        L.FRAME[0] = None
        L.text(0, heads[0][1] - 200, "Earlier options: plan A and plan B (kept to compare with plan C)", 54, GRAY)
        L.els[-1]["id"] = "head-earlier-options"
    for x, hy, h in heads:                           # the column heads, above the first row
        L.FRAME[0] = None
        L.text(x, hy, h, 44)
        L.els[-1]["id"] = f"head-{h}"                # tidy() removed elements, so a count-based id could repeat
    for e in L.els:
        e.pop("_owner", None)


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s01-insight-ladder.excalidraw"
    L.els.clear()
    L.FRAME[0] = None
    decide()
    plan_c(0, bottom() + FRAME_GAP)
    evolve(0, bottom() + FRAME_GAP)
    a_block = define_option_a()
    y = bottom() + FRAME_GAP + 100
    blocks = [a_block] + [t for t in L.BLOCK_TREES if L.BLOCK_FAMILY.get(t[0], "").startswith("insight")]
    jobs = [t for t in L.JOB_TREES if LV.JOB_FAMILY.get(t[0]) == "insight"]
    tasks = [t for t in L.TASK_TREES if LV.TASK_FAMILY.get(t[0]) == "insight"]
    L.draw_trees("Board level: plan A, plan B, then the older register board", SUB, blocks, y,
                 frame_each=True, views=LV.rows("Block"), block=True)
    y = bottom() + FRAME_GAP
    L.draw_trees("Job level: plan A, then plan B", SUB, [define_job_a()] + jobs, y, frame_each=True,
                 views=LV.rows("Job"), block=False)
    y = bottom() + FRAME_GAP
    L.draw_trees("Task level: a question", SUB, tasks, y, frame_each=True, views=LV.rows("Task"), block=False)
    rename_frames()
    tidy()
    layout()
    canvas.write(out, list(L.els), "build_s01_insight_ladder.py")


if __name__ == "__main__":
    main()
