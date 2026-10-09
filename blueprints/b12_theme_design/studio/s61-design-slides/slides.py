"""s61 · Design slides: the deck's content, in one place.

The drawing (build_s61_design_slides.py) and the deck (build_deck.py) both read this file, so the logic
flow, the storyboard and the slides never drift apart. Edit the deck here, then rebuild both.

Each slide: its number and slug, its title (the claim it makes), the bullets (one sentence each), its
picture (a kind and its data, drawn by slide_kit.py), the drawings in this Block it is drawn from, the
words that lead to the next slide, its group in the argument, and speaker notes.

Placeholders only (<app>, <goal>, G01, M04, j03): no project content, no data values.
"""

GROUPS = [("why", "the pain"), ("what", "the idea and the ladder"), ("how", "one Job, kept honest"),
          ("learn", "the loops that improve it"), ("now", "where you see it, where it stands")]

SLIDES = [
    dict(n=1, slug="cover", group="why",
         title="The design theme on the ladder",
         sub="N designs for one goal, by one method: how we make them, check them and learn from them",
         foot="b12_theme_design · s61-design-slides",
         src="s01", lead="start from the pain",
         notes="One idea runs through the deck: a design Job changes one thing at a time, so when the designs "
               "change we can say why, and the Exp can teach the method, not only the designs."),

    dict(n=2, slug="why", group="why",
         title="Today we cannot say why a design changed",
         bullets=["Design work sits in stage folders: a brief, the principles, then one Design folder per method.",
                  "A method folder holds every goal, so the goal, the method and the inputs change together.",
                  "When a new batch of designs reads differently, nobody can name the one cause."],
         picture=("cards", dict(arrow=True, cards=[
             ("Today", ["0-BR-brief/ · 1-P-principle/ · 2-Design-M<NN>/",
                        "a method folder holds every goal",
                        "Runs: commission · generate · verify"]),
             ("On the ladder", ["Block → Job → Task → Run",
                                "a Job pins one goal, one method version, one inputs version",
                                "every Run is named run-<type>-<target>"])])),
         src="s01 · s21", lead="so: make the method the unit",
         notes="Name the pain before the fix: several things move at once, so a better or worse design has "
               "no single cause, and nothing we learn sticks to a method."),

    dict(n=3, slug="method", group="what",
         title="A design method is a frozen recipe: a goal and inputs in, N designs out",
         bullets=["Each method version is frozen, so two Jobs on the same version are comparable.",
                  "It runs in five steps, and checking a design is always another agent's work.",
                  "Thirteen method cards in three families say where the rule comes from: the goal alone, "
                  "research, or our own data."],
         picture=("flow", dict(nodes=[
             ("goal + inputs", "the Job's fence", "in"),
             ("1 See input", "what the method reads"),
             ("2 Reason ideas", "15 ideas, each named"),
             ("3 Conduct", "one design per idea"),
             ("4 Check each", "T0 rules · T1 sources · T2 critique · T3 pretest"),
             ("5 Check whole", "rank, keep N"),
             ("N designs", "to a person", "out")])),
         src="s03 · s00", lead="where it lives",
         notes="The method is the thing we want to improve, so it is versioned and frozen like code. The three "
               "families: Goal Only (no rule yet), External Insights (a rule from research), Internal "
               "Insights (a rule from our data)."),

    dict(n=4, slug="ladder", group="what",
         title="Four levels: Block, Job, Task, Run",
         bullets=["A Block is one application and one channel: its goals, its inputs versions and what the Exps "
                  "returned.",
                  "A Job is one goal done by one method version on one inputs version, returning N designs.",
                  "A Task is one step of the method, and a Run is one piece of work inside it."],
         picture=("ladder", dict(rows=[
             ("Block", "bNN_<app>/", "one application, one channel: goals · inputs i1, i2 · observed e01"),
             ("Job", "jNN_<goal>_<design-method>/", "one goal × one method version × one inputs version → N designs"),
             ("Task", "t00_reason-ideas/ · tNN_d<NN>_<slug>/ · t99_review-whole/",
              "one method step: reason ideas · one design · review the whole set"),
             ("Run", "runs/run-<type>-<target>/", "hard: an agent writes a result · soft: a set-up or a sign-off")])),
         src="s01 · s11 · s12 · s13", lead="why a Job pins three things",
         notes="Every design theme Board has the same four levels as every other theme; only what each level "
               "holds is the design theme's own."),

    dict(n=5, slug="one-clock", group="what",
         title="One change per Job, so every difference has one cause",
         bullets=["A new goal, a new method version or a new inputs version each starts a new Job.",
                  "To compare two methods, run sibling Jobs on the same goal and the same inputs.",
                  "The Block's Map lays goals against methods, and each cell holds its chain of Jobs."],
         picture=("grid", dict(head=["", "M01 by goal", "M03 by insight", "M04 by insight"], rows=[
             ["G01 <goal>", "j01 · i1", "j02 · i1  →  j05 · i2", "j03 · m2 · i2"],
             ["G02 <goal>", "—", "j04 · i1", "j06 · m2 · i1"],
             ["G03 <goal>", "j07 · i2", "—", "—"]],
             note="A row is one goal's history: each → is a new Job that changed one thing. "
                  "A column is one method across goals.")),
         src="s00 · s11", lead="inside one Job",
         notes="Read a row as a goal's history: each arrow is one Job to the next, and it changed exactly one "
               "thing. Read a column as one method across goals. Two Jobs in a cell can be opened side by side."),

    dict(n=6, slug="one-job", group="how",
         title="Inside one Job: set up, reason, make, check, rank, release",
         bullets=["Three set-up Runs pin the goal, the method version and the inputs.",
                  "t00 reasons out 15 ideas, and each idea becomes its own design Task.",
                  "Each design is generated, verified by another agent, and revised until it passes.",
                  "t99 ranks the 15, keeps 10 with a prediction each, and a person releases them."],
         picture=("flow", dict(nodes=[
             ("Set up ×3", "goal · method · inputs", "in"),
             ("t00 Reason", "15 ideas"),
             ("t01 – t15 Make", "generate → verify → revise"),
             ("t99 Rank", "keep 10, predict each"),
             ("Release", "a person signs"),
             ("Delivery", "the designs, word for word", "out")])),
         src="s12 · s13", lead="what keeps it honest",
         notes="Every method step is a Task: one for reasoning, one per design, one for the whole set. A "
               "revision is another Run in the same design Task, never a new Task."),

    dict(n=7, slug="guardrails", group="how",
         title="Four guardrails keep the designs honest",
         bullets=["None of them relies on the maker checking its own work."],
         picture=("cards", dict(cards=[
             ("Inputs fence", ["The Job sees only its inputs/ folder.",
                               "A manifest pins each file by its hash.",
                               "Each reasoning step cites a file, or says own knowledge."]),
             ("Another agent checks", ["Verify and rank run in a separate reviewer agent.",
                                       "A failed check sends the design back to revise."]),
             ("A person decides", ["A person signs each goal once, at the Block.",
                                   "A person releases the designs; nothing ships on its own."]),
             ("Predictions frozen", ["Each kept design carries a predicted effect.",
                                     "It is frozen at release, before the Exp runs."])])),
         src="s12 · s13", lead="after release",
         notes="The fence makes a design traceable; the second agent makes the check independent; the person "
               "owns the goal and the release; the frozen prediction makes the Exp a real test."),

    dict(n=8, slug="learning-loop", group="learn",
         title="The Exp teaches the method, not only the designs",
         bullets=["The Exp runs outside the theme, and only per-arm totals come back, never rows.",
                  "Each released design's frozen prediction is scored against its arm.",
                  "Scores add up to a scorecard per method version, and its weak spots become proposals for "
                  "the next version."],
         picture=("flow", dict(loop="the next Job runs on the new version", nodes=[
             ("Release", "designs + predictions"),
             ("Exp", "outside the theme"),
             ("Arm totals", "in observed/eNN/"),
             ("Score", "run-score-eNN"),
             ("Scorecard", "per method version"),
             ("New version", "from the proposals")])),
         src="s11 · s00", lead="where the rule can come from",
         notes="This is the Learning loop. A method version is never edited after it closes: a better idea "
               "becomes the next version, benched against the last on the same goals and inputs."),

    dict(n=9, slug="insight-steers", group="learn",
         title="Insight steers design through one handoff",
         bullets=["An insight Block's signed Wisdom answer is the only crossing between the two Blocks.",
                  "It enters the design Block as a new inputs version.",
                  "Jobs whose method reads our data use it, and each design element names where it came from."],
         picture=("flow", dict(nodes=[
             ("Insight Block", "a signed Wisdom answer", "in"),
             ("Handoff", "W-NN"),
             ("Design inputs", "a new version iN"),
             ("A Job", "by insight · tailoring · theory and insight"),
             ("Each element", "from = W-NN", "out")])),
         src="s01", lead="where you see it",
         notes="A newer handoff never makes a released design stale: it is a new inputs version, so it is a "
               "new Job. The insight side of this crossing is drawn in b11."),

    dict(n=10, slug="workbench", group="now",
         title="One workbench: the same six Spaces at every level",
         bullets=["Block, Job and Task each show the same six Spaces, and what a Space holds follows the level.",
                  "At the Task level, the Task's run types decide what each Space shows."],
         picture=("grid", dict(head=["Space", "Block", "Job", "Task"], rows=[
             ["Description", "Map · Goals · Methods · Inputs", "its goal, method and inputs", "what it reads and returns"],
             ["Audience Report", "Questions · Cost · Predicted vs observed", "Ideas · Designs · Ranking",
              "Tests · Drafts · Performance"],
             ["Work Details", "one card per Job", "t00 · t01 – t15 · t99", "Chains · Elements · Kept"],
             ["Runs", "set up · launch · report", "set up · reason · make · rank", "its own Runs"],
             ["Delivery", "every released design", "the kept designs", "what it hands on"],
             ["Idea Studio", "drawings", "drawings", "drawings"]])),
         src="s11 · s12 · s13 · s02", lead="where we are",
         notes="One UI with different content: the tab, the six Spaces and the Runs panel are the same at every "
               "level, so a reader who knows one level can read the others."),

    dict(n=11, slug="status", group="now",
         title="Where it stands",
         bullets=["Next: the workbench serves all three levels, then the older design Boards carry over."],
         picture=("cards", dict(cards=[
             ("Done", ["The skills carry the ladder: contract, inputs and methods, worker, Runs and release.",
                       "95 tests pass, and one Job runs end to end."]),
             ("In progress", ["The workbench screens for Block, Job and Task on the new ladder."]),
             ("Open", ["Token usage in each Run's receipt.",
                       "The Exp names the Job and design on each arm.",
                       "Carrying the older design Boards over."])])),
         src="s21", lead=None,
         notes="Status as of 2026-10-07; rebuild the deck before each showing so this slide stays true."),
]
