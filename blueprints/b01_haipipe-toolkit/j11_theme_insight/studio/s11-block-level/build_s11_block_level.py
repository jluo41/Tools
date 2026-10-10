"""s11 · Block level: s11-block-level.excalidraw, the insight Board's tab on the shared frame, its Spaces
as full screens (JL 261007: "s11, s12, s13 ... for the Block level, Job level and task level").

The Board follows s00 (261007): one dataset with its versions; its Jobs pin one Prototype version and one
data version (j03_p2_<d>v2); the questions and their code live in the Prototype's own work Block. So the
Description is one Map, the two clocks crossed (JL 261007: "for the description you only show
Partition. How about the Dataset and Questions? do we have a better way?"): the data versions are its
columns (the Dataset, each with its partitions' counts), the Prototype releases its rows (the
Questions, counted by DIKW level), and a Job sits where the two cross. Placeholders only; written
through canvas.write, so every mark a person adds survives a rebuild.

    python build_s11_block_level.py [out.excalidraw]
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "_build"))
import insight_ui as U  # noqa: E402

text, base, path, INK, GRAY, RED, TEAL, MONO = U.text, U.base, U.path, U.INK, U.GRAY, U.RED, U.TEAL, U.MONO

MOVES = [("Scope › Dataset", "Description › Dataset: the data versions (the Map's columns)"),
         ("Scope › Partitions", "Description › Partitions: defined in the release, counted per data version"),
         ("Scope › Questions", "Description › Prototype: the releases (the Map's rows), questions by D · I · K · W"),
         ("(none)", "Description › Map: the two crossed, a Job in each cell"),
         ("Prototype (a Space)", "its own work Block, work/bNN_<topic>_prototype/: a Job per version (s00)"),
         ("(none)", "Work Details: the Jobs, one per pair, Prototype version × data version"),
         ("Insight › <partition>", "Job › Work Details (s12): Logic │ Work │ Report under D · I · K · W"),
         ("(none)", "Audience Report: Partition (Full · A · B · Cross) × Reading (Coverage · Tracks · Consistency · Findings)"),
         ("Check › Gates · Checks · Runtime", "no Space: gates as chips on the rows, checks are Runs"),
         ("Delivery › Handoff", "Delivery › Handoff: the signed Wisdom answer names its Job (pN × vM)")]

DATA = [("<d>v1", "frozen <date> · <n> rows", "full <n> · A <n> · B <n>"),
        ("<d>v2", "frozen <date> · <n> rows", "full <n> · A <n> · B <n>"),
        ("<d>v3", "frozen <date> · <n> rows", "full <n> · A <n> · ? B low")]
PROTO = [("p1", "signed <date>", "D 2 · I 3 · K 2 · W 1"),
         ("p2", "signed <date> · +2 · 1 changed", "D 2 · I 4 · K 3 · W 1"),
         ("? p3", "proposals/: 3 waiting", "not cut yet")]
JOBS = {("p1", "<d>v1"): ("j01", "✅ closed", "start"), ("p1", "<d>v2"): ("j02", "✅ closed", "data moved"),
        ("p2", "<d>v2"): ("j03", "✅ closed", "code moved"), ("p2", "<d>v3"): ("j04", "open", "data moved")}


def the_map(cx, cy, cw):
    """The two clocks crossed: a column per data version, a row per Prototype release, a Job per cell."""
    text(cx, cy, "columns = the Dataset (its versions) · rows = the Questions (the Prototype's releases) · a cell = a Job", 14, GRAY)
    HX, CW_, top = 290, 262, cy + 34
    for k, (v, frozen, parts) in enumerate(DATA):                  # the column heads: one data version each
        x = cx + HX + k * CW_
        text(x + 10, top, v + " ↗", 17, INK, MONO)
        text(x + 10, top + 26, frozen, 13, GRAY)
        text(x + 10, top + 46, parts, 13, RED if "?" in parts else INK)
    y = top + 76
    path([(cx, y), (cx + HX + 3 * CW_, y)], arrow=False, color=INK)
    for p, signed, levels in PROTO:                               # a row per Prototype release
        open_ = p.startswith("?")
        text(cx + 10, y + 12, p.lstrip("? ") + (" ↗" if not open_ else ""), 17, RED if open_ else INK, MONO)
        text(cx + 10, y + 38, signed, 13, RED if open_ else GRAY)
        text(cx + 10, y + 58, levels, 13, GRAY if open_ else INK)
        for k, (v, *_) in enumerate(DATA):
            x = cx + HX + k * CW_
            job = JOBS.get((p, v))
            if job:
                base("rectangle", x + 8, y + 10, CW_ - 20, 66, INK, 1.5 if job[1] == "open" else 1, rough=0)
                text(x + 20, y + 18, f"{job[0]}_{p}_{v} ↗", 14, INK, MONO)
                text(x + 20, y + 44, f"{job[1]} · {job[2]}", 13, GRAY)
            elif open_ or (p, v) == ("p2", "<d>v3"):
                pass
            else:
                text(x + 20, y + 34, "—", 15, GRAY)
        y += 86
        path([(cx, y), (cx + HX + 3 * CW_, y)], arrow=False, color=GRAY)
    base("rectangle", cx + HX + 2 * CW_ + 8, y - 76, CW_ - 20, 66, RED, 1, dashed=True, rough=0)
    text(cx + HX + 2 * CW_ + 20, y - 58, "+ Add a Job: p3 × v3", 14, RED)
    path([(cx + HX, top - 4), (cx + HX, y)], arrow=False, color=GRAY)
    text(cx, y + 18, "a column head opens its data version; a row head opens its release in the Prototype Block;", 14, GRAY)
    text(cx, y + 40, "a cell opens its Job (s12). One clock per Job: a new version of one kind, never both at once.", 14, GRAY)
    text(cx, y + 70, "? p2 × v1 (new code on old data): a backfill Job, or never", 14, RED)


def prototype(cx, cy, cw):
    """The rows of the Map, opened: the Prototype's releases, each its questions by DIKW level and what changed."""
    text(cx, cy, "the questions and their code live in work/bNN_<topic>_prototype/ ↗ ; here, its releases", 14, GRAY)
    y = U.table(cx, cy + 34, cw, ["release", "signed", "D · I · K · W", "new · changed · retired", "Jobs on it"],
                [0, 140, 320, 540, 860],
                [("p1 ↗", "✅ <date>", "2 · 3 · 2 · 1", "first release", "j01 · j02"),
                 ("p2 ↗", "✅ <date>", "2 · 4 · 3 · 1", "I04, K03 · K01 · —", "j03 · j04"),
                 ("? p3", "? not cut", "", "3 proposals waiting", "")], mono=(0,), h=40)
    text(cx, y + 24, "proposals/ · the backlog the Board sends back", 15, INK)
    U.table(cx, y + 54, cw, ["proposal", "from", "kind"], [0, 520, 860],
            [("K02: split by <factor>", "j03 · weak answer", "fix"), ("I05: <new question>", "<d>v3 · a new field", "new"),
             ("<partition C>: a new cut", "<d>v3 · a new field", "new cut"),
             ("D02: retire", "a check failed", "retire")])


