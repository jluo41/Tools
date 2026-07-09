---
name: haipipe-application-lifecycle
description: "Orchestrator for the intervention structure lifecycle (1-lifecycle). Routes to stage specialists across the venue-free/venue-aligned boundary: seed and the evidence ladder (1a-descriptions, 1b-themes, 1c-claims, 1d-principles) are venue-FREE (don't change on retarget); venue pins the modality and gates stages 3-5; pitch, narrative, display, and section-edit are venue-ALIGNED (rewrite on retarget). The `ladder` verb runs 1a->1d as one sweep with venue-scaled gate batching. Stage skills internally run DRAFT -> PROBE -> REVISE -> CHECK via 2-phase/ workers. Trigger: lifecycle, advance, next stage, ladder, intervention structure, /haipipe-application-lifecycle."
argument-hint: "[stage-verb|ladder] [intervention-path]"
allowed-tools: Bash, Read, Grep, Glob, Skill
metadata:
  version: "4.0.0"
  last_updated: "2026-07-09"
  summary: "Ladder restage (SOP-ladder-restage.md): stage 1 split into the venue-FREE evidence ladder 1a-descriptions -> 1b-themes -> 1c-claims -> 1d-principles (echoes D->I->K->W); composite `ladder` sweep verb; gate batching per venue depth. Spine: seed (0), ladder (1a-1d) [venue-FREE] -> venue (pin) -> pitch (2), narrative (3), display (4), section-edit (5) [venue-ALIGNED, gated]. Never routes users to phase skills."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-application-lifecycle (orchestrator)
====================================================

User-facing entry for **intervention structural work** -- everything that decides *what the intervention is* before the artifact exists, or when the argument needs rethinking. The orchestrator owns routing only; each stage specialist owns its own workflow, inputs, and outputs.

