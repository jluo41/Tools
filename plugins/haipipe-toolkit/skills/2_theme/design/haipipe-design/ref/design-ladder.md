Design ladder: the design theme's Block · Job · Task · Run
==========================================================

(JL 261007, designed in Tools/blueprints/Project-Ladder/work/b12_theme_design: s00 the thinking, s11 Block, s12 Job, s13 Task, s21 Runs
and skills.) A design sits on the shared ladder: one Block per application and channel, one Job per goal done by one
registered method version on one inputs version, one Task per step of that method (t00 reason ideas, one Task per
design, t99 review whole), and the Runs that make and check them. On the older tabbed screen each level has the six Spaces of the base
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
design/DesignMethodBook-<Topic>/           Block: the designer of one kind of thing (JL 261109)
├── board.md                                its face: board-kind: design-method-book · channel · serves: design/Design-<name> · goal
├── jNN_M0x-<slug>/                         one method type: its face (method · title · state · versions) and
│                                           mK.md, each signed version copied from the library and frozen
└── proposals/<slug>.md                     the backlog: kind · step · from · state · taken-in; a type's next version is cut here

design/Design-<name>/                      Block: one application, one channel
├── board.md                                its face: board-kind: design-board · channel · method-book · spine · close
│                                           ## Goals (```yaml goals:) · ## Questions (```yaml questions:)
├── design-goal.md                          the shared rules every goal keeps: rules: r<k> · signed: (haipipe-design-goal)
├── inputs/inputs-vN/                       one inputs version: rules · theory · handoff copies, manifest.yaml (frozen)
├── observed/eNN_<exp>/                     what one Exp returned: arms.csv · source.md · manifest.yaml (frozen)
├── sNN-<topic>/                     Idea Studio: drawings, one topic each
├── reports/qNN_<topic>/                    Audience Report: the Block's questions
├── runs/run-<type>-<target>/               every Block Run is soft: run.yaml · passes/
├── delivery/                               designs.json · designs.md · screens/<jNN>-<dNN>.<ext>: every Job's release
└── jNN_<goal>_M0x-<slug>-mK_inputs-vM/  Job: one goal × one method version × one inputs version → N designs
    ├── jNN_<goal>_M0x-<slug>-mK_inputs-vM.md   its face (front matter): goal · method · method-sha ·
    │                                       inputs · n · state · moved
    ├── inputs/                             the fence: goal.md · method.md · links into ../inputs/inputs-vM/ ·
    │                                       manifest.yaml (each file, its source, its sha256 as its first 12 hex;
    │                                       with method-sha, a decided exception to the SPACE no-hash rule)
    ├── studio/ · reports/                  optional
    ├── runs/                               soft: run-setup-goal · run-setup-method · run-setup-inputs ·
    │                                       run-open-designs · run-freeze-predictions · run-release · run-close
    ├── (delivery in Block)                 <Block>/delivery/jNN_<job>/: designs.json · designs.md · screens/<dNN>.<ext>, word for word
    ├── t00_reason-ideas/                   ② reason ideas, one per Job
    │   ├── t00_reason-ideas.md             state · step: ②
    │   └── runs/run-reason-t00/result/     hard: ideas.yaml · chains.yaml · topics.md
    ├── tNN_d<NN>_<slug>/                   ③ ④ one design, its short name born with its idea in t00
    │   ├── tNN_d<NN>_<slug>.md             state · name · idea · rank; ## Design · ## Evaluation
    │   ├── elements.yaml                   one entry per element: element · words · from · because · step · changed
    │   ├── prediction.yaml                 predicted · against · by · why · frozen (a draft until the release)
    │   └── runs/                           hard: run-generate-d<NN>/result/ (design.md · elements.yaml) ·
    │                                             run-verify-d<NN>-v<k>/result/ (review.md)
    │                                       soft: run-revise-d<NN>/passes/pNN-<MMDD>/ (one pass per new draft:
    │                                             design.md · elements.yaml · feedback.md)
    └── t99_review-whole/                   ⑤ review whole, one per Job
        ├── t99_review-whole.md             state · step: ⑤
        └── runs/run-rank-t99/result/       hard: ranking.csv (rank · design · predicted · why · kept)
