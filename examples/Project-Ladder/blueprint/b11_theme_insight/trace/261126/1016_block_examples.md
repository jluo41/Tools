---
title: block examples
date: 2026-11-26 10:16
aim: 'The Files pane has a fourth part, Block Examples, from the Block face examples: line'
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b11_theme_insight/trace/261126/1016_block_examples.md
  what: this trace's own record, written first
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/work_files.py
  what: examples_tree and the fourth part
- do: add
  path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/tests/test_block_examples.py
  what: its test
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/board.md
  what: 'the examples: line'
changed:
- examples/Project-Ladder/blueprint/b11_theme_insight/trace/261126/1016_block_examples.md
---

# block examples

## Prompts

- **10:16** for these, I think you should also add 4. Block Examples ... for each of them, you should have a section for them

## Check

- 5623: b11's Files pane shows 4 · Block Examples with the three examples; files_tree tests pass (13)

## Summary

The Files pane has a fourth part, Block Examples, read from the Block face's examples: line; b11 names its three insight examples.

