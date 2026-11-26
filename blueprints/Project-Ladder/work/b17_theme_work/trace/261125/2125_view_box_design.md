---
title: view box design
date: 2026-11-25 21:25
topic: s11-work-job-preview
aim: s11's Topic rows preview shows the whole proposed structure in one place; the four rows, then the picked view's content in one box with its open dot on the top-right corner; Main's content is Job Main (Plan + Results with one boxed fold per Task, Traces, open Findings only), a Task's content its page. The design first, the code after JL looks.
closed: true
plan:
  - do: add
    path: blueprints/Project-Ladder/work/b17_theme_work/trace/261125/2125_view_box_design.md
    what: this trace's own record, written first
  - do: edit
    path: blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/delivery/ui/job-view-topics.html
    what: the boxed view content; Main drawn as Job Main with Task folds; a Task drawn as its page
  - do: edit
    path: blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/s11-work-job-preview.md
    what: the decision, with the real page's differences
changed:
  - blueprints/Project-Ladder/work/b17_theme_work/trace/261125/2125_view_box_design.md
  - blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/delivery/ui/job-view-topics.html
  - blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/s11-work-job-preview.md
---

# view box design

## Prompts

- **21:20** http://100.121.165.84:5623/_board/workbench?path=blueprints%2FProject-Ladder%2Fwork%2Fb17_theme_work&layout=focus&section=jobs&group=j11 can you check the real layout and the proposed the structure [Image] You need to tell the differneces!!!!
- **21:24** go ahead and updat ethe design first.

## Check

- 5623 Studio, s11 › Topic rows (FEW, the default now): Main in the box shows Plan + Results with 5 Task folds and Findings; the dot's hover names j11
- clicked Page components › t04: the box shows its Runs (p02 ⬜, p01 🙋) and its Findings; the dot's hover names t04

## Summary

The Topic rows preview is now the one place that shows the whole structure: the four rows, then the picked view in one box with its open dot; Main drawn as Job Main with a boxed fold per Task, a Task drawn as its page. FEW, with j11's real rounds, opens first. The code waits for JL to look.
