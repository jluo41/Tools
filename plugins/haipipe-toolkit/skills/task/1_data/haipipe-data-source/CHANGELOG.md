haipipe-data-source — Changelog
===============================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## [1.2.0] — 2026-07-08

- skill-diagnose fixes: opening line no longer claims HumanFn ownership (Stage 2 owns it; matches Stage Scope + 1.1.0 correction); Recipe/config locations -> task-folder configs/ + haistepconfig reference-only note; dead `test/test_haistep` block removed from templates/config.yaml (replaced by `python -m scripts.haistepcli.source`).
- (2026-07-08 earlier, unversioned at the time — recorded here) builder home repointed from code-dev/ to per-project `01_source_fn_develop_<cohort>/`; "Large Tables That Don't Fit in RAM" section added (CHUNKED_TABLES pattern).

## [1.1.0] — 2026-07-04

- ownership corrected: Stage 1 owns SourceFn only (HumanFn builders live in Stage 2's 2-Record-WorkSpace); rename-damaged sentence restored; dead template path -> own templates/config.yaml.

## [1.0.0] — 2026-05-31

- baseline metadata added.
