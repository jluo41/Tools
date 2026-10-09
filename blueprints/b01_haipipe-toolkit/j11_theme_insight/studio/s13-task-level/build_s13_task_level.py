"""s13 · Task level: s13-task-level.excalidraw, one question's Task tab on the shared frame, its Spaces as full
screens (JL 261007: "s11, s12, s13 ... for the Block level, Job level and task level").

A Task is one question on one Job's pair (s00): drawn for K01 in j03_p2_<d>v2. On the Insight Board every Task is
of one type, an insight question; its DIKW level changes what it may say and which methods fit, and a W Task
cites the levels below and is signed. Its question, plan and three methods (ask, answer, read) are the pinned
release's, read only here; a new or changed question is proposed from the Job (run-propose), not from a Task
(JL 261007: "the question propose is conducted in the job level?"). The Task owns its Runs (hard, one per
partition, and rNN_cross; soft write and check) and its page. It follows s12 one level down (JL 261007: "yes, I
think so, that will be better"): the Audience Report is Question │ Work │ Report over the question's needs, need
→ the Run that answers it → the page's sentence, filtered by Partition × Period; Work Details is the Task → Run
tree. Placeholders only; written through canvas.write, so every mark a person adds survives a rebuild.

    python build_s13_task_level.py [out.excalidraw]
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "_build"))
import insight_ui as U  # noqa: E402

text, base, path, INK, GRAY, RED, TEAL, MONO, GREEN = U.text, U.base, U.path, U.INK, U.GRAY, U.RED, U.TEAL, U.MONO, U.GREEN
ASK, ANSWER, READ = "By estimand", "By hypothesis test", "By multiverse"
STATUS = "K01 · in j03_p2_<d>v2 · release p2 · <d>v2 · ✅ checked"   # no band (JL 261007): Question's first line
TASK = "j03_p2_<d>v2/t04_K01_<q>/"
REL = "work/…_prototype/j02_p2/t04_K01_<q>/"

MOVES = [("Insight › a question's row", "the Task tab t04_K01_<q> in j03_p2_<d>v2: one question on one pair"),
         ("Prototype › its question.md", "Description: Question · Plan · Data, read only from release p2; ? its three methods"),
         ("(none)", "a new or changed question is proposed from the Job (run-propose), never from a Task"),
         ("its page tNN_<name>.md", "Audience Report: Question │ Work │ Report over its needs, Partition × Period"),
         ("Insight › each partition, its row", "Work Details: the Task → Run tree, hard per partition and cross, then soft"),
         ("Check › Gates (this question's)", "chips on the rows; checks are Runs"),
         ("(none)", "Runs: by type, and the order a Task runs in")]

CHANGES = ["✎ 261007  redrawn after s12: Question · Plan · Data; needs as Question │ Work │ Report; Task → Run tree",
           "✎ 261007  no band beside the tab (JL: remove it on every frame page); its line opens Description › Question",
           "✎ 261007  proposing a question moved to the Job (run-propose-j03); a Task is read only"]

DESC = lambda on: [(lab, on == k) for k, lab in enumerate(["Question", "Plan", "Data"])]
READ_ONLY = "read only: a change is\nproposed from the Job\n(run-propose-j03)"


def question(cx, cy, cw):
    """The question as release p2 has it, read only, and the three methods it names."""
    text(cx, cy, STATUS, 16, INK, MONO)
    text(cx, cy + 26, "from release p2 (hash <sha>) · read only", 14, GRAY)
    text(cx + 420, cy + 26, "✎ 261007  the status line moved here (was: a band beside the tab)", 13, GREEN)
    cy += 60
    rows = [("the ask", "<question>, one thing, at its DIKW level"), ("DIKW level", "Knowledge · may say: " + U.LEVEL["K"][1]),
            ("why now", "<the reason it is asked>"), ("signed", "✅ <date> by a person")]
    for k, (a, b) in enumerate(rows):
        text(cx, cy + k * 30, a, 14, GRAY)
        text(cx + 150, cy + k * 30, b, 15, INK)
    my = cy + len(rows) * 30 + 20
    base("rectangle", cx, my, cw, 280, RED, 1.5, dashed=True, rough=0)
    text(cx + 16, my + 12, "? Methods · named in the release's plan, before any data", 16, RED)
    for k, (step, m, what) in enumerate([("ask · step 1", ASK, "fixed: the number that answers it"),
                                         ("answer · step 3", ANSWER, "fixed: the test, its alpha and power"),
                                         ("read · step 5", READ, "fixed: the defensible choices to vary")]):
        ry = my + 52 + k * 62
        text(cx + 16, ry + 4, step, 14, GRAY)
        U.chip(cx + 170, ry, m, 260)
        text(cx + 450, ry + 4, what, 14, RED)
    text(cx + 16, my + 52 + 3 * 62, "a change is proposed from the Job, then the next release, then a new Job", 13, RED)


def plan(cx, cy, cw):
    """The plan: each need with its work spec or source and its pass rule, agreed by another agent."""
    text(cx, cy, "from release p2 · agreed ✅ <date> by another agent · read only", 14, GRAY)
    y = U.table(cx, cy + 30, cw, ["need", "kind", "work spec · source", "passes when"], [0, 90, 200, 720],
                [("E1", "compute", "cut · unit · measure · by · uncertainty · rivals · output", "<estimate> with its interval"),
                 ("E2", "compute", "the rival analyses: each defensible choice", "same sign and size (T7)"),
                 ("E3", "cite", "<source> (a Discovery Result)", "the source says <x>")], mono=(0,), h=40)
    text(cx, y + 20, "Ask covered", 15, INK)
    text(cx, y + 46, '"does X change Y" → E1 · "with other things held equal" → E2 · "how sure" → E1 (interval)', 14, INK)
    text(cx, y + 74, "every phrase of the ask maps to a need or a refusal (T0); each need is fully specified (T1)", 14, GRAY)


def data(cx, cy, cw):
    """This question's n and power on each partition, read before any outcome."""
    text(cx, cy, "<d>v2 · from each Run's partition_power.csv, computed before any outcome", 14, GRAY)
    y = U.table(cx, cy + 30, cw, ["partition", "n", "base rate", "power (smallest effect <pp>)", "state"],
                [0, 220, 360, 520, 820],
                [("full", "<n>", "<rate>", "ok", "r01 run"), ("<partition A>", "<n>", "<rate>", "ok", "r02 run"),
                 ("<partition B>", "<n>", "<rate>", "ok", "r03 run"), ("Cross", "A against B", "", "the difference test", "r04 run")],
                mono=(0,), h=40)
    text(cx, y + 16, "a cut too small for this question is refused here and shown, never run (as K02 on <B> in this Job)", 14, GRAY)


