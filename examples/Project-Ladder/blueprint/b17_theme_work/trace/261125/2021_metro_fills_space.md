---
title: metro fills the space
date: 2026-11-25 20:21
topic: s31-files-pane
aim: 'When the Files pane is wider, the metro map takes the free space: the tree keeps the width its names need, the metro gets the rest and spreads its columns.'
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/2021_metro_fills_space.md
  what: this trace's own record, written first
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
  what: tree column sized to its names, metro column takes the rest, columns spread to fill, scroll only when they do not fit
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/tests/test_trace_view.py
  what: assert the metro column is the flexible one
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/2021_metro_fills_space.md
- plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
- plugins/haipipe-toolkit/servers/workbench/tests/test_trace_view.py
---

# metro fills the space

## Prompts

- **20:21** how could I make the metro map to fill the white space, whhen i make the panel larger, do you understand what I want?
- **20:27** yes, pleas do it, What are the files to change? what is the plan?

## Check

- workbench tests: 242 passed
- 5623 in Chrome: pane 1186px, tree 486px, metro 700px, 13 columns spread to fill, no scroll needed

## Summary

The tree column now sizes to its names (at most 65%) and the metro column takes the rest; column spacing spreads to fill the metro width, up to three times the base step, and it scrolls only when the columns still do not fit. Zoom keeps its centre with the new spacing, and the metro redraws when the pane is resized.

