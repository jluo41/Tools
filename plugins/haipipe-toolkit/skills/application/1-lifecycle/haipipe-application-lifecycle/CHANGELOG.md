haipipe-application-lifecycle — Changelog
=========================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Oldest first (append at the bottom).


## [1.0.0] — 2026-06-22

- initial version modeled on paper-lifecycle.

## [2.0.0] — 2026-06-23

- renamed stages to paper vocabulary; venue-aware stage skipping.

## [3.0.0] — 2026-07-06

- paper-aligned spine seed->claims->[venue]->pitch->narrative->display->section-edit; venue-gated dispatch via STATUS.md stages_skipped; loopback fix: venue change re-runs venue+pitch, claims survives; drives 2-phase workers (paper-alignment refactor, SOP archived in haipipe-application/CHANGELOG.md §5.0.0).

## [4.0.0] — 2026-07-09

- ladder restage (family 6.0.0/6.1.0): stage 1 becomes the venue-FREE evidence ladder 1a-descriptions -> 1b-themes -> 1c-claims -> 1d-advice; composite `ladder` sweep verb with venue-scaled gate batching; loopback table gains the four rung rows; spine seed -> ladder -> [venue] -> pitch -> narrative -> display -> section-edit.

## [4.1.0] — 2026-07-09

- BREADTH ROUND: ladder sweep acknowledges the flywheel — rungs loop internally (multi-round DPRC, loop-until-dry per wiki/08 Rounds) and may back-route mid-phase ([ROUTE -> <rung>]); the sweep re-enters the routed-to rung, then resumes order.

## [4.2.0] — 2026-07-15

- probe redesign port (family alignment with paper): the stage-skill line now describes the flat probe pool `1-probes/PPNN_<topic>.md` instead of per-stage `_PROBE/` folders; phase engine reads DRAFT -> PROBE -> REVISE -> CHECK with PROBE running the five-step loop through `haipipe-application-probe`.
- metadata hygiene: `summary:` deflated from a changelog blob to one line + `History: ./CHANGELOG.md`; dropped the redundant history comment line.

## [4.3.0] — 2026-07-17

- Delivery-tooling path references updated `3-build-deploy/` -> `3-deliver/` (layer renamed to match paper).
