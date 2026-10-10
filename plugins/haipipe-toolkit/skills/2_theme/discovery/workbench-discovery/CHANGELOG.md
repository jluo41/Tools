## 0.3.1 · 2026-10-09 · Theme folders are singular

- Docs name the singular Theme folders (s01-D29, JL 261007): `work/`, `discovery/`, `paper/`, `insight/`,
  `design/`, `labeling/`, `ideation/`; the older plural names still read.

## 0.3.0 · 2026-10-07 · The Guide moves to its server folder (JL 261007, via b02)

- `ref/discovery-method.md` → `servers/workbench-discovery/guide/method.md`, `ref/methods/` →
  `guide/methods/`, `ref/discovery-methods.excalidraw` → `guide/methods.excalidraw`,
  `ref/discovery-papers.md` → `servers/workbench-discovery/related/papers.md`; their links fixed.
- The `discovery` entry and `DISCOVERY_DESIGN` leave `servers/workbench/guide_families.py`; the
  same entry is `servers/workbench-discovery/guide/guide.yaml` (RoadMap Draw: the b14 design Block's
  `studio/s02-discovery-workbench/`). `ref/workbench-table.md` stays here; its `Tools ›` is the server folder.

## 0.2.0 · 2026-10-07 · Renamed from haipipe-workbench-discovery (JL 261007)

- The skill is `workbench-discovery` (was `haipipe-workbench-discovery`), its folder `discovery/workbench-discovery/`, its trigger `/workbench-discovery`; every live reference in Tools follows. Older entries below keep the old name.

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
