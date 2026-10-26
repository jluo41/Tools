haipipe-task-for-fit — Changelog
================================

Skill-scoped changelog (never loaded at invocation; read on demand).
Versions match SKILL.md frontmatter `version:`.
Newest first.

## [0.3.0] — 2026-10-25

Merged 2 helper skill(s) into `_parts/`: `haipipe-task-gpu` -> `_parts/gpu`, `haipipe-task-gpu-training` -> `_parts/gpu-training`. /haipipe-task-for-fit reads `_parts/<name>/PART.md` instead of calling a separate skill; allowed-tools gained the parts' tools. Old commands map as `/haipipe-task-gpu` -> `haipipe-task-for-fit/_parts/gpu`. (merge-parts 261025)

## [0.2.0] · 2026-10-21 · One folder per Run, and the Type contract

- `## Type contract` is the first section of SKILL.md (haipipe-task ref/types.md): roles [trial, make, fix],
  heavy output in `_WorkSpace/5-ModelInstanceStore/`, companions, plan sample.
- Every page states the current Run layout: the ticket `runs/rNN_<run>/rNN_<run>.sh`, its `config.yaml`
  (`scripts/config/rNN_<run>.yaml` in a Block not yet moved) and `run.yaml` card, and the Result
  `$OUTPUT_ROOT/<task>/runs/<run>/result/`, never `results/<run>/` (SKILL.md, fn/scaffold.md,
  ref/config-seed.yaml, ref/workflow-plan-sample.yaml with `target: work/...`).
- The ticket sets `REQUIRED_RESULTS=("metrics.json" "model_path.txt")`; the frontmatter names
  `jNN_<job>/tNN_<task>/` Task folders, not `{NN}_<name>/` jobs.
- The fit-owned companions follow the same layout: haipipe-task-for-fit/_parts/gpu 0.3.0, haipipe-task-for-fit/_parts/gpu-training 0.3.0
  (they keep no CHANGELOG of their own).

## [0.1.5] · 2026-10-09 · Theme folders are singular

- Docs name the singular Theme folders (s01-D29, JL 261007): `work/`, `discovery/`, `paper/`, `insight/`,
  `design/`, `labeling/`, `ideation/`; the older plural names still read.

## [0.1.3] — 2026-09-20

- Clarify that Build is an internal step of the owning Task authoring Run.


## [0.1.2] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 1.2.0; older entries below keep their original numbers).

## [1.2.0] — 2026-07-04

- review sweep: plan-sample schema header + reviewer name + relative hub paths + letter A as default + CHANGELOG order; SKILL: algo cross-ref path fixed (../../2_nn/), metadata summary 'model-fitting' (was pre-rename 'model-run'), Lessons section deduped to a LESSON.md pointer (E4).

## [1.1.0] — 2026-06-09

- unwrap prose; fix agent names; add 4-stage lifecycle paragraph.


## [1.0.0] — 2026-05-31

- baseline metadata added.
