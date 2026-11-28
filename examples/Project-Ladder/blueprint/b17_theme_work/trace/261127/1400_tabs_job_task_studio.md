---
title: The Block Structure tabs read Folder, Job-Task, Studio
date: 2026-11-27 14:00
topic: s71-studio-type-block-structure
aim: The three left tabs of a Block Structure topic are Folder, Job-Task and Studio, in the type s71, its instances s01-s04, the builder and the skill references.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1400_tabs_job_task_studio.md
  what: this trace's own record, written first
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/elements.md
  what: tab names; requirement pages and views rebuilt
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s01-work-structure/studio-views.json
  what: tab names (s02, s03, s04 and their faces the same)
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/build_organization.py
  what: LABELS; check_organization.py follows; pages rebuilt
- do: edit
  path: plugins/haipipe-toolkit/skills
  what: the three reference files and studio_views wording that name the tabs
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1400_tabs_job_task_studio.md
- examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/elements.md
- examples/Project-Ladder/blueprint/b17_theme_work/s01-work-structure/studio-views.json
- examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/build_organization.py
---

# The Block Structure tabs read Folder, Job-Task, Studio

## Prompts

- **14:00** change this to Folder, Job-Task, Studio, okay?

## Check

- served Studio: s71 and s01-s04 show Folder, Job-Task, Studio; s71's 11 requirement pages rebuilt; organization pages rebuilt (check stops only at the old work folder hash); workbench failures are all in the known draft-reader set

## Summary

The three Block Structure tabs read Folder, Job-Task, Studio in b17 and the skill references.

