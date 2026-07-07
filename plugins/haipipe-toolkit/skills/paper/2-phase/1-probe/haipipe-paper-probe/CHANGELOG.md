haipipe-paper-probe — Changelog
===============================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## [3.0.0] — 2026-07-06

Changed (rethink after the ProjC seed shortcut: rules existed but were prose-only, buried in 15-line paragraphs — the executor compressed them away and searched inline, writing tables into _PROBE/ cards with nothing landed in discoveries/)
- Rebuilt as a 4-step procedure: BOOKKEEP → DISPATCH → TRANSLATE → VERIFY, each ending in a mandatory PROOF shown in the reply (project_root + ls, the literal Agent call, per-card refs + ls, checker output). A step without its proof did not happen.
- NEW `check-probe-cards.sh`: deterministic verifier (read/verdicted ⇒ refs resolve under project_root; no markdown tables in any card; ≤80 lines; status:failed surfaced). Run at STEP 4 and re-run by the stage CHECK gate — two enforcement points.
- project_root resolution corrected: walk-up to first ancestor with discoveries/ ONLY; `git rev-parse --show-toplevel` dropped (repo-backed papers are their own repos, it returns paper_root).
- Reference prose moved out of the invocation path: `ref/per-stage-dispatch.md` (stage map, seed/claims specifics, section-edit logic, status forms) + `ref/harvest-acceptance.md` (harvest dispatch + literal acceptance greps). Main file 260 → ~150 lines.
- Hard boundary added: NO markdown tables in PP cards / _CITATION_ / probe-discovery documents (JL standing rule).

## [2.6.0] — 2026-07-06

Changed (first pass at the same incident, prose-only — superseded by 3.0.0 same day)
- BOOKKEEP resolves project_root + ensures PP-card anatomy by spec path, not memory; DISPATCH shows the concrete Agent input {project_root, mode, plan}; TRANSLATE makes refs MANDATORY (empty refs = failed phase, not green).

## [2.5.0] — 2026-07-05

Changed (probe folderless refactor — probes/ retired; PPNN card = single source of truth)
- Step 0 RE-INVOKE PER RUN: every stage's PROBE phase invokes this skill fresh (test-123333333 PP02 ran from a 3-hour-old in-context copy missing same-day rules).
- TRANSLATE: `refs:` always point directly at execution artifacts (discoveries/tasks); full-mode verdicts land in the PPNN card's `## Verdict` (gates + verdict + reasoning) and flip the claims ledger in the same pass.
- DISPATCH: shape vocabulary aligned to gateway 2.0.0 (reused | enriched | fresh); no shape creates a probe folder.

## [2.4.1] — 2026-07-05

Changed (test-123333333: harvest synonymized the canonical status string — `retrieved ✅ (discovery, ...)` for `VERIFIED-by-discovery (...)` — and acceptance waved it through on semantic equivalence)
- Provenance acceptance grep made LITERAL: `grep -c 'VERIFIED-by-discovery'` must equal the discovery-verified pick count; same-meaning rewordings are REJECTS. Meaning-judgment is what mechanical acceptance exists to remove; canonical strings are VERBATIM per the citation skill's spec (1.5.2).

## [2.4.0] — 2026-07-05

Changed (cost pass after test-2-2222: $24 / 28min, 54% of spend = context loading)
- Harvest subagent dispatches on the CHEAPEST model tier (Agent model: haiku, effort low) — pure transcription guarded by mechanical acceptance; the one acceptance-reject retry escalates one tier up instead of same-tier.

## [2.3.3] — 2026-07-05

Changed (test-2-2222 harvest: cards had substance but NO authors/year/venue — the worker's own compressed re-enumeration of the citation card spec had dropped the identity bullet, the dispatch prompt followed it, acceptance didn't check identity → passed. JL: "title author 还有 venue 这些都没有呀")
- DISPATCH-to-harvest: never paraphrase the card spec into the prompt; point the subagent at the citation skill's SKILL.md spec section (single source of truth). Spec-drift by telephone game is the named failure mode.
- ACCEPTANCE gains two greps: identity bullet per card (a `^- ` line with `(YYYY)`; title-only card = REJECT) and status-carries-provenance (S## VERIFIED in sources.md → card must say `VERIFIED-by-discovery`; bare "unverified" = REJECT).

## [2.3.2] — 2026-07-05

Changed (test-2-2222: worker went sync on a from-scratch probe; JL's session froze 25 minutes through the 4-layer chain)
- DISPATCH: fresh runs go `run_in_background`, hard. The "I need the return to TRANSLATE" excuse is named and voided (background return arrives, TRANSLATE runs then). Fresh-vs-reuse judged from plan content alone; when unsure, background.

## [2.3.1] — 2026-07-05

Changed (Paper-Probe-Test: an elicited AUDIT scope had no named route, so the stage hand-rolled a general-purpose web auditor)
- DISPATCH: audit-shaped scopes (re-verify / audit / double-check the existing set) are ordinary plans for the SAME `Agent(haipipe-probe-orchestrator-agent)` dispatch — the agent answers them from the ledger (VERIFIED + method + date IS the verification). Never invent a side-channel worker because a scope has no named row.

## [2.3.0] — 2026-07-05

Changed (run-3 audit: acceptance claimed "each has anchor + finding" while `grep -c 'finding:'` returned 0)
- TRANSLATE harvest acceptance is MECHANICAL-FOR-REAL: run the greps, never eyeball. Four checks: card count == pick_list; every new card has `- summary:` + `- finding:`; every `source_ref` S## must EXIST in the named sources.md (unresolvable anchor = REJECT — it means the agent's fresh evidence never landed); no bibtex. One reject → re-dispatch harvest with defect list (one retry), else `status: read (harvest DEFECTIVE)` surfaced in the stage reply.
- Harvest dispatch prompt now PASSES the card-format spec explicitly (### heading + summary/finding/relevance/status/Scholar/source_ref bullets) instead of assuming the subagent infers it.

## [2.2.0] — 2026-07-04

Changed
- TRANSLATE: citation harvest now dispatches the harvest SUBAGENT on a pick_list return, then does mechanical acceptance (produce/review split); the worker no longer transcribes source substance itself.

## [2.1.0] — 2026-07-04

Changed
- TRANSLATE = pure transcription of the agent's anchored return (takeaways with per-line source anchors; structured sources manifest -> _CITATION_); the worker reads NO project files, may only `ls`-verify returned refs (existence, never content). Large harvests (>~20 entries / multi-discovery) run the citation worker as a subagent. DISPATCH: likely-reuse plans go synchronous, likely-fresh-discovery plans go run_in_background.

## [2.0.0] — 2026-07-04

Changed (JL ruling from the seed-test replication: 不管是啥，probe orchestrator agent 来做)
- Worker contract narrowed to BOOKKEEP / DISPATCH / TRANSLATE. Dispatch is ALWAYS `Agent(haipipe-probe-orchestrator-agent)` — the tiny-lookup inline carve-out is removed (it was the license for the observed bypass). The worker never sweeps the project or reads discoveries/probes/insights inline; the reuse decision (enrich / reuse-directly-no-wrapper / create+gather) belongs to the agent's SWEEP in clean context. Plan `ref:` may point at a probe or a directly-reused artifact (lean option B).

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
