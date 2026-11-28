---
title: 'More icons for Studio drawings: downloaded libraries, used by name'
date: 2026-11-27 21:38
topic: s60-skill-studio
aim: A builder draws any item of a downloaded Excalidraw library by its name, so adding icons is adding a library file
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2138_studio_icon_libraries.md
  what: this trace's own record, written first
- do: add
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/icons/libraries/
  what: a few Excalidraw public libraries (.excalidrawlib), as downloaded
- do: add
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/icon_library.py
  what: draw a library item by name at a place and size; list and picture every item
- do: add
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/tests/test_icon_library.py
  what: tests
- do: add
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/icon-libraries.md
  what: where the libraries come from, how to add one, how a builder uses an item
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/SKILL.md
  what: name the script and the ref; also CHANGELOG.md
- do: edit
  path: references/sources.yaml
  what: each library's origin and license
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2138_studio_icon_libraries.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/icon_library.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/tests/test_icon_library.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/icon-libraries.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/SKILL.md
- references/sources.yaml
---

# More icons for Studio drawings: downloaded libraries, used by name

## Prompts

- **21:38** okay, think about it. You just add it and save it.

## Check

- hai-studio tests pass, with 5 new ones: every item of every kept library draws
- ref/icons/libraries.png rendered and looked at: 173 items in four libraries, named
- s60 drawing rebuilt with two library items (Ideation, Search) and looked at

## Summary

Four Excalidraw public libraries are kept in hai-studio ref/icons/libraries; icon_library.py draws any item by name. A fifth, dashboard-charts (4 MB), was looked at and not kept for its size.

