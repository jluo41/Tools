haipipe-paper-lifecycle — Changelog
===================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## [0.4.0] — 2026-07-26 — the router names paths that exist

Aligned with the paper-folder layout ruled 2026-07-26 on the design board (`skills/diagrams/01-haipipe-paper-260725`, face QA6): `0-sections/` to `sections/`, `0-displays/` to `displays/` (one folder per unit, the only home of an asset, no top-level `figures/`), `1-compile.sh` to `2-src/compile.sh`, and `STATUS.md` retired. 14 path corrections across the verb table, the skill roster, the stage descriptions and the two ASCII maps. The router is where a reader learns what a verb produces, so every wrong path here is a wrong expectation set before the work starts.

Notable: the `haipipe-paper-folder` roster line described the old three-empty-container scaffold including `STATUS.md`; it now describes the Board-first one.


## [0.3.1] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 3.1.1; older entries below keep their original numbers).

## 3.1.0 — 2026-07-19 — the claims router line and ⑤ HARVEST now name the real probe artifacts

Two vocabulary rulings from JL, both dated 2026-07-19, applied across `paper/`.

**Ruling A — the `probe` nickname.** JL: "宪法 don't use this name, just use `probe`." Every "THE CONSTITUTION" / "the constitution" / "the probe constitution" naming `probe/haipipe-probe/SKILL.md` is replaced by `probe` or by the actual path, whichever reads better at the site. A nickname already in the repo is still a nickname.

**Ruling B — the `a-consumer:` probe-file field.** `- a-consumer:` as a FIELD IN A PROBE FILE was replaced by the entry's `### a-executor`; `check-probe-cards.sh` HARD FAILs it under the `stale-old-format` rule. The a-consumer CONCEPT is untouched and still named a-consumer: it is the per-consumer interpretation written in the STAGE DOC (station ②), anchored `[source: PP<NN>]`. Prose that said "the probe section carries its `a-consumer:`" was wrong twice over — probe files hold ENTRIES, not sections, and what an entry carries is `### a-executor`.

Current model, for reference:
```
QA file (bank)  ->  the ENTRY's `### a-executor`  (probe file: the copy, single source of truth)
                ->  each Q-consumer's a-consumer  (STAGE DOC: what it MEANS for this consumer)
                ->  stage content                 (REVISE weaves it in, discharges the bracket)
```

Written under JL's NO TOMBSTONES rule (2026-07-19): "不需要留退役告示,直接抹除任何痕迹" then "follow this rule to do all the following changes." The docs state only the current contract; this CHANGELOG carries the history.

### Changed — the claims router line (ruling B)
"each claim tied to a probe section's answering QA file ... it reads the section's `a-consumer:`, not a probe verdict" -> "each claim tied to a probe entry's answering QA file ... it reads the entry's `### a-executor` and writes its own a-consumer in the stage doc". The trailing "not a probe verdict" was a ban-list naming a dead thing and is gone per the NO TOMBSTONES rule; the checker owns that enforcement.

### Changed — the global-pass ⑤ HARVEST step (ruling B)
The step said a PROBE re-run "re-resolves each `commissioned` section's target:, `ls` its QA file, and lands the `a-consumer:`". It now re-resolves each `commissioned` **entry's** `**target**:` and lands the `### a-executor` **plus** each Q-consumer's a-consumer in its stage doc. Both sinks are now named, which is the contract clarification behind the minor bump: an agent following the old line would have written the answer into the probe file under a field the checker HARD FAILs.
Also in that block: "the q-executor block in the section is the bridge" -> "the `### q-executor` block in the entry is the bridge".

## 3.0.1 — 2026-07-19 — retired sidecars erased from the router and the shared `ref/` docs

This skill owns the shared `1-lifecycle/ref/` reference docs, and both of the load-bearing ones still described the retired sidecar model as the current contract — so an agent consulting the lifecycle map or the stage-gate table would scaffold files nothing reads, and would gate on their existence.

JL ruling on the removal style, 2026-07-19: "不需要留退役告示，直接抹除任何痕迹" / "follow this rule to do all the following changes."

Changed (SKILL.md)
- The section-edit specialist line described the per-section folder as "outline .md, _LOG changelog, _CITATION_ map, _VALUES_ registry" → "outline .md and _LOG changelog".

Changed (`../ref/04-lifecycle-map.md`)
- `1-claims` Writes — `+ _LOG + _EVIDENCE_` → `+ _LOG`.
- `3-narrative` Writes — `+ _LOG + _DISPLAY_` → `+ _LOG`, plus the DR rows it files in `0-lifecycle/4-display/_DISPLAY_REQUEST.md` (the display stage owns that file and its statuses).
- `5-section-edit` Writes — `(outline .md, _LOG, _CITATION_, _VALUES_)` → `(outline .md, _LOG)`.

Changed (`../ref/08-stage-gate.md`)
- The section-edit exit question no longer requires a scaffold containing `_CITATION_ + _VALUES_`; it asks for `outline + _LOG`, and adds the check that actually matters now — every `\cite{TOADD}` / `{VAL:?}` carries its `[Q-<Stage>-<n>]` anchor bracket.

Untouched (deliberately)
- Every `mode: light | full` reference — deferred to a separate review.
- `_DISPLAY_REQUEST.md` — alive.

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

- lifecycle reordered to the current spine (claims (1) before pitch (2), venue as the decision gate between them); minimap stage removed; section-edit added as stage 5 (per-paper folder renamed 5-editing -> 5-section-edit); two-axis restructure documented (stage skills x DRAFT->GATHER->POLISH->CHECK phases via 2-phase/ workers, CHECK the only human-involved phase); folder dispatch fixed to haipipe-paper-folder; shared conventions repointed to the numbered shared-reference docs.

## [1.0.0] — 2026-06-08

- created as orchestrator over all 1-lifecycle specialists.
