---
title: tree scrolls left and right
date: 2026-11-25 20:56
topic: s31-files-pane
aim: 'The tree and metro keep their widths; a deep or long name is never cut with …: the tree scrolls left and right on its own, like the metro.'
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/2056_tree_scrolls_sideways.md
  what: this trace's own record, written first
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
  what: tree column keeps its width and scrolls sideways (trackpad, Shift+wheel, drag); names on one line, no …; hover title kept
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/tests/test_trace_view.py
  what: assert the tree scrolls sideways and names are not cut
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/2056_tree_scrolls_sideways.md
- plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
- plugins/haipipe-toolkit/servers/workbench/tests/test_trace_view.py
---

# tree scrolls left and right

## Prompts

- **20:56** and for this, how do you think? could I do the left and right scroll? I mean we can just make the current width for the files and metro canvas unchangaged, and make the files tree to be scrollable as well.

## Check

- 5623 in Chrome: tree 260px wide, content 333px, scrolls sideways, starts at the left after the jump to the first file

## Summary

The tree keeps its column width and scrolls left and right on its own with no visible bar; names stay on one line, whole, with a hover title, and the jump to a trace's first file never scrolls the tree sideways. Drag scrolling was left out because a drag on the tree would fight clicks on files; trackpad and Shift+wheel scroll it.

