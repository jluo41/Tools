---
title: Job UI previews numbered as the Block Structure topics
date: 2026-11-27 12:49
topic: s02-blueprint-structure
aim: 'The second digit names the Block type in every band: 1 Work, 2 Blueprint, 3 CoWork, 4 Discovery; so s11 Work, s12 Blueprint, s13 CoWork, s14 Discovery, as s01-s04 and s51-s54.'
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1249_job_previews_mapped.md
  what: this trace's own record, written first
- do: move
  path: examples/Project-Ladder/blueprint/b17_theme_work/s12-blueprint-job-preview
  what: to s12-blueprint-job-preview
- do: move
  path: examples/Project-Ladder/blueprint/b17_theme_work/s13-cowork-job-preview
  what: to s13-cowork-job-preview
- do: move
  path: examples/Project-Ladder/blueprint/b17_theme_work/s14-discovery-job-preview
  what: to s14-discovery-job-preview
- do: edit
  path: examples
  what: every path and sNN-D code of the three, repo-wide
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/board.md
  what: Renumbered note
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/topic-numbering.md
  what: the s1N example line
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1249_job_previews_mapped.md
- examples/Project-Ladder/blueprint/b17_theme_work/board.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/topic-numbering.md
---

# Job UI previews numbered as the Block Structure topics

## Prompts

- **12:49** things here should be mapped, s01 to s11, do you get what I mean?

## Check

- served Studio: s11 work, s12 blueprint, s13 cowork, s14 discovery under Job previews; the three previews pages answer 200

## Summary

Job UI previews numbered by Block type, as s01-s04 and s51-s54.

