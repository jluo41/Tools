Task Workbench Table
====================

Shape and check: `skills/0_utils/table-workbench/SKILL.md`. One Task Block is one
workbench (`/w/<block>`). Rows run input → process → output: Scope states the
Block, its Questions, its data and its drawings; Task does the work and writes the
answers, one View per register group; Check reads what was run and judges the reports;
Delivery holds the answered reports. Folder is where the run writes: `Block ›` is
the Block folder (`work/bNN_<block>/`), `Tools ›` the workbench's own `ref/`;
`none` writes no file, only a verdict.

Agents: `haipipe-task-creator-agent` makes a Task (plan, build, report of a Run);
`haipipe-task-reviewer-agent` judges each gate and never reviews its own work; it is
read-only and returns its review, which the orchestrator saves. `haipipe-task-orchestrator-agent`
runs a Ticket. The Block-level writes (the Questions register, a report scaffold, a
drawing) need an agent of their own, planned as `haipipe-task-block-agent (new)`.
Questions are asked and reviewed by the question skills in `skills/1_base/question/`
(`haipipe-question-asking`, `haipipe-question-review`), recorded by `haipipe-question`.
Reports are Pages: one agent plans, another writes, `haipipe-page-check-agent` checks.
`haipipe-task` routes and gates; it is no row's Skill: each row names the small skill
that does the work, `(new)` where it is still to be split out of `haipipe-task`.

| Level | Space | View | Run type | Agent | Skill | Person signs | Folder |
|---|---|---|---|---|---|---|---|
| board | Guide | Description | none | none | none | none | none |
| board | Guide | Method | none | none | none | none | none |
| board | Guide | RoadMap Draw | none | none | none | none | none |
| board | Guide | Related Paper | Add a paper | haipipe-discovery-orchestrator-agent | haipipe-discovery | the source check | Tools › servers/workbench-work/related/papers.md |
| board | Scope | Block | none | none | none | none | none |
| board | Scope | Questions | Ask a Question | haipipe-task-block-agent (new) | haipipe-question-asking | the question | Block › board.md (Questions) · reports/qNN_<topic>/ |
| board | Scope | Questions | Review the questions | haipipe-task-reviewer-agent | haipipe-question-review | a change | none |
| board | Scope | Resources | Add a resource | haipipe-task-block-agent (new) | haipipe-question | none | Block › board.md (Related resources) |
| board | Scope | RoadMap Draw | Draw the question map | haipipe-task-block-agent (new) | workbench-work | none | Block › studio/question-map.excalidraw |
| board | Scope | RoadMap Draw | Draw | haipipe-task-block-agent (new) | workbench-studio | none | Block › studio/<name>.excalidraw |
| board | Task | each group | Plan a Task | haipipe-task-creator-agent | haipipe-task-plan (new) | none | Block › jNN_<job>/tNN_<task>/workflow/plan.yaml · board.md (Questions › work) |
| board | Task | each group | Review the plan | haipipe-task-reviewer-agent | haipipe-task-review (new) | none | none |
| board | Task | each group | Build the Task | haipipe-task-creator-agent | haipipe-task-plan (new) | none | Block › jNN_<job>/tNN_<task>/scripts/ · runs/rNN_<run>.sh |
| board | Task | each group | Review the Task code | haipipe-task-reviewer-agent | haipipe-task-review (new) | none | Block › CODE_REVIEW.md beside the code it reviews |
| board | Task | each group | Run a Task | haipipe-task-orchestrator-agent | haipipe-task-run (new) | none | $OUTPUT_ROOT › tNN_<task>/results/rNN_<run>/ |
| board | Task | each group | Report the Run | haipipe-task-creator-agent | haipipe-task-plan (new) | none | Block › jNN_<job>/tNN_<task>/workflow/report.yaml · RUN_AUDIT.md |
| board | Task | each group | Plan the report | haipipe-page-structure-agent | haipipe-page-structure | none | Block › reports/qNN_<topic>/draft/ |
| board | Task | each group | Write the report | haipipe-page-writing-agent | haipipe-page-writing | none | Block › reports/qNN_<topic>/ |
| board | Check | Runs | none | none | none | none | none |
| board | Check | Tasks | Check a Task | haipipe-task-reviewer-agent | haipipe-task-audit (new) | none | none |
| board | Check | Reports | Check a report | haipipe-page-check-agent | haipipe-page-check | none | Block › reports/qNN_<topic>/runs/ |
| board | Delivery | Reports | Build the report | haipipe-page-writing-agent | haipipe-page-delivery | the release | Block › reports/qNN_<topic>/ (web, LaTeX, Word) |

Notes
-----

- **Scope.** Block reads the spine and close condition in `board.md`. A Question is
  one main topic; its Logic (question, hypothesis, acceptance) is the person's to
  sign. "Review the questions" proposes keep, split or merge; a person signs a change.
- **Scope.** RoadMap Draw holds the Block's drawings: first the question map, written only
  by `servers/workbench-work/question_map.py` from the register, then freeform ones.
- **Task.** One View per register `group:` (one, Questions, when there is none), each a
  table with a row per Question (Logic │ Task Work │ Report), as Insight's partition Views. A Task's
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
  `servers/workbench/guide_families.py`; Method has no run.
- **Delivery.** Reports lists every report whose `answer-status` is `answered`; building it
  as a web page, LaTeX and Word is the Page delivery run, and a person signs its release.
- **Person signs.** What changes the Block's meaning: a Question and a change to it, the
  source check of a paper, and a report's release.
