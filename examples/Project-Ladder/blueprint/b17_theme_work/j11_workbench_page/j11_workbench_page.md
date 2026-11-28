# j11 · Workbench page

goal: keep the page framework of servers/workbench (page/ and home/) healthy: each Task owns one folder and checks and updates it, one round at a time
close: when this part of servers/workbench is retired; until then the Job stays open and its Tasks keep checking
bands: t0N Page components

## Topic

The page framework every theme's workbench stands on: how a Block is the one index page, how its Jobs and Tasks show as views with bands and folds, the marks on every element, the shared parts, and the Home and Project pages above the Block. Every Job here is code work. Its delivery is the code in `plugins/haipipe-toolkit/servers/workbench/`, committed to the plugin.

A Task here never closes while its folder lives. Each Task keeps one standing Run, `runs/run-check-<folder>`, and each round is one dated pass of it: run the Task's ## Checks, fix what fails inside the folder, and write the results in the pass. A trace that changes the folder names the Task in `work:`.

Studio: s04-discovery-structure (the page shape), s11-work-job-preview (Job and Task views, t02).

Code: `plugins/haipipe-toolkit/servers/workbench/`; each Task's face lists the files it owns, and a test sits with the file it tests.

## Tasks

<!-- in order; new_job.py task adds each -->
1. t01_block_index_page · Block index page
2. t02_job_task_views · Job and Task views
3. t03_element_marks · Element marks
4. t04_parts_and_map · Shared parts and file map
5. t05_home_and_project · Home and Project pages

