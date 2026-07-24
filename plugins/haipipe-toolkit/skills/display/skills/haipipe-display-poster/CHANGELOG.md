paper-poster — Changelog
========================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## [0.2.0] — 2026-07-24 · became a renderer

Renamed `paper-poster → haipipe-display-poster` and cut loose from papers. It now takes a poster content plan plus a figures folder (`display/ref/content-plan-spec.md`) and renders it — it never opens `main.tex` or `sections/*.tex`, and refuses rather than hunting for a source when the plan is incomplete. The extraction half (deciding what a poster shows of a paper) went back to `paper/5-present/paper-poster`.

## [0.1.0] — 2026-07-24 · moved to display/

Moved from `paper/5-present/` to the shared `display/` bucket (name kept — it still consumes a compiled paper).

## [0.1.0] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 1.0.0; older entries below keep their original numbers).

## [1.0.0] — 2026-05-31

- baseline metadata added.
