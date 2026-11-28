---
title: tree half width, tracked-only fix
date: 2026-11-25 20:30
topic: s31-files-pane
aim: The tree takes about half its current width (long names cut with … and shown in full on hover), and Tracked only hides every untracked row, also rows that load later.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/2030_tree_half_and_filter_fix.md
  what: this trace's own record, written first
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
  what: tree column capped near a third of the pane with … on long names; the tracked-only filter gets its own timer so the marks timer no longer cancels it
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/tests/test_trace_view.py
  what: assert the narrower tree column and the filter's own timer
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/2030_tree_half_and_filter_fix.md
- plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
- plugins/haipipe-toolkit/servers/workbench/tests/test_trace_view.py
---

# tree half width, tracked-only fix

## Prompts

- **20:30** I think for hte file, it can be just half of the current width. and why the filter here doesn't work as we expected? could you check it.
- **20:35** yes, go ahead and update all of them.

## Check

- workbench tests: 242 passed
- 5623 in Chrome, Tracked only on: 215 rows shown, 0 untracked rows or folders shown (before: workbench-task-draft files showed)
- tree column 486px -> 260px, metro 700px -> 926px, long names end with … and show whole on hover

## Summary

Tracked only failed because its timer was shared with the marks timer, which cancelled it whenever rows loaded; it now has its own timer. The tree column is capped at min(34%, 260px) and may shrink below its longest name, with long names cut by … and a hover title; the metro takes the freed width.

