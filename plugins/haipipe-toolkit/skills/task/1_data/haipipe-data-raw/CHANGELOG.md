haipipe-data-raw — Changelog
============================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## [1.2.0] — 2026-07-08

- skill-diagnose fixes: templates/datapoint-timeline.txt Sources footer `0-RawStore` -> `0-RawDataStore` (the 1.1.0 "bucket-wide" rename had missed the template).
- Stage Scope now documents VOLUME-RESIDENT (PHI) cohorts: raw may live only on a Databricks catalog volume; a missing local folder does not mean the cohort doesn't exist (JL: "ok, go ahead and fix all of them" — approved recommended option A).

## [1.1.0] — 2026-07-04

- store name corrected bucket-wide: 0-RawStore -> 0-RawDataStore (the only store on disk); Stage-1 output is a SourceSet (was HumanSet).

## [1.0.0] — 2026-05-31

- baseline metadata added.
