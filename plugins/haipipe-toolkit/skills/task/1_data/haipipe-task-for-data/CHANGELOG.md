haipipe-task-for-data — Changelog
=================================

Skill-scoped changelog (never loaded at invocation; read on demand).
Versions match SKILL.md frontmatter `version:`.
Newest first.

## [0.8.1] — 2026-09-23

- WellDoc Proj01 is migrated (260923) and is now the many-dataset reference for the Source Block: five topic Jobs, fixed card numbers `t11`-`t26`, cross-dataset checks in `j49_procdf_coverage`.

## [0.8.0] — 2026-09-23

- Dataset Jobs share a number in `b00` to `b03` only. New Case Block tree (topic Jobs `triggerfn_`/`casefn_`, one `j5N_…_case` per raw dataset) and AIData Block tree: each `j5N_<aidataset>_aidata` is one AIDataSet that merges several raw datasets, with its own number and `record_set_names:` in its defaults (JL 260923).
- Coverage matrix is `b01/j49_procdf_coverage` (2+ datasets only). `t11` table numbers match `b00` only when raw tables map one to one onto ProcNames.
- Reference implementation is now REACH PD2D; WellDoc Proj01 named as the older shape that migrates.

## [0.7.0] — 2026-09-23

- Jobs in two ranges: topic Jobs `j01`-`j49` named by Fn kind first
  (`j01_procdf_cohort`, `j01_recordfn_cohort`); dataset Jobs `j51`-`j99`,
  same number in every Block. `j00` retired.
- b01 contracts split into topic Jobs; the conformance check moves into the
  dataset Job as `t02`. b02 RecordFns follow b01's topic numbers.
- Task folders keep the real CamelCase Fn or ProcName; Runs name only the
  action (`r01_build`, `r01_card`, `r01_table`, `r02_materialize`).
- Shared code and rules of a Block's topic Jobs live in the Block's `src/`.

## [0.6.0] — 2026-09-23

- Record Block pattern: `b02/j00_<project>_recordfn` (HumanFn + RecordFns,
  built once) and one `jNN_<dataset>_record` Job per dataset holding one
  materialize Task whose single Run builds and counts the RecordSet. Event
  RecordFns keep a date window. (JL: a dataset is a Job, and b02 needs no
  per-record Tasks because b01 already unified the ProcNames.)

## [0.5.2] — 2026-09-22

- A PHI SPACE runs EVERY Run as a `.cmd` Databricks ticket (J21 shape): one
  entry per Task over `haiutils.haistep.task_entry`, `main(ctx)` workers, a
  `run_all.cmd` per Job, generated bundle jobs. Build Runs check the committed
  Fn instead of writing it. The synthetic twin moved from a Run to a laptop
  selftest through the real inline runner (JL: "we cannot run with sh").

## [0.5.1] — 2026-09-22

- SourceFn Block pattern: the SourceFn is generated from the `j00` contracts;
  `origin: not_extracted` grades a table `partial`; a RecordFn reads one
  ProcName (the record framework intersects patients across RawNames); a PHI
  dataset gets a synthetic laptop twin with `_SYNTHETIC.yaml`. Learned building
  REACH PD2D `REACHPD2DV260922` and its 15 signal RecordFns.

## [0.5.0] — 2026-09-22

- Dataset Job is `jNN_<cohort>_v<yymmdd>_source`, same `jNN` as its `b00` Job; `j00` order follows `b00` routing; contract columns keep the SourceFn's existing names else CamelCase, and carry every raw column; card Tasks only for stored tables.

## [0.4.0] — 2026-09-22

- SourceFn Job pattern replaced by the SourceFn Block pattern: Source is Block `b01`; `j00_procname_to_procdf_contract` holds one Task per ProcName; one Job per dataset holds `t00_sourcefn_develop_and_use` (build, materialize, inventory Runs) plus one card Task per stored ProcName. A new SourceFn version is a Run, named `<Family>V<yymmdd>`. One ProcName per raw table; Source never merges tables or applies thresholds.

## [0.2.3] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 2.3.0; older entries below keep their original numbers).

## [2.3.0] — 2026-07-08

- skill-diagnose fixes: dead `python -m scripts.haistep.*` invocations -> `scripts.haistepcli.*` (SKILL Path B block, execute-flow summary, fn/execute.md; the old module path raises ModuleNotFoundError — note pyproject's haistep-* console entry points carry the same rot upstream); CHANGELOG reordered newest-first.

## [2.2.0] — 2026-07-04

- ref/config-seed.yaml hub ref was 4-up (dangling) -> 3-up; scaffold Steps 4-5 artifact naming aligned to the Step-3 tree + SKILL.md (configs/run_<task_name>.yaml); notebook-templates group map a1/a2/a3/a4 (was aa/ab/ac/ad).

## [2.1.0] — 2026-07-04

- review sweep: plan-sample schema header task/haipipe-workflow; reviewer name haipipe-task-reviewer-agent; fn/ref relative hub paths ../../../haipipe-task; group letter D now a project-specific default.

## [2.0.0] — 2026-06-11

- add execute path, notebook template pattern, multi-partition support.

## [1.1.0] — 2026-06-09

- unwrap prose; fix agent names; add 4-stage lifecycle paragraph.

## [1.0.0] — 2026-05-31

- baseline metadata added.
