haipipe-task-for-endpoint — Changelog
=====================================

Skill-scoped changelog (never loaded at invocation; read on demand).
Versions match SKILL.md frontmatter `version:`.
Newest first.

## [0.4.0] · 2026-10-21 · One folder per Run, and the Type contract

- `## Type contract` is the first section of SKILL.md (haipipe-task ref/types.md): roles [make], heavy output
  in `_WorkSpace/6-EndpointStore/`, companions, plan sample.
- Every page states the current Run layout: the ticket `runs/r01_base/r01_base.sh`, its `config.yaml`
  (`scripts/config/r01_base.yaml` in a Block not yet moved) and `run.yaml` card, and the Result
  `$OUTPUT_ROOT/<task>/runs/<run>/result/`, never `results/<run>/` (SKILL.md, fn/scaffold.md,
  ref/config-seed.yaml, ref/workflow-plan-sample.yaml with `target: work/...`); the Execution example's
  config path is the `work/` form, not `examples/.../scripts/config/`.
- fn/scaffold.md sets `TASK_NAME="<task_name>"`, the worker `scripts/<task_name>.py`, as the shared
  template requires; it said `TASK_NAME="t01_<task_name>"`, the Task folder, so the ticket looked for
  `scripts/t01_<task_name>.py` and stopped.
- Body names the fit and data Task types, not B-series and A-series.

## [0.3.2] · 2026-10-09 · Theme folders are singular

- Docs name the singular Theme folders (s01-D29, JL 261007): `work/`, `discovery/`, `paper/`, `insight/`,
  `design/`, `labeling/`, `ideation/`; the older plural names still read.

## [0.3.1] - 2026-09-28 - No content hashes (JL 260928)

- AGENTS.md rule 9: `external_contract` has no `checksum` field (`SKILL.md`, `fn/scaffold.md`, `ref/config-seed.yaml`).

## [0.2.5] — 2026-09-04

- Scaffold new Task Pages with `folder-kind: task` under canonical
  `haipipe-task` ownership.
- Stop creating the retired PageX relationship lane; X2 input remains a
  proposed packet under `workflow/inbox/application/`.

## [0.2.4] — 2026-08-31

- Move new endpoint scaffolds to the canonical nested Task Folder: Task Page,
  `scripts/config/`, `runs/`, `workflow/`, and reciprocal PageX surface.
- Accept X2 candidates only as immutable proposed inbox material; endpoint
  Plan/Build/Execute/Report remains Task-owned. Legacy flat jobs stay readable.
- Remove the unsupported `argument-hint` frontmatter key so the package passes
  current skill metadata validation.


## [0.2.3] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 2.3.0; older entries below keep their original numbers).

## [2.3.0] — 2026-07-08

- skill-diagnose fixes: config-seed build pointer -> endpoint fn_develop task folder (was unqualified retired code-dev path); ref/inference-perf-notes.md retitled as the knowledge base behind /haipipe-end profile (kept — endpointset fn-3-profile reads it; task-side profiling scope was retired in 2.2.0).

## [2.2.0] — 2026-07-04

- CONFIRMED by JL 2026-07-05 ("ok 我同意。"); review thread removed from fn/scaffold.md.
- fn/scaffold.md + ref/workflow-plan-sample.yaml REWRITTEN from the retired inference-profiling scope (P-groups, ProfileArgs, latency.json, skill: haipipe-task-for-inference) to the 2.x endpoint-packaging scope (c_endpoint_nb.py, Endpoint_Pipeline, Setup->Package->Verify->Report); profiling pointer now /haipipe-end profile; metadata summary + body letter-neutral; store layout points at the canonical 0-overview; CHANGELOG reordered newest-first.

## [2.1.0] — 2026-07-04

- review sweep: plan-sample schema header task/haipipe-workflow; reviewer name haipipe-task-reviewer-agent; fn relative hub path ../../../haipipe-task.

## [2.0.0] — 2026-06-12

- rewritten from inference-profiling to endpoint-building scope. Renamed from haipipe-task-for-inference.
## [1.1.0] — 2026-06-09

- unwrap prose; fix agent names; add 4-stage lifecycle paragraph.

## [1.0.0] — 2026-06-01

- created as haipipe-task-for-inference (latency profiling).
