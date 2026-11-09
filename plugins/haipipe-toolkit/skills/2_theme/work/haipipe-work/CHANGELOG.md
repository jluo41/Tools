## [0.2.1] — 2026-11-09

- `update` also aligns: Run UI (`ui-run:`, b17 `ui/run-views.md`) on a Blueprint, the title line's use case from records only, stale Task states brought up to their Runs as RESULTS IN, UNREAD (never DONE), a Job's `emoji:`, and Status listing what still waits on the person.

## [0.2.0] — 2026-11-09

- Add the agent-driven `update <Block>` procedure and read-only `--check`, with source-backed alignment, scoped checklists and live verification.
- Distinguish Work Block and Blueprint Block without a new theme or board-kind; only Blueprint gets configured UI views.
- Preserve execution state and owning contracts; separate current focus alignment from the legacy `/wb update` migration.

# Changelog

## [0.1.2] — 2026-10-26

Shorter description (745 -> 407 characters): what it does, when to use it, its trigger words; aliases and old command names kept (diagnostics/descriptions/261026.yaml). (describe 261026)

## [0.1.1] · 2026-10-09 · Theme folders are singular

- Docs name the singular Theme folders (s01-D29, JL 261007): `work/`, `discovery/`, `paper/`, `insight/`,
  `design/`, `labeling/`, `ideation/`; the older plural names still read.

## [0.1.0] — 2026-10-07

- New: the door of the work theme (the task theme until 2026-10-07), in
  `skills/2_theme/work/` beside `workbench-work`. It routes to the skills that own
  each part (haipipe-task, workbench-work, the haipipe-task-for-<kind> skills,
  haipipe-workflow, haipipe-report, haipipe-draft) and owns no contract yet.