def dataset(cx, cy, cw):
    """The Map's columns, opened: the data versions of the Board's one dataset."""
    y = U.table(cx, cy, cw, ["data version", "extract", "frozen", "rows", "new since", "Jobs on it"],
                [0, 160, 440, 600, 720, 900],
                [("<d>v1 ↗", "$EXTRACTS/<d>v1", "<date>", "<n>", "first", "j01"),
                 ("<d>v2 ↗", "$EXTRACTS/<d>v2", "<date>", "<n>", "+<n> rows", "j02 · j03"),
                 ("<d>v3 ↗", "$EXTRACTS/<d>v3", "<date>", "<n>", "+ <field>", "j04")], mono=(0, 1), h=40)
    text(cx, y + 16, "one dataset, its versions frozen outside the Project; a new version is a new column of the Map", 14, GRAY)


def partitions(cx, cy, cw):
    """The cuts: defined in a Prototype release (part of the plan, fixed before any outcome); then their counts,
    a row per data version, so the table grows down as data arrives (JL 261007: "each row is a dataset, and
    columns are the partitions")."""
    text(cx, cy, "defined in the Prototype's release, with the questions", 14, GRAY)
    y = U.table(cx, cy + 30, cw, ["partition", "filter", "why", "since"], [0, 200, 440, 900],
                [("full", "all rows", "the whole extract", "p1"),
                 ("<partition A>", "<column> = <a>", "<why this cut>", "p1"),
                 ("<partition B>", "<column> = <b>", "<why this cut>", "p1"),
                 ("<partition C>", "<field> = <c>", "<a new field in v3>", "? p3"),
                 ("Cross", "A against B", "pool or split: one test of the difference", "p1")], mono=(0, 1))
    text(cx, y + 30, "counts · a row per data version, a column per partition", 15, INK)
    y = U.table(cx, y + 60, cw, ["data version", "full", "<partition A>", "<partition B>", "<partition C>"],
                [0, 220, 420, 640, 860],
                [("<d>v1", "<n>", "<n>", "<n>", "—"), ("<d>v2", "<n>", "<n>", "<n>", "—"),
                 ("<d>v3", "<n>", "<n>", "? <n> low", "<n>"), ("…", "", "", "", "")], mono=(0,))
    text(cx, y + 16, "a new data version adds a row; a new cut (a new release) adds a column; — = the field is not there", 14, GRAY)
    text(cx, y + 40, "low = under the release's smallest effect (thresholds.yaml); power is checked per Job (s12)", 14, GRAY)


