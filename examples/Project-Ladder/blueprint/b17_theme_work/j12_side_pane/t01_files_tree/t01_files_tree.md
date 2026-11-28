# Files tree
state: 🔴 OPEN
goal: the Files tree in the side pane: the scope's own folders highlighted, the rest faded
close: never while its folder lives; each check round is one dated pass of runs/run-check-files-tree
owner: JL
folder-kind: task
task-type:
task: .

## Files

`plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/` and the side pane part of `focus-assets/`: every file in it is this Task's; a new file for this part goes there.

## Checks

1. Tests: its own `servers/workbench/side_pane/files_tree/tests/` , through uv with `PYTHONPATH=_host`
2. Size: no file in the folder passes 700 lines (AGENTS.md § Keep files short)
3. `folder_icons_check.py` (A05 icon table, A06 real folders, A07 traces)
4. Live: restart every server on this code (5623, 5602, 5607, 5599) and open a page that uses the folder
5. Speed: t03_pane_speed's bench passes (`../t03_pane_speed/scripts/bench_pane.py`, no ❗ row)
