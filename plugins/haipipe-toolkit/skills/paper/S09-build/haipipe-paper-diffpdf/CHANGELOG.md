haipipe-paper-edit-diffpdf — Changelog
======================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## [0.2.0] — 2026-07-26 — diff tree paths

Aligned with the paper-folder layout ruled 2026-07-26 on the design board (`skills/diagrams/01-haipipe-paper-260725`, face QA6): `0-sections/` to `sections/`, `0-displays/` to `displays/` (one folder per unit, the only home of an asset, no top-level `figures/`), `1-compile.sh` to `2-src/compile.sh`, and `STATUS.md` retired. Four references in the diff-tree recipe, including the symlink that resolves figures for the old-side build.


## [0.1.1] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 1.1.1; older entries below keep their original numbers).

## 1.1.1 — 2026-07-19 — the pre-submission citation walk is now `haipipe-paper-check-evidence`

Reference update only; no behavior change here. The `REVIEW` verb of the retired `haipipe-paper-probe-citation` — the slow, human-paced pre-submission walk over every citation — moved to `haipipe-paper-check-evidence` in `2-phase/3-check/`, dispatched conditionally by the CHECK gate the way the proof-checker is. This file's pointers now name it. Background: `../../../_console/260719-02-PHASE-BOUNDARY-REFACTOR.md`, ruling D11 (JL confirmed the NARROW reading: verification belongs to the CHECK PHASE, not to a probe lane, and not — the alternative reading — pushed across the wall to the executor).


## [1.1.0] — 2026-06-05

- renamed from paper-diff-pdf to haipipe-paper-edit-diffpdf (haipipe-paper-* name unification).

## [1.0.0] — 2026-05-31

- baseline metadata added.
