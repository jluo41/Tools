---
title: scope fade parts
date: 2026-11-25 11:49
topic: s31-files-pane
aim: In Files, only rows of the Block part fade when they lie outside the page's folder; the UI and Skills parts never fade.
closed: true
plan:
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/focus_scope.py
    what: the fade applies inside 1 · Block only (.fixed-folder)
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/tests/test_element_info.py
    what: the fade rule is scoped to the Block part
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1149_scope_fade_parts.md
  - plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/focus_scope.py
  - plugins/haipipe-toolkit/servers/workbench/tests/test_element_info.py
---

# scope fade parts

## Prompts

- **11:49** [image] I WANT TO UNDERSTAND THIS. why they are faded? I assume they are the dielvery output, right? that will be the output of this block, is that correct?

## Check

- workbench 230 passed.
- j03 page on 5623: Block part j01 at .32, j03 at 1; UI and Skills parts all at 1.

## Summary

The faded rows were not delivery: the scope fade marked every row outside the page's folder, so the UI and Skills
parts faded too. The fade now lives inside 1 · Block only.
