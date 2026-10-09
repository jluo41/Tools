Design ladder: the design theme's Block · Job · Task · Run
==========================================================

(JL 261007, designed in Tools/blueprints/b01_haipipe-toolkit/j12_theme_design: s00 the thinking, s11 Block, s12 Job, s13 Task, s21 Runs
and skills.) A design sits on the shared ladder: one Block per application and channel, one Job per goal done by one
registered method version on one inputs version, one Task per step of that method (t00 reason ideas, one Task per
design, t99 review whole), and the Runs that make and check them. Each level has the six Spaces of the base
workbench (Description · Idea Studio · Audience Report | Work Details | Runs · Delivery); the design workbench fills
them (servers/workbench-design: design_reader.py reads this tree, design_views.py draws it). `scripts/design_ladder.py`
makes each folder.

Read this reference when creating, naming or auditing a design folder. `haipipe-design` keeps only the routing in its
entrypoint; the goal, method, unit, workflow and delivery owners stay authoritative for their own records. An older
board (`B00_DesignBoard-<name>/` with `0-BR-brief/` and `2-Design[-M<NN>]/Design-NN-…/`) keeps its own workbench and
its own contract, [legacy/design-folder.md](legacy/design-folder.md), until it is carried over.


The tree
--------

```text
design/Design-<name>/                      Block: one application, one channel
├── board.md                                its face: board-kind: design-board · channel · spine · close
│                                           ## Goals (```yaml goals:) · ## Questions (```yaml questions:)
├── design-goal.md                          the shared rules every goal keeps: rules: r<k> · signed: (haipipe-design-goal)
├── inputs/iN/                              one inputs version: rules · theory · handoff copies, manifest.yaml (frozen)
├── observed/eNN_<exp>/                     what one Exp returned: arms.csv · source.md · manifest.yaml (frozen)
├── studio/sNN-<topic>/                     Idea Studio: drawings, one topic each
├── reports/qNN_<topic>/                    Audience Report: the Block's questions
├── runs/run-<type>-<target>/               every Block Run is soft: run.yaml · passes/
├── delivery/                               designs.json · designs.md · screens/<jNN>-<dNN>.<ext>: every Job's release
└── jNN_<goal>_<method>/                    Job: one goal × one method version × one inputs version → N designs
    ├── jNN_<goal>_<method>.md              its face (front matter): goal · method · method-sha · inputs · n ·
    │                                       state · moved
    ├── inputs/                             the fence: goal.md · method.md · links into ../inputs/iN/ ·
    │                                       manifest.yaml (each file, its source, its sha256 as its first 12 hex)
    ├── studio/ · reports/                  optional
    ├── runs/                               soft: run-setup-goal · run-setup-method · run-setup-inputs ·
    │                                       run-open-designs · run-freeze-predictions · run-release · run-close
    ├── delivery/                           designs.json · designs.md · screens/<dNN>.<ext>: the released, word for word
    ├── t00_reason-ideas/                   ② reason ideas, one per Job
    │   ├── t00_reason-ideas.md             state · step: ②
    │   └── runs/run-reason-t00/result/     hard: ideas.yaml · chains.yaml · topics.md
    ├── tNN_d<NN>_<slug>/                   ③ ④ one design, its short name born with its idea in t00
    │   ├── tNN_d<NN>_<slug>.md             state · name · idea · rank; ## Design · ## Evaluation
    │   ├── elements.yaml                   one entry per element: element · words · from · because · step · changed
    │   ├── prediction.yaml                 predicted · against · by · frozen (a draft until the release)
    │   └── runs/                           hard: run-generate-d<NN>/result/ (design.md · elements.yaml) ·
    │                                             run-verify-d<NN>-v<k>/result/ (review.md)
    │                                       soft: run-revise-d<NN>/passes/pNN-<MMDD>/ (one pass per new draft:
    │                                             design.md · elements.yaml · feedback.md)
    └── t99_review-whole/                   ⑤ review whole, one per Job
        ├── t99_review-whole.md             state · step: ⑤
        └── runs/run-rank-t99/result/       hard: ranking.csv (rank · design · predicted · why · kept)
```

A design Block is a special board (JL 261008: Paper, Insight, Prototype and Design are the special boards; Labeling will be one too), named by its kind: `Design-<name>[-<YYMMDD>]`, e.g. `Design-<app>-<round>-<YYMMDD>`. The folder name is a label; a reader knows the Block by its `board.md` (`board-kind: design-board`). An older `bNN_<app>` Block stays readable.

`jNN_<goal>-<goal-slug>_<method>-<method-slug>` names the goal and the method by their ids, lowercased, each followed by its slug so a person can read the folder (JL 261008: "MNN, GNN are not human readable … add the <slug>"): `j03_g01-review-new-rx_m04-actionable-insights`. The goal's slug is its `name:` in `board.md ## Goals`; the method's is its registry folder's (`M04-actionable-insights`). Both slugs are optional for an older folder. The folder name is only a label; the face's `goal:`, `method:` and `inputs:` lines are the pins every reader uses.


