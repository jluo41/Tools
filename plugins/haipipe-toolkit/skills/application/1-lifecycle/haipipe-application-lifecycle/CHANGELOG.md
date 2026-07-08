haipipe-application-lifecycle — Changelog
=========================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## [1.0.0] — 2026-06-22

- initial version modeled on paper-lifecycle.

## [2.0.0] — 2026-06-23

- renamed stages to paper vocabulary; venue-aware stage skipping.

## [3.0.0] — 2026-07-06

- paper-aligned spine seed->claims->[venue]->pitch->narrative->display->section-edit; venue-gated dispatch via STATUS.md stages_skipped; loopback fix: venue change re-runs venue+pitch, claims survives; drives 2-phase workers (paper-alignment refactor, SOP archived in haipipe-application/CHANGELOG.md §5.0.0).
