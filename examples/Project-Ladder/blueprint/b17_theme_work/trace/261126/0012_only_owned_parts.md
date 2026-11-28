---
title: Only owned folders in Code and Skills
date: 2026-11-26 00:12
topic: s31-files-pane
aim: Code and Skills show only the folders the page owns; every other folder a trace touched (workbench-design, workbench-labeling, design/workbench-design, paper/hai-paper) is listed under Also touched.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261126/0012_only_owned_parts.md
  what: this trace's own record, written first
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/work_files.py
  what: stop adding traced folders to Code and Skills
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
  what: drop touched_homes
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/tests/test_trace_view.py
  what: 'test: other folders land in Also touched'
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/CONSTITUTION.md
  what: folder rule rewritten, JL's words added
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s31-files-pane/s31-files-pane.md
  what: folder-scope decision rewritten
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261126/0012_only_owned_parts.md
- plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/work_files.py
- plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
- plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/tests/test_trace_view.py
- plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/CONSTITUTION.md
- examples/Project-Ladder/blueprint/b17_theme_work/s31-files-pane/s31-files-pane.md
---

# Only owned folders in Code and Skills

## Prompts

- **00:12** these two should be the Also Touch, these two will also be the also touched, can you remove them out? what is your htoughts?

## Check

- b17 Files: Code holds workbench, workbench-work; Skills holds the owned skills only
- Also touched lists workbench-design, workbench-labeling, design/workbench-design, paper/hai-paper, AGENTS.md
- workbench tests: 300 passed, 6 failed as before

## Summary

Code and Skills hold only what the page owns; every other traced file is Also touched.

