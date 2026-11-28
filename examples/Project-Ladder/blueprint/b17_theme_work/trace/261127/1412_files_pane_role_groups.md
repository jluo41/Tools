---
title: files pane role groups
date: 2026-11-27 14:12
topic: s31-files-pane
aim: 'The Files pane names each part by its role: Block (where the work is), Maintain N (a folder the Block changes and keeps, with the Jobs and Studio topics that touch it), ReadFrom N (a folder it only reads), Touch N (a folder a trace touched outside them); no part carries a page-wide number.'
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1412_files_pane_role_groups.md
  what: this trace's own record, written first
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/work_files.py
  what: role parts with their own numbers replace the page-wide numbers and the extends-into line
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
  what: Also touched becomes Touch N, one per folder
- do: add
  path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/touched_by.py
  what: the Jobs and Studio topics that touch a folder, from Job and Task faces, topic faces and traces
- do: add
  path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/tests/test_role_parts.py
  what: tests of the role names, their numbers and the touched-by marks
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/tests/test_trace_view.py
  what: Touch N in place of Also touched
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s31-files-pane/s31-files-pane.md
  what: 'Decided: role parts and touched-by marks'
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1412_files_pane_role_groups.md
- plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/work_files.py
- plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
- plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/touched_by.py
- plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/tests/test_role_parts.py
- plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/tests/test_trace_view.py
- examples/Project-Ladder/blueprint/b17_theme_work/s31-files-pane/s31-files-pane.md
- plugins/haipipe-toolkit/servers/workbench/page/job_task_views/tests/test_work_frame.py
---

# files pane role groups

## Prompts

- **14:12** okay, could you try to update the current one? what is the design for it.
- **14:24** this looks too sparse.
- **19:49** 确认

## Check

- files_tree tests: 20 passed; test_work_frame.py: 27 passed
- Live Files panel on 5623, driven in Chrome: headings Block, Maintain, ReadFrom, Touch; a folder row expands and loads nested rows; +N opens the hidden marks without toggling the folder; all 22 Job and Studio links return 200 and land on their Job page or Studio topic
- folder_icons_check.py --url http://127.0.0.1:5623: no problem on the Files roles; its 11 problems are older trace files (no front matter, a moved path not on disk)
- The rule (hai-ui CONSTITUTION and its details file), folder_icons_check.py and most of test_work_frame.py were already updated to the role parts by another session; here only the last old-heading assertion in test_work_frame.py changed

## Summary

The Files pane groups its parts by role: Block where the work is, Maintain for the folders the Block changes and keeps, ReadFrom for the folders it only reads, Touch for folders a trace touched outside them. A role shows its name once and one row per folder, numbered inside the role, with a path line per shared parent folder; the numbers follow the sort order and are not stable ids. A Maintain row ends with the Jobs and Studio topics that touch its folder, read from Job and Task faces, topic faces and traces (touched_by.py); past four they open from +N.

