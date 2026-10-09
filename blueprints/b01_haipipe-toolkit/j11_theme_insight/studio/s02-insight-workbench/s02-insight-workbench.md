s02 · Insight workbench, today
==============================

**Topic:** the Insight workbench as it is built today: its five Spaces after the Guide (Scope ·
Prototype · Insight · Check · Delivery), every View, every run type with its skill and agent, and
where each reads and writes on disk. It is the "before" that s01-insight-ladder's proposal replaces.
Moved here from `plugins/haipipe-toolkit/servers/workbench-insight/studio/` (261007, JL: the
workbench's studio belongs to its Block); the server keeps no studio of its own.

**Served:** the workbench's Guide › RoadMap Draw shows this drawing, view only. The path is
`explain.roadmap-draw` in `plugins/haipipe-toolkit/servers/workbench-insight/guide/guide.yaml`
(the Insight Guide, moved out of `servers/workbench/guide_families.py` on 261007).

**Feeds:** `reports/` q01_insight_ladder (the View each level replaces), q03_question_gates
(today's Check Space).


Files
-----

```text
s02-insight-workbench/
├── s02-insight-workbench.md           this notes file
├── insight-workbench-design.excalidraw the drawing (generated: never edit it by hand)
├── insight-workbench-design.py         draws it from workbench-insight/ref/workbench-table.md
└── chat/chat-insight-remake-261002.*   the design chat that led to it (.md summary · .jsonl)
```

Rebuild: `python insight-workbench-design.py`. It writes through haipipe-studio's `canvas.write`
(261007): black, red and green only, the selected tab drawn bold, and a person's marks kept on a
rebuild (seed snapshot `.insight-workbench-design.seed.json` beside the drawing).
