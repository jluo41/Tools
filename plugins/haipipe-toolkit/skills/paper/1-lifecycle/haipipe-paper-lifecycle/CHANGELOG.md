haipipe-paper-lifecycle — Changelog
===================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## [2.1.0] -- 2026-07-08

Changed
- Routing description adopts venue lockfile semantics: venue stage compiles 0-lifecycle/2-venue/2-venue.md (the venue contract with pack+outlet+commit provenance); new Venue consumption rule -- aligned stages read 2-venue.md FIRST (pitch: Venue Profile + Fit Assessment; narrative: Blueprint beats + Writing Principles; display: display units + limits; section-edit: per-section Blueprint block), packs only as fallback when 2-venue.md is absent or as deep dives via its [source] tags; stale provenance -> "venue contract stale" note, never silent pack re-reads.

## [2.0.3] — 2026-07-03

Fixed
- Closing-line rule updated: stage skills close with the FULL closing block (simplified tail + stage line + phase line) per the umbrella Closing Block section, not just the stage strip line.

## [2.0.2] — 2026-07-03

- haipipe-paper-folder specialist description updated to the minimal quick scaffold (absent-until-written; manuscript machinery on request; repo wiring belongs to /haipipe-paper create); seed description corrected to the 3-section contract; retired prospectus / kill-criteria keywords removed from the maps.

## [2.0.1] — 2026-07-03

- phase spine renamed DGPC -> DPRC (GATHER -> PROBE, POLISH -> REVISE; workers 2-phase/1-probe/haipipe-paper-probe*, 2-phase/2-revise/haipipe-paper-revise*).

## [2.0.0] — 2026-07-03

- lifecycle reordered to the current spine (claims (1) before pitch (2), venue as the decision gate between them); minimap stage removed; section-edit added as stage 5 (per-paper folder renamed 5-editing -> 5-section-edit); two-axis restructure documented (stage skills x DRAFT->GATHER->POLISH->CHECK phases via 2-phase/ workers, CHECK the only human-involved phase); folder dispatch fixed to haipipe-paper-folder; shared conventions repointed to ../../wiki/NN-* (ref/ consolidated into wiki/).

## [1.0.0] — 2026-06-08

- created as orchestrator over all 1-lifecycle specialists.
