haipipe-application-venue — Changelog
=====================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## [0.3.4] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 3.4.0; older entries below keep their original numbers).

## [3.4.0] — 2026-07-19

- ⑩ probe files hold `## QX<n>` ENTRIES, not "sections" — wording corrected.


## [3.3.0] — 2026-07-18

- Template alignment sweep: dropped the template's "How to use:" header line; Q-consumer questions renamed `## Q<n>` -> `## Q-Venue-<n>` (id carries the origin stage) + reshaped to the fixed 3-field form Ask / Why / Answer (`__TO_BE_FILLED__` == OPEN, else ANSWERED — the doc's only state). SKILL skeleton + formatting synced.

## [3.2.0] — 2026-07-17

- Q-consumer migration: template + SKILL `Probes` -> `Q-consumer` (`## Q` blocks; venue-level investigation questions).

## [3.1.0] — 2026-07-17

- Template D2: Artifact Principles tone now sourced from the venue pack's tone-by-audience, not a separate `audience profile` (post the _audience -> venue merge).

## [1.0.0] — 2026-06-23

- initial version modeled on paper-venue.

## [2.0.0] — 2026-07-06

- moved AFTER claims (was after pitch); pin writes venue + stages_skipped + claims_settlement; retarget rule inverted (claims survives, settlement may deepen); minimap column retired (paper-alignment refactor, SOP archived in haipipe-application/CHANGELOG.md §5.0.0).

## [3.0.0] — 2026-07-06

- Port of paper venue 2.0.0 (765696f): venue becomes an artifact-producing stage — writes 0-lifecycle/2-venue/2-venue.md + _LOG + _PROBE/ with Artifact Principles (the downstream contract pitch/display/section-edit/artifact read); still writes the 3 STATUS rows; dual-2 numbering mirrors paper (2-venue + 2-pitch).
