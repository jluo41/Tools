---
title: effect only part
date: 2026-11-26 11:42
topic: s11-insight-job-preview
aim: 'Each Effect quick view shows only the part it is about, as b17''s Task states shows only the Tasks band: no title, no rows, no Overview, no red outline'
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b11_theme_insight/trace/261126/1142_effect_only_part.md
  what: this trace's own record, written first
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s11-insight-job-preview/delivery/ui/segment-grid.html
  what: only the Segments grid
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s12-questionbook-job-preview/delivery/ui/version-changes.html
  what: only the Changes and Proposals
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s13-dataprep-job-preview/delivery/ui/steps-and-runs.html
  what: only the Steps and Runs
changed:
- examples/Project-Ladder/blueprint/b11_theme_insight/trace/261126/1142_effect_only_part.md
---

# effect only part

## Prompts

- **11:42** b17_Jobs_Design could you follow this to design?

## Check

- Chrome: Segment grid shows only the grid, Version changes only Changes and Proposals, Steps and Runs only Steps and Runs; no title, rows or red outline

## Summary

Each b11 Effect quick view shows only the part it is about, as b17's Task states does; a grid cell is a mark whose hover names its Run and the reason it was refused.

