# j14 · Draft Lab

goal: keep the Draft Task page of servers/workbench (workbench-task-draft/) healthy: each Task owns one module folder and checks and updates it, one round at a time
close: when this part of servers/workbench is retired; until then the Job stays open and its Tasks keep checking
bands: t0N Draft Lab parts

## Topic

The Draft Task page, the one Page every theme's draft Task opens: its shell and Steps view, the Plan, Evidence and Revise steps, the Runs tab, Delivery and the exports, and the standalone reader. It took over j13 t03 when the folder split into module folders. Every Job here is code work. Its delivery is the code in `plugins/haipipe-toolkit/servers/workbench/`, committed to the plugin.

A Task here never closes while its folder lives. Each Task keeps one standing Run, `runs/run-check-<folder>`, and each round is one dated pass of it: run the Task's ## Checks, fix what fails inside the folder, and write the results in the pass. A trace that changes the folder names the Task in `work:`.

Studio: none yet: a Task opens one when its design starts.

Code: `plugins/haipipe-toolkit/servers/workbench/`; each Task's face lists the files it owns, and a test sits with the file it tests.

## Tasks

<!-- in order; new_job.py task adds each -->
1. t01_page_shell · Page shell
2. t02_plan_outline · Plan and outline
3. t03_evidence_steps · Evidence steps
4. t04_revise_steps · Revise steps
5. t05_run_views · Run views
6. t06_delivery_export · Delivery and export
7. t07_reader · Reader
