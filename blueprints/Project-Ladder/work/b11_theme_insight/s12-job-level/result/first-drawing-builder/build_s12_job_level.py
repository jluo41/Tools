"""s12 · Job level: s12-job-level.excalidraw, one Job's tab on the shared frame, its Spaces as full screens
(JL 261007: "s11, s12, s13 ... for the Block level, Job level and task level").

A Job pins one Prototype version and one data version (s00, 261007: "the prototype_version (method version)
and data version to be a job"), drawn for j03_code-v2_data-v2. Its questions are grouped by DIKW level, D · I · K
· W headings in one Logic │ Work │ Report table, with the partitions as the third row (JL 261007). Each row
shows its three methods, read from the pinned release. Placeholders only; written through canvas.write,
so every mark a person adds survives a rebuild.

    python build_s12_job_level.py [out.excalidraw]
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "_build"))
import insight_ui as U  # noqa: E402

text, base, INK, GRAY, RED, TEAL, MONO, GREEN = U.text, U.base, U.INK, U.GRAY, U.RED, U.TEAL, U.MONO, U.GREEN

CHANGES = [  # the drawing's own history (JL 261007: "add the short green comments to where we made the changes")
    "✎ 261007  run-propose-j03 added after run-compare-j02: a new or changed question is proposed from the Job "
    "(was: from a Task, s13)",
    "✎ 261007  Runs › run types: the Board's soft Runs now in s11's words (was: run-check-board · run-read-<reading>)",
    "✎ 261007  no band beside the tab (JL: remove it on every frame page); its line opens Description › Prototype"]

MOVES = [("(none: a Job was a DIKW level)", "the Job tab j03_code-v2_data-v2: one Prototype version × one data version"),
         ("Scope, at one data version", "Description: Prototype (release p2) · Dataset (<d>v2); the pair's line opens Prototype"),
         ("Insight › <partition>", "Audience Report: Question │ Work │ Report under D · I · K · W; every cell opens a pop-out"),
         ("(none)", "Work Details: the Job › Task › Run tree; the partitions are the hard Runs"),
         ("Work Details: the Job › Task › Run tree", "Work: its steps 1 · Launch … 6 · Close, a folded work panel each (261022)"),
         ("Prototype › Data … Wisdom", "the D · I · K · W headings of that table (a level groups questions)"),
         ("(none)", "Audience Report: Partition (Full · A · B · Cross) × Period (Current · vs previous)"),
         ("Task › Propose a change (s13)", "the Job proposes: run-propose-j03, after the compare, to the Prototype's proposals/"),
         ("(none)", "? Delivery: the Wisdom counsel of this pair, if it is the latest Job")]


DESC = lambda on: [(lab, on == k) for k, lab in enumerate(["Prototype", "Dataset"])]
# the Job's Description is its two pins (JL 261007, via the s00/s01 session: "It will be of no map, just the
# prototype and Dataset, right?"); no band beside the tab (JL 261007: remove it on every frame page): the Job's
# line opens Description › Prototype
JOB_LINE = "p2 × <d>v2 · closed, frozen · moved from j02: the code (p1 → p2)"
CUTS = [("full", "all rows", "the whole extract"), ("<partition A>", "<column> = <a>", "<why this cut>"),
        ("<partition B>", "<column> = <b>", "<why this cut>"), ("Cross", "A against B", "pool or split: one test")]


def job_prototype(cx, cy, cw):
    """Release p2: its questions by DIKW level (new · changed · retired), its cuts, its shared code; read only."""
    text(cx, cy, JOB_LINE, 16, INK, MONO)
    text(cx + 640, cy + 2, "✎ 261007  the Job's line moved here (was: a band beside the tab)", 13, GREEN)
    cy += 34
    text(cx, cy, "release p2 (hash <sha>) · read only: it is changed in the Prototype Block", 14, GRAY)
    y = U.table(cx, cy + 30, cw, ["level", "questions", "new in p2", "changed in p2", "retired"], [0, 180, 480, 680, 880],
                [("D · Data", "D01 · D02", "", "", ""), ("I · Information", "I01 – I04", "I04", "", ""),
                 ("K · Knowledge", "K01 · K02 · K03", "K03", "K01 (its script)", ""), ("W · Wisdom", "W01", "", "", "")])
    text(cx, y + 22, "cuts, as defined in the release", 15, INK)
    y = U.table(cx, y + 48, cw, ["partition", "filter", "why"], [0, 260, 560], CUTS, mono=(0, 1))
    text(cx, y + 22, "shared code", 15, INK)
    U.table(cx, y + 48, cw, ["file", "in release", "used by", "changed in p2"], [0, 420, 580, 860],
            [("src/<module>.py", "p1", "I01 · K01 · K02", "—"), ("src/<helper>.py", "p2", "I04 · K03", "new"),
             ("scripts/k01_<name>.py", "p2", "K01", "Δ changed")], mono=(0,))


def job_dataset(cx, cy, cw):
    """Data version v2: the extract, then each cut's count in it, its power, the cells it refuses."""
    rows = [("data version", "<d>v2 · $EXTRACTS/<d>v2"), ("frozen", "<date>"), ("rows", "<n>"),
            ("new against v1", "+<n> rows · no new field"), ("also used by", "j02 (p1)")]
    for k, (a_, b_) in enumerate(rows):
        text(cx, cy + k * 30, a_, 14, GRAY)
        text(cx + 180, cy + k * 30, b_, 15, INK, MONO if k == 0 else U.SANS)
    y = U.table(cx, cy + len(rows) * 30 + 24, cw, ["partition", "n in <d>v2", "power (smallest effect <pp>)", "refused"],
                [0, 240, 420, 800],
                [("full", "<n>", "ok", ""), ("<partition A>", "<n>", "ok", ""), ("<partition B>", "<n>", "? low", "K02"),
                 ("Cross", "A against B", "the difference test", "")], mono=(0,), h=40)
    text(cx, y + 16, "the cuts are the release's; the counts this data version's; power is checked here, before any outcome", 14, GRAY)


