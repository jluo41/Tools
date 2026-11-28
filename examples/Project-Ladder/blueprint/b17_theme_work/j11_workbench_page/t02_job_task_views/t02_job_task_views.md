# Job and Task views
state: 🔴 OPEN
goal: a Job is a view on the Block page, with Main and one view per Task, each Task its bands and folds
close: never while its folder lives; each check round is one dated pass of runs/run-check-job-task-views
owner: JL
folder-kind: task
task-type:
task: .

## Files

`plugins/haipipe-toolkit/servers/workbench/page/job_task_views/`: every file in it is this Task's; a new file for this part goes there.

## Checks

1. Tests: its own `servers/workbench/page/job_task_views/tests/` first; then the 8 test files that import this folder's modules, in `_host/tests`, `workbench-paper/tests`, `workbench/workbench-task-draft/reader/tests`, through uv with `PYTHONPATH=_host`
2. Size: no file in the folder passes 700 lines (AGENTS.md § Keep files short)
3. Live: restart every server on this code (5623, 5602, 5607, 5599) and open a page that uses the folder
