---
title: effect view
date: 2026-11-26 10:10
work: [s11, j13t01]
aim: "A UI preview topic's quick html views move to their own top button, Effect, beside Page, Draw and Delivery; Page keeps the live pages the server renders."
closed: true
plan:
  - do: add
    path: blueprints/Project-Ladder/work/b17_theme_work/trace/261126/1010_effect_view.md
    what: this trace's own record, written first
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
    what: a topic page with both live and quick views shows Page (live) and Effect (quick) as two top buttons, each with its own left tabs
  - do: add
    path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/tests/test_effect_view.py
    what: a topic with live and quick views gets Page then Effect; a topic with only files keeps one Page
changed:
  - blueprints/Project-Ladder/work/b17_theme_work/trace/261126/1010_effect_view.md
  - plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
  - plugins/haipipe-toolkit/servers/workbench/studio/tabs/tests/test_effect_view.py
---

# effect view

## Prompts

- **09:36** I want to have a new view here, about the effect, [Image #6] which will be the quick hmtl and will be saved in the sNN delivery/ui, do you get it? [Image #10]
- **10:08** What I mean is putting the effect to [Image #13] why you still don't do it?

## Check

- test_effect_view.py 2 passed.
- 5623 restarted; b17's Studio shows s11 with Page, Effect, Draw, Delivery; Page holds Topic rows and Job Main (live), Effect holds Effects, Two rows, Path + menus, Rows (first) (the last three faded).
- 5602, 5607, 5599 restarted, 200.

## Summary

A UI preview topic now shows its live pages under Page and its quick html under Effect, two top buttons beside Draw and Delivery; a topic whose page lists only files keeps one Page.