STEPS = ["1 · Launch", "2 · Run", "3 · Write", "4 · Check", "5 · Compare", "6 · Close"]
WORK_TABS = lambda on: [(st, st == on) for st in STEPS]
# the Job's Work is its steps (JL 261022: "how to make it that when the user want, they can open this work panel and
# work on it"): a tab per step, its work panel folded until opened, its result under it, as the draft and labeling
# Tasks' steps are; the Job → Task → Run tree (261007) is 2 · Run's last card


def _fold_row(cx, y, cw, title, chip, opened=False, h=44):
    """A folding row: ▸ or ▾, its title, its chip on the right; returns its bottom."""
    base("rectangle", cx, y, cw, h, INK, 1, rough=0)
    text(cx + 14, y + 11, ("▾ " if opened else "▸ ") + title, 18, INK)
    text(cx + cw - 16 - len(chip) * 9, y + 12, chip, 16, INK)
    return y + h


def _grid(cx, y, cw, heads, rows, cols):
    for h_, c in zip(heads, cols):
        text(cx + c + 10, y, h_, 14, GRAY)
    y += 26
    U.path([(cx, y), (cx + cw, y)], arrow=False, color=GRAY)
    for row in rows:
        for k, (cell, c) in enumerate(zip(row, cols)):
            text(cx + c + 10, y + 7, cell, 15, RED if str(cell).startswith("?") else INK, MONO if k == 0 else U.SANS)
        y += 32
        U.path([(cx, y), (cx + cw, y)], arrow=False, color=GRAY)
    return y


def _open_tab(cx, cy, on):
    """Underline the open step's tab (a black drawing cannot tell it by colour); the tabs sit as screen() lays them."""
    px = cx
    for st in STEPS:
        w = len(st) * 10 + 34
        if st == on:
            for d in (0, 3, 6):
                U.path([(px, cy - 16 + d), (px + w, cy - 16 + d)], arrow=False, color=INK)
        px += w + 12


