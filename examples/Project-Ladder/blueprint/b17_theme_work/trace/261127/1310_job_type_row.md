---
title: job type row
date: 2026-11-27 13:10
work: [s11, s71]
aim: "A Block's 💼 Jobs gains a Job type row above its Job group row: All, then each `job-type:` its Jobs' faces name; a pick shows only the groups and Jobs of that type. A Job's type is one face field, job-type:, apart from its group (board.md bands:). s71 Studio Type: Block Job UI Preview draws the Jobs page's rows as a folder tree and lists s11-s14 as its examples."
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1310_job_type_row.md
    what: this trace's own record, written first
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_jobs.py
    what: a Job type row (All + each job-type:) above the Job group row, drawn only when a Job names one; picking it filters the group and Job rows
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/tests/test_focus_jobs.py
    what: the row is drawn when Jobs name types (each Job button carries its type), and not when none does
  - do: edit
    path: examples/Project-Ladder/work/b01_example_work/ (11 Job faces)
    what: "job-type: code (j01, j12, j13, j15, j16, j17, j21), doc (j02, j18), check (j11, j14)"
  - do: edit
    path: plugins/haipipe-toolkit/skills/1_base/project/hai-job/SKILL.md
    what: "defines job-type: (what kind of Job; its group stays the Block's bands:)"
  - do: edit
    path: plugins/haipipe-toolkit/skills/2_work/work/hai-work/SKILL.md
    what: "the bands: grouping is called Job group, not Job type; Job type is job-type:"
  - do: edit
    path: plugins/haipipe-toolkit/skills/2_work/work/workbench-work/SKILL.md
    what: "its two 'section per Job type' lines say Job group (the same naming, swept)"
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/ (its face, a new studio-views.json and delivery/rows.html)
    what: Shape (the Jobs page rows as a folder tree) and Examples (s11-s14), named as the b17 session asked so s70-s79 read alike; the face keeps Holds as one line and gains a Definition section
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/s11-work-job-preview.md
    what: its Decision notes say the Jobs page has a Job type row
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1310_job_type_row.md
  - plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_jobs.py
  - plugins/haipipe-toolkit/servers/workbench/page/job_task_views/tests/test_focus_jobs.py
  - examples/Project-Ladder/work/b01_example_work/ (11 Job faces, job-type:)
  - plugins/haipipe-toolkit/skills/1_base/project/hai-job/SKILL.md
  - plugins/haipipe-toolkit/skills/2_work/work/hai-work/SKILL.md
  - plugins/haipipe-toolkit/skills/2_work/work/workbench-work/SKILL.md
  - examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/ (face Definition, studio-views.json, delivery/rows.html)
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/s11-work-job-preview.md
---

# job type row

## Prompts

- **13:08** so they will be the job type, right? [Image #49] I think here, we should also have the job type as well a the top view buttom. okay, for this, how do you think you should update this [Image #50]
- **13:12** go go go

## Check

- 5623's b01_example_work Jobs (Chrome): rows read Job type (All · code · check · doc), Job group (Ideas j2N · Second version j1N · First version j0N), Jobs, then Main · Tasks.
- Picking (Chrome): check shows only Second version and j11, j14; doc shows Second and First version and opens j18 (the first doc Job), then First version opens j02; code shows j01 there; All brings every group back.
- First try kept j11 open after picking doc (the group pick reopened a hidden Job); fixed: a group pick opens only a visible Job.
- 5623's b17 Studio (Chrome): s71 has Shape (the rows as a folder tree, one item so full width) and Examples (left tabs s11 Work, s12 Blueprint, s13 CoWork, s14 Discovery).
- Tests: workbench page, side_pane, studio, home 246 passed, 1 skipped; the Job type tests: the row above the groups with each type, each Job and group carrying its types; no row when no Job names a type.
- 5623 and 5602 restarted, both 200.

## Summary

A Block's Jobs has a Job type row above its group row; a Job's type is its face's job-type:, its group the Block's bands:. s71 shows the Jobs page's rows as a folder tree and s11-s14 as its examples.
