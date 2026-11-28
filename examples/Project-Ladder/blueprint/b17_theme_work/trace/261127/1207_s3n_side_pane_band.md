---
title: s31 and s32 become s31 and s32; Studio topics grouped by named bands with emojis
date: 2026-11-27 12:07
topic: s32-trace-section
aim: The Files pane and Trace section topics sit together as s31 and s32 under a named band; the Studio groups topics by the board's bands line, as Jobs are, and every band name carries an emoji.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1207_s3n_side_pane_band.md
  what: this trace's own record, written first
- do: move
  path: examples/Project-Ladder/blueprint/b17_theme_work/s31-files-pane
  what: to s31-files-pane, its files renamed too
- do: move
  path: examples/Project-Ladder/blueprint/b17_theme_work/s32-trace-section
  what: to s32-trace-section, its files renamed too
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace
  what: 'about 50 trace files: topic and sNN-D codes renamed'
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/j12_side_pane/j12_side_pane.md
  what: s31 links to s31
- do: edit
  path: plugins/haipipe-toolkit/skills/0_utils/hai-trace/SKILL.md
  what: example topic s31 to s31
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/board.md
  what: 'bands line: emojis, and s0N s1N s3N s9N names'
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
  what: group topics by the board's sNN band when named, else by tags
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_jobs.py
  what: band_names reads s bands too
- do: add
  path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/tests/test_studio_bands.py
  what: topics fall into their named decade band
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1207_s3n_side_pane_band.md
- examples/Project-Ladder/blueprint/b17_theme_work/j12_side_pane/j12_side_pane.md
- plugins/haipipe-toolkit/skills/0_utils/hai-trace/SKILL.md
- examples/Project-Ladder/blueprint/b17_theme_work/board.md
- plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
- plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_jobs.py
- plugins/haipipe-toolkit/servers/workbench/studio/tabs/tests/test_studio_bands.py
---

# s31 and s32 become s31 and s32; Studio topics grouped by named bands with emojis

## Prompts

- **12:07** for each band, why there are no emojis?
- **12:11** go

## Check

- no old names left in the repo; 354 tests pass (6 known draft-reader failures); served Studio shows 🪜 Work ladder, 👀 Job previews, 📁 Side pane (s31, s32), 🧭 Guide; Chrome not connected

## Summary

s06 and s07 are s31 and s32; the Studio groups topics by the board's sNN bands; every band name has an emoji.

