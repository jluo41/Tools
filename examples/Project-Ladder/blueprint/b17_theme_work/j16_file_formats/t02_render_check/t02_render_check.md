# Render check
state: 🔴 OPEN
goal: a script renders every real file of each kind in t01's table through the page code that reads it, and reports each one that errors, comes back empty, or loses a field
close: never while the workbench draws these files; each round is one dated pass of runs/run-check-render
owner: JL
folder-kind: task
task-type:
task: .

## Files

`plugins/haipipe-toolkit/servers/workbench/checks/`: `render_check.py` renders every file of each kind in the format table (`delivery/page-spec/file-formats.md`) through its page code, in process; one line per problem, exit 1 on any. Its test, `checks/tests/test_render_check.py`, keeps the script's kinds equal to the table's.

Run: `PYTHONPATH=plugins/haipipe-toolkit/servers/_host <host venv python> plugins/haipipe-toolkit/servers/workbench/checks/render_check.py [examples/<sub>]`

## Checks

1. The script runs over every kind and every file of it, under 60 s
2. No file errors or renders empty; each field the table names shows on the page
3. A format change (a field added or renamed) is followed by a run of this check
