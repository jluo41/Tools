# Pane speed
state: 🔴 OPEN
goal: the side pane and its Block page load fast: Files panel under 1 s, the page under 1.5 s and 1.2 MB, no style or script sent twice
close: never while the side pane lives; each check round is one dated pass of runs/run-check-pane-speed
owner: JL
folder-kind: task
task-type:
task: .

## Files

`scripts/bench_pane.py`: times the Files panel and the Block page on a running workbench (median and first request), counts the page's size and its repeated style and script blocks, and lists the five slowest workbench functions while the panel renders. It exits 1 when a row passes a limit. The code it measures is t01's (`side_pane/files_tree/`) and the page around it.

## Checks

1. Bench: `PYTHONPATH=plugins/haipipe-toolkit/servers/_host <host venv python> examples/Project-Ladder/blueprint/b17_theme_work/j12_side_pane/t03_pane_speed/scripts/bench_pane.py --base <the 5623 address>` on a freshly restarted 5623; no ❗ row
2. Hot spots: the five slowest functions it prints; any one over 0.3 s gets a reason in the pass
3. Browser: open b17's Block UI view in Chrome, open Elements › Work Block, click a left tab; the page answers within 2 s
4. Each round's numbers go into a pass, so the next round can see what got slower
