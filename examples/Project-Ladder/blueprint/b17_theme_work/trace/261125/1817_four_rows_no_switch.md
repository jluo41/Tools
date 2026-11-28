---
title: four rows no switch
date: 2026-11-25 18:17
topic: s11-work-job-preview
aim: The four rows are always four rows (Job topic, Job view, Task topic, Task view) with full names on every button; the switch mark goes, from the s11 preview, the s11 drawing and the page; a topic is an underlined word, a view a bordered button, in the preview as on the page.
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1817_four_rows_no_switch.md
    what: this trace's own record, written first
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/delivery/ui/job-view-topics.html
    what: no switch and no flat mode; always four rows; full names; topics as underlined words; Main in the Task topic row
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/build_s11_work_job_preview.py
    what: MANY drawn as the four rows with full names, no switch mark; rebuilt
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_jobs.py
    what: topic_group draws no switch and no flat mode; the JS that kept the choice goes
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/tests/test_focus_jobs.py
    what: no row-switch on the page
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1817_four_rows_no_switch.md
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/delivery/ui/job-view-topics.html
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/build_s11_work_job_preview.py
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/s11-work-job-preview.excalidraw
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/s11-work-job-preview.png
  - plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_jobs.py
  - plugins/haipipe-toolkit/servers/workbench/tests/test_focus_jobs.py
---

# four rows no switch

## Prompts

- **18:17** what is this? [s07's Topic rows preview, in its flat state] please upda the things here firs.t [the orange switch mark] what is this? [t01 t02 ... t14 as bare numbers] alawasy give me the full name? where are the four rows?
- **18:19** make it the reward level design, okay? (read as: the row-level design, the four rows)

## Check

- 5623 b17 Studio s11 › Topic rows: row 1 Workbench · j1N, Paper · j2N, Earlier · j0N as words; row 2 j11 · Job 1 … j18 · Job 8; row 3 Main | Build · t0N, Check · t1N as words; row 4 t01 · Read the brief … t09 · Hand over, full names; no switch (0 on the page); Check · t1N shows t10 · Review A … t14 · Sign off.
- drawing: MANY is the four rows with full names, no switch mark; looked at as PNG.
- page: no row-switch, no localStorage; workbench 242 pass.

## Summary

Four rows, always, full names, no switch, topics as words, views as buttons: in the preview, the drawing and the page.