PERIOD = lambda part, on: [[("Partition:", 0)] + [(lab, lab == part) for lab, _ in U.PARTS],
                           [("Period:", 0), ("Current", on == 0), ("vs previous", on == 1)]]
HEADS = ["Logic · the need", "Work · the Run that answers it", "Report · the page's sentence"]
CHIPS = {"E1": [(0, f"ask: {ASK}"), (1, f"answer: {ANSWER}"), (2, f"read: {READ}")], "E2": [(2, f"read: {READ}")], "E3": []}


def answer_box(cx, cy, cw, line):
    base("rectangle", cx, cy, cw, 44, INK, 1.5, rough=0)
    text(cx + 14, cy + 12, line, 15, INK)


def current(cx, cy, cw):
    """Question │ Work │ Report over the needs, on one partition: need → the Run → the page's sentence."""
    answer_box(cx, cy, cw, "the page on <partition A>: <one claim> · <interval> · CHECK ✅ ↗")
    groups = [("compute", "", [("E1 · <estimate of X on Y> ↗", "r02_<partition A>/ ● ok ↗\nresult/metrics.json",
                                '"<claim sentence>" · <interval> ↗', CHIPS["E1"]),
                               ("E2 · the rival analyses ↗", "r02_<partition A>/ ● ok ↗\nresult/multiverse.csv",
                                '"<same sign and size across choices>" ↗', CHIPS["E2"])]),
              ("cite", "", [("E3 · <source> ↗", "a Discovery Result ↗\n(no Run here)", '"<sentence citing it>" ↗', [])])]
    y = U.qwr(cx, cy + 64, cw, HEADS, groups)
    text(cx, y + 6, "each need is answered by one Run (or a cited source) and cited by one sentence of the page", 14, GRAY)


