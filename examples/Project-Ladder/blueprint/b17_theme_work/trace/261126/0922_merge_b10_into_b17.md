---
title: Merge b10 into b17
date: 2026-11-26 09:22
aim: b10's topics, chat, page spec and related move into b17 as one Job, b10 is removed, and every link to b10 points at its new place.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261126/0922_merge_b10_into_b17.md
  what: this trace's own record, written first
- do: move
  path: examples/Project-Ladder/blueprint/b17_theme_work/j16_project_structure
  what: from examples/Project-Ladder/work/b10_project_workbench (its 22 sNN topics keep their names)
- do: move
  path: examples/Project-Ladder/blueprint/b17_theme_work/c01_plugin_principle_and_chat
  what: from examples/Project-Ladder/work/b10_project_workbench/c01_plugin_principle_and_chat
- do: move
  path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/page-spec/project-views.md
  what: from examples/Project-Ladder/work/b10_project_workbench/delivery/page-spec/project-views.md (with view-guide, preview)
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/board.md
  what: a line for the new Job and the chat
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench
  what: b10 paths in ref, guide, workbench-work
- do: edit
  path: plugins/haipipe-toolkit/skills
  what: b10 paths in response-format, hai-paper
- do: edit
  path: blueprints
  what: b10 paths in b11, b12, b15, b16, b17 and other Projects
- do: delete
  path: examples/Project-Ladder/work/b10_project_workbench
  what: after the move, with its _old and runs
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261126/0922_merge_b10_into_b17.md
---

# Merge b10 into b17

## Prompts

- **09:22** examples/Project-Ladder/work/b10_project_workbench I think we can delete this, and merge this into the b17, how do you think about it?

## Check

- not done: replaced by 0939_delete_b10 (JL chose to delete b10, not merge it); c01 became trace 261121/0046

## Summary

Dropped: b10 was deleted instead of merged, so nothing here was made.

