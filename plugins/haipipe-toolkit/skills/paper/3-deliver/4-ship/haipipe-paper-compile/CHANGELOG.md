paper-compile — Changelog
=========================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.

## [0.3.0] — 2026-07-26

- Replaced the hard-coded `paper/main.tex` workflow with explicit target
  resolution: named `.tex`, canonical Display gallery, or full-paper build.
- Compiles Display from the paper root into
  `0-lifecycle/3-display/4-display.pdf`; full papers prefer the owned
  `2-src/compile.sh`.
- Separated compiler success from Board approval. The skill reads the owning
  gate and receipt but never advances it or recommends submission from a PDF
  alone.
- Limited venue page checks to full-paper targets and made missing venue limits
  produce `unknown`, not a guessed pass.
- Removed the unsupported `argument-hint` frontmatter key.

## [0.2.0] — 2026-07-26 — assets live in their unit

Aligned with the paper-folder layout ruled 2026-07-26 on the design board (`skills/diagrams/01-haipipe-paper-260725`, face QA6): `0-sections/` to `sections/`, `0-displays/` to `displays/` (one folder per unit, the only home of an asset, no top-level `figures/`), `1-compile.sh` to `2-src/compile.sh`, and `STATUS.md` retired. The preflight `ls` and the worked error example both assumed a top-level `figures/`. An asset lives in `displays/<unit>/assets/`, and there is no `figures/`.


## [0.1.0] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 1.0.0; older entries below keep their original numbers).

## [1.0.0] — 2026-05-31

- baseline metadata added.
