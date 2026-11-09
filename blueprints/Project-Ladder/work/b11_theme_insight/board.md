# b11 · Theme: insight

board-kind: task-block
package: plugins/haipipe-toolkit
theme: insight
ui-block: blueprints/Project-Ladder/insight/Insight-Example
ui-block: blueprints/Project-Ladder/insight/Prototype-Example
ui-job: blueprints/Project-Ladder/insight/Insight-Example/j01_code-v1-example-questions_data-v1
ui-job: blueprints/Project-Ladder/insight/Insight-Example/j02_code-v1-example-questions_data-v2
ui-job: blueprints/Project-Ladder/insight/Prototype-Example/j01_code-v1_example-questions
ui-task: blueprints/Project-Ladder/insight/Insight-Example/j02_code-v1-example-questions_data-v2/t01_D01_extract-shape
ui-task: blueprints/Project-Ladder/insight/Insight-Example/j02_code-v1-example-questions_data-v2/t03_I01_outcome-by-arm
ui-task: blueprints/Project-Ladder/insight/Insight-Example/j02_code-v1-example-questions_data-v2/t05_K01_gap-holds
ui-task: blueprints/Project-Ladder/insight/Insight-Example/j02_code-v1-example-questions_data-v2/t06_W01_next-round
ui-task: blueprints/Project-Ladder/insight/Insight-Example/j02_code-v1-example-questions_data-v2/t07_X01_what-we-found
shared-blueprint: b01_haipipe-toolkit
spine: Design questions about the insight Theme as one ladder: what an insight Board (one dataset), an analysis plan × data freeze Job, a question Task and a cut Run each hold and show, how partitions and pooling appear, where a question's gates live, what each level delivers, and what becomes of the older register boards.
close: Each recorded question has a report Page with an answer status, and every answered question names the skill, workbench or builder change that settled it.
session: Ladder-b11-Insight-v1031

## Topic

The insight Theme answers what one dataset can and cannot say, climbing Data → Information →
Knowledge → Wisdom. Its layout (plan C, `haipipe-insight` ref/insight-ladder.md) has two folders: a
Prototype (`insight/Prototype-<Topic>/`, the questions and their scripts, one Job per release, read as
an analysis plan AP<N>) and an insight Board (`insight/Insight-<dataset>/`, one dataset and its data
freezes F<M>). A Board Job runs one analysis plan on one data freeze (`jNN_pN_<d>vM/`); a Task is one
question at one level (`tNN_<L><NN>_<slug>/`); a hard Run is one cut (`r01_full`, `r02_<cut>`,
`r04_cross`). The older layouts (an Insight Block with `j01_data` … `j04_wisdom`; a register board
`*-InsightBoard`) keep their shape until carried over.

The original focus-page design gives every level Report (check), Work (do) and Studio (think).
The 261101 baseline used the base's vanilla views; the later Insight renderer now supplies the
Board's Answers, Questions, Jobs, Data and Handoff; the Job's Overall, Grid and vs previous; and the
Task's Answer, By cut, Across Jobs and Plan. Each also has MindMap. The earlier five-Space and
six-Space drawings remain historical references. This Block asks how Insight fits the ladder level
by level, and what it needs that no other theme has.

## Work alignment and Task design

The [comparison](ui/structure.md) distinguishes the original three-level design, current implementation
and proposed alignment with Work's shared frame. The **Block UI**, **Job UI** and **Task UI** views show their respective
[Block](ui/block-views.md), [Job](ui/job-views.md) and [Task](ui/task-views.md) tables above the existing
live examples. Each specialized section has a clickable specification with content, layout, source,
skills and its actual View route. The shared-section row is an integration target; the dataset-facing
Insight pages are unchanged.

Use Cases in all three matrices now open source-backed project pages and Blueprint examples, grouped
by SPACE with hierarchy links and expandable Tasks/Path. Source coverage and service availability
are recorded in [acceptance](ui/acceptance.md); private mappings remain in ignored local configuration.

