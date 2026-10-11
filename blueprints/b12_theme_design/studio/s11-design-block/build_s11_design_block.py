"""b12 s11 · Design Block: s11-design-block.excalidraw, the design Board's tab on the shared frame, its Spaces
as full screens (JL 261007: "s11, s12, s13 … for the Block level, Job level and task level"; "check s11 s12
and s13 [of b11] … borrow their ideas").

One application, one channel: its goals, the inputs every Job reads, its Jobs (goal × method version ×
inputs version, s00), and what they release. Borrowed from b11's Block: Description's Map crosses two axes
(here goals down × registered methods across, the chain of Jobs in each cell); Work Details opens a Job in
place to its t00 · t01 – tNN · t99; Audience Report is the Block's own questions, answered across Jobs, what
each Job cost, each tested design's prediction against the Exp, and the method scorecard (JL 261007). Every list is a card, as the Job's (s12: "change it to cards"); every design shows
as it reads; "on disk" is a tree from the Block folder. Placeholders only; written through canvas.write, so
every mark a person adds survives a rebuild.

    python build_s11_design_block.py [out.excalidraw]
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "_build"))
import design_ui as U  # noqa: E402

text, base, INK, GRAY, RED, MONO = U.text, U.base, U.INK, U.GRAY, U.RED, U.MONO
fold, note, phone = U.fold, U.note, U.phone

MOVES = [("Board › Design Tasks: a list of Design folders", "Work Details: one card per Job; open, its t00 · t01 – tNN · t99"),
         ("(none)", "Description › Map: goals down × registered methods across, the Jobs in each cell"),
         ("Brief Folder 0-BR-brief/", "Description › Goals: the goal list (the Brief merged in)"),
         ("design-goal.md · Theory of Design", "Description › Inputs: rules · theory · handoff, versioned i1, i2 …"),
         ("(none)", "Description › Methods: the registered methods in use, read from the design skill"),
         ("(none)", "Audience Report: Questions · Cost · Predicted vs observed · Method scorecard"),
         ("Delivery: word for word", "Delivery: every released design as it reads, across Jobs, to the Exp")]

DESC = lambda on: [(lab, on == k) for k, lab in enumerate(["Map", "Goals", "Methods", "Inputs"])]
AR = lambda on: [(lab, on == k) for k, lab in enumerate(["Questions", "Cost", "Predicted vs observed", "Method scorecard"])]
SMS = "<opening>. <the reason>. <the ask>: {LINK}"


def block_map(cx, cy, cw):
    cy = note(cx, cy, "261007  columns are registered methods (M01 … M05, s03), each a type of one of the 13 cards")
    y = U.goal_map(cx, cy + 6)
    text(cx, y + 24, "a cell's Jobs are one chain: each moved one clock (method or inputs) from the one above", 14, GRAY)
    note(cx, y + 76, "261007  two Jobs in a cell → ↗ what moved and what it changed (a pop-out; was the Versions view)")
    text(cx, y + 50, "two Jobs in one row, different columns = the same goal by two methods: they compare (Method scorecard)", 14, GRAY)


def goals(cx, cy, cw):
    cy = note(cx, cy, "261007  one card per goal (was a table); run-setup-goal-jNN pins one into a Job (s12)")
    y = fold(cx, cy, cw, "G01 <goal>", "for <audience> · sms · N = 10 · Jobs j01 – j04 · signed ✅",
             [("aim", "<the behaviour to change>"), ("who", "<audience>"), ("venue", "sms · <n> characters · venue-sms ↗"),
              ("N", "10 designs a Job (N + 5 ideas)"), ("rules", "1 for this goal only; the shared ones come with inputs"),
              ("leave out", "<what>"),
              ("Jobs", "j01 j02 j03 on M04 · j04 on M01"), ("signed", "✅ <date> · a person")])
    y = note(cx, y, "261007  as the Job's Goal cards (s12): its own rules here, the shared ones in Inputs")
    y = fold(cx, y, cw, "G02 <goal>", "for <audience> · sms · N = 10 · Job j05 · signed ✅")
    y = fold(cx, y, cw, "G03 <goal>", "proposed · not signed · + Add a Job", red=True)
    text(cx, y + 6, "the goal is set here once; every Job on it reads the same words (its inputs/goal.md)", 14, GRAY)


def methods(cx, cy, cw):
    cy = note(cx, cy, "261007  no methods Block (JL): a registered method is a card in the design skill, read here")
    cy = note(cx, cy, "261007  one card per registered method (was a by-<method> table)")
    text(cx, cy, "read only: haipipe-design-unit/methods/ · the ones this Block's Jobs use first", 14, GRAY)
    y = fold(cx, cy + 30, cw, "M04 · Actionable insights", "type By insight · m1 · m2 · Jobs j01 j02 j03",
             [("type", "By insight (one of the 13 cards ↗)"),
              ("versions", "m1 (j01 · j02) · m2 (j03): Δ ② spread, Δ ⑤ top N of N + 5"),
              ("① sees", "goal · rules · ours: the insight handoff"),
              ("runs it", "designer agent ①②③ · ? a reviewer agent ④⑤"),
              ("scorecard", "pass 70% (m2) · prediction in range 1 of 2")], mono_title=False)
    y = fold(cx, y, cw, "M01 · Goal only", "type By goal · m1 · Jobs j04 j05 · the baseline")
    for m, t in [("M02 · Overall performance", "type By precedent"), ("M03 · Detailed evidence", "type By insight"),
                 ("M05 · Raw-data agent", "type By insight")]:
        y = fold(cx, y, cw, m, t + " · no Job here yet")
    y = fold(cx, y, cw, "proposals from this Block", "2 · widen the spread (M04, j02's review whole) · retire M01? (the Exp)",
             red=True)
    text(cx, y + 6, "a proposal goes to the registry (run-propose-method-<slug>); a new version is cut there, not here", 14, GRAY)


def inputs(cx, cy, cw):
    cy = note(cx, cy, "261007  one card per inputs version; its parts labelled as step ①'s parts (s03), as the Job's (s12)")
    y = fold(cx, cy, cw, "i1", "start · rules r1 · handoff W-02 · Job j01", mono_title=True)
    y = fold(cx, y, cw, "i2", "a new handoff · rules r2 · W-03 · Jobs j02 – j05",
             [("Goal · how much is set", "rules.md · r2, the shared rules (run-setup-rules)"),
              ("Information · whose", "ours: the insight Block's signed handoff"),
              ("Information · form", "handoff-W-03.md · theory/ <papers>  (the venue profile comes from the skill, s12)"),
              ("Examples", "past released designs, from Delivery (a method picks them or not)"),
              ("new since i1", "W-03 replaced W-02; r2.3 added"),
              ("frozen", "✅ <date> · each file's sha256 in i2/manifest.yaml")], mono_title=True)
    y = fold(cx, y, cw, "i3", "lands with W-04 · + Add a Job", red=True, mono_title=True)
    text(cx, y + 6, "a Job's own inputs/ is its fence: relative links into one version, plus a frozen manifest.yaml", 14, GRAY)
    text(cx, y + 30, "(each file's sha256), the only thing its design work sees; a Job takes only the parts its method picks (s12)", 14, GRAY)


def pill(x, y, s, red=False):
    """A small rounded label, the workbench's item-kind pill (Question N · Task Work · Report)."""
    w = len(s) * 8.4 + 18
    r = base("rectangle", x, y, w, 24, RED if red else U.TEAL, 1.2, dashed=red, rough=0)
    r["roundness"] = {"type": 3}
    text(x + 9, y + 3, s, 13, RED if red else U.TEAL, MONO)
    return x + w + 8


