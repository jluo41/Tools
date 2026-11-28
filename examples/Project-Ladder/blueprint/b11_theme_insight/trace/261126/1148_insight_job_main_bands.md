---
title: insight job main bands
date: 2026-11-26 11:48
topic: s11-insight-job-preview
aim: 'An insight Job''s Main has the same bands as a work Job''s: Overview (Goal, Requirements, MindMap), Tasks, Findings, on the Board, the Question Book and the DataPrep Block'
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b11_theme_insight/trace/261126/1148_insight_job_main_bands.md
  what: this trace's own record, written first
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/page/block_index_page/focus_render.py
  what: an insight Job takes the live work path, so its Report views are bands of Main
- do: add
  path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/tests/test_focus_jobs.py
  what: a test that an insight Job's Main has the three bands
changed:
- examples/Project-Ladder/blueprint/b11_theme_insight/trace/261126/1148_insight_job_main_bands.md
---

# insight job main bands

## Prompts

- **11:48** for the job Main, where is the band names, like the Overview etc. Like this [Image] you should follow the same structure. Pelase go ahead and do it.

## Check

- Chrome: Insight-Example j03 Main shows Overview (Goal, Requirements, MindMap), Tasks, Findings; the Question Book j02 and the DataPrep j01 Mains show the same bands
- pytest workbench/page workbench-insight workbench/side_pane: 268 passed, 1 skipped; test_focus_jobs asserts an insight Job's Main bands

## Summary

An insight Job (Board, Question Book, DataPrep) takes the live work path, so its Main has the work Job's bands; an older insight Job keeps its own letters (Findings, Changes, Progress) as views beside Main.

