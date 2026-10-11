s02 · Workbench UI
==================

**Topic:** the design workbench's own drawing: the skills, the method, the workbench (board level,
then page level, each Space with its Runs panel), the folders, and one design followed Run by Run.
It is what Guide › RoadMap Draw shows for the design family.

**Source:** `design-workbench-ui.py` writes `design-workbench-ui.excalidraw` beside it; the design
Guide's RoadMap Draw opens it here (moved from `servers/workbench-design/studio/`, 261007: the servers
hold code only).

**Feeds:** `../../reports/` q02_design_workbench.


Files
-----

```text
s02-workbench-ui/
├── s02-workbench-ui.md          this notes file
├── design-workbench-ui.excalidraw  the drawing (Guide › RoadMap Draw opens it)
├── design-workbench-ui.png      preview
├── design-workbench-ui.py       draws it
└── _archive/                    its predecessors (261002 and before), kept as history
    ├── design-board-workbench-design.excalidraw
    ├── design-workbench-design.excalidraw
    └── design-workbench-design-sms.excalidraw
```

Rebuild: `python3 design-workbench-ui.py`. It is an older author script: it does not keep canvas
marks the way `canvas.write` does, so fold any edit made on the served drawing into the script first.
A dry run on 261007 drew the same 392 elements as the drawing, with two texts different: check them
before the next rebuild.


Open
----

- Redraw it on the ladder agreed in `../s01-design/` (a Job = one goal × one method → N designs)?

(write here, or mark the drawing in red)
