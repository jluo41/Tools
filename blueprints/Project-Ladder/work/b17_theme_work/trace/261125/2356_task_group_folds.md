---
title: task group folds
date: 2026-11-25 23:56
topic: s11-work-job-preview
aim: A Job's 📊 Tasks band draws one fold per Task group, named by the Job face's `bands:` line (t0N Page components), as a Block draws its Job bands; a Job with no `bands:` keeps one fold named Tasks; the s11 preview does the same.
closed: true
plan:
  - do: add
    path: blueprints/Project-Ladder/work/b17_theme_work/trace/261125/2356_task_group_folds.md
    what: this trace's own record, written first
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_plan_results.py
    what: tasks_section returns one fold per tNN decade, named by the face's bands line
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/block_index_page/tests/test_focus_status_map.py
    what: Tasks split into named group folds; no bands line keeps one Tasks fold
  - do: edit
    path: blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/delivery/ui/job-view-topics.html
    what: Main's Tasks band draws one fold per Task group
changed:
  - blueprints/Project-Ladder/work/b17_theme_work/trace/261125/2356_task_group_folds.md
  - plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_plan_results.py
  - plugins/haipipe-toolkit/servers/workbench/page/block_index_page/tests/test_focus_status_map.py
  - blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/delivery/ui/job-view-topics.html
---

# task group folds

## Prompts

- **23:50** [Image] I think each fold here should be the things like the Task group name, right? How do you think?
- **23:55** yes, I think that should be, please go ahead and update it.

## Check

- workbench tests: 297 passed; 6 failed, all in the reader's tests (the /private path issue, not this change)
- 5623 restarted; j11 Main shows 1 · 🧱 Page components (its face's bands line), opened t01 to t05 under it; s11 preview the same

## Summary

A Job's 📊 Tasks band now draws one fold per Task group (tNN decade), named by the Job face's `bands:` line, as a Block draws its Job bands; with no `bands:` line it keeps one fold named Tasks. The bar's mark keeps the old rule (the Task faces' states, per group).
