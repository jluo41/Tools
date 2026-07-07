haipipe-paper-revise-weaving — Changelog
========================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## [2.2.0] — 2026-07-07

- repointed 5 dead Skill() dispatch targets to real siblings: paper-check-numeric -> haipipe-paper-probe-values (fixes Gate Q Substep Q2 runtime crash), paragraph/sentence -> haipipe-paper-revise-content, write -> haipipe-paper-draft, paper-revise -> haipipe-paper-revise, /paper-structure-planning -> /haipipe-paper-lifecycle.

## [2.1.0] — 2026-07-03

- phase spine renamed DGPC -> DPRC (GATHER->PROBE, POLISH->REVISE).

## [2.0.0] — 2026-07-03

- removed human gates from POLISH. POLISH is now fully automatic (apply directly, leave explanatory comments for CHECK). Human review happens in CHECK only. Aligned with DGPC architecture.

## [1.1.0] — 2026-06-05

- renamed from paper-weaving to haipipe-paper-revise-weaving; consolidated into 2-section-edit/ (haipipe-paper-* name unification).

## [1.0.0] — 2026-05-31

- baseline metadata added.
