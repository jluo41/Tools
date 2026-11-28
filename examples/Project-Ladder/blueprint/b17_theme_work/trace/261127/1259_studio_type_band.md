---
title: 'Studio Type band: one topic per Studio type, the one list'
date: 2026-11-27 12:59
topic: s02-work-skills
aim: Each Studio type is its own topic in b17's s8N Studio Type band (s80-s89, last digit = the band it defines); the Studio page, the s02 tree, new_topic.py and the title check read the band names from them.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1259_studio_type_band.md
  what: this trace's own record, written first
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure
  what: 'Studio Type: Block Structure (and s81-s89: Block Job UI Preview, Report, Theme Guide, Task Procedure, Skills, Slide Draft, UI Plugin, Studio Type, Guide)'
- do: add
  path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_types.py
  what: 'read the Studio Type topics: {digit: (emoji, name, holds)}'
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
  what: a blueprint Block's bands from the types, board.md adds or renames
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/tests/test_studio_bands.py
  what: bands read from type topics
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/build_organization.py
  what: BLUEPRINT_BANDS from the types; check_organization.py follows; tree rebuilt
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/board.md
  what: s bands dropped (the types hold them)
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/new_topic.py
  what: band_name falls back to the types
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/topic-numbering.md
  what: points to the Studio Type topics
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1259_studio_type_band.md
- plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_types.py
- plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
- plugins/haipipe-toolkit/servers/workbench/studio/tabs/tests/test_studio_bands.py
- examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/build_organization.py
- examples/Project-Ladder/blueprint/b17_theme_work/board.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/new_topic.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/topic-numbering.md
---

# Studio Type band: one topic per Studio type, the one list

## Prompts

- **12:59** yes, please go ahead and do it.
- **13:02** I think this should be like s3N series, please update this again.

## Check

- served b17 Studio: 🧱 s01-s04 · 👀 s11-s14 · 🧩 s31 s32 · 🧰 s51-s54 · 🏷️ s80-s89 · 🧭 s99; s02 tree lists the ten types read from s80-s89; workbench 356 pass (6 known draft-reader failures), studio 19 and hai-studio 42 pass; topic_titles_check: b17 clean, 27 titles in b11, b12, b15, b16 for their sessions

## Summary

Each Studio type is its own topic (b17 s80-s89), the one list the Studio page, the s02 tree and hai-studio read; UI Plugin is s3N again (s31, s32), the theme Guide s7N.

