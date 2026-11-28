# j13 · Studio and Guide

goal: keep Studio and Guide of servers/workbench (studio/, guide/) healthy: each Task owns one folder and checks and updates it, one round at a time
close: when this part of servers/workbench is retired; until then the Job stays open and its Tasks keep checking
bands: t0N Studio and Guide

## Topic

The tools served inside a workbench page for drawing and explaining: Studio's tabs and its canvas, and the Guide pages. The Draft Task page moved to j14 and the chat and terminal to j15. Every Job here is code work. Its delivery is the code in `plugins/haipipe-toolkit/servers/workbench/`, committed to the plugin.

A Task here never closes while its folder lives. Each Task keeps one standing Run, `runs/run-check-<folder>`, and each round is one dated pass of it: run the Task's ## Checks, fix what fails inside the folder, and write the results in the pass. A trace that changes the folder names the Task in `work:`.

Studio: none yet: a Task opens one when its design starts.

Code: `plugins/haipipe-toolkit/servers/workbench/`; each Task's face lists the files it owns, and a test sits with the file it tests.

## Tasks

<!-- in order; new_job.py task adds each -->
1. t01_studio · Studio tabs
2. t02_guide · Guide
3. t03_draft_lab · Draft Lab (moved to j14)
4. t04_canvas · Canvas
