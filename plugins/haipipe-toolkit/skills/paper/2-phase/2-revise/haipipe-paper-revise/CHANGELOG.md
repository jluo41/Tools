haipipe-paper-revise — Changelog
================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## [1.2.0] — 2026-07-03

- phase spine renamed DGPC -> DPRC (GATHER->PROBE, POLISH->REVISE). Phase verb is REVISE: the agent changes prose directly and leaves why-comments; the human gives preferences in CHECK.

## [1.1.0] — 2026-07-03

- reframed as internal worker. Users invoke stage skills (pitch, narrative, section-edit...), not this skill directly. Stage skills call this during their POLISH phase.

## [1.0.0] — 2026-07-03

- new hub skill for the POLISH phase. Dispatches to polish-content, -humanizer, -weaving, -results based on section needs.
