---
title: type right side requirements
date: 2026-11-27 14:20
work: [s72]
aim: "A Studio type and its instances share top views and left tabs; the right side differs: the type shows the requirement (what must be shown there, where it comes from, why), the instance the real thing. s72's right side reads as requirements, built from its elements.md, in place of the small trees."
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1420_type_right_side_requirements.md
    what: this trace's own record, written first
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/elements.md
    what: "must: lines per part, what an instance must show there"
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/build_type_pages.py
    what: each part's page is its requirement, read from elements.md (what, must, from, why); the RULES trees go
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/ (6 part pages, instances.html)
    what: rebuilt
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1420_type_right_side_requirements.md
  - examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/elements.md
  - examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/build_type_pages.py
  - examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/ (page-block, page-job, page-task, effect, draw, delivery, instances .html, rebuilt)
---

# type right side requirements

## Prompts

- **14:15** So for the studio class vs instance, I think we will have the same top, left, right? right? for the top, and right, they will be the same, in the class, for the right content, it will be the describption, like what we want to show here, it is more like the requirements, and in the studio instance, it will just be the real things, do you get it?
- **14:20** go

## Check

- Each of s72's six part pages now reads: the part's name, what it is, Must show (a numbered list), Comes from, Why; all from elements.md, no text written twice. Read from the built page-job.html and served by 5623 (200); not looked at in a browser (the Chrome extension is disconnected).
- s72's views and left tabs are unchanged (Page: Block, Job, Task; Effect; Draw; Delivery; Instances).
- build_type_pages.py --check: pages current; the same five instance gaps as before (s12: Effect, Draw, Delivery; s13, s14: Effect).

## Summary

On s72 the right side is the requirement; on s11-s14 it is the real page. Top views and left tabs are the same on both.
