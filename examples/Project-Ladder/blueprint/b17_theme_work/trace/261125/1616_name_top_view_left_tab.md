---
title: name top view left tab
date: 2026-11-25 16:16
aim: The layout inside an open fold (view buttons on top, the picked view's things as left tabs, the picked thing on the right in a frame with a hide dot top-left and an open dot top-right) has one name, top-view-left-tab-right-content, and one ref that says it.
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1616_name_top_view_left_tab.md
    what: this trace's own record, written first
  - do: add
    path: plugins/haipipe-toolkit/servers/workbench/ref/top-view-left-tab-right-content.md
    what: the pattern; its three parts and two dots, when a view has one thing, the phone layout, the code (ui_parts._side_tabs, open_dot, studio_tabs.page_items) and Studio s31 as the example
  - do: edit
    path: plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/SKILL.md
    what: the Page parts table names it under fold, with a link to the ref
  - do: edit
    path: AGENTS.md
    what: the UI design line calls it by its name and links the ref
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1616_name_top_view_left_tab.md
  - plugins/haipipe-toolkit/servers/workbench/ref/top-view-left-tab-right-content.md
  - plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/SKILL.md
  - AGENTS.md
  - plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
  - plugins/haipipe-toolkit/servers/workbench/page/parts_and_map/ui_parts.py
---

# name top view left tab

## Prompts

- **16:16** I want to give it a name, this framework, add it to the ref/ we can call it top-review-left-tab-right-contnet, how do you think about it? [Studio s31: Page Draw MindMap Delivery on top, the frame with a dot on each top corner]
- **16:20** ok

## Check

- `grep -rn top-view-left-tab` finds the ref, hai-ui SKILL.md's Page parts row, AGENTS.md › UI design, and the
  comments in studio_tabs.render and ui_parts._side_tabs. workbench 236 pass.

## Summary

Named top-view-left-tab-right-content ("view", not "review": the top row is view buttons, like view-button-list).
The ref holds its three parts, its two dots, the one-thing and phone cases, the code and s31 as the example. Two
comment lines in code point to it; no behaviour changed.
