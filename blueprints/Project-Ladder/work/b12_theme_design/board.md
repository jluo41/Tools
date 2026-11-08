# b12 · Theme: design

board-kind: task-block
package: plugins/haipipe-toolkit
theme: design
ui-block: blueprints/Project-Ladder/design/Design-Example
ui-job: blueprints/Project-Ladder/design/Design-Example/j03_confirm-by-reply_overall-performance
ui-job: blueprints/Project-Ladder/design/Design-Example/j01_confirm-by-reply_goal-only
ui-job: blueprints/Project-Ladder/design/Design-Example/j02_confirm-by-reply_goal-only
ui-task: blueprints/Project-Ladder/design/Design-Example/j03_confirm-by-reply_overall-performance/t00_reason-ideas
ui-task: blueprints/Project-Ladder/design/Design-Example/j03_confirm-by-reply_overall-performance/t02_d02_reminder-one-ask
ui-task: blueprints/Project-Ladder/design/Design-Example/j03_confirm-by-reply_overall-performance/t99_review-whole
shared-blueprint: b01_haipipe-toolkit
spine: How the design theme sits on the Block → Job → Task → Run ladder and shows in its workbench: a design Board for one application, a Job for one goal done by one design method returning N designs, a Task for one design, and the Runs that commission, generate, verify and revise them; how an insight Block steers a design through one handoff; and which skill and workbench owns each part.
close: Each recorded question has a report Page with an answer status; the drawings in studio/ match the shared definitions in b10_project_workbench, and every open point is either decided or carried as a question.
session: Ladder-b12-Design-v1031

## Topic

The design theme makes N designs for one goal by one method, checks them, and releases the ones that
pass; running the experiment is outside it. This Block designs that theme's place on the ladder:

```text
design/Design-<name>/             Block: one application, one channel; goals signed, inputs versions, Exp results
└── jNN_<goal>_<method>/           Job: goal G01 × method M04 m2 × inputs i2 → N designs; inputs/ is its fence
    ├── inputs/                    goal.md · method.md (the pinned version) · manifest.yaml
    ├── t00_reason-ideas/          ② reason ideas        run-reason-t00
    ├── tNN_d<NN>_<slug>/          ③ ④ one design        run-generate-d<NN> · run-verify-d<NN>-v<k> · run-revise-d<NN>
    └── t99_review-whole/          ⑤ review whole        run-rank-t99
```

A design method turns a goal and its inputs into N designs in five steps (① See input · ② Reason ideas ·
③ Conduct process · ④ Review item · ⑤ Review whole); it is registered and versioned in
`haipipe-design-method`, and a Job pins one version. The 13 kinds of method are the Guide's
(`plugins/haipipe-toolkit/servers/workbench-design/guide/method.md`). The folder contract is
`haipipe-design/ref/design-ladder.md`.

The trees, skills and screens are defined once with every other theme's, in
`../b10_project_workbench/s01-overall-tree-structure/` (`build_ladder_v4.py`, `level_views.py`); this
Block's drawings gather the design rows from there. Its sibling is `../b11_theme_insight/`, the theme
that steers a design.

Its Studio topics sit directly in the Block, each drawing beside the script that draws it (the
servers hold code only, 261007):

```text
b12_theme_design/
├── s01-design/             the design ladder at a glance
├── s02-workbench-ui/       the workbench's drawing (Guide › RoadMap Draw)
├── s03-design-methods/     the methods drawing and the design unit (Guide › Method)
├── s04-design-structure/   the thinking: what a design method is, how it evolves (a scratch)
├── s05-design-method-ladder/ where a method version is made and tried: the method Block, its five Tasks (Q06)
├── s06-design-workflow/     the whole workflow as one map, five acts A-E, and its deck (vivid slides)
├── s11-design-block/       the Block level on the six-Space frame (the "before" of s51 to s53)
├── s12-design-job/         the Job level on the six-Space frame (the "before" of s54 to s56)
├── s13-design-task/        the Task level on the six-Space frame (the "before" of s57 to s59)
├── s21-run-skill/          every design Run and the skills behind them
├── s31-design-guide/       the Guide tab cut by level: four Views × Block · Job · Task
├── s32-design-element-ui/  every element the design theme draws, today and as planned
├── s33-ui-issue/           every problem the 261008 review found in the served workbench
├── s61-design-slides/      the high-level deck (writes delivery/design-slides/)
└── j01_design_workbench_pages/   the 3 × 3: s51 to s59 (below, ## Pages)
```

