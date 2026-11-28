---
title: side tabs dot
date: 2026-11-25 16:00
aim: The left list's hide handle is a dot, not ‹ ›; hidden, the list leaves no column, the content starts at the left edge and the dot sits on the content's top-left corner.
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1600_side_tabs_dot.md
    what: this trace's own record, written first
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/parts_and_map/ui_parts.py
    what: PB_CSS draws .pb-fold as a 8px grey dot (accent on hover); hidden, `.pb-side` is one column and the dot is absolute on the content's top-left corner
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1600_side_tabs_dot.md
  - plugins/haipipe-toolkit/servers/workbench/page/parts_and_map/ui_parts.py
---

# side tabs dot

## Prompts

- **16:00** I wnat this [the › strip] to be a point, and I don't want to have the margin, do you know howto do it?
- **16:05** ok, go ahead and dupdate it.

## Check

- 5623 b17 Studio s31: a grey dot above the list; a click hides the list, the content starts at the left edge with the dot on its corner; a second click brings the list back. workbench 236.

## Summary

`.pb-fold` is a dot (`::before`, 8px); hidden, `.pb-side` is one column and its `.pb-list` (the dot alone) is absolute at -9px,-9px, so it takes no width. Phones reset it to static.