Keep the three levels and their different responsibilities. Overview, Status, Findings and Delivery
remain a proposal, not a requirement for adopting Review Content and Around the Work. The linked
Prototype keeps its own question/script and release responsibilities. The [new Task discussion](ui/task-design.md)
separates ongoing data enrichment, question development and literature/theory work from finite Tasks,
with inputs, outputs, completion evidence and placement options. No new Task kinds are implemented.

Most answers here are a change to the insight skills (`2_theme/insight/haipipe-insight`,
`workbench-insight`, `haipipe-insight-workflow`), the Insight workbench server, or b10's
shared builder, not a Task Run. A Question may have no work entries; its report links the
changed files and the drawings.

Excluded: the ladder itself and what every Theme shares (b10_project_workbench); the Design Theme
that reads Insight's handoff (b12_theme_design); the DIKW methods, which live in the
family's Guide.

## Pipeline

```text
chat section -> Related question -> haipipe-report -> skill, workbench or builder change -> report Page
                                                     -> studio/ drawings (shared by the questions)
```

## Pages

`j01_insight_workbench_pages/` (261101) designs the insight pages as a 3 × 3, copied from the paper
theme's (b16 j01) and the labeling theme's (b15 j01): Board, Job and Task × Report, Work and Studio, one
sNN each (s51 to s59, labeling's numbers), every view drawn as the same full screen, lettered, settled
one letter per round. All nine are drawn by its `insight_ui_cells.py`. In the later designs the Job
has Overall, Grid and vs previous; the Task has Answer, By cut, Across Jobs and Plan. DIKW levels
classify the questions, not separate analysis Jobs. The earlier level sketches s11 · s12 · s13
(six Spaces each) are the "before" it refines. The Work alignment tables preserve this design
history while proposing a new shared frame.

```text
                 Report · check    Work · do    Studio · think
t01 Board        s51               s52          s53
t02 Job          s54               s55          s56
t03 Task         s57               s58          s59
```

The drawings the questions share are in the Block's topic folders:

```text
b11_theme_insight/
├── s01-insight-ladder/          the proposal: every level, Board to Task, options A and B
├── s02-insight-workbench/       today's old five-Space Insight page (the Guide's RoadMap Draw serves it)
├── s03-insight-methods/         the methods: the cards, their code; and the Guide's methods drawing
├── s04-insight-structure/       the thinking: Prototype versions × data versions, the two clocks
├── s05-insight-workflow/        the whole workflow as one map: 16 steps in five zones, the loops, who signs
├── s11-block-level/             the Block tab, six Spaces (before j01's s51 to s53)
├── s12-job-level/               a Job tab, six Spaces (before s54 to s56)
├── s13-task-level/              a Task tab, six Spaces (before s57 to s59)
├── s21-insight-run-skill/       every insight Run type and the skill behind it
├── s31-insight-guide/           the Guide tab by level: Block · Job · Task (b16's s31 shape)
├── s32-insight-element-ui/      the old frame's element gallery
├── s33-ui-issue/                the 261008 review of the served pages, worst first
├── s61-insight-slides/          the slide deck's storyboard, then a frame per slide
└── j01_insight_workbench_pages/ the 3 × 3: t01 Board · t02 Job · t03 Task (s51 to s59)
```

s01 is drawn from b10's shared definitions (`b10_project_workbench/s01-overall-tree-structure/`).
s02 and s03 came from the Insight workbench's own studio (`servers/workbench-insight/studio/`,
removed 261007). The shared `_build/insight_ui.py` that s11 · s12 · s13 named no longer exists, so
those three are frozen drawings now; j01 replaces them.

## Questions

