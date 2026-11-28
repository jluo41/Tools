---
title: open dot
date: 2026-11-25 16:10
aim: The "Open Metro map ↗" button under a preview becomes a dot on the preview's top-right corner; a click opens it, its name is the hover; no words. AGENTS.md says so for every preview.
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1610_open_dot.md
    what: this trace's own record, written first
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/parts_and_map/ui_parts.py
    what: open_dot(href, name, pop) and its CSS in PB_CSS; an 8px dot on the frame's top-right corner, on hover a round ↗ in the accent
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
    what: frame_of and the Draw picture use open_dot instead of "Open <name> ↗"
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/parts_and_map/focus_ui.py
    what: the UI view's live page uses open_dot instead of "Open <title> ↗"
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/tests/test_focus_studio.py
    what: a preview carries its open dot and no "Open … ↗" words
  - do: edit
    path: AGENTS.md
    what: UI design gains the rule; a preview opens from a dot on its corner, its name a hover, never an "Open X ↗" button
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1610_open_dot.md
  - plugins/haipipe-toolkit/servers/workbench/page/parts_and_map/ui_parts.py
  - plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
  - plugins/haipipe-toolkit/servers/workbench/page/parts_and_map/focus_ui.py
  - plugins/haipipe-toolkit/servers/workbench/tests/test_focus_studio.py
  - AGENTS.md
---

# open dot

## Prompts

- **16:10** remove the words, and make it to be something like d dot and I can click and open it, no words, add to the AGENTS.md [the "Open Metro map ↗" button under the preview]
- **16:15** ok

## Check

- 5623 b17 Studio s31 Metro map: the dot's centre is the frame's top-right corner (994, 527); hover "Open Metro map"; data-pop keeps the pop-out; no "Open Metro map ↗" text on the page.
- workbench 236, labeling 85, paper 112 pass.

## Summary

`ui_parts.open_dot(inner, href, name, pop, new_tab)` wraps a preview and puts an 18px link on its top-right corner: an
8px grey dot, a ↗ in the accent on hover. Studio (frames and the Draw picture) and the UI view's live page use it.
About 20 other "Open … ↗" in paper, insight and design pages are left to their owners; AGENTS.md › UI design now
states the rule.
