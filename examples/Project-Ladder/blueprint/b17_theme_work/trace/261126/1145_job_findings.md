---
title: job findings
date: 2026-11-26 11:45
work: [j11t02, s11]
aim: "s11's Page tabs are job-rows, job-overview, job-tasks and job-findings, one page with four marks; a work Job's Findings shows what its Tasks' rounds found, a fold per Task group, a left tab per Task, its newest round on the right."
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261126/1145_job_findings.md
    what: this trace's own record, written first
  - do: add
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/round_findings.py
    what: a Job's round findings, a section per Task group, side tabs per Task, its newest round's summary, changes and pass.md
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/home/project_findings.py
    what: a work Job's Findings adds the round findings
  - do: add
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/tests/test_round_findings.py
    what: a Job with two groups gets two sections, each Task a tab, its newest round's summary
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/s11-work-job-preview.html
    what: Page tabs job-rows, job-overview, job-tasks, job-findings, marks view=overview, view=standing, view=findings
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/s11-work-job-preview.md
    what: Files names the four Page tabs
  - do: edit
    path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/ui-preview-topic.md
    what: s11's four tabs as the example, a tab named level-part
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261126/1145_job_findings.md
  - plugins/haipipe-toolkit/servers/workbench/page/job_task_views/round_findings.py (new)
  - plugins/haipipe-toolkit/servers/workbench/home/project_findings.py
  - plugins/haipipe-toolkit/servers/workbench/page/job_task_views/tests/test_round_findings.py (new)
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/s11-work-job-preview.html
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/s11-work-job-preview.md
  - plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/ui-preview-topic.md (the four tab names, level-part)
---

# job findings

## Prompts

- **11:43** [Image #28] I want to call it job-tasks, How do you think? and I also want a job-overview, and then a job Finding, what is your thoughts? Please think about how to arrange the logics and list here: [Image #29] Maybe we can have a better names here. a better name list.
- **11:45** Yes, Please go ahead and do it, I think you can make the examples for the findings, I think they will be the top view left tab and right content foramt as well.

## Check

- Chrome, b01_example_work Jobs, j11, mark=view=findings: the Findings band outlined; folds 1 · 📌 Task Group 1 and 2 · 📌 Task Group 2; tabs t01 (waits for you), t02 (running), t11 (done), t12 (waits for you); t01's panel its second check round, round 2 · 11-25 · run-check-02-name, "One column, date, reads as text in two rows; keep it as text or fix the file?"; the corner dot opens the round in the viewer; no "Open … ↗" word.
- s11's Page tabs: job-rows, job-overview, job-tasks, job-findings (marks rows, view=overview, view=standing, view=findings); Effect Task states.
- test_round_findings.py passes; workbench, _host and workbench-work tests: the reader's known 6 and the b10 drawing (another session's removal) fail, nothing else.
- 5623, 5602, 5607, 5599 restarted, 200.

## Summary

A work Job's Findings shows what its Tasks' rounds found, a fold per Task group, a left tab per Task, its newest round on the right; s11's Page reads job-rows, job-overview, job-tasks, job-findings over one live page.
