haipipe-nn-tuner — Changelog
============================

Skill-scoped changelog (never loaded at invocation; read on demand).
Versions match SKILL.md frontmatter `version:`.
Newest first.


## [1.1.0] — 2026-07-04

- repoint dangling layer-3 ref; L2->L3 hand-off contract corrected: ModelInstance drives the Tuner via the registry (fit/save_model), no best_config+checkpoint artifact hand-off (C4).

## [1.0.0] — 2026-05-31

- baseline metadata added.
