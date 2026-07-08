haipipe-task-for-raw — Changelog
================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## [1.3.0] — 2026-07-08

- Added Pattern 2: server-resident rawstore (PHI cohorts) — all-Spark multi-stage group that stays on the catalog volume (A00_rawstore_* shape from Project-REACH-ADHD: group-root orchestrator, _databricks/ .ipynb bundle, group README allowed). Output path must align to the Stage-1 SourceFn's `0-RawDataStore/<cohort-slug>/`. Existing doctrine renamed Pattern 1 (extract-wide-process-local, non-PHI). Cross-links haipipe-task/ref/databricks-execution.md; MUST NOT list gains the PHI no-local-sync rule.

## [1.2.0] — 2026-07-04

- WIRED into the orchestrator (JL decision: raw extraction is how data leaves the database): type-table row raw → /haipipe-task-for-raw ↔ /haipipe-data-raw, known-type list, keyword row (raw/ingest/extract/databricks moved out of the data row), script-inference pattern (databricks/spark.sql/dbutils), dispatch table. Position-in-the-series list updated (for-training → for-fit; for-inference → for-endpoint).

## [1.1.0] — 2026-07-04

- group letter R now a project-specific default (orchestrator rule: the project's scheme wins).

## [1.0.0] — 2026-06-10

- initial version — extract-wide-process-local doctrine.
