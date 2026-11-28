---
title: fold dot corner
date: 2026-11-25 16:20
aim: The left list's hide dot takes no row of its own; it sits on the content frame's top-left corner in both states, so the frame's left line runs down from it, the first tab starts level with the content (today 25px lower), and the view buttons sit a little closer.
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1620_fold_dot_corner.md
    what: this trace's own record, written first
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/parts_and_map/ui_parts.py
    what: _side_tabs puts the .pb-fold dot first in .pb-read, not in the list; PB_CSS sets it absolute on .pb-read's top-left corner (-9px,-9px), shown or hidden; hidden, the list is not drawn and the content takes the one column
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
    what: .studio-view-buttons margin 10px 0 to 6px 0 8px
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1620_fold_dot_corner.md
  - plugins/haipipe-toolkit/servers/workbench/page/parts_and_map/ui_parts.py
  - plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
  - plugins/haipipe-toolkit/servers/workbench/tests/test_focus_studio.py
---

# fold dot corner

## Prompts

- **16:20** I feel there are too many margins, think about how to update this? [the hide dot on its own row between the view buttons and the left tabs]
- **16:25** or you can have a line from point to the [content frame's left edge]?
- **16:30** you can try it.

## Check

- measured before, 5623 b17 s31: view buttons end 506, tabs and content start 516, the dot row 517-535, the first tab 541 (25px below the content's top).
- after, shown: view buttons end 508, the frame's corner (333, 514), the dot's centre (333, 514), the first tab 515.
- after, hidden: the list not drawn, the frame from the left edge (199, 514), 810 wide, the dot on its corner; a second click brings the list back.
- workbench 236, labeling 85, paper 112 pass.

## Summary

The `.pb-fold` dot now lives in `.pb-read` and sits on its top-left corner, so the content frame's left line runs down
from it and the list has no row for it; hidden, only `.pb-list` goes and the content takes the one column.
