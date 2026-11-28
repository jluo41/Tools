---
title: overview one fold
date: 2026-11-27 00:10
work: [s11, j11t02]
aim: "A work Job's 🧭 Overview is one fold, the Job's name on its bar, with top views Goal · Requirements · MindMap (the s11 quick view overview-top-views JL picked); MindMap keeps its left tabs Topics and Work Structure. A Block's and a Task's Overview are unchanged."
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/0010_overview_one_fold.md
    what: this trace's own record, written first
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/work_frame.py
    what: overview() on a Job draws one fold with three top views (TOP_VIEWS css and a click script); other levels keep their folds
  - do: add
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/tests/test_job_main.py
    what: a Job's Overview is one fold with the three top views; a Block keeps its numbered folds
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/
    what: the face's Decision records the pick; overview-top-views fades (class old), the other three quick views and their buttons go
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261126/1225_job_main_content.md
    what: closed, its open pick answered here
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/0010_overview_one_fold.md
  - plugins/haipipe-toolkit/servers/workbench/page/job_task_views/work_frame.py
  - plugins/haipipe-toolkit/servers/workbench/page/job_task_views/tests/test_job_main.py
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/s11-work-job-preview.md
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/s11-work-job-preview.html
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/delivery/ui/ (overview-left-tabs, overview-brief-and-map, overview-goal-lead removed)
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261126/1225_job_main_content.md
---

# overview one fold

## Prompts

- **00:08** [Image #37] I think I prefer to have this one. How do you think? plaese do it. [Image #38] i want this style.

## Check

- work_frame.py is shared: another session's uncommitted view_asks() is kept; only overview() changed, and top_views() with TOP_VIEWS added below it (566 lines).
- 5623's b01_example_work Jobs, j11: 🧭 Overview is one fold "j11 · Core checks"; opened, Goal is picked and shows the goal; MindMap shows Topics and Work Structure as left tabs with the map on the right (Chrome). It opens closed and its body sits under its bar, as every other fold on the page does.
- The click script is added once however many Jobs the page draws (window.wbTopViews).
- Tests: test_job_main.py 4 pass; workbench page, side_pane, studio, home 215 passed, 1 skipped.
- ui_preview_check.py: s11 passes. 5623, 5602, 5607, 5599 restarted, all 200.

## Summary

A work Job's Overview is one fold with Goal · Requirements · MindMap as top views; Blocks and Tasks keep their numbered folds.
