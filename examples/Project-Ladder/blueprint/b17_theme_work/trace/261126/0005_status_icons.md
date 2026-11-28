---
title: status icons
date: 2026-11-26 00:05
topic: s11-work-job-preview
aim: s11's Topic rows preview draws a Task's and a round's mark as one family of drawn status icons (16px circles, one color and shape per state, its word on hover) in place of the ✅ 🙋 ⬜ 🏃 ❗ emoji.
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261126/0005_status_icons.md
    what: this trace's own record, written first
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/delivery/ui/job-view-topics.html
    what: an SVG icon per mark (done, waits for you, running, not yet, void) on Task rows and round rows
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261126/0005_status_icons.md
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/delivery/ui/job-view-topics.html
---

# status icons

## Prompts

- **00:04** [Image] these emojis are outdated, you know, could you get more modern and award level icons here. Please think about it.

## Check

- 5623, job-view-topics.html, j11 Main: t01 to t05 and their rounds show green check circles; t04 and its newest round the orange ring with a dot; each word on hover; zoomed, aligned at 16px

## Summary

The preview's marks are drawn icons: done a green filled check, waits for you an orange ring with a dot that pings, running a blue half-filled ring, not yet a grey dashed ring, void a red filled cross. The live page still shows emoji until JL says go.
