---
title: question levels expanded
date: 2026-11-27 13:02
aim: The Task group of a Board and a Book reads as one group per question level (Data, Information, Knowledge, Wisdom, Executive), each with its own Task name pattern
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b11_theme_insight/trace/261127/1302_question_levels_expanded.md
  what: this trace's own record, written first
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/build_structure.py
  what: one Task group per level
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
- examples/Project-Ladder/blueprint/b11_theme_insight/trace/261127/1302_question_levels_expanded.md
---

# question levels expanded

## Prompts

- **13:02** for these, it should be four groups, right? expand them.

## Check

- check_structure.py PASS; Board jobs-rules: Prep + Data, Information, Knowledge, Wisdom, Executive groups, each with its tNN 〈L〉NN 〈question〉; Book the same five

## Summary

Each question level is its own Task group.

