# Run views
state: 🔴 OPEN
goal: the Runs tab: a Page's Runs, their cards, receipts and results
close: never while its folder lives; each check round is one dated pass of runs/run-check-run-views
owner: JL
folder-kind: task
task-type:
task: .

## Files

`plugins/haipipe-toolkit/servers/workbench/workbench-task-draft/run_views/`: every file in it is this Task's; a new file for this part goes there.

## Checks

1. Tests: the test files that import this folder's modules, in `workbench/workbench-task-draft/reader/tests`, `workbench-paper/tests`, `_host/tests` and `skills/1_base/draft/hai-draft/tests`, and the workbench Tasks' own `tests/` folders, through uv with `PYTHONPATH=_host`
2. Size: no file in the folder passes 700 lines (AGENTS.md § Keep files short)
3. Live: restart every server on this code (5623, 5602, 5607, 5599) and open a page that uses the folder
