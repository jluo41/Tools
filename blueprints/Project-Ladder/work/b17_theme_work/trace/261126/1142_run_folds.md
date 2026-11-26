---
title: run folds
date: 2026-11-26 11:42
work: [j11t02, s11]
aim: "In a Job's Task fold each Run is a fold of its rounds: the newest Run open, older ones closed; the arrow folds it, its name opens the Run page; a Run with no round stays one row."
closed: true
plan:
  - do: add
    path: blueprints/Project-Ladder/work/b17_theme_work/trace/261126/1142_run_folds.md
    what: this trace's own record, written first
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_plan_results.py
    what: a Task's rounds grouped under its Run as a details fold, the first open
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/tests/test_open_rounds.py
    what: two Runs, two folds, the newest open
  - do: add
    path: blueprints/Project-Ladder/work/b01_example_work/j11_core_checks/t01_schema_check/runs/run-check-01-name/
    what: a second Run on t01 by soft_run.py, so the example shows more than one Run
changed:
  - blueprints/Project-Ladder/work/b17_theme_work/trace/261126/1142_run_folds.md
  - plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_plan_results.py
  - plugins/haipipe-toolkit/servers/workbench/page/job_task_views/tests/test_open_rounds.py
  - blueprints/Project-Ladder/work/b01_example_work/j11_core_checks/t01_schema_check/runs/run-check-01-name/
---

# run folds

## Prompts

- **11:41** [Image #27] so why the run here cannot be collapsed? what if I have mutiple runs?

## Check

- Runs ordered by their newest round, not by name: run-check-02-name (1125) before run-check-01-name (1110), the first open.
- Chrome, b01_example_work Jobs, j11 › t01: two Run folds, the first open with its two rounds; a click on the second's arrow opened it, its round "an earlier check" showing; a Run's name still opens the Run page.
- test_open_rounds.py (now with two Runs) and test_focus_status_map.py: 16 passed; workbench as before (the reader's known 6 fail).
- 5623, 5602, 5607, 5599 restarted, 200.

## Summary

Each Run in a Task fold is now a fold of its rounds, the one with the newest round first and open; the example's t01 has two Runs to show it.