def work(cx, cy, cw):
    """The Jobs, one row each; a row opens in place to its Tasks' quick results, so the work is seen from the
    Block (JL 261007: "maybe just show the tasks's quick results ... each row, with tasks' results")."""
    cols = [0, 290, 420, 520, 760]
    for h, c in zip(["Job", "pins", "moved", "answered D · I · K · W", "state"], cols):
        text(cx + c + 10, cy, h, 14, GRAY)
    y = cy + 26
    path([(cx, y), (cx + cw, y)], arrow=False, color=GRAY)
    for job, pin, moved, ans, state, opened in [
            ("j01_p1_<d>v1/", "p1 · v1", "start", "2/2 · 3/3 · 2/2 · 1/1", "✅ closed", False),
            ("j02_p1_<d>v2/", "p1 · v2", "data", "2/2 · 3/3 · 2/2 · 1/1", "✅ closed", False),
            ("j03_p2_<d>v2/", "p2 · v2", "code", "2/2 · 4/4 · 3/3 · 1/1", "✅ closed", False),
            ("j04_p2_<d>v3/", "p2 · v3", "data", "2/2 · 2/4 · 0/3 · 0/1", "open", True)]:
        for c, cell in zip(cols, [("▾ " if opened else "▸ ") + job, pin, moved, ans, state]):
            text(cx + c + 10, y + 10, cell, 14, INK, MONO if c == 0 else U.SANS)
        y += 38
        if opened:                                   # its Tasks, each with its quick result
            tc = [24, 300, 560, 960]
            for h, c in zip(["Task", "full · A · B", "quick result", "state"], tc):
                text(cx + c, y + 4, h, 13, GRAY)
            y += 26
            for task, runs, result, st in [("t01_D01_<q>", "● · ● · ●", "<n> <unit>, <what was seen>", "✅"),
                                           ("t02_D02_<q>", "● · ● · ●", "<n> <unit>, <what was seen>", "✅"),
                                           ("t03_I01_<q>", "● · ● · ●", "<rate> vs <rate>, A > B", "✅"),
                                           ("t06_I04_<q>", "● · ◐ · –", "<rate> on full; A running", "◐"),
                                           ("t04_K01_<q>", "◐ · – · –", "running: <test> on full", "◐"),
                                           ("t05_K02_<q>", "– · – · ✕", "B refused: power low", "–"),
                                           ("t08_W01_<q>", "", "waits for K01 · I01", "–")]:
                base("rectangle", cx + 14, y, cw - 14, 30, GRAY, 1, rough=0)
                text(cx + tc[0] + 8, y + 7, task + " ↗", 13, INK, MONO)
                text(cx + tc[1], y + 7, runs, 13, INK, MONO)
                text(cx + tc[2], y + 7, result, 13, RED if "refused" in result else INK)
                text(cx + tc[3], y + 7, st, 13, INK)
                y += 34
            y += 6
        path([(cx, y), (cx + cw, y)], arrow=False, color=GRAY)
    text(cx, y + 16, "a row opens in place to its Tasks' quick results (results/ of each Task): you stay on the Block;", 14, GRAY)
    text(cx, y + 40, "open the Job tab (s12) only to work on it.  ● done · ◐ running · – not yet · ✕ refused", 14, GRAY)


