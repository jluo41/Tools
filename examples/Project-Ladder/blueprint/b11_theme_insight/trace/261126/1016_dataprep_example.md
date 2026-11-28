---
title: dataprep example
date: 2026-11-26 10:16
topic: s11-insight-job-preview
aim: 'The insight examples cover all three Jobs: a DataPrep Block with a signed prep-v1, and a Board Job of three versions run end to end'
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b11_theme_insight/trace/261126/1016_dataprep_example.md
  what: this trace's own record, written first
- do: add
  path: examples/Project-Ladder/insight/InsightDataPrep-Example
  what: the DataPrep Block, three agreed steps, signed
- do: add
  path: examples/Project-Ladder/insight/Insight-Example/j03_data-v2_prep-v1_question-v1
  what: the Board Job of three versions, run
- do: edit
  path: examples/Project-Ladder/insight/Insight-Example/board.md
  what: dataprep, raw for each data version
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_jobs.py
  what: a Job label shows its prep version
changed:
- examples/Project-Ladder/blueprint/b11_theme_insight/trace/261126/1016_dataprep_example.md
---

# dataprep example

## Prompts

- **10:16** go ahead

## Check

- insight_ladder.py audit: InsightDataPrep-Example all 0; j03's tables carry the same sha256 as j02's

## Summary

InsightDataPrep-Example holds prep-v1 (three steps agreed by reviewer agents, signed 261126); Insight-Example j03_data-v2_prep-v1_question-v1 ran its prep Run and eleven question Runs, one refused for power; the Jobs row reads j03 · data-v2 · prep-v1.

