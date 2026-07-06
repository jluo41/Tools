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

- venue-FREE ledger moved BEFORE venue; stage folder + _LOG + _EVIDENCE_ + _PROBE/ cards + index; settlement-depth-at-gate replaces content-depth modes; supported|refuted|inconclusive enum; plan-from-need retired (paper-alignment refactor, ../SOP-paper-alignment.md).