def cross(cx, cy, cw):
    """On Cross: the difference test between the partitions, and the verdict the page states."""
    answer_box(cx, cy, cw, "the page on Cross: POOL · one answer for <A> and <B> ↗")
    groups = [("compute", "", [("E1 · <estimate> on A against B ↗", "r04_cross/ ● ok ↗\nA vs B: <statistic>, <p>",
                                '"the effect does not differ by <cut>" ↗', [(2, "read: By heterogeneity")])])]
    y = U.qwr(cx, cy + 64, cw, HEADS, groups)
    text(cx, y + 6, "one test of the difference, never two separate tests (By heterogeneity)", 14, GRAY)


def vs_previous(cx, cy, cw):
    """The needs against K01 in the Job before: read from the Job's run-compare-j02 report."""
    text(cx, cy, "K01 in j03 against K01 in j02 · the code moved (p1 → p2) · from j03's reports/vs-j02.md", 14, INK, MONO)
    text(cx, cy + 28, "0 new · 2 held · 1 changed · 0 dropped · 0 not comparable", 17, INK)
    groups = [("compute", "", [("E1 · <estimate> ↗", "r02_<partition A>/ ↗ (j03)\nj02: r02_<partition A>/ ↗",
                                "Δ changed: <b> → <b'> · its script changed in p2 (code)", CHIPS["E1"]),
                               ("E2 · the rival analyses ↗", "r02_<partition A>/ ↗ (j03)", "= held: same sign and size", CHIPS["E2"])]),
              ("cite", "", [("E3 · <source> ↗", "a Discovery Result ↗", "= held", [])])]
    y = U.qwr(cx, cy + 66, cw, HEADS, groups)
    text(cx, y + 6, "the held rule is the release's (thresholds.yaml); a Task has no compare Run of its own", 14, GRAY)


def studio(cx, cy, cw):
    text(cx, cy, "optional: the page's argument, drawn", 15, GRAY)
    base("rectangle", cx, cy + 34, cw, 46, GRAY, 1, rough=0)
    text(cx + 14, cy + 46, "▸ s01-<page-logic>", 17, INK, MONO)
    text(cx, cy + 100, "+ Add topic  ->  t04_K01_<q>/studio/sNN-<topic>/", 16, GRAY, MONO)


RUNS = [("r01_full/", "hard · partition", "● ok", "p01", "<MMDD>"), ("r02_<partition A>/", "hard · partition", "● ok", "p01", "<MMDD>"),
        ("r03_<partition B>/", "hard · partition", "● ok", "p02", "<MMDD>"), ("r04_cross/", "hard · cross", "POOL", "p01", "<MMDD>"),
        ("run-write-t04/", "soft · write", "closed", "p02", "<MMDD>"), ("run-check-t04/", "soft · check", "✅", "p01", "<MMDD>")]


def tree(cx, cy, cw):
    """The Task → Run tree: its hard Runs, one per partition and the cross, then its soft write and check."""
    cols = [0, 400, 600, 760, 860]
    for h, c in zip(["t04_K01_<q> › Run", "kind · type", "status", "passes", "last"], cols):
        text(cx + c + 10, cy, h, 14, GRAY)
    y = cy + 26
    path([(cx, y), (cx + cw, y)], arrow=False, color=GRAY)
    for group, rows in [("hard · one per partition, then the cross", RUNS[:4]), ("soft", RUNS[4:])]:
        text(cx, y + 8, group, 15, INK)
        y += 32
        path([(cx, y), (cx + cw, y)], arrow=False, color=INK)
        for name, kind, status, passes, last in rows:
            for c, cell in zip(cols, [name + " ↗", kind, status, passes, last]):
                text(cx + c + 10, y + 8, cell, 14, INK, MONO if c == 0 else U.SANS)
            y += 34
            path([(cx, y), (cx + cw, y)], arrow=False, color=GRAY)
    text(cx, y + 14, "a Run's ↗ opens its pop-out: run.yaml, pins, n and power, passes, result/, report.md", 14, GRAY)


