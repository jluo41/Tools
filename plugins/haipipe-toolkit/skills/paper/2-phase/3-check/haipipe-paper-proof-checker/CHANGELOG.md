haipipe-paper-proof-checker — Changelog
=======================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## [1.1.2] — 2026-07-07

Fixed (skillset-diagnose D10)
- Caller orientation was stale toward the retired `/paper-writing` orchestrator: the skill only named legacy Phase 6 as its integrator. Now names `haipipe-paper-check` (which dispatches this skill as its PROOF sub-checker) as the primary caller everywhere, with `/paper-writing` kept as a legacy-compat note.

## [1.1.1] — 2026-07-07

- repointed 4 dangling shared-references/tools refs to their real Tools/legacy/ paths; refreshed stale last_updated.

## [1.1.0] — 2026-06-05

- renamed from proof-checker to haipipe-paper-proof-checker; consolidated into 2-section-edit/ (haipipe-paper-* name unification).

## [1.0.0] — 2026-05-31

- baseline metadata added.
