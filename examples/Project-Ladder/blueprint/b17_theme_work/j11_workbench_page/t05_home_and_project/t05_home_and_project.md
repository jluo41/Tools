# Home and Project pages
state: 🔴 OPEN
goal: the SPACE Home and Project pages above the Block
close: never while its folder lives; each check round is one dated pass of runs/run-check-home-and-project
owner: JL
folder-kind: task
task-type:
task: .

## Files

`plugins/haipipe-toolkit/servers/workbench/home/`: every file in it is this Task's; a new file for this part goes there.

## Checks

1. Tests: its own `servers/workbench/home/tests/` first; then the 6 test files that import this folder's modules, in `_host/tests`, `workbench-work/tests`, through uv with `PYTHONPATH=_host`
2. Size: no file in the folder passes 700 lines (AGENTS.md § Keep files short)
3. Live: restart every server on this code (5623, 5602, 5607, 5599) and open a page that uses the folder
