---
title: title caret
date: 2026-11-25 11:44
aim: The ▾ beside the section word in a page title reads as part of a menu button, crisp and aligned.
closed: true
plan:
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/block_index_page/focus_shell.py
    what: the ▾ glyph becomes an inline chevron drawn to sit on the word's middle
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/focus-assets/focus.css
    what: chevron size, colour, turn when open; the button's hover shape
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1144_title_caret.md
  - plugins/haipipe-toolkit/servers/workbench/page/block_index_page/focus_shell.py
  - plugins/haipipe-toolkit/servers/workbench/focus-assets/focus.css
  - plugins/haipipe-toolkit/servers/workbench/focus-assets/focus.js
  - plugins/haipipe-toolkit/servers/workbench/tests/test_focus_faces.py
  - plugins/haipipe-toolkit/servers/workbench/tests/test_focus_status_map.py
---

# title caret

## Prompts

- **11:44** [image] [image] HOW COULD YOU MAKE THIS ONE TO BE BETTER?

## Check

- workbench 230 passed (two tests now look for the drawn chevron).
- b17 on 5623: chevron sits on the word's middle; hover and open turn it accent; open turns it up.
- Found on the way: Esc did not close the menu (focus went to the hidden Files row); fixed in focus.js, checked live.

## Summary

The ▾ text glyph is now a drawn chevron, centred, 14px, that turns up while the menu is open, inside a soft
rounded hover. The menu takes focus on its first visible row and closes on Esc from anywhere.
