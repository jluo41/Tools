haipipe-application-display — Changelog
=======================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## [4.7.0] — 2026-07-19

- Probe-pool anatomy line restated as the current entry contract. Vocabulary: `a-consumer:` as a PROBE-FILE FIELD is gone — the probe entry's answer subsection is
  `### a-executor` (the copy of the answering QA file's answer, the consumer-side single source of truth).
  The a-consumer CONCEPT is untouched: it remains the per-consumer interpretation written in the STAGE DOC
  (station 2, anchored `[source: PP<NN>]`).

## [4.6.0] — 2026-07-18

- Template alignment sweep: dropped the template's "How to use:" header line; Q-consumer questions renamed `## Q<n>` -> `## Q-Disp-<n>` (id carries the origin stage; the materialize-U<nn> title kept) + reshaped to the fixed 3-field form Ask / Why / Answer (`__TO_BE_FILLED__` == OPEN, else ANSWERED — the doc's only state). SKILL skeleton + formatting synced.
- Fixed a stray `</content></invoke>` artifact left at the end of SKILL.md.

## [4.5.0] — 2026-07-17

- Q-consumer migration: template + SKILL `Probes` -> `Q-consumer` (`## Q` per unit to materialize).

## [4.4.0] — 2026-07-17

- Template D3+D4: probe roster placeholder `<status>` -> `<state>`; U02 data-source Status enum now matches U01 (`planned | commissioned (PP<nn>) | landed`).

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
