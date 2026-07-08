haipipe-paper-display — Changelog
=================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## [2.1.0] -- 2026-07-08

Changed
- Venue consumption rewired to lockfile semantics (SKILL.md principle 9 + Venue Constraints + CHECKLIST.md venue-set item): read the paper's 0-lifecycle/2-venue/2-venue.md (Structural Blueprint display units + Writing Principles display limits) FIRST; pack README -> Display only as fallback when 2-venue.md is absent or as deep dives via its [source] tags; stale provenance -> note "venue contract stale", never silent pack re-reads.

## [1.6.2] — 2026-07-03

Changed
- Added the Phase Transition Contract pointer (wiki/08): announce every phase boundary, no silent phase skips (explicit logged verdict only), CHECK never implicit.

## [1.6.1] — 2026-07-03

- phase spine renamed DGPC -> DPRC (GATHER -> PROBE, POLISH -> REVISE; workers haipipe-paper-probe*, haipipe-paper-revise*).

## [1.6.0] — 2026-07-03

- display becomes stage orchestrator that drives its own phases (DRAFT/GATHER/POLISH/CHECK). Phase skills are internal workers called by this skill, not user-facing. Subcommands (plan/scaffold/framework/materialize/build/audit/insert) reorganized as internal operations within phases. Comment lifecycle wired in (wiki/02). Removed shared-protocols listing. Handoff updated to promote to section-edit.

## [unversioned]

- v1.5.0: added canonical CHECKLIST.md done-gate (absorbs gallery requirements out of the paper's 4-display.tex); elbow/icon vector-render rules

## [unversioned]

- v1.4.1: added mandatory compile-after-edit rule; venue awareness note

## [unversioned]

- v1.4.0: added illuminate protocol + cross-refs to stage-gate, tex-quality
