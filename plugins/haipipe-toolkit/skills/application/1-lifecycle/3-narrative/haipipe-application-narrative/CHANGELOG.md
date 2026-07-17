haipipe-application-narrative — Changelog
=========================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## [5.1.0] — 2026-07-17

- Q-consumer migration: template + SKILL `Probes` -> `Q-consumer` (`## Q` blocks; rare, routed back to claims).

## [1.0.0] — 2026-06-22

- initial version as haipipe-application-design.

## [2.0.0] — 2026-06-23

- renamed from design to narrative; match paper vocabulary; venue-gated.

## [3.0.0] — 2026-06-29

- added _LOG, _DISPLAY_ tracking file (beat → display unit mapping). Output folder 3-narrative/ (was flat file). Borrowed per-stage tracking pattern from paper.

## [4.0.0] — 2026-07-06

- stage-folder paths; gating via STATUS.md stages_skipped; settlement-bar precondition; DPRC phases (paper-alignment refactor, SOP archived in haipipe-application/CHANGELOG.md §5.0.0).

## [4.1.0] — 2026-07-06

- 765696f port: visible Probes section + reads 2-venue.md Artifact Principles + ascii artifact formatting.

## [4.2.0] — 2026-07-09

- ladder restage + review sweep (family 6.0.0-6.1.1): primary input is 1d-advice (A entries) with 1c-claims as backstop; inline schema blocks converted to ascii ====/---- (JL heading ruling); id examples unpadded (C1/A1).

## [5.0.0] — 2026-07-15

- reshaped to the 5-part stage skeleton (what-it-decides / What's special / four phases / artifact+template pointer / Exits); inline per-venue templates moved into ref/narrative-template.md; probe-model repointed to the flat pool 1-probes/PPNN_<topic>.md (section fields serves/target/state/q-executor/a-consumer + ## Why; states planned|commissioned|answered|read|answered-local|failed; no _PROBE/, no 1-probe-plans, no verdict/dispatched, no G1/G2/G3); summary deflated to one line + History pointer.
