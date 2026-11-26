---
title: title center
date: 2026-11-25 21:49
topic: s11-work-job-preview
aim: A page title's section word ("• Report") sits on the title's middle, not 4px low on its baseline.
closed: true
plan:
  - do: add
    path: blueprints/Project-Ladder/work/b17_theme_work/trace/261125/2149_title_center.md
    what: this trace's own record
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/focus-assets/focus.css
    what: h1 align-items baseline to center
changed:
  - blueprints/Project-Ladder/work/b17_theme_work/trace/261125/2149_title_center.md
  - plugins/haipipe-toolkit/servers/workbench/focus-assets/focus.css
---

# title center

## Prompts

- **22:00** [Image] why I feel this is not aligned in the middle?
- **22:02** fix them.

## Check

- 5623, b17 Report: h1 align-items center; title middle 74.2px, Report middle 74.4px (was 77 and 81); zoomed screenshot: the dot and Report sit on the title's middle

## Summary

focus.css's h1 now centers its words, so the smaller section word no longer sinks to the big title's baseline.
