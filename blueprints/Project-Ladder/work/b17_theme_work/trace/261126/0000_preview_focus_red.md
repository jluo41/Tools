---
title: preview focus red
date: 2026-11-26 00:00
topic: s11-work-job-preview
aim: s11's Topic rows and Job Main previews are the same page; Topic rows outlines its four rows in red, Job Main outlines the Main content under them in red.
closed: true
plan:
  - do: add
    path: blueprints/Project-Ladder/work/b17_theme_work/trace/261126/0000_preview_focus_red.md
    what: this trace's own record, written first
  - do: edit
    path: blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/delivery/ui/job-view-topics.html
    what: a focus (rows by default, main from ?focus=main) outlines that part in red
  - do: edit
    path: blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/delivery/ui/job-main.html
    what: the same page with focus main, in a full-size frame
  - do: edit
    path: blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/s11-work-job-preview.md
    what: the Files lines for the two previews
changed:
  - blueprints/Project-Ladder/work/b17_theme_work/trace/261126/0000_preview_focus_red.md
  - blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/delivery/ui/job-view-topics.html
  - blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/delivery/ui/job-main.html
  - blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/s11-work-job-preview.md
---

# preview focus red

## Prompts

- **23:59** [Image] How do you think you can make it to the job Main, I mean the same UI, but for the Job Main, we will show the job main related content, for the Topic Rows, you can focus on the topic rows, you can red highlight the elements, do you understand what I mean here?

## Check

- 5623, job-view-topics.html: the four rows (Job topics, Jobs, Task topics) outlined red, nothing else
- 5623, job-main.html: the same page, the Main (Overview, Tasks, Findings) outlined red

## Summary

Topic rows and Job Main are now one page: Topic rows outlines its rows in red, Job Main loads it with `?focus=main` and outlines the Main under them.
