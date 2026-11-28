---
title: job vs studio
date: 2026-11-25 14:52
task: j03_work_workbench_pages/t04_shared_parts
aim: hai-block's constitution says what a Job is (a fixed workflow, coding heavy, closed by a check a command runs) and what a Studio topic is (free design a person drives, closed when the person picks), with a check that finds every Job whose close waits on a person.
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1452_job_vs_studio.md
    what: this trace's own record, written first
  - do: edit
    path: plugins/haipipe-toolkit/skills/1_base/project/hai-block/CONSTITUTION.md
    what: A06 Job is a fixed workflow, Studio is free design; A05 picks open in the main page
  - do: add
    path: plugins/haipipe-toolkit/skills/1_base/project/hai-block/scripts/job_close_check.py
    what: lists every Job whose close line waits on a person (agreed, signed, approved)
  - do: add
    path: plugins/haipipe-toolkit/skills/1_base/project/hai-block/constitution/A06-job-is-a-workflow.md
    what: report for A06
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1452_job_vs_studio.md
  - plugins/haipipe-toolkit/skills/1_base/project/hai-block/CONSTITUTION.md
  - plugins/haipipe-toolkit/skills/1_base/project/hai-block/scripts/job_close_check.py
  - plugins/haipipe-toolkit/skills/1_base/project/hai-block/constitution/A06-job-is-a-workflow.md
  - examples/Project-Ladder/blueprint/b17_theme_work/j01_work_ladder_contract/j01_work_ladder_contract.md
  - examples/Project-Ladder/blueprint/b17_theme_work/j03_work_workbench_pages/j03_work_workbench_pages.md
---

# job vs studio

## Prompts

- **14:46** do you think it should be in our block? how do you think? should this be a job? is this what I am not sure.
- **14:48** for here, what is the differences between job and studio? I still cannot tell the differences.
- **14:50** they can stil be many overlapping, right? I think this is the things I am still not very clean. What I think is job is more AI-auto, and studio will be human driven. I am not sure
- **14:52** okay, a new trace now, so I think the job should be coding heavy, right? and no much design things, it is like the fixed workflow, they are in the job, and studio will be free style things. I can think and design.

## Check

- job_close_check.py: 30 Jobs, 8 waited on a person before; 6 now, none in b17 (b11, b12, b15, b16, b35 left to their sessions).
- constitution.py --check lists hai-block A06 with its report.

## Summary

hai-block A06: a Job is a fixed, coding-heavy workflow closed by a check; a Studio topic is free design closed by
the person. b17 j01 and j03 closes rewritten as checks. A05 now says a menu pick opens in the main page and the side
pane holds Files only.
