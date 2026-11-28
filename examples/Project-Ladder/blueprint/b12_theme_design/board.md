# b12 · Theme: design

board-kind: task-block
package: plugins/haipipe-toolkit
theme: design
examples: design/Design-Example, design/DesignMethodBook-Example
bands: j0N 🗄️ Earlier design · s0N 🧱 Block Structure · s1N 👀 Block Job UI Preview
ui-block: examples/Project-Ladder/design/Design-Example
ui-block: examples/Project-Ladder/design/DesignMethodBook-Example
ui-job: examples/Project-Ladder/design/Design-Example/j03_confirm-by-reply_M02-overall-performance-m1_inputs-v2
ui-job: examples/Project-Ladder/design/Design-Example/j01_confirm-by-reply_M01-goal-only-m2_inputs-v1
ui-job: examples/Project-Ladder/design/Design-Example/j02_confirm-by-reply_M01-goal-only-m2_inputs-v2
ui-job: examples/Project-Ladder/design/DesignMethodBook-Example/j02_M02-overall-performance
ui-task: examples/Project-Ladder/design/Design-Example/j03_confirm-by-reply_M02-overall-performance-m1_inputs-v2/t00_reason-ideas
ui-task: examples/Project-Ladder/design/Design-Example/j03_confirm-by-reply_M02-overall-performance-m1_inputs-v2/t02_d02_reminder-one-ask
ui-task: examples/Project-Ladder/design/Design-Example/j03_confirm-by-reply_M02-overall-performance-m1_inputs-v2/t99_review-whole
shared-blueprint: b01_haipipe-toolkit
spine: How the design theme sits on the Block → Job → Task → Run ladder and shows in its workbench: a design Board for one application, a Job for one goal done by one design method returning N designs, a Task for one design, and the Runs that commission, generate, verify and revise them; how an insight Block steers a design through one handoff; and which skill and workbench owns each part.
close: Each recorded question has a report Page with an answer status; the drawings in studio/ match the shared definitions in b10_project_workbench (removed 261126), and every open point is either decided or carried as a question.
session: Ladder-b12-Design-v1031

## Topic

The design theme makes N designs for one goal by one method, checks them, and releases the ones that
pass; running the experiment is outside it. This Block designs that theme's place on the ladder:

```text
design/Design-<name>/             Block: one application, one channel; goals signed, inputs versions, Exp results
└── jNN_<goal>_M0x-<slug>-mK_inputs-vM/           Job: goal G01 × method M04 m2 × inputs inputs-v2 → N designs; inputs/ is its fence
    ├── inputs/                    goal.md · method.md (the pinned version) · manifest.yaml
    ├── t00_reason-ideas/          ② reason ideas        run-reason-t00
    ├── tNN_d<NN>_<slug>/          ③ ④ one design        run-generate-d<NN> · run-verify-d<NN>-v<k> · run-revise-d<NN>
    └── t99_review-whole/          ⑤ review whole        run-rank-t99
```

A design method turns a goal and its inputs into N designs in five steps (① See input · ② Reason ideas ·
③ Conduct process · ④ Review item · ⑤ Review whole); it is registered and versioned in
`hai-design-method`, and a Job pins one version. The 13 kinds of method are the Guide's
(`plugins/haipipe-toolkit/servers/workbench-design/guide/method.md`). The folder contract is
`hai-design/ref/design-ladder.md`.

The trees, skills and screens are defined once with every other theme's, in
`b10_project_workbench/s01-overall-tree-structure/ (removed 261126)` (`build_ladder_v4.py`, `level_views.py`); this
Block's drawings gather the design rows from there. Its sibling is `../b11_theme_insight/`, the theme
that steers a design.

Its Studio topics sit directly in the Block, in two bands as b17's (261127): one structure topic per
kind of design Block, and one Job UI preview per kind of Job, live over the examples under
`examples/Project-Ladder/design/`. b12 is itself a blueprint Block; its own Jobs follow b17's s02 and s14.
The older topics are in `_archive/20261127/`.

