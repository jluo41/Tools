haipipe-paper-enter — Changelog
===============================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## [3.2.1] — 2026-07-03

Fixed
- Return Contract still carried the retired 4-field tail (status / paper_root / current_layer / next); the live test session rendered it. Replaced with the umbrella Closing Block shape (status merged with active stage, no paper_root/current_layer) and pointed to haipipe-paper/SKILL.md as the single source of truth.

## [3.2.0] — 2026-07-03

- GET-OR-CREATE absorbed (JL: 直接去掉create，enter的时候没有就call create): a missing path now offers to create the paper -- confirm-gated (repo creation is outward-facing), org resolved per invocation, repo-backed inside Project-* repos per the papers-inside recipe, contents scaffolded via haipipe-paper-lifecycle folder, double-bump, then straight into the console. The umbrella's create verb is retired (haipipe-paper 2.4.0).

## [3.1.1] — 2026-07-03

- phase spine renamed DGPC -> DPRC (GATHER -> PROBE, POLISH -> REVISE); phase strip line now 'draft │ probe: cite val disp │ revise │ check' (stages without sub-tracks show just 'probe').

## [3.1.0] — 2026-07-03

- focus strip dual markers -- 🔥 (active now) + 🚀 (frontier reached); both appear on stage and phase lines, collapse to 🔥🚀 when coincident; convention codified in ../../wiki/01-focus-strip-markers.md; added wiki/ folder parallel to feedback/.

## [3.0.0] — 2026-07-02

- lifecycle reorder (seed -> claims -> venue -> pitch -> narrative -> display -> section-edit); claims is stage 1 (venue-free), pitch is stage 2 (venue-aligned); minimap removed; section-edit replaces write/edit with per-section DGPC status grid (DRAFT/GATHER/POLISH auto, CHECK human); updated file paths, stage strip, diagnosis rules, free-form routing, and dashboard format.

## [2.1.0] — 2026-06-22

- dashboard leads with pitch summary + stage strip before operational details; read order prioritizes 1-pitch.tex; return contract enforces structured tail + failed status; stale-deliverable flag from ../../wiki/13-tex-quality.md.

## [2.0.0] — 2026-06-22

- reframed as the Paper Console; added derive-from-disk frontier, free-form routing, copilot policy, and .paper-console.yaml session state.

## [1.2.0] — 2026-06-21

- open-needs paper session loader.
