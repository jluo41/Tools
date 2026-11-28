---
title: studio own snn
date: 2026-11-25 15:18
topic: s31-files-pane
aim: A page's Studio lists the sNN that sit in its own folder, in number order, each row named sNN · title; topics inside its Jobs and Tasks stay on their own pages.
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1518_studio_own_snn.md
    what: this trace's own record, written first
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/block_index_page/focus_render.py
    what: the Studio section keeps the page's own topics (all of them when it has none of its own); no group buttons
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
    what: one list in sNN order, no group bands, sNN in each row's title
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/tests/test_focus_studio.py
    what: a Block shows its own topics only, each with its sNN
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1518_studio_own_snn.md
  - plugins/haipipe-toolkit/servers/workbench/page/block_index_page/focus_render.py
  - plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
  - plugins/haipipe-toolkit/servers/workbench/tests/test_focus_studio.py
---

# studio own snn

## Prompts

- **15:14** I didn't find s31. for here I didn;t find the name of sNN
- **15:16** we only have [s01 to s31] why we have so many these? could you just display these sNN?
- **15:18** go ahead and do it.
- **15:20** we only have sNN in the block root, right?

## Check

- 5623 Studio: b17 lists s01 to s31 in order (s31 · 🎨 Files pane); t03_task_page lists s57 to s59; j03, with no sNN
  of its own, lists its Tasks' s51 to s59.
- workbench tests: 234 passed; test_focus_studio's group-filter test became the own-sNN test (JL's new rule replaces
  the group buttons of 261029).

## Summary

A page's Studio is one list of the sNN in its own folder, in number order, each fold named `sNN · 🎨 title`, no group
bands or buttons; a page with none of its own shows its children's. b17 also holds s51 to s59 inside j03's three Tasks.
