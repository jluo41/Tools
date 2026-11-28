---
title: s11 job page view
date: 2026-11-25 16:42
topic: s11-work-job-preview
aim: s11 · Job page view records JL's design for a Job inside the Block's 💼 Jobs, and the code builds it. View buttons pick the Job (j01 j02 j03); the picked Job has its own sub view buttons (Tasks · Overview · Findings, only those it has); Tasks is top-view-left-tab, its Tasks t01 t02 t03 on the left, the picked Task's page on the right, and that Task page holds its folds (its Runs among them).
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1642_s11_work_job_preview.md
    what: this trace's own record, written first
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/s11-work-job-preview.md
    what: the face, shaped like s31; its decision is JL's 16:45 design (Job buttons, its sub view buttons, Tasks as left tabs, the Task page with its folds on the right); Excluded names s54-s56 and hai-block A06
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/delivery/ui/job-view.html
    what: the preview, JL's design with j03's real Tasks and Runs, clickable (Job, sub view, Task)
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/s11-work-job-preview.html
    what: the topic's Page holding the preview
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/build_s11_work_job_preview.py
    what: the drawing's builder (quick_draw kit), reading j03's Jobs, Tasks and Runs from disk; writes the .excalidraw and .png
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_jobs.py
    what: each Job pane gets its sub view bar (Tasks first, then Overview, Findings when it has any); Tasks is _side_tabs of its tNN, each panel that Task's body by the page pipeline; switching stays in place, scoped to its own Job
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/build_s11_work_job_preview.py
    what: the drawing follows 17:05 (Job, then Main or a Task as its views, then the Task page's folds); rebuilt
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/tests/test_focus_jobs.py
    what: the Job's sub bar, its Tasks as left tabs in number order, a Task's folds inside its panel
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1642_s11_work_job_preview.md
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/s11-work-job-preview.md
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/s11-work-job-preview.html
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/delivery/ui/job-view.html
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/build_s11_work_job_preview.py
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/s11-work-job-preview.excalidraw
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/s11-work-job-preview.png
  - plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_jobs.py
  - plugins/haipipe-toolkit/servers/workbench/tests/test_focus_jobs.py
---

# s11 job page view

## Prompts

- **16:38** [j03 in 💼 Jobs] how do you think we can better design this?
- **16:42** yes, how do you think we shouuld do it, maybe we need a new studio for it? what is your thoughts? maybe call it s07 Job Page View?
- **16:45** I think what we can do is, we select Job in the view bottom and that job can have its own sub view buttom list, and then each task view buttom can have a list of task folder, and we may have task 1, 2, 3, and then we have the things like task page, how do you think about this? task then can have the fold.
- **16:47** create the s07 first.
- **16:55** what is the draw for this studio, I want to have a quick check
- **17:00** yes, go ahead and do it.
- **17:05** [Overview] should we call it the main? [a fold "1 · 🎯 Goal"] I want to make this the same to [s31's open fold], do you get it? [the Tasks as left tabs] how about we get the tasks to be the view as well in [Tasks · Overview]. Pelase update it again.

## Check

- s11 first: 5623 b17 Studio lists s11 · Job page view (shaping) after s31, its Page shows the preview: j03 picked, Tasks · Overview, t01-t04 on the left with ⬜ and 🙋 3, t01's page on the right with Goal, Runs (r01-r04, run-design-block-page), Interactions. The code (focus_jobs.py) waits for JL.
- 16:55: s11's drawing, one zoom left to right (b17 Jobs → j03 → Tasks → t01 → its page: Goal, Runs r01-r04, Interactions), the picked step orange; looked at as PNG, the first arrow fixed to j03 and the emoji the PNG preview cannot draw taken out; Studio shows s11 with Page · Draw · Delivery.

- 17:05 code: 5623 b17 💼 Jobs, j03: its views read Main · t01 · Block page 🙋 3 · t02 · Job page 🙋 3 · t03 · Task page 🙋 3 · t04 · Shared parts; a click on t02 shows t02's page (🧭 Overview: Goal, Requirements, MindMap; 📊 Plan + Results: Runs; 🔎 Findings) in the same document; no 🔴. workbench 239, labeling 85, paper 112 pass. The preview and the drawing follow the same design.
- Left for next: the Task page itself still draws its MindMap fold and "No findings here." (the shared Task Report; s11 says neither).

## Summary

A Job in 💼 Jobs has its own view buttons, Main (its Report body) and one per Task with its marks (⏳ ✅, 🙋 N; open
shows none); a Task's view is its page drawn by the same pipeline, inside an open dot. s11 holds the decision, the
clickable preview and the drawing built from disk.
