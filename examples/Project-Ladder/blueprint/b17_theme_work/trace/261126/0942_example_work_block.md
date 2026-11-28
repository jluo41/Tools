---
title: example work block
date: 2026-11-26 09:42
work: [s11, j11t02]
aim: "b01_example_work is a real example work Block, scaffolded by the skills' own scripts, with every case a Job page must draw (many Jobs in one band, few Jobs, Tasks done, running, waiting on you, not started, a check Run with an open finding, traces). s11's Topic rows and Job Main tabs show its page as the server renders it; Effects stays a quick html."
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261126/0942_example_work_block.md
    what: this trace's own record, written first
  - do: add
    path: examples/Project-Ladder/work/b01_example_work/
    what: board.md (bands j0N, j1N, j2N), Jobs, Tasks, Runs and passes by new_board.py, new_job.py and soft_run.py; its own trace/
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/s11-work-job-preview.html
    what: Topic rows and Job Main open the live page of b01_example_work (its Block, and one Job), not a hand-drawn file
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
    what: a topic page's button may name a live page (/_board/workbench?...), origin-relative; Studio lists it as a left tab
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/s11-work-job-preview.md
    what: Files names b01_example_work as the example the previews render
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261126/0942_example_work_block.md
  - examples/Project-Ladder/work/b01_example_work/ (board.md; j01, j02, j11 to j18, j21; 15 Tasks; 12 Runs with passes; 3 traces)
  - plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/s11-work-job-preview.html
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/s11-work-job-preview.md
---

# example work block

## Prompts

- **09:33** examples/Project-Ladder/work/b01_example_work <--- For the example, I want you to work on these examples, we have many many examples, right? examples/Project-Ladder/paper/Paper-Example like this. So my point is [Image #9] for this, could you just work on the real examples, and showing the UI, do you get what I mean?
- **09:38** [Image #11] for this, it is from the servers, right?
- **09:41** could we make it to be server generated? and working with examples/Project-Ladder/work/b01_example_work? Do you get it?
- **09:43** so it is the real things to be rendered, and Effect is the quick hmtl

## Check

- Scaffolded by new_board.py, new_job.py and soft_run.py; new_job.py check: every Job's ## Tasks agrees with its folders.
- 5623 renders b01_example_work (200, its three bands First version, Second version, Ideas) and j11_core_checks (200, bands Checks and Reports), no traceback.
- b17's Studio lists s11's Topic rows and Job Main as live pages (data-studio-src /_board/workbench?path=...b01_example_work...); Effects and the earlier ones stay files.
- 5623, 5602, 5607, 5599 restarted, all 200. Tests: workbench 306 passed (the reader's known 6 fail); _host 152 passed, 1 failed (test asserting a b10 drawing, removed today by another session's b10 merge).
- folder_icons_check.py: b01's traces pass; the one left is 2147_ui_means_one_thing (b10 removed by another session).

## Summary

s11's Topic rows and Job Main are now the server's own pages over b01_example_work, a real example Block that holds every Job and Task state; a code change shows there on the next open.
