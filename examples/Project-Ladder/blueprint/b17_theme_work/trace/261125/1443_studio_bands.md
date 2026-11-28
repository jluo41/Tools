---
title: studio bands
date: 2026-11-25 14:43
aim: The Studio section reads like Main; a row of group buttons, one band per group, each topic a numbered fold that opens its Slide, Draw, MindMap in place.
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1443_studio_bands.md
    what: this trace's own record, written first
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
    what: bands by group and numbered folds in place of the left list and one card
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/block_index_page/focus_render.py
    what: the Studio views bar lists All and every group, as Main lists its views
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1443_studio_bands.md
  - plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
  - plugins/haipipe-toolkit/servers/workbench/page/block_index_page/focus_render.py
---

# studio bands

## Prompts

- **14:40** How do you think we can make it like this structure? (Main: views row, bands, numbered folds)
- **14:43** yes, could you try and do it?

## Check

- 5623 b17 section=studio in Chrome: buttons All, Skill, All pages, Block UI, Job UI, Task UI; bands Skill 2, All pages 1, Block UI 3, Job UI 3, Task UI 3, Other 2; opening 1 · Work ladder loads its Slide in place; the Block UI button shows only its band.
- workbench tests: 230 passed; workbench-work: the same 3 failures with and without this change (test_work_progress).

## Summary

Studio no longer has a left list and one card: one band per group (Main's heading style), each topic a numbered fold
(🎨 name, stage pill, ☆) that opens its goal, Slide, Draw, MindMap, Work, Delivery in place; the views bar lists every
group. A #sNN link opens its fold.