AR = lambda on: [[("Partition:", 0)] + [(lab, k == 1) for k, (lab, _) in enumerate(U.PARTS)],
                 [("Reading:", 0)] + [(lab, on == k) for k, lab in enumerate(["Coverage", "Tracks", "Consistency", "Findings"])]]
# two dimensions, as the Job's (JL 261007: "Dimension 1: Partition: full, female, xxx; Dimension 2: ... we can have
# dimension 1 and dimension 2"): the partition picks the cut; the reading picks how the Jobs are read across
# The topics are kinds of reading across Jobs; D · I · K · W are the sections inside each (JL 261007: "I think the
# D I K W should be the group sections in the page ... like the same questions, how to across, how to check the
# consistency"), each view a Question │ Work │ Report table (JL 261007: "make sure it will follow the Question, Work,
# and Report format"). Compare only Jobs that differ in one clock; a question changed in a release is a new version.


HEADS = ["Logic · the question it reads", "Work · the Board's soft Run", "Report · what it says"]


def coverage(cx, cy, cw):
    """Coverage: for each question, on which Jobs it was answered, and where it was not."""
    seen = {"K02": ("j01 – j03 ✓ · j04 ✕ <B>", "? refused on <B> in j04 (power)"), "W01": ("j01 – j03 ✓ · j04 –", "waits for K01 in j04")}
    y = U.dikw_table(cx, cy, cw, U.LEVELS, heads=HEADS,
                     work=lambda lv, q: "run-coverage/ ● ok ↗  " + seen.get(q, ("j01 – j03 ✓ · j04 ◐",))[0],
                     report=lambda lv, q: seen.get(q, (0, "answered on 3 of 4 Jobs · j04 running"))[1],
                     chips=lambda lv, q, ask, ans, rd: [f"ask: {ask}", "reads: every Job's receipts", None])
    text(cx, y, "on <partition A> · ✓ answered · ◐ running · ✕ refused · – waits · I04 new in p2: 1 of 2 Jobs", 14, GRAY)


def tracks(cx, cy, cw):
    """Tracks: each question's answer Job by Job; along one release, a trend over the data versions."""
    trend = {"D": "↑ volume", "I": "→ flat", "K": "↑ along p1", "W": "the counsel stands"}
    y = U.dikw_table(cx, cy, cw, U.LEVELS, heads=HEADS,
                     work=lambda lv, q: f"run-track-{q.lower()}/ ● ok ↗  <est> ± <ci> per Job",
                     report=lambda lv, q: "K01 changed in p2: a new track, <b'>" if q == "K01" else f"{trend[lv]} · [ the track ] ↗",
                     chips=lambda lv, q, ask, ans, rd: [f"ask: {ask}", ans and f"answer: {ans} (each Job)", "read: By heterogeneity"])
    text(cx, y, "along one release (p1: v1 → v2; p2: v2 → v3), the data versions are slices of time; like with like only", 14, GRAY)


RULES = {"D": "rule: same counts within the data's drift",
         "I": "rule: same direction; one test of the difference",
         "K": "rule: same sign and size; replicates (T8); rivals say why (T7)",
         "W": "rule: stands while what it stands on holds"}


def consistency(cx, cy, cw):
    """Consistency: each step between Jobs moves one clock, so each change gets a verdict and one cause."""
    verdict = {"D02": "drifts with the data", "I01": "? weaker on v3: check",
               "K01": "replicates on p1 (T8) · p2 a new version", "K02": "open: refused on <B> in j04", "W01": "stands"}
    y = U.dikw_table(cx, cy, cw, U.LEVELS, heads=HEADS, note=lambda lv: RULES[lv],
                     work=lambda lv, q: "run-consistency-j01-j02/ ↗ data  run-consistency-j02-j03/ ↗ code",
                     report=lambda lv, q: verdict.get(q, "holds"),
                     chips=lambda lv, q, ask, ans, rd: [f"ask: {ask}", ans and f"answer: {ans} (each Job)",
                                                        "read: By multiverse" if lv == "K" else "read: By heterogeneity"])
    text(cx, y, "compare only Jobs one clock apart; never pool across Jobs", 14, GRAY)


