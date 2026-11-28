---
title: trace popout
date: 2026-11-25 17:38
topic: s31-files-pane
aim: "A click on the trace name opens its content as a pop-out over the tree, not a block that pushes the tree down; Esc, an outside click or the name closes it."
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1738_trace_popout.md
    what: this trace's own record, written first
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
    what: the content floats under the name over the tree; closes on Esc, an outside click or the name
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s31-files-pane/delivery/ui/files-metro-lr.html
    what: the same in the Metro map preview
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1738_trace_popout.md
  - plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
  - examples/Project-Ladder/blueprint/b17_theme_work/s31-files-pane/delivery/ui/files-metro-lr.html
---

# trace popout

## Prompts

- **17:38** I prefer to make it to be the pop out window, instaed of make the changes, how do you think?
- **17:42** yes, go ahead and do it.

## Check

- 5623 b17 Files: a click on the name opens the content over the tree (the tree moved 0 px); an outside click closes
  it, Esc closes it. workbench tests: 239 passed. The s31 Metro map preview does the same.

## Summary

The trace content is a pop-out under its name, floating over the tree; Esc, an outside click or the name closes it.
