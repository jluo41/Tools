---
title: type matches instance
date: 2026-11-27 14:00
work: [s72, s11, s12, s13, s14]
aim: "A Studio type reads like its instances: s72 · Studio Type: Block Job UI Preview shows the same top views as s11-s14 (Page, Effect, Draw, Delivery) and the same Page left tabs (Block, Job, Task), each holding the rule with 〈placeholders〉; one more view, Instances, lines s11-s14 up against it, ✅ or ❗ per tab. s11-s14 move to the same tabs."
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1400_type_matches_instance.md
    what: this trace's own record, written first
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/build_type_pages.py
    what: "builds the type's view pages (each part's rule as a tree with 〈placeholders〉) and the Instances table; --check fails on a stale page or an instance that lacks a part. In place of the planned elements.md and servers type_check.py: an elements.md adds an Elements button the instances do not have, and a script in the topic touches no shared renderer"
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/ (page-block, page-job, page-task, effect, draw, delivery, instances .html)
    what: built by build_type_pages.py
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/studio-views.json
    what: "views Page (Block, Job, Task), Effect, Draw, Delivery, Instances, in place of Shape and Examples"
  - do: delete
    path: examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/delivery/rows.html
    what: the Jobs page rows now belong to s71 Block Structure
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/s72-studio-type-block-job-ui-preview.md
    what: its Definition section goes; Holds stays one line
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/s11-work-job-preview.html
    what: "Page's left tabs open with Block, Job, Task; job-rows, job-overview, job-tasks, job-findings stay after them (JL: 'you should still keep this')"
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/ (s12, s13, s14 pages)
    what: "their Page left tabs read exactly Block, Job, Task, in that order, the Job's or Task's name in the hover"
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1400_type_matches_instance.md
  - examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/ (build_type_pages.py, studio-views.json, its face, delivery/: 7 pages built, rows.html deleted)
  - examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/elements.md
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/s11-work-job-preview.html
  - examples/Project-Ladder/blueprint/b17_theme_work/s12-blueprint-job-preview/s12-blueprint-job-preview.html
  - examples/Project-Ladder/blueprint/b17_theme_work/s13-cowork-job-preview/s13-cowork-job-preview.html
  - examples/Project-Ladder/blueprint/b17_theme_work/s14-discovery-job-preview/s14-discovery-job-preview.html
---

# type matches instance

## Prompts

- **13:55** now I change s71 to the s72. [Image #53] for this, how do you want to align this metaclass to the instance. I mean when we see the studio type's layout, it will be the same to the studio type instance layout as well.
- **14:00** what is the next step, could you make the plan?
- **14:05** go

## Check

- 5623's b17 Studio, read from the served page (the Chrome extension was disconnected, so not looked at in a browser): s72 shows Page, Effect, Draw, Delivery, Instances, its Page tabs Block, Job, Task; s11 shows Page, Effect, Draw, Delivery, its Page tabs Block, Job, Task, then job-rows, job-overview, job-tasks, job-findings; s12 and s14 Block, Job, Task; s13 Block, Job.
- s72's built pages answer 200; s11's Task tab address (the Jobs page with task=t02) answers 200.
- build_type_pages.py --check: pages current; five parts lacking, left as they are for JL: s12 has no Effect, Draw or Delivery; s13 and s14 have no Effect. s13's Task reads — (a CoWork Job has no Task level).
- No server code changed; no restart needed.
- Later, once the b17 session made a type topic with its own studio-views.json skip the Elements button (trace 261127/1352): s72/elements.md added as first planned (Page, Effect, Draw, Delivery, Block, Job, Task; what, why, from), feeding the right-click cards only. The served page still shows s72's five views, no Elements button.

## Summary

s72 reads as its instances do: the same views and Page tabs, each holding the rule, plus Instances, which shows s12 lacking three views and s13, s14 lacking Effect.
