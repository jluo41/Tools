---
title: 's71: left column fits its names; a Pattern tree to follow on each requirement page'
date: 2026-11-27 20:05
topic: s71-studio-type-block-structure
aim: 'The left tab column is as wide as its longest name, up to 170 px. Each s71 requirement page shows a Pattern row: a small tree with placeholder names in 〈 〉 and the Files pane icons.'
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2005_s71_pattern_trees.md
  what: this trace's own record, written first
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
  what: left column fits its names, max 170 px (test_studio_bands.py)
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_types.py
  what: read the > tree lines of a requirement
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/type_requirements.py
  what: draw the Pattern tree with the Files pane icons
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/elements.md
  what: placeholder trees; pages rebuilt
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2005_s71_pattern_trees.md
- plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
- plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_types.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/type_requirements.py
- examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/elements.md
---

# s71: left column fits its names; a Pattern tree to follow on each requirement page

## Prompts

- **20:05** why the gap here is very large? and for the right content, could you give the examples, like give the examples to follow? I want the icons like this, but not the real name, just the placeholder within <xxx>

## Check

- type_requirements.py --check, checks/run.py --target s71, placeholder_check.py: pass; Studio tests 30 and hai-studio tests 70 pass; pages and left column rendered in headless Chrome

## Summary

Left tab column fits its names up to 170 px. Folder, Job-Task, Studio and the eight type tabs of s71 show a Pattern tree with placeholder names and the Files pane icons.

