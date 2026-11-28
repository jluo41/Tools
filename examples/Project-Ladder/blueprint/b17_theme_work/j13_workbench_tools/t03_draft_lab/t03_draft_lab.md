# Draft Lab
state: ⏸️ SUPERSEDED by j14_draft_lab
goal: the Draft Task page
close: closed 261125: workbench-task-draft/ split into module folders, each a Task of j14_draft_lab
owner: JL
folder-kind: task
task-type:
task: .

## Files

Under `plugins/haipipe-toolkit/servers/workbench/`: workbench-task-draft/

## Checks

1. Tests: the 27 test files that import this folder's modules, in `_host/tests`, `workbench-paper/tests`, `workbench-work/tests`, `workbench/workbench-task-draft/exporters`, `workbench/workbench-task-draft/reader/tests`, and the workbench Tasks' own `tests/` folders, through uv with `PYTHONPATH=_host`
2. Size: no file in the folder passes 700 lines (AGENTS.md § Keep files short)
3. Live: restart every server on this code (5623, 5602, 5607, 5599) and open a page that uses the folder
