---
title: s11 job main
date: 2026-11-25 20:38
work: [s11, j11t02]
aim: "Design a Job's Main view for s11: each Task's row carries its newest check round (never the face's 🔴), the traces that name the Job, and only the findings still open; no MindMap, no empty Findings. A preview for JL to review before any code."
closed: false
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/2038_s07_job_main.md
    what: this trace's own record, written first
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/delivery/ui/job-main.html
    what: the Job Main preview with j11's real Tasks, rounds and traces, today beside the proposal
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/s11-work-job-preview.md
    what: a Job Main section in Decision, its sketch, and the preview in Files
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/s11-work-job-preview.html
    what: a Job Main tab beside the other previews
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/2038_s07_job_main.md
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/delivery/ui/job-main.html
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/s11-work-job-preview.md
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/s11-work-job-preview.html
---

# s11 job main

## Prompts

- **20:30** [Image #3] how do you want to update this UI?
- **20:34** [Image #4] why the status is this? I think you might want to design the structure of the s07 for how should the job's main should looks like.
- **20:38** how do you want to design it? what is your thoughts? you can design it and I will review them first.

## Check

- 5623 serves `delivery/ui/job-main.html` (200); s11's Page lists it as the Job Main tab.
- folder_icons_check.py: no problem for this trace.

## Summary
