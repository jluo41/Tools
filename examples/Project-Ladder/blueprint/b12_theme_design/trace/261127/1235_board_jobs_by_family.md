---
title: "Design Board Jobs grouped by method family"
date: 2026-11-27 12:35
topic: s01-design
aim: A Design Board keeps one Job Type; its Job topics group Jobs by the pinned method's family (Goal Only, External, Internal) instead of by goal, and each Job's label names its goal.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b12_theme_design/trace/261127/1235_board_jobs_by_family.md
  what: this trace's own record, written first
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench-design/design_jobs.py
  what: topic() groups a Board Job by its method's registry family; label() adds the goal id
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench-design/tests/test_design_jobs.py
  what: Board groups by family and the label names goal, method and inputs
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/s01-design/delivery/organization.mindmap.md
  what: Grouping line says method family
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/s01-design/delivery/structure.md
  what: Job topic is the method family; selector label with goal
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/design/workbench-design/SKILL.md
  what: Work Details groups one per method family
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/design/workbench-design/ref/topics.md
  what: T14 Board Jobs by method family, with its guard
changed:
- examples/Project-Ladder/blueprint/b12_theme_design/trace/261127/1235_board_jobs_by_family.md
---

# Design Board Jobs grouped by method family

## Prompts

- **12:2x** [screenshot of s01's mind map: Design Board → job type Design execution] we jus t have one type of job here? for the design?
- **12:3x** but we can still group the design by the design types, how do you think? or we just have one job type?
- **12:35** go ahead adn try it.

## Plan details

- One Job Type stays: every Board Job holds the same folders whatever its method.
- The family comes from the method registry (`hai-design-method/methods/M0x-*/method.md` `family:`),
  read by `design_reader.registry()`; the Job's pinned `inputs/method.md` has no family line.
- A Job whose method is not in the registry falls back to its goal group.

## Check

- `pytest servers/workbench-design/tests`: 68 passed, 298 subtests passed.
- Restarted the Tools host on 5623 with its existing command; Design-Example's Jobs show two groups, Goal Only
  (j01 · G01 · M01 m2 · inputs-v1, j02 · G01 · M01 m2 · inputs-v2) and Internal (j03 · G01 · M02 m1 · inputs-v2).

## Summary

One Job Type kept. Board Jobs group by their method's registry family; the goal moved into each Job's label.
