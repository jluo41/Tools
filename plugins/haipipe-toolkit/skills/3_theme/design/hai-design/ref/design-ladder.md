# Design ladder: Block, Job, Task and Run

This is the folder contract read by `hai-design/scripts/design_ladder.py` and the Design workbench reader.
A Design Board owns one application in one channel. A Design Method Book owns one channel's methods and may
serve several Boards. Each owner skill controls its own records; this reference defines how they connect.

## Types, names and groups

| Block | Job contract | Job naming rule | Task types and naming rules |
|---|---|---|---|
| Design Board | Design execution: one goal × pinned method version × inputs version | `jNN_〈goal〉_M0x-〈method〉-mK_inputs-vM` | `design-reason` → fixed `reason ideas`; `design-item` → `〈design name〉`; `design-whole` → fixed `review whole` |
| Design Method Book | Method type: one registered method identity and its signed versions | `jNN_M0x-〈method〉` | No execution Task layer |

The Board's Task face carries `task-type:`. These three values are written by the scaffold and occur in the
real examples. Job contracts here describe roles; the current example Job faces do not declare a separate
`job-type:` enum. Do not invent serialized Job types or method-development Tasks.

Job grouping is independent of type. A Board groups by its pinned method's registry `family:`; without a family
the reader falls back to its goal, then Goals. A Book uses its Job's authored `family:`, then the registry family,
then Methods. Board Task groups are Ideas, Designs and Review. The current reader maps those groups from the
Task's role; they are not additional Task types.

The Board selector labels a Job with its jNN, goal id, method/version and inputs version. The Job face keeps the
goal and method in words. The Book labels a Job with its jNN, method id and title. Fixed names have no brackets;
a name filled in by the work uses 〈brackets〉 in a rule diagram. Never rename a real folder merely to change a label.

A Book's M01 and M02 are different method identities, not versions of one another. Signed `mK.md` files live inside
the method Job and are listed in its `versions:` field. The Board names its Book with `method-book:`; its Jobs pin
`method: M01 m2`, for example. Recipes come from `hai-design-method/methods/` and remain frozen once pinned.
The channel rules live in the venue pack, application rules in signed `design-goal.md`, and goal-specific rules
in `board.md ## Goals`. A new material set changes inputs, not the method identity.

The tree
--------

```text
design/DesignMethodBook-〈Topic〉/           Block: the designer of one kind of thing
├── board.md                                its face: board-kind: design-method-book · channel · serves: design/Design-〈name〉 · goal
├── jNN_M0x-〈slug〉/                         one method type: its face (method · title · state · versions) and
│                                           mK.md, each signed version copied from the library and frozen
└── proposals/〈slug〉.md                     the backlog: kind · step · from · state · taken-in; a type's next version is cut here

design/Design-〈name〉/                      Block: one application, one channel
├── board.md                                its face: board-kind: design-board · channel · method-book · spine · close
│                                           ## Goals (```yaml goals:) · ## Questions (```yaml questions:)
├── design-goal.md                          the shared rules every goal keeps: rules: r〈k〉 · signed: (hai-design-goal)
├── inputs/inputs-vN/                       one inputs version: rules · theory · handoff copies, manifest.yaml (frozen)
├── observed/eNN_〈exp〉/                     what one Exp returned: arms.csv · source.md · manifest.yaml (frozen)
├── sNN-〈topic〉/                     Studio: drawings, one topic each
├── reports/qNN_〈topic〉/                    Report: the Block's questions
├── runs/run-〈type〉-〈target〉/               every Block Run is soft: run.yaml · passes/
├── delivery/                               designs.json · designs.md · screens/〈jNN〉-〈dNN〉.〈ext〉: every Job's release
└── jNN_〈goal〉_M0x-〈slug〉-mK_inputs-vM/  Job: one goal × one method version × one inputs version → N designs
    ├── jNN_〈goal〉_M0x-〈slug〉-mK_inputs-vM.md   its face (front matter): goal · method · method-sha ·
    │                                       inputs · n · state · moved
    ├── inputs/                             the fence: goal.md · method.md · links into ../inputs/inputs-vM/ ·
    │                                       manifest.yaml (each file, its source, its sha256 as its first 12 hex;
    │                                       with method-sha, a decided exception to the SPACE no-hash rule)
    ├── sNN-〈topic〉/ · reports/              optional topics and reports
    ├── runs/                               soft: run-setup-goal · run-setup-method · run-setup-inputs ·
    │                                       run-open-designs · run-freeze-predictions · run-release · run-close
    ├── (delivery in Block)                 〈Block〉/delivery/jNN_〈job〉/: designs.json · designs.md · screens/〈dNN〉.〈ext〉, word for word
    ├── t00_reason-ideas/                   ② reason ideas, one per Job
    │   ├── t00_reason-ideas.md             state · step: ②
    │   └── runs/run-reason-t00/result/     hard: ideas.yaml · chains.yaml · topics.md
    ├── tNN_d〈NN〉_〈slug〉/                   ③ ④ one design, its short name born with its idea in t00
    │   ├── tNN_d〈NN〉_〈slug〉.md             state · name · idea · rank; ## Design · ## Evaluation
    │   ├── elements.yaml                   one entry per element: element · words · from · because · step · changed
    │   ├── prediction.yaml                 predicted · against · by · why · frozen (a draft until the release)
    │   └── runs/                           hard: run-generate-d〈NN〉/result/ (design.md · elements.yaml) ·
    │                                             run-verify-d〈NN〉-v〈k〉/result/ (review.md)
    │                                       soft: run-revise-d〈NN〉/passes/pNN-〈MMDD〉/ (one pass per new draft:
    │                                             design.md · elements.yaml · feedback.md)
    └── t99_review-whole/                   ⑤ review whole, one per Job
        ├── t99_review-whole.md             state · step: ⑤
        └── runs/run-rank-t99/result/       hard: ranking.csv (rank · design · predicted · why · kept)
