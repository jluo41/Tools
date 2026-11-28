---
title: Studio Type band starts at s70; theme Guide to s8N
date: 2026-11-27 13:04
topic: s02-blueprint-structure
aim: The Studio Type topics are s70-s79 (last digit = the band each defines), the theme Guide band is s8N; every reader of the types follows.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1304_studio_type_s7n.md
  what: this trace's own record, written first
- do: move
  path: examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure
  what: to s70-...; s81-s89 to s71-s79 (Studio Type s77, Theme Guide s78)
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_types.py
  what: glob s7N
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/build_organization.py
  what: glob s7N; tree rebuilt
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/new_topic.py
  what: bands type 70-79, guide 81-89; glob s7N
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/topic-numbering.md
  what: s7N Studio Type, s8N theme Guide (SKILL.md, ui-preview-topic.md the same)
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1304_studio_type_s7n.md
- plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_types.py
- examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/build_organization.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/new_topic.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/topic-numbering.md
---

# Studio Type band starts at s70; theme Guide to s8N

## Prompts

- **13:04** for the studio type, I want it strated from s70, do you get it?

## Check

- served b17 Studio: 🏷️ Studio Type s70-s79; s02 tree: s7N Studio Type, s8N Theme Guide; studio 19, hai-studio 42 pass; b17 titles clean

## Summary

Studio Type topics are s70-s79 (s77 Studio Type itself), the theme Guide band s8N; every reader follows.

