haipipe-paper — Changelog
=========================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## [2.0.2] — 2026-07-03

- create verb added to the front door (JL: should be /haipipe-paper create, not a sub-skill invocation): routes to haipipe-paper-lifecycle folder; repo-backed inside Project-* repos per project/haipipe-project/fn/repo-project.md papers-inside recipe; --org resolved per invocation (paper owner may differ from project owner). Retired prospectus verb/aliases removed (seed replaced it); haipipe-paper-bootstrap specialist entry replaced by haipipe-paper-folder; paper-folder contract tree fixed to current spine (1-claims, 2-pitch, 5-section-edit, .md early stages).

## [2.0.1] — 2026-07-03

- phase spine renamed DGPC -> DPRC (GATHER -> PROBE, POLISH -> REVISE; phase workers probe/ and revise/).

## [2.0.0] — 2026-06-22

- cross-cutting protocol wiring. All stage skills now reference ../wiki/08-stage-gate.md (confirm-before-advance), ../wiki/09-stage-illuminate.md (Socratic taste elicitation), ../wiki/13-tex-quality.md (self-contained compilable tex), ../wiki/12-evidence-routing.md (\needprobe macro + probe handoff). Stage strip end-of-reply convention enforced. Enter dashboard restructured (pitch summary first). 22 feedback items addressed.

## [1.5.0] — 2026-06-22

- probe buffer (1-probe-plans/). Claim-related evidence needs accumulate as probe plans during lifecycle work, then batch-dispatch to /haipipe-probe. Probe is the universal evidence gateway for claims; it calls task/discover during Gather. Direct task/discover verbs kept for non-claim utility work. See fn/probe-plans.md.

## [1.4.0] — 2026-06-22

- added probe/discover/task verbs as evidence-worker dispatchers. Paper orchestrator can now route directly to /haipipe-probe, /haipipe-discovery, /haipipe-task with project context resolved from the paper path. Paper stays story layer; evidence workers do the work.

## [1.3.0] — 2026-06-21

- renamed paper working-memory layer from feedback to rounds; added lifecycle, rounds, and skill-structure references.

## [1.2.0] — 2026-06-21

- made paper lifecycle the delivery-side owner of story/claims and routed GAP/NEED items through the shared delivery-need interface.

## [1.1.0] — 2026-06-21

- added enter/status paper-session loader routing.

## [1.0.0] — 2026-05-31

- baseline metadata added.
