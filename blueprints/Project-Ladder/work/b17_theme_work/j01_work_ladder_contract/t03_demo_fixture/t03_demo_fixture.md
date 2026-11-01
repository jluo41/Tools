# t03 · Test haipipe-work with a fresh agent
state: 🔴 OPEN
goal: a fresh agent given only haipipe-work routes each request
close: on a demo work Block in a temp folder (placeholders only, never real project data), the agent picked the skill each route names without being told and stopped where a person decides, and the demo Block passes ladder.py audit with no debt or failure
task-type: tool

Part of j01 · Make s01's delivery (its sNN's Process). Its Runs are soft (agent work, one pass each), in `runs/`.
run-check-demo-block

It runs after t01, in a context that wrote nothing of the SKILL.md (Tools' README: a changed skill is validated from
a fresh context, its process watched, not only its output). A wrong route goes back to t01's Run as a new pass.

Re-aimed on 2026-10-31: it tested the work scaffold (t02, now in `../_old/`). Before it was: goal "the scaffold is
tested on a demo Block in a temp folder, placeholders only, never real project data", close "the demo Block passes
check_task_tree and opens in the workbench". The folder and its Run keep their names: the demo Block stays.