```

A design Block is a special board (JL 261008: Paper, Insight, Question Book and Design are the special boards; Labeling will be one too), named by its kind: `Design-<name>[-<YYMMDD>]`, e.g. `Design-<app>-<round>-<YYMMDD>`. The folder name is a label; a reader knows the Block by its `board.md` (`board-kind: design-board`). An older `bNN_<app>` Block stays readable.

**The Design Method Book** (JL 261109: "we should have both … just like Workbench Insight, we have the Prototype block
and Insight Block"; named `DesignMethodBook`, as insight's `InsightQuestionBook`) is the designer of one channel
(sms, a checklist), beside the Board it serves; `<Topic>` names the channel and the face says it (`channel: sms`, the
same line a Board carries). One Board designs in one channel, so a Project with two channels has two Books and two
Boards; one Book may serve several Boards of its channel. Rules sit in three places, each where it stays true: the
channel's own in the Guide's venue pack (`venue/venue-<channel>/`), an application's shared rules on its Board
(`design-goal.md`, signed there), and a goal's own on the goal's line. A Book
holds one Job per method type `jNN_M0x-<slug>/`. Types sit side by side and are compared, never read as versions of
each other (M01 goal only, M02 overall performance, each seeing a different amount of input); only `mK` is a version
of one type, listed on the type's face with its sign (`versions:`) and frozen beside it (`mK.md`). A method does not
change when the materials do: new materials are a new inputs version on the Board. The Board's Jobs and experiments
come back as `proposals/`; a signed proposal becomes that type's next version. The registry in
`haipipe-design-method/methods/` stays the library every Book takes its types from. The Board names its Book
(`method-book: design/DesignMethodBook-<Topic>`), and each Job pins a type and a version (`method: M01 m2`). On screen the Book reads Method · Versions · Ideas · Scorecard · MindMap.

On a Board with a Book, a Job is `jNN_<goal name>_M0x-<slug>-mK_inputs-vM`: the goal in words, then the
same ids a person reads on screen, in the face and in the Run names (`j03_confirm-by-reply_M02-overall-performance-m1_inputs-v2`),
as the insight Board's `jNN_question-vN-<slug>_data-vM`. An inputs version is `inputs/inputs-vN/`. `design_ladder.py book`,
`method` and `job` make them, and refuse an unsigned version or a name whose words do not match its pins.

On a Board with no Book (the older names), `jNN_<goal name>_<method name>` names the Job in words: the goal's `name:` in `board.md ## Goals` and the method's registry slug (`M01-goal-only` gives `goal-only`), so a person reads the folder as it is, and the workbench shows it as it is, wherever it names the Job, never the bare `jNN` (JL 261011: "make the j01 job folder name to be as readable as possible"; "I don't want we just have jNN here, not readable"; b10 s32-D15): `j01_prepare-before-visit_goal-only`, `j02_prepare-before-visit_actionable-insights`. The ids are not in the name: the face's `goal:`, `method:` and `inputs:` lines are the pins every reader uses, and the scaffold refuses a name whose words do not match them. The face's heading is in words too: `# Prepare before visit, by Actionable insights`. The older id form `jNN_<goal>[-<goal-slug>]_<method>[-<method-slug>]` (`j03_g01-review-new-rx_m04-actionable-insights`, JL 261008) stays readable.


The rules
---------

1. **One goal × one method version × one inputs version per Job.** The face pins `goal: G01`, `method: M04 m2` with
   `method-sha:`, and `inputs: inputs-v2` (an older Block: `i2`). A changed method or a new inputs version is a new Job, never an edit; `moved:`
   says which one clock moved from the Job before it (`start` · `method` · `inputs`). Two Jobs on one goal and one
   inputs version, with different methods, compare methods.
2. **The goal is signed once, at the Block.** `run-add-goal-<goal>` writes it into `board.md ## Goals` and a person
   signs it (`signed:`); aim, who, venue and n must be filled, only `leave-out` may stay `?`. The shared rules in
   `design-goal.md` carry `rules: r<k>` and their own `signed:`. `run-add-job` writes the pins and copies the goal's
   `n` onto the face; `run-setup-goal-jNN` only confirms the pin names a signed goal.
3. **A method is registered, never written in a Job.** The registry is `haipipe-design-method/methods/`: a method
   `MNN` and its versions `m<k>`, each version its choices at the five steps of the design unit (① See input ·
   ② Reason ideas · ③ Conduct process · ④ Review item · ⑤ Review whole). `run-setup-method-jNN` copies the pinned
   version into `inputs/method.md` and records its sha. A Block proposes changes (`run-propose-method-<slug>`); on a
   Board with a Book the proposal lands in the Book's `proposals/` and a person signs the type's next version there, else the
   registry cuts the next version.
4. **The Job's `inputs/` is the fence.** The design work sees only `inputs/`: `goal.md`, `method.md`, relative links
   into the Block's `inputs/inputs-vN/` (and the insight handoff copied there), and `manifest.yaml`, which lists every file
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
   `haipipe-design-workflow` projects each row into its design Task: `prediction.yaml` (`frozen: draft`, with the
   row's `why`, so every predicted number on screen carries its basis: JL 261012, from the 10-08 demo, where a leader
   asked of a +3.6 "where is that from?") and `state: kept` or `dropped`. `run-freeze-predictions-jNN` freezes them
   (`frozen: <date>`) when a person releases (`run-release-jNN`); both are signed together, as one review step
   (Review and approve: the one place a person reviews before launch). Dropped designs keep their Tasks, folded at the end.
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
       run-add-inputs-v<N>              soft  an inputs version, frozen                 haipipe-design-goal
       run-add-job-j<NN>                soft  an empty Job, its pins written            haipipe-design
       run-propose-method-<slug>        soft  a method change, to the registry          haipipe-design-method
       run-add-observed-e<NN>           soft  an Exp's per-arm totals                   haipipe-design-method
       run-score-e<NN>                  soft  every arm's design scored (reviewer)      haipipe-design-method
       run-propose-questions            soft  the Block's questions; another agent agrees haipipe-report
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
Block   Map · Goals · Methods ·  Summary · Rounds · Questions ·         one card per Job           set up · launch ·   every released design
        Inputs                   Predicted vs observed ·                                           report
                                 Method scorecard · Cost
Job     Goal · Method · Inputs   Reason ideas · Design display ·        Reason ideas · Conduct &   Setup · Reason ·    designs.md ·
                                 Review whole · Predicted vs            review · Review whole      Conduct · Whole     designs.json
                                 observed · Performance
Task    t00: Task                t00: Topics · Ideas                    t00: Chains                its Runs            what it hands on
        a design: Design ·       a design: Tests · Drafts · Performance a design: Elements
        Evaluation               t99: Ranking · Coverage                t99: Kept · Dropped
        t99: Task
```

One tab serves every Task; its run types decide what each Space shows (s13). Every level has an Idea Studio.
