---
title: job main mark
date: 2026-11-26 11:17
work: [s11, j13t01]
aim: "s11's Topic rows and Job Main are one live page (the example Block's Jobs, j11 picked) that differ only in what they outline; a mark can name a data attribute; Effect keeps left tabs even for one view; Task states shows the Tasks band alone."
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261126/1117_job_main_mark.md
    what: this trace's own record, written as the work was asked for, mid-turn
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/focus-assets/focus.js
    what: mark takes a class or a data attribute (jsub=main), outlines the visible ones, redraws after a click
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/s11-work-job-preview.html
    what: Topic rows and Job Main open the Jobs view with group=j11; marks jobs-rows,job-ttopics,job-subs and jsub=main
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
    what: a UI preview's Page and Effect keep left tabs for a single view
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/tests/test_effect_view.py
    what: one quick view still has its left tab
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/delivery/ui/job-view-topics.html
    what: only=tasks draws the Tasks band alone
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/delivery/ui/task-states.html
    what: the Tasks band alone, no legend
  - do: edit
    path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/ui-preview-topic.md
    what: mark with a data attribute, views of one page differ only by mark, left tabs even for one view
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261126/1117_job_main_mark.md
  - plugins/haipipe-toolkit/servers/workbench/focus-assets/focus.js
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/s11-work-job-preview.html
  - plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
  - plugins/haipipe-toolkit/servers/workbench/studio/tabs/tests/test_effect_view.py
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/delivery/ui/job-view-topics.html
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/delivery/ui/task-states.html
  - plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/ui-preview-topic.md
---

# job main mark

## Prompts

- **11:13** [Image #20] is the job main correct? I don't think it? these two [Image #21] show use the same UI, but different element to highlight, right?
- **11:14** [Image #22] for the effect, we should have the left tab as well, and we can add more effect.
- **11:16** I think for the [Image #23] you just need to keep [Image #24] the tasks band should be okay.

## Check

- Chrome, the example Block's Jobs with group=j11: mark=jsub=main outlines one element, j11's Main (421px), j11 · Core checks picked; mark=jobs-rows,job-ttopics,job-subs outlines the Job rows and the Task topic row (job-subs is hidden on Main, so not outlined).
- Chrome, b17 Studio s11: Page tabs Topic rows and Job Main; Effect one left tab, Task states, its frame task-states.html.
- task-states.html in Chrome: the Tasks band alone, t01 to t07, no title, rows, Overview, Findings or legend.
- test_effect_view.py 3 passed; focus.js parses; 5623, 5602, 5607, 5599 restarted, 200.

## Summary

Topic rows and Job Main are one page with two marks; Effect keeps its left tabs so more effects are one more tab; Task states is the Tasks band alone.
