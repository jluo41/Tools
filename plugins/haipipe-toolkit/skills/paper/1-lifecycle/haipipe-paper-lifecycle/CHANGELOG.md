haipipe-paper-lifecycle — Changelog
===================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## [2.4.0] -- 2026-07-14
## 3.0.0 — 2026-07-14

- PROBE REDESIGN (Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3, approved JL 2026-07-14 — R1-R18). 1-probe-plans/ -> 1-probes/ (PPNN_<topic>.md, one file per TOPIC, one SECTION per question: serves/target/state/commission/reading + ONE `## Why` per file holding the stake). Binding is by PATH: a section's `target:` points at the answering `<leaf>/QA/<n>-<slug>.md` in the bank. DELETED: `## Verdict`, the `verdicted` and `dispatched` states, `_ASK/`/`_ANS/` stubs, `answers:`, and Agent(haipipe-probe-orchestrator-agent) (the GATEWAY — archived + de-registered). A claim's STATUS now lives ONLY in 0-lifecycle/1b-claims/1b-claims.md. Dispatch is now DIRECT: the section's `commission:` block, VERBATIM, to Agent(haipipe-task-orchestrator-agent) / Agent(haipipe-discovery-orchestrator-agent).
- CAMPAIGN DAG DEADLOCK FIXED: step ③ told a dependent card to 'wait for `answers:`' — a field DELETED from both banks, so the wait could never end. A dependent SECTION now waits until its upstream section's `target:` QA FILE EXISTS ON DISK (state: answered). Step ③ also now MATCHes before dispatching.

Added (JL resource ruling 2026-07-14; pairs with haipipe-paper-resource 1.0.0 + haipipe-paper 2.11.0)
- RESOURCE registered as a lifecycle stage everywhere this router enumerates stages: the verbs block (`resource <args>` -> `0-lifecycle/1a-resource/1a-resource.md`), the Specialists list (`haipipe-paper-resource  RESOURCE (1)`), the Natural Pipeline Order, the Routing Logic stage set, the Function Keyword Map + positional aliases, the no-arg dashboard, and the parent-orchestrator diagram.
- Venue boundary prose now reads seed + resource + claims as venue-FREE (what a paper NEEDS to exist does not depend on where you send it); the Retarget rule says the same.
- resource SHARES the number 1 with claims, deliberately -- precedented on disk by 2a-venue/ and 2b-pitch/. No other stage renumbers; `stage-strip.sh` strips the digit and keys on the bare name `resource`.

## [2.3.0] -- 2026-07-11

Added (JL cross-stage ruling 2026-07-11; pairs with haipipe-probe 7.5.0 + haipipe-paper 2.8.0)
- "Global-pass mode (breadth-first — the whole-paper cycle)" section after the Natural Pipeline Order: ① DRAFT SWEEP all stages (placeholders/GAPs fine; venue still pins before the ALIGNED drafts) → ② PROBE-PLAN (`/haipipe-paper probe plan`, campaign consolidation, HUMAN GATE) → ③ HANDOFF BATCH per the DAG → ④ RUN (task/discovery sessions — often a separate concurrent session) → ⑤ HARVEST (query-once) then REVISE/CHECK per stage. Depth-first per-stage cycles remain valid for single-stage work; stage gates unchanged.

## [2.2.0] -- 2026-07-09

Changed (JL ruling 2026-07-09 (LLMTrait-Section session postmortem): normalize the writing process)
- Phase-verb pass-through: trailing `draft|probe|revise|check` after stage args forwards verbatim to the stage skill.
- Two-axis section updated: TWO human gates (DRAFT structure review + CHECK), REVISE proof-carrying, agent never self-advances (was "CHECK is the only human-involved phase").

## [2.1.0] -- 2026-07-08

Changed
- Routing description adopts venue lockfile semantics: venue stage compiles 0-lifecycle/2a-venue/2a-venue.md (the venue contract with pack+outlet+commit provenance); new Venue consumption rule -- aligned stages read 2a-venue.md FIRST (pitch: Venue Profile + Fit Assessment; narrative: Blueprint beats + Writing Principles; display: display units + limits; section-edit: per-section Blueprint block), packs only as fallback when 2a-venue.md is absent or as deep dives via its [source] tags; stale provenance -> "venue contract stale" note, never silent pack re-reads.

## [2.0.3] — 2026-07-03

Fixed
- Closing-line rule updated: stage skills close with the FULL closing block (simplified tail + stage line + phase line) per the umbrella Closing Block section, not just the stage strip line.

## [2.0.2] — 2026-07-03

- haipipe-paper-folder specialist description updated to the minimal quick scaffold (absent-until-written; manuscript machinery on request; repo wiring belongs to /haipipe-paper create); seed description corrected to the 3-section contract; retired prospectus / kill-criteria keywords removed from the maps.

## [2.0.1] — 2026-07-03

- phase spine renamed DGPC -> DPRC (GATHER -> PROBE, POLISH -> REVISE; workers 2-phase/1-probe/haipipe-paper-probe*, 2-phase/2-revise/haipipe-paper-revise*).

## [2.0.0] — 2026-07-03

- lifecycle reordered to the current spine (claims (1) before pitch (2), venue as the decision gate between them); minimap stage removed; section-edit added as stage 5 (per-paper folder renamed 5-editing -> 5-section-edit); two-axis restructure documented (stage skills x DRAFT->GATHER->POLISH->CHECK phases via 2-phase/ workers, CHECK the only human-involved phase); folder dispatch fixed to haipipe-paper-folder; shared conventions repointed to ../../wiki/NN-* (ref/ consolidated into wiki/).

## [1.0.0] — 2026-06-08

- created as orchestrator over all 1-lifecycle specialists.
