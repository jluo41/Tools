haipipe-paper-check — Changelog
===============================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## [1.3.0] — 2026-07-03

- renamed haipipe-paper-checker -> haipipe-paper-check. Phase workers are named by the phase verb (draft/probe/revise/check); agent nouns are reserved for sub-tools (proof-checker stays).

## [1.2.0] — 2026-07-03

- phase spine renamed DGPC -> DPRC (GATHER->PROBE, POLISH->REVISE); sibling worker names updated; seed check row aligned with the 3-section seed.

## [1.1.0] — 2026-07-03

- reframed as internal worker. Users invoke stage skills (seed, claims, pitch...), not this skill directly. Stage skills call this during their CHECK phase.

## [1.0.0] — 2026-07-02

- created as the general auto-gate. The former checker was actually a proof-checker (mathematical proofs only); renamed to haipipe-paper-proof-checker and kept as one sub-checker.
