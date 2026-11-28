---
session: null
provider: claude
date: '2026-11-25'
goal: first check round
paths: []
cards: []
---

# first check round

## Ask

run the Task's ## Checks after the page/ split

## Summary

tests (8 files): _host/tests: 22 passed, 138 subtests passed; workbench-paper/tests: 8 passed, 6 subtests passed; workbench/tests: 48 passed; workbench/workbench-task-draft/reader/tests: 2 errors. size: 19 files, largest 541 lines (work_frame.py), none over 700. reader/tests put page/ on sys.path for runs_panel.py; fixed to page/job_task_views in test_runs_panel.py, test_run_family_lists.py, test_space_views.py (now pass); test_standalone_server.py's 5 failures are the same at HEAD (j13t03's). live: 5623 restarted and serving; 5602, 5607 and 5599 still run the code from before the move (5602's log: No module named 'live.work_sections'), and their restart waits on JL.

## Changed

<nothing>
