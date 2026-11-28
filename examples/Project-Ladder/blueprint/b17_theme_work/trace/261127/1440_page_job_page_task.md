---
title: page job page task
date: 2026-11-27 14:40
work: [s72, s11, s12, s13, s14]
aim: "A Block Job UI Preview's top views are Page-Job, Page-Task, Job types, Task types, Effect, Draw, Delivery, the same on the type (s72) and on its instances (s11-s14); no Block tab. Page-Job's left tabs are the parts of a Job page (job-rows, job-overview, job-tasks, job-findings), Page-Task's the parts of a Task page (task-rows, task-overview, task-runs, task-findings). Job types and Task types say which types this Block uses and which Jobs or Tasks have them. The type shows each part's requirement, an instance the real thing."
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1440_page_job_page_task.md
    what: this trace's own record, written first
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_views.py
    what: "a studio-views.json item may name a live workbench page (url: an origin-relative /_board/workbench? address) and be an earlier one (old: true), so a view's left tabs can be parts of a live page"
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/tests/test_structure_views.py
    what: a url item is kept when it is a workbench address and dropped otherwise
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/ (elements.md, build_type_pages.py, studio-views.json, delivery/)
    what: the new views and tabs with their requirements; the builder also writes each instance's studio-views.json and its Job types and Task types pages
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/ (s11, s12, s13, s14: studio-views.json, delivery/types/job-types.html, task-types.html)
    what: written by s72's builder from each example Block's faces
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/s11-work-job-preview.html
    what: "the Block, Job, Task buttons of trace 1400 come out again (s12-s14's pages stay: their views now come from studio-views.json)"
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1440_page_job_page_task.md
  - plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_views.py
  - plugins/haipipe-toolkit/servers/workbench/studio/tabs/tests/test_structure_views.py
  - examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/ (elements.md, build_type_pages.py, studio-views.json, delivery/: 13 requirement pages and instances.html; page-block, page-job, page-task deleted)
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/ (studio-views.json, delivery/types/, its page)
  - examples/Project-Ladder/blueprint/b17_theme_work/s12-blueprint-job-preview/ (studio-views.json, delivery/types/)
  - examples/Project-Ladder/blueprint/b17_theme_work/s13-cowork-job-preview/ (studio-views.json, delivery/types/)
  - examples/Project-Ladder/blueprint/b17_theme_work/s14-discovery-job-preview/ (studio-views.json, delivery/types/)
---

# page job page task

## Prompts

- **14:30** [Image #54] I think we will do not have the block, right? But we will have the things like Job and Tasks, [Image #55] how to show the thigns like [Image #56] Do you get what I mean? Maybe we can have Page-Job and Page-Task in the top?
- **14:40** go and also show we have the top view buttom for the job types and task types? to explain for this job, what are the types we will using. do you get it?

## Check

- 5623's b17 Studio, read from the served page (the Chrome extension is disconnected; not looked at in a browser): s72 shows Page-Job, Page-Task, Job types, Task types, Effect, Draw, Delivery, Instances; s11 the same seven without Instances; both with left tabs job-rows, job-overview, job-tasks, job-findings and task-rows, task-overview, task-runs, task-findings.
- Every live tab was fetched and its mark looked for on the page: s11 and s12 have all eight parts. A CoWork or Discovery page draws no Overview, Tasks or Findings band, so s13 and s14 keep only job-rows (and s14 task-rows); Instances marks the rest ❗.
- Job types, s11: check (j11, j14), code (seven Jobs), doc (j02, j18). Task types, s11: code, display. s12: its Jobs name no type; its Tasks ui, tool, and many with none.
- First build read an empty `task-type:` line as the next line's text; fixed (the value must be on the same line).
- build_type_pages.py --check: files current; lacking: s12 Effect, Draw; s13 Page-Job parts, Effect; s14 Page-Job parts, Page-Task parts, Effect.
- Tests: workbench page, side_pane, studio, home 251 passed, 1 skipped (a live url item is kept, any other address dropped). 5623 and 5602 restarted, both 200.

## Summary

A Block Job UI Preview reads Page-Job, Page-Task, Job types, Task types, Effect, Draw, Delivery on the type and on its instances; the type's right side is the requirement, an instance's the real page part or the real types.
