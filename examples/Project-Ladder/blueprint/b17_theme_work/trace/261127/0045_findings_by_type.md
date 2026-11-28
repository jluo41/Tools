---
title: findings by type
date: 2026-11-27 00:45
work: [s11, j11t02]
aim: "A work Job's 🔎 Findings is what its Runs made, grouped by type: a Run names its finding files in run.yaml `finds:` (file, kind value, display or report), and Findings draws one fold per kind, 🔢 Values, 🖼️ Displays, 📄 Reports, a left tab per file of each Task's newest Run that names one, the file on the right, its open dot opening it. The round folds per Task group go: rounds stay in Tasks. A Run with a tables.json and no finds: still reads as a value."
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/0045_findings_by_type.md
    what: this trace's own record, written first
  - do: add
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/run_finds.py
    what: reads run.yaml finds:, picks each Task's newest Run that names one, draws the three folds (Values a table, Displays a picture, Reports the text or page)
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/home/project_findings.py
    what: "on a Job, the finds: folds instead of the round folds; the older Values or Displays fold only for a kind finds: does not name"
  - do: delete
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/round_findings.py
    what: the round folds per Task group, and its test
  - do: add
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/tests/test_findings_by_type.py
    what: three kinds give three folds, a tab per file; the newest Run wins; no finds gives no fold
  - do: edit
    path: examples/Project-Ladder/work/b01_example_work/j11_core_checks/
    what: t02 a value table, t11 a text report, t12 an HTML report, a new t13 display Task with a figure, each Run's run.yaml naming them under finds:; the Job face lists t13
  - do: edit
    path: plugins/haipipe-toolkit/skills/1_base/project/hai-run/ref/receipts-and-inventory.md
    what: "the finds: field of run.yaml"
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/s11-work-job-preview.md
    what: its Decision says Findings is the Runs' outputs by type
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/0045_findings_by_type.md
  - plugins/haipipe-toolkit/servers/workbench/page/job_task_views/run_finds.py
  - plugins/haipipe-toolkit/servers/workbench/home/project_findings.py
  - plugins/haipipe-toolkit/servers/workbench/page/job_task_views/round_findings.py (deleted)
  - plugins/haipipe-toolkit/servers/workbench/page/job_task_views/tests/test_round_findings.py (deleted)
  - plugins/haipipe-toolkit/servers/workbench/page/job_task_views/tests/test_findings_by_type.py
  - examples/Project-Ladder/work/b01_example_work/j11_core_checks/ (j11 face lists t13; t13_range_figure new; t02, t11, t12, t13 Runs' result files and finds:)
  - plugins/haipipe-toolkit/skills/1_base/project/hai-run/ref/receipts-and-inventory.md
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/s11-work-job-preview.md
---

# findings by type

## Prompts

- **00:40** [Image #39] I think for the findings, they are more like the values, the tables, the figures, the report, do you get it? I want the folder for the views table, and fold for the displays, how do you think about it?
- **00:42** so for the overiew, it is like the aim, the scope? for the findings, we have the things groupby types, right? could you show me the plan again?
- **00:45** oka, if so, plesae go ahead and do it.

## Check

- The reports live in run_finds.py with the other two kinds rather than a report_findings.py of their own: one reader for finds:, 125 lines.
- t13_range_figure made by new_job.py task, its Run by soft_run.py new and pass; result files written by hand: ranges.csv (t02), ranges.svg (t13), report.txt (t11), report.html (t12).
- 5623's b01_example_work Jobs, j11: 🔎 Findings is 1 · 🔢 Values, 2 · 🖼️ Displays, 3 · 📄 Reports, no Task Group fold; in Chrome Displays shows the ranges figure under t13 · Task 13 name, Reports its two tabs, the HTML report drawn in its frame; Values holds the ranges table (height_cm row on the page).
- Tests: test_findings_by_type.py 3 pass; workbench page, side_pane, studio, home 217 passed, 1 skipped.
- 5623, 5602, 5607, 5599 restarted, all 200.

## Summary

A work Job's Findings is its Runs' outputs by type, named in run.yaml finds:, one fold per kind; the round folds are gone.
