---
title: studio tabs narrow
date: 2026-11-26 09:32
topic: s11-work-job-preview
aim: A Studio topic's left tabs no longer squeeze its preview to nothing at 601 to 700px wide; the Studio two-column rule switches at the same width as the page's side tabs (700px).
closed: true
plan:
  - do: add
    path: blueprints/Project-Ladder/work/b17_theme_work/trace/261126/0932_studio_tabs_narrow.md
    what: this trace's own record, written first
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
    what: the two-column media query starts at 701px, not 601px
changed:
  - blueprints/Project-Ladder/work/b17_theme_work/trace/261126/0932_studio_tabs_narrow.md
  - plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
---

# studio tabs narrow

## Prompts

- **09:20** [Image] Why I have this?
- **09:32** go

## Check

- 5623 restarted; s11 in a frame 620 and 650px wide: tabs in one row on top, preview full width below (was: list 675px, preview 0px at 650); 720 and 1000px keep the left list beside the preview

## Summary

The Studio two-column rule now starts at 701px, the same width where the page's side tabs turn into a row (ui_parts, 700px), so between 601 and 700px the row of tabs no longer widens the left column and hides the preview.
