haipipe-application-venue — Changelog
=====================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.

## [3.1.0] — 2026-07-14

Changed (PROBE LAYER REDESIGN — Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3, approved JL 2026-07-14)
- Venue-level questions (channel capability, compliance constraints, prior sends) are SECTIONS with `serves: 2-venue` in `1-probes/PPNN_<topic>.md` at the intervention root. The per-stage `0-lifecycle/2-venue/_PROBE/` folder is RETIRED — probe files live in ONE flat pool, and stage affinity is the section's `serves:` field, never its path.

## [1.0.0] — 2026-06-23

- initial version modeled on paper-venue.

## [2.0.0] — 2026-07-06

- moved AFTER claims (was after pitch); pin writes venue + stages_skipped + claims_settlement; retarget rule inverted (claims survives, settlement may deepen); minimap column retired (paper-alignment refactor, SOP archived in haipipe-application/CHANGELOG.md §5.0.0).

## [3.0.0] — 2026-07-06

- Port of paper venue 2.0.0 (765696f): venue becomes an artifact-producing stage — writes 0-lifecycle/2-venue/2-venue.md + _LOG + _PROBE/ with Artifact Principles (the downstream contract pitch/display/section-edit/artifact read); still writes the 3 STATUS rows; dual-2 numbering mirrors paper (2-venue + 2-pitch).
