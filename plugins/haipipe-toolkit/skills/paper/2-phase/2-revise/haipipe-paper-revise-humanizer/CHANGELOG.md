haipipe-paper-revise-humanizer — Changelog
==========================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## [2.1.1] — 2026-07-07

Fixed (skill-family quality sweep)
- Broken reference path: the "Path:" line resolved to `skills/references/academic-humanizer/` (4 levels up lands in `skills/`, wrong). Corrected to the canonical repo-root `Tools/references/academic-humanizer/SKILL.md` (7 levels up as a relative path). Added an honest NOTE that the reference catalog dir is currently empty in this checkout, so the inline Six-layer audit is self-sufficient; re-vendoring the catalog is a separate task.

## [2.1.0] — 2026-07-03

- phase spine renamed DGPC -> DPRC (GATHER->PROBE, POLISH->REVISE).

## [2.0.0] — 2026-07-03

- removed comment-first protocol. POLISH is now fully automatic (apply directly, leave explanatory comments for CHECK). Aligned with DGPC architecture where only CHECK is human-involved.

## [1.0.0] — 2026-06-29

- created from academic-humanizer repo. Integrated into POLISH phase with comment-first workflow.