The rules
---------

1. **One goal × one method version × one inputs version per Job.** The face pins `goal: G01`, `method: M04 m2` with
   `method-sha:` and `inputs: i2`. A changed method or a new inputs version is a new Job, never an edit; `moved:`
   says which one clock moved from the Job before it (`start` · `method` · `inputs`). Two Jobs on one goal and one
   inputs version, with different methods, compare methods.
2. **The goal is signed once, at the Block.** `run-add-goal-<goal>` writes it into `board.md ## Goals` and a person
   signs it (`signed:`); aim, who, venue and n must be filled, only `leave-out` may stay `?`. The shared rules in
   `design-goal.md` carry `rules: r<k>` and their own `signed:`. `run-add-job` writes the pins and copies the goal's
   `n` onto the face; `run-setup-goal-jNN` only confirms the pin names a signed goal.
3. **A method is registered, never written in a Job.** The registry is `haipipe-design-method/methods/`: a method
   `MNN` and its versions `m<k>`, each version its choices at the five steps of the design unit (① See input ·
   ② Reason ideas · ③ Conduct process · ④ Review item · ⑤ Review whole). `run-setup-method-jNN` copies the pinned
   version into `inputs/method.md` and records its sha. A Block proposes changes (`run-propose-method-<slug>`); the
   registry cuts the next version.
4. **The Job's `inputs/` is the fence.** The design work sees only `inputs/`: `goal.md`, `method.md`, relative links
   into the Block's `inputs/iN/` (and the insight handoff copied there), and `manifest.yaml`, which lists every file
   with its source and its sha256 (stored as the first 12 hex) and which part of step ① it serves. Each reasoning
   step's `from` (its own, or its topic's) names a file in the manifest or says `own knowledge`. Before any design
   Task opens, the reviewer agent checks it in the first pass of `run-open-designs-jNN`
   (`passes/pNN-<MMDD>/fence-check.md`); the Tasks open only after it says pass.
5. **Every step of the method is a Task.** `t00_reason-ideas/` (②), one `tNN_d<NN>_<slug>/` per design (③ ④),
   `t99_review-whole/` (⑤). A new object is a new Task; another step on the same object is another Run. A revision
   is a Run in the design's Task, never a new Task; a new idea is a new Task.
6. **`run-open-designs-jNN` opens the design Tasks**, one per idea in t00's `ideas.yaml` (each idea carries the
   `name` its Task is named by); t00 only writes ideas. ② makes N + 5 ideas unless the method version's ② says
   otherwise; N is the goal's `n`, copied onto the Job's face.