ORDER = [("rNN_<partition>", "hard · each cut"), ("rNN_cross", "hard"), ("run-write-t04", "soft · the page"),
         ("run-check-t04", "soft · another agent"), ("? run-sign-t04", "W only: a person")]


def runs(cx, cy, cw):
    """The Task's Runs by type, then the order they run in."""
    y = U.table(cx, cy, cw, ["Run", "kind · type", "writes", "state"], [0, 380, 600, 840],
                [(n + " ↗", k, "result/" if k.startswith("hard") else ("t04_K01_<q>.md" if "write" in n else "CHECK"), s)
                 for n, k, s, *_ in RUNS], mono=(0,))
    text(cx, y + 26, "the order a Task runs in (inside its Job's run-launch … run-close)", 15, INK)
    x, yy = cx, y + 60
    for k, (name, who) in enumerate(ORDER):
        w = max(len(name) * 9.5, len(who) * 7) + 28
        red = name.startswith("?")
        base("rectangle", x, yy, w, 52, RED if red else INK, 1, dashed=red, rough=0)
        text(x + 10, yy + 6, name.lstrip("? "), 13, RED if red else INK, MONO)
        text(x + 10, yy + 28, who, 11, RED if red else GRAY)
        if k < len(ORDER) - 1:
            path([(x + w + 2, yy + 26), (x + w + 18, yy + 26)], color=INK)
        x += w + 22
    text(cx, yy + 70, "power is checked before the first hard Run (the Job's run-power); write waits for every hard Run", 14, GRAY)


def delivery(cx, cy, cw):
    text(cx, cy, "none of its own: its answer shows in the Job's Audience Report (s12) and the Block's readings (s11)", 15, GRAY)
    base("rectangle", cx, cy + 40, cw, 120, RED, 1, dashed=True, rough=0)
    text(cx + 14, cy + 54, "? a W Task only: its counsel, signed by a person (run-sign), goes to the Block's handoff", 15, RED)
    text(cx + 14, cy + 88, "W01 → insights/bNN_<topic>/delivery/handoff-<date>.md", 15, INK, MONO)


SCREENS = [
    ("Description", DESC(0), [], READ_ONLY, question,
     [(REL, "the question, in release p2"), ("├── question.md", "Question (read only here)"),
      ("│   ? method: ask · answer · read", "? the three cards, fixed with the plan"), ("└── scripts/<name>.py", "the one script")]),
    ("Description", DESC(1), [], READ_ONLY, plan,
     [(REL + "question.md", "needs · work spec · Ask covered · agreed"), ("check_evidence.py", "T0 covered · T1 specified")]),
    ("Description", DESC(2), [], "", data,
     [(TASK + "runs/rNN_<partition>/result/partition_power.csv", "n · base rate · power"),
      ("work/…_prototype/j02_p2/thresholds.yaml", "the smallest effect that matters")]),
    ("Idea Studio", None, ["Add a topic"], "", studio,
     [(TASK + "studio/", "optional"), ("└── s01-<page-logic>/", "the page's argument")]),
    ("Audience Report", PERIOD("<partition A>", 0), ["Write the Knowledge report", "Check a report"], "", current,
     [(TASK + "t04_K01_<q>.md", "Report: the page, its sentences"), (TASK + "runs/r02_<partition A>/result/", "Work: the Run"),
      (REL + "question.md", "Logic: the needs (E1 · E2 · E3)")]),
    ("Audience Report", PERIOD("Cross", 0), ["Pool or split"], "", cross,
     [(TASK + "runs/r04_cross/result/", "the difference test"), (TASK + "t04_K01_<q>.md", "its Cross section")]),
    ("Audience Report", PERIOD("<partition A>", 1), [], "from the Job's\nrun-compare-j02", vs_previous,
     [("j03_p2_<d>v2/reports/vs-j02.md", "the Job's comparison, this question's rows"),
      ("j02_p1_<d>v2/t04_K01_<q>/", "K01 in the Job before")]),
    ("Work Details", [("All", 1), ("hard", 0), ("soft", 0)], ["Run a partition", "Check alignment"], "", tree,
     [(TASK, "the Task"), ("├── runs/rNN_<partition>/", "hard: one per partition, + r04_cross"),
      ("│   ├── run.yaml · passes/", "kind · status · passes · last"), ("│   └── result/", "what its pop-out previews"),
      ("└── runs/run-<type>-<target>/", "soft: write · check")]),
    ("Runs", [("All", 1), ("hard", 0), ("soft", 0), ("partition", 0), ("cross", 0), ("write", 0), ("check", 0)],
     ["Run a partition", "Write the report", "Check a report"], "", runs,
     [(TASK + "runs/rNN_<partition>/", "hard: result/ · passes/"), (TASK + "runs/run-<type>-<target>/", "soft: write · check")]),
    ("Delivery", None, [], "", delivery, [("? " + TASK + "(W Tasks only)", "? the signed counsel, up to the Block")]),
]

