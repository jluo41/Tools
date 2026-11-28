---
title: viewer icon buttons
date: 2026-11-27 21:11
topic: s04-workbench-page-structure
aim: 'The pop-out viewer''s top bar shows two icons and no words: an arrow that goes to the page and a cross that closes, each named on hover.'
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2111_viewer_icon_buttons.md
  what: this trace's own record, written first
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/page/block_index_page/focus_base.py
  what: the two buttons become icons with hover names
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/focus-assets/focus.css
  what: icon button size
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/tests/test_work_frame.py
  what: the top bar holds no button words
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s04-workbench-page-structure/s04-workbench-page-structure.md
  what: 'Decided: icon buttons'
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2111_viewer_icon_buttons.md
- plugins/haipipe-toolkit/servers/workbench/page/block_index_page/focus_base.py
- plugins/haipipe-toolkit/servers/workbench/focus-assets/focus.css
- plugins/haipipe-toolkit/servers/workbench/page/job_task_views/tests/test_work_frame.py
- examples/Project-Ladder/blueprint/b17_theme_work/s04-workbench-page-structure/s04-workbench-page-structure.md
---

# viewer icon buttons

## Prompts

- **21:11** yes, do it.

## Check

- test_work_frame.py: 27 passed, with the top bar asserted to hold the two icons and no Close word
- Live on 5623 in Chrome: the pop-out viewer opened on board.md shows ↗ and ✕, 26 px each, hover names Go to this page and Close; ↗ points at the opened file's page; a click on ✕ closes the viewer

## Summary

The pop-out viewer's top bar now holds two icons and no words: ↗ goes to the page and ✕ closes, each named on hover and for a screen reader. The other Close buttons on the workbench are unchanged.

