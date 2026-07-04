haipipe-paper-probe — Changelog
===============================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## [1.8.0] — 2026-07-04

Changed
- From-buffer reads the index then per-stage `_PROBE/` files; default dispatch = Agent(haipipe-probe-orchestrator-agent) (clean context), inline Skill only for tiny single lookups.
- TRANSLATE step made explicit (probe is paper-unaware; this worker is the bilingual layer): light-probe takeaways backfill the PP plan file (`status: read`, `_DISCOVERY_` retired); sources in the Read output are HARVESTed by haipipe-paper-probe-citation into `_CITATION_{stage}.md`. Seed dispatch row gains `○ harvest` for citation.

## [1.7.2] — 2026-07-03

Changed
- Evidence-routes rule extended: stage skills never dispatch discovery/task orchestrator agents or /haipipe-probe directly; this worker is the only door (bypassing it leaves no project-side probe). Seed row de-"optional"-ed: DEFAULT RUN for a new seed, skip only by explicit logged verdict.

## [1.7.1] — 2026-07-03

Fixed
- Strip-form example corrected to `probe: cite 🔥🚀` (was a marker-less `cite ⬜` while probe is the active phase; violates the exactly-one-🔥-one-🚀 rule).

## [1.7.0] — 2026-07-03

- From-buffer entry added (JL: 不要让 haipipe-paper 直接 call /haipipe-probe，由本 worker 在 stage 的 phase 里 call): Skill(haipipe-paper-probe, args="from-buffer <paper_root> [PPNN]") reads planned items in 1-probe-plans/, applies reuse-before-create, dispatches to /haipipe-probe, writes back status/probe_ref, returns a dispatch summary. The umbrella's probe run verb now routes here; this worker is the single dispatch point.

## [1.6.0] — 2026-07-03

- phase spine renamed DGPC -> DPRC (GATHER->PROBE, POLISH->REVISE). This phase is now named after what it does: dispatch evidence needs through /haipipe-probe. The old name GATHER collided with probe's own internal Gather stage; the rename removes that collision.

## [1.5.0] — 2026-07-03

- probe dispatch rules. (1) mode: light DEFAULT (stops at Read, returns to caller), full only for committed verdicts (claims); escalation supported. (2) reuse-before-create: sweep 1-probe-plans/ + project probes + insight KB, ENRICH an existing probe over creating a near-duplicate. Also: _DISPLAY_{stage}.md declared the display worker's needs registry (need → unit → status), parallel to _CITATION_/_VALUES_; added /haipipe-insight to the downstream lifecycle map (probe deposits at Deposit).

## [1.4.0] — 2026-07-03

- reframed GATHER around two route families. Evidence routes through /haipipe-probe (the universal gateway; probe calls discovery/task during its own Gather). Seed = light probe → discovery (landscape/related-work/novelty, _DISCOVERY_0-seed.md takeaways). Claims = HEAVY probe + task (probe plans per GAP claim, tasks for runs/data, verdicts backfill _EVIDENCE_).

## [1.3.0] — 2026-07-03

- added the seed discovery route (superseded by 1.4.0's probe-gateway framing).

## [1.2.0] — 2026-07-03

- reframed as internal worker. Users invoke stage skills (seed, claims, pitch...), not this skill directly. Stage skills call this during their GATHER phase.

## [1.1.0] — 2026-07-03

- made stage-aware. GATHER now works for all stages, not just section-edit. Added per-stage dispatch table.

## [1.0.0] — 2026-07-03

- new hub skill for the GATHER phase.
