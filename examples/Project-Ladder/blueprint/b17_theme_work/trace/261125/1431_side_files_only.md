---
title: side files only
date: 2026-11-25 14:31
aim: The sections menu (Studio, Interactions, ...) opens its section in the main page; the right pane holds Files only.
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1431_side_files_only.md
    what: this trace's own record, written first
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/focus-assets/focus.js
    what: a menu pick other than Files goes to that section in the main page; only Files reopens in the pane
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1431_side_files_only.md
  - plugins/haipipe-toolkit/servers/workbench/focus-assets/focus.js
---

# side files only

## Prompts

- **14:20** When I choose studio, will it show it in the main page? Now I want in the right panel. we will just show the files. do you get it?
- **14:31** yes, and could you also show the effects? ... Can you make the studio back to the main first.

## Check

- 5623 b17 in Chrome: Report ▾ → Studio lands on section=studio in the main page (🎨 Studio title), the side pane closed.
- workbench tests: 230 passed.

## Summary

A sections-menu pick other than Files now goes to that section in the main page (the URL without panel=); the side
pane reopens on load only for Files. Chat-Block-Framework told.