QROWS = [  # (question, mark, title, the question, Task Work rows, tree, report status, report title, its opening)
    ("Question 1", "🟡", "Which method suits G01?", "M04 m2 against M01 m1 on G01, the same inputs i2",
     ["1. j03 · G01 × M04 m2 × i2 · 8 of 10 passed · d04 tested → ranking.csv · scores.csv",
      "2. j04 · G01 × M01 m1 × i2 · 2 of 4 passed · d02 tested → scores.csv"],
     ["b01 <app>", "   j03 g01_m04 ▸ 15 designs · released", "   j04 g01_m01 ▸ 4 designs · verify"],
     "Not answered yet", "Q01 · Which method suits G01? ↗", "<the opening: what the two Jobs show so far>"),
    ("Question 2", "✅", "Did m2 beat m1?", "",
     ["1. j02 · G01 × M04 m1 × i2 · 6 of 6 passed → ranking.csv", "2. j03 · G01 × M04 m2 × i2 · 8 of 10 passed → ranking.csv"],
     ["b01 <app>", "   j02 g01_m04 ▸ 6 designs · closed", "   j03 g01_m04 ▸ 15 designs · released"],
     "Answered", "Q02 · Did m2 beat m1? ↗", "<the opening: the answer, one paragraph>")]


def questions(cx, cy, cw):
    """Each Block question a row: Question │ Task Work │ Report (JL 261007: "I want this style for the Question Work
    Report", the workbench's own rows)."""
    cy = note(cx, cy, "261007  each question a row: Question │ Task Work │ Report, the workbench's style (JL; was folding cards)")
    C1, C2 = 300, 680
    for h, x in [("Question", 0), ("Task Work", C1), ("Report", C2)]:
        text(cx + x + 10, cy, h, 13, GRAY)
    y = cy + 24
    for q, mark, title, ask, work, tree, status, rtitle, opening in QROWS:
        h = 64 + 22 * (len(work) * 2 + len(tree)) + 20
        base("rectangle", cx, y, cw, h, GRAY, 1, rough=0)
        for x in (C1, C2):
            U.path([(cx + x, y), (cx + x, y + h)], arrow=False, color=GRAY)
        nx = pill(cx + 12, y + 12, q)
        text(nx, y + 12, mark, 16, INK)
        text(cx + 12, y + 46, "\n".join(U.wrap(title, 30)), 16, INK)
        if ask:
            text(cx + 12, y + 74, "\n".join(U.wrap(ask, 34)), 14, INK)
        text(cx + 12, y + h - 30, "› More", 13, U.TEAL)
        nx = pill(cx + C1 + 12, y + 12, "Task Work")
        text(nx, y + 15, f"{len(work)} Jobs", 13, GRAY)
        yy = y + 46
        for w in work:
            text(cx + C1 + 12, yy, "\n".join(U.wrap(w, 46)), 13, INK)
            yy += 22 * len(U.wrap(w, 46)) + 4
        for t in tree:
            text(cx + C1 + 12, yy, t, 12, GRAY, MONO)
            yy += 20
        nx = pill(cx + C2 + 12, y + 12, "Report")
        text(nx, y + 15, status, 13, GRAY)
        text(cx + C2 + 12, y + 46, rtitle, 15, INK)
        text(cx + C2 + 12, y + 74, "\n".join(U.wrap(opening, 44)), 13, INK)
        text(cx + C2 + 12, y + h - 30, f"report {rtitle[:3].lower()}", 12, GRAY)
        y += h + 10
    y = fold(cx, y, cw, "Q04 does M04 m2 hold on G02?", "proposed by run-propose-questions: no Job on G02 × M04 yet · agreed ✅", red=True)
    text(cx, y + 6, "a Block question needs evidence from two or more Jobs; one Job's is the Job's (s12)", 14, GRAY)


