haipipe-display-figure — Changelog
========================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.

## [0.2.1] — 2026-07-27 — Caller-owned wrapper semantics

- Makes the Paper-owned caption, label, and placement boundary explicit; the plot renderer only emits the asset/recipe and may refresh an already-approved asset reference.

## [0.2.0] — 2026-07-27 — Display Intake

- Requires a verified Intake manifest and approved snapshot before plotting.
- Separates values in `intake/inputs/` from scripts in `recipe/`, and removes ad hoc section include snippets.

## [0.1.2] — 2026-07-24 · moved to display/

Moved to the shared `display/` bucket and renamed `haipipe-paper-display-figure → haipipe-display-figure` — it's a generic data-plot renderer, not paper-specific.

## [0.1.2] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 1.2.0; older entries below keep their original numbers).

## [1.2.0] — 2026-06-22

- joined the display family as haipipe-display-figure; shed table rendering to haipipe-display-table (now plots-only); bumped reviewer model to gpt-5.5.

## [1.1.0] — 2026-06-05

- renamed from paper-figure to haipipe-paper-figure (haipipe-paper-* name unification).

## [1.0.0] — 2026-05-31

- baseline metadata added.
