Task Workbench Table
====================

Shape and check: `skills/0_utils/table-workbench/SKILL.md`. One Task Block is one
workbench (`/w/<block>`). Rows run input → process → output: Scope states the
Block and its Questions, Task does the work and writes the answers, Check reads
what was run and judges the reports. Folder is where the run writes: `Block ›` is
the Block folder (`tasks/bNN_<block>/`), `Tools ›` the workbench's own `ref/`;
`none` writes no file, only a verdict.

Agents: `haipipe-task-creator-agent` makes a Task (plan, build, report of a Run);
`haipipe-task-reviewer-agent` judges each gate and never reviews its own work; it is
read-only and returns its review, which the orchestrator saves. `haipipe-task-orchestrator-agent`
runs a Ticket. The Block-level writes (the Questions register, a report scaffold, a
drawing) need an agent of their own, planned as `haipipe-task-block-agent (new)`.
Reports are Pages: one agent plans, another writes, `haipipe-page-check-agent` checks.
`haipipe-task` routes and gates; it is no row's Skill: each row names the small skill
that does the work, `(new)` where it is still to be split out of `haipipe-task`.

| Level | Space | View | Run type | Agent | Skill | Person signs | Folder |
|---|---|---|---|---|---|---|---|
| board | Guide | Description | none | none | none | none | none |
| board | Guide | Method | none | none | none | none | none |
| board | Guide | RoadMap Draw | none | none | none | none | none |
| board | Guide | Related Paper | Add a paper | haipipe-discovery-orchestrator-agent | haipipe-discovery | the source check | Tools › haipipe-workbench-task/ref/task-papers.md |
| board | Scope | Block | none | none | none | none | none |
| board | Scope | Questions | Ask a Question | haipipe-task-block-agent (new) | haipipe-task-question (new) | the question | Block › board.md (Questions) · reports/qNN_<topic>/ |
| board | Scope | Questions | Review the questions | haipipe-task-reviewer-agent | haipipe-task-question (new) | a change | none |
| board | Scope | Resources | Add a resource | haipipe-task-block-agent (new) | haipipe-task-question (new) | none | Block › board.md (Related resources) |
| board | Task | Questions | Plan a Task | haipipe-task-creator-agent | haipipe-task-plan (new) | none | Block › jNN_<job>/tNN_<task>/workflow/plan.yaml · board.md (Questions › work) |
| board | Task | Questions | Review the plan | haipipe-task-reviewer-agent | haipipe-task-review (new) | none | none |
| board | Task | Questions | Build the Task | haipipe-task-creator-agent | haipipe-task-plan (new) | none | Block › jNN_<job>/tNN_<task>/scripts/ · runs/rNN_<run>.sh |
| board | Task | Questions | Review the Task code | haipipe-task-reviewer-agent | haipipe-task-review (new) | none | Block › CODE_REVIEW.md beside the code it reviews |
| board | Task | Questions | Run a Task | haipipe-task-orchestrator-agent | haipipe-task-run (new) | none | $OUTPUT_ROOT › tNN_<task>/results/rNN_<run>/ |
| board | Task | Questions | Report the Run | haipipe-task-creator-agent | haipipe-task-plan (new) | none | Block › jNN_<job>/tNN_<task>/workflow/report.yaml · RUN_AUDIT.md |
| board | Task | Questions | Plan the report | haipipe-page-structure-agent | haipipe-page-structure | none | Block › reports/qNN_<topic>/draft/ |
| board | Task | Questions | Write the report | haipipe-page-writing-agent | haipipe-page-writing | none | Block › reports/qNN_<topic>/ |
| board | Task | Studio | Draw | haipipe-task-block-agent (new) | haipipe-workbench-studio | none | Block › studio/<name>.excalidraw |
| board | Check | Runs | none | none | none | none | none |
| board | Check | Tasks | Check a Task | haipipe-task-reviewer-agent | haipipe-task-audit (new) | none | none |
| board | Check | Reports | Check a report | haipipe-page-check-agent | haipipe-page-check | none | Block › reports/qNN_<topic>/runs/ |

Notes
-----

- **Scope.** Block reads the spine and close condition in `board.md`. A Question is
  one main topic; its Logic (question, hypothesis, acceptance) is the person's to
  sign. "Review the questions" proposes keep, split or merge; a person signs a change.
- **Task.** Questions is the stacked cards (Logic │ Task Work │ Report). A Task's
  code is reviewed by a different agent before its Ticket runs; a Run's Result is
  written only by its Ticket. A report answers its Question from exact Results.
- **Check.** Runs reads every receipt's status (complete, running, failed); a
  running receipt is not a heartbeat. "Check a Task" checks a Task Folder against
  its contract; "Check a report" is the Page CHECK, by an agent that did not write it.
- **Make and judge apart.** Every judging row names a different agent from the row
  that made the thing it judges.
- **Folders.** `$OUTPUT_ROOT` is the Job folder when the Job serves itself, or its
  declared store; a Result's path keeps the `tNN_<task>/results/rNN_<run>/` shape either way.
  CODE_REVIEW.md sits beside the code it reviews (a Task's, or a Job's shared `src/`).
- **Guide › Method.** The method steps live in the `task` entry of
  `servers/workbench-shared/guide_families.py`; Method has no run.
- **Person signs.** Only what changes the Block's meaning: a Question and a change
  to it, and the source check of a paper.
