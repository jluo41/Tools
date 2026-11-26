---
title: preview element menu
date: 2026-11-25 21:55
topic: s11-work-job-preview
aim: s11's Topic rows preview has the real page's element menu; right-click a part (title, view-button-list, band, fold, job-row) and it lights up with its kind and offers Info, Comment and Copy address, the real script copied from element_info.py.
closed: true
plan:
  - do: add
    path: blueprints/Project-Ladder/work/b17_theme_work/trace/261125/2155_preview_element_menu.md
    what: this trace's own record
  - do: add
    path: blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/delivery/ui/job-view-topics-el.py
    what: copies element_info.py's STYLE and SCRIPT with the preview's selectors
  - do: add
    path: blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/delivery/ui/job-view-topics-el.js
    what: its output
  - do: edit
    path: blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/delivery/ui/job-view-topics.html
    what: loads job-view-topics-el.js
changed:
  - blueprints/Project-Ladder/work/b17_theme_work/trace/261125/2155_preview_element_menu.md
  - blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/delivery/ui/job-view-topics-el.py
  - blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/delivery/ui/job-view-topics-el.js
  - blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/delivery/ui/job-view-topics.html
---

# preview element menu

## Prompts

- **22:24** can you make it as well?

## Check

- 5623, the preview: right-click on 📊 Tasks lights it with the band tag and the menu band · 📊 Tasks, ℹ️ Info, 💬 Comment…, 📋 Copy address; Info opens its card with el.page.band.tasks and drawn by; 1 · 🧱 Tasks is a fold, t01 to t05 job-rows

## Summary

The preview carries the real element menu, copied from element_info.py by job-view-topics-el.py; a static file keeps no comment, so Comment opens the Info card.
