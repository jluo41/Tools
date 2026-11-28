---
title: metro side scroll
date: 2026-11-25 16:41
topic: s31-files-pane
aim: "The metro map moves left and right without its scrollbar, which sits at the bottom of a very tall strip; arrows in the top row step through the columns, and the map can be dragged sideways."
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1641_metro_side_scroll.md
    what: this trace's own record, written first
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
    what: arrows beside the metro icon step four columns; dragging the map moves it sideways; the scrollbar is hidden
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/tests/test_trace_view.py
    what: the two arrows are there
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1641_metro_side_scroll.md
  - plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
  - plugins/haipipe-toolkit/servers/workbench/tests/test_trace_view.py
---

# metro side scroll

## Prompts

- **16:41** it feel it cannot be left and right scool
- **16:43** go ahead and do it.

## Check

- Cause: the strip is as tall as the tree (9052 px), so its scrollbar sat at y 8296, out of sight; a mouse wheel only
  moves up and down.
- 5623 b17 Files: › is off at the newest end; two clicks on ‹ moved the map from 554 to 407 px; a drag of 80 px moved
  it 86 px and did not change the picked trace (1505 stayed). workbench tests: 238 passed.

## Summary

‹ and › beside the metro icon step four columns; the map can be dragged sideways; its hidden scrollbar is gone.
