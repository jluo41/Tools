---
title: 's76: skills on top, a skill''s files on the left, a folder as folds'
date: 2026-11-27 14:05
topic: s75-studio-type-skills
aim: A Skills topic shows its skills as the top buttons and the picked skill's SKILL, Rules, ref and scripts as left tabs; a tab that is a folder shows one fold per file on the right, read live; s76 shows the same top and left with the requirement on the right.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1405_s76_top_is_skills.md
  what: this trace's own record, written first
- do: add
  path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/folder_folds.py
  what: a folder read live as one fold per file
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_views.py
  what: an item may name a folder
- do: add
  path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/tests/test_folder_folds.py
  what: folds, empty folder, path outside the SPACE
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s75-studio-type-skills/elements.md
  what: top 〈skill〉, left SKILL, Rules, ref, scripts, each with its requirement
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s75-studio-type-skills/ (delivery/requirements, studio-views.json, face)
  what: rebuilt; Holds line
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s51-skills-work, s52-skills-blueprint, s53-skills-cowork, s54-skills-discovery, s60-skill-studio, s61-skill-trace (studio-views.json, face)
  what: one top button per skill, its files on the left
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1405_s76_top_is_skills.md
- plugins/haipipe-toolkit/servers/workbench/studio/tabs/folder_folds.py
- plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_views.py
- plugins/haipipe-toolkit/servers/workbench/studio/tabs/tests/test_folder_folds.py
- examples/Project-Ladder/blueprint/b17_theme_work/s75-studio-type-skills/elements.md
- plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
- examples/Project-Ladder/blueprint/b17_theme_work/s75-studio-type-skills/ (delivery/requirements rebuilt, studio-views.json, face)
- examples/Project-Ladder/blueprint/b17_theme_work/s51-skills-work, s52-skills-blueprint, s53-skills-cowork, s54-skills-discovery, s60-skill-studio, s61-skill-trace (studio-views.json, one face line each)
---

# s76: skills on top, a skill's files on the left, a folder as folds

## Prompts

- **14:05** I think the top will just be the related skills? and in the left, is showing the skill content? like the first one will be the SKILL.md, but you will also have other things, right?
- **14:05** how do you think you can make the left better? if it is a folder, in the right content, could we make the right content to have the fold, and content as well?
- **14:05** go

## Check

- studio tabs tests: 28 passed, 4 of them new (folder folds)
- type_requirements.py --check on s76: 4 requirement pages, not stale
- 5623 restarted; served Studio: s76 top 〈skill〉, left SKILL, Rules, ref, scripts; s51-s54 one top button per skill; s60 hai-studio with 39 folds, s61 hai-trace with 1
- every fold's file address answers 200; not clicked in a browser (the Chrome extension was not connected)
- off the plan: studio_tabs.py (frame_of shows a folder as folds)

## Summary

A Skills topic now reads skill on top, the skill's SKILL, Rules, ref and scripts on the left, and a folder as one fold per file on the right; s76 shows the same top and left with the requirement on the right.

