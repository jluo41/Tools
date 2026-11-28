---
title: insight structure as rule trees
date: 2026-11-27 12:38
aim: s01-s03 Structure shows each Block type's rule tree like b17 (Folder with hovers; Job group, Job name, Task group, Task name, all open; Studio), the real example moves to Examples; map ids come from the path inside the example Block so a move does not break them
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b11_theme_insight/trace/261127/1238_structure_rule_trees.md
  what: this trace's own record, written first
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/build_structure.py
  what: rule trees for the three Blocks; ids relative to the example Block
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/check_structure.py
  what: guards for the rule levels and optional groups
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/structure.js
  what: any section id
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/structure.css
  what: plain tree look and hovers
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/insight-board.html
  what: rebuilt
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/question-book.html
  what: rebuilt
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/data-prep.html
  what: rebuilt
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s01-insight-board-structure/studio-views.json
  what: Structure and Draw on rule trees; real views under Examples
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s02-question-book-structure/studio-views.json
  what: same
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s03-dataprep-structure/studio-views.json
  what: same
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s01-insight-board-structure/s01-insight-board-structure.mindmap.md
  what: rebuilt from scratch
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s02-question-book-structure/s02-question-book-structure.mindmap.md
  what: rebuilt from scratch
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s03-dataprep-structure/s03-dataprep-structure.mindmap.md
  what: rebuilt from scratch
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/insight/workbench-insight/ref/block-structure.md
  what: the three rule trees
changed:
- examples/Project-Ladder/blueprint/b11_theme_insight/trace/261127/1238_structure_rule_trees.md
---

# insight structure as rule trees

## Prompts

- **12:38** go

## Check

- check_structure.py PASS, with rule guards (three rule sections, the headings, no real folder in a rule tree, Structure on -rules, Examples on the real views)
- served 5623 Studio: s01 tabs open insight-board.html#folder-rules, #jobs-rules, #studio-rules (Structure), -rules-draw (Draw), #folder, #jobs (Examples); the html 200
- Chrome not checked: the browser extension was not connected
- the three maps rebuilt from scratch; ids read the path inside the example Block

## Summary

s01-s03 Structure shows each insight Block type's rule tree as b17 does; the real example is under Examples; map ids survive a folder move.

