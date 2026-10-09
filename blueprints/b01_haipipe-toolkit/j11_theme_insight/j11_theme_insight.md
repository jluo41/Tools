# j11 · Theme: insight

job-of: b01_haipipe-toolkit (the Block `b11_theme_insight` until 261009; its questions, studio and runs moved with it)
spine: Design questions about the insight Theme as one ladder: what an Insight Block, a DIKW level Job, a question Task and a dataset × partition Run each hold and show, how partitions and pooling appear, where a question's gates live, what each level delivers, and what becomes of the older register boards.
close: Each recorded question has a report Page with an answer status, and every answered question names the skill, workbench or builder change that settled it.

## Topic

The insight Theme answers questions about one data extract, climbing Data → Information →
Knowledge → Wisdom. Its new layout is a task Block (`tasks/b5N_<topic>_dikw/`, `workbench:
insight`): one Job per level (`j01_data` … `j04_wisdom`), one Task per question
(`tNN_<question>/`), one hard Run per dataset × partition (`runs/<dataset>_<partition>/`).
The older register board (`insights/<Dataset>-InsightBoard/`: `board.md`, `0-MT-meta/`, one
folder per partition) keeps its layout until it is carried over.

Today the Insight workbench shows all of it at Block level, in five Spaces (Scope ·
Prototype · Insight · Check · Delivery), with the levels as Views of Prototype and the
partitions as Views of Insight. The shared ladder (b03) gives every level the same six
Spaces: Description · Idea Studio · Audience Report | Work Details | Runs · Delivery. This
Block asks how insight fits that ladder level by level, and what it needs that no other
Theme has.

Most answers here are a change to the insight skills (`2_theme/insight/haipipe-insight`,
`workbench-insight`, `haipipe-insight-workflow`), the Insight workbench server, or b03's
shared builder, not a Task Run. A Question may have no work entries; its report links the
changed files and the drawings.

Excluded: the ladder itself and what every Theme shares (b03_project_workbench); the Design Theme
that reads Insight's handoff (b12_theme_design); the DIKW methods, which live in the
family's Guide.

## Pipeline

```text
chat section -> Related question -> haipipe-question -> skill, workbench or builder change -> report Page
                                                     -> studio/ drawings (shared by the questions)
```

## Pages

No Jobs yet. The drawings the questions share are in `studio/`:

```text
studio/
├── s00-insight-structure/   the thinking: Prototype versions × data versions, triggers
├── s01-insight-ladder/      the proposal: every level, Board to Task, options A and B
├── s02-insight-workbench/   today's Insight workbench (the Guide's RoadMap Draw serves it)
├── s03-insight-methods/     the methods: the cards, their code, today's screens; and the Guide's methods drawing
├── s11-block-level/         the Block tab: its six Spaces, proposed
├── s12-job-level/           a Job tab (one DIKW level): its six Spaces, proposed
├── s13-task-level/          a Task tab (one question): its six Spaces, proposed
├── s31-insight-guide/       the Guide tab by level: Block · Job · Task (b16's s31 shape)
├── s61-insight-slides/      the slide deck's storyboard: the logic flow, then a frame per slide
└── _build/insight_ui.py     the screen helpers and card reader s03 · s11-s13 share
```

s01 is drawn from b03's shared definitions (`b03_project_workbench/studio/s01-overall-tree-structure/`)
and rebuilt by b03's `studio/_build/make.sh`. s02 and s03 came from the Insight workbench's
own studio (`servers/workbench-insight/studio/`, removed 261007).

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
    today View it replaces, drawn in studio/s01-insight-ladder and agreed.
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
- title: b03_project_workbench Q07 (how the workbench maps onto the ladder)
  url: ../b03_project_workbench/reports/q07_workbench_mapping/q07_workbench_mapping.md
  questions:
  - Q01
  contribution: The six Spaces every level shares, and the builder that draws them.
  notes: ''
```