Excluded: making real designs (that is a design Board's own work, under a Project), and the ladder
shared by every theme (`../b10_project_workbench/`).

## Pipeline

```text
a mark on a drawing -> the shared definitions (b03) -> the drawings rebuilt -> a question's report
```

## Pages

`j01_design_workbench_pages/` (261101) designs the design pages as a 3 × 3, copied from the labeling theme's (b15 j01),
itself copied from the paper theme's (b16 j01): Block, Job and Task × Report, Work and Studio, one sNN each (s51 to s59,
the same numbers as b15 and b17), every view drawn as the same full screen, lettered, settled one letter per round. All
nine are drawn by its `design_ui_cells.py`. The Task page letters the three Task types (A 💡 t00 reason ideas, B ✏️ one
Task per design, C 🏆 t99 review whole) and numbers each type's steps; each step is drawn from its run card, checked by
`task_views.py`'s coverage table. No Task asks the person; a person signs at the Block and the Job. They replace the
six-Space screens of s11, s12 and s13.

```text
                 Report · check    Work · do    Studio · think
t01 Block        s51               s52          s53
t02 Job          s54               s55          s56
t03 Task         s57               s58          s59
```

## Questions

```yaml
questions:
- id: Q01
  title: How does design climb the ladder?
  question: Where does design sit on the ladder, and what do its Block, Job, Task
    and Runs each hold and show on screen?
  hypothesis: The Block is one application and channel (its goal list, theory and
    shared rules); a Job is one goal done by one method, returning N designs, with
    the Block's six Spaces; a Task is one design (Design · Rationale · Evaluation);
    verify and revise are per-design Runs, Generate is the Job's.
  acceptance: Answered when every level names its folder and its six Spaces' content,
    drawn in s11-design-block, s12-design-job and s13-design-task, and method-folders.md
    agrees or is changed.
  work: []
  report: reports/q01_design_ladder/q01_design_ladder.md
- id: Q02
  title: What does the design workbench show?
  question: What does the design workbench show at each level, Space by Space, and
    how do today's Design Tasks, Design and Delivery views move there?
  hypothesis: Description = the goal and the frozen method card; Audience Report =
    the element matrix across the N designs; Work Details = the designs; Runs = commission
    · generate · verify · revise; Delivery = the released designs, word for word.
  acceptance: Answered when each level's screen is drawn (s02-workbench-ui
    redrawn on the new Job) and the workbench serves it.
  work: []
  report: reports/q02_design_workbench/q02_design_workbench.md
- id: Q03
  title: How does insight steer a design?
  question: How does an insight Block steer a design, and where does that link show
    on both sides?
  hypothesis: 'Through one crossing: a signed Wisdom answer is handed off, listed
    in the design Block''s Resources, read by the Jobs whose method reads our data
    (by insight · tailoring · theory and insight); each design''s elements name it.'
  acceptance: Answered when the handoff path is written on both sides (b11 Q04 and
    here) and drawn.
  work: []
  report: reports/q03_insight_steers_design/q03_insight_steers_design.md
- id: Q04
  title: How does one design round feed the next?
  question: 'How does a design Block keep its memory across rounds: what an Exp returns,
    how it reaches the next inputs version, and how the workbench shows the rounds?'
  hypothesis: 'One round per inputs version. An Exp returns per-arm totals once, at
    the Block (observed/eNN), scored against the frozen predictions; the next inputs
    version holds them with the insight Board newer data version, and its Jobs pin
    it (moved: inputs). Audience Report › Rounds strings the rounds in time order.'
  acceptance: Answered when the SMSR2 design Block closes one round (observed e01
    scored) and starts i2, and Rounds shows both.
  work: []
  report: reports/q04_design_rounds/q04_design_rounds.md
- id: Q05
  title: Do the design methods predict what an Exp observes?
  question: How well do each method version frozen predictions match what an Exp observes,
    and does that say which method to trust in the next round?
  hypothesis: Predictions are frozen at release with their why and scored after the
    Exp (direction, in range); the Method scorecard sums them per method version;
    with few arms a match is only a hint.
  acceptance: Answered when one Exp has been scored across two or more methods and
    the Method scorecard reads it.
  work: []
  report: reports/q05_method_predictions/q05_method_predictions.md
- id: Q06
  title: Where is a design method made and tried?
  question: Where on the ladder is a design method version written, tested and compared
    before a design Job pins it, and how do the Board's results come back as its next
    version?
  hypothesis: 'A method Block beside the design Board (as insight''s Prototype): one
    Job per method version with five Tasks (write the recipe, build its checks, bench
    it on fixed goals and inputs, compare it with another agent, release it with a
    person''s sign); a Board Job pins a released version by path and hash; Board results
    and Exp scores file proposals into the method Block''s backlog. The generic method
    stays in the Tools skill; an app''s version moves to the Project.'
  acceptance: Answered when s05-design-method-ladder is agreed, the method Block is
    scaffolded by haipipe-design, and one real version (M05 m3) is carried onto it with
    its five Tasks and shown in the Block's Methods view.
  work: []
  report: reports/q06_design_method_ladder/q06_design_method_ladder.md
```

## Blueprint home

This Theme is an independent blueprint Block under `blueprints/Project-Ladder/work/b12_theme_design/`
since 261010. Its studio topics, questions, reports and Runs keep their existing
identities. Shared toolkit foundations remain in [b01](../../../Project-Packages/work/b01_haipipe-toolkit/board.md).
