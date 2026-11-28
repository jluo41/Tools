---
title: right click card
date: 2026-11-25 15:31
topic: s31-files-pane
aim: A file's or folder's information opens on a right-click (Open, Copy path), never on hover; Shift and right-click keeps the browser's own menu.
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1531_right_click_card.md
    what: this trace's own record, written first
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/file_info.py
    what: hover becomes right-click; Open and Copy path; closes on Esc, an outside click or its ✕
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/tests/test_file_info.py
    what: no hover left; the right-click script is there
  - do: edit
    path: plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/CONSTITUTION.md
    what: A07 says right-click card, not hover card
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s31-files-pane/s31-files-pane.md
    what: s31-D06 becomes right-click, with JL's words
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1531_right_click_card.md
  - plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/file_info.py
  - plugins/haipipe-toolkit/servers/workbench/tests/test_file_info.py
  - plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/CONSTITUTION.md
  - examples/Project-Ladder/blueprint/b17_theme_work/s31-files-pane/s31-files-pane.md
---

# right click card

## Prompts

- **15:30** for the information, I want to make it like, you right click it, show the informaiton, and I don't want to hover and how the information anymore, how do you think?
- **15:31** okay, I make the plan and I will check

## Check

- 5623 b17 Files: a real right-click on file_info.py opens the card at the mouse (its docstring line, path, ●, two
  traces, Open ↗, Copy path); a mouseover opens nothing; a click outside closes it. test_file_info: 5 passed.

## Summary

The file card opens on a right-click (Shift keeps the browser's menu), never on hover; it has ✕, Open and Copy path and
closes on Esc, an outside click, a scroll or leaving the window. A07 and s31-D06 say so.
