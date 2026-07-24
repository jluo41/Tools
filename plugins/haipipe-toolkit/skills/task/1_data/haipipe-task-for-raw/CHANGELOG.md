haipipe-task-for-raw — Changelog
================================

Skill-scoped changelog (never loaded at invocation; read on demand).
Versions match SKILL.md frontmatter `version:`.
Newest first.


## [0.1.4] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 1.4.0; older entries below keep their original numbers).

## [1.4.0] — 2026-07-08

- Pattern 2 PROPAGATED into the operative files (v1.3.0 had added it to SKILL.md only): fn/scaffold.md gains Step 0 pattern gate + ⚡P2 deltas per step (A00 group shape, all-Spark, volume output aligned to the SourceFn cohort-slug, group-root README carve-out); ref/config-seed.yaml gains Pattern-2 execution/volume_path guidance and marks the local: block Pattern-1-only; ref/run-databricks-sh-template.sh sync hint marked "Pattern 1 only"; SKILL intro paragraph de-Pattern-1-ified (JL: "ok, go ahead and fix all of them" — approved recommended option A).

## [1.3.0] — 2026-07-08

- Added Pattern 2: server-resident rawstore (PHI cohorts) — all-Spark multi-stage group that stays on the catalog volume (A00_rawstore_* shape from Project-REACH-ADHD: group-root orchestrator, _databricks/ .ipynb bundle, group README allowed). Output path must align to the Stage-1 SourceFn's `0-RawDataStore/<cohort-slug>/`. Existing doctrine renamed Pattern 1 (extract-wide-process-local, non-PHI). Cross-links haipipe-task/ref/databricks-execution.md; MUST NOT list gains the PHI no-local-sync rule.

## [1.2.0] — 2026-07-04

- WIRED into the orchestrator (JL decision: raw extraction is how data leaves the database): type-table row raw → /haipipe-task-for-raw ↔ /haipipe-data-raw, known-type list, keyword row (raw/ingest/extract/databricks moved out of the data row), script-inference pattern (databricks/spark.sql/dbutils), dispatch table. Position-in-the-series list updated (for-training → for-fit; for-inference → for-endpoint).

## [1.1.0] — 2026-07-04

- group letter R now a project-specific default (orchestrator rule: the project's scheme wins).

## [1.0.0] — 2026-06-10

- initial version — extract-wide-process-local doctrine.
