# Guide
state: 🔴 OPEN
goal: the Guide pages of every theme
close: never while its folder lives; each check round is one dated pass of runs/run-check-guide
owner: JL
folder-kind: task
task-type:
task: .

## Files

Under `plugins/haipipe-toolkit/servers/workbench/`: guide/

## Checks

1. Tests: its own `servers/workbench/guide/tests/` first; then the 3 test files that import this folder's modules, in `_host/tests`, `workbench-design/tests`, through uv with `PYTHONPATH=_host`
2. Size: no file in the folder passes 700 lines (AGENTS.md § Keep files short)
3. Live: restart every server on this code (5623, 5602, 5607, 5599) and open a page that uses the folder
