haipipe-application-section-edit — Changelog
============================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## [5.3.0] — 2026-07-19

- ⑩ probe files hold `## QX<n>` ENTRIES, not "sections" — wording corrected in the frontmatter summary.


## [5.2.0] — 2026-07-19

- Evidence-gap line restated: gaps are raised as ENTRIES in the flat probe pool, in the current
  `## QX<n>` + four-`###` anatomy. Vocabulary: `a-consumer:` as a PROBE-FILE FIELD is gone — the probe entry's answer subsection is
  `### a-executor` (the copy of the answering QA file's answer, the consumer-side single source of truth).
  The a-consumer CONCEPT is untouched: it remains the per-consumer interpretation written in the STAGE DOC
  (station 2, anchored `[source: PP<NN>]`).

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