def work_closed(cx, cy, cw):
    """Reading: 2 · Run, opened from a bare link (the step that comes next); its work panel folded, its result below."""
    _open_tab(cx, cy, "2 · Run")
    text(cx, cy + 8, "Operation", 16, GRAY)
    y = _fold_row(cx, cy + 34, cw, "🧮 2 · Run", "→ next")
    text(cx, y + 10, "✎ 261022  the work panel (Input · Running now · the prompt with your notes · the sign) folds until you open its bar",
         14, GREEN)
    text(cx, y + 50, "Result", 16, GRAY)
    y = _fold_row(cx, y + 76, cw, "D · Data", "1 of 1 ✓") + 10
    y = _fold_row(cx, y, cw, "I · Information", "1 of 2", opened=True) + 12
    y = _grid(cx + 20, y, cw - 40, ["Task", "Full", "<A>", "<B>", "Cross"],
              [("t03_I01_<q> ↗", "✅", "✅", "✅", "POOL"), ("t06_I04_<q> ↗", "· not run", "·", "·", "·")],
              [0, 330, 470, 610, 750]) + 14
    y = _fold_row(cx, y, cw, "K · Knowledge", "1 of 2") + 10
    y = _fold_row(cx, y, cw, "Every Run, by Task", "the Job → Task → Run tree") + 22
    text(cx, y, "a bare link opens the step that comes next; All and hard open 2 · Run, soft opens 4 · Check", 15, GRAY)


def work_open(cx, cy, cw):
    """Working: the same Job later, 4 · Check with its work panel opened: what it has, what runs now, the prompt
    with your notes."""
    label_y = cy - 228                                    # the screens' names above them (level_drawing)
    U.path([(cx - 1644 + 170, label_y + 14), (cx - 44, label_y + 14)], color=INK)
    text(cx - 1644 + 430, label_y - 24, "the same Job, later: open a step's bar to work on it", 20, INK)
    _open_tab(cx, cy, "4 · Check")
    text(cx, cy + 8, "Operation", 16, GRAY)
    y = _fold_row(cx, cy + 34, cw, "🔍 4 · Check", "→ next", opened=True)
    ix = cx + 20
    text(ix, y + 12, "Input", 15, GRAY)
    y = _grid(ix, y + 38, cw - 40, ["", ""],
              [("Pages checked", "3 of 6 written"), ("Alignment Runs", "3 of 6"),
               ("Still to check", "t05_K02_<q> · t06_I04_<q> · t08_W01_<q>")], [0, 230]) + 12
    base("rectangle", ix, y, cw - 40, 38, INK, 1, rough=0)
    text(ix + 12, y + 9, "⏳ Running now · run-check-alignment-t05 · open since <time>", 16, INK)
    y += 54
    text(ix, y, "Prompt · alignment", 15, INK)
    base("rectangle", ix + cw - 40 - 150, y - 6, 150, 32, INK, 1.5, rough=0)
    text(ix + cw - 40 - 136, y, "Copy prompt", 16, INK)
    y += 34
    base("rectangle", ix, y, cw - 40, 92, GRAY, 1, rough=0)
    for k, line in enumerate(["Run with haipipe-insight-reviewer-agent. /haipipe-insight-check check each answered",
                              "cut of a question in <Board>/j03_code-v2_data-v2 against its question and plan, as",
                              "run-check-alignment-t<NN>. Still to check: t05_K02_<q>, t06_I04_<q>, t08_W01_<q>."]):
        text(ix + 12, y + 10 + k * 26, line, 14, INK, MONO)
    y += 92
    base("rectangle", ix, y, cw - 40, 64, INK, 1, rough=0)
    text(ix + 12, y + 8, "user feedback:", 14, GRAY, MONO)
    text(ix + 12, y + 32, "<your notes: a row, a sentence to change>", 15, INK)
    y += 64
    text(ix + 12, y + 8, 'Run this in the Claude session "<Board>: j03-prototype-p2-data-<d>v2"; start it if it is not running.', 13, GRAY, MONO)
    text(ix + 12, y + 32, "? work in place: a chat docked under the open step, or copy only (today)", 15, RED)
    y += 62
    y = _fold_row(ix, y, cw - 40, "Prompt · CHECK", "Copy prompt", h=40) + 14
    text(cx, y, "✎ 261022  Copy prompt copies the prompt, your notes and the session line; you paste them into any Claude session",
         14, GREEN)
    text(cx, y + 34, "Result", 16, GRAY)
    y = _fold_row(cx, y + 60, cw, "D · Data", "1 of 1 ✓") + 10
    y = _fold_row(cx, y, cw, "I · Information", "1 of 2") + 10
    y = _fold_row(cx, y, cw, "K · Knowledge", "1 of 2", opened=True) + 12
    y = _grid(cx + 20, y, cw - 40, ["Task", "CHECK", "alignment", "its check Run"],
              [("t04_K01_<q> ↗", "✅ <date> · a person", "run-check-alignment-t04 ✅", "run-check-t04 ✅"),
               ("t05_K02_<q> ↗", "▾ not yet · check it", "run-check-alignment-t05 · open", "—")], [0, 280, 520, 820])
    # a person's own CHECK, folded in the page's row (261023): tick, then ✅ Pass or ↩ Return with the reason
    fx = cx + 300
    base("rectangle", fx, y + 6, cw - 320, 44, INK, 1, rough=0)
    px = fx + 12
    for word, w in (("☐ I read the page and its Runs' results", 330), ("why, if it goes back", 220),
                    ("✅ Pass", 90), ("↩ Return", 110)):
        base("rectangle", px, y + 13, w, 30, INK if "Pass" in word or "Return" in word else GRAY, 1, rough=0)
        text(px + 8, y + 19, word, 15, INK if "why" not in word else GRAY)
        px += w + 10
    text(cx, y + 64, "✎ 261023  🙋 a person checks a page here: tick, then ✅ Pass, or ↩ Return with the reason "
                     "(the page's check: line, a pass of run-check-tNN, by: a person)", 14, GREEN)


