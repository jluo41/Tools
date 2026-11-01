b02 s04 · Guide design
======================

**Topic:** the Guide UI design (261002): Guide holds family explanations only, and working Views
stay in their own workbench's Spaces. One drawing: `s04-guide-design.excalidraw` (v4, the design
that was kept).

Split from the old `s02-guide-drawings/` (it was `workbench-shared-guide-v4`, 261007).

Files
-----

```text
s04-guide-design/
├── s04-guide-design.md              this notes file
├── s04-guide-design.excalidraw      the drawing, v4 (generated)
├── build_s04_guide_design.py        its generator (its primitives come from history/)
└── history/                         the earlier versions, kept as the record, each with its generator:
    ├── workbench-shared-design.*    v1, the first composition; also the drawing primitives v2 and v4 import
    ├── workbench-shared-guide-v2.*  v2, grouped Views
    └── workbench-shared-guide-v3.*  v3, horizontal Views
```
