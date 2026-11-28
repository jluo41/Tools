---
title: read-from data
date: 2026-11-27 19:59
topic: s31-files-pane
aim: 'Read-From also lists the Block''s data: each store in its board.md Data list whose where is a folder of the SPACE, with no new line on the face.'
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1959_read_from_data.md
  what: this trace's own record, written first
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/work_files.py
  what: data stores with a SPACE folder join Read-From
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/tests/test_role_parts.py
  what: test of a data store in Read-From
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/CONSTITUTION.md
  what: Read-From names where its data comes from
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/constitution/A06-real-folders-in-parts.md
  what: the same in the parts table
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-block/ref/board-contract.md
  what: 'Data: a store in a SPACE folder shows in Read-From'
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s31-files-pane/s31-files-pane.md
  what: 'Decided: data in Read-From'
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1959_read_from_data.md
- plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/work_files.py
- plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/tests/test_role_parts.py
- plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/CONSTITUTION.md
- plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/constitution/A06-real-folders-in-parts.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-block/ref/board-contract.md
- examples/Project-Ladder/blueprint/b17_theme_work/s31-files-pane/s31-files-pane.md
---

# read-from data

## Prompts

- **19:59** yes, plesae go ahead and do it.

## Check

- files_tree tests: 21 passed (one new: a data store in a SPACE folder is row 2 of Read-From; a catalog and a missing folder are left out); test_work_frame.py: 27 passed
- Live after restart of 5623, 5602, 5607, 5599: b17's Files panel unchanged (Maintain 7 rows, Read-From 4 rows); REACH b11_adhd_raw_extraction, whose Data list names a catalog and remote Volume paths, renders with no Read-From data row, as it has no SPACE folder
- folder_icons_check.py --url http://127.0.0.1:5623: no problem on the Files roles
- No Block on this machine has a Data store whose where is a local SPACE folder, so the new row is proven by the test only, not yet on a real page

## Summary

Read-From now also lists a Block's data: each store of its board.md Data list whose where is a folder of the SPACE, named from the SPACE root. The face gets no new line, because the Data list already says where the data is; a catalog, a share or a remote path has no folder and stays in Findings only.