def cost(cx, cy, cw):
    """What each Job spent to make its designs: the Job's Performance (s12), one card each."""
    cy = note(cx, cy, "261007  one card per Job (was a table); each reads the Job's Performance (s12)")
    y = fold(cx, cy, cw, "j03", "M04 m2 · i2 · <n>k tok and <m> min a design · 7 of 10 first try",
             [("tokens / design", "<n>k  (generate + every verify and revise)"), ("time / design", "<m> min"),
              ("rounds", "1.2 drafts a design"), ("first try", "7 of 10 passed on draft 1"),
              ("per passed", "<n>k tok: all tokens / passed designs"), ("ideas", "t00: <n>k tok · t99: <n>k tok")],
             mono_title=True)
    for j, s in [("j02", "M04 m1 · i2 · <n>k tok · <m> min · 5 of 10 first try"),
                 ("j01", "M04 m1 · i1 · <n>k tok · <m> min · 4 of 10 first try"),
                 ("j04", "M01 m1 · i2 · <n>k tok · <m> min · 6 of 10 first try")]:
        y = fold(cx, y, cw, j, s, mono_title=True)
    text(cx, y + 6, "time: each Run's started_at → finished_at · tokens: ? not in the Run receipt yet (add usage:)", 14, RED)


def predicted(cx, cy, cw):
    """Each tested design as it reads, its frozen prediction, and the Exp's result for its arm."""
    cy = note(cx, cy, "261007  each tested design as it reads (a phone), its prediction beside the Exp (was a table)")
    C1, C2 = 330, 690
    for h, x in [("Design", 0), ("Predicted · frozen at release (s12)", C1), ("Observed · the Exp, its arm", C2)]:
        text(cx + x + 10, cy, h, 13, GRAY)
    y, h = cy + 24, 200
    base("rectangle", cx, y, cw, h, GRAY, 1, rough=0)
    for x in (C1, C2):
        U.path([(cx + x, y), (cx + x, y + h)], arrow=False, color=GRAY)
    text(cx + 12, y + 10, "▾ j03 · d04", 15, INK, MONO)
    phone(cx + 22, y + 38, SMS)
    for k, s in enumerate(["+x [lo, hi] against the control", "by the ④ ⑤ reviewer · <date>",
                           "run-freeze-predictions-j03", "M04 m2 · i2"]):
        text(cx + C1 + 12, y + 12 + k * 26, s, 13, INK if k == 0 else GRAY)
    for k, s in enumerate(["+y [lo, hi] · arm B", "observed/e01_<exp>/arms.csv", "direction ✓ · in range ✓"]):
        text(cx + C2 + 12, y + 12 + k * 26, s, 13, INK if k != 1 else GRAY)
    y += h + 8
    for d, prev, pred, obs, bad in [("j02 · d06", "<opening>. <the reason as a question> …", "+x [lo, hi]", "✓ direction · ✗ range", 1),
                                    ("j04 · d02", "<opening>. <the ask> …", "+x [lo, hi]", "✗ direction · ✗ range", 1),
                                    ("j03 · d01", "<opening>. <the reason> …", "+x [lo, hi]", "not tested", 0)]:
        base("rectangle", cx, y, cw, 38, GRAY, 1, rough=0)
        text(cx + 12, y + 10, "▸ " + d, 15, INK, MONO)
        text(cx + 150, y + 11, prev, 13, INK)
        text(cx + C1 + 12 + 180, y + 11, pred, 13, GRAY)
        text(cx + C2 + 12, y + 11, obs, 13, RED if bad and "✗" in obs else GRAY)
        y += 44
    text(cx, y + 8, "observed: observed/e01_<exp>/arms.csv, per-arm totals (run-add-observed-e01); never patient rows", 14, GRAY)
    text(cx, y + 34, "the match: run-score-e01 reads each prediction.yaml + arms.csv, once per Exp; a Job's view shows its rows", 14, GRAY)


