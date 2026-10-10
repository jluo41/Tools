s03 · Work workbench, today
===========================

**Topic:** the Work workbench as it is built today: its Spaces, Views and run types, with each
run's skill and agent. It is the "before" that this Block's s01 ladder proposal replaces. Moved here
from `plugins/haipipe-toolkit/servers/workbench-work/studio/` (261007, JL: every workbench's studio
belongs to its theme's design Block); the server keeps no studio of its own.

**Served:** the workbench's Guide › RoadMap Draw shows this drawing, view only. Its path is
`TASK_DESIGN` in `plugins/haipipe-toolkit/servers/workbench/guide_families.py`.

`question_map.py`, which draws a work Block's question map, is server code, not design: it
moved up beside `task_questions.py`, to `servers/workbench-work/question_map.py`.


Files
-----

```text
s03-work-workbench/
├── s03-work-workbench.md             this notes file
├── task-workbench-design.excalidraw  the drawing (generated: never edit it by hand)
├── task-workbench-design.py          draws it from the theme's ref/workbench-table.md
└── plan-insight-style-261003.md      the 3 Oct plan that remade it in the Insight workbench's style
```

Rebuild: `python task-workbench-design.py`. It rewrites the whole drawing, so marks on it are lost: mark the s01
ladder drawing instead.
