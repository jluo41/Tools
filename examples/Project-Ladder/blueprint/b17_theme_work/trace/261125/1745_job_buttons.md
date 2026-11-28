---
title: job buttons
date: 2026-11-25 17:45
aim: The 💼 Jobs buttons read in one line each; Jobs group by their decade (j1N, then j0N) with a thin divider, the newest decade first; a Job whose face says closed or superseded reads faded, last.
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1745_job_buttons.md
    what: this trace's own record, written first
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/build_s11_work_job_preview.py
    what: the drawing first; Jobs by decade, newest first, a line between, the earlier decade dashed and faded; j11 › t02 job task views as the example; rebuilt
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/s11-work-job-preview.md
    what: Covers and the Decision name the Job buttons' design
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_jobs.py
    what: section orders the Jobs by decade, newest first, closed ones last and faded; a divider span between groups; CSS white-space:nowrap on the buttons
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/tests/test_focus_jobs.py
    what: j11 before j01, a divider between, a closed Job faded and last
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1745_job_buttons.md
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/build_s11_work_job_preview.py
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/s11-work-job-preview.excalidraw
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/s11-work-job-preview.png
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/s11-work-job-preview.md
  - plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_jobs.py
  - plugins/haipipe-toolkit/servers/workbench/tests/test_focus_jobs.py
---

# job buttons

## Prompts

- **17:45** How could we make this to be better? [the Jobs buttons: j01 · Work ladder contract ... j13 · Workbench tools, each wrapping onto two or three lines]
- **17:48** could you put the design of the UI of the Job to the draw first? how do you think about it?
- **17:52** go

## Check

- drawing first: s11's PNG looked at; j11 j12 j13, a line, j01 j02 j03 dashed; j11 › t02 · job task views › its folds (no Run yet). The code waits for JL.
- code: 5623 b17 💼 Jobs bar reads j11 · Workbench page (open), j12 · Side pane, j13 · Workbench tools, a line, j01 · j02 · j03 faded; every button 34 px high (one line); j11's views Main · t01 Block index page … t05 Home and project. workbench 240 pass.

## Summary

`focus_jobs.ordered` puts the newest decade first and closed Jobs last, marks an earlier decade or a closed Job `job-old` (faded), and puts a `job-div` line between groups; buttons never wrap. Drawn first in s11, then built.
