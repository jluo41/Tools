---
title: jobs four rows
date: 2026-11-25 18:08
topic: s11-work-job-preview
aim: 💼 Jobs reads in four rows, row 1 Job topic (a decade of Jobs, named by bands:), row 2 Job view (the Jobs of that topic), row 3 Task topic (Main, then a decade of Tasks), row 4 Task view (the Tasks of that topic); a topic row shows when its level has two decades or more; topics are the default, the square mark switches to flat and the browser keeps it.
closed: true
plan:
  - do: add
    path: blueprints/Project-Ladder/work/b17_theme_work/trace/261125/1808_jobs_four_rows.md
    what: this trace's own record, written first
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_jobs.py
    what: topic_group defaults to topics; a topic reads as an underlined word (no border), a view as a bordered button; an earlier decade's topic button reads faded; Main moves into the Task topic row when there is one; the switch mark only on the Job topic row
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/tests/test_focus_jobs.py
    what: four rows; the Job topic row with j1N first, j0N faded; the Jobs of one topic; Main and the Task topics; the switch
changed:
  - blueprints/Project-Ladder/work/b17_theme_work/trace/261125/1808_jobs_four_rows.md
  - plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_jobs.py
  - plugins/haipipe-toolkit/servers/workbench/tests/test_focus_jobs.py
---

# jobs four rows

## Prompts

- **18:08** No, I just show you the idea. we have four rows: rows 1: Job topic, rows 2: job view, rows 3: task topic, rows 4: task view. Do you get it? How do you want to update it again here?
- **18:15** I think the topic and view, the button style should be different, do you get what I mean?

## Check

- 5623 b17 (restarted 18:04 by tools-space-ce with the half-done topic code live; it showed flat rows and a switch on each row): now row 1 j1N, j0N faded, the switch mark; row 2 j11 · Workbench page, j12 · Side pane, j13 · Workbench tools; j0N shows j01-j03 and opens j01; the mark gives one flat row of all six and back. b17's Tasks are one decade, so rows 3 and 4 are one row (Main, t01-t05).
- 18:15: a topic reads as an underlined word (no border, 2 px accent line when picked), a view as a bordered button; seen on 5623.
- workbench 241 (new test_four_rows_job_topic_job_view_task_topic_task_view), labeling 85, paper 112 pass.

## Summary

`focus_jobs.topic_group` draws a topic row above a view row when its level has two decades; topics are the default; a
"" button (Main) moves up into the Task topic row; Task decades are steps and never fade; the switch sits on the Job
topic row only. Topics are words, views are buttons.
