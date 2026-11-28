---
title: read-from compact
date: 2026-11-27 19:55
topic: s31-files-pane
aim: 'In the Files pane the role is written Read-From (what the Block does not change: sources, supporting Blocks, data), and Read-From and Maintain each show one path line, the folder all their rows share, with each row named by its path below it.'
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1955_read_from_compact.md
  what: this trace's own record, written first
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/work_files.py
  what: heading Read-From; one shared path line per role, rows named below it
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/tests/test_role_parts.py
  what: new heading and row names
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/tests/test_work_frame.py
  what: row names below the shared path
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/scripts/folder_icons_check.py
  what: role name Read-From
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/CONSTITUTION.md
  what: role name Read-From and what it holds
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/constitution/A06-real-folders-in-parts.md
  what: role name Read-From, one path line per role
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s31-files-pane/s31-files-pane.md
  what: 'Decided: Read-From and the shared path line'
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1955_read_from_compact.md
- plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/work_files.py
- plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/tests/test_role_parts.py
- plugins/haipipe-toolkit/servers/workbench/page/job_task_views/tests/test_work_frame.py
- plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/scripts/folder_icons_check.py
- plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/CONSTITUTION.md
- plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/constitution/A06-real-folders-in-parts.md
- examples/Project-Ladder/blueprint/b17_theme_work/s31-files-pane/s31-files-pane.md
---

# read-from compact

## Prompts

- **19:55** okay pease do it, I think we will main taim as well. READ-FROM is more like somethings we will not change, like the sources, supporting blocks, and the things like data.

## Check

- files_tree tests: 20 passed; test_work_frame.py: 27 passed
- Live Files panel on 5623, driven in Chrome: heading Read-From with one path line examples/Project-Ladder/ and 4 rows (work/, cowork/, discovery/, knowledge/); Maintain with one path line plugins/haipipe-toolkit/ and 7 rows; Read-From 2 and Maintain 4 expand and load their rows
- folder_icons_check.py --url http://127.0.0.1:5623: no problem on the Files roles; its 12 problems are other traces (no front matter, a moved path not on disk)

## Summary

The role is written Read-From and means what the Block does not change: sources, supporting Blocks, data. Read-From and Maintain each open with one path line, the folder all their rows share, and a row that sits deeper is named by its path below it, so four example Blocks take five lines and seven maintained folders take eight. The rule, its check and the tests name the role the same way.

