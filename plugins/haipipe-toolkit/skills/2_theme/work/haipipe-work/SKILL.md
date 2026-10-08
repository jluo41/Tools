---
name: haipipe-work
description: >-
  The door of the work theme: bounded execution work in a Project's tasks/
  world, where a Block (tasks/bNN_<topic>/) groups Jobs (jNN_<series>/), each
  Task (tNN_<task>/) plans, builds, executes and reports, and each hard Run
  (rNN_<noun>_<qualifier>.sh) leaves a Result and a receipt that the Block's
  Question reports read. Routes a request to the skill that owns it: the Task
  folder and its Plan, Build, Execute, Report contract (haipipe-task), the work
  workbench (workbench-work), a kind of work Task (haipipe-task-for-<kind>), a
  Run graph (haipipe-workflow), a Block Question (haipipe-question). Owns no
  folder contract of its own yet. Trigger: work theme, work Block, work Job,
  which work skill, where does this work go, /haipipe-work.
metadata:
  version: "0.1.0"
  last_updated: "2026-10-07"
---

# Work theme

The work theme runs bounded execution work: code, data, models, calculations.
It is one of the themes in `skills/2_theme/` (beside cowork, design, discovery,
insight, labeling and paper) and is served by `servers/workbench-work`. It was
called the task theme until 2026-10-07; the Task as a ladder level (Block ->
Job -> Task -> Run) belongs to every theme and keeps its name.

```text
tasks/bNN_<topic>/                    a work Block: board.md, Questions, reports/, studio/
└── jNN_<series>/                     a Job: one series of Tasks (j0N, j1N, j5N ...)
    └── tNN_<task>/                   a work Task: Plan -> Build -> Execute -> Report
        ├── runs/rNN_<noun>_<qualifier>.sh     a hard Run (one ticket)
        └── results/rNN_<noun>_<qualifier>/    its Result and runtime receipt
```


Route
-----

| You want to | Skill | Where |
|---|---|---|
| create, run, audit or close a Task folder; Plan, Build, Execute, Report; read a Run's Result | `haipipe-task` | `1_base/task/` (base: other themes call it too) |
| open or read the work Block on screen (Scope, Task, Check, Delivery, Runs panel) | `workbench-work` | `2_theme/work/` |
| a Task of one kind | `haipipe-task-for-<kind>`: data, raw, description, algo, fit, eval, endpoint, individual, display, stata, agent, page | `1_base/task/<N>_<kind>/` |
| plan a Run graph: Run Specs, dependencies, gates, routes | `haipipe-workflow` | `1_base/task/` |
| a Block Question, its register and its report folder | `haipipe-question` | `1_base/question/` |
| write a Question's report Page | `haipipe-page` | `1_base/page/` |
| the stage pipelines a Task runs (data, nn, end, individual) | `haipipe-data`, `haipipe-nn`, `haipipe-end`, `haipipe-individual` | `1_base/task/<N>_<stage>/`; not part of the theme |

Name the skill you route to before acting; never perform its work here.


Boundary
--------

- This door owns no folder contract and no scaffold yet. Until the work theme's
  Block, Job and Task contract is written, `haipipe-task` owns the Task folder,
  its tickets and its receipts.
- Which `1_base/task` skills move into this theme (the kinds, the task agents,
  `haipipe-page-task`) is still open; the table above names where each one is
  today.
- The ladder itself (what every level holds and its six Spaces) is shared by
  every theme and owned by `haipipe-project`.
