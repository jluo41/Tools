---
title: top views one row
date: 2026-11-27 15:30
work: [s72]
aim: "The top-view buttons of a fold are one row that never wraps; when they do not fit, the row scrolls left and right. In a Studio topic and in a Job's Brief fold; written into the layout's ref and hai-ui."
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1530_top_views_one_row.md
    what: this trace's own record, written first
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
    what: .studio-view-buttons is one row, scrolling sideways
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/work_frame.py
    what: .top-views (a Job's Brief fold) the same
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/ref/top-view-left-tab-right-content.md
    what: the top-view is one row that scrolls, never wraps
  - do: edit
    path: plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/SKILL.md
    what: its top-view-left-tab line says one row, scrolling sideways
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1530_top_views_one_row.md
  - plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
  - plugins/haipipe-toolkit/servers/workbench/page/job_task_views/work_frame.py
  - plugins/haipipe-toolkit/servers/workbench/page/job_task_views/job_overview.py
  - plugins/haipipe-toolkit/servers/workbench/ref/top-view-left-tab-right-content.md
  - plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/SKILL.md
---

# top views one row

## Prompts

- **15:28** [Image #59] make this to be one row and left right scrollable, update the related skills as well.

## Check

- 5623 serves the new rule on the Studio page (.studio-view-buttons: flex-wrap:nowrap, overflow-x:auto) and on the Jobs page (.jov-views, the row a Job's Brief fold draws today, in job_overview.py; .top-views in work_frame.py got the same rule but is no longer what the page draws); each button flex:none, so none shrinks or wraps. Read from the served CSS; not looked at in a browser (the Chrome extension is disconnected), so the scrolling itself is not seen yet.
- Tests: workbench page, side_pane, studio, home pass. 5623 and 5602 restarted, both 200.

## Summary

A fold's top-view buttons are one row that scrolls sideways; the layout's ref and hai-ui say so.
