---
title: discovery example on the work page
date: 2026-11-27 23:43
work: [s14, s72]
aim: "The Discovery example Block is read by the work page (workbench: work, as the Knowledge example), so its Job and Task pages have Overview, Tasks and Findings, and s14 shows them live. CoWork stays undecided."
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2343_discovery_example_work_page.md
    what: this trace's own record, written first
  - do: edit
    path: examples/Project-Ladder/discovery/b01_example_discovery/board.md
    what: "one line, workbench: work"
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/build_type_pages.py
    what: s14 leaves ROWS_ONLY, so its Job and Task views are the live pages
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s14-discovery-job-preview/ (studio-views.json, delivery/check.html, Checklist)
    what: rebuilt by the builder
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2343_discovery_example_work_page.md
  - examples/Project-Ladder/discovery/b01_example_discovery/board.md
  - examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/build_type_pages.py
  - examples/Project-Ladder/blueprint/b17_theme_work/s14-discovery-job-preview/ (studio-views.json, delivery/check.html, its face's Checklist)
---

# discovery example on the work page

## Prompts

- **23:43** go

## Check

- Cause found first: no theme reads the Discovery (or CoWork) example Block, so it opened on the vanilla page; the Knowledge example has the views through `workbench: work`. No server code changed.
- 5623, served pages (not looked at in a browser; the Chrome extension is disconnected): the Discovery Block, its j01 Job and t01 Task answer 200 with the Overview and Tasks (Plan + Results) bands; the Task also Findings. The Job draws no Findings band (nothing registered to show), so the builder keeps job-findings as the type's requirement (NOT_DRAWN), 🙋 in the Checklist.
- build_type_pages.py --check PASS; checks/run.py: every line for s11 to s15 and s72 PASS.
- CoWork is left as it was: undecided.

## Summary

The Discovery example is read by the work page; s14 shows its Job and Task views live, job-findings still open.