The lifecycle has a **venue-free / venue-aligned boundary**. Seed and the evidence ladder (1a-1d) are venue-FREE (they don't change when you retarget to a different channel). Venue is the decision gate that pins the modality in STATUS.md -- and, because application venues differ in weight, it also writes which stages the venue skips (`stages_skipped`) and how much of the claims ledger must settle (`claims_settlement`). Pitch, narrative, display, and section-edit are venue-ALIGNED (they rewrite when you retarget).

```
/haipipe-application-lifecycle                       -> dashboard (list specialists + pipeline)
/haipipe-application-lifecycle seed <args>           -> 0-lifecycle/0-seed/0-seed.md (venue-FREE)
/haipipe-application-lifecycle ladder <args>         -> the 1a->1d sweep (each rung's skill in order; ONE batched gate per the venue's depth, wiki/08)
/haipipe-application-lifecycle descriptions <args>   -> 0-lifecycle/1a-descriptions/1a-descriptions.md (venue-FREE anchored data profile)
/haipipe-application-lifecycle themes <args>         -> 0-lifecycle/1b-themes/1b-themes.md (venue-FREE grounded themes)
/haipipe-application-lifecycle claims <args>         -> 0-lifecycle/1c-claims/1c-claims.md (venue-FREE claim ledger + campaign)
/haipipe-application-lifecycle principles <args>     -> 0-lifecycle/1d-principles/1d-principles.md (venue-FREE design directives -- the ladder's deliverable)
/haipipe-application-lifecycle venue <args>          -> 0-lifecycle/2-venue/2-venue.md (choice + Artifact Principles) + STATUS.md venue pin (venue + stages_skipped + claims_settlement) (decision gate)
/haipipe-application-lifecycle pitch <args>          -> 0-lifecycle/2-pitch/2-pitch.md (venue-ALIGNED goal + theory of change)
/haipipe-application-lifecycle narrative <args>      -> 0-lifecycle/3-narrative/3-narrative.md (venue-gated)
/haipipe-application-lifecycle display <args>        -> 0-lifecycle/4-display/4-display.md (venue-gated; owns per-unit jobs)
/haipipe-application-lifecycle section-edit <args>   -> 0-lifecycle/5-section-edit/{section}/ (sectioned venues only)
/haipipe-application-lifecycle "<natural language>"  -> infer stage, dispatch
```

Two-Axis Model (stages x phases)
---------------------------------

Stage skills are the USER-FACING surface. Internally, each stage skill drives the shared phase cycle **DRAFT -> PROBE -> REVISE -> CHECK** by dispatching the internal workers in `2-phase/` (`haipipe-application-draft`, `haipipe-application-probe`, `haipipe-application-revise`, `haipipe-application-check`). CHECK is the only human-involved phase; DRAFT settles content with the user, PROBE and REVISE are agent-only.

**This router routes users to STAGE skills only -- never to phase skills.** If a request sounds like a phase ("gather evidence for claims", "polish the pitch"), route to the owning stage skill and let it dispatch.

Stage artifacts are markdown (`N-<stage>.md` + `_LOG_` + `_PROBE/` in a stage FOLDER). Stage gates: `../../wiki/08-stage-gate.md`.

Natural Pipeline Order
----------------------

```
  VENUE-FREE (don't change on retarget)
  ──────────────────────────────────────
  seed (0)       why this intervention might work (kill criteria, audience hunch)
      ↓
  THE EVIDENCE LADDER (1a-1d, echoes D->I->K->W; `ladder` runs the sweep)
      ↓
  descriptions (1a)   what the data looks like: anchored summaries (statistic + pointer + as-of date)
      ↓
  themes (1b)         what patterns/topics emerge: thematic extraction grounded in D ids + discovery sources
      ↓
  claims (1c)         what generalizes: supported / weak / GAP, theme-tagged, evidence campaign
      ↓
  principles (1d)     what to do: design directives derived from claims -- the ladder's DELIVERABLE
                      venue-neutral throughout; no slot-mapping, no channel framing

  VENUE DECISION
  ──────────────────────────────────────
      ↓
  venue          pin modality in STATUS.md (stages_skipped + claims_settlement); write 2-venue.md (Artifact Principles)
                 (gate between FREE and ALIGNED)

  VENUE-ALIGNED (rewrite on retarget; ° = fires only if the venue requires it)
  ──────────────────────────────────────
      ↓
  pitch (2)      one-minute goal + theory of change for THIS venue + audience
      ↓
  narrative (3)° arc structure from the claim ledger
      ↓
  display (4)°   content elements: what unit carries each claim + each unit's job
                 (the retired minimap concern lives here, per-unit)
      ↓
  section-edit (5)°  per-section DPRC for sectioned venues (report, dashboard spec),
                     syncing prose to 0-sections/
```

After the lifecycle spine, delivery tooling lives under `3-build-deploy/` (`haipipe-application-artifact` = the `draft` verb, then review, claim-audit, deploy) and `4-iterate/`.

**Retarget rule:** when the venue changes, seed and the ladder stay unchanged (venue-FREE); the new venue may demand deeper claims SETTLEMENT (more GAPs resolved, deeper 1d derivations), which is gate work, not content invalidation. Pitch, narrative, display, and section-edit rewrite for the new venue.

**Ladder sweep (`ladder` verb):** dispatch the four rung skills in order (descriptions -> themes -> claims -> principles), each running its own DPRC. Gate batching per the venue's depth (wiki/08-stage-gate.md): light = ONE combined inline gate at 1d (one approval writes four ledger rows); medium = combined gate at 1c + gate at 1d; full = four individual gates. A rung that hits a blocker stops the sweep at its own CHECK.

Venue-Gated Dispatch
---------------------

Before dispatching stages 3-5, read STATUS.md `stages_skipped`. Dispatching a skipped stage is a routing error: tell the user the pinned venue skips it and offer the frontier instead. Venue examples (authoritative table: each `_venue/venue-<name>/README.md`):

```
sms / push / reminder    skip narrative, display, section-edit   (claims_settlement: light)
checklist / email        narrative optional; skip section-edit   (claims_settlement: medium)
dashboard / ui-card /    all stages fire                         (claims_settlement: full)
report
```

Auto-Detect Frontier (no verb given)
-------------------------------------

```
1. Read STATUS.md: venue, stages_skipped, Gate Ledger, current_layer.
2. Build the ordered stage list [0-seed, 1a-descriptions, 1b-themes, 1c-claims,
   1d-principles, venue, 2-pitch, 3-narrative, 4-display, 5-section-edit],
   dropping stages in stages_skipped.
3. Frontier = earliest stage without a gate-confirmed artifact
   (disk predicate first, ledger second; drift -> trust disk).
4. If no venue pinned and the ladder (through 1d) is confirmed -> frontier = venue.
5. Dispatch to the frontier's stage skill (an unstarted ladder -> suggest the
   `ladder` sweep); if the lifecycle is complete for this venue -> suggest
   /haipipe-application draft.
```

Loopback Rule
--------------

```
symptom                                  → loop back to
─────────────────────────────────────────────────────────
data profile stale / number unanchored   → descriptions (1a)
theme ungrounded / pattern space wrong   → themes (1b)
evidence missing for claim               → claims (1c)
principle doesn't follow from its claims → principles (1d)
theory of change wrong                   → pitch
output structure wrong                   → narrative (or venue)
content element doesn't carry its claim  → display
section prose fails its job              → section-edit
venue wrong for audience                 → venue (re-pin; pitch+ re-couple; the ladder SURVIVES)
stakeholder/clinician review rejected    → round → target stage
A/B test shows no effect                 → pitch or claims (1c), with fresh A/B data backfilled into 1a first
kill criterion met                       → seed → STATUS.md retired
```

Specialist Return Contract
---------------------------

Each stage specialist returns the standard tail (status / summary / artifacts / next) and closes with the full closing block (simplified tail + stage line + phase line) defined in `../../haipipe-application/SKILL.md` (Closing Block section); the stage line renders from disk via `../../haipipe-application/stage-strip.sh`.

Relation to Parent Orchestrator
--------------------------------

```
haipipe-application (router + Console)  -- consults _venue/venue-<name> + _audience/profile-<name>
            |
            v
haipipe-application-lifecycle (this orchestrator)
  VENUE-FREE:
  |-- seed (0)
  |-- the evidence ladder (`ladder` = the sweep):
  |     |-- descriptions (1a)   anchored data profile
  |     |-- themes (1b)         grounded patterns
  |     |-- claims (1c)         ledger + campaign
  |     +-- principles (1d)     design directives (deliverable)
  VENUE DECISION:
  |-- venue              (pin modality + stages_skipped + claims_settlement in STATUS.md; write 2-venue/2-venue.md Artifact Principles)
  VENUE-ALIGNED (° = venue-gated):
  |-- pitch (2)
  |-- narrative (3)°
  |-- display (4)°       (content elements + per-unit jobs)
  +-- section-edit (5)°  (sectioned venues; per-section hub dispatching 2-phase/ workers)

Every stage skill runs its phases through the shared 2-phase/ workers
(haipipe-application-draft / -probe / -revise / -check); users never invoke those directly.
Delivery tooling (artifact/review/claim-audit/deploy) lives in 3-build-deploy/; post-deploy in 4-iterate/.
```

Risk profile
=============

READ-ONLY. Dispatches to stage skills which do the writing.
