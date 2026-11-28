---
title: preview real data
date: 2026-11-25 21:46
topic: s11-work-job-preview
aim: s11's Topic rows preview shows only what is on disk; every Job, Task, round, mark, date and summary read from b17's folders by a script beside it; Overview back as the real Job Main has it; no made-up Findings.
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/2146_preview_real_data.md
    what: this trace's own record
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/delivery/ui/job-view-topics-data.py
    what: reads b17's Jobs, Tasks, Runs and passes into window.FEW
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/delivery/ui/job-view-topics-data.js
    what: its output
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/delivery/ui/job-view-topics.html
    what: hand-typed FEW removed; Overview (Goal, Requirements) from the Job face; Findings and the made-up 🙋 count removed
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/2146_preview_real_data.md
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/delivery/ui/job-view-topics-data.py
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/delivery/ui/job-view-topics-data.js
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/delivery/ui/job-view-topics.html
---

# preview real data

## Prompts

- **21:50** then tell me what error you found !!!! I am furious now.
- **21:52** plesae update it excatly as what we want!!!

## Check

- 5623, the preview: j11 Main shows Overview (Goal, Requirements) then t01 to t05 named from their faces (t02 Job and Task views, t05 Home and Project pages); t04 🙋 from run.yaml status waiting; rounds p02 and p01 with their pass.md titles, dates and Summary on hover
- Earlier design › j03 › Page design › t01: its five Runs' passes as rows; j14 and j15 now in row 2

## Summary

The preview no longer holds typed data: job-view-topics-data.py reads b17's folders into job-view-topics-data.js, and the page draws from it. Overview is back; the invented Findings row and 🙋 count are gone.
