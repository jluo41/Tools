# Evidence steps
state: 🔴 OPEN
goal: the Evidence step: evidence items, their cards, cite items, displays and values
close: never while its folder lives; each check round is one dated pass of runs/run-check-evidence-steps
owner: JL
folder-kind: task
task-type:
task: .

## Files

`plugins/haipipe-toolkit/servers/workbench/workbench-task-draft/evidence_steps/`: every file in it is this Task's; a new file for this part goes there.

## Checks

1. Tests: its own `servers/workbench/workbench-task-draft/evidence_steps/tests/` first; then the test files that import this folder's modules, in `workbench/workbench-task-draft/reader/tests`, `workbench-paper/tests`, `_host/tests` and `skills/1_base/draft/hai-draft/tests`, through uv with `PYTHONPATH=_host`
2. Size: no file in the folder passes 700 lines (AGENTS.md § Keep files short)
3. Live: restart every server on this code (5623, 5602, 5607, 5599) and open a page that uses the folder
