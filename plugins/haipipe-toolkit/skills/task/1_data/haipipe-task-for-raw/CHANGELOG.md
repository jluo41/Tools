haipipe-task-for-raw — Changelog
================================

Skill-scoped changelog (never loaded at invocation; read on demand).
Versions match SKILL.md frontmatter `version:`.
Newest first.

## [0.5.2] — 2026-09-23

- WellDoc Proj01 `b00_rawdata` (14 datasets, Jobs `j51`-`j96`) is now a second reference implementation, migrated 260923.

## [0.5.1] — 2026-09-23

- Pattern 2 names the current J21/J22 `.cmd` extraction shape ahead of the legacy A00 `.ipynb` one.

## [0.5.0] — 2026-09-23

- `b00` tree renumbered to the PD2D shape: dataset Job `j51`-`j99` (same number in `b01` to `b03`), `t01`-`t02` dataset-wide, `t11`+ one per table, `t91`-`t93` routing, timeline, hand-off. Reference is REACH PD2D; WellDoc Proj01 `b01_rawdata` named as the older shape that migrates.


## [0.4.1] — 2026-09-23

- New § Dataset versions: name, freeze, refresh. The version lives on the dataset folder (`_WorkSpace/0-RawDataStore/<cohort>-v<yymmdd>/`), never on the workspace; typed once as `raw_data_name`, the start date; the runner hands `raw_root` to workers and writes `_FROZEN.yaml` after `freeze_after`; a refresh is one line. How to know a refresh is due: rerun the table census (`n_rows` per source table) and `git diff` its `table_catalog.csv`. Every `0-RawDataStore/<cohort>` path in SKILL, scaffold and config seed now reads `<raw_data_name>`.

## [0.4.0] — 2026-09-22

- Corrects 0.3.0: `b00` never extracts. Two kinds of raw Job: the Extraction Job (own extraction Project, versioned `raw_data_name` typed once) and the new Raw understanding Block `b00` (WellDoc shape: intake, catalog, one profile Task per table, routing, timeline, gated source hand-off). Example back to `b01_prediabetes_raw`.

## [0.3.0] — 2026-09-22

- Raw is Block `b00`, in two uses: extract (writes RawStore) or inspect (extraction lives in another Project; reads its receipts, same `jNN`). Replaces the `A00_rawstore_<cohort>` group-letter note; example renamed `b00_prediabetes_raw`.

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
