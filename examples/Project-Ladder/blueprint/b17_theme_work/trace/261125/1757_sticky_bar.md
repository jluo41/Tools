---
title: sticky bar
date: 2026-11-25 17:57
topic: s31-files-pane
aim: The Files pane's top row (Trace, the trace name, zoom, arrows, metro icon) stays at the top while the tree scrolls.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1757_sticky_bar.md
  what: this trace's own record, written first
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
  what: the top row sticks to the top of the pane
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1757_sticky_bar.md
- plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
---

# sticky bar

## Prompts

- **17:57** and how about to put this always at the top? when i scroll down, they will still be there, do you get it?
- **18:01** please go ahead and update it.

## Check

- 5623 b17 Files after the 18:04 restart: the top row is position sticky; scrolled 3000 px down it stays at the top (0 px), and the trace content opens right under it (40 px).
- workbench tests: 240 passed.

## Summary

The Files pane's top row (Trace, the trace name, zoom, arrows, metro icon) stays at the top while the tree scrolls; the trace content hangs from it.

