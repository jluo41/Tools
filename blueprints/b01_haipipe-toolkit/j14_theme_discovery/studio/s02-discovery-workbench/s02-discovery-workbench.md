s02 · Discovery workbench, today
================================

**Topic:** the Discovery workbench as it is built today: its Spaces, Views and run types, with each
run's skill and agent. It is the "before" that this Block's s01 ladder proposal replaces. Moved here
from `plugins/haipipe-toolkit/servers/workbench-discovery/studio/` (261007, JL: every workbench's studio
belongs to its theme's design Block); the server keeps no studio of its own.

**Served:** the workbench's Guide › RoadMap Draw shows this drawing, view only. Its path is
`explain.roadmap-draw` in `plugins/haipipe-toolkit/servers/workbench-discovery/guide/guide.yaml`.


Files
-----

```text
s02-discovery-workbench/
├── s02-discovery-workbench.md             this notes file
├── discovery-workbench-design.excalidraw  the drawing (generated: never edit it by hand)
└── discovery-workbench-design.py          draws it from the theme's ref/workbench-table.md
```

Rebuild: `python discovery-workbench-design.py`. It rewrites the whole drawing, so marks on it are lost: mark the s01
ladder drawing instead.
