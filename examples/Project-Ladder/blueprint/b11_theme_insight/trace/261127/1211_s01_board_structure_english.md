---
title: s01 board structure in English, by question version
date: 2026-11-27 12:11
aim: 's01''s Job / Task map reads like the live Jobs page: Insight-Example → question version → Job (its versions) → Task kind → Task → Runs (segments), no Job Type node; every structure label is English'
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b11_theme_insight/trace/261127/1211_s01_board_structure_english.md
  what: this trace's own record, written first
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/build_structure.py
  what: English labels; the Board map grouped by question version with Runs
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/check_structure.py
  what: guards for the Board's new levels
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/insight-board.html
  what: rebuilt
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/question-book.html
  what: rebuilt, English
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/data-prep.html
  what: rebuilt, English
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s01-insight-board-structure/s01-insight-board-structure.mindmap.md
  what: rebuilt
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s02-question-book-structure/s02-question-book-structure.mindmap.md
  what: rebuilt, English
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s03-dataprep-structure/s03-dataprep-structure.mindmap.md
  what: rebuilt, English
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/page-spec/example-types.json
  what: English type names
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s01-insight-board-structure/s01-insight-board-structure.md
  what: Topic says the new levels
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/insight/workbench-insight/ref/block-structure.md
  what: English only; the Board row's levels
changed:
- examples/Project-Ladder/blueprint/b11_theme_insight/trace/261127/1211_s01_board_structure_english.md
---

# s01 board structure in English, by question version

## Prompts

- **12:11** go ahead and update s01

## Check

- check_structure.py: PASS, with new guards: Board levels, newest Job first, I01's Runs, no visible Chinese
- rebuilt map nodes read question-v1 → j03 · data-v2 · prep-v1, j02 · data-v2, j01 · data-v1 → Prep/Data/…/Executive → Tasks → Runs; Studio page 200 on 5623
- Chrome not checked: the browser extension was not connected

## Summary

s01's map reads as the live Jobs page (question version, Job, Task kind, Task, Run), with no Job Type level; s01 to s03 labels are English.