PERIOD = lambda on: [[("Partition:", 0)] + [(lab, k == 1) for k, (lab, _) in enumerate(U.PARTS)],
                     [("Period:", 0), ("Current", on == 0), ("vs previous", on == 1)]]
# two dimensions (JL 261007, via the s00/s01 session): "Partition: full, female, xxx; Period: Current, compare with
# previous ... we can check whether we get the new insights, or we just keep what we found previously"


def current(cx, cy, cw):
    """Question │ Work │ Report under D · I · K · W, on the picked partition (JL 261007: "I actually want to put the
    Question Work Report to the Audience Report"); every cell opens a pop-out."""
    rep = lambda lv, q: ("? refused: power low on B" if q == "K02" else
                         "Answer: <one line> · <interval> · CHECK ✅" if lv == "K" else "Answer: <one line> · CHECK ✅")
    y = U.dikw_table(cx, cy, cw, U.LEVELS, rep)
    text(cx, y + 12, "↗ the question: question.md from p2 · the run: the Run pop-out · the page: the page · a chip: its card", 14, GRAY)


def cross_current(cx, cy, cw):
    """On Cross: each question's difference test between the partitions, and its verdict."""
    rep = lambda lv, q: "—" if lv in "DW" else ("SPLIT · the page's Cross section ↗" if q == "K02" else "POOL · the page's Cross section ↗")
    y = U.dikw_table(cx, cy, cw, U.LEVELS, rep, run="r04_cross")
    text(cx, y + 12, "Work on Cross is r04_cross: one test of the difference, never two separate tests (By heterogeneity)", 14, GRAY)


STATUS = ["All", "New question", "New finding", "Held", "Changed", "Dropped", "Not comparable"]