FINDINGS = {"D": ("q01 · what has the Board answered, on which pairs?", "run-report-q01/ ↗\ncites run-coverage",
                  "Answer: 10 questions · 4 Jobs · 1 refused cell · q01 ↗", "By level"),
            "I": ("q02 · which answers moved, and was it the data or the code?", "run-report-q02/ ↗\ncites run-consistency-…",
                  "Answer: 3 moved: 2 by code, 1 by data · q02 ↗", "By heterogeneity"),
            "K": ("q03 · does K01 hold on every data version?", "run-report-q03/ ↗\ncites run-track-k01 · consistency",
                  "Answer: replicates on p1; p2 open on v3 · q03 ↗", "By multiverse"),
            "W": ("q04 · what do we hand to Design now?", "run-report-q04/ ↗\ncites q03 · q02",
                  "Answer: <counsel> · signed ✅ → Delivery · q04 ↗", "By sensemaking")}


def findings(cx, cy, cw):
    """Findings: the Block's own questions (the second ladder), their reports citing the readings' Runs."""
    text(cx, cy, "the Block's own questions (board.md, reports/qNN_<topic>/): their evidence is the readings above", 14, GRAY)
    groups = [(f"{lv} · {U.LEVEL[lv][0]}", "may say: " + U.LEVEL[lv][1],
               [(FINDINGS[lv][0] + " ↗   signed ✅", FINDINGS[lv][1], FINDINGS[lv][2],
                 [(0, "ask: By level"), (1, "cites: " + FINDINGS[lv][1].split("cites ")[1]), (2, "read: " + FINDINGS[lv][3])])])
              for lv in U.LEVELS]
    y = U.qwr(cx, cy + 34, cw, ["Logic · the Block's question", "Work · its report Run", "Report · what it says"], groups)
    text(cx, y, "each report: Answer · Evidence · Limits · Next; W's signed counsel is the Board's Delivery", 14, GRAY)


def studio(cx, cy, cw):
    text(cx, cy, "one topic per row, by name; click one and it opens in place", 15, GRAY)
    base("rectangle", cx, cy + 34, cw, 46, INK, 1, rough=0)
    text(cx + 14, cy + 46, "▾ s01-question-map", 17, INK, MONO)
    text(cx + 330, cy + 48, "generated from the latest release · view only", 15, GRAY)
    base("rectangle", cx + 14, cy + 94, cw - 28, 280, GRAY, 1, dashed=True, rough=0)
    text(cx + 34, cy + 210, "[ the question map: D → I → K → W, each question's needs and cites ]", 16, GRAY)
    base("rectangle", cx, cy + 390, cw, 46, GRAY, 1, rough=0)
    text(cx + 14, cy + 402, "▸ s02-<topic>", 17, INK, MONO)


def runs(cx, cy, cw):
    """The Board's own soft Runs (the readings across Jobs, each writing what an Audience Report view shows),
    then the Jobs' hard Runs from below."""
    y = U.table(cx, cy, cw, ["Run", "type", "writes", "state"], [0, 360, 560, 860],
                ["the Board's own · soft",
                 ("run-add-job-j04/", "Add a Job", "j04_p2_<d>v3/", "closed · p01"),
                 ("run-coverage/", "Update the coverage", "Coverage", "closed · p03"),
                 ("run-track-k01/", "Draw a track", "Tracks › K01", "closed · p02"),
                 ("run-consistency-j02-j03/", "Check consistency", "Consistency", "closed · p01"),
                 ("run-consistency-j03-j04/", "Check consistency", "Consistency", "waits for j04"),
                 ("run-report-q03/", "Write the report", "reports/q03", "open · p01"),
                 ("run-check-q03/", "Check a report", "reports/q03", "waiting"),
                 ("run-handoff/", "Draft the handoff", "delivery/", "open"),
                 "from below · hard",
                 ("j04 › t04_K01 › r02_<A>/", "Run a partition", "result/", "open")], mono=(0,))
    text(cx, y + 16, "a soft Run reads results, never data: the readings across Jobs are the Board's own work", 14, GRAY)


def delivery(cx, cy, cw):
    base("rectangle", cx, cy, cw, 190, INK, 1, rough=0)
    text(cx + 14, cy + 12, "W01 · <counsel> ↗", 17, INK)
    text(cx + 14, cy + 44, "from j03_p2_<d>v2 · cites K01 · I01", 15, INK, MONO)
    text(cx + 14, cy + 76, "signed ✅ <date> by a person · → Design, as an internal insight", 15, INK)
    text(cx + 14, cy + 140, "? stale once j04 lands, or it stands for its own pair", 14, RED)


