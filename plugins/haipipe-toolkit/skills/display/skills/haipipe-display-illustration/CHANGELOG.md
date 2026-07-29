haipipe-display-illustration — Changelog
==============================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.

## [0.2.1] — 2026-07-27 — Caller-owned wrapper semantics

- Requires an explicit Paper-approved caption and label when finalizing into a display unit.
- Preserves an existing unit wrapper rather than changing its caption, label, or placement.

## [0.2.0] — 2026-07-27 — Display Intake

- Requires Intake context before prompt planning and prohibits unsupported numeric facts in illustrations.
- Uses `recipe/` for prompt and review receipts, supports new `displays/` units, and preserves legacy `source/` units in the helper.

## [0.1.3] — 2026-07-24 · moved to display/

Moved to `display/` and renamed `haipipe-paper-display-illustration → haipipe-display-illustration` — generic Codex-image-2 concept/hero-figure renderer, decoupled from paper.

## [0.1.3] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 1.3.0; older entries below keep their original numbers).

## [1.3.0] — 2026-06-22

- promoted to the DEFAULT illustration renderer and renamed haipipe-display-illustration (the Codex bridge is the maintained path); the Gemini backend moved to haipipe-display-illustration-gemini as the named fallback.

## [1.2.0] — 2026-06-22

- completed the migration -- vendored the canonical helper scripts/paper_illustration_image2.py (the 1.1.0 rename dropped it, leaving the $IMAGE2_HELPER reference dangling) and the codex-image2 MCP bridge (toolkit mcp-servers/codex-image2/). Added the Fit & Readiness section.

## [1.1.0] — 2026-06-05

- renamed from paper-illustration-image2 to haipipe-paper-illustration-image2 (haipipe-paper-* name unification).

## [1.0.0] — 2026-05-31

- baseline metadata added.
