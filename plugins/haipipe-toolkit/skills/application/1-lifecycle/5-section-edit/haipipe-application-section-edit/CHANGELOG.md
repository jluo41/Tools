haipipe-application-section-edit — Changelog
============================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## [5.1.0] — 2026-07-17

- Citations lens traces to the 1c ledger anchors only (dropped `or K/W insight cards`).

## [1.0.0] — 2026-06-22

- initial version as haipipe-application-delivery.

## [2.0.0] — 2026-06-23

- renamed from delivery to minimap; match paper vocabulary; venue-gated.

## [3.0.0] — 2026-07-02

- replaced minimap with section-editing; per-section comment->reply->apply cycle adapted from paper's write-edit.

## [4.0.0] — 2026-07-06

- paper-alignment: renamed section-edit; venue-profile-driven section list (was hardcoded 01-subgroup-profile..06-gate-check report sections, now in _venue/venue-report); DPRC via shared 2-phase workers; stage folder 0-lifecycle/5-section-edit/; kept the comment->reply->apply convention and the six edit topics as REVISE/CHECK lenses.

## [5.0.0] — 2026-07-15

- Stage-skeleton reshape (paper-alignment, matching the paper section-edit twin + the application claims exemplar): 5-part shape — one-line aim, What's special, The four phases in section-edit, The artifact, Exits.
- Frontmatter: dropped the in-YAML changelog block (moved here); added metadata.summary ending "History: ./CHANGELOG.md".
- Probe model repointed to the flat pool `1-probes/PPNN_<topic>.md` (fields serves/target/state/q-executor/a-consumer + `## Why`; states planned|commissioned|answered|read|answered-local|failed); legacy per-stage `_PROBE/` is migrate-from only. No `## Verdict`, no `dispatched`/`verdicted`, no G1/G2/G3.
