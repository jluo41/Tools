haipipe-paper-seed — Changelog
==============================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## [3.2.0] — 2026-07-04

Changed
- Artifact spec + Location gain `_PROBE/PPNN_<slug>.md` (probe plans + backfilled takeaways; `_DISCOVERY_0-seed.md` retired) and `_CITATION_0-seed.md` (harvested candidates when the probe returns literature). PROBE step routes via Agent(haipipe-probe-orchestrator-agent).

## [3.1.0] — 2026-07-03

Changed (live seed run silently skipped PROBE+REVISE and drifted into CHECK)
- frontmatter summary listed phases as draft -> revise -> check; PROBE restored to the spine.
- PROBE no longer "optional": DEFAULT RUN for a new seed (landscape/related-work/novelty, mode light -- it answers the gate's "who cares?" / "is this new?"); skip only on re-entry/minor edits by explicit logged verdict. Direct dispatch of discovery/task agents or /haipipe-probe from the stage is forbidden.
- REVISE now explicitly weaves probe takeaways into Motivations.
- Phase visibility pointer added (Phase Transition Contract, wiki/08): announce every boundary, no silent skips, CHECK opens with the exit-criteria report + approval ask.

## [3.0.1] — 2026-07-03

- phase spine renamed DGPC -> DPRC (GATHER -> PROBE, POLISH -> REVISE; workers haipipe-paper-probe*, haipipe-paper-revise*).

## [3.0.0] — 2026-07-03

- seed becomes stage orchestrator that drives its own phases. Phase skills (draft/polish/check) are internal workers called by this skill, not user-facing. Simplified to 3 sections (question/motivations/claim-shape). Comment lifecycle wired in (wiki/02). All ref/ moved to wiki/.

## [2.1.0] — 2026-07-03

- simplified seed to 4 sections (question/motivations/claim-shape/promotion-gate); removed current-evidence-status, open-evidence-needs, kill-criteria (belong in claims, not seed); removed 'prospectus' terminology.

## [2.0.0] — 2026-06-29

- switched from .tex to .md + _LOG. Argument documents are markdown; only display compiles to PDF.

## [unversioned]

- v1.1.1: added mandatory compile-after-edit rule; venue awareness note

## [1.1.0] — 2026-06-22

- added illuminate+gate+compile protocol (../../wiki/08-stage-gate.md, ../../wiki/09-stage-illuminate.md, ../../wiki/13-tex-quality.md)

## [1.0.0] — 2026-06-22

- baseline.
