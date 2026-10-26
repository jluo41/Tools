haipipe-task-for-display — Changelog
====================================

Skill-scoped changelog (never loaded at invocation; read on demand).
Versions match SKILL.md frontmatter `version:`.
Newest first.

## [0.4.1] — 2026-10-26

Hidden from the skill listing (`disable-model-invocation: true`); reached through the `/haipipe-task` door, which reads this SKILL.md by path. Nothing moved; `/haipipe-task-for-display` still works when a person types it. (hide 261026)

## [0.4.0] · 2026-10-21 · One folder per Run, and the Type contract

- `## Type contract` is the first section of SKILL.md (haipipe-task ref/types.md): roles [make], heavy none,
  the REQUIRED_RESULTS and `result_gate()` checks, companions, plan sample.
- Every page states the current Run layout: the ticket `runs/<run>/<run>.sh`, its `config.yaml`
  (`scripts/config/<run>.yaml` in a Block not yet moved) and `run.yaml` card, and the Result
  `$OUTPUT_ROOT/t01_display_input_summary/runs/<run>/result/`, never `results/<run>/` (SKILL.md,
  fn/scaffold.md, ref/config-seed.yaml, ref/provenance-template.json with its `work/` holder,
  ref/workflow-plan-sample.yaml with `target: work/...`).

## [0.3.5] · 2026-10-09 · Theme folders are singular

- Docs name the singular Theme folders (s01-D29, JL 261007): `work/`, `discovery/`, `paper/`, `insight/`,
  `design/`, `labeling/`, `ideation/`; the older plural names still read.

## [0.3.4] - 2026-09-28 - No content hashes (JL 260928)

- AGENTS.md rule 9: `provenance.json`, `ref/config-seed.yaml` and `fn/scaffold.md` carry no `sha256`; `RUN_INPUTS` lists plain source paths; the result gate checks `row_count` against `source_data.csv`. This replaces the 0.3.3 path/hash binding.

## [0.3.3] — 2026-09-04

- Bind every source Run Result path/hash into the Ticket's `RUN_INPUTS` so the
  runtime receipt preserves the display aggregate's frozen provenance.

## [0.3.2] — 2026-09-04

- Preserve the Page family's single numeric door: a display-input aggregate
  feeds `haipipe-task-for-evidence` before becoming a Page Supporting Run; only a
  non-Page holder may consume it directly.

## [0.3.1] — 2026-09-04

- Align the config, workflow-plan, and provenance specimens with canonical
  nested Task paths, `$OUTPUT_ROOT`, full Run identities, and
  `status: complete`.

## [0.3.0] — 2026-09-04

- Replace the retired flat/C-series scaffold with the canonical nested
  `bNN/jNN/tNN/rNN` Task dialect.
- Put Task-owned code in `scripts/`, per-Run configuration in
  `scripts/config/`, Tickets in `runs/`, and generated display-input Results
  under resolved `$OUTPUT_ROOT/results/<task>/<run>/`.
- Configure the neutral Ticket fields and require both `source_data.csv` and
  `provenance.json` before the Run may complete.


## [0.2.0] — 2026-07-27

- Reframed this as a display-input task: it now owns a verified, display-ready summary
  `source_data.csv` plus `provenance.json`, not a promoted paper PDF/PNG/TeX asset.
- Added the task-to-Display Intake handoff: the display unit snapshots the small aggregate and
  records task holder, run, canonical artifact, hashes, and permitted use in `intake/manifest.yaml`.
- Added `ref/provenance-template.json` so each task result records source artifacts, selection
  logic, output hash, and the display-safety assertion before a paper may snapshot it.
- Reserved task-generated images for `diagnostics/`; the Display unit owns candidate selection,
  paper rendering, caption, and final asset promotion.

## [0.1.2] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 1.2.0; older entries below keep their original numbers).

## [1.2.0] — 2026-07-04

- review sweep: schema header + reviewer name + relative hub paths + CHANGELOG order; group letter C now a project-specific default (description too — Z01_Display-style project schemes are legal); paper-layer skill mentions removed from SKILL.md + fn/scaffold.md (task names no upper-layer skill, D1).

## [1.1.0] — 2026-06-09

- unwrap prose; fix agent names; add 4-stage lifecycle paragraph.
## [1.0.0] — 2026-05-31

- baseline metadata added.
