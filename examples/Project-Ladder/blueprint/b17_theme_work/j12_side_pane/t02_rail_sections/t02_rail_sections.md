# Rail sections
state: 🔴 OPEN
goal: the rail sections opened in the side pane from the round menu
close: never while its folder lives; each check round is one dated pass of runs/run-check-rail-sections
owner: JL
folder-kind: task
task-type:
task: .

## Files

`plugins/haipipe-toolkit/servers/workbench/side_pane/rail_sections/`: every file in it is this Task's; a new file for this part goes there.

## Checks

1. Tests: its own `servers/workbench/side_pane/rail_sections/tests/` first; then the 4 test files that import this folder's modules, in `workbench-design/tests`, `workbench-paper/tests`, through uv with `PYTHONPATH=_host`
2. Size: no file in the folder passes 700 lines (AGENTS.md § Keep files short)
3. Live: restart every server on this code (5623, 5602, 5607, 5599) and open a page that uses the folder
