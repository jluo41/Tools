---
title: A Task that measures pane speed
date: 2026-11-26 09:55
aim: 'j12 gets t03_pane_speed: a bench script measures Files panel and Block page time, size, repeats and hot functions against limits, each round one pass.'
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261126/0955_pane_speed_task.md
  what: this trace's own record, written first
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/j12_side_pane/t03_pane_speed/t03_pane_speed.md
  what: 'the Task face: goal, limits, checks'
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/j12_side_pane/t03_pane_speed/scripts/bench_pane.py
  what: time, size, repeats, hot functions; exit 1 over a limit
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/j12_side_pane/t03_pane_speed/runs/run-check-pane-speed
  what: standing Run, first pass p01 with today's numbers
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/j12_side_pane/j12_side_pane.md
  what: Tasks list gains t03
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/j12_side_pane/t01_files_tree/t01_files_tree.md
  what: 'check 5: t03 bench passes'
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261126/0955_pane_speed_task.md
- examples/Project-Ladder/blueprint/b17_theme_work/j12_side_pane/t03_pane_speed/t03_pane_speed.md
- examples/Project-Ladder/blueprint/b17_theme_work/j12_side_pane/t03_pane_speed/scripts/bench_pane.py
- examples/Project-Ladder/blueprint/b17_theme_work/j12_side_pane/j12_side_pane.md
- examples/Project-Ladder/blueprint/b17_theme_work/j12_side_pane/t01_files_tree/t01_files_tree.md
- examples/Project-Ladder/blueprint/b17_theme_work/j12_side_pane/t03_pane_speed/runs/run-check-pane-speed/run.yaml
- examples/Project-Ladder/blueprint/b17_theme_work/j12_side_pane/t03_pane_speed/runs/run-check-pane-speed/run-check-pane-speed.md
- examples/Project-Ladder/blueprint/b17_theme_work/j12_side_pane/t03_pane_speed/runs/run-check-pane-speed/passes/p01-1126/pass.md
---

# A Task that measures pane speed

## Prompts

- **09:55** yes, pleaese go ahead and do it.

## Check

- t03_pane_speed made with new_job.py task; j12 Tasks and folders agree
- bench_pane.py on a fresh 5623: b17 first Files panel 1.01 s ❗ (trace parsing on first visit), median 0.59 s; b11 0.14 s, b16 0.19 s; pages 0.3-0.8 s first, b17 1.1 MB
- first pass p01-1126 written; t01's Checks gain the speed check

## Summary

j12 has a Task that measures the pane's speed each round and flags what got slow.

