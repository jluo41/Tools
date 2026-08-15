haipipe-display-diagram — Changelog
=========================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## [0.2.0] — 2026-07-27 — Display Intake

- Requires Intake context before FigureSpec drafting and forbids inventing real numeric facts.
- Uses `recipe/` for FigureSpec files and `displays/` for paper units.

## [0.1.3] — 2026-07-24 · moved to display/

Moved to `display/` and renamed `haipipe-paper-display-diagram → haipipe-display-diagram` — generic JSON-spec → SVG renderer.

## [0.1.3] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 1.3.0; older entries below keep their original numbers).

## [1.3.0] — 2026-06-22

- joined the display family as haipipe-display-diagram (was haipipe-paper-figure-spec); the deterministic-vector renderer for architecture/pipeline figures.

## [1.2.0] — 2026-06-22

- completed the migration -- vendored the canonical scripts/figure_renderer.py (the 1.1.0 rename dropped it) and repointed invocations from the ARIS-root tools/ path to the skill-local $CLAUDE_SKILL_DIR/scripts/. Now self-contained (pure stdlib, no MCP, no API key).

## [1.1.0] — 2026-06-05

- renamed from figure-spec to haipipe-paper-figure-spec (haipipe-paper-* name unification).

## [1.0.0] — 2026-05-31

- baseline metadata added.
