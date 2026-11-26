---
title: shared state marks
date: 2026-11-26
topic: s11-work-job-preview
aim: s11's Topic rows preview draws its marks with the Files pane's own state marks (file_icons.STATE_MARKS, same shapes, colors and 12px box); the two it lacks, waits for you and void, drawn in the same style.
closed: true
plan:
  - do: add
    path: blueprints/Project-Ladder/work/b17_theme_work/trace/261126/0007_shared_state_marks.md
    what: this trace's own record, written first
  - do: edit
    path: blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/delivery/ui/job-view-topics.html
    what: its icons are the Files pane's state marks; you and void added in their style
changed:
  - blueprints/Project-Ladder/work/b17_theme_work/trace/261126/0007_shared_state_marks.md
  - blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/delivery/ui/job-view-topics.html
---

# shared state marks

## Prompts

- **00:12** I think we can use the same system as we used in the folder panel, right? it can also be sharing, what is your thoughts?

## Check

- 5623, job-view-topics.html, j11 Main zoomed: done rows the Files pane's green check, t04 the amber ring with a dot, 14px, aligned

## Summary

The preview's marks are the Files pane's STATE_MARKS drawings, copied; waits for you and void added in their style. The live code does not share them yet.
