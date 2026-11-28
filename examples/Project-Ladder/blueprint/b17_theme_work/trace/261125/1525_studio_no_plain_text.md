---
title: studio no plain text
date: 2026-11-25 15:25
aim: An open Studio fold carries no plain-text line (the topic's sentence moves to a hover on the fold title) and shows its Draw, MindMap, Work and Delivery as left tabs with the content on the right; AGENTS.md says why (the UI explains itself).
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1525_studio_no_plain_text.md
    what: this trace's own record, written first
  - do: edit
    path: AGENTS.md
    what: UI design gains the principle; a sentence that restates what the layout, a mark or a control already shows is cut, kept only on hover
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
    what: drop the studio-goal line (topic sentence + "ui" pill) and "No preview available yet."; the sentence becomes the fold title's hover; the Draw/MindMap/Work/Delivery button row becomes ui_parts._side_tabs (left list, right panel), each frame loading when its tab shows
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1525_studio_no_plain_text.md
  - AGENTS.md
  - plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
  - plugins/haipipe-toolkit/servers/workbench/tests/test_focus_studio.py
---

# studio no plain text

## Prompts

- **15:25** a trace (`trace/<YYMMDD>/<HHMM>_<slug>.md`) is one piece of work with its plan written first.ui I dont wnat this, add the princile to AGENTS.md, try to remove the plain text, and let the UI explain themsevel.
- **15:35** do you think here should we have the left-tab right panel? we should do that, plsae think about it.
- **15:45** can you try to do it?

## Check

- 5623 b17 Studio, s04 open: no sentence line, no type pill; Slide · Draw · MindMap · Work · Delivery as left tabs; Slide loads first, Draw shows its picture on click; the fold title's hover is the topic's sentence (none for s03, s05, whose face still holds the template's <placeholder>).
- workbench 234 pass (four studio asserts moved: no studio-goal, no type pill, `<b>Draw</b>`, `<b>Delivery</b>` tabs).

## Summary

A Studio fold now holds only the topic itself: its 🙋 Interaction when one waits, then its views as `ui_parts._side_tabs`.
The topic's sentence is the hover of the fold's title. AGENTS.md › UI design says it for every page: no plain-text line
that restates what the layout shows, and several things in one fold are left tabs.
