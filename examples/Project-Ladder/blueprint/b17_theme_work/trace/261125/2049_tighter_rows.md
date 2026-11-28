---
title: tighter file rows
date: 2026-11-25 20:49
topic: s31-files-pane
aim: File and folder rows in the Files pane sit about 26px apart instead of about 50px, so twice as many fit on screen.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/2049_tighter_rows.md
  what: this trace's own record, written first
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/work_files.py
  what: 'the tree''s own CSS: no 7px page margin on rows, smaller row and folder padding'
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/tests/test_trace_view.py
  what: assert the tight row CSS
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/2049_tighter_rows.md
- plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/work_files.py
- plugins/haipipe-toolkit/servers/workbench/tests/test_trace_view.py
---

# tighter file rows

## Prompts

- **20:49** and for the gap between file rows, could we make them narrawer, it is too large now.
- **20:51** Let's make it as narraw as possible.

## Check

- workbench tests: 242 passed
- 5623 in Chrome: rows 20-21px apart (before about 50px), page margin on rows 0, metro stations still on their rows

## Summary

The tree's own CSS now sets rows to no margin and no padding, folder and file lines to 1px padding with an 18px line height, and the empty-folder note to almost no margin, so rows sit 21px apart instead of about 50px and the metro map follows them.

