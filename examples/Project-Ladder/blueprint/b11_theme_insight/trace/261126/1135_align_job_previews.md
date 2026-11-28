---
title: align job previews
date: 2026-11-26 11:35
topic: s11-insight-job-preview
aim: 'b11''s three Job UI previews follow hai-studio ui-preview-topic.md as b17''s do: named sNN-<kind>-job-preview, a UI preview line, Page with Topic rows (red), Job Main and a Task, Effect with one quick view named for what it shows'
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b11_theme_insight/trace/261126/1135_align_job_previews.md
  what: this trace's own record, written first
- do: move
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s11-insight-job-preview
  what: from s11-insight-job-page-view
- do: move
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s12-questionbook-job-preview
  what: from s12-book-job-page-view
- do: move
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s13-dataprep-job-preview
  what: from s13-prep-job-page-view
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s11-insight-job-preview/delivery/ui/segment-grid.html
  what: 'the quick view: Job Main with the question x segment grid'
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s11-insight-job-preview/delivery/ui/insight-job-view-data.py
  what: segments from the Book's partitions, status and reason, no soft Runs
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s12-questionbook-job-preview/delivery/ui/version-changes.html
  what: 'the quick view: a version''s changes'
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s13-dataprep-job-preview/delivery/ui/steps-and-runs.html
  what: 'the quick view: steps and the Board Jobs that ran them'
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/board.md
  what: tree, Renumbered
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/ui-preview-topic.md
  what: b11's three rows
changed:
- examples/Project-Ladder/blueprint/b11_theme_insight/trace/261126/1135_align_job_previews.md
---

# align job previews

## Prompts

- **11:35** please go ahead and do it.

## Check

- ui_preview_check.py: s11, s12, s13 pass (the remaining problems are j01's s51-s59 and s99)
- 5623 Studio: each shows Page (Topic rows, Job Main, Task) and Effect (Segment grid, Version changes, Steps and Runs); Chrome: Job Main outlined red on Insight-Example j03; the grid opens I01 on third with its reason

## Summary

b11's Job UI previews follow ui-preview-topic.md as b17's do: s11-insight-job-preview, s12-questionbook-job-preview, s13-dataprep-job-preview, each with a UI preview line, three live views under Page (Topic rows and Job Main one address with two marks, a Task) and one quick view under Effect named for what it shows; s11's grid shows each question x segment Run; b11's rows are in the skill's table.

