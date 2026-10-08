b02 s02 · Guide views
=====================

**Topic:** the Guide's Views (Skill set, Methods, Workbench, Folder map, RoadMap Draw), drawn as
they appear in the Guide, with the Paper family as the example. One drawing:
`s02-guide-views.excalidraw`.

Split from the old `s02-guide-drawings/` (JL 261007: "each sNN just one draw").

Files
-----

```text
s02-guide-views/
├── s02-guide-views.md            this notes file
├── s02-guide-views.excalidraw    the drawing: all five Guide Views (generated)
├── build_s02_guide_views.py      its generator; also writes parts/ (reads s04's generator for the look)
├── drawing-catalog.json          the drawing types (skill map, method flow, UI map, folder map)
├── method-canvas.py              a tool, no drawing here: draws a theme's first
│                                 servers/workbench-<theme>/guide/methods.excalidraw from its method.md
└── parts/                        each View's drawing alone: the catalog's examples (generated)
```

Rebuild: `python build_s02_guide_views.py` (after `../s04-guide-design/build_s04_guide_design.py`).
