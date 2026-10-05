# Changelog

## 0.1.0 · 2026-10-04

- New workbench (JL 261004: separate workbenches per kind, one style) for Blocks with
  `board-kind: discovery-block`: `servers/workbench-discovery/` (`discoveryboard.py` reads,
  `discovery_views.py` draws) at `/_board/discovery-board`, short `/w/<block>`, and a Project
  view at `?path=<Project>/discoveries`. Spaces Guide · Scope (Block, Questions, Resources,
  RoadMap Draw) · Work (Papers, Tasks, Questions) · Check (Runs, Citations, Reports) ·
  Delivery (Reports, BibTeX), each with the shared Runs panel from `ref/workbench-table.md`.
- Task Pages and Paper Runs are read with the Task Workbench's `task_snapshot`; each Paper
  Run adds its Result card (title, cite, subject, venue, verification, Readout), receipt
  (status, subject kind, reading depth, claim support) and one-entry BibTeX. The Task-only
  READING finding is left out. Style: the Task Workbench's own CSS and script files.
- Guide: `discovery` entry in `workbench-shared/guide_families.py`; `ref/discovery-method.md`
  (six steps), `ref/methods/discovery/` (8 cards), `ref/discovery-methods.excalidraw`,
  `ref/discovery-papers.md` (7 papers, checked online), and the generated
  `servers/workbench-discovery/studio/discovery-workbench-design.excalidraw`.
- Tests: `servers/workbench-discovery/tests/test_discoveryboard.py` (4). First used on
  Proj10-LLM-Baseline's 10 Discovery Blocks (490 Paper Runs).
