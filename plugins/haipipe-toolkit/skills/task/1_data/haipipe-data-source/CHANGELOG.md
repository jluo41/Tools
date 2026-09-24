haipipe-data-source — Changelog
===============================

Skill-scoped changelog (never loaded at invocation; read on demand).
Versions match SKILL.md frontmatter `version:`.
Newest first.

## [0.3.2] — 2026-09-24

- Generated SourceFns may live in `code/haifn/fn_source/<fn_version>/` (Run config `fn_version:`); the version names the `ProcName_to_ProcDf` shape. `templates/config.yaml` shows the optional `fn_version:`.

## [0.3.1] — 2026-09-23

- External-data contract points to `haipipe-data-external/ref/asset-model.md`: explicit per-asset `lookup` with `obs_dt`, lock-pinned versions, shared `enrich_<table>()` with Input2SrcFn, `external-dependency.json`, frozen versions only in training; v4 attach helpers kept until `external_base` exists.

## [0.3.0] — 2026-09-23

- Contract-generated SourceFn with committed-file check; `load_tables=[]` for huge stores; schema-superset question recorded as open (JL 260923).

## [0.2.1] — 2026-09-23

- Builder location line names the exact Block, Job and Task (rule: `haipipe-task/ref/hierarchy.md`).


## [0.1.2] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 1.2.0; older entries below keep their original numbers).

## [1.2.0] — 2026-07-08

- skill-diagnose fixes: opening line no longer claims HumanFn ownership (Stage 2 owns it; matches Stage Scope + 1.1.0 correction); Recipe/config locations -> job configs/ + haistepconfig reference-only note; dead `test/test_haistep` block removed from templates/config.yaml (replaced by `python -m scripts.haistepcli.source`).
- (2026-07-08 earlier, unversioned at the time — recorded here) builder home repointed from code-dev/ to per-project `01_source_fn_develop_<cohort>/`; "Large Tables That Don't Fit in RAM" section added (CHUNKED_TABLES pattern).

## [1.1.0] — 2026-07-04

- ownership corrected: Stage 1 owns SourceFn only (HumanFn builders live in Stage 2's 2-Record-WorkSpace); rename-damaged sentence restored; dead template path -> own templates/config.yaml.

## [1.0.0] — 2026-05-31

- baseline metadata added.
