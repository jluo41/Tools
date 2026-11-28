# Block index page
state: 🔴 OPEN
goal: the Block page is the one index page: Main and its view buttons, bands, folds
close: never while its folder lives; each check round is one dated pass of runs/run-check-block-index-page
owner: JL
folder-kind: task
task-type:
task: .

## Files

`plugins/haipipe-toolkit/servers/workbench/page/block_index_page/` and the page shell part of `focus-assets/`: every file in it is this Task's; a new file for this part goes there.

## Checks

1. Tests: its own `servers/workbench/page/block_index_page/tests/` first; then the 46 test files that import this folder's modules, in `_host/tests`, `workbench-design/tests`, `workbench-insight/tests`, `workbench-labeling/tests`, `workbench-paper/tests`, `workbench-work/tests`, through uv with `PYTHONPATH=_host`
2. Size: no file in the folder passes 700 lines (AGENTS.md § Keep files short)
3. `page_words.py --running` (A01 to A03 page words)
4. Live: restart every server on this code (5623, 5602, 5607, 5599) and open a page that uses the folder
