---
title: a color per level
date: 2026-11-27 13:03
aim: Each level of the Job / Task tree has its own color (Job group, Job name, Task group, Task name), the same color for the same level in s01-s03, light and dark
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b11_theme_insight/trace/261127/1303_level_colors.md
  what: this trace's own record, written first
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/build_structure.py
  what: each item carries its level
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/structure.css
  what: one color per level
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/insight-board.html
  what: rebuilt
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/question-book.html
  what: rebuilt
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/data-prep.html
  what: rebuilt
changed:
- examples/Project-Ladder/blueprint/b11_theme_insight/trace/261127/1303_level_colors.md
---

# a color per level

## Prompts

- **13:03** Yes, and for the differnet layer, could you use different color things?

## Check

- check_structure.py PASS; every jobs-rules item carries data-level (block, job-group, job-name, task-group, task-name); the css colors each, light and dark
- Chrome not checked: the browser extension was not connected

## Summary

Each Job / Task level has its own color, the same across s01-s03.

