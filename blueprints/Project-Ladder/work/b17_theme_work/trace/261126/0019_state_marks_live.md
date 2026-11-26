---
title: state marks live
date: 2026-11-26
topic: s11-work-job-preview
aim: The live pages draw a state as s11's Effects tab does; one shared table of state marks (the Files pane's, plus waits for you, new and void) that state_mark and the Files pane both read; Task rows and round rows carry the effects; a group bar pings when work runs or waits inside; a Task or Run not yet in git is new.
closed: true
plan:
  - do: add
    path: blueprints/Project-Ladder/work/b17_theme_work/trace/261126/0019_state_marks_live.md
    what: this trace's own record, written first
  - do: add
    path: plugins/haipipe-toolkit/servers/workbench/page/parts_and_map/state_marks.py
    what: the one table of state marks and state_key
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/file_icons.py
    what: STATE_MARKS comes from state_marks
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/parts_and_map/ui_parts.py
    what: state_mark draws the drawn mark with its fx class, its word on hover
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_plan_results.py
    what: Task and round rows carry their fx class; new from git; the group bar's dot
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/focus-assets/focus.css
    what: the fx effects and the live dot, still under reduced motion
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/tests/test_work_sections.py
    what: state_mark's drawn marks
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/block_index_page/tests/test_focus_status_map.py
    what: Task rows' fx classes and new rows
  - do: edit
    path: plugins/haipipe-toolkit/skills/1_base/workbench/haipipe-ui/constitution/A05-one-icon-table.md
    what: a state's mark comes from the one table too
  - do: edit
    path: plugins/haipipe-toolkit/skills/1_base/workbench/haipipe-ui/scripts/folder_icons_check.py
    what: fail when a server module draws its own state mark
changed:
  - blueprints/Project-Ladder/work/b17_theme_work/trace/261126/0019_state_marks_live.md
  - plugins/haipipe-toolkit/servers/workbench/page/parts_and_map/state_marks.py
  - plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/file_icons.py
  - plugins/haipipe-toolkit/servers/workbench/page/parts_and_map/ui_parts.py
  - plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_plan_results.py
  - plugins/haipipe-toolkit/servers/workbench/focus-assets/focus.css
  - plugins/haipipe-toolkit/servers/workbench/page/job_task_views/tests/test_work_sections.py
  - plugins/haipipe-toolkit/servers/workbench/page/block_index_page/tests/test_focus_status_map.py
  - plugins/haipipe-toolkit/skills/1_base/workbench/haipipe-ui/constitution/A05-one-icon-table.md
  - plugins/haipipe-toolkit/skills/1_base/workbench/haipipe-ui/scripts/folder_icons_check.py
---

# state marks live

## Prompts

- **00:31** [Image] Yes, I think this effect could be better. How do you want to update this accordingly
- **00:34** go ahead and update them accordingly.
- **00:41** for the task row effects, we will not change the code in the server yet?

## Check

- workbench tests: 275 passed (reader tests left out: their six old /private failures)
- folder_icons_check: 0 problems, the new state-mark rule included
- 5623 j11 Main: t01 t02 t03 t05 green checks, t04 and its newest round the amber ring pinging, Page components the amber dot; zoomed, aligned
- 5623 j03 Main: t01 to t04 grey and still (not yet), waiting rounds pinging, no pill border on a mark
- first pass made every uncommitted Task new (all of j11 is untracked); new now means untracked and not run yet

## Summary

The live pages draw a state with the Files pane's own marks, from one table (state_marks.py), and carry s11's effects; a Task or Run git does not track and that has not run is new, a plus, fading; a group bar pings when work waits or runs inside.
