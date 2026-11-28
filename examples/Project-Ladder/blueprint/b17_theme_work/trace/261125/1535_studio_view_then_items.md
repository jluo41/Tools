---
title: studio view then items
date: 2026-11-25 15:35
aim: An open Studio fold reads like a page; the view buttons on top (Page, Slide, Draw, MindMap, Work, Delivery) pick the kind, the left tabs list the things inside that view (s31's Page, Metro map, Tree + timeline, Marks + hover card, First trace tree), and the right shows the picked one. A view with one thing has no left tabs.
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1535_studio_view_then_items.md
    what: this trace's own record, written first
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
    what: a row of view buttons on top of the fold; each view's panel is its items as ui_parts._side_tabs when there are two or more (Page, its own data-src buttons; Draw, the topic's drawings), else the one item full width
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/tests/test_focus_studio.py
    what: the view buttons are back; a Page with data-src buttons lists them as left tabs
  - do: edit
    path: AGENTS.md
    what: the UI design line reads "a fold's kinds are view buttons on top; the things inside one view are left tabs", not "never a row of buttons"
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1535_studio_view_then_items.md
  - plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
  - plugins/haipipe-toolkit/servers/workbench/tests/test_focus_studio.py
  - AGENTS.md
---

# studio view then items

## Prompts

- **15:35** I think in the top here, we can still have the view button [Page, Draw, MindMap, Delivery] How do you think? maybe the left tab should be [Metro map, Tree + timeline, Marks + hover card, First trace tree], go ahead and think about the plan.
- **15:40** I might want this [Page, Draw, MindMap, Delivery] to be on the top, do you know, and these [Metro map, Marks + card, Earlier: Metro by trace, Tree + timeline, First trace tree] to be in the left, do you get it?

## Check

- 5623 b17 Studio s31: Page · Draw · MindMap · Delivery on top; Page's left tabs Metro map, Marks + card, then Metro by trace, Tree + timeline, First trace tree faded; Metro map loads on the right.
- workbench 236 pass (new test_a_topic_page_lists_its_previews_as_left_tabs; Draw and Delivery asserts back to buttons).

## Summary

`studio_tabs.page_items` reads the `<button data-src>` of a topic's own page (missing files and outside links dropped,
`class="old"` read as earlier and faded). The fold has view buttons on top; a view with two or more things shows them
as `_side_tabs`, else the one thing full width. AGENTS.md › UI design says the same for every fold.
