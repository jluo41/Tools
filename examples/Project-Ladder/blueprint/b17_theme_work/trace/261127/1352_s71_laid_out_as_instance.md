---
title: s71 is laid out as its instances are
date: 2026-11-27 13:52
topic: s71-studio-type-block-structure
aim: The type topic s71 shows the same views and left tabs as a Block Structure instance (Structure, Draw, Examples, Skills; Folder, Job / Task Organization, Studio Organization), not an Elements list; a right-click on any of them, in s71 or an instance, says what it is and why.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1352_s71_laid_out_as_instance.md
  what: this trace's own record, written first
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/studio-views.json
  what: the instance's four views and their tabs
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/elements.md
  what: Structure added; the elements are right-click words
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
  what: a type with its own views keeps them, no Elements view
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_types.py
  what: right-click finds the type's own view buttons too
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/tests/test_studio_types.py
  what: the type's view buttons are found
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1352_s71_laid_out_as_instance.md
- examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/studio-views.json
- examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/elements.md
- plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
- plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_types.py
- plugins/haipipe-toolkit/servers/workbench/studio/tabs/tests/test_studio_types.py
---

# s71 is laid out as its instances are

## Prompts

- **13:52** s71 should be the same, as a metaclass, should be the same layout as the studio class intance, do you get it?
- **13:53** let me know what is the top, left, and right?

## Check

- served Studio: s71 and s01 show the same views (Structure, Draw, Examples, Skills) and the same left tabs (Folder, Job / Task Organization, Studio Organization); right-click entries exist for s71's buttons and tabs; 52 tests pass

## Summary

s71 is laid out as its instance s01; its elements are right-click words.

