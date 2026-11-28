---
title: Job types and Task types are top views of a Block Structure topic
date: 2026-11-27 14:13
topic: s71-studio-type-block-structure
aim: 's71 and its instances show Job types and Task types beside Structure: the class lists placeholder slots with the requirement of a type, an instance lists its real types from types.md, each with its definition and the real Jobs or Tasks of that type. Work (s01) first.'
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1413_job_task_types_views.md
  what: this trace's own record, written first
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/elements.md
  what: two views, placeholder tabs; pages rebuilt
- do: add
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/block_types_pages.py
  what: an instance's type pages and its two views, from types.md
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s01-work-ladder/studio-views.json
  what: Job types and Task types views; delivery/types/ pages built
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/check_organization.py
  what: views found by name, the two new ones allowed
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
  what: a view's content carries its name
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_types.py
  what: right-click finds a tab by its view's name, not its position (test updated)
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1413_job_task_types_views.md
- examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/elements.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/block_types_pages.py
- examples/Project-Ladder/blueprint/b17_theme_work/s01-work-ladder/studio-views.json
- examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/check_organization.py
- plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
- plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_types.py
---

# Job types and Task types are top views of a Block Structure topic

## Prompts

- **14:13** go

## Check

- served Studio: s71 and s01 both show Structure, Job types, Task types, Draw, Examples, Skills; s71 lists the slots (Job group type 1, 2, Job type 1, 2; the same for Task), s01 the real types (Version, Ideas, code, check, doc; Make, Show, code, display); the code page lists b01's seven code Jobs; studio and element tests pass; one side_pane test fails in trace_view.py, changed by another session at 14:14

## Summary

Job types and Task types are top views of s71 (slots and their requirement) and of s01 (Work's real types with their Jobs and Tasks).

