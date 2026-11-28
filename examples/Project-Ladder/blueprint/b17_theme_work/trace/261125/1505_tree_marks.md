---
title: tree marks
date: 2026-11-25 15:05
topic: s31-files-pane
task: j03_work_workbench_pages/t04_shared_parts
aim: One Files tree; a trace in play marks its files on it (planned, touched, done, off plan, still to create) with quiet effects; UI and Skills read as the Block's extension; a hover card says what a file or folder is, in place of grey titles on the rows.
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1505_tree_marks.md
    what: this trace's own record, written first
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
    what: drop the Files/Timeline switch; marks and effects on the tree, the Timeline behind a button
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/work_files.py
    what: rows carry their path; the extends-into line; UI part starts at plugins/
  - do: add
    path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/file_info.py
    what: the hover card; a file's first line, its last commit, the traces that touched it; a folder's face title
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/block_index_page/frame_view.py
    what: one view, focus-file-info, that returns the card
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/focus_scope.py
    what: no grey title on folder rows; the fade stays
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/tests/test_element_info.py
    what: no .sc-what on rows
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/tests/test_trace_view.py
    what: the marks list, no switch
  - do: add
    path: plugins/haipipe-toolkit/servers/workbench/tests/test_file_info.py
    what: the card for a file and a folder
  - do: edit
    path: plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/CONSTITUTION.md
    what: A07 marks sit on the one tree
  - do: edit
    path: plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/scripts/folder_icons_check.py
    what: checks the marks, not the switch
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1505_tree_marks.md
  - plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
  - plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/work_files.py
  - plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/file_info.py
  - plugins/haipipe-toolkit/servers/workbench/page/block_index_page/frame_view.py
  - plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/focus_scope.py
  - plugins/haipipe-toolkit/servers/workbench/tests/test_element_info.py
  - plugins/haipipe-toolkit/servers/workbench/tests/test_trace_view.py
  - plugins/haipipe-toolkit/servers/workbench/tests/test_file_info.py
  - plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/CONSTITUTION.md
  - plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/scripts/folder_icons_check.py
---

# tree marks

## Prompts

- **14:58** how do you want to implement it.
- **15:00** we don't wnat this as well, this will be hover over to change, do you get it (the grey folder titles)
- **15:05** okay, go ahead, I hope next time, the things to change will be shown in [the Files tree] go ahead and do it.
- **15:20** when I hover away, the information card is still there. (fix confirmed: yes)

## Check

- workbench tests: 234 passed (test_file_info 4 new, test_trace_view and test_element_info updated).
- folder_icons_check.py --url 5623: 11 trace files, 0 problems.
- 5623 b17 Files in Chrome: chips for the 2 open traces only; 13 folder dots; trace_view.py row sweeps with ◐; hovering it
  shows the card (first sentence, path, ●, 3 traces); s03-cowork-structure's card says "How does work climb the ladder?";
  no grey titles on rows; "extends into" line above 2 · UI, which now starts at plugins/haipipe-toolkit/servers/.

- Hover fix: the card stayed when the mouse left the pane (a frame gets no event); it now hides on the document's
  mouseleave and the window's blur. Checked on 5623: hover s03-cowork-structure in the pane, card shows; move into the main page, card gone.

## Summary

The Files/Timeline switch is gone: the one tree carries the marks of every trace in play (+ rows for files still to
create, a sweep on files being changed, dots on folders), a chip per open trace above it, and the Timeline opens from a
button. A hover card (file_info.py, view focus-file-info) says what a file or folder is; focus_scope no longer writes
grey titles. UI and Skills sit under an "extends into" line, and UI leaves out the Block's own folders.
