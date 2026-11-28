---
title: tracked only
date: 2026-11-25 18:21
topic: s31-files-pane
aim: A button in the top row hides every file and folder no trace has touched, opens the tree down to those that have, and shows the whole tree again on a second click.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1821_tracked_only.md
  what: this trace's own record, written first
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
  what: a tracked-only button; hide rows with no station; open folders down to tracked files
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/tests/test_trace_view.py
  what: the button is there
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1821_tracked_only.md
- plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
- plugins/haipipe-toolkit/servers/workbench/tests/test_trace_view.py
---

# tracked only

## Prompts

- **18:21** I think we might need another things to make it readable, which means only show the files with the track, and hide others, do you get what I mean?
- **18:23** okay, I agree, please do it.

## Check

- 5623 b17 Files: the funnel button hides every row no trace touched (_old, records, runs and the like) and opens the folders down to tracked files; a second click brings the whole tree back; the metro redraws to the rows left.
- workbench tests: 242 passed.

## Summary

A funnel button in the top row shows only the files and folders some trace touched, so the metro reads densely; it works with Trace, which then lights one trace among them.

