s02 · Labeling workbench, today
===============================

**Topic:** the Labeling workbench as it is built today: its Spaces, Views and run types, with each
run's skill and agent. It is the "before" that this Block's s01 ladder proposal replaces. Moved here
from `plugins/haipipe-toolkit/servers/workbench-labeling/studio/` (261007, JL: every workbench's studio
belongs to its theme's design Block); the server keeps no studio of its own.

**Served:** the workbench's Guide › RoadMap Draw shows this drawing, view only. Its path is
`LABELING_DESIGN` in `plugins/haipipe-toolkit/servers/workbench/guide_families.py`.


Files
-----

```text
s02-labeling-workbench/
├── s02-labeling-workbench.md         this notes file
├── labeling-workbench-ui.excalidraw  the drawing (generated: never edit it by hand)
├── labeling-workbench-ui.py          draws it from the theme's ref/workbench-table.md
└── labeling-shared-rules.md          how the Labeling workbench met the shared workbench rules
```

Rebuild: `python labeling-workbench-ui.py`. It rewrites the whole drawing, so marks on it are lost: mark the s01
ladder drawing instead.
