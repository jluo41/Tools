---
title: task folds live
date: 2026-11-25 21:40
topic: s11-work-job-preview
aim: A Job's Main shows its Tasks as s11's Topic rows preview does (as of 22:24); its band named 📊 Tasks; 1 · 🧱 Tasks with ☆ and no progress bar; each Task a row under it named tNN · its heading, the newest round's mark on the right; opened, one row per round (mark, title, pNN · MM-DD) under it, its Summary on hover.
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/2140_task_folds_live.md
    what: this trace's own record, written first
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_plan_results.py
    what: tasks_section prints a row per Task (tNN · heading, newest round's mark) opening to its round rows; no progress bar
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/block_index_page/focus_render.py
    what: a Job's Main names its standing band Tasks
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/tests/test_focus_runs.py
    what: the Job's Tasks rows (name, mark, rounds)
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/tests/test_focus_status_map.py
    what: a Task row's name, mark and round rows
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/2140_task_folds_live.md
  - plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_plan_results.py
  - plugins/haipipe-toolkit/servers/workbench/page/block_index_page/focus_render.py
  - plugins/haipipe-toolkit/servers/workbench/tests/test_focus_runs.py
  - plugins/haipipe-toolkit/servers/workbench/tests/test_focus_status_map.py
---

# task folds live

## Prompts

- **21:38** [Image] [Image] can you tell the differnces!!!!!!!!!
- **21:40** ok
- **21:42** I don't want that box to contain the results.
- **22:26** go

## Check

- workbench tests: 243 passed
- 5623 restarted; b17 💼 Jobs, j11 Main: bands 🧭 Overview, 📊 Tasks, 🔎 Findings; 1 · 🧱 Tasks with ☆, no progress bar; rows t01 · Block index page ✅, t02 · Job and Task views ✅, t03 · Element marks ✅, t04 · Shared parts and file map 🙋 waiting for you, t05 · Home and Project pages ✅; t01 opened: ✅ live restarts p02 · 11-25, ✅ first check round p01 · 11-25, each Summary on hover

## Summary

A Job's Main now draws its Tasks as the s11 preview does: the band is 📊 Tasks, 1 · 🧱 Tasks has no progress bar, each Task is a row named tNN · its heading with its newest round's mark (not the face's 🔴 OPEN), and opened it lists its rounds from passes/pNN-MMDD/pass.md.
