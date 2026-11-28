---
title: Trace bar on every Block
date: 2026-11-26 00:18
topic: s31-files-pane
aim: Every Block's Files pane shows the trace bar; a Block's metro also carries the traces of other Blocks that changed its files (b11 was changed by b17's page-spec move).
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261126/0018_trace_bar_on_every_block.md
  what: this trace's own record, written first
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
  what: bar always drawn; traces gathered from every Block touching this one
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/tests/test_trace_view.py
  what: 'tests: bar with no trace, a foreign trace shows'
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/CONSTITUTION.md
  what: 'rule: bar on every Block, foreign traces join'
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s31-files-pane/s31-files-pane.md
  what: 'decision: trace bar everywhere'
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261126/0018_trace_bar_on_every_block.md
- plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
- plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/tests/test_trace_view.py
- plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/CONSTITUTION.md
- examples/Project-Ladder/blueprint/b17_theme_work/s31-files-pane/s31-files-pane.md
---

# Trace bar on every Block

## Prompts

- **00:18** I didn't see [the trace bar] in [the b11 Files tree] from b11_theme_insight studio
- **10:25** for this, why I cannot see [the trace bar] ... what I have is [no bar]
- **10:25** go

## Check

- b11 own 7 + 2 visiting, b12 0 + 2 visiting (b17's clean and page-spec traces), b17 112 + 0
- b11, b12, b15 panels: bar and metro drawn; Chrome: b12's pane shows 'Clean the theme Blocks' on its metro
- files_tree tests 14 passed, two new: bar with no trace, another Block's trace marks only this Block's files

## Summary

Every Block's pane has the trace bar; other Blocks' traces that touched it join its metro.

