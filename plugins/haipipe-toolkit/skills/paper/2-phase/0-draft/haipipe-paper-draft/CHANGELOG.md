haipipe-paper-draft — Changelog
===============================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## [3.3.0] — 2026-07-03

- phase spine renamed DGPC -> DPRC (GATHER->PROBE, POLISH->REVISE).

## [3.2.0] — 2026-07-03

- DRAFT-oriented cleanup. Archived leftover venue LaTeX templates (templates/) and the 3 write-* style skills to 2-phase/_archive/ (venue knowledge belongs in _venue/ packs, prose style in POLISH). Step 1 now reads the stage's template from 1-lifecycle/ via an explicit registry table; this skill carries no templates of its own. Added venue guard: venue-ALIGNED stages STOP with status: blocked when no venue is pinned or no pack matches; missing per-section style file proceeds with a flagged warning, never silently invented norms.

## [3.1.0] — 2026-07-03

- reframed as internal worker. Users invoke stage skills (seed, claims, pitch...), not this skill directly. Stage skills call this during their DRAFT phase.

## [3.0.0] — 2026-07-03

- rewritten as generic stage-aware DRAFT hub. Section-specific outline format moved to 1-lifecycle/5-section-edit/ref/outline-format.md. Draft now works for all stages (seed, claims, pitch, narrative, display, section-edit).

## [2.0.0] — 2026-07-02

- complete rewrite for section-edit outline creation.

## [1.1.0] — 2026-06-05

- renamed from paper-write to haipipe-paper-section-edit-write.

## [1.0.0] — 2026-05-31

- baseline metadata added.
