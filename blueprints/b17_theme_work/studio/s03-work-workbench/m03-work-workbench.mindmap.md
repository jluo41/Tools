---
mindmap: 1
title: s03 · The Work workbench, today · structured
built: from-topic .
written: 261026, from the topic's face
---

# s03 · The Work workbench, today

The "before": the workbench as built today, which s01's ladder proposal replaces.

- [today] What the workbench shows <!-- n01 -->
  → Where does a person see it?
  - [spaces] Its Spaces, Views and run types <!-- n02 -->
  - [owners] Each run's skill and agent <!-- n03 -->
  - [role] The "before" for s01's proposal <!-- n04 -->
    s01 draws the proposed ladder over it: [s01-work-ladder](../s01-work-ladder/s01-work-ladder.md).
- [served] Shown inside the workbench <!-- n05 -->
  → How is the drawing made?
  - [screen] Guide › RoadMap Draw, view only <!-- n06 -->
  - [path] TASK_DESIGN in guide_families.py <!-- n07 -->
    `plugins/haipipe-toolkit/servers/workbench/guide_families.py`
- [built] Generated, never edited by hand <!-- n08 -->
  → Why is it here, and not in the server?
  - [builder] Drawn from the theme's workbench table <!-- n09 -->
    [task-workbench-design.py](task-workbench-design.py) reads the theme's `ref/workbench-table.md`.
  - [warning] A rebuild rewrites it: marks are lost <!-- n10 -->
  - [instead] Mark the s01 ladder drawing instead <!-- n11 -->
    [s01-work-ladder.excalidraw](../s01-work-ladder/s01-work-ladder.excalidraw) keeps a person's marks.
  - [history] The 3 Oct plan remade it in Insight's style <!-- n12 -->
    [plan-insight-style-261003.md](plan-insight-style-261003.md)
- [moved] Design lives with its theme's Block <!-- n13 -->
  - [from] Moved from the server's own studio/ (261007) <!-- n14 -->
    From `plugins/haipipe-toolkit/servers/workbench-work/studio/`. JL: every workbench's studio belongs to its theme's design Block; the server keeps no studio of its own.
  - [code] question_map.py stays: it is server code <!-- n15 -->
    It draws a work Block's question map, so it moved up beside `task_questions.py`, to `servers/workbench-work/question_map.py`.
- [files] What the folder holds <!-- @files #6ce6c5 -->
  - [md] [plan-insight-style-261003.md](plan-insight-style-261003.md) <!-- @files/0 #ba7cda -->
  - [md] [s03-work-workbench.md](s03-work-workbench.md) <!-- @files/1 #06194d -->
  - [excalidraw] [task-workbench-design.excalidraw](task-workbench-design.excalidraw) <!-- @files/2 #71bc96 -->
  - [py] [task-workbench-design.py](task-workbench-design.py) <!-- @files/3 #638d27 -->