def scorecard(cx, cy, cw):
    """One card per method version: what it costs, how its designs pass, and how well it predicts."""
    cy = note(cx, cy, "261007  one card per method version (was a table)")
    y = fold(cx, cy, cw, "M04 m2", "j03 · pass 70% · <n>k tok per passed · predictions 1 of 2 in range",
             [("Jobs", "j03"), ("per passed", "<n>k tok"), ("pass rate", "70% (7 of 10 first try)"),
              ("tested", "2 designs"), ("direction", "1 of 2"), ("in range", "1 of 2"), ("rank match", "ρ <r> (n 2): a hint")],
             mono_title=True)
    y = fold(cx, y, cw, "M04 m1", "j01 · j02 · pass 45% · predictions 1 of 2 in range", mono_title=True)
    y = fold(cx, y, cw, "M01 m1", "j04 · j05 · pass 60% · predictions 0 of 1 in range", mono_title=True)
    text(cx, y + 6, "every card shows how many designs were tested: with few arms, the rank match is only a hint", 14, GRAY)
    text(cx, y + 32, "M04 m2 against m1 on the same inputs → a proposal to the registry (keep, fix or retire)", 14, GRAY)


TILES = [("t01 · d01", "<opening>. <the reason>. <the ask>", "✓ passed · #2 kept"),
         ("t02 · d02", "<opening>. <the reason as a question>", "✓ passed · #5 kept"),
         ("t03 · d03", "<opening>. <the ask>", "✓ passed · #7 kept"),
         ("t04 · d04", "<opening>. <the reason>. <the ask>", "✓ draft 2 · #1 kept"),
         ("t05 · d05", "<opening>. <the ask>", "✗ T0 r2.3 · dropped"),
         ("t06 · d06", "<sender>. <the reason>", "✓ passed · #4 kept")]


def tile(x, y, w, h, title, lines, color=GRAY):
    """A small Task tile inside an open Job card: its name, then a few lines; opens the Task tab (s13)."""
    base("rectangle", x, y, w, h, color, 1, rough=0)
    text(x + 10, y + 8, title, 13, INK, MONO)
    for k, (ln, c) in enumerate(lines):
        text(x + 10, y + 32 + k * 20, ln, 12, c)


def mini_phone(x, y, w, title, msg, state):
    """A design Task as a tile: the message as it reads (a small bubble), its state underneath."""
    base("rectangle", x, y, w, 150, RED if "✗" in state else GRAY, 1, rough=0)
    text(x + 10, y + 8, title, 13, INK, MONO)
    ls = U.wrap(msg + ": {LINK}", 19)[:3]
    b = base("rectangle", x + 10, y + 32, w - 20, 16 + len(ls) * 17, GRAY, 1, rough=0)
    b["backgroundColor"] = "#f1f3f5"
    for k, ln in enumerate(ls):
        text(x + 16, y + 38 + k * 17, ln, 11, U.TEAL if "{LINK}" in ln else INK)
    text(x + 10, y + 124, state, 12, RED if "✗" in state else GRAY)


def work(cx, cy, cw):
    cy = note(cx, cy, "261007  one card per Job (was a table); open, its Tasks as the Job shows them (s12)")
    y = fold(cx, cy, cw, "j01_<goal>_<design-method>", "G01 · M04 m1 · i1 · start · 5 of 10 · closed ✅", mono_title=True)
    y = fold(cx, y, cw, "j02_<goal>_<design-method>", "G01 · M04 m1 · i2 · inputs moved · 6 of 10 · closed ✅", mono_title=True)
    # j03 open: a preview of its Tasks (JL 261007: "could we have a preview of the tasks as well?")
    top, H = y, 440
    base("rectangle", cx, top, cw, H, GRAY, 1, rough=0)
    text(cx + 14, top + 13, "▾", 16, GRAY)
    title = "j03_<goal>_<design-method>"
    text(cx + 40, top + 12, title, 17, INK, MONO)
    text(cx + 40 + len(title) * 10.4 + 24, top + 15, "G01 · M04 m2 · i2 · method moved · 10 kept · released ✅", 14, GRAY)
    U.path([(cx, top + 46), (cx + cw, top + 46)], arrow=False, color=GRAY)
    ix, iy = cx + 20, note(cx + 20, top + 56, "261007  a preview of its Tasks: t00's ideas, each design as it reads, t99's ranking")
    text(ix, iy, "set up  ✓ run-setup-goal-j03 · ✓ -method · ✓ -inputs", 13, GRAY, MONO)
    iy += 30
    tile(ix, iy, 330, 96, "t00 · reason ideas", [("② 6 topics → I01 – I15", INK), ("T1 why click at all → I01 I02", GRAY),
                                                       ("closed ✅", GRAY)])
    tile(ix + 350, iy, 330, 96, "t99 · review whole", [("⑤ ranked 15 · kept 10 · dropped 5", INK),
                                                          ("#1 d04 · #2 d01 · #3 d09 …", GRAY), ("closed ✅", GRAY)])
    tile(ix + 700, iy, cw - 740, 96, "released", [("d01 · d04 → Delivery", INK), ("predictions frozen", GRAY), ("✅ <date>", GRAY)])
    iy += 112
    text(ix, iy, "t01 – t15  ③ ④  one design each, in order", 13, GRAY)
    iy += 24
    tw = (cw - 40 - 6 * 10 - 110) / 6
    for k, (t, msg, state) in enumerate(TILES):
        mini_phone(ix + k * (tw + 10), iy, tw, t, msg, state)
    text(ix + 6 * (tw + 10) + 8, iy + 60, "+ 9 more ›", 14, U.TEAL)
    y = top + H + 10
    y = fold(cx, y, cw, "j04_<goal>_<design-method>", "G01 · M01 m1 · i2 · 7 of 10 · verify", mono_title=True)
    text(cx, y + 6, "a tile opens that Task's tab (s13); a card's name opens the Job tab (s12) to work on it", 14, GRAY)


