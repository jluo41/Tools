---
title: s11 quick views
date: 2026-11-26 11:12
work: [s11]
aim: "s11's Effect keeps one quick view, Task states (each Task state and its effect); the three earlier designs and the old Job Main preview are deleted, and a retired quick view may now be deleted rather than kept faded."
closed: true
plan:
  - do: add
    path: blueprints/Project-Ladder/work/b17_theme_work/trace/261126/1112_s11_quick_views.md
    what: this trace's own record, written first
  - do: move
    path: blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/delivery/ui/task-states.html
    what: from delivery/ui/job-view-effects.html, its title Task states
  - do: delete
    path: blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/delivery/ui/job-view-rows.html
    what: Two rows, not taken
  - do: delete
    path: blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/delivery/ui/job-view-path.html
    what: Path and menus, not taken
  - do: delete
    path: blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/delivery/ui/job-view.html
    what: Rows (first)
  - do: delete
    path: blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/delivery/ui/job-main.html
    what: the old Job Main preview, now a live view under Page
  - do: edit
    path: blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/s11-work-job-preview.html
    what: Effect lists Task states only
  - do: edit
    path: blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/s11-work-job-preview.md
    what: Files lists Task states; the decisions name the deleted previews as removed
  - do: edit
    path: plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/ref/ui-preview-topic.md
    what: a retired quick view fades, and once the design is settled it may be deleted
changed:
  - blueprints/Project-Ladder/work/b17_theme_work/trace/261126/1112_s11_quick_views.md
  - blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/delivery/ui/ (task-states.html from job-view-effects.html; job-view-rows, job-view-path, job-view and job-main deleted)
  - blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/s11-work-job-preview.html
  - blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/s11-work-job-preview.md
  - plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/ref/ui-preview-topic.md
---

# s11 quick views

## Prompts

- **11:10** [Image #17] for this, should we delete [Image #18] (Two rows, Path + menus, Rows (first)) and have a better name for [Image #19] (Effects), do you understand what I mean?
- **11:12** go

## Check

- b17's Studio, s11: Page holds Topic rows (marked) and Job Main, both live; Effect holds Task states alone, shown full width; task-states.html returns 200.
- job-view-topics.html and its data files stay: Task states draws through it.
- No link to a deleted file is left outside traces; the face's decisions name each one "(removed 261126)".
- ui_preview_check.py: s11 passes. folder_icons_check.py: the 3 problems left are another session's b10 traces.

## Summary

s11's Effect is one quick view, Task states; the three earlier designs and the old Job Main preview are gone, and the UI preview rules now say a settled, faded quick view is deleted.
