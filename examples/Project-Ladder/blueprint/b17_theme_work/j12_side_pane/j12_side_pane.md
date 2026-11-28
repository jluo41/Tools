# j12 · Side pane

goal: keep the side pane of servers/workbench (side_pane/) healthy: each Task owns one folder and checks and updates it, one round at a time
close: when this part of servers/workbench is retired; until then the Job stays open and its Tasks keep checking
bands: t0N Pane components

## Topic

The right split pane: the Files tree with the current scope highlighted and the rest faded, and the rail sections (Studio, Report, Timeline, Skills) opened from the round bottom-right menu. Every Job here is code work. Its delivery is the code in `plugins/haipipe-toolkit/servers/workbench/`, committed to the plugin.

A Task here never closes while its folder lives. Each Task keeps one standing Run, `runs/run-check-<folder>`, and each round is one dated pass of it: run the Task's ## Checks, fix what fails inside the folder, and write the results in the pass. A trace that changes the folder names the Task in `work:`.

Studio: s31-files-pane.

Code: `plugins/haipipe-toolkit/servers/workbench/`; each Task's face lists the files it owns, and a test sits with the file it tests.

## Tasks

<!-- in order; new_job.py task adds each -->
1. t01_files_tree · Files tree
2. t02_rail_sections · Rail sections
3. t03_pane_speed · Pane speed