def studio(cx, cy, cw):
    for i, t in enumerate(["▸ s01-<goal map>", "▸ s02-<method comparison>"]):
        base("rectangle", cx, cy + i * 56, cw, 46, GRAY, 1, rough=0)
        text(cx + 14, cy + 12 + i * 56, t, 17, INK, MONO)


def runs(cx, cy, cw):
    """The Block's Runs, all soft (JL 261007: "all the runs are the soft run"), grouped by what they are for."""
    cy = note(cx, cy, "261007  every Block Run is soft (JL): it writes the Block's own files; hard Runs sit in a Job's Tasks (s12)")
    cy = note(cx, cy, "261007  grouped by purpose (was All · hard · soft): set up · launch a Job · report")
    text(cx, cy, "① set up, before any Job: what a Job will pin", 15, INK)
    y = cy + 28
    for r, t in [("run-add-goal-g01", "G01 into the goal list · a person signs ✅"),
                 ("run-setup-rules", "the shared rules r2 · signed ✅"),
                 ("run-add-inputs-i2", "inputs i2: rules · theory · handoff W-03, frozen ✅")]:
        y = fold(cx, y, cw, r, t, mono_title=True)
    text(cx, y + 4, "② launch a Job: one goal × one registered method × one inputs version", 15, INK)
    y = fold(cx, y + 32, cw, "run-add-job-j04", "G01 × M01 m1 × i2 → j04 · closed ✅",
             [("needs", "a signed goal · a registered method (the skill) · a frozen inputs version"),
              ("makes", "j04_<goal>_<design-method>/, empty, its pins written"),
              ("then, in the Job", "run-setup-goal-j04 → -method-j04 → -inputs-j04 = set up → t00 … (s12)")], mono_title=True)
    text(cx, y + 4, "③ report: what came back, the questions, the answers", 15, INK)
    y += 32
    for r, t in [("run-add-observed-e01", "Exp e01's per-arm totals into observed/ · frozen ✅"),
                 ("run-score-e01", "every arm's design: direction · in range · error → scores.csv ✅"),
                 ("run-propose-questions", "reads the Map, scores, scorecard → Q04 · Q05 proposed; another agent agrees"),
                 ("run-report-q01", "Q01's report, from the Jobs it names · open")]:
        y = fold(cx, y, cw, r, t, mono_title=True)
    text(cx, y + 4, "also: run-propose-method-<slug> (Methods) · run-draw-<sNN> (Idea Studio) · run-plan-test-<app> (outside the theme)", 13, GRAY)


def delivery(cx, cy, cw):
    cy = note(cx, cy, "261007  every released design as it reads (a phone), in order, each naming its Job (was word for word)")
    for k, (d, j, when) in enumerate([("d01", "j03 · M04 m2 · i2", "✅ <date>"), ("d04", "j03 · M04 m2 · i2", "✅ <date>"),
                                      ("d02", "j04 · M01 m1 · i2", "✅ <date>")]):
        x = cx + k * 350
        base("rectangle", x, cy, 330, 300, GRAY, 1, rough=0)
        text(x + 14, cy + 12, "G01 · " + d, 15, INK, MONO)
        yb = phone(x + 20, cy + 44, SMS)
        text(x + 20, yb + 14, j, 13, GRAY)
        text(x + 20, yb + 38, "released " + when + " · predicted +x", 13, GRAY)
    text(cx, cy + 330, "→ the Exp (outside the theme); its result returns through an insight Block as a new handoff", 15, INK)
    text(cx, cy + 358, "a UI design shows its rendered screen; designs.json beside it holds the words for the Exp", 14, GRAY)