```yaml
questions:
- id: Q01
  title: How does an insight topic climb the ladder?
  question: What do the insight Block, a DIKW level Job, a question Task and a dataset × partition
    Run each hold and show on screen, and which of today's Insight workbench Views moves to
    which level?
  hypothesis: The Block keeps what spans the levels (the dataset and partitions, the full Insight
    table, Meta's counts, the handoff); each level is a Job with the Block's six Spaces, Work
    Details = its questions; each question is a Task, Work Details = its partitions; each
    Run is one dataset × partition with its generated report.
  acceptance: Answered when every level names its folder, its six Spaces' content and the
    today View it replaces, drawn in s01-insight-ladder and agreed.
  work: []
  report: reports/q01_insight_ladder/q01_insight_ladder.md
- id: Q02
  title: How do partitions and pooling show?
  question: Where do an extract's partitions (Full, the cuts, Cross) and a question's pooling
    verdict (POOL, SPLIT, UNDETERMINED) show at each level, and how is a cut added?
  hypothesis: Partitions are the third row of Audience Report at Block, Job and Task; the
    pooling verdict is a Knowledge question's own row under Cross; a cut is a Block Run (register
    a cut) that adds a Run per question, never a new folder.
  acceptance: Answered when each level's screen places the partitions and the verdict, and
    registering a cut names the Runs it makes.
  work: []
  report: reports/q02_partitions_pooling/q02_partitions_pooling.md
- id: Q03
  title: Where do a question's gates live?
  question: Today's Check Space shows a question's seven gates, its checks and its runtime;
    the six Spaces have no Check. Where do the gates, the alignment check and handoff eligibility
    go?
  hypothesis: A gate is a chip on the question's row (Work Details, Audience Report); a check
    is a Run under Runs; handoff eligibility shows only in Delivery, read from the owner receipts.
  acceptance: Answered when every one of today's Check Views has a place in the six Spaces,
    or a stated reason to keep a Check Space for insight.
  work: []
  report: reports/q03_question_gates/q03_question_gates.md
- id: Q04
  title: What does each level deliver?
  question: 'What does each DIKW level hand on, to whom, and where: do Data, Information and
    Knowledge deliver anything of their own, and how does the Wisdom counsel become the Design
    handoff?'
  hypothesis: D, I and K hand their signed answers up to the next level, not out; only j04_wisdom
    delivers, its counsel and handoff draft, which the Block's Delivery shows once a person
    signs it and Design reads it by exact identity.
  acceptance: Answered when each level's Delivery is either empty with a reason or names what
    it releases, and the handoff path to b12 is written.
  work: []
  report: reports/q04_level_delivery/q04_level_delivery.md
- id: Q05
  title: What becomes of the register boards?
  question: Should the older register boards (insights/<Dataset>-InsightBoard/) be carried
    over to DIKW Blocks, kept as they are, or shown by one workbench in both layouts?
  hypothesis: Carry each over with carry_over.py, word for word, when it is next worked on;
    until then the same workbench reads both, and a register board's Work Details lists its
    registers in place of level Jobs.
  acceptance: Answered when the choice is made, each existing register board has a named plan,
    and the workbench's handling of the older layout is written.
  work: []
  report: reports/q05_register_boards/q05_register_boards.md
```

## Related resources

```yaml
resources:
- title: haipipe-insight skill (the Insight door, the Block contract, carry over)
  url: https://github.com/jluo41/Tools/tree/main/plugins/haipipe-toolkit/skills/2_theme/insight/haipipe-insight
  questions:
  - Q01
  - Q02
  - Q04
  - Q05
  contribution: Owns the Insight Block contract (one Job per level, one Task per question) and the register-board laws.
  notes: ''
- title: workbench-insight skill (the served Insight workbench)
  url: https://github.com/jluo41/Tools/tree/main/plugins/haipipe-toolkit/skills/2_theme/insight/workbench-insight
  questions:
  - Q01
  - Q02
  - Q03
  contribution: Today's five Spaces, the Prototype and Insight Views, the Check Space and the pop-outs.
  notes: ''
- title: b10_project_workbench Q07 (how the workbench maps onto the ladder)
  url: ../b10_project_workbench/reports/q07_workbench_mapping/q07_workbench_mapping.md
  questions:
  - Q01
  contribution: The six Spaces every level shares, and the builder that draws them.
  notes: ''
```

## Blueprint home

This Theme is an independent blueprint Block under `blueprints/Project-Ladder/work/b11_theme_insight/`
since 261010. Its studio topics, questions, reports and Runs keep their existing
identities. Shared toolkit foundations remain in [b01](../../../Project-Packages/work/b01_haipipe-toolkit/board.md).
