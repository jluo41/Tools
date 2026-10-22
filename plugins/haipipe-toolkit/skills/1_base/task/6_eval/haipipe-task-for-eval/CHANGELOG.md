haipipe-task-for-eval — Changelog
=================================

Skill-scoped changelog (never loaded at invocation; read on demand).
Versions match SKILL.md frontmatter `version:`.
Newest first.

## [0.2.0] · 2026-10-21 · One folder per Run, and the Type contract

- `## Type contract` is the first section of SKILL.md (haipipe-task ref/types.md): roles [make, check],
  heavy none, companions, plan sample.
- Every page states the current Run layout: the ticket `runs/rNN_<run>/rNN_<run>.sh`, its `config.yaml`
  (`scripts/config/rNN_<run>.yaml` in a Block not yet moved) and `run.yaml` card, and the Result
  `$OUTPUT_ROOT/<task>/runs/<run>/result/`, never `results/<run>/` (SKILL.md, fn/scaffold.md,
  ref/config-seed.yaml, ref/workflow-plan-sample.yaml with `target: work/...`).
- The frontmatter names `jNN_<job>/tNN_<task>/` Task folders in the eval Block, not `{NN}_<name>/` jobs of a
  B-series; the config seed's example names a Run address, not `A01.02`.


## [0.1.3] · 2026-10-09 · Theme folders are singular

- Docs name the singular Theme folders (s01-D29, JL 261007): `work/`, `discovery/`, `paper/`, `insight/`,
  `design/`, `labeling/`, `ideation/`; the older plural names still read.

## [0.1.2] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 1.2.0; older entries below keep their original numbers).

## [1.2.0] — 2026-07-04

- review sweep: plan-sample schema header task/haipipe-workflow; reviewer name haipipe-task-reviewer-agent; fn/ref relative hub paths ../../../haipipe-task; group letter B now a project-specific default; CHANGELOG flipped to newest-first.

## [1.1.0] — 2026-06-09

- unwrap prose; fix agent names; add 4-stage lifecycle paragraph.
## [1.0.0] — 2026-05-31

- baseline metadata added.

