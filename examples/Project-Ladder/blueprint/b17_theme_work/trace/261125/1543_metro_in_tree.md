---
title: metro in tree
date: 2026-11-25 15:43
topic: s31-files-pane
aim: "The real Files pane draws the metro map beside the tree, as the s31 preview; each visible row a file line left to right, each trace a coloured column of stations, opening on the newest; the branching-line icon shows or hides it; a click on a station or a time picks that trace."
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1543_metro_in_tree.md
    what: this trace's own record, written first
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
    what: one SVG beside the tree, redrawn as folders open and close and as the pane scrolls; stations by state; the show or hide icon; a click on a station or time picks the trace; the Trace button becomes the highlighter icon, the show or hide icon the branching line
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/tests/test_trace_view.py
    what: the metro data (traces in time order, colours, stations per file) and the show or hide icon
  - do: edit
    path: plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/CONSTITUTION.md
    what: A07 says the metro map sits beside the tree
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s31-files-pane/s31-files-pane.md
    what: s31-D14, the metro map in the real Files pane
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1418_trace_timeline.md
    what: close it (Check, Summary); its work is done, and its open marks hide this plan's on three shared files
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1543_metro_in_tree.md
  - plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
  - plugins/haipipe-toolkit/servers/workbench/tests/test_trace_view.py
  - plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/CONSTITUTION.md
  - examples/Project-Ladder/blueprint/b17_theme_work/s31-files-pane/s31-files-pane.md
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1418_trace_timeline.md
---

# metro in tree

## Prompts

- **15:43** have you make this work? (the metro map preview)
- **15:45** I think we might wnat to delete and remove this as well. (the Timeline window)
- **15:47** is this the plan? I want the plan work until I can view them in the file panel. for this, could you list the shared folder path as well? Like plugins/haipipe-toolkit/skills/ make the plan first
- **16:36** where is the metro map? (in the real Files pane)
- **16:47** I want this [C Highlighter for Trace] and this [D Branching line for the metro]
- **16:55** okay, good, what is your plan to update it?
- **16:58** okay, go ahead and do it.

## Check

- workbench tests: 238 passed (metro data: order, day, time, a state per file, a colour per trace; both icons).
- 5623 b17 Files: the metro sits beside the tree, 31 traces as columns, opening on the newest; each trace file under
  trace/261125 has its station in its own column (a diagonal); folder rows carry the rolled-up stations.
- A click on a 1505 station turns Trace on and lights its 11 files; the branching-line icon hides the metro (the row
  marks come back) and shows it again. The metro is capped at 38% of the pane so names keep room.
- A stray CSS line left in trace_view.py from the Timeline removal is gone.

## Summary

The real Files pane draws the metro map beside the tree, redrawn as folders open and load; Trace is the highlighter, the
metro's show or hide the branching line (s31-D14, A07). 1418's Timeline work is closed.
