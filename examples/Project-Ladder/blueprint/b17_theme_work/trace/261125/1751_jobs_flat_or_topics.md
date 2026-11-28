---
title: jobs flat or topics
date: 2026-11-25 17:51
topic: s11-work-job-preview
aim: The Jobs and a Job's Tasks can read flat (one row, FEW) or by topic (a decade a topic button, MANY); a small mark at the row's right end switches them, its hover names the other way, the choice kept in this browser; past about 7 buttons the topic way is the default.
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1751_jobs_flat_or_topics.md
    what: this trace's own record, written first
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/build_s11_work_job_preview.py
    what: the drawing first; the switch mark at the end of FEW's and MANY's rows; the headings that overlap in Excalidraw's font made shorter or spaced
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_jobs.py
    what: a topic row (decade, named by board.md bands) drawn beside the flat row; html.jobs-topics shows one or the other; the switch mark toggles it (localStorage wb:jobs-topics)
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/tests/test_focus_jobs.py
    what: both rows on the page, the switch mark, the topic row named by bands
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1751_jobs_flat_or_topics.md
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/build_s11_work_job_preview.py
  - plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_jobs.py
---

# jobs flat or topics

## Prompts

- **17:51** I htink we can have both version, and we can swith the view? how do you think?
- **17:55** okay, please go ahead and do it.
- **18:00** [the MANY wireframe, four rows of buttons] we might need to think about what is the best UI design for it, not to be too crowded.

## Check

- drawing: the switch mark at FEW's and MANY's row ends; the overlapping headings shortened (a Job · Main or a Task · its folds).
- code: focus_jobs.topic_group written, workbench 240 pass, 5623 not restarted; paused at 18:00 when JL found MANY's four rows too crowded. The design comes back to s11 first.

## Summary

Paused at 18:00, then finished as JL's four rows in 1808_jobs_four_rows.md (topics the default, topics as words).
