haipipe-task-for-display — Changelog
====================================

Skill-scoped changelog (never loaded at invocation; read on demand).
Versions match SKILL.md frontmatter `version:`.
Newest first.

## [0.3.3] — 2026-09-04

- Bind every source Run Result path/hash into the Ticket's `RUN_INPUTS` so the
  runtime receipt preserves the display aggregate's frozen provenance.

## [0.3.2] — 2026-09-04

- Preserve the Page family's single numeric door: a display-input aggregate
  feeds `haipipe-task-for-page` before becoming a Page Supporting Run; only a
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
