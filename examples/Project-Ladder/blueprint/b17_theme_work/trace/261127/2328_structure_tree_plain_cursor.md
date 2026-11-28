---
title: 'Structure trees: no question-mark cursor'
date: 2026-11-27 23:28
topic: s71-studio-type-block-structure
aim: A tree line with a hover keeps the ordinary cursor; the hover words still show.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2328_structure_tree_plain_cursor.md
  what: this trace's own record, written first
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/gallery/block-structure/scripts/block_structure_page.py
  what: drop the help cursor; s01 to s04 Structure pages rebuilt
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2328_structure_tree_plain_cursor.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/gallery/block-structure/scripts/block_structure_page.py
---

# Structure trees: no question-mark cursor

## Prompts

- **23:28** no need to show  ?, just the mouse itself should be okay

## Check

- type_follow.py follow on s01 to s04: all follow; the built pages hold no cursor:help and keep their title hovers; checks/run.py passes on the four

## Summary

Tree lines keep the ordinary cursor; the hover words stay.