DESC = lambda on: [("Map", on == 0), ("Prototype", on == 1), ("Dataset", on == 2), ("Partitions", on == 3)]
BOARD_TREE = [("insights/bNN_<topic>/", ""), ("├── board.md", "dataset: <d> · its versions"),
              ("├── meta/status.md", "written only by the checker"), ("├── j0N_pN_<d>vM/", "a Job: a cell of the Map")]
SCREENS = [
    ("Description", DESC(0), ["Add a data version", "Add a Job"],
     "a new release comes from the\nPrototype Block (s00)", the_map,
     BOARD_TREE + [("$EXTRACTS/<d>v1 · v2 · v3", "the columns: outside the Project"),
                   ("work/bNN_<topic>_prototype/j0N_pN/release.yaml", "the rows: one per release")]),
    ("Description", DESC(1), ["Open the Prototype Block ↗"], "releases are cut there", prototype,
     [("work/bNN_<topic>_prototype/", "the Prototype Block (its own tab)"), ("├── proposals/", "the backlog"),
      ("├── j01_p1/release.yaml", "a row: p1"), ("├── j02_p2/release.yaml", "a row: p2"),
      ("└── j0N_pN/partitions.md · thresholds.yaml", "its cuts and power: part of the release")]),
    ("Description", DESC(2), ["Add a data version"], "", dataset,
     [("insights/bNN_<topic>/board.md", "dataset: <d> · its versions"), ("$EXTRACTS/<d>v1 · v2 · v3", "a row each: frozen extracts")]),
    ("Description", DESC(3), ["Propose a cut"], "a cut is made in the release:\nit goes to proposals/", partitions,
     [("work/bNN_<topic>_prototype/j0N_pN/partitions.md", "filter · why · since: the release's"),
      ("work/…_prototype/j0N_pN/thresholds.yaml", "power.smallest_effect_pp"), ("$EXTRACTS/<d>vM", "the counts, per data version")]),
    ("Work Details", [("All", 1), ("p1", 0), ("p2", 0)], ["Add a Job", "Close a Job"], "", work,
     BOARD_TREE[:1] + [("├── j01_p1_<d>v1/", "a row"), ("│   └── j01_p1_<d>v1.md", "pins: j01_p1 (hash) · <d>v1"),
                       ("├── j03_p2_<d>v2/", "uses p2 by path + hash, never a copy"), ("└── j04_p2_<d>v3/", "open: its Tasks shown"),
                       ("    └── tNN_…/runs/rNN_<partition>/result/", "a Task's quick result, per partition")]),
    ("Audience Report", AR(0), ["Update the coverage"], "run-coverage/ · reads every\nJob's receipts", coverage,
     [("insights/bNN_<topic>/runs/run-coverage/", "soft: the Board's own Run"), ("├── run.yaml", "type: coverage · reads: j01 – j04"),
      ("└── result/coverage.csv", "this view: question × Job × partition"),
      ("j0N_…/tNN_…/runs/rNN_<partition>/", "what it reads: each hard Run's state")]),
    ("Audience Report", AR(1), ["Draw a track"], "run-track-k01/ · one per question", tracks,
     [("insights/bNN_<topic>/runs/run-track-k01/", "soft: one question across Jobs"), ("├── run.yaml", "type: track · target: K01 · partition"),
      ("└── result/track.csv · track.png", "this view: estimate ± interval per Job, the trend"),
      ("j0N_…/tNN_K01_…/runs/rNN_<p>/result/metrics.json", "what it reads")]),
    ("Audience Report", AR(2), ["Check consistency"], "run-consistency-j02-j03/ ·\none per pair of Jobs", consistency,
     [("insights/bNN_<topic>/runs/run-consistency-j02-j03/", "soft: two Jobs one clock apart"), ("├── run.yaml", "type: consistency · the clock that moved"),
      ("└── result/consistency.csv", "this view: question × verdict × cause"),
      ("j0N_pN_<d>vM/j0N_….md", "what it reads: the pins")]),
    ("Audience Report", AR(3), ["Ask a Block question", "Write the report", "Check a report"], "run-report-q03/ · a person signs W",
     findings,
     [("insights/bNN_<topic>/runs/run-report-q03/", "soft: writes one Block report"), ("insights/bNN_<topic>/reports/q03_<topic>/", "Answer · Evidence · Limits · Next"),
      ("    Evidence: run-track-k01 · run-consistency-…", "it cites the readings' Runs"),
      ("insights/bNN_<topic>/board.md", "the register: q01 – q04, each with its level")]),
    ("Idea Studio", None, ["Draw the question map", "Add a topic"], "", studio,
     [("insights/bNN_<topic>/studio/", "the Space"), ("├── s01-question-map/", "generated, view only"),
      ("└── s02-<topic>/", "a person's topic")]),
    ("Runs", [("All", 1), ("soft", 0), ("from below", 0)], ["Add a Job", "Update the coverage", "Check consistency"], "", runs,
     [("insights/bNN_<topic>/runs/run-<type>-<target>/", "soft: run.yaml · passes/ · result/"),
      ("j0N_…/tNN_…/runs/rNN_<partition>/", "from below: hard, one per partition")]),
    ("Delivery", [("Handoff", 1)], ["Write the counsel", "Draft the handoff"], "a person signs the handoff", delivery,
     [("insights/bNN_<topic>/delivery/", "the signed handoff, naming its Job"), ("designs/", "reads it")]),
]

