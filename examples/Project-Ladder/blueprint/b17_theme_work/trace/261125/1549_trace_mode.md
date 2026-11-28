---
title: trace mode
date: 2026-11-25 15:49
topic: s31-files-pane
aim: The chips row and the ⊞ button go; one Trace button at the top of Files switches to trace mode, which shows only the files the current trace plans or touched, every folder open, each with its mark; a second click goes back to the whole tree.
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1549_trace_mode.md
    what: this trace's own record, written first
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
    what: remove the chips and the ⊞ Timeline; a Trace button that lights up one trace's files (its plan and changes), opens the tree to them and dims the rest; a picker for the trace
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/tests/test_trace_view.py
    what: the Trace button, the trace mode tree, no chips, no Timeline window
  - do: edit
    path: plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/CONSTITUTION.md
    what: A07 says trace mode shows a trace's files; no chips, no Timeline window
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s31-files-pane/s31-files-pane.md
    what: s31-D12, trace mode in place of the chips and the Timeline
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s31-files-pane/delivery/ui/files-metro-lr.html
    what: changed in place, no new file; trace mode (Trace button, a trace picker, only its files) and no explaining words
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s31-files-pane/delivery/ui/files-trace-effects.html
    what: no explaining words (the hint line under the tree)
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s31-files-pane/delivery/ui/files-metro.html
    what: no explaining words (the note above the map)
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s31-files-pane/delivery/ui/files-tree-timeline.html
    what: no explaining words (the note above the map)
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1549_trace_mode.md
  - plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
  - plugins/haipipe-toolkit/servers/workbench/tests/test_trace_view.py
  - plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/CONSTITUTION.md
  - examples/Project-Ladder/blueprint/b17_theme_work/s31-files-pane/s31-files-pane.md
  - examples/Project-Ladder/blueprint/b17_theme_work/s31-files-pane/delivery/ui/files-metro-lr.html
  - examples/Project-Ladder/blueprint/b17_theme_work/s31-files-pane/delivery/ui/files-trace-effects.html
  - examples/Project-Ladder/blueprint/b17_theme_work/s31-files-pane/delivery/ui/files-metro.html
  - examples/Project-Ladder/blueprint/b17_theme_work/s31-files-pane/delivery/ui/files-tree-timeline.html
---

# trace mode

## Prompts

- **15:49** I didn't see which file will be modified. maybe we remove things here, and can have a trace mode to replace [the ⊞ button], and click it, and we can show which files will be infleunces by the current trace, how do you think about it?
- **15:52** how do you want to update this first? (the metro preview)
- **15:58** remove the words here, like UI explain themself. and why you donjut change the [Metro map] this one direclty, but create a new one?
- **16:02** could you just first change this? (the Metro map preview)
- **16:05** why I find many details are gone compared to the previous version? could you work based on the previous version? for the plan, we can just go ahead and update.
- **16:10** wait, before you change the things, could you explain what is the design purpose???
- **16:12** okay, go ahead and do it.

## Check

- workbench tests: 236 passed (one Studio test failed once mid-change, from another session's edit; it passed on the
  next run).
- 5623 b17 Files: no chips, no ⊞, one Trace button; on, the picker starts on 1549_trace_mode and lights all 9 of its
  files (s31 previews, s31-files-pane.md, this trace, trace_view.py, test_trace_view.py, hai-ui CONSTITUTION.md),
  opening the folders down to them; every other row stays, dimmed.
- First try lit only CONSTITUTION.md: opening a folder whose rows are already there changes nothing, so light() now
  runs again after each opening.
- s31 Metro map preview rebuilt from the earlier version: every row and trace kept, Trace dims instead of hiding; the
  explaining words are gone from all four previews.

## Summary

The Files pane has one Trace button in place of the chips row and the Timeline window: it lights up one trace's files and
folders and dims the rest, never hiding a row (s31-D12, A07). The s31 previews say nothing in words; the layout does.
