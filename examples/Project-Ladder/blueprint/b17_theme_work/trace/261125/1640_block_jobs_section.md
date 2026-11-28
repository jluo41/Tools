---
title: block jobs section
date: 2026-11-25 16:40
aim: A Block's sections menu has 💼 Jobs, the place to work; its view buttons are the Block's own jNN, and the picked Job's Main (its bands and folds) sits right on the Block page, switched in place. The Report keeps its Jobs fold for reporting.
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1640_block_jobs_section.md
    what: this trace's own record, written first
  - do: add
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_jobs.py
    what: own_jobs(folder) the Block's jNN in order; section(theme, root, folder, group) builds each Job's Report body with the page pipeline (page_route ... section_body) and returns its bar and body, switched by data-job-pane
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/block_index_page/focus_render.py
    what: rail_sections adds ('jobs', '💼 Jobs') after Report on a Block with jNN; section_body draws it through focus_jobs
  - do: add
    path: plugins/haipipe-toolkit/servers/workbench/tests/test_focus_jobs.py
    what: a Block with two Jobs has Jobs in its rail; section=jobs lists j01 and j02 as view buttons and holds both Jobs' bands
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1640_block_jobs_section.md
  - plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_jobs.py
  - plugins/haipipe-toolkit/servers/workbench/page/block_index_page/focus_render.py
  - plugins/haipipe-toolkit/servers/workbench/tests/test_focus_jobs.py
  - plugins/haipipe-toolkit/servers/workbench/tests/test_work_frame.py
---

# block jobs section

## Prompts

- **16:35** do you think we should have the jobs here? how do you think here? just like the studio? [the Report word's sections menu]
- **16:37** how we should display the job? each job is one view?
- **16:40** you can try to add it. so the Job will be place to work, and in the Report, we also have Jobs, but that is for reporting, right? what is your thougths?
- **16:50** So I can tell that Studio is design heavy (can change the code), and Job is code heavy (auto , and also need a bit human design) This is my thoughts.

## Check

- 5623 b17: the sections menu reads Report, 💼 Jobs, 🎨 Studio, ...; section=jobs shows j01 · Work ladder contract, j02 · Workbench work skill, j03 · Work workbench pages, j01's 🧭 Overview, 📊 Plan + Results (Tasks), 🔎 Findings; a click on j02 shows j02's folds in the same document and the URL reads group=j02. The page renders in 0.56 s.
- workbench 238 (new test_focus_jobs.py; test_work_frame's rail order now has 💼 Jobs after Report), labeling 85, paper 112, design 58 pass.

## Summary

`focus_jobs.section` runs the page pipeline (`page_route` ... `section_body`) on each own jNN and lays its Report body
on the Block page, one `data-job-pane` per Job, switched by its own script (not `data-pane`, which each Job's inner
Main already uses). The rail gets 💼 Jobs after Report on a Block with Jobs. The Report's Jobs fold stays for
reporting. JL's frame for the two: Studio is design heavy (a person changes the design), Jobs is code heavy (it runs
by itself and asks a person for a little design).
