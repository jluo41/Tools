---
mindmap: 1
title: s03 · The Work workbench, today · structured
built: from-topic .
written: 261026, from the drawing task-workbench-design.excalidraw, frame by frame
---

# s03 · The Work workbench, today

The "before": the Task workbench as built, one Task Block, four Spaces; s01's ladder proposal replaces it.

- [design] One workbench, one Task Block <!-- n01 -->
  → What does each Space ask, and which runs answer it?
  - [row] Each Question: its Logic, its Task Work, its Report <!-- n02 -->
    Task Work is the chain that answers it: Block → Job → Task → Run.
  - [spaces] Four Spaces: Scope, Task, Check, Delivery <!-- n03 -->
  - [source] Drawn from the theme's workbench table <!-- n04 -->
    [task-workbench-design.py](task-workbench-design.py) reads `ref/workbench-table.md`; a rebuild rewrites it, so mark [s01's drawing](../s01-work-ladder/s01-work-ladder.excalidraw) instead.
- [Scope] What is this Block for, what does it ask? <!-- n05 -->
  → Then what answers each Question?
  - [Block] A view, no run <!-- n06 -->
  - [Questions] Ask a Question · Review the questions <!-- n07 -->
    haipipe-report ask (agent haipipe-task-block-agent*, signs the question) · haipipe-report review (agent haipipe-task-reviewer-agent, signs a change).
  - [Resources] Add a resource <!-- n08 -->
  - [RoadMap Draw] Draw the question map · Draw <!-- n09 -->
- [Task] What answers each Question? <!-- n10 -->
  → Did each run finish, and can each report be trusted?
  - [plan] Plan a Task · Review the plan <!-- n11 -->
  - [build] Build the Task · Review the Task code <!-- n12 -->
  - [run] Run a Task, by the orchestrator agent <!-- n13 -->
  - [report] Report the Run · Plan · Write the report <!-- n14 -->
    haipipe-task-plan* (creator agent) · haipipe-page-structure (structure agent) · haipipe-page-writing (writing agent). * marks a skill or agent planned, not yet built.
- [Check] Can each run and each report be trusted? <!-- n15 -->
  → Which answers are ready to leave the Block?
  - [Runs] A view, no run <!-- n16 -->
  - [Tasks] Check a Task, by the reviewer agent <!-- n17 -->
  - [Reports] Check a report, by the page-check agent <!-- n18 -->
  - [route] A failed check routes back; a passed one moves on <!-- n19 -->
- [Delivery] Which answers are ready to leave? <!-- n20 -->
  → How does the Task Space look on screen?
  - [build] Build the report: web, LaTeX and Word <!-- n21 -->
  - [sign] The writing agent signs the release <!-- n22 -->
- [screen] The Task Space: a row per Question <!-- n23 -->
  → And where does it all live on disk?
  - [table] Logic │ Task Work │ Report, one table per group <!-- n24 -->
  - [work] Task Work folds Block → Job → Task → Run <!-- n25 -->
  - [panel] The Runs panel: buttons, a prompt to copy <!-- n26 -->
    Status lives in the panel, never in the table. Picking a Question narrows the list; Copy hands the prompt to a session; nothing here starts a run.
- [disk] The Block folder behind it <!-- n27 -->
  → Why is this design kept here, not in the server?
  - [face] board.md: spine, close, Questions, resources <!-- n28 -->
  - [reports] reports/qNN_<topic>/: one report Page each <!-- n29 -->
  - [studio] studio/: the question map and free drawings <!-- n30 -->
  - [work] jNN_<job>/tNN_<task>/: the Task Page, code, Runs <!-- n31 -->
- [moved] Design lives with its theme's Block <!-- n32 -->
  - [from] Moved from the server's own studio/ (261007) <!-- n33 -->
  - [served] Shown in Guide › RoadMap Draw, view only <!-- n34 -->
    Its path is `TASK_DESIGN` in `plugins/haipipe-toolkit/servers/workbench/guide_families.py`.
  - [code] question_map.py stays: it is server code <!-- n35 -->
- [files] What the folder holds <!-- @files #6ce6c5 -->
  - [md] [plan-insight-style-261003.md](plan-insight-style-261003.md) <!-- @files/0 #ba7cda -->
  - [md] [s03-work-workbench.md](s03-work-workbench.md) <!-- @files/1 #06194d -->
  - [excalidraw] [task-workbench-design.excalidraw](task-workbench-design.excalidraw) <!-- @files/2 #71bc96 -->
  - [py] [task-workbench-design.py](task-workbench-design.py) <!-- @files/3 #638d27 -->
