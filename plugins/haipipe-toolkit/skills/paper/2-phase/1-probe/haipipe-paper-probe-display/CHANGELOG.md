haipipe-paper-probe-display — Changelog
=======================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## [3.0.1] -- 2026-07-10

Fixed (fresh-agent audit, C2/C3/C4/M16)
- Intro line still said "commissioning generation through the probe" -- now "requesting missing units via DR rows".
- HB scope carve-out: the no-commissioning ban binds section/narrative context; invoked BY the display stage on its own accepted units, commissioning follows the display hub's PROBE lanes (no DR row into the stage's own inbox).
- HB4 comment home updated to md-first: > USER: threads in 4-display.md (4-display.tex is generated); anti-pattern line matched.
- Hard Boundary numbering de-duplicated (two "2." -> 2/3/4/5).

## [3.0.0] -- 2026-07-10

Changed -- BREAKING (JL: "In section-edit, we don't create the display ourself")
- Unit generation from section context is RETIRED entirely (both direct /haipipe-task and PP card -> gateway -> task). PLAN now files a DR request row in `0-lifecycle/4-display/_DISPLAY_REQUEST.md` (the display stage's inbox; DRNN numbering, bullet lines, status requested -> accepted -> done|declined, only the display stage advances it).
- New Hard Boundary 2: section-edit never CREATES a display; the display stage (index, interrogation, venue set, gallery, CHECKLIST) is the only creator.
- LINK only touches units that exist or whose DR row is done; 📨 pending requests flagged for CHECK, never pre-placed \ref.

## [2.0.0] — 2026-07-07

Changed (Part-0 harvester ruling, JL: "they are the harveste agents... just one step within the whole probe")
- BREAKING: Phase 3 ROUTE retired — this worker no longer calls /haipipe-task or task agents directly (that bypassed the gateway AND ran with no PP card = no receipt, invisible to the checker; the harvest-hole class in a second place). Unit generation is now commissioned like any evidence need: PLAN emits probe-plan suggestions → PP card → gateway → task orchestrator, with the gateway's SWEEP answering "does this unit already exist?" before new work. LINK becomes the harvest step (expand unit_refs; connect landed units), under the display lane's OWED→accepted machinery.
- Lifecycle is now AUDIT→PLAN→LINK→REVIEW (4 phases); allowed-tools: Agent/Skill dropped.
- Added the missing feedback/ inbox (B11 — was the only probe worker without one).

## [1.1.0] — 2026-07-03

- phase spine renamed DGPC -> DPRC (GATHER->PROBE, POLISH->REVISE).

## [1.0.0] — 2026-07-02

- created as the display gather worker. Previously no dedicated skill existed.
