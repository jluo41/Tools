haipipe-task-for-display — Changelog
====================================

Skill-scoped changelog (never loaded at invocation; read on demand).
Versions match SKILL.md frontmatter `version:`.
Newest first.


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
