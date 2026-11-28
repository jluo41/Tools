# Element marks
state: 🔴 OPEN
goal: every element carries its info, comments and 🙋 mark, gathered in the page's 🙋 tray
close: never while its folder lives; each check round is one dated pass of runs/run-check-element-marks
owner: JL
folder-kind: task
task-type:
task: .

## Files

`plugins/haipipe-toolkit/servers/workbench/page/element_marks/` and the 🙋 tray part of `focus-assets/`: every file in it is this Task's; a new file for this part goes there.

## Checks

1. Tests: its own `servers/workbench/page/element_marks/tests/` first; then the 9 test files that import this folder's modules, in `workbench-paper/tests`, through uv with `PYTHONPATH=_host`
2. Size: no file in the folder passes 700 lines (AGENTS.md § Keep files short)
3. `page_words.py --running`: the 🙋 tray and marks
4. Live: restart every server on this code (5623, 5602, 5607, 5599) and open a page that uses the folder
