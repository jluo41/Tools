# b11 · Theme: insight

board-kind: task-block
package: plugins/haipipe-toolkit
theme: insight
examples: insight/Insight-Example, insight/InsightDataPrep-Example, insight/InsightQuestionBook-Example
ui-block: examples/Project-Ladder/insight/Insight-Example
ui-block: examples/Project-Ladder/insight/InsightQuestionBook-Example
ui-block: examples/Project-Ladder/insight/InsightDataPrep-Example
shared-blueprint: b01_haipipe-toolkit
spine: Design questions about the insight Theme as one ladder: what an insight Board (one dataset), a question version × data version Job, a question Task and a segment Run each hold and show, how segments and pooling appear, where a question's gates live, what each level delivers, and what becomes of the older register boards.
close: Each recorded question has a report Page with an answer status, and every answered question names the skill, workbench or builder change that settled it.
session: Ladder-b11-Insight-v1031

## Topic

Insight has three cooperating Block kinds. A Question Book defines versioned questions and methods. DataPrep defines versioned preparation code. An Insight Board pins a question version, a data version and a prep version when used; its Tasks execute prep or answer questions, with segment calculations recorded as Runs.

The Block owns the page. Jobs, Tasks and Runs remain inside its Jobs section. Brief explains the goal and evidence; Plan + Results pairs work with its outcome; Findings carries source-linked understanding across levels. Each Studio uses the shared frame and existing mindmap.

Band classification comes from Work's shared registry, separate from Studio Type definitions. This theme references Block Structure, Block Job UI Preview and Theme Guide; its current instances need no additional local type definition or empty type group. Shared readers and server lifecycle belong to Work.

## Pipeline

```text
chat section -> Related question -> hai-report -> skill, workbench or builder change -> report Page
                                                     -> sNN topic drawings (shared by the questions)
```

## Pages

- [s01 · Block Structure: Insight Board](s01-insight-board-structure/s01-insight-board-structure.md)
- [s02 · Block Structure: Question Book](s02-question-book-structure/s02-question-book-structure.md)
- [s03 · Block Structure: DataPrep](s03-dataprep-structure/s03-dataprep-structure.md)

Each has Structure / Draw / Skills. Naming rules and their real examples sit together under Folder, Job-Task and Studio.

- [s11 · Block Job UI Preview: Insight Board](s11-insight-job-preview/s11-insight-job-preview.md)
- [s12 · Block Job UI Preview: Question Book](s12-questionbook-job-preview/s12-questionbook-job-preview.md)
- [s13 · Block Job UI Preview: DataPrep](s13-dataprep-job-preview/s13-dataprep-job-preview.md)

Page-Job and Page-Task embed real Block selections. Contract views describe the responsibilities. QuickHtml preserves Segment grid, Version changes and Steps and Runs. Draw preserves the existing MindMap and Canvas; Files keeps the original outputs.

[s99 · Theme Guide: Insight](s99-guide/s99-guide.md) retains its directory, content and drawings. It references the shared Theme Guide definition. Directory numbering is not a new Studio Type.

## Renumbered

- 261126: s07-job-page-view is s11-insight-job-preview, s08-book-job-page-view is s12-questionbook-job-preview, s09-prep-job-page-view is s13-dataprep-job-preview; the s1N band holds insight's Job UI Previews, one per kind of insight Block. The earlier s11 to s13 (Block, Job and Task level sketches) were deleted the same day.

## Questions

```yaml
questions:
- id: Q01
  title: How does an insight topic climb the ladder?
  question: What do the insight Block, a DIKW level Job, a question Task and a dataset × segment
    Run each hold and show on screen, and which of today's Insight workbench Views moves to
    which level?
  hypothesis: The Block keeps what spans the levels (the dataset and segments, the full Insight
    table, Meta's counts, the handoff); each level is a Job with the Block's six Spaces, Work
    Details = its questions; each question is a Task, Work Details = its segments; each
    Run is one dataset × segment with its generated report.
  acceptance: Answered when every level names its folder, its six Spaces' content and the
    today View it replaces, drawn and agreed.
  work: []
  report: ''
- id: Q02
  title: How do segments and pooling show?
  question: Where do an extract's segments (Full, the segments, Cross) and a question's pooling
    verdict (POOL, SPLIT, UNDETERMINED) show at each level, and how is a segment added?
  hypothesis: Segments are the third row of Audience Report at Block, Job and Task; the
    pooling verdict is a Knowledge question's own row under Cross; a segment is a Block Run (register
    a segment) that adds a Run per question, never a new folder.
  acceptance: Answered when each level's screen places the segments and the verdict, and
    registering a segment names the Runs it makes.
  work: []
  report: ''
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
  report: ''
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
  report: ''
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
```

## Related resources

```yaml
resources:
- title: hai-insight skill (the Insight door, the Block contract, carry over)
  url: plugins/haipipe-toolkit/skills/3_theme/insight/hai-insight
  questions:
  - Q01
  - Q02
  - Q04
  - Q05
  contribution: Owns the Insight Block contract (one Job per level, one Task per question) and the register-board laws.
  notes: ''
- title: workbench-insight skill (the served Insight workbench)
  url: plugins/haipipe-toolkit/skills/3_theme/insight/workbench-insight
  questions:
  - Q01
  - Q02
  - Q03
  contribution: Today's five Spaces, the Question Book and Insight Views, the Check Space and the pop-outs.
  notes: ''
- title: b10_project_workbench (removed 261126) Q07 (how the workbench maps onto the ladder)
  url: b10_project_workbench/s02-studio-workbench-skill/s02-studio-workbench-skill.md (removed 261126)
  questions:
  - Q01
  contribution: The six Spaces every level shares, and the builder that draws them.
  notes: ''
```

## Blueprint home

This Theme is an independent blueprint Block under `examples/Project-Ladder/blueprint/b11_theme_insight/`
since 261010. Its studio topics, questions, reports and Runs keep their existing
identities. Shared toolkit foundations remain in [b01](../../../Project-Packages/work/b01_haipipe-toolkit/board.md).
