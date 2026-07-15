haipipe-application-display — Changelog
=======================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


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

## [4.2.0] — 2026-07-09

- ladder restage + review sweep (family 6.0.0-6.1.1): display units renamed D<nn> -> U<nn> (1a owns the D namespace); primary input is 1d-advice with 1c backstop; inline schema blocks converted to ascii; id examples unpadded (C1); example task refs renamed T<nn> -> X<nn>_<slug> (T is the theme namespace).