7. **Verify and rank are another agent's.** ④ and ⑤ run in a fresh reviewer context, never the agent that generated
   (the verify's `by:` differs from every generate and revise `by:` of the Task). ④ runs T0 rules and T1 sources
   on every draft, and T2 critique when the method version's ④ lists it. T3 pretest, when the method's ⑤ asks for
   it, runs once per Job on the kept designs, inside t99's rank Run.
8. **A hard Run's Result reaches its Task only by projection.** A hard Run writes only its `result/`; once it has
   closed, `haipipe-design-workflow` carries it into the Task: `project_draft.py draft` (the newest draft into the
   face's `## Design` and `elements.yaml`, `state: verify`), `project_draft.py verdict` (the verify's status into
   `state: passed | revise`).
9. **A prediction is a draft until the release.** t99's `run-rank-t99` writes the ranking and each design's
   predicted effect into its own `result/ranking.csv` (a hard Run writes nothing else). When it closes,
   `haipipe-design-workflow` projects each row into its design Task: `prediction.yaml` (`frozen: draft`) and
   `state: kept` or `dropped`. `run-freeze-predictions-jNN` freezes them (`frozen: <date>`) when a person releases
   (`run-release-jNN`); both are signed together. Dropped designs keep their Tasks, folded at the end.
10. **What an Exp returns lands once, at the Block.** `run-add-observed-eNN` writes `observed/eNN_<exp>/arms.csv`
   (`arm · job · design · n · observed`: per-arm totals only, never rows) from an insight Block's signed handoff
   or a vendor's per-arm report; `run-score-eNN` scores every arm's design into the `scores.csv` in its own folder. A
   Job's Predicted vs observed reads its own rows; the method scorecard sums them per method version.
11. **The fence never changes after `run-reason-t00`.** A newer handoff never makes a released design stale, and a
   fix that needs an input the fence lacks is not a revise: the design is dropped, or a new inputs version makes a
   new Job (`moved: inputs`).

A design's `state:` walks `draft → verify → revise → passed → kept | dropped → released`.


Runs
----

Every Run is a folder named `run-<type>-<target>/` (JL 261007: "unify the name to be run-xxx-xxx") with its
`run.yaml` card (`run · kind · type · scope · target · skill · agent · signs · status · by · started_at ·
finished_at · usage`), which is also its ticket. A **hard** Run (`kind: hard`) writes only its own `result/` and
counts as evidence; it may retry in place while open, and its `result/` never changes once closed. A **soft** Run
writes into its level's own files and keeps its passes in `passes/pNN-<MMDD>/`; `run-revise` keeps each new draft
in its pass and `run-score` keeps its `scores.csv` in its own folder. A repeat on the same target names what it
reads, never a counter: the verify of draft 2 of d04 is `run-verify-d04-v2` (k = 1 + the revise passes). Older names stay readable: `rNN_<type>_<target>/`
(drawn before 261007) and `run-design-<step>-<MMDD>-<slug>` (the older board).

```text
level  Run                              kind  does                                    skill
Block  run-add-goal-<goal>              soft  a goal into the goal list; a person signs haipipe-design-goal
       run-setup-rules                  soft  the shared rules                          haipipe-design-goal
       run-add-inputs-i<N>              soft  an inputs version, frozen                 haipipe-design-goal
       run-add-job-j<NN>                soft  an empty Job, its pins written            haipipe-design
       run-propose-method-<slug>        soft  a method change, to the registry          haipipe-design-method
       run-add-observed-e<NN>           soft  an Exp's per-arm totals                   haipipe-design-method
       run-score-e<NN>                  soft  every arm's design scored (reviewer)      haipipe-design-method
       run-propose-questions            soft  the Block's questions; another agent agrees haipipe-question
       run-report-q<NN>                 soft  a question's report                       haipipe-report
       run-draw-s<NN>                   soft  a studio topic                            excalidraw-report
Job    run-setup-goal-j<NN>             soft  confirm the pin names a signed goal       haipipe-design-goal
       run-setup-method-j<NN>           soft  pin a method version: inputs/method.md    haipipe-design-method
       run-setup-inputs-j<NN>           soft  goal.md · links · manifest (step ①)       haipipe-design-goal
       run-open-designs-j<NN>           soft  fence check, then a Task per idea         haipipe-design
       run-freeze-predictions-j<NN>     soft  freeze the kept predictions; a person     haipipe-design-delivery
       run-release-j<NN>                soft  release the kept designs; a person signs  haipipe-design-delivery
       run-close-j<NN>                  soft  close the Job; a person signs             haipipe-design-workflow
Task   run-reason-t00                   hard  ② ideas.yaml · chains.yaml                haipipe-design-unit
       run-generate-d<NN>               hard  ③ one design, its elements                haipipe-design-unit
       run-verify-d<NN>-v<k>            hard  ④ T0 · T1 (· T2) on draft k, another agent haipipe-design-unit
       run-revise-d<NN>                 soft  the next draft from feedback, one pass    haipipe-design-unit
       run-rank-t99                     hard  ⑤ rank, keep N, predict (· T3), another   haipipe-design-unit
```

The run cards (`haipipe-design-workflow/references/run-cards.md`) give each Run its button, agent, sign and prompt;
`haipipe-design-workflow` routes them.


The six Spaces at each level
----------------------------

```text
        Description              Audience Report                        Work Details               Runs                Delivery
Block   Map · Goals · Methods ·  Questions · Cost · Predicted vs        one card per Job           set up · launch ·   every released design
        Inputs                   observed · Method scorecard                                       report
Job     Goal · Method · Inputs   Reason ideas · Design display ·        Reason ideas · Conduct &   Setup · Reason ·    designs.md ·
                                 Review whole · Predicted vs            review · Review whole      Conduct · Whole     designs.json
                                 observed · Performance
Task    t00: Task                t00: Topics · Ideas                    t00: Chains                its Runs            what it hands on
        a design: Design ·       a design: Tests · Drafts · Performance a design: Elements
        Evaluation               t99: Ranking · Coverage                t99: Kept · Dropped
        t99: Task
```

One tab serves every Task; its run types decide what each Space shows (s13). Every level has an Idea Studio.
