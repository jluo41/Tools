---
title: preview like page
date: 2026-11-25 18:19
topic: s11-work-job-preview
aim: s11's Topic rows preview looks like the page's 💼 Jobs (a picked view blue with a soft fill, a topic an underlined word, the Task rows indented with a grey line), and inside a picked topic its Jobs are not faded twice.
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1819_preview_like_page.md
    what: this trace's own record, written first
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/delivery/ui/job-view-topics.html
    what: the page's colours and shapes; no orange; the Task rows have no grey vertical line
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/build_s11_work_job_preview.py
    what: the wireframes in the page's style (picked blue, topics as words with the picked one underlined, no orange); rebuilt
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_jobs.py
    what: with topics on, a Job in the picked topic reads full, not faded; the Task level has no grey vertical line (no indent line, no line after Main)
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1819_preview_like_page.md
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/delivery/ui/job-view-topics.html
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/build_s11_work_job_preview.py
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/s11-work-job-preview.excalidraw
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/s11-work-job-preview.png
  - plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_jobs.py
---

# preview like page

## Prompts

- **18:19** [the page's 💼 Jobs: j1N j0N words, j01 · Work ladder contract blue, Main, t01, t03] why not using this???
- **18:24** please make it to be algined withat that design style.
- **18:26** For the task level, I don't wnat [the grey vertical line before Main], remove this. for the topic row, we can use [j1N j0N, words, the picked one underlined], please think about how to update hte design first.

## Check

- preview: picked views blue with a soft fill, topics as words with the picked one underlined, no orange, no grey line at the Task level; seen in s11.
- drawing: FEW and MANY picked blue, topics as words with the picked underlined; PNG looked at.
- page, 5623 b17 💼 Jobs: row 1 j1N (underlined) j0N (faded) and no switch; j11-j13 full; Main, t01-t05 with no grey line left of Main (border-left 0, padding 0). workbench 242.

## Summary

The preview, the drawing and the page now share one look: views are bordered buttons, blue when picked; topics are words, underlined when picked; the Task level has no grey lines.
