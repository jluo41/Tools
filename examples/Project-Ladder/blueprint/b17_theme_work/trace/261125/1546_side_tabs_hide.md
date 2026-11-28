---
title: side tabs hide
date: 2026-11-25 15:46
aim: Any left tab list (ui_parts._side_tabs) can be hidden with one small handle on its edge; hidden, the content takes the full width and a thin strip with › brings the list back; the choice is remembered in this browser.
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1546_side_tabs_hide.md
    what: this trace's own record, written first
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/parts_and_map/ui_parts.py
    what: _side_tabs adds a ‹ handle at the list's top; PB_CSS draws `.pb-side.pb-folded` (list a 22px strip with ›, content full width); PB_JS toggles it and keeps it in localStorage (wb:pb-folded)
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/tests/test_focus_studio.py
    what: a side tab list carries its hide handle
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1546_side_tabs_hide.md
  - plugins/haipipe-toolkit/servers/workbench/page/parts_and_map/ui_parts.py
  - plugins/haipipe-toolkit/servers/workbench/tests/test_focus_studio.py
---

# side tabs hide

## Prompts

- **15:46** How could i hide the left panel if I want? [the Studio fold's left tabs: Metro map, Marks + card, ...]
- **15:50** plse do it.

## Check

- 5623 b17 Studio s31: ‹ at the list's top; a click hides the list, Metro map takes the full width; › brings it back.
- workbench 236, labeling 85, paper 112, design 58 pass.

## Summary

`_side_tabs` puts a `.pb-fold` handle first in every left list; `PB_JS` toggles `pb-fold-on` on `<html>` and keeps it in
`localStorage['wb:pb-folded']`, so one choice holds for every list in this browser. Phones (≤700px) keep the tabs on
top and show no handle.
