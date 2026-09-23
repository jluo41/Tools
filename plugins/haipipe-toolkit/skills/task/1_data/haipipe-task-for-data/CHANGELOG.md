haipipe-task-for-data — Changelog
=================================

Skill-scoped changelog (never loaded at invocation; read on demand).
Versions match SKILL.md frontmatter `version:`.
Newest first.

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
