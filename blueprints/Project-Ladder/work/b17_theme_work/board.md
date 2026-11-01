# b17 · Theme: work

board-kind: task-block
package: plugins/haipipe-toolkit
theme: work
ui-block: http://100.121.165.84:5599/_board/workbench?layout=focus&path=examples-2-cms/Project-Personality-OpioidRx/work/b11_CD_visit_pain_lbp
ui-job: http://100.121.165.84:5599/_board/workbench?layout=focus&path=examples-2-cms/Project-Personality-OpioidRx/work/b11_CD_visit_pain_lbp/j21_D_reg_VisitLBP_1stPair_yr16_19_bigfive_ols
ui-task: http://100.121.165.84:5599/_board/workbench?layout=focus&path=examples-2-cms/Project-Personality-OpioidRx/work/b11_CD_visit_pain_lbp/j21_D_reg_VisitLBP_1stPair_yr16_19_bigfive_ols/t01_C1_D_reg_VisitLBP_agre
shared-blueprint: b01_haipipe-toolkit
spine: Design the work theme: its three pages (a Block, a Job and a Task, each with Report, Work and Studio), what every page shares, and its two skills, haipipe-work and workbench-work, which say what each level holds.
close: Every sNN is agreed and its delivery made: the two skills rewritten in skills/2_theme/work/ and the screens named for the focus page's owner.
session: Ladder-b17-Work-v1031

## Topic

The work Theme runs bounded execution work: a Task plans, builds, executes and reports, and
each Run is one hard ticket (`rNN_<noun>_<qualifier>.sh`) with its Result and receipt. Its Block
is a task Block (`tasks/bNN_<topic>/`), a Job groups Tasks by series (j0N, j1N, j5N), and a
Block's Questions are answered by report Pages that read the Tasks' Runs.

Today the Task workbench shows it at Block level in four Spaces (Scope · Task · Check ·
Delivery): the Question groups are Views of Task. Its server is moving to
`servers/workbench-work` and its skills to `2_theme/work/` (in progress, 261007).

The shared ladder (b03) gives every level the same six Spaces: Description · Idea Studio ·
Audience Report | Work Details | Runs · Delivery. This Block asks how work fits that ladder level
by level, and what it needs that no other Theme has.

Most answers here are a change to the work skills (`2_theme/work/` (being set up), the work Task skills in `1_base/task`, the server `servers/workbench-work`), the Work workbench
server, or b03's shared builder, not a Task Run. A Question may have no work entries; its report
links the changed files and the drawings.

Excluded: the ladder itself and what every Theme shares (b10_project_workbench); the stage pipelines a
Task runs (haipipe-data, -nn, -end).

## Pipeline

```text
chat section -> Related question -> haipipe-report -> skill, workbench or builder change -> report Page
                                                     -> sNN drawings beside their Jobs (shared by the questions)
```

## Deliveries

One sNN, one idea, one delivery of one type (b35 s01-D02; JL 261031, agreed the b17 plan); each sNN sits beside the
Job that makes its delivery:

- s01 · skill: a deck, and haipipe-work's SKILL.md, rewritten to today's work ladder (made by `j01_work_ladder_contract/`)
- s02 · skill: a deck, and workbench-work's SKILL.md and ref/workbench-table.md, rewritten for the three work pages
  (made by `j02_workbench_work_skill/`)
- s04 · ui: a deck, and the parts every work page shares: the frame, Interactions, Delivery, Related, Timeline and
  Files (made by `j03_work_workbench_pages/t04_shared_parts/`)
- s51 to s59 · ui: one screen each, the work Block, Job and Task × Report, Work and Studio, three sNN at each of
  j03's first three Tasks (JL 261031: as b16's 3 × 3)

