haipipe-application-venue — Changelog
=====================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## [1.0.0] — 2026-06-23

- initial version modeled on paper-venue.

## [2.0.0] — 2026-07-06

- moved AFTER claims (was after pitch); pin writes venue + stages_skipped + claims_settlement; retarget rule inverted (claims survives, settlement may deepen); minimap column retired (paper-alignment refactor, SOP archived in haipipe-application/CHANGELOG.md §5.0.0).

## [3.0.0] — 2026-07-06

- Port of paper venue 2.0.0 (765696f): venue becomes an artifact-producing stage — writes 0-lifecycle/2-venue/2-venue.md + _LOG + _PROBE/ with Artifact Principles (the downstream contract pitch/display/section-edit/artifact read); still writes the 3 STATUS rows; dual-2 numbering mirrors paper (2-venue + 2-pitch).
