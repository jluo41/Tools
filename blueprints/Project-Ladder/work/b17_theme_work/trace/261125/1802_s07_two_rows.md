---
title: s11 two rows
date: 2026-11-25 18:02
topic: s11-work-job-preview
aim: Every Job and Task stays a visible button, one click away, in at most two rows; a decade's topic is a small grey word inside the row (j1N Workbench · j11 j12 … │ j0N earlier · j01 …), not a row of its own; with many Tasks a Task button shows its number and its name only when picked or hovered. No menus, no switch.
closed: true
plan:
  - do: add
    path: blueprints/Project-Ladder/work/b17_theme_work/trace/261125/1802_s07_two_rows.md
    what: this trace's own record, written first
  - do: add
    path: blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/delivery/ui/job-view-rows.html
    what: the preview, two rows with the topics inside them; a FEW / MANY toggle in the preview only, to see b17 today and a Block with 12 Jobs and 14 Tasks
  - do: edit
    path: blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/s11-work-job-preview.html
    what: Two rows first; Path + menus and Rows (today) after it, faded (class old)
  - do: edit
    path: blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/build_s11_work_job_preview.py
    what: MANY in the drawing becomes two rows with the topic words inside; no switch mark; rebuilt and looked at
  - do: edit
    path: blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/s11-work-job-preview.md
    what: the Decision records 18:06 (no menus; see and get) and the two-row design
changed:
  - blueprints/Project-Ladder/work/b17_theme_work/trace/261125/1802_s07_two_rows.md
  - blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/delivery/ui/job-view-rows.html
  - blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/s11-work-job-preview.html
  - blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/build_s11_work_job_preview.py
  - blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/s11-work-job-preview.excalidraw
  - blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/s11-work-job-preview.png
  - blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/s11-work-job-preview.md
---

# s11 two rows

## Prompts

- **18:02** [the path row • j03 · Work workbench pages › • Main] I don't like this. [MANY's four rows] still want things here, to see, to get.

## Check

- drawing: MANY redrawn as two rows with the topic words inside (j2N Paper · j21 … │ j1N Workbench · j11 … │ j0N earlier · j01 j02 j03 faded; Main │ t0N Build · t01-t09 │ t1N Check · t10-t14); the picked j11 first fell on its topic word, fixed.
- preview in s11 (Studio's narrow frame, about 560 px): FEW, b17's six Jobs with their topic words; MANY (12 Jobs, 14 Tasks), earlier Jobs and all Tasks as numbers, names on hover and when picked: Jobs wrap to 3 lines, Tasks to 2. In the page's full width it is fewer; the narrow frame is the hard case.

## Summary

Every Job and Task stays a visible button; the topic is a grey word in its row; past 7 the names shorten to numbers. No menus, no switch, no code yet (page/ paused).
