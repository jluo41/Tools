---
title: brief top left right
date: 2026-11-27 23:54
work: [s11]
aim: "A Job's Brief fold is top-view-left-tab-right-content all the way: Goal, Requirements and MindMap stay the top buttons, each opens the standard left tabs and framed content (a single thing keeps its left tab), and the blue expand dot beside the buttons is gone."
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2354_brief_top_left_right.md
    what: this trace's own record, written first
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/job_overview.py
    what: "Goal and Requirements in the shared side tabs; the expand button, its dialog, style and script removed; the content frame is the standard one"
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/work_frame.py
    what: "the other themes' Job Brief: the same left tabs under each top button"
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/tests/test_job_overview.py
    what: a test for the left tabs and the missing expand dot
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/ref/top-view-left-tab-right-content.md
    what: the Job Brief joins the views that keep a left tab for one thing
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2354_brief_top_left_right.md
  - plugins/haipipe-toolkit/servers/workbench/page/job_task_views/job_overview.py
  - plugins/haipipe-toolkit/servers/workbench/page/job_task_views/work_frame.py
  - plugins/haipipe-toolkit/servers/workbench/page/job_task_views/tests/test_job_overview.py
  - plugins/haipipe-toolkit/servers/workbench/ref/top-view-left-tab-right-content.md
---

# brief top left right

## Prompts

- **23:5x** [Image #63] do we need this? should we drop it?
- **23:5x** [Image #64] is this not hte top-left-right format?
- **23:54** go ahead, and make the Brief to be the top left right format. (asked which layout: top buttons with left tabs under each)

## Check

- Workbench tests (page, side_pane, studio, home): 279 passed, 1 skipped; the new test pins the three top buttons, the left tabs Goal, Requirements, Topics, Work Structure, and no expand dot.
- 5623 and 5602 restarted. Read from 5623's served pages (not looked at in a browser; the Chrome extension is disconnected): the Work example's j11 and the Discovery example's j01 Brief carry no expand button, and Goal and Requirements each sit in the shared side tabs.
- The right content now has the standard frame (the Brief's own rule that removed it is gone).

## Summary

A Job's Brief is top buttons, left tabs and framed content for every view; the expand dot is gone.