```text
b12_theme_design/
├── j01_design_workbench_pages/      🗄️ Earlier design: the 3 × 3 pages, s51 to s59 (below, ## Pages)
├── s01-design/                      🧱 Design Board Structure
├── s02-workbench-ui/                🧱 Design Method Book Structure
├── s11-design-job-preview/          👀 Design Job UI preview, over Design-Example
├── s12-methodbook-job-preview/      👀 Method Book Job UI preview, over DesignMethodBook-Example
└── _archive/20261127/               s03-s06, s11-s13, s21, s31-s33, s61 and s01's first drawing
```

Excluded: making real designs (that is a design Board's own work, under a Project), and the ladder
shared by every theme (`b10_project_workbench/ (removed 261126)`).

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
    drawn in s11-design-block, s12-design-job and s13-design-task (now in _archive/20261127/), and method-folders.md
    agrees or is changed.
  work: []
  report: s01-design/s01-design.md
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
  report: s01-design/s01-design.md
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
  report: s01-design/s01-design.md
- id: Q04
  title: How does one design round feed the next?
  question: 'How does a design Block keep its memory across rounds: what an Exp returns,
    how it reaches the next inputs version, and how the workbench shows the rounds?'
  hypothesis: 'One round per inputs version. An Exp returns per-arm totals once, at
    the Block (observed/eNN), scored against the frozen predictions; the next inputs
    version holds them with the insight Board newer data version, and its Jobs pin
    it (moved: inputs). Audience Report › Rounds strings the rounds in time order.'
  acceptance: Answered when the SMSR2 design Block closes one round (observed e01
    scored) and starts inputs-v2, and Rounds shows both.
  work: []
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
  report: _archive/20261127/s06-design-workflow/s06-design-workflow.md
- id: Q06
  title: Where is a design method made and tried?
  question: Where on the ladder is a design method version written, tested and compared
    before a design Job pins it, and how do the Board's results come back as its next
    version?
  hypothesis: 'A Method Book (design/DesignMethodBook-<app>/) beside the design Board (as insight''s Question Book): one
    Job per method version with five Tasks (write the recipe, build its checks, bench
    it on fixed goals and inputs, compare it with another agent, release it with a
    person''s sign); a Board Job pins a released version by path and hash; Board results
    and Exp scores file proposals into the method Block''s backlog. The generic method
    stays in the Tools skill; an app''s version moves to the Project.'
  acceptance: Answered when s02-workbench-ui (formerly s05-design-method-ladder) is agreed, the method Block is
    scaffolded by hai-design, and one real version (M05 m3) is carried onto it with
    its five Tasks and shown in the Block's Methods view.
  work: []
  report: s02-workbench-ui/s02-workbench-ui.md
```

## Blueprint home

This Theme is an independent blueprint Block under `examples/Project-Ladder/blueprint/b12_theme_design/`
since 261010. Its studio topics, questions, reports and Runs keep their existing
identities. Shared toolkit foundations remain in [b01](../../../Project-Packages/work/b01_haipipe-toolkit/board.md).

## Current Block frame · 2026-11-08

The Design Board now combines content and actions in Report, under Review Content followed by the shared Around the Work sections. Summary, Goals, Jobs, Rounds, Methods and MindMap remain the business views. The previous Report/Work split above is historical for the Block; Job and Task pages retain their specialist workflow. The current Block specification is `examples/Project-Ladder/blueprint/b12_theme_design/delivery/page-spec/structure.md`, with the section matrix in `delivery/page-spec/block-views.md` and routed examples in `delivery/page-spec/view-guide.json`. Historical drawings have not been redrawn. Human approval of release is unchanged.


## Structure Studios

The current type inventory is Design Board (`design-board`) and Design Method Book
(`design-method-book`). Their structure Studios are [s01](s01-design/s01-design.md) and
[s02](s02-workbench-ui/s02-workbench-ui.md). Each uses Structure / Draw / Examples / Skills
through the shared Studio manifest. The Draw uses generic names; Examples embeds the actual
Block. Skills stays inside its owning Studio. Earlier diagrams and hypotheses remain as history;
the Method Book currently owns method-type Jobs and signed versions, without execution Tasks.