POPOUTS = [
    ("E1 · a need", [(REL + "question.md › E1", GRAY), ("kind: compute · <estimate of X on Y>", INK),
                     ("spec: cut · unit · measure · by · uncertainty · rivals · output", INK),
                     ("passes when: <estimate> with its interval", INK),
                     ("answered by: r02_<partition A>/ ↗ · cited by: the page's sentence S3 ↗", INK),
                     ("agreed ✅ <date> by another agent", GRAY)]),
    ("r02_<partition A>  ·  the Run", [("run.yaml: hard · partition <A> · target t04_K01", INK),
                                      ("pins: question K01 · script <hash> · release p2 · data <d>v2", INK),
                                      ("n <n> on <A> · power ok (smallest effect <pp>)", INK), ("passes: p01 <MMDD> ok", GRAY),
                                      ("[ result/ preview: metrics · the first figure ]", GRAY),
                                      ("result/report.md (generated) → the page cites it", INK),
                                      ("open the folder  ·  Rerun  ·  Check", GRAY)]),
    ("K01 · the page", [(TASK + "t04_K01_<q>.md", GRAY), ("Answer", INK), ("  <one claim, how sure, its rivals, its limits>", GRAY),
                        ("Evidence", INK), ("  E1 → r02_<A> ↗ · E2 → r02_<A> ↗ · E3 → <source> ↗", GRAY),
                        ("Limits  ·  Next", INK), ("a section per partition, and Cross", GRAY)]),
    U.card_window(ANSWER)]

QUESTIONS = [
    "? the Task's Audience Report rows are its needs: need → the Run that answers it → the page's sentence",
    "? method: { ask, answer, read } in the release's question.md, fixed with the plan and agreed with it",
    "? a new or changed question is proposed from the Job (run-propose), never from a Task",
    "? a weak partition (low power): refused and shown in Data, never run",
    "? vs previous per need comes from the Job's run-compare; a Task has no compare Run of its own",
    "? run-sign: only a W Task's counsel is signed, then goes to the Block's handoff",
]

ASIDES = {"Idea Studio": ("typical topics, tNN_…/studio/sNN-<topic>/", [
    ("s01-<page-logic>", "the page's argument: claim, evidence, rivals"),
    ("? s02-<a rival>", "an explanation the page must rule out")])}


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s13-task-level.excalidraw"
    U.level_drawing(out, Path(__file__).name, "Task",
                    "Task level: one question on one Job's pair (K01 in j03_p2_<d>v2)",
                    "One Task type on the Insight Board, an insight question: its question is the release's, read only; "
                    "its needs are answered by its Runs and cited by its page.", MOVES, SCREENS, POPOUTS, QUESTIONS, ASIDES,
                    changes=CHANGES)


if __name__ == "__main__":
    main()
