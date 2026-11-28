---
title: A Studio type's right side is the requirement
date: 2026-11-27 13:55
topic: s71-studio-type-block-structure
aim: A type and its instances share the top buttons and left tabs; the type's right side says what that tab must show and why (What, Why, Must show, From, Check), the instance's right side is the real thing. Built for s71 from its elements.md.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1355_s71_right_side_requirements.md
  what: this trace's own record, written first
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/elements.md
  what: one requirement per view and tab, grouped by view
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/studio-views.json
  what: 'generated: each tab opens its requirement page'
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/delivery/requirements
  what: generated pages, one per view and tab
- do: add
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/type_requirements.py
  what: build a type's requirement pages and views from its elements.md
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_types.py
  what: elements grouped by view, must and check lines; right-click finds a tab inside its own view
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/tests/test_studio_types.py
  what: views, must lines, per-view right-click
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1355_s71_right_side_requirements.md
- examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/elements.md
- examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/studio-views.json
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/type_requirements.py
- plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_types.py
- plugins/haipipe-toolkit/servers/workbench/studio/tabs/tests/test_studio_types.py
---

# A Studio type's right side is the requirement

## Prompts

- **13:55** pelase go ahead and do it.
- **13:58** I asked these should be merged together, remoe [the Skill band heading]

## Check

- served Studio: s71 and s01 have the same four buttons and the same left tabs in Structure, Draw and Examples; s71's right side opens its requirement pages (11, built, --check clean); right-click entries tell Folder under Structure, Draw and Examples apart; Skills band holds s51-s54, s60, s61 under one heading; workbench tests as before

## Summary

s71's right side is the requirement of each tab, built from elements.md; hai-studio A06 holds the rule; s60 and s61 sit in the Skills band.