def vs_previous(cx, cy, cw):
    """The table against the Job before, read from run-compare-j02's report: each Report cell carries its status."""
    text(cx, cy, "j03 against j02 · the code moved (p1 → p2) · on <partition A> · from reports/vs-j02.md (run-compare-j02)", 14, INK, MONO)
    text(cx, cy + 28, "1 new question · 1 new finding · 4 held · 1 changed · 0 dropped · 1 not comparable", 17, INK)
    px = cx
    for k, lab in enumerate(STATUS):
        w = len(lab) * 8 + 26
        base("rectangle", px, cy + 60, w, 28, INK if k == 0 else GRAY, 1.5 if k == 0 else 1, rough=0)
        text(px + 12, cy + 65, lab, 13, INK if k == 0 else GRAY)
        px += w + 8
    text(cx, cy + 98, "? held = same direction and the intervals overlap; D: counts within <tolerance> (the release's compare rule)",
         13, RED)
    rep = lambda lv, q: {"K01": "Δ changed: its script changed in p2 (code)",
                         "K02": "∅ not comparable: <B> refused in j02",
                         "I01": "new finding: A > B now clear (was within noise)"}.get(q, "= held · <answer>")
    y = U.dikw_table(cx, cy + 128, cw, U.LEVELS, rep)
    text(cx, y + 12, "new question: I04, first asked in p2 · ✗ dropped = no longer answered · one clock per Job, one cause", 14, GRAY)
    text(cx, y + 40, "Propose questions → run-propose-j03 reads these statuses and the gaps ('we cannot answer <what>'), "
         "files each to the Prototype's proposals/", 14, INK)
    text(cx, y + 66, "✎ 261007  Propose questions added here: the gaps show on this view (was: Propose a change, on a Task)", 13, GREEN)


def studio(cx, cy, cw):
    text(cx, cy, "optional: a drawing about this pair", 15, GRAY)
    base("rectangle", cx, cy + 34, cw, 46, GRAY, 1, rough=0)
    text(cx + 14, cy + 46, "▸ s01-<what moved>", 17, INK, MONO)


ORDER = [("Add a Job", "Board"), ("run-launch-j03", "Job"), ("run-power-j03", "Job"), ("rNN_<partition>", "each Task"),
         ("rNN_cross", "each Task"), ("run-write", "each Task"), ("run-check", "each Task"),
         ("run-compare-j02", "Job · waits for the checks"), ("run-propose-j03", "Job · reads the compare"),
         ("run-close-j03", "Job · frozen")]


def runs(cx, cy, cw):
    """The Job's Runs by type, then the order they run in."""
    y = U.table(cx, cy, cw, ["Run", "kind · type", "target", "state"], [0, 380, 600, 800],
                ["the Job's own · soft",
                 ("run-launch-j03/ ↗", "soft · launch", "j03", "closed"), ("run-power-j03/ ↗", "soft · power", "every cut", "closed · B low"),
                 ("run-compare-j02/ ↗", "soft · compare", "j02 → reports/vs-j02.md", "closed"),
                 ("run-propose-j03/ ↗", "soft · propose", "→ the Prototype's proposals/", "closed · 2 filed"),
                 ("run-close-j03/ ↗", "soft · close", "j03", "✅ frozen"),
                 "its Tasks'",
                 ("t04_K01 › r01_full/ ↗", "hard · partition", "K01", "ok"), ("t04_K01 › r02_<A>/ ↗", "hard · partition", "K01", "ok"),
                 ("t05_K02 › r03_<B>/ ↗", "hard · partition", "K02", "? refused: power"),
                 ("t04_K01 › r04_cross/ ↗", "hard · cross", "K01", "POOL"),
                 ("t04_K01 › run-write-t04/ ↗", "soft · write", "K01", "closed"), ("t04_K01 › run-check-t04/ ↗", "soft · check", "K01", "✅")],
                mono=(0,))
    text(cx, y + 26, "the order a Job runs in", 15, INK)
    x, yy = cx, y + 60
    for k, (name, who) in enumerate(ORDER):
        w = max(len(name) * 9.5, len(who) * 7) + 28
        if x + w > cx + cw:
            x, yy = cx, yy + 80
        base("rectangle", x, yy, w, 52, INK, 1, rough=0)
        text(x + 10, yy + 6, name, 13, INK, MONO)
        text(x + 10, yy + 28, who, 11, RED if "waits" in who else GRAY)
        if k < len(ORDER) - 1:
            U.path([(x + w + 2, yy + 26), (x + w + 18, yy + 26)], color=INK)
        x += w + 22
    text(cx, yy + 70, "a row's ↗ opens the Run pop-out · compare waits for every check; propose reads the compare; close "
         "freezes the Job", 14, GRAY)
    text(cx, yy + 98, "✎ 261007  run-propose-j03 added between compare and close (a row above, a box here)", 13, GREEN)


