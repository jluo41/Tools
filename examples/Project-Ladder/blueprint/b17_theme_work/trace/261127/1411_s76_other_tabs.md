---
title: 's76: a skill''s other folders and loose files on the left'
date: 2026-11-27 14:11
topic: s76-studio-type-skills
aim: 'A skill''s left tabs are its whole top level: SKILL, Rules, ref, scripts, then one tab per other folder, then other (its loose files); s76 shows the same with 〈folder〉 and other.'
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1411_s76_other_tabs.md
  what: this trace's own record, written first
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/folder_folds.py
  what: a folder item may skip named files
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_views.py
  what: reads the item's skip list
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/tests/test_folder_folds.py
  what: a test for skipped files
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s76-studio-type-skills/elements.md
  what: requirements for 〈folder〉 and other
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s76-studio-type-skills/ (delivery/requirements, studio-views.json)
  what: rebuilt
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s51-skills-work, s52-skills-blueprint, s53-skills-cowork, s54-skills-discovery, s60-skill-studio, s61-skill-trace (studio-views.json)
  what: the new tabs
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1411_s76_other_tabs.md
- plugins/haipipe-toolkit/servers/workbench/studio/tabs/folder_folds.py
- plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_views.py
- plugins/haipipe-toolkit/servers/workbench/studio/tabs/tests/test_folder_folds.py
- examples/Project-Ladder/blueprint/b17_theme_work/s76-studio-type-skills/elements.md
- examples/Project-Ladder/blueprint/b17_theme_work/s76-studio-type-skills/ (delivery/requirements rebuilt, studio-views.json)
- examples/Project-Ladder/blueprint/b17_theme_work/s51-skills-work, s52-skills-blueprint, s53-skills-cowork, s54-skills-discovery, s60-skill-studio, s61-skill-trace (studio-views.json)
---

# s76: a skill's other folders and loose files on the left

## Prompts

- **14:11** for things here, it should be more, right? should we add <other>, etc.
- **14:11** go

## Check

- studio tabs tests: 29 passed, 1 new (skipped files)
- type_requirements.py --check on s76: 6 requirement pages, not stale
- 5623 restarted; served Studio: s76 left SKILL, Rules, ref, scripts, 〈folder〉, other; every one of the 19 skills shows its other folders and other
- all 215 fold addresses answer 200; not clicked in a browser

## Summary

A skill's left tabs are now its whole top level: after scripts come its other folders by name, then other for its loose files; s76 states both as requirements.

