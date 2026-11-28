---
title: Design Structure as a mind map
date: 2026-11-27 11:20
topic: s01-design
aim: Use left-to-right connected Job Type → Job Name → Task Type → Task Name branches, with each parent once and Book ending at Job Name.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b12_theme_design/trace/261127/1120_design_structure_mindmap.md
  what: this trace's own record, written first
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/delivery/build_structure_studios.py
  what: Render and check left-to-right connected mind maps
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/s01-design/delivery/structure.html
  what: Render connected mind map
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/s01-design/studio-views.json
  what: Share mind map in Structure and Draw; retain canvas
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/s01-design/delivery/structure.md
  what: Document mind map and no-Task stopping boundary
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/s02-workbench-ui/delivery/structure.html
  what: Render connected mind map
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/s02-workbench-ui/studio-views.json
  what: Share mind map in Structure and Draw; retain canvas
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/s02-workbench-ui/delivery/structure.md
  what: Document mind map and no-Task stopping boundary
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/design/workbench-design/ref/topics.md
  what: Record mind-map correction and guard
changed:
- examples/Project-Ladder/blueprint/b12_theme_design/trace/261127/1120_design_structure_mindmap.md
- examples/Project-Ladder/blueprint/b12_theme_design/delivery/build_structure_studios.py
- examples/Project-Ladder/blueprint/b12_theme_design/s01-design/delivery/structure.html
- examples/Project-Ladder/blueprint/b12_theme_design/s01-design/studio-views.json
- examples/Project-Ladder/blueprint/b12_theme_design/s01-design/delivery/structure.md
- examples/Project-Ladder/blueprint/b12_theme_design/s02-workbench-ui/delivery/structure.html
- examples/Project-Ladder/blueprint/b12_theme_design/s02-workbench-ui/studio-views.json
- examples/Project-Ladder/blueprint/b12_theme_design/s02-workbench-ui/delivery/structure.md
- plugins/haipipe-toolkit/skills/3_theme/design/workbench-design/ref/topics.md
---

# Design Structure as a mind map

## Prompts

- **11:20** Work owner relayed the user correction: “不是，我意思是做一个mind map一样的炊，你懂吗。” Update Structure/Draw to a connected left-to-right mind map; keep verified names and actual folders.

## Check

- Builder --check passed for both shared-view manifests, branch/role counts, actual example names and Book boundary; scoped git diff --check passed.
- Chrome confirmed Board branching, Book ending at Job Name, Structure/Draw agreement, Actual size scale(1) and Fit to width scale(0.630208). Screenshot: /tmp/design-structure-mindmap.jpg.

## Summary

Both Studios now share connected left-to-right mind maps in Structure and Draw. Each parent occurs once per branch; Book stops at Job Name. Folder, original canvases and actual storage are preserved. T10 records the correction and regression guard.

