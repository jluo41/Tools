---
title: job main content
date: 2026-11-26 12:25
work: [s11, j11t02]
aim: "A work Job's Main draws no empty Findings band (no 'No findings here.'); its Overview's three folds (Goal, Requirements, MindMap) become one fold laid out top-view-left-tab-right-content, proposed first as s11 quick views for JL to pick. A Block's and a Task's pages are unchanged."
closed: false
plan:
  - do: add
    path: blueprints/Project-Ladder/work/b17_theme_work/trace/261126/1225_job_main_content.md
    what: this trace's own record, written first
  - do: add
    path: blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/delivery/ui/ (overview-top-views, overview-left-tabs, overview-brief-and-map, overview-goal-lead)
    what: four quick views of one Overview fold over j11, each a way to lay out Goal, Requirements and MindMap
  - do: edit
    path: blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/s11-work-job-preview.html
    what: a button per Overview quick view, under Effect
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/home/project_findings.py
    what: work_findings() returns nothing on a Job with no section, so Main draws no Findings band
  - do: add
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/tests/test_job_main.py
    what: a Job with nothing found draws no Findings band; a Block keeps its line
  - do: edit
    path: blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/s11-work-job-preview.md
    what: its Open names the Overview layout to pick; its Decided says Job Main draws no empty Findings
changed:
  - blueprints/Project-Ladder/work/b17_theme_work/trace/261126/1225_job_main_content.md
  - blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/delivery/ui/overview-top-views.html
  - blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/delivery/ui/overview-left-tabs.html
  - blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/delivery/ui/overview-brief-and-map.html
  - blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/delivery/ui/overview-goal-lead.html
  - blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/s11-work-job-preview.html
  - blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/s11-work-job-preview.md
  - plugins/haipipe-toolkit/servers/workbench/home/project_findings.py
  - plugins/haipipe-toolkit/servers/workbench/page/job_task_views/tests/test_job_main.py
---

# job main content

## Prompts

- **12:22** go ahead, please go ahead and do them
- **12:30** [Image #35] how could we update this? could you propose several effect quick html? what I want is more like a top-review-left-tab-right content, to merge the three fold in to one fold. Please propose several examples and we can check them.

## Check

- MindMap is not removed: JL's 12:30 picture keeps it as one of the three; the Overview layout waits for JL's pick among the four quick views.
- 5623 serves the four quick views (200); in Chrome each draws one Overview fold over j11, its buttons and left tabs switch the right content.
- 5623's b01_example_work Jobs page: no Job draws "No findings here." any more; the one left is the Block's own Findings.
- Tests: workbench page, side_pane, studio, home 211 passed, 1 skipped; one trace_view test failed once while another session edited trace_view.py, and passed on rerun.
- 5623 and 5602 restarted, both 200.

## Summary

A Job with nothing found draws no Findings band; s11's Effect holds four Overview layouts, one fold each, for JL to pick before the code changes.
