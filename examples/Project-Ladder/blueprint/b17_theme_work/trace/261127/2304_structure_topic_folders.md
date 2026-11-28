---
title: structure topic folders
date: 2026-11-27 23:04
aim: 'Each b17 Studio topic''s folder says what its title says: s01-work-structure, s02-blueprint-structure, s03-cowork-structure, s04-discovery-structure, s62-skills-project, with every mention in plugins/ and examples/ following.'
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2304_structure_topic_folders.md
  what: this trace's own record, written first
- do: move
  path: examples/Project-Ladder/blueprint/b17_theme_work/s01-work-structure/
  what: to s01-work-structure, its named files with it
- do: move
  path: examples/Project-Ladder/blueprint/b17_theme_work/s02-blueprint-structure/
  what: to s02-blueprint-structure, its named files with it
- do: move
  path: examples/Project-Ladder/blueprint/b17_theme_work/s03-cowork-structure/
  what: to s03-cowork-structure, its named files with it
- do: move
  path: examples/Project-Ladder/blueprint/b17_theme_work/s04-discovery-structure/
  what: to s04-discovery-structure, its named files with it
- do: move
  path: examples/Project-Ladder/blueprint/b17_theme_work/s62-skills-project/
  what: to s62-skills-project, its named files with it
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/ (every file that names one of the five)
  what: the new folder names
- do: edit
  path: examples/ (Project-Packages b01, Project-PageParts b35, b15, b16)
  what: the new folder names
- do: edit
  path: plugins/haipipe-toolkit/ (hai-studio, hai-ladder and workbench-work skills, servers/workbench-work)
  what: the new folder names
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2304_structure_topic_folders.md
---

# structure topic folders

## Prompts

- **23:04** how do you update it. Please update them accoridngly

## Check

- Five folders renamed with the 62 files and folders inside that carried the old name; 228 files updated; no old name left in plugins/ or examples/ outside CHANGELOG.md, references/ and binary files
- Live on 5623 in Chrome: the Studio page lists s01-work-structure to s05-knowledge-structure and s62-skills-project, no old name on the page, each topic link lands on its topic, s01 opens with its views, no failed request; the Files pane shows the new folder names
- Server tests 449 passed; the failures are not from this change: 5 in test_standalone_server.py (403 != 400 and page text), tests needing pandas, pyarrow or pillow pass once those are installed, and test_type_follow.py fails on a TypeError in code another session is changing
- s05 build_structure.py rebuilt and its check passes. s01's builder has no --check and redrew s01-work-structure.excalidraw when run; s02's and s04's builders fail on their own (they read page code that has since changed)

## Summary

The five Studio topics whose folder no longer matched its title are renamed to match: s01-work-structure, s02-blueprint-structure, s03-cowork-structure, s04-discovery-structure, s62-skills-project, with their named files and every mention following.

