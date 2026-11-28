---
title: Design Structure as a tree
date: 2026-11-27 11:10
topic: s01-design
aim: Replace both four-column Structure tables with expanded collapsible type/name trees using the peer Studio content pattern.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b12_theme_design/trace/261127/1110_design_structure_tree.md
  what: this trace's own record, written first
- do: add
  path: examples/Project-Ladder/blueprint/b12_theme_design/s01-design/delivery/structure.html
  what: Show collapsible type/name tree
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/s01-design/studio-views.json
  what: Point Structure to the tree
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/s01-design/delivery/structure.md
  what: Replace table with tree while retaining sources
- do: add
  path: examples/Project-Ladder/blueprint/b12_theme_design/s02-workbench-ui/delivery/structure.html
  what: Show collapsible type/name tree
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/s02-workbench-ui/studio-views.json
  what: Point Structure to the tree
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/s02-workbench-ui/delivery/structure.md
  what: Replace table with tree while retaining sources
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/delivery/build_structure_studios.py
  what: Render and validate tree relationships
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/design/workbench-design/ref/topics.md
  what: Record tree correction and guard
changed:
- examples/Project-Ladder/blueprint/b12_theme_design/trace/261127/1110_design_structure_tree.md
- examples/Project-Ladder/blueprint/b12_theme_design/s01-design/delivery/structure.html
- examples/Project-Ladder/blueprint/b12_theme_design/s01-design/studio-views.json
- examples/Project-Ladder/blueprint/b12_theme_design/s01-design/delivery/structure.md
- examples/Project-Ladder/blueprint/b12_theme_design/s02-workbench-ui/delivery/structure.html
- examples/Project-Ladder/blueprint/b12_theme_design/s02-workbench-ui/studio-views.json
- examples/Project-Ladder/blueprint/b12_theme_design/s02-workbench-ui/delivery/structure.md
- examples/Project-Ladder/blueprint/b12_theme_design/delivery/build_structure_studios.py
- plugins/haipipe-toolkit/skills/3_theme/design/workbench-design/ref/topics.md
---

# Design Structure as a tree

## Prompts

- **11:10** 你这里的 structure能不能变成一个 tree啊？你画了一个表，他妈谁看得好啊？你看别人怎么做的，你画了一个 tree不行吗。

## Check

- Structure builder --check passed for both Studios; scoped git diff --check passed.
- Chrome showed both expanded trees, Board Task collapse/expand and separate Folder/Studio trees. Screenshot: /tmp/design-structure-tree.jpg.

## Summary

Replaced both Structure tables with expandable trees using the shared Studio tabs. Preserved contract names and boundaries, Draw and actual folders. T09 records the request and regression guard.

## Authorization

The user directly requested correcting the existing Structure presentation to a tree. The implementation paths were listed in chat before edits. This is a reversible correction to the already authorized two Studios; no shared code or execution Folder changes. The Work organization HTML was inspected as the tree-pattern reference.
