---
title: A drag line between the folder tree and the metro map
date: 2026-11-26 16:34
aim: The reader drags the line between the folder tree and the metro map to give the names or the map more room; the width is kept.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261126/1634_tree_metro_split.md
  what: this trace's own record, written first
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
  what: a drag line between tree and metro; double-click resets; width kept
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/tests/test_trace_view.py
  what: one test that the drag line is on the page
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261126/1634_tree_metro_split.md
- plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
- plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/tests/test_trace_view.py
---

# A drag line between the folder tree and the metro map

## Prompts

- **16:34** for the folder tree and metro canvas, could we adjust them the split line of them. do you get what I mean?
- **16:39** have you fixed it? why I cannot see it.

## Check

- side_pane tests 35 passed; Chrome drag 260 to 410 px, saved, double-click back to 260

## Summary

A drag line between the folder tree and the metro map; drag resizes, double-click resets, width kept.

