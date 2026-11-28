---
title: Render check and its rule
date: 2026-11-26 11:58
topic: s31-files-pane
aim: The format table moves to delivery/page-spec/file-formats.md, render_check.py renders every real file of each kind through its page code, and hai-ui A09 makes it a rule with a Run line.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261126/1158_render_check_rule.md
  what: this trace's own record, written first
- do: move
  path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/page-spec/file-formats.md
  what: from examples/Project-Ladder/blueprint/b17_theme_work/j16_file_formats/t01_format_table/format-table.md
- do: add
  path: plugins/haipipe-toolkit/servers/workbench/checks/render_check.py
  what: every file of each kind through its page code; exit 1 on a problem
- do: add
  path: plugins/haipipe-toolkit/servers/workbench/checks/tests/test_render_check.py
  what: the table and the script name the same kinds; a broken file is caught
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/j16_file_formats/t01_format_table/t01_format_table.md
  what: 'Files: the table''s new place'
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/j16_file_formats/t02_render_check/t02_render_check.md
  what: 'Files: the script''s place, its run'
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/j16_file_formats/t03_example_files/t03_example_files.md
  what: link to the table's new place
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/j16_file_formats/t02_render_check/runs/run-check-render
  what: first round, written by soft_run.py
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/CONSTITUTION.md
  what: 'A09: one format per kind, every file renders'
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261126/1158_render_check_rule.md
- examples/Project-Ladder/blueprint/b17_theme_work/delivery/page-spec/file-formats.md
- plugins/haipipe-toolkit/servers/workbench/checks/render_check.py
- plugins/haipipe-toolkit/servers/workbench/checks/tests/test_render_check.py
- examples/Project-Ladder/blueprint/b17_theme_work/j16_file_formats/t01_format_table/t01_format_table.md
- examples/Project-Ladder/blueprint/b17_theme_work/j16_file_formats/t02_render_check/t02_render_check.md
- examples/Project-Ladder/blueprint/b17_theme_work/j16_file_formats/t03_example_files/t03_example_files.md
- plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/CONSTITUTION.md
- examples/Project-Ladder/blueprint/b17_theme_work/j16_file_formats/t02_render_check/runs/run-check-render/run.yaml
- examples/Project-Ladder/blueprint/b17_theme_work/j16_file_formats/t02_render_check/runs/run-check-render/passes/p01-1126/pass.md
---

# Render check and its rule

## Prompts

- **11:58** go

## Check

- render_check.py over b17: 289 files, 0 problems, 17 s; over examples/: 769 files, 16 problems (cowork, discovery, labeling Job and Task pages miss their goal), 47 s
- checks/tests/test_render_check.py 3 passed: table and script kinds equal; a missing goal, an empty page and a thin trace are caught
- first round p01-1126 written by soft_run.py; A09 added to hai-ui, status open

## Summary

The format table lives in b17's page spec, render_check.py proves every file draws, and A09 makes it a rule.

