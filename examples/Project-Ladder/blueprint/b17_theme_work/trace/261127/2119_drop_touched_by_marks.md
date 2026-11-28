---
title: drop touched-by marks
date: 2026-11-27 21:19
topic: s31-files-pane
aim: 'A Maintain row shows its folder only: the Job and Studio codes at the end of the row are gone, with the code that computed them.'
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2119_drop_touched_by_marks.md
  what: this trace's own record, written first
- do: delete
  path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/touched_by.py
  what: the touched-by computation goes
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/work_files.py
  what: rows carry no codes; their style goes
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/tests/test_role_parts.py
  what: the touched-by tests go
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s31-files-pane/s31-files-pane.md
  what: the touched-by decision is withdrawn
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2119_drop_touched_by_marks.md
- plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/work_files.py
- plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/tests/test_role_parts.py
- examples/Project-Ladder/blueprint/b17_theme_work/s31-files-pane/s31-files-pane.md
---

# drop touched-by marks

## Prompts

- **21:19** yes, please go ahead and do them, please update it again/ And I also find that when I scroll down and up, the UI doesn't work. Wht hapened?

## Check

- files_tree tests: 21 passed (the two touched-by tests removed, one asserts no code on a row and no touched_by.py); test_work_frame.py: 27 passed
- Live Files panel of b17 on 5623 after restart: no files-by element on the page; every Maintain row ends with its folder name
- Scroll report (the pane does not work after scrolling down and up): not reproduced. In Chrome, in the Block page's side pane, 30 wheel steps down and 30 up over the tree and over the metro map return to the top with no long task and no metro redraw, and a folder still opens after. Found on the way: the Block page throws 4 script errors on load from page/parts_and_map/matrix_help.py line 84 (its root element is null), which is outside this trace

## Summary

The Job and Studio codes at the end of Maintain rows are gone, with touched_by.py, their style and their tests. The reported scroll problem was not reproduced by driving the real pane; the hosts were restarted many times today while the page was open, which breaks an open pane until it is reloaded, and is the likeliest cause.