# "on disk" under each screen: a tree from the design Block's folder (JL 261007: "it should start from the block
# folder level"), as the Job's (s12)
B, J = "bNN_<app>/", "jNN_<goal>_<design-method>/"
TREE = ("✎ 261007  a tree from the Block folder (was loose paths)", "")
DISK = {
    "Map": [(B, "the design Block"), ("├── board.md", "the goal list, the close"),
            ("└── " + J, "a cell's Jobs: pins goal · method · inputs"), ("    └── jNN_<goal>_<design-method>.md", "its pins, read for the cell")],
    "Goals": [(B, ""), ("├── board.md", "## Goals: one card each, signed"), ("├── 0-BR-brief/", "retired: merged into the goal list"),
              ("└── " + J + "inputs/goal.md", "a Job's copy, by run-setup-goal-jNN (s12)")],
    "Methods": [(B, ""), ("└── " + J + "inputs/method.md -> …", "a Job's pin, linked by run-setup-method-jNN"),
                ("haipipe-design-unit/methods/", "the registry, in the design skill (generic)"),
                ("├── M04-actionable-insights.md", "its five steps' choices · its type · its versions"),
                ("└── M01 … M05 …", "the registered methods")],
    "Inputs": [(B, ""), ("├── inputs/", "the Block's inputs versions"), ("│   ├── i1/ · i2/", "rules · theory · handoff links"),
               ("│   └── i2/manifest.yaml", "each file's sha256; frozen"),
               ("└── " + J + "inputs/", "a Job's fence: links into iN + its manifest (s12)"),
               ("insights/bNN_<topic>/delivery/W-NN", "the handoff an inputs version names")],
    "Questions": [(B, ""), ("└── reports/qNN_<topic>/", "a Block question's report (run-report-qNN)")],
    "Cost": [(B, ""), ("└── " + J, "one card"), ("    ├── runs/*/run.yaml", "started_at · finished_at · ? usage: tokens"),
             ("    └── tNN_*/runs/*/run.yaml", "each Task's Runs: t00 · designs · t99")],
    "Predicted": [(B, ""), ("├── " + J, "predicted"), ("│   ├── runs/run-freeze-predictions-jNN/", "✎ 261007  the Job's Run, listed here (s12)"),
                  ("│   └── tNN_d<NN>_<slug>/prediction.yaml", "frozen at release: +x [lo, hi], by whom, date"),
                  ("├── observed/", "✎ 261007  what the Exp returned (the twin of inputs/)"),
                  ("│   └── e01_<exp>/", "one Exp, filled by run-add-observed-e01, frozen"),
                  ("│       ├── arms.csv", "arm · jNN · dNN · n · outcome totals; per arm only"),
                  ("│       ├── source.md -> …/W-NN", "the handoff (or the vendor report) it came from"),
                  ("│       └── manifest.yaml", "each file's sha256; frozen"),
                  ("├── runs/run-score-e01/scores.csv", "soft, once per Exp: each arm's design scored"),
                  ("└── reports/qNN_<topic>/", "the comparison, written"),
                  ("$RESULT_STORE/… (the Exp's rows)", "never here: an insight Block reads them")],
    "Scorecard": [(B, ""), ("└── runs/run-score-e01/scores.csv", "per design: direction · in range · error; summed per method version"),
                  ("haipipe-design-unit/methods/", "where its proposals go")],
    "Work": [(B, ""), ("└── " + J, "a card: one Job (s12)"), ("    ├── jNN_<goal>_<design-method>.md", "its pins and state"),
             ("    ├── t00_reason-ideas/", "the ideas"), ("    ├── tNN_d<NN>_<slug>/", "one design each"),
             ("    └── t99_review-whole/", "the ranking, the kept N")],
    "Studio": [(B, ""), ("└── studio/sNN-<topic>/", "a drawing and its builder")],
    "Runs": [(B, ""), ("├── runs/run-<type>-<target>/", "soft, every one: the Block's own Runs"), ("├── board.md", "## Questions, from run-propose-questions"),
             ("└── " + J + "runs/", "the Jobs' Runs (s12)")],
    "Delivery": [(B, ""), ("├── delivery/", "every released design, every Job"), ("│   ├── designs.json · designs.md", "the words, by run-release-jNN"),
                 ("│   └── screens/", "how each reads (render_screen.py)"),
                 ("└── " + J + "delivery/", "a Job's kept designs, before release (s12)")],
}
DISK = {k: v + [TREE] for k, v in DISK.items()}