Merged 261031 from five: s03 (today's workbench) and s32 (the element gallery) into s04, kept whole in its
`result/merged-*/`; their numbers are retired. The topics left `studio/` the same day. Rewritten the same evening (JL 261031: "I think many things in the studios are outdated, how could you try to update them accordingly"):
s01 and s02 now deliver the two work skills in `skills/2_theme/work/`, and s04 only what every page shares.

## Pages

[s01 · work ladder](s01-work-ladder/s01-work-ladder.md): haipipe-work's SKILL.md, rewritten to today's work ladder:
five rungs, a page for a Block, a Job and a Task, none for a Run or a Studio topic. Its older drawings stay in `result/`.

[s02 · work skills](s02-work-skills/s02-work-skills.md): workbench-work's SKILL.md and ref, rewritten for the three
work pages from j03's nine cells. The old skill-homes question stays in its `result/skill-homes-261031/`.

[s04 · Workbench page structure](s04-workbench-page-structure/s04-workbench-page-structure.md): the parts every
work page shares, the frame and the right rail's other sections. Its older discussion of page order and navigation,
in its `result/face-history-261031.md`, and its
[mind map](s04-workbench-page-structure/s04-workbench-page-structure.mindmap.md) and
[drawing](s04-workbench-page-structure/s04-workbench-page-structure.excalidraw) distinguish stated requirements,
proposals and open questions. The old s03 workbench reference is in
[result/merged-s03-work-workbench/](s04-workbench-page-structure/result/merged-s03-work-workbench/s03-work-workbench.md).

## Questions

```yaml
questions:
- id: Q01
  title: How does work climb the ladder?
  question: What do the task Block, a work Job, a work Task and a hard Run each hold
    and show on screen, and which of today's Scope, Task, Check and Delivery Views
    moves to which level?
  hypothesis: The Block keeps its Questions (Audience Report) and Job series (Work
    Details groups); a Job's Work Details = its Tasks; a Task's Runs are its tickets;
    a Question's report reads them.
  acceptance: Answered when every level names its folder and its six Spaces' content,
    drawn in studio/.
  work: []
  report: reports/q01_work_ladder/q01_work_ladder.md
- id: Q02
  title: Where do Plan, Build, Execute and Report show?
  question: 'How do a Task''s four phases appear in the six Spaces: Description, Work
    Details, Runs, Audience Report?'
  hypothesis: Plan is the Task's Description; Build and Execute are its Runs (by type);
    Report is its Audience Report; the phase state is a chip on the Task's row one
    level up.
  acceptance: Answered when each phase has one place and today's Task Work tree has
    a home.
  work: []
  report: reports/q02_plan_build_execute_report/q02_plan_build_execute_report.md
- id: Q03
  title: How does a Question read its Runs?
  question: How does a Block Question's report Page name and read the Tasks' Runs
    that answer it, and where does that link show?
  hypothesis: By exact Run identity in the report's Evidence; the Question's row in
    Audience Report links its Tasks; the Runs Space lists the Runs per Question.
  acceptance: Answered when the link is written both ways and drawn.
  work: []
  report: reports/q03_questions_and_runs/q03_questions_and_runs.md
- id: Q04
  title: Which skills make the work theme?
  question: Which of today's 1_base/task skills belong to the work theme (2_theme/work),
    which stay in base because every theme calls them, and what is the work theme's
    door?
  hypothesis: Base keeps haipipe-task (the Task folder and Plan, Build, Execute, Report
    contract other themes call) and haipipe-workflow (beside haipipe-run); work gets
    workbench-work, the task-for-* kinds and their agents; the stage pipelines stay
    out (this Block excludes them).
  acceptance: Answered when each skill in 1_base/task has a home JL agrees, drawn
    in studio/, and b04 has moved the files.
  work: []
  report: reports/q04_work_skills/q04_work_skills.md
```

## Related resources

```yaml
resources:
- title: haipipe-task skill (the Task door)
  url: https://github.com/jluo41/Tools/tree/main/plugins/haipipe-toolkit/skills/2_theme/../1_base/task
  questions:
  - Q01
  - Q02
  - Q03
- title: the work Theme folder (being set up)
  url: https://github.com/jluo41/Tools/tree/main/plugins/haipipe-toolkit/skills/2_theme/work
  questions:
  - Q01
  - Q02
  - Q03
```

## Blueprint home

This Theme is an independent blueprint Block under `blueprints/Project-Ladder/work/b17_theme_work/`
since 261010. Its studio topics, questions, reports and Runs keep their existing
identities. Shared toolkit foundations remain in [b01](../../../Project-Packages/work/b01_haipipe-toolkit/board.md).

## Earlier purpose (until 261031)

- spine: Design questions about the work Theme as one ladder: what a task Block, a work Job, a work Task and a hard Run each hold and show, how Plan, Build, Execute and Report map onto the six Spaces, and how a Question's report reads its Tasks' Runs.
- close: Each recorded question has a report Page with an answer status, and every answered question names the skill, workbench or builder change that settled it.
