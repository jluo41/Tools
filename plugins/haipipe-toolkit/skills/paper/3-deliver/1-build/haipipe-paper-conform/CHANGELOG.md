haipipe-paper-build-check — Changelog
=====================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## [0.2.0] — 2026-07-26 — audits the ruled layout, and runs the delete test as an actual test

Rewritten against the paper-folder layout ruled on the design board (`skills/diagrams/01-haipipe-paper-260725`, face QA6). The old contract audited the npjDM2025 shape: `0-*.tex` masters, `1-compile.sh`, `0-sections/`, `0-displays/`. Under the new rule every one of those is a FINDING, so a correct folder used to fail this audit.

`scripts/check_structure.sh` rewritten, 141 to ~250 lines, blocks A-K:

- **B** three numbered entries are legal and only three (`0-lifecycle` `1-probes` `2-src`); any other `[0-9]-*` is a finding. Missing `1-probes/`/`2-src/` is a warning, because both are absent-until-needed.
- **C** `displays/` is the only home of an asset. `figures/`, `Figures/`, `0-displays/`, and flat `Figure/`/`Table/` buckets are findings.
- **D** NEW: `0-lifecycle/` purity plus one-family-one-folder. A family folder holds `S-*.md` and its own `_archive/`, nothing else, and `S-<Family>-…` must sit in the folder named for `<Family>`.
- **F** the build script is `2-src/compile.sh`; a surviving `1-compile.sh` is a finding.
- **G** generated prose is unnumbered, in `sections/` and `appendices/`.
- **J** NEW, and the headline: **the delete test**. Every `\input`, `\includegraphics` and `\bibliography` target the masters reach is resolved and asserted not to sit behind a `0-`/`1-`/`2-` prefix, as are the masters, `.bib`, `.cls` and `.bst` themselves. `rm -rf 0-* 1-* 2-*` stops being a convention and becomes a check.
- **K** a surviving `STATUS.md` is a warning: the frontier is derived from disk, so a stored one can only go stale.

Verified on `Paper-Personality2Opioid-MISQ2026`: exit 1, 56 findings, 18 of them delete-test failures including the driver `.tex` and the `.bib`. That paper's `0-lifecycle/` passes block D except for known build products; everything above it is still the old shape.


## [0.1.1] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 1.1.1; older entries below keep their original numbers).

## 1.1.1 — 2026-07-19 — the pre-submission citation walk is now `haipipe-paper-check-evidence`

Reference update only; no behavior change here. The `REVIEW` verb of the retired `haipipe-paper-probe-citation` — the slow, human-paced pre-submission walk over every citation — moved to `haipipe-paper-check-evidence` in `2-phase/3-check/`, dispatched conditionally by the CHECK gate the way the proof-checker is. This file's pointers now name it. Background: `../../../_console/260719-02-PHASE-BOUNDARY-REFACTOR.md`, ruling D11 (JL confirmed the NARROW reading: verification belongs to the CHECK PHASE, not to a probe lane, and not — the alternative reading — pushed across the wall to the executor).


## [1.1.0] — 2026-06-05

- renamed from paper-structure-check to haipipe-paper-build-check (haipipe-paper-* name unification).

## [1.0.0] — 2026-06-04

- initial version; script verified green on Paper-MapPhyTrait-npjDM2025.
