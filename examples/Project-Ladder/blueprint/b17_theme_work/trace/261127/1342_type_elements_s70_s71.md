---
title: A Studio type defines its elements; instances and right-click read them (s70, s71)
date: 2026-11-27 13:42
topic: s77-studio-type-studio-type
aim: 'A Studio Type topic is the class of its band''s topics: its elements.md names each element with what it is, why it exists and where its data comes from; the type shows them live in an Elements view laid out like an instance, and a right-click on that element anywhere (the type, an instance, the real page) shows the type''s what and why.'
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1342_type_elements_s70_s71.md
  what: this trace's own record, written first
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/elements.md
  what: Folder, Job / Task Organization, Studio Organization, Draw, Examples, Skills
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/elements.md
  what: Job type row, Job group row, Job row, Main, Task group row, Task row
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_types.py
  what: read elements.md; the Elements view; the right-click entries
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
  what: a type topic opens on its Elements view
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/page/element_marks/element_info.py
  what: the card and menu show a type element's what, why and source
- do: add
  path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/tests/test_studio_types.py
  what: elements parse, the view, the right-click entries
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1342_type_elements_s70_s71.md
- examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/elements.md
- examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/elements.md
- plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_types.py
- plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
- plugins/haipipe-toolkit/servers/workbench/page/element_marks/element_info.py
- plugins/haipipe-toolkit/servers/workbench/studio/tabs/tests/test_studio_types.py
---

# A Studio type defines its elements; instances and right-click read them (s70, s71)

## Prompts

- **13:42** plese make the s70 and s71 first, go.

## Check

- served Studio: s70 opens on Elements (6 tabs, all 200), s71 on Elements (6 rows of b01's Jobs page, each with mark=); the Jobs page carries the six right-click entries and their selectors exist on it; workbench 361 pass (6 known draft-reader failures); the card script parses (node --check); not clicked in a browser, the extension is disconnected

## Summary

s70 and s71 define their elements in elements.md; the type shows them live, and a right-click on an element shows the type's what, why and source.

