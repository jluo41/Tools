s02 · CoWork workbench, today
=============================

**Topic:** the CoWork workbench as it is built today: its Spaces, Views and run types, with each
run's skill and agent. It is the "before" that this Block's s01 ladder proposal replaces. Moved here
from `plugins/haipipe-toolkit/servers/workbench-cowork/studio/` (261007, JL: every workbench's studio
belongs to its theme's design Block); the server keeps no studio of its own.

**Served:** the workbench's Guide › RoadMap Draw shows this drawing, view only. Its path is
`COWORK_DESIGN` in `plugins/haipipe-toolkit/servers/workbench/guide_families.py`.


Files
-----

```text
s02-cowork-workbench/
├── s02-cowork-workbench.md             this notes file
├── cowork-workbench-design.excalidraw  the drawing (generated: never edit it by hand)
└── cowork-workbench-design.py          draws it from the theme's ref/workbench-table.md
```

Rebuild: `python cowork-workbench-design.py`. It rewrites the whole drawing, so marks on it are lost: mark the s01
ladder drawing instead.
