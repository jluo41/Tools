---
title: workbench jobs
date: 2026-11-25 17:40
work: [j11, j12, j13]
aim: "Every folder and file of plugins/haipipe-toolkit/servers/workbench is managed by one b17 Job: j11 the page framework, j12 the side pane, j13 the tools inside the page."
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1740_workbench_jobs.md
    what: this trace's own record, written first
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/j11_workbench_page/
    what: Job face and Tasks t01 block index page, t02 job and task views, t03 element marks, t04 parts and map, t05 home and project
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/j12_side_pane/
    what: Job face and Tasks t01 files tree, t02 rail sections
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/j13_workbench_tools/
    what: Job face and Tasks t01 studio, t02 guide, t03 draft lab
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/board.md
    what: list j11, j12, j13 if new_job.py does not
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1740_workbench_jobs.md
  - examples/Project-Ladder/blueprint/b17_theme_work/j11_workbench_page/ (face and t01 to t05)
  - examples/Project-Ladder/blueprint/b17_theme_work/j12_side_pane/ (face and t01, t02)
  - examples/Project-Ladder/blueprint/b17_theme_work/j13_workbench_tools/ (face and t01 to t03)
---

# workbench jobs

## Prompts

- **17:00** I want to have a job, I think the job1, I will rename to be server-workbench job, this mention how do we design haipipe-toolkit/servers/workbench
- **17:05** I want to create the j01 for it, what are the tasks? how do you want to design it?
- **17:10** how do you map each tasks to the workbench folder?
- **17:15** why studio, guide, and workbench-task-draft is not in it?
- **17:20** or should we have differnet jobs for it? so for this one, I want to make the jobs to make the server/workbench to be managemented
- **17:30** two many jobs, we need to save the jobs.
- **17:40** okay, I will call it j11 ... I want to have the j12 to be side_pane, put them seprate ... Please udpate it.

- **17:45** so these jobs are mainly code driven, try to main the code quality, delivery the code to the plugins, etc. right?
- **17:46** we can also map the jobs to the studio as well.

## Check

- `new_job.py check`: j11, j12, j13 each "Tasks and its Task folders agree"
- every page/*.py has exactly one owning Task (no owner: none, two owners: none)
- b17 on 5623 shows j11, j12, j13 and their Tasks; board.md needed no edit

## Summary

j11 (5 Tasks), j12 (2) and j13 (3) are made with new_job.py; each Job names its Studio topic and its code-quality close; each Task's ## Files now names its folder (1748_page_subfolders).
