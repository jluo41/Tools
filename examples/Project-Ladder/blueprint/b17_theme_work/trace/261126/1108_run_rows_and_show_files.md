---
title: Run rows and Show files
date: 2026-11-26 11:08
topic: s31-files-pane
aim: A Task's rows show its Run over its rounds; right-clicking an element at once folds the Files pane to that element's folder and the files it owns, all else closed; the pane opens with every folder closed.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261126/1108_run_rows_and_show_files.md
  what: this trace's own record, written first
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_plan_results.py
  what: a Run row over its rounds; 'round N · MM-DD' not 'pNN'
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/page/element_marks/element_info.py
  what: on right-click, tell the pane the element's folder (no extra menu item)
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/focus_scope.py
  what: close all, open only the asked folder and its owned files, highlight them
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/focus-assets/focus.js
  what: open the pane and pass the folder to it
- do: add
  path: plugins/haipipe-toolkit/servers/workbench/page/element_marks/tests/test_show_files.py
  what: right-click folds the pane to the folder; default all closed
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/CONSTITUTION.md
  what: 'rule: right-click folds the pane to the element; the pane opens closed'
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
  what: no folder opens on load; an open trace only marks its folders
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261126/1108_run_rows_and_show_files.md
- plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_plan_results.py
- plugins/haipipe-toolkit/servers/workbench/page/element_marks/element_info.py
- plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/focus_scope.py
- plugins/haipipe-toolkit/servers/workbench/focus-assets/focus.js
- plugins/haipipe-toolkit/servers/workbench/page/element_marks/tests/test_show_files.py
- plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/CONSTITUTION.md
- plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
- plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/work_files.py
- plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/tests/test_trace_view.py
- plugins/haipipe-toolkit/servers/workbench/page/block_index_page/tests/test_focus_status_map.py
---

# Run rows and Show files

## Prompts

- **11:08** I also want another type of effect, like when I right click the element, in the folder panel, it will show the corrspoding files as wel.. do you understand what I mean?
- **11:11** What I mean is when I right click them, the same time, the related files will be highlighted ... and the others will be collapsed. How could you make them by default are collapsed?
- **11:20** go

## Check

- Chrome j12: each Task shows its Run (run-check-files-tree) over 'round 2 · 11-25', 'round 1 · 11-25'
- Chrome: right-click t02 row: pane open folders = b17, j12_side_pane, t02_rail_sections, workbench, side_pane, rail_sections; highlighted t02_rail_sections and rail_sections
- Chrome b17: pane opens with every Block folder closed (only the path to the page and the owned skills' parents); open folders were remembered per tab, now not
- workbench tests 315 passed (6 old draft-reader failures); new test_show_files 3 passed

## Summary

Task rows show their Run over numbered rounds; a right-click folds the Files pane to the element's folder and owned code; the pane opens closed.

