haipipe-application-display — Changelog
=======================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.

## [4.1.0] — 2026-07-14

Changed (PROBE LAYER REDESIGN — Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3, approved JL 2026-07-14)
- A unit whose data source does not exist yet is raised as a question SECTION in `1-probes/` (`serves: 4-display`); the PROBE worker MATCHes the bank first and commissions the unit only if it does not already exist. The per-stage `_PROBE/` folder is RETIRED.
- Display never writes under `tasks/` (LAW 1: a consumer session never executes task/discovery work inline). It never ran `/haipipe-task` inline before; that boundary is now named as the law it always was.
- ("metric-card" as a display UNIT TYPE is untouched — it is not a probe card, and the rename does not reach it.)

## [1.0.0] — 2026-06-22

- initial version as haipipe-application-variants.

## [2.0.0] — 2026-06-23

- renamed from variants to display; match paper vocabulary; venue-gated.

## [3.0.0] — 2026-06-29

- added _LOG, _PROBE/ subfolder. Output folder 4-display/ (was flat file). Complex venues (dashboard, report) get .tex + PDF for visual preview. Simple venues stay .md only. Borrowed per-stage tracking pattern from paper.

## [4.0.0] — 2026-07-06

- absorbs minimap: per-unit Job field required; materialization routes through the PROBE worker to /haipipe-task; stage-folder paths; DPRC phases (paper-alignment refactor, SOP archived in haipipe-application/CHANGELOG.md §5.0.0).

## [4.1.0] — 2026-07-06

- 765696f port: visible Probes section + reads 2-venue.md Artifact Principles + ascii artifact formatting.
