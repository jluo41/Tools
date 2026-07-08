haipipe-paper-probe-display — Changelog
=======================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## [2.0.0] — 2026-07-07

Changed (Part-0 harvester ruling, JL: "they are the harveste agents... just one step within the whole probe")
- BREAKING: Phase 3 ROUTE retired — this worker no longer calls /haipipe-task or task agents directly (that bypassed the gateway AND ran with no PP card = no receipt, invisible to the checker; the harvest-hole class in a second place). Unit generation is now commissioned like any evidence need: PLAN emits probe-plan suggestions → PP card → gateway → task orchestrator, with the gateway's SWEEP answering "does this unit already exist?" before new work. LINK becomes the harvest step (expand unit_refs; connect landed units), under the display lane's OWED→accepted machinery.
- Lifecycle is now AUDIT→PLAN→LINK→REVIEW (4 phases); allowed-tools: Agent/Skill dropped.
- Added the missing feedback/ inbox (B11 — was the only probe worker without one).

## [1.1.0] — 2026-07-03

- phase spine renamed DGPC -> DPRC (GATHER->PROBE, POLISH->REVISE).

## [1.0.0] — 2026-07-02

- created as the display gather worker. Previously no dedicated skill existed.
