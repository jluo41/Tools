haipipe-application-claims — Changelog
======================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## [1.0.0] — 2026-06-22

- initial version modeled on paper-claims.

## [2.0.0] — 2026-06-23

- added claims_depth (light/medium/full) driven by venue profile.

## [3.0.0] — 2026-06-29

- added _LOG, _EVIDENCE_ tracking file, _PROBE/ subfolder for claim-gap probe plans (was flat 1-probe-plans/). Output folder 2-claims/ (was flat file). Borrowed per-stage tracking pattern from paper.

## [4.0.0] — 2026-07-06

- venue-FREE ledger moved BEFORE venue; stage folder + _LOG + _EVIDENCE_ + _PROBE/ cards + index; settlement-depth-at-gate replaces content-depth modes; supported|refuted|inconclusive enum; plan-from-need retired (paper-alignment refactor, SOP archived in haipipe-application/CHANGELOG.md §5.0.0).

## [5.0.0] — 2026-07-06

- Port of paper claims 4.0.0 (765696f): evidence-campaign brain — three sections (Claims short / Probes full / Evidence Campaign with dispatch order + deps); no Hypotheses section (app delta, mechanism lives in seed/pitch); _EVIDENCE_ → _VALUES_; _CITATION_ sectioned venues only; settlement gate reads the campaign table; ascii heading + one-sentence-per-line artifact formatting.

## [5.1.0] — 2026-07-07

- Port of paper claims 4.1.0 (paper-alignment round 2, SOP §4 row 8, R4): FORWARD reader clause — claims DRAFT opens by grepping seed's `_LOG_0-seed.md` for `[FORWARD -> CLAIMS]` pointers; each becomes a PP entry in Probes + an Evidence Campaign row or is explicitly declined in `_LOG`; new done-criterion fails CHECK on any unconsumed pointer. Closes the writer-without-reader gap at the seed→claims handoff.
