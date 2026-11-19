## [0.3.1] — 2026-11-16

- `update` gives each paragraph and one-line item of a face's own sections its invisible id (`servers/workbench-work/paragraph_ids.py`), so it can carry marks and cards (JL 261116); a built file is left to its builder.

## [0.3.0] — 2026-11-14

- 🗺️ Work map on every work Block's Overview: a line per Job, a station per Run, a click opens the Run in the pop-out (`work_map.py`); b41 draws its decisions with the same code (JL 261114).
- Work pages carry no state words: a Job, Task or Run row shows its mark (✅ ⏳ ⬜ ❌ 🔶) with the word in its hover (`ui_parts.state_mark`); a Job row has no "done · N Tasks"; the Job's state lead line and the "No Run has returned anything yet" lines are gone; a row that waits on the person keeps its words (JL 261113).
- `propose <Block>`: read loose material, propose the Block's own Overview and Findings sections and its Jobs, the person ticks, then make them (`ref/propose.md`). A face names its own sections under `## Review Content` and `## Findings` (`### title`, `embed: path` for a .md, never an .html, `each: glob`), rendered by `servers/workbench/page/work_sections.py`; first case b41_agreeablerx_replay (JL 261114). `## Plan + Results` adds sections after the Jobs; an `.html` is never framed; a list item with sub-items is a card (chips, tinted blocks) and bold-time items a timeline with phases; an empty Data, Values or Displays section is not drawn.

## [0.2.4] — 2026-11-11

- 🧠 Maps returns to Findings, after Displays and only when the work drew maps (JL 261111).
- A work Block's Findings leads with 🗄️ Data: one row per store from board.md's `data:` block (name, where, holds, access, link), counts read from a Result file and key (JL 261111).
- Findings is exactly 🔢 Values (haipipe-evidence) and 🖼️ Displays (haipipe-display), the paper's Evidence views; no Maps or Studio topic sections (JL 261111).

## [0.2.3] — 2026-11-09

- `update` aligns the renamed views: Status is Plan + Results (one section per Job type: `bands:`, else `use-case:`, else the Tasks' task-type), View BJTR is gone, Findings reads 🗂️ Data, 🖼️ Displays, 🧠 Maps then other kinds, and a work Block has no ❓ question sections or ✍️ Answers to write or agree (JL 261109).

## [0.2.2] — 2026-11-09

- New work is planned as the records the Plan + Results view reads (Job and Task faces, `status: planned` Run cards from `src/gen_runs.py`); the plan is ready when the Plan + Results view shows it (JL 261109).

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