# "skills" to the right of "on disk": the skills behind each screen, a tree from skills/ (JL 261007: "in the right
# we will have skills … so we understand what skills will be used here"); "?" = proposed, not in the skill yet
SK = ("✎ 261007  the skills behind this screen, from skills/", "")
SKILLS = {   # each root is a full path from skills/, so its children stay one level deep and short
    "Map": [("skills/2_theme/design/", ""), ("├── haipipe-design/", "owns the Block, its Jobs"),
            ("│   └── scripts/", "design_ladder.py: a Job"), ("└── workbench-design/", "draws the Map")],
    "Goals": [("skills/2_theme/design/", ""), ("├── …-design-goal/", "writes the goal list"),
              ("├── …-design-brief/", "retires: merged in"), ("└── venue/venue-sms/", "the venue a goal names")],
    "Methods": [("skills/2_theme/design/", ""), ("└── …-design-unit/", "runs a method's steps"),
                ("    └── ? methods/", "? the registry M01 … M05"), ("        └── ? M04-….md", "? one registered method")],
    "Inputs": [("skills/2_theme/design/", ""), ("├── haipipe-design/", "freezes inputs/iN"), ("└── …-design-goal/", "the shared rules"),
               ("skills/2_theme/insight/", ""), ("└── haipipe-insight/", "signs the handoff W-NN")],
    "Questions": [("skills/1_base/question/", ""), ("├── haipipe-question/", "a question, its report"), ("└── …-question-asking/", "shapes a new question"),
                  ("skills/1_base/page/", ""), ("└── haipipe-page/", "writes the report Page")],
    "Cost": [("skills/1_base/project/", ""), ("└── haipipe-run/", "the receipt: time"), ("    └── ? usage:", "? tokens in · out, to do"),
             ("skills/2_theme/design/", ""), ("└── workbench-design/", "sums it per Job")],
    "Predicted": [("skills/2_theme/design/", ""), ("├── …-design-unit/", "④ ⑤ reviewer predicts"), ("└── ? …-design-workflow/", "? add-observed · score"),
                  ("skills/2_theme/insight/", ""), ("└── haipipe-insight/", "per-arm totals, signed")],
    "Scorecard": [("skills/2_theme/design/", ""), ("├── workbench-design/", "sums scores per method"), ("└── …-design-unit/", ""),
                  ("    └── ? methods/", "? takes the proposals")],
    "Work": [("skills/2_theme/design/", ""), ("├── haipipe-design/", "the Jobs, their Tasks"), ("├── …-design-workflow/", "each Job's Runs"),
             ("└── …-design-unit/", "t00 · designs · t99")],
    "Studio": [("skills/1_base/page/", ""), ("└── workbench-studio/", "a drawing and its chat")],
    "Runs": [("skills/1_base/project/", ""), ("└── haipipe-run/", "a soft Run, its receipt"), ("skills/2_theme/design/", ""), ("└── …-design-workflow/", ""),
             ("    └── ? run-cards.md", "? the Block's Run cards")],
    "Delivery": [("skills/2_theme/design/", ""), ("├── ? …-design-delivery/", "? the hand-off (s12)"),
                 ("│   └── ? ref/", "? designs-schema.md"), ("├── haipipe-design/", "the Jobs it gathers"),
                 ("└── venue/venue-sms/", "how a design reads")],
}
SKILLS = {k: v + [SK] for k, v in SKILLS.items()}

SCREENS = [
    ("Description", DESC(0), ["run-add-job-<jNN>"], "", block_map, DISK["Map"], SKILLS["Map"]),
    ("Description", DESC(1), ["run-add-goal-<goal>"], "", goals, DISK["Goals"], SKILLS["Goals"]),
    ("Description", DESC(2), ["run-propose-method-<slug>"], "", methods, DISK["Methods"], SKILLS["Methods"]),
    ("Description", DESC(3), ["run-add-inputs-<iN>"], "", inputs, DISK["Inputs"], SKILLS["Inputs"]),
    ("Audience Report", AR(0), ["run-propose-questions", "run-report-<qNN>"], "", questions, DISK["Questions"], SKILLS["Questions"]),
    ("Audience Report", AR(1), [], "", cost, DISK["Cost"], SKILLS["Cost"]),
    ("Audience Report", AR(2), ["run-add-observed-<eNN>", "run-score-<eNN>"], "", predicted, DISK["Predicted"], SKILLS["Predicted"]),
    ("Audience Report", AR(3), [], "", scorecard, DISK["Scorecard"], SKILLS["Scorecard"]),
    ("Work Details", [("All", 1), ("G01", 0), ("G02", 0)], ["run-add-job-<jNN>"], "", work, DISK["Work"], SKILLS["Work"]),
    ("Idea Studio", None, ["run-draw-<sNN>"], "", studio, DISK["Studio"], SKILLS["Studio"]),
    ("Runs", [("All", 1), ("Set up", 0), ("Launch a Job", 0), ("Report", 0)], ["run-add-goal-<goal>", "run-add-job-<jNN>", "run-propose-questions"], "", runs, DISK["Runs"], SKILLS["Runs"]),
    ("Delivery", None, ["? run-plan-test-<app>"], "", delivery, DISK["Delivery"], SKILLS["Delivery"]),
]

POPOUTS = [U.card_window("By insight"),
           ("j02 → j03  ·  two Jobs in one Map cell", [("what moved", INK), ("  the method, m1 → m2: ② spread · ⑤ top N of N + 5; inputs i2 held", GRAY),
                                                      ("what it changed", INK), ("  passed 6 → 8 of 10 · <n>k → <n>k tok per passed · near pairs 3 → 1", GRAY),
                                                      ("read from", INK), ("  each Job's pins and its Performance (s12)", GRAY)]),
           ("j03 · the Job  ·  one cell of the Map", [("pins", INK), ("  G01 · M04 m2 (sha) · inputs i2", GRAY),
                                                    ("state", INK), ("  released ✅ · 10 kept of 15", GRAY),
                                                    ("opens the Job tab (s12)", GRAY)])]

