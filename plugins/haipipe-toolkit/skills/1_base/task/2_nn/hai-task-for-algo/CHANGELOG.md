haipipe-task-for-algo — Changelog
=================================

Skill-scoped changelog (never loaded at invocation; read on demand).
Versions match SKILL.md frontmatter `version:`.
Newest first.


## [0.2.2] — 2026-10-26

Hidden from the skill listing (`disable-model-invocation: true`); reached through the `/haipipe-task` door, which reads this SKILL.md by path. Nothing moved; `/haipipe-task-for-algo` still works when a person types it. (hide 261026)

## [0.2.1] — 2026-10-25

Links, commands and companions repointed at the helper skills merged into `haipipe-nn`, `haipipe-end`, `haipipe-data`, `haipipe-task-for-fit`, `haipipe-task-for-agent` (now `_parts/<name>/PART.md`). (merge-parts 261025)

## [0.2.0] · 2026-10-21 · Type contract, one folder per Run

- `## Type contract` block added as the first section (haipipe-task `ref/types.md`): algo, role trial,
  no heavy output; plan sample `ref/workflow-plan-sample.yaml`.
- Frontmatter says "scaffolds jNN_<job>/tNN_<task>/ Task folders in an algo-dev Block" (was
  "{NN}_<name>/ jobs ... (default X_algo)"); the argument hint names Block, Job and Task.
- Pages name the current layout: Ticket, `config.yaml` and `run.yaml` card in `runs/<run>/`, Result
  `$OUTPUT_ROOT/<task>/runs/<run>/result/` (was `results/<run>/`); plan sample target is `work/...`.

## [0.1.3] · 2026-10-09 · Theme folders are singular

- Docs name the singular Theme folders (s01-D29, JL 261007): `work/`, `discovery/`, `paper/`, `insight/`,
  `design/`, `labeling/`, `ideation/`; the older plural names still read.

## [0.1.2] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 1.2.0; older entries below keep their original numbers).

## [1.2.0] — 2026-07-04

- review sweep: plan-sample schema header task/haipipe-workflow (was dead project/ path); reviewer name haipipe-task-reviewer-agent (was retired Run Script Reviewer); fn/ref relative hub paths ../../../haipipe-task (were off-by-one); X_algo group now a project-specific default; plan-sample output loss.json (was smoke_test.json); CHANGELOG flipped to newest-first.

## [1.1.0] — 2026-06-09

- unwrap prose; fix agent names; add 4-stage lifecycle paragraph.
## [1.0.0] — 2026-05-31

- baseline metadata added.
