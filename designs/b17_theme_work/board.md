# b17 · Theme: work

board-kind: task-block
spine: Design questions about the work Theme as one ladder: what a task Block, a work Job, a work Task and a hard Run each hold and show, how Plan, Build, Execute and Report map onto the six Spaces, and how a Question's report reads its Tasks' Runs.
close: Each recorded question has a report Page with an answer status, and every answered question names the skill, workbench or builder change that settled it.

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

Excluded: the ladder itself and what every Theme shares (b03_project_workbench); the stage pipelines a
Task runs (haipipe-data, -nn, -end).

## Pipeline

```text
chat section -> Related question -> haipipe-question -> skill, workbench or builder change -> report Page
                                                     -> studio/ drawings (shared by the questions)
```

## Pages

No Jobs yet. The shared drawing is `studio/s01-work-ladder/s01-work-ladder.excalidraw`:
every work row, Block to Run, proposed and today. It is drawn from b03's shared definitions
(`b03_project_workbench/studio/s01-overall-tree-structure/`) by `b03_project_workbench/studio/_build/theme_ladder.py`
and rebuilt by b03's `studio/_build/make.sh`.

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
