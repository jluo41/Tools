haipipe-display-table — Changelog
=======================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.

## [0.2.1] — 2026-07-27 — Caller-owned wrapper semantics

- Emits only `assets/table-body.tex`; Paper supplies the caption/label/placement wrapper.
- Removes the legacy self-contained `float.tex` and `latex_include.tex` example so the renderer cannot invent paper-facing semantics.

## [0.2.0] — 2026-07-27 — Display Intake

- Requires a verified Intake manifest and summary snapshot before table rendering.
- Separates `intake/inputs/` values from the `recipe/` generation script and uses `displays/` unit paths.

## [0.1.0] — 2026-07-24 · moved to display/

Moved to `display/` and renamed `haipipe-paper-display-table → haipipe-display-table` — generic CSV/JSON → LaTeX table renderer.

## [0.1.0] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 1.0.0; older entries below keep their original numbers).

## [1.0.0] — 2026-06-22

- created as the dedicated table renderer of the display family; takes over table duty from haipipe-display-figure (which is now plots-only).