```

The rules
---------

1. **One goal × one method version × one inputs version per Job.** The face pins `goal: G01`, `method: M04 m2` with
   `method-sha:`, and `inputs: inputs-v2`. A changed method or a new inputs version is a new Job, never an edit; `moved:`
   says which one clock moved from the Job before it (`start` · `method` · `inputs`). Two Jobs on one goal and one
   inputs version, with different methods, compare methods.
2. **The goal is signed once, at the Block.** `run-add-goal-〈goal〉` writes it into `board.md ## Goals` and a person
   signs it (`signed:`); name, aim, who, venue and n must be filled, only `leave-out` may stay `?`. The shared rules in
   `design-goal.md` carry `rules: r〈k〉` and their own `signed:`. `run-add-job` writes the pins and copies the goal's
   `n` onto the face; `run-setup-goal-jNN` only confirms the pin names a signed goal.
3. **A method is registered, never written in a Job.** The registry is `hai-design-method/methods/`: a method
   `MNN` and its versions `m〈k〉`, each version its choices at the five steps of the design unit (① See input ·
   ② Reason ideas · ③ Conduct process · ④ Review item · ⑤ Review whole). `run-setup-method-jNN` copies the pinned
   version into `inputs/method.md` and records its sha. A Block proposes changes (`run-propose-method-〈slug〉`); on a
   Board with a Book the proposal lands in the Book's `proposals/` and a person signs the type's next version there, else the
   registry cuts the next version.
4. **The Job's `inputs/` is the fence.** The design work sees only `inputs/`: `goal.md`, `method.md`, relative links
   into the Block's `inputs/inputs-vN/` (and the insight handoff copied there), and `manifest.yaml`, which lists every file
   with its source and its sha256 (stored as the first 12 hex) and which part of step ① it serves. Each reasoning
   step's `from` (its own, or its topic's) names a file in the manifest or says `own knowledge`. Before any design
   Task opens, the reviewer agent checks it in the first pass of `run-open-designs-jNN`
   (`passes/pNN-〈MMDD〉/fence-check.md`); the Tasks open only after it says pass.
5. **Three Task roles organize execution.** `t00_reason-ideas/` (②), one `tNN_d〈NN〉_〈slug〉/` per design (③ ④),
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
   closed, `hai-design-workflow` carries it into the Task: `project_draft.py draft` (the newest draft into the
   face's `## Design` and `elements.yaml`, `state: verify`), `project_draft.py verdict` (the verify's status into
   `state: passed | revise`).
