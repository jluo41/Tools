---
title: studio tabs narrow
date: 2026-11-25 15:55
aim: A Studio fold's left tab list is only as wide as its longest name (Delivery), so the content gets the rest.
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1555_studio_tabs_narrow.md
    what: this trace's own record, written first
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
    what: STYLE scopes `.studio-topic-content .pb-side` to a max-content first column, 8px gap, tighter tab padding (wide screens only; the phone layout keeps tabs on top)
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1555_studio_tabs_narrow.md
  - plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
---

# studio tabs narrow

## Prompts

- **15:55** could we make this as narraw as posible. [the Studio fold's left tab list: Page, Draw, MindMap, Delivery at 170px]
- **16:00** ok

## Check

- 5623 b17 Studio s04: the tab list is as wide as Delivery (about 80px), the slide fills the rest; workbench 234 pass.

## Summary

Only Studio's side tabs shrink to `max-content` (wide screens); the shared `PB_CSS` and the UI view's 170px stay.