# each question sits under the screen it decides (JL 261007); decided ones are green "✎" notes with the reason
# (JL 261007: "have your own judgements"), only what still needs another owner stays red
D = "✎ 261007 decided: "
QUESTIONS = [
    ("Description", "Map", D + "the Map's columns and the Methods cards name registered methods (M01 … M05), each with "
                           "its type; the Job folder already names one (s12), and two methods of one type must still compare"),
    ("Description", "Methods", D + "the registry lives in the design skill (haipipe-design-unit/methods/): a method is a "
                               "generic recipe, the app's part comes through inputs/; an app's own variant is a new M, not a copy"),
    ("Description", "Methods", D + "M02 is By precedent (it reads how past messages did), M03 and M05 By insight (they read "
                               "our evidence, M05 from raw data)"),
    ("Description", "Goals", D + "the Brief merges into the goal list and haipipe-design-brief retires: one place for a "
                             "goal's aim, who, venue, N and its own rules"),
    ("Description", "Goals", D + "a goal is signed once, here; a Job's run-setup-goal-jNN only pins it (s12 agrees)"),
    ("Description", "Inputs", D + "inputs are versioned i1, i2 …; a new handoff or new rules make a new version; a Job "
                              "fences one in its inputs/, so a change has one cause"),
    ("Audience Report", "Predicted vs observed", D + "another agent predicts: the ④ ⑤ reviewer, which already ranks by "
                                                 "predicted outcome at t99 (s12); the scorecard scores it, so it can be replaced"),
    ("Audience Report", "Predicted vs observed", D + "what the Exp returns lands once, in the Block's observed/eNN_<exp>/: "
                                                 "per-arm totals, each arm naming jNN · dNN; one Exp spans Jobs, so not a copy per Job"),
    ("Audience Report", "Predicted vs observed", D + "one soft Run per Exp, run-score-<eNN>, scores every arm's design (arithmetic on two small files); "
                                                 "Job › Predicted vs observed (s12) shows its own rows, the scorecard sums them"),
    ("Audience Report", "Predicted vs observed", D + "observed/ takes per-arm totals from an insight Block's signed handoff, "
                                                 "or a vendor's own per-arm report; raw Exp data stays in its store (it is analysis, and PHI)"),
    ("Audience Report", "Cost", D + "every Run's receipt gets usage: (tokens in · out); without it Cost and the scorecard "
                                "have no tokens"),
    ("Audience Report", "Cost", "? to do, outside b12: the Run skill's owner adds usage: to the receipt"),
    ("Description", "Map", D + "no Versions view: the Map's cell already is the chain, and the scorecard compares method "
                           "versions; two Jobs picked in a cell open what moved between them"),
    ("Delivery", "", D + "the test is planned outside the theme, with the Exp; Delivery hands the released designs over "
                     "(designs.json) and the result returns into observed/"),
]

ASIDES = {"Idea Studio": ("typical topics, bNN_<app>/studio/sNN-<topic>/", [
    ("s01-<goal map>", "the goals and which methods suit each"),
    ("s02-<method comparison>", "two methods on one goal, side by side"),
    ("? s03-<what the Exp said>", "the result back, before the next inputs")])}


CHANGES = ["261007  the method proposal is run-propose-method-<slug>, as every Run is run-<type>-<target> (was run-propose-<method>)",
           "261007  Runs panel entries are folding cards named run-<type>-<target>; every Block Run is soft (JL)",
           "261007  predictions freeze at the Job (run-freeze-predictions-jNN, s12); the Block lists them",
           "261007  run-add-job-<jNN> makes an empty Job; the Job's own setup Runs (goal · method · inputs) set it up (s12)",
           "261007  every list is a card, as the Job's (s12: JL \"change it to cards\"); every screen's on disk is a tree from bNN_<app>/",
           "261007  no methods Block (JL): Methods reads the registered methods from the design skill; the Map's columns are M01 … M05",
           "261007  Inputs: each version's parts labelled as step ①'s parts, as the Job's",
           "261007  Work Details: a Job card opens to a preview of its Tasks: t00 · each design as it reads · t99 (s12)",
           "261007  Predicted vs observed and Delivery show each design as it reads (a phone), as the Job's Design display",
           "261007  decided here, not left open (JL: \"have your own judgements\"): each decision a green note under its screen",
           "261007  observed/eNN_<exp>/ holds what the Exp returned (per-arm totals), the twin of a Job's inputs/",
           "261007  run-propose-questions: proposes the Block's report questions from the Map, the scores and the scorecard",
           "261007  skills beside on disk: the skills behind each screen, a tree from skills/ (JL)",
           "261007  Questions: each a Question │ Task Work │ Report row, the workbench's style (JL)",
           "261007  no Versions view (JL: its purpose unclear): two Jobs in a Map cell open what moved between them",
           "261007  observed/ and its scoring sit at the Block, once per Exp (an Exp spans Jobs); a Job's view reads its own arms"]


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s11-design-block.excalidraw"
    U.level_drawing(out, Path(__file__).name, "Block",
                    "Block level: one application, one channel (bNN_<app>)",
                    "Goals and inputs here; each Job pins a goal, a registered method version and an inputs version.",
                    MOVES, SCREENS, POPOUTS, QUESTIONS, ASIDES, changes=CHANGES)


if __name__ == "__main__":
    main()
