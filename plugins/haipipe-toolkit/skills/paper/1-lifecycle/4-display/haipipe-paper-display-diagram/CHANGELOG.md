haipipe-paper-display-diagram — Changelog
=========================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## [1.3.0] — 2026-06-22

- joined the display family as haipipe-paper-display-diagram (was haipipe-paper-figure-spec); the deterministic-vector renderer for architecture/pipeline figures.

## [1.2.0] — 2026-06-22

- completed the migration -- vendored the canonical scripts/figure_renderer.py (the 1.1.0 rename dropped it) and repointed invocations from the ARIS-root tools/ path to the skill-local $CLAUDE_SKILL_DIR/scripts/. Now self-contained (pure stdlib, no MCP, no API key).

## [1.1.0] — 2026-06-05

- renamed from figure-spec to haipipe-paper-figure-spec (haipipe-paper-* name unification).

## [1.0.0] — 2026-05-31

- baseline metadata added.
