---
title: trace card
date: 2026-11-25 16:43
topic: s31-files-pane
aim: "Picking a trace opens its card under the top row: title and time, the whole aim, its prompts, its Check and Summary, and Open; it folds to one line and stays at the top while the tree scrolls."
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1643_trace_card.md
    what: this trace's own record, written first
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
    what: send each trace's prompts, check and summary; a folding card under the top row in place of the one-line aim
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/tests/test_trace_view.py
    what: the card's data (prompts, check, summary) and its place
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s31-files-pane/s31-files-pane.md
    what: s31-D15, the trace card
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s31-files-pane/delivery/ui/files-metro-lr.html
    what: the trace card in the Metro map preview first; the aim moves from the top row into the card
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1643_trace_card.md
  - plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
  - plugins/haipipe-toolkit/servers/workbench/tests/test_trace_view.py
  - examples/Project-Ladder/blueprint/b17_theme_work/s31-files-pane/s31-files-pane.md
  - examples/Project-Ladder/blueprint/b17_theme_work/s31-files-pane/delivery/ui/files-metro-lr.html
---

# trace card

## Prompts

- **16:43** and I cannot see the content of the trace, when I select one, how do you think we can improve this better?
- **16:47** can you update this first? (the s31 Metro map preview)
- **16:52** please go ahead and update this. A06 <-- what is the A here?

## Check

- s31 Metro map preview: a click on 1418_trace_timeline.md opens its card above the tree (aim, three prompts and
  1 more, Check, Summary, Open); the aim no longer repeats in the top row.
- 5623 b17 Files: Trace on, a click on 1452_job_vs_studio.md opens its card with its real aim, prompts (3 and 1 more),
  Check and Summary read from the trace file; the file viewer does not open. workbench tests: 239 passed.

## Summary

A picked trace shows its card under the top row, read from its own file (aim, Prompts, Check, Summary), folding to one
line and staying at the top (s31-D15), in the preview and the real Files pane.