9. **A prediction is a draft until the release.** t99's `run-rank-t99` writes the ranking and each design's
   predicted effect into its own `result/ranking.csv` (a hard Run writes nothing else). When it closes,
   `hai-design-workflow` projects each row into its design Task: `prediction.yaml` (`frozen: draft`, with the
   row's `why`, so every predicted number carries its basis) and `state: kept` or `dropped`. `run-freeze-predictions-jNN` freezes them
   (`frozen: 〈date〉`) when a person releases (`run-release-jNN`); both are signed together, as one review step
   (Review and approve: the one place a person reviews before launch). Dropped designs keep their Tasks, folded at the end.
10. **What an Exp returns lands once, at the Block.** `run-add-observed-eNN` writes `observed/eNN_〈exp〉/arms.csv`
   (`arm · job · design · n · observed`: per-arm totals only, never rows) from an insight Block's signed handoff
   or a vendor's per-arm report; `run-score-eNN` scores every arm's design into the `scores.csv` in its own folder. A
   Job's Predicted vs observed reads its own rows; the method scorecard sums them per method version.
11. **The fence never changes after `run-reason-t00`.** A newer handoff never makes a released design stale, and a
   fix that needs an input the fence lacks is not a revise: the design is dropped, or a new inputs version makes a
   new Job (`moved: inputs`).

A design's `state:` walks `draft → verify → revise → passed → kept | dropped → released`.


Runs
----

Every Run is a folder named `run-〈type〉-〈target〉/` with its
`run.yaml` card (`run · kind · type · scope · target · skill · agent · signs · status · by · started_at ·
finished_at · usage`), which is also its ticket. A **hard** Run (`kind: hard`) writes only its own `result/` and
counts as evidence; it may retry in place while open, and its `result/` never changes once closed. A **soft** Run
writes into its level's own files and keeps its passes in `passes/pNN-〈MMDD〉/`; `run-revise` keeps each new draft
in its pass and `run-score` keeps its `scores.csv` in its own folder. A repeat on the same target names what it
reads, never a counter: the verify of draft 2 of d04 is `run-verify-d04-v2` (k = 1 + the revise passes).

```text
level  Run                              kind  does                                    skill
Block  run-add-goal-〈goal〉              soft  a goal into the goal list; a person signs hai-design-goal
       run-setup-rules                  soft  the shared rules                          hai-design-goal
       run-add-inputs-v〈N〉              soft  an inputs version, frozen                 hai-design-goal
       run-add-job-j〈NN〉                soft  an empty Job, its pins written            hai-design
       run-propose-method-〈slug〉        soft  a method change, to the registry          hai-design-method
       run-add-observed-e〈NN〉           soft  an Exp's per-arm totals                   hai-design-method
       run-score-e〈NN〉                  soft  every arm's design scored (reviewer)      hai-design-method
       run-propose-questions            soft  the Block's questions; another agent agrees hai-report
       run-report-q〈NN〉                 soft  a question's report                       hai-report
       run-draw-s〈NN〉                   soft  a studio topic                            hai-draw report
Job    run-setup-goal-j〈NN〉             soft  confirm the pin names a signed goal       hai-design-goal
       run-setup-method-j〈NN〉           soft  pin a method version: inputs/method.md    hai-design-method
       run-setup-inputs-j〈NN〉           soft  goal.md · links · manifest (step ①)       hai-design-goal
       run-open-designs-j〈NN〉           soft  fence check, then a Task per idea         hai-design
       run-freeze-predictions-j〈NN〉     soft  freeze the kept predictions; a person     hai-design-delivery
       run-release-j〈NN〉                soft  release the kept designs; a person signs  hai-design-delivery
       run-close-j〈NN〉                  soft  close the Job; a person signs             hai-design-workflow
Task   run-reason-t00                   hard  ② ideas.yaml · chains.yaml                hai-design-unit
       run-generate-d〈NN〉               hard  ③ one design, its elements                hai-design-unit
       run-verify-d〈NN〉-v〈k〉            hard  ④ T0 · T1 (· T2) on draft k, another agent hai-design-unit
       run-revise-d〈NN〉                 soft  the next draft from feedback, one pass    hai-design-unit
       run-rank-t99                     hard  ⑤ rank, keep N, predict (· T3), another   hai-design-unit
```

The run cards (`hai-design-workflow/references/run-cards.md`) give each Run its button, agent, sign and prompt;
`hai-design-workflow` routes them.



## Workbench and Studio

The only standalone workbench page is the Block. Open its Jobs section and select a Job, Main or a Task there.
Main hides the Task row. A selected Task retains its owning Block and original Run identities. Method Book Main
shows Method, Steps, Versions and Used by when populated; it has no execution Task selector.

The two structure Studios are `b12_theme_design/s01-design` and `s02-workbench-ui`; the live Job previews are
`s11-design-job-preview` and `s12-methodbook-job-preview`. The shared renderer owns the layout and Bands.
Structure includes naming rules and real examples, Draw uses the shared drawing implementation, and Skills
opens the actual owners. Studio Type definitions are distinct from Band classification. Reference shared types
and add theme-specific definitions only when needed; do not create empty type groups on actual Work Blocks.

Read [workbench-design](../../workbench-design/SKILL.md) and its constitution for UI behavior and validation.
