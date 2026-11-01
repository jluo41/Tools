"""s61 · Insight slides: the deck's content, in one place.

The drawing (build_s61_insight_slides.py) and the deck (build_deck.py) both read this file, so the logic
flow, the storyboard and the slides never drift apart. Edit the deck here, then rebuild both. The shape is
b12's s61-design-slides (same keys, same slide layout), so the two theme decks read as one pair.

Each slide: its number and slug, its title (the claim it makes), the bullets (one sentence each), its
picture (a kind and its data, drawn by b12's slide_kit.py), the drawings it is drawn from, the words that
lead to the next slide, its group in the argument, and speaker notes.

Placeholders only (<topic>, <d>v1, <A>, K01, j03); the worked example is illustrative, with no data. The
published numbers on slide 2 are from the Insight Guide (workbench-insight guide/method.md § 5).
"""

THESIS = ("An insight Job changes one thing at a time, so when an answer changes we can say why; and a claim "
          "leaves the Board only once it has earned it.")

GROUPS = [("why", "the pain, and its evidence"), ("what", "the idea and the ladder"),
          ("how", "one Job, kept honest"), ("learn", "what it catches, how it grows"),
          ("now", "where you see it, its limits, the bet")]

SLIDES = [
    dict(n=1, slug="cover", group="why",
         title="The insight theme on the ladder",
         sub="Questions that evolve, on data that grows: how we ask, answer, check and hand on what the data says",
         foot="b11_theme_insight · s61-insight-slides",
         src="s00", lead="start from the evidence",
         notes=THESIS),

    dict(n=2, slug="evidence", group="why",
         title="Analysis is cheap now; a reason to trust it is not",
         bullets=["An agent runs a hundred analyses in the time a person checks one.",
                  "Each way an analysis fools itself has been measured, and none is rare."],
         picture=("grid", dict(head=["failure", "what was measured"], rows=[
             ["Forking paths", "29 teams, one dataset and question: odds ratios from 0.89 to 2.93 (Silberzahn 2018)"],
             ["Subgroup claims", "46 of 117 tested the difference; none of 5 attempts to confirm one did (Wallach 2017)"],
             ["No replication", "97% of 100 studies significant; 36% of their replications (Open Science 2015)"],
             ["Self-checking", "a language model rates its own output above others' (Panickssery 2024)"]],
             note="Each failure has a known remedy; the design puts every remedy on the path of every question.")),
         src="Guide method.md § 5", lead="and today's boards add one more",
         notes="Speed is no longer scarce. Also: over 60% of insights reported in visual exploration of data with a "
               "known truth were false (Zgraggen 2018); the best agents solve a quarter to a third of "
               "data-analysis benchmark tasks (Majumder 2024; Chen 2024)."),

    dict(n=3, slug="why", group="why",
         title="Today we cannot say why an answer changed",
         bullets=["A register board holds one extract, its partitions and the questions, edited in place.",
                  "A new extract, a fixed script and a new question tend to land in the same week.",
                  "When an answer moves, nobody can name the one cause."],
         picture=("cards", dict(arrow=True, cards=[
             ("Today", ["insights/<Dataset>-InsightBoard/: one extract",
                        "questions and their code edited in place",
                        "a new extract: a new board, or an overwrite"]),
             ("On the ladder", ["a Prototype Block: the questions and their code, released p1, p2",
                                "an insight Board: the data versions, a Job per pair",
                                "a Job pins one release and one data version"])])),
         src="s00 · s01", lead="so: version both, separately",
         notes="Name the pain before the fix: not a wrong answer, an unexplainable change."),

    dict(n=4, slug="two-clocks", group="what",
         title="Two things change, on two clocks: the questions and the data",
         bullets=["The questions change when we learn; the data changes when it arrives.",
                  "A Job pins one of each, by path and hash, and is frozen when it closes."],
         picture=("cards", dict(cards=[
             ("Prototype", ["the questions, their scripts, the cuts and the compare rule",
                            "released p1 → p2 → p3; a person signs each",
                            "lives in work/bNN_<topic>_prototype/"]),
             ("Dataset", ["extracts by date, outside the Project",
                          "versions <d>v1 → <d>v2 build up",
                          "a new one needs no release"]),
             ("Job", ["one release × one data version",
                      "j03_p2_<d>v2 in insights/bNN_<topic>/",
                      "frozen when closed; a change is a new Job"])])),
         src="s00", lead="laid on a grid",
         notes="This is the core move. Everything after it follows from pinning the two clocks."),

    dict(n=5, slug="one-clock", group="what",
         title="One change per Job, so every changed answer has one cause",
         bullets=["Each step to the next Job moves the data or the code, never both.",
                  "Backfill (new code on old data) is one more cell, not a special case."],
         picture=("grid", dict(head=["", "<d>v1", "<d>v2", "<d>v3"], rows=[
             ["p1", "j01 · start", "j02 · data moved", "—"],
             ["p2", "+ backfill p2 × <d>v1", "j03 · code moved", "j04 · data moved"],
             ["p3", "—", "—", "+ the next release"]],
             note="The Board's Map: data versions as columns, releases as rows. Jobs two clocks apart are never "
                  "compared.")),
         src="s00 · s11", lead="the levels that hold it",
         notes="Read a row as one release meeting new data; a column as one data version meeting new questions."),

    dict(n=6, slug="ladder", group="what",
         title="Four levels: Board, Job, Task, Run",
         bullets=["Every theme has these four levels; what each holds is insight's own."],
         picture=("ladder", dict(rows=[
             ("Board", "insights/bNN_<topic>/", "one dataset, its versions, the Map, and reports across Jobs"),
             ("Job", "j03_p2_<d>v2/", "one release × one data version; its questions grouped by D · I · K · W"),
             ("Task", "t04_K01_<q>/", "one question on this pair, at its DIKW level, with its page"),
             ("Run", "runs/r02_<A>/ · run-<type>-<target>/",
              "hard: one partition's result/ · soft: write, check, compare, propose")])),
         src="s11 · s12 · s13", lead="what a level may claim",
         notes="The Prototype Block beside the Board has the same four levels: a release is its Job, a question "
               "its Task."),

    dict(n=7, slug="dikw", group="what",
         title="Each DIKW level may say more, and has one thing it may not say",
         bullets=["A question's level is set when it is asked, before the data, so a weak result cannot be promoted."],
         picture=("grid", dict(head=["level", "may say", "may not say", "must show"], rows=[
             ["D · Data", "counts, what was seen", "any comparison", "n, coverage, missingness"],
             ["I · Information", "rates, contrasts, segments", "\"because\"", "one test for each contrast"],
             ["K · Knowledge", "one claim, how sure, its rivals", "advice", "rivals ruled out; replicates (T8)"],
             ["W · Wisdom", "advice for Design", "new evidence", "the K claims it rests on; a signature"]])),
         src="s03 · s11 – s13", lead="how a question is made",
         notes="Claim discipline: each level must cite the one below it."),

    dict(n=8, slug="question", group="how",
         title="A question is planned, agreed and signed before any data is read",
         bullets=["The ask, the plan, the cuts, the power floors and the compare rule are fixed in a release.",
                  "A different agent agrees the plan (T0 – T3), and a person signs the release."],
         picture=("flow", dict(nodes=[
             ("ask", "a person signs it", "in"),
             ("plan", "T0 covered · T1 specified"),
             ("agree", "another agent · T2 · T3 powered"),
             ("script", "the code that answers it"),
             ("review", "another agent"),
             ("release p2", "signed; used by path and hash", "out")])),
         src="s00 · Guide method.md", lead="then a Job runs it",
         notes="Plan first works: once outcomes had to be registered, trials showing a benefit fell from 17 of 30 to "
               "2 of 25 (Kaplan & Irvin 2015)."),

    dict(n=9, slug="one-job", group="how",
         title="Inside one Job: power first, then run, check, compare and propose",
         bullets=["Power is checked before any outcome is read, so a weak cut is refused and shown, never run.",
                  "Each partition is its own hard Run; Cross runs one test of the difference.",
                  "Compare and propose come after the checks, so a proposal rests on checked answers."],
         picture=("flow", dict(nodes=[
             ("launch", "pins · one Task per question", "in"),
             ("power", "n per cut; refuse"),
             ("rNN_<cut>", "hard · result/"),
             ("rNN_cross", "POOL or SPLIT"),
             ("write · check", "the page · T4 – T7"),
             ("compare", "vs the previous Job"),
             ("close", "frozen", "out")])),
         src="s12 · s13", lead="what keeps it honest",
         notes="Run order: Add a Job (Board) → run-launch → run-power → rNN_<partition> → rNN_cross → run-write → "
               "run-check → run-compare-<prev> → run-propose-<job> → run-close."),

    dict(n=10, slug="guardrails", group="how",
         title="Four guardrails keep the answers honest",
         bullets=["None of them relies on the maker checking its own work."],
         picture=("cards", dict(cards=[
             ("Plan first", ["the release is fixed before outcomes",
                             "T0 – T3 gate the plan"]),
             ("Planned cuts", ["filters and power floors live in the release",
                               "a weak cut is refused and shown",
                               "Cross tests the difference"]),
             ("Another agent checks", ["T4 – T7 by an agent that did not write it",
                                       "T5: each sentence says what its result says"]),
             ("A person signs", ["the release before the data",
                                 "the handoff after it",
                                 "nothing else leaves the Board"])])),
         src="s00 · s12 · Guide method.md", lead="across Jobs",
         notes="T4 to T6 ask whether it was done right; only T7 (robustness) and T8 (replication) ask whether it "
               "is true."),

    dict(n=11, slug="compare", group="learn",
         title="Every answer gets a status against the previous Job",
         bullets=["The rule for \"held\" is fixed in the release before any outcome, not by whoever reads the result."],
         picture=("grid", dict(head=["status", "means"], rows=[
             ["new question", "first asked in this release: not yet a finding"],
             ["new finding", "a question asked before now has an answer"],
             ["held", "the release's rule says it is the same"],
             ["changed", "it moved beyond the rule, and the moved clock is its cause"],
             ["dropped · not comparable", "answered before and not now · the question itself changed"]],
             note="Held: D counts within a tolerance; I the same direction; K the same sign and size; W its ground "
                  "holds.")),
         src="s12", lead="what that catches",
         notes="Written by the Job's soft Run run-compare-<prev> into reports/vs-<prev>.md; the Audience Report's "
               "vs previous reads only that file."),

    dict(n=12, slug="example", group="learn",
         title="One question, four Jobs: what a naive pipeline would have shipped",
         bullets=["K01 asks whether <arm X> beats <arm Y> on <outcome>, split by <A> and <B>.",
                  "Illustrative only: placeholders, no data."],
         picture=("grid", dict(head=["Job", "moved", "<A> vs <B>", "a naive pipeline", "this design"], rows=[
             ["j01 p1 × v1", "start", "SPLIT: larger in <A>", "ships \"works better in <A>\"", "a K claim: W waits for T8"],
             ["j02 p1 × v2", "data", "POOL", "the effect \"disappears\"", "changed; cause: data"],
             ["j03 p2 × v2", "code", "<B> below power", "old and new mixed", "<B> refused, and shown"],
             ["j04 p2 × v3", "data", "POOL", "—", "held: the split was noise"]])),
         src="s00 · s12", lead="how the questions grow",
         notes="The design does not make answers right; it makes changes attributable and claims proportionate."),

    dict(n=13, slug="learning-loop", group="learn",
         title="Comparing Jobs is how the questions grow",
         bullets=["Gaps and changed answers become proposals; proposals become the next release.",
                  "A question added after seeing the data stays exploratory until the next data version confirms it."],
         picture=("flow", dict(loop="the new Job is compared with this one in turn", nodes=[
             ("Job closes", "frozen"),
             ("compare", "new · held · changed"),
             ("propose", "→ proposals/"),
             ("next release", "asked, agreed, signed"),
             ("new Job", "pN+1 × <d>vM")])),
         src="s00 · s12", lead="one level up",
         notes="A release is also opened when a level is answered (D raises I questions), a check fails, an answer "
               "is weak, a new data field arrives, someone asks, or a paper suggests it."),

    dict(n=14, slug="across-jobs", group="learn",
         title="The Board reads across Jobs: a second D · I · K · W",
         bullets=["Readings use the Jobs' results, never raw data, and compare only Jobs one clock apart."],
         picture=("grid", dict(head=["reading", "asks", "soft Run"], rows=[
             ["Coverage", "what was asked and answered, on which Job", "run-coverage"],
             ["Tracks", "one question Job by Job; a trend over data versions", "run-track-<q>"],
             ["Consistency", "each step held or changed, and its one cause", "run-consistency-<jA>-<jB>"],
             ["Findings", "the Board's own questions, each citing a reading", "run-report-<qNN>"]])),
         src="s11", lead="where it goes",
         notes="The Board's reports/qNN_<topic>/ are these second-order questions: about the answers, not the data."),

    dict(n=15, slug="handoff", group="now",
         title="Only signed Wisdom leaves, and it steers design",
         bullets=["D, I and K hand their answers up, not out.",
                  "A signed Wisdom counsel names its Job, and enters the design Block as a new inputs version."],
         picture=("flow", dict(nodes=[
             ("D · I · K", "answers, cited", "in"),
             ("W counsel", "a person signs"),
             ("Handoff", "W-NN · names pN × vM"),
             ("Design inputs", "a new version iN"),
             ("A design Job", "each element: from = W-NN", "out")])),
         src="s11 · s12 · b12 s61", lead="where you see it",
         notes="This is the same crossing b12's deck draws from the design side."),

    dict(n=16, slug="workbench", group="now",
         title="One workbench: the same six Spaces at every level",
         bullets=["Board, Job and Task each show the same six Spaces; what a Space holds follows the level."],
         picture=("grid", dict(head=["Space", "Board", "Job", "Task"], rows=[
             ["Description", "Map · Prototype · Dataset · Partitions", "the release and the data version",
              "Question · Plan · Data"],
             ["Audience Report", "Coverage · Tracks · Consistency · Findings", "Question │ Work │ Report",
              "need → Run → sentence"],
             ["Work Details", "the Jobs, their quick results", "Job › Task › Run", "Task › Run"],
             ["Runs", "add a version or a Job · readings", "launch … compare · propose", "rNN · cross · write · check"],
             ["Delivery", "the signed handoff", "its counsel, to the Board", "W only"]])),
         src="s11 · s12 · s13", lead="what it does not do",
         notes="Partition × Period filters every Audience Report: Full · <A> · <B> · Cross, and Current · vs "
               "previous. Every cell opens the Run behind it."),

    dict(n=17, slug="limits", group="now",
         title="What it guarantees, and what it does not",
         bullets=["It narrows how an analysis can go wrong; it does not replace judgment about what to ask."],
         picture=("cards", dict(cards=[
             ("It guarantees", ["every sentence traces to a Run and a release",
                                "each change between Jobs has one cause",
                                "tests and cuts were fixed before outcomes",
                                "a person signed what left"]),
             ("It does not guarantee", ["that the question was worth asking",
                                        "causal validity beyond what the data supports",
                                        "power in small data (it refuses instead)",
                                        "that the signer read carefully"]),
             ("It costs", ["a Run per partition, plus cross, write, check",
                           "a review and a signature per release",
                           "coverage: refused cuts"])])),
         src="s00 · s12", lead="so is it worth it?",
         notes="Mitigations proposed: reuse unchanged Runs by hash; batch proposals into one release."),

    dict(n=18, slug="bet", group="now",
         title="The design is itself a bet, and we can measure it",
         bullets=["Planned, agreed, powered questions should replicate on the next extract more often than ad hoc ones.",
                  "No study compares these methods head to head on one question; this would be the first."],
         picture=("grid", dict(head=["measure", "definition", "read against"], rows=[
             ["Replication (T8)", "K answers held on the next data version", "an agent's ad hoc analysis"],
             ["Attributed changes", "changed answers with one moved clock", "100% by construction"],
             ["Refusals", "planned cuts refused for power", "the coverage we give up"],
             ["Time per Job", "launch to close", "the latency we pay"]])),
         src="Guide method.md", lead="where it stands",
         notes="From the Insight Guide: the workbench is itself a bet."),

    dict(n=19, slug="status", group="now",
         title="Where it stands",
         bullets=["Next: real Boards on the ladder, then the older register boards carry over."],
         picture=("cards", dict(cards=[
             ("Done", ["the design: structure (s00), Board · Job · Task screens (s11 – s13), the Guide (s31)",
                       "the workbench draws all three levels from a placeholder Board; 17 tests pass"]),
             ("In progress", ["the run types and skills by level (s21)",
                              "the first Board with a Prototype and data versions on disk"]),
             ("Open", ["one Prototype per Board, or shared?",
                       "when a release is cut",
                       "does a signed handoff go stale?"])])),
         src="s00 · s11 – s13 · s31", lead=None,
         notes="Status as of 2026-10-07; rebuild the deck before each showing so this slide stays true."),
]