def delivery(cx, cy, cw):
    base("rectangle", cx, cy, cw, 150, RED, 1, dashed=True, rough=0)
    text(cx + 14, cy + 14, "? W01's counsel for this pair, if this is the latest Job", 16, RED)
    text(cx + 14, cy + 50, "→ Block › Delivery › Handoff, naming j03_code-v2_data-v2", 15, INK)


JOB = "j03_code-v2_data-v2/"
SCREENS = [
    ("Description", DESC(0), ["Open the release ↗"], "read only: the release is\nchanged in the Prototype Block", job_prototype,
     [("work/bNN_<topic>_prototype/j02_code-v2/", "the release, used by path + hash"), ("├── release.yaml", "its questions"),
      ("├── partitions.md · thresholds.yaml", "its cuts and power"), ("├── src/ · configs/", "the shared code"),
      ("└── tNN_<L><NN>_<q>/scripts/", "each question's own script")]),
    ("Description", DESC(1), [], "", job_dataset,
     [("$EXTRACTS/<d>v2", "the data version, frozen"), (JOB + "j03_code-v2_data-v2.md", "pins: j02_code-v2 (hash) · <d>v2 · state"),
      (JOB + "tNN_…/runs/rNN_<partition>/result/partition_power.csv", "power, per question")]),
    ("Audience Report", PERIOD(0), ["Write a report", "Check a report"], "", current,
     [(JOB + "tNN_<L><NN>_<q>/tNN_….md", "Report: the page, at the picked partition"),
      (JOB + "tNN_…/runs/rNN_<partition>/", "Work: the Run"), ("work/…_prototype/j02_code-v2/tNN_…/question.md", "Logic: the question")]),
    ("Audience Report", [[("Partition:", 0), ("Full", 0), ("<partition A>", 0), ("<partition B>", 0), ("Cross", 1)],
                         [("Period:", 0), ("Current", 1), ("vs previous", 0)]], ["Pool or split"], "", cross_current,
     [(JOB + "tNN_…/runs/rNN_cross/", "the difference test"), (JOB + "tNN_…/tNN_….md", "its Cross section")]),
    ("Audience Report", PERIOD(1), ["Compare with j02", "Propose questions"], "run-compare-j02/ · after\nevery check", vs_previous,
     [(JOB + "runs/run-compare-j02/", "soft: reads both Jobs' results and pages"),
      (JOB + "reports/vs-j02.md", "generated: this view reads only it"),
      ("work/…_prototype/j02_code-v2/thresholds.yaml", "compare: the held rule, fixed in the release"),
      (JOB + "runs/run-propose-j03/", "soft: files new or changed questions"),
      ("work/bNN_<topic>_prototype/proposals/<slug>.md", "kind · DIKW level · from j03 · why"),
      ("insights/bNN_<topic>/reports/", "the same across all Jobs (s11)")]),
    ("Work Details", WORK_TABS("2 · Run"), ["rNN_<partition>", "run-pool-t<NN>"],
     "r02_<partition A>  ok", work_closed,
     [(JOB + "tNN_<L><NN>_<q>/runs/rNN_<partition>/run.yaml", "2 · Run: a cell's mark, its status"),
      (JOB + "tNN_<L><NN>_<q>/tNN_….md", "answer-status: 3 · Write · check: 4 · Check"),
      (JOB + "runs/run-<type>-<jNN>/", "the Job's own: launch · power · compare · close"),
      ("haipipe-insight-workflow/ref/run-cards.md", "each tab's buttons: Job › Work Details · views <step>")]),
    ("Work Details", WORK_TABS("4 · Check"), ["run-check-alignment-t<NN>", "run-check-t<NN>"],
     "run-check-alignment-t05  open", work_open,
     [(JOB + "tNN_…/runs/run-check-alignment-tNN/", "alignment: the reviewer's Run"),
      (JOB + "tNN_…/runs/run-check-tNN/", "the page's CHECK, by another agent"),
      (JOB + "tNN_…/tNN_….md", "check: ✅ <date>  (the verdict line)"),
      (JOB + "j03_code-v2_data-v2.md", "session: the Job's Claude session (optional)")]),
    ("Idea Studio", None, ["Add a topic"], "", studio, [(JOB + "studio/", "optional")]),
    ("Runs", [("All", 1), ("hard", 0), ("soft", 0), ("launch", 0), ("power", 0), ("compare", 0), ("propose", 0), ("close", 0)],
     ["Run the Job", "Run a partition", "Compare with j02", "Propose questions", "Close the Job"], "", runs,
     [(JOB + "runs/run-<type>-<target>/", "the Job's soft Runs: launch · power · compare · propose · close"),
      (JOB + "tNN_…/runs/rNN_<partition>/", "hard: result/ · passes/"), (JOB + "tNN_…/runs/run-<type>-<target>/", "soft: write · check")]),
    ("Delivery", None, [], "", delivery, [("? " + JOB + "delivery/", "? only when it is the latest Job")]),
]

