---
title: click pick
date: 2026-11-25 16:15
topic: s31-files-pane
aim: The real Files pane picks a trace by a click, not a dropdown; Trace on starts on the newest open trace, and a click on another trace file under trace/ switches to it (its card still opens it).
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1615_click_pick.md
    what: this trace's own record, written first
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
    what: no dropdown; in trace mode a click on a trace file picks that trace
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/tests/test_trace_view.py
    what: no dropdown; each trace carries its file path for the click
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s31-files-pane/s31-files-pane.md
    what: s31-D13, a click picks the trace; a button shows or hides the metro
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1615_click_pick.md
  - plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
  - plugins/haipipe-toolkit/servers/workbench/tests/test_trace_view.py
  - examples/Project-Ladder/blueprint/b17_theme_work/s31-files-pane/s31-files-pane.md
---

# click pick

## Prompts

- **16:20** I don't thinks we need this, we can just clikc and select, we can drop [the dropdown] and keep [the aim]
- **16:15** very nice, go ahead and do it.

## Check

- 5623 b17 Files: no dropdown; Trace on (restored from the last visit) lights 1418's six files; a click on
  1505_tree_marks.md switches to 1505 and lights its eleven files; the file viewer does not open.
- Two fixes on the way: the pick ran after the viewer's own click handler (it now listens on window, first); a folder
  opened by trace mode right at load sometimes stayed empty (it now asks the loader again after a moment).
- workbench tests: 236 passed.

## Summary

The real Files pane picks a trace by a click on its file under trace/ while Trace is on; the dropdown is gone; folders
opened for a trace always load their rows (s31-D13).
