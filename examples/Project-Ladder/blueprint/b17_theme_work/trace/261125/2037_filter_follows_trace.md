---
title: filter folds what the picked trace left alone
date: 2026-11-25 20:37
topic: s31-files-pane
aim: 'With the funnel on, nothing is hidden: folders the picked trace did not touch stay listed but folded, folders on its path open, and the untouched files beside its files fold into one ⋯ row that opens on a click; with no trace picked the same holds for all traces'' files.'
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/2037_filter_follows_trace.md
  what: this trace's own record, written first
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
  what: 'the funnel folds instead of hiding: untouched folders closed, path folders open, untouched sibling files gathered under one ⋯ row; follows the picked trace'
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/tests/test_trace_view.py
  what: assert the funnel folds (no hide class) and follows the picked trace
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/CONSTITUTION.md
  what: 'the Files pane article: highlighter fades, funnel folds, nothing is hidden'
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/2037_filter_follows_trace.md
- plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
- plugins/haipipe-toolkit/servers/workbench/tests/test_trace_view.py
- plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/CONSTITUTION.md
---

# filter follows the picked trace

## Prompts

- **20:37** How do you think the filter should work? we I selected a track, and the choose the filter, only the file that associated with this trace will be left, what isthe current design?
- **20:58** could you explain how the filter works? I feel it is current very hard to use. I want to make it more readable. Like for the files that untouched, you can make them collapse, only show the files it changed, right? But for now, it idesont work as we expeced.
- **20:59** how about they are folded, I dont want to hiden them anymore. but I wawnt them to be folded, do you get it?
- **21:12** go, and call the chrome to test it yourself, the rule is, make it clear to see the content, do you get it? currently it is very hard to see the which files are chnaged

## Check

- workbench tests: 242 passed
- 5623 in Chrome, trace 'tree half width, tracked-only fix' picked with the funnel on: its 3 files shown bold with their folders open, all other folders listed and closed, untouched files under ⋯, 0 rows hidden, page scrolled to the first file

## Summary

The funnel no longer hides: it keeps the picked trace's files (every trace's when none is picked), opens their folders, closes every other folder, gathers the untouched files beside them under one ⋯ row that opens on a click, and scrolls the page to the first kept file. Picking another trace refolds at once. The hai-ui Files pane article now says the highlighter fades and the funnel folds.