POPOUTS = [  # each cell opens one: the question (Logic), the Run (Work), the page (Report), the card (a chip)
    ("K01 · the question  ·  from release p2", [
        ("work/bNN_<topic>_prototype/j02_code-v2/t04_K01_<q>/question.md", GRAY),
        ("ask: <question>, one thing, at Knowledge", INK), ("why now: <the reason>", INK),
        ("needs: E1 compute <spec> · E2 cite <source>", INK),
        ("method: ask By estimand ↗ · answer By hypothesis test ↗ · read By multiverse ↗", RED),
        ("signed ✅ <date> · agreed ✅ <date> by another agent · read only here", GRAY)]),
    ("r02_<partition A>  ·  the Run", [
        ("run.yaml: hard · partition <A> · target t04_K01", INK),
        ("pins: question K01 · script <hash> · release p2 · data <d>v2", INK),
        ("n <n> on <A> · power ok (smallest effect <pp>)", INK),
        ("passes: p01 <MMDD> ok", GRAY),
        ("[ result/ preview: metrics · the first figure ]", GRAY),
        ("result/report.md (generated) → the page cites it", INK),
        ("open the folder  ·  Rerun  ·  Check", GRAY)]),
    ("r04_cross  ·  the difference test", [
        ("run.yaml: hard · Cross · target t04_K01", INK),
        ("the difference test: A vs B, <statistic>, <p>", INK),
        ("verdict: POOL (one answer for both cuts)", INK),
        ("[ result/ preview: A and B side by side, the difference ]", GRAY),
        ("result/report.md → the page's Cross section", INK),
        ("open the folder  ·  Rerun  ·  Check", GRAY)]),
    ("K01 · the page  ·  at <partition A>", [("Answer", INK), ("  <one claim, how sure, its rivals, its limits>", GRAY),
                                            ("Evidence", INK), ("  <cited run: t04_K01 › r02_<A>> ↗", GRAY),
                                            ("read: By multiverse ↗ · the same sign and size across the choices", RED)]),
    U.card_window("By model comparison")]

