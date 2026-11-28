# Shared parts and file map
state: 🔴 OPEN
goal: the shared page parts and the file map: a check that every servers/workbench file has one owning Task
close: never while its folder lives; each check round is one dated pass of runs/run-check-parts-and-map
owner: JL
folder-kind: task
task-type:
task: .

## Files

`plugins/haipipe-toolkit/servers/workbench/page/parts_and_map/`, plus `ref/`, `README.md`, `assets/`, `related/` and `removal/`: every file in it is this Task's; a new file for this part goes there.

## Checks

1. Tests: its own `servers/workbench/page/parts_and_map/tests/` first; then the 11 test files that import this folder's modules, in `_host/tests`, `workbench-paper/tests`, through uv with `PYTHONPATH=_host`
2. Size: no file in the folder passes 700 lines (AGENTS.md § Keep files short)
3. `page_words.py --running` (A01 to A03 page words)
4. Live: restart every server on this code (5623, 5602, 5607, 5599) and open a page that uses the folder
