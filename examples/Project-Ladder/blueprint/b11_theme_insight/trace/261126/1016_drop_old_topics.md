---
title: drop old topics
date: 2026-11-26 10:16
topic: s11-insight-job-preview
aim: 'b11 Studio keeps only the topics in use: s11 renamed Insight-Job page view; s01-s04, s11-s13, s21, s31, s32, s33, s61 deleted, their references swept'
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b11_theme_insight/trace/261126/1016_drop_old_topics.md
  what: this trace's own record, written first
- do: move
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s11-insight-job-preview
  what: renamed from s11-work-job-preview
- do: delete
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s01-insight-ladder
  what: dropped
- do: delete
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s31-insight-guide
  what: dropped
- do: move
  path: plugins/haipipe-toolkit/servers/workbench-insight/studio/insight-workbench-design.py
  what: the Guide RoadMap drawing, out of s02
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench-insight/guide/guide.yaml
  what: RoadMap Draw path
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/board.md
  what: tree, Questions report lines
changed:
- examples/Project-Ladder/blueprint/b11_theme_insight/trace/261126/1016_drop_old_topics.md
---

# drop old topics

## Prompts

- **10:16** yes, plesae just to drop them, we can drop them.

## Check

- 5623: b11 Studio lists only s05, s11, s12, s13, s99; the workbench conformance test passes (11)

## Summary

b11 Studio keeps only the topics in use. s11 is now s11-insight-job-preview. s01 to s04, s11 to s13, s21, s31, s32, s33 and s61 are deleted; the Insight Guide's RoadMap drawing moved to servers/workbench-insight/studio/ and every reference was swept.