QUESTIONS = [
    "? Description: Prototype · Dataset only; the pair's line opens Description › Prototype",
    "? vs previous comes from run-compare-j02 (reports/vs-j02.md); its held rule is the release's (thresholds.yaml)",
    "? statuses: new question · new finding · held · changed · dropped · not comparable",
    "? run types by level (Job: launch · power · compare · close), and the Job's run order",
    "? a partition too weak for one question in this Job: refused and shown, or left out of the table",
    "? Delivery: only the latest Job's Wisdom counsel goes to the Board's handoff",
    "? a new question answered on data already seen: exploratory until the next data version confirms it",
    "? the next Job (p3 × the same data): rerun the unchanged questions, or link their earlier Runs by hash",
    "? one name for proposing at the Board and the Job: run-propose-<target>, both with Propose questions",
    "? the Task's Work as steps too (s13): Plan · Run cuts · Pool · Write · Check",
    "? work in place: a chat docked under the open step, or copy to a session only (today)",
]


ASIDES = {"Work Details": ("one Job through its six steps (built 261022)", [
    ("what it is", "read each step's result; open its bar to work on it · workbench-insight 1.2.0"),
    ("1 · Launch", "reads the release's thresholds.yaml → run-launch, run-power: n and power per cut"),
    ("2 · Run", "each Task's run.sh (question and script from the release) → result/, run.yaml; rNN_cross → run-pool"),
    ("3 · Write", "the Runs' result/report.md → the page and its answer-status, D → I → K → W, then X (Executive)"),
    ("4 · Check", "alignment: against the question and plan; CHECK: every number back to result/ → the check: line"),
    ("5 · Compare", "both Jobs' results and pages → reports/vs-<prev>.md; the gaps → the Prototype's proposals/"),
    ("6 · Close", "every page checked, the comparison written → 🙋 Sign the close on the screen, or the prompt"),
    ("✎ 261023", "🙋 by hand: CHECK a page (4 · Check) and sign the close (6 · Close), POST /_board/insight-act"),
    ("its chip", "from those files: ✓ done · → next (the first not done) · later · optional · sign (the close)"),
    ("words", "a cut: a partition of the rows (Full, <A>, <B>) · Cross: one test across the cuts, POOL or SPLIT"),
    ("? the Task", "the Task's Work as steps too (s13): Plan · Run cuts · Pool · Write · Check")]),
          "Idea Studio": ("typical topics, j0N_…/sNN-<topic>/", [
    ("s01-<what moved>", "this pair against the Job before: what changed, and why"),
    ("s02-<a surprise>", "an answer that did not hold: drawn, then a proposal"),
    ("? s03-<partition story>", "why a cut pooled or split here")]),
          "Runs": ("run types, by level (proposed)", [
    ("Job · soft", "run-launch · run-power (n and power per cut, before any outcome) · run-compare · run-propose · run-close"),
    ("Task · hard", "rNN_<partition> · rNN_cross (the difference test)"),
    ("Task · soft", "run-write · run-check · run-sign (W only: a person signs the counsel)"),
    ("Board · soft", "run-add-version-vM · run-add-job-jNN · run-coverage · run-track-<q> · run-consistency-<jA>-<jB> · "
                     "run-report-<qNN> · run-check-<qNN> · run-handoff (s11)"),
    ("✎ 261007", "Job: + run-propose · Board: in s11's words (was run-check-board · run-read-<reading>)"),
    ("Prototype · soft", "run-propose · run-open-release-pN · run-define-cuts (cuts · thresholds · compare rule)"),
    ("  per question", "run-ask · run-plan · run-review-plan · run-script · run-review-script"),
    ("  the release", "run-sign-release (a person) · run-close-release")])}


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s12-job-level.excalidraw"
    U.level_drawing(out, Path(__file__).name, "Job",
                    "Job level: one Prototype version × one data version (j03_code-v2_data-v2)",
                    "After s00: a Job pins a release and a data version; its questions sit under D · I · K · W headings.",
                    MOVES, SCREENS, POPOUTS, QUESTIONS, ASIDES, changes=CHANGES)


if __name__ == "__main__":
    main()
