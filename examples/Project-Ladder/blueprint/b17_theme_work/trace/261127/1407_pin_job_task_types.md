---
title: Job and Task types pinned per Block type
date: 2026-11-27 14:07
topic: s71-studio-type-block-structure
aim: Each Block Structure instance pins its Block type's four lists (Job group types, Job types, Task group types, Task types) in a types.md; s71 states the requirement; a check finds a Job or Task whose type is not listed. Work (s01) first.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1407_pin_job_task_types.md
  what: this trace's own record, written first
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/elements.md
  what: Job-Task must pin the four lists in types.md; pages rebuilt
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/s01-work-ladder/types.md
  what: 'Work: Job group types, Job types, Task group types, Task types'
- do: add
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/block_types_check.py
  what: every Job and Task type of the example Block is one its types.md lists
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1407_pin_job_task_types.md
- examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/elements.md
- examples/Project-Ladder/blueprint/b17_theme_work/s01-work-ladder/types.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/block_types_check.py
---

# Job and Task types pinned per Block type

## Prompts

- **14:07** go

## Check

- block_types_check: 1 Block type pinned (Work), 0 problems over b01's 11 Jobs and 16 Tasks; s71's Job-Task requirement page rebuilt with the four lists

## Summary

Work's Job group types, Job types, Task group types and Task types are pinned in s01/types.md; s71 requires it; a check holds it.