POPOUTS = [("<d>v2  ·  a data version (a column)", [("$EXTRACTS/<d>v2 · frozen <date> · <n> rows", INK),
                                                    ("new since v1: <n> rows · fields: + <field>", GRAY),
                                                    ("partitions: full <n> · A <n> · B <n>", INK),
                                                    ("Jobs on it: j02 (p1) · j03 (p2)", GRAY)]),
           ("p2  ·  a release (a row), in the Prototype Block", [("work/bNN_<topic>_prototype/j02_p2/release.yaml", INK),
                                                                ("live: D 2 · I 4 · K 3 · W 1 · signed <date>", INK),
                                                                ("new: I04, K03 · changed: K01 (its script) · retired: none", GRAY),
                                                                ("each question: its methods (ask · answer · read)", RED),
                                                                ("Jobs on it: j03 (v2) · j04 (v3)", GRAY)]),
           U.card_window("By hypothesis test")]

QUESTIONS = [
    "? Description: Map · Prototype · Dataset · Partitions",
    "? a backfill Job (new code on old data, p2 × v1): allowed, or never",
    "? Work Details: a Job row opens in place to its Tasks' quick results; the open Job opened by default",
    "? the counts: a row per data version, a column per partition, so the table grows down",
    "? a signed handoff: stale once a newer Job lands, or it stands for its own pair",
    "? Audience Report: two dimensions, Partition × Reading, as the Job's Partition × Period; D · I · K · W as sections",
    "? each reading is a soft Run of the Board (coverage · track · consistency · report), reading results, never data",
    "? Findings follow the Partition button: each finding is 'on <partition>', Cross shows where cuts disagree",
    "? consistency rules per DIKW level (D drift · I direction · K sign and size, T8 · W stands while its ground holds)",
    "? Block questions live on the Board (board.md, reports/qNN), not in the Prototype: they are about Jobs",
]


ASIDES = {"Idea Studio": ("typical topics, studio/sNN-<topic>/", [
    ("s01-question-map", "generated from the latest release: D → I → K → W, needs and cites"),
    ("s02-<what moved>", "one per new Job: what changed between two pairs, and why"),
    ("s03-<a pattern seen>", "noticed while reading: drawn, then sent on as a proposal"),
    ("s04-<cut ideas>", "partitions worth asking: becomes Propose a cut"),
    ("s05-<handoff story>", "the Wisdom argument for Design, before the counsel is signed"),
    ("? s06-<compare Prototypes>", "two releases side by side: which questions changed")])}


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s11-block-level.excalidraw"
    U.level_drawing(out, Path(__file__).name, "Block",
                    "Block level: the insight Board, one dataset and its versions, a Job per pair",
                    "After s00: the questions live in the Prototype Block; the Board crosses its releases with the data versions.",
                    MOVES, SCREENS, POPOUTS, QUESTIONS, ASIDES)


if __name__ == "__main__":
    main()
