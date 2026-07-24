---
name: haipipe-application-lifecycle
description: "Orchestrator for the intervention structure lifecycle (1-lifecycle). Routes to stage specialists across the venue-free/venue-aligned boundary: seed and the evidence ladder (1a-descriptions, 1b-themes, 1c-claims, 1d-advice) are venue-FREE (don't change on retarget); venue pins the modality and gates stages 3-5; pitch, narrative, display, and section-edit are venue-ALIGNED (rewrite on retarget). The `ladder` verb runs 1a->1d as one sweep with venue-scaled gate batching. Stage skills internally run DRAFT -> PROBE -> REVISE -> CHECK via 2-phase/ workers. Trigger: lifecycle, advance, next stage, ladder, intervention structure, /haipipe-application-lifecycle."
argument-hint: "[stage-verb|ladder] [intervention-path]"
allowed-tools: Bash, Read, Grep, Glob, Skill
metadata:
  version: "0.4.4"
  last_updated: "2026-07-19"
  summary: "Routes intervention structural work across the venue-free/venue-aligned boundary: seed + the ladder (1a-1d) are venue-FREE, the venue pin gates stages 3-5, and pitch/narrative/display/section-edit rewrite on retarget. History: ./CHANGELOG.md."
---

Skill: haipipe-application-lifecycle (orchestrator)
====================================================

User-facing entry for **intervention structural work** -- everything that decides *what the intervention is* before the artifact exists, or when the argument needs rethinking. The orchestrator owns routing only; each stage specialist owns its own workflow, inputs, and outputs.

The lifecycle has a **venue-free / venue-aligned boundary**. Seed and the evidence ladder (1a-1d) are venue-FREE (they don't change when you retarget to a different channel). Venue is the decision gate that pins the modality in STATUS.md -- and, because application venues differ in weight, it also writes which stages the venue skips (`stages_skipped`) and how much of the claims ledger must settle (`claims_settlement`). Pitch, narrative, display, and section-edit are venue-ALIGNED (they rewrite when you retarget).

```
/haipipe-application-lifecycle                       -> dashboard (list specialists + pipeline)
/haipipe-application-lifecycle seed <args>           -> 0-lifecycle/0-seed/0-seed.md (venue-FREE)
/haipipe-application-lifecycle ladder <args>         -> the 1a->1d sweep (each rung's skill in order; ONE batched gate per the venue's depth, Stage Gate Protocol)
/haipipe-application-lifecycle descriptions <args>   -> 0-lifecycle/1a-descriptions/1a-descriptions.md (venue-FREE anchored data profile)
/haipipe-application-lifecycle themes <args>         -> 0-lifecycle/1b-themes/1b-themes.md (venue-FREE grounded themes)
/haipipe-application-lifecycle claims <args>         -> 0-lifecycle/1c-claims/1c-claims.md (venue-FREE claim ledger + campaign)
/haipipe-application-lifecycle advice <args>         -> 0-lifecycle/1d-advice/1d-advice.md (venue-FREE design advice -- the ladder's deliverable)
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

Stage artifacts are markdown (`N-<stage>.md` + `_LOG_` in a stage FOLDER); the questions a stage raises live in the flat pool `1-probes/`, keyed back by each section's `serves:`. Stage gates: `../../haipipe-application/SKILL.md` (Stage Gate Protocol section).

Intervention Lifecycle Contract
================================

THE single source of truth for the intervention lifecycle: the folder contract, the stage spine, venue gating, the venue-FREE/ALIGNED boundary, the maturity ladder, and the evidence flow. The application lifecycle is a delivery lifecycle. It owns the intervention-specific story, the stage-1 evidence ladder, content elements, and artifact text. Project-level evidence lives in discoveries and tasks. Same spine ORDER as the paper family with one intentional delta: paper's single `1-claims` stage is here the four-rung ladder `1a-1d` (`../../SOP-ladder-restage.md`); the venue profile gates which stages fire.

Folder Contract
----------------

```text
<intervention-root>/
├── STATUS.md                 venue, stages_skipped, claims_settlement, current_layer, maturity, Gate Ledger
├── 0-lifecycle/
│   ├── 0-seed/           venue: FREE      0-seed.md + _LOG
│   ├── 1a-descriptions/  venue: FREE      1a-descriptions.md (anchored data summaries + as-of dates) + _LOG
│   ├── 1b-themes/        venue: FREE      1b-themes.md (grounded themes T←D) + _LOG
│   ├── 1c-claims/        venue: FREE      1c-claims.md (Claims/Campaign, C←T + claim STATUS) + _LOG
│   ├── 1d-advice/        venue: FREE      1d-advice.md (design advice A←C — the ladder's deliverable) + _LOG
│   ├── 2-venue/          venue: PIN       2-venue.md (choice + Artifact Principles) + _LOG
│   ├── 2-pitch/          venue: ALIGNED   2-pitch.md + _LOG
│   ├── 3-narrative/      venue: GATED     3-narrative.md + _LOG          (if venue requires)
│   ├── 4-display/        venue: GATED     4-display.md + _LOG            (if venue requires)
│   └── 5-section-edit/   venue: GATED     per-section scaffolds + _LOG   (sectioned venues)
├── 0-sections/               sectioned-venue prose
├── 0-artifacts/              <slug>-v{N}.md · REVIEW-* · CLAIM_AUDIT.md
├── 1-probes/                 the flat probe pool (one file per TOPIC, PPNN_<topic>/)
├── 1-rounds/vYYMMDD/         work rounds
└── data/contract.yaml        input-data contract (data-consuming venues)
```

Stage docs are markdown + `_LOG` (argument documents need no compilation). `0-` = source of truth, `1-` = process.

Lifecycle Stages
-----------------

| Stage | Job | Main question | Venue | Typical handoff |
|---|---|---|---|---|
| `0-seed` | Keep the intervention possibility alive | Why might this work? | FREE | ladder (1a) or drop |
| `1a-descriptions` | Anchored data profile (the D rung) | What does the data look like, dated? | FREE | themes |
| `1b-themes` | Grounded pattern space (the I rung) | Which patterns/topics emerge? | FREE | claims |
| `1c-claims` | Claim ledger + evidence campaign (the K rung) | Which claims generalize? | FREE | advice |
| `1d-advice` | Design advice (the W rung, the deliverable) | What should the content do, derived from which claims? | FREE | venue → pitch |
| `venue` | Pin the output modality | Which channel fits? | (chooser) | writes venue + stages_skipped + claims_settlement |
| `2-pitch` | One-minute goal + theory of change | What is this selling, to whom? | ALIGNED | narrative or draft |
| `3-narrative` | Structure the output's arc | How do claims compose? | GATED | display |
| `4-display` | Content elements + per-unit jobs | What element carries each claim, and what job does each unit do? | GATED | section-edit or draft |
| `5-section-edit` | Per-section DPRC on venue-declared sections | Does each section's prose do its job? | GATED | draft |
| `draft` | Compose the deliverable (haipipe-application-artifact) | Is the artifact venue+audience-true? | ALIGNED | review |
| `review` / `claim-audit` | Audience fit + claim traceability | Ship it? | -- | deploy or loopback |
| `deploy` | Ship to channel | -- | -- | iterate |
| `round` / `iterate` | Feedback + A/B refinement | What did the channel teach us? | -- | target stage |

The retired `minimap` stage's concern (per-unit jobs) lives inside `4-display`.

Venue Gating
-------------

The venue pin (between the ladder's 1d gate and pitch) writes three STATUS.md rows the whole system reads:

```text
| venue |             sms | push | reminder | checklist | email | dashboard | ui-card | report
| stages_skipped |    which of narrative/display/section-edit this venue skips
| claims_settlement | light | medium | full   (how much of the ledger must settle before draft)
```

```text
                 narrative   display   section-edit   claims_settlement   gate depth
venue-sms        skip        skip      skip           light               inline
venue-push       skip        skip      skip           light               inline
venue-reminder   skip        skip      skip           light               inline
venue-checklist  optional    skip      skip           medium              inline
venue-email      req         optional  skip           medium              inline
venue-dashboard  req         req       req            full                report
venue-ui-card    req         req       optional       full                report
venue-report     req         req       req            full                report
```

Authoritative per-venue table: each `../../venue/venue-<name>/README.md`. Simple venues: seed → ladder → venue → pitch → draft. Complex venues: all stages before draft. The venue also batches the LADDER's gates (light: one combined gate at 1d; medium: 1c + 1d; full: four) — see the Stage Gate Protocol in `../../haipipe-application/SKILL.md`.

Venue-FREE / Venue-ALIGNED Boundary
------------------------------------

Seed and the evidence ladder (1a-1d) are venue-FREE: written before the pin, unchanged on retarget (data truth, patterns, claims, and content-level design advice does not change with the channel). Pitch, narrative, display, and section-edit are venue-ALIGNED: they rewrite on retarget. Retargeting (sms → dashboard) re-runs venue + pitch and may DEEPEN the ladder's settlement requirement — it never invalidates it. Slot-mapping (which advice entry fills which template slot) is venue-ALIGNED work and happens in draft/display, never in the ladder.

Phase Dimension
----------------

Stages × phases is a two-axis model. Each stage skill in `1-lifecycle/` defines WHAT the stage delivers; the `2-phase/` workers define HOW: DRAFT → PROBE → REVISE → CHECK (`haipipe-application-{draft,probe,revise,check}`). The PROBE phase runs the probe layer's five-step loop — ORGANIZE → MATCH → DISPATCH → POINT → INTERPRET — through the `haipipe-application-probe` worker, the ONLY door. DISPATCH goes through the stake-free collector `Agent(haipipe-probe-q-executor-agent)`, which calls the task/discovery orchestrators in clean context; the stage never calls them itself. A probe is COMMUNICATION, not judgment: it carries a question out and an answer back, and a claim's STATUS is written by the author into `1c-claims.md`, never in the probe file. PROBE ends with a VERIFY step: `check-probe-cards.sh` FAILs `state: planned` sections, dangling refs, `harvest: OWED` lane debts, and dead vocabulary. The CHECK gate re-runs the same checker (its teeth) and runs `checks.sh` (markdown-safe deterministic checks); `> CHECK:` threads are seeded in stage docs only, and artifact-level findings go to the Gate Ledger notes. CHECK is the only human-involved phase, venue-scaled (inline for simple venues, full reports for complex). Users invoke stage skills only, never phases.

Maturity Ladder
----------------

Maturity is derived from disk, not declared. Orthogonal to the current stage.

```text
maturity           condition
──────────         ─────────────────────────────────────────────
prospect           0-seed/ exists
data-described     1a-descriptions/ has anchored D entries
claim-ledger       1c-claims/ has C-slots
advised            1d-advice/ has derived A entries (ladder gate passed)
venue-pinned       STATUS.md has venue:
pitched            2-pitch/ gate-approved
narrated           3-narrative/ gate-approved (if venue requires)
display-mapped     4-display/ gate-approved (if venue requires)
section-edit       5-section-edit/ scaffolds with DPRC in progress (sectioned venues)
drafted            0-artifacts/ has >=1 artifact
reviewed           review pass completed
deployed           artifact shipped to channel
iterating          post-deploy round open with A/B results
retired            kill criterion met; no further work
```

For simple venues, maturity jumps from `pitched` straight to `drafted`.

Evidence Flow (flat probe pool)
--------------------------------

```text
stage DRAFT raises the questions (a Q-consumer list); APPROVE (human) picks which to pursue
    ↓
① ORGANIZE  each approved question → an ENTRY (## QX<n>) in 1-probes/PPNN_<topic>/ (one file per
            TOPIC), with ### q-executor (stake stripped) / ### q-consumer / ### bank binding / ### a-executor
    ↓
② MATCH     scan the bank's QA corpus FIRST — most sections REUSE an existing answer and stop here
    ↓
③ DISPATCH  only the misses, via Agent(haipipe-probe-q-executor-agent) — the stake-free collector,
            which calls the task/discovery orchestrators in clean context (that context IS the wall)
    ↓
④ POINT     target: → the answering QA FILE (verify with ls + the state line)
    ↓
⑤ INTERPRET copy the QA answer into ### a-executor; each Q-consumer then writes its own a-consumer
            in the stage doc. If it serves a claim, the AUTHOR flips that claim's STATUS
            (supported | weak | GAP) in 1c-claims.md — never in the probe file
    ↓
VERIFY: check-probe-cards.sh — planned entries, dangling refs, and stale vocabulary FAIL;
the stage CHECK gate re-runs the same script before it can go green
```

Light settlement venues rarely dispatch — they REUSE from the bank's existing QA corpus; full venues run the whole chain. Probe files live in the flat `1-probes/` pool: one file per TOPIC, one `## QX<n>` ENTRY per q-executor.

Paper ↔ Application Comparison
-------------------------------

```text
paper                                application
─────                                ──────────────
same spine order                     stage 1 differs by design: paper = single 1-claims ledger
                                     (Hypotheses play the theme role; the manuscript's own
                                     Methods/Results carry D/I) — paper delivers K;
                                     application = the 1a-1d evidence ladder — delivers W
venue/ = journal playbooks          venue/ = output modalities (tone-by-audience folded in)
all stages fire; claims fully settle venue gates stages 3-5 + sets settlement depth + batches ladder gates
0-sections/ TeX → compile → submit   0-artifacts/ markdown → draft → review → deploy
respond (rebuttal) / present         iterate (A/B results → refine; backfills 1a, staleness A←C←T←D)
Paper Console                        Intervention Console
papers repo-backed                   interventions = plain in-project folders
```

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
  advice (1d)         what to do: design advice derived from claims -- the ladder's DELIVERABLE
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

After the lifecycle spine, delivery tooling lives under `3-deliver/` (`haipipe-application-artifact` = the `draft` verb, then review, claim-audit, deploy) and `4-iterate/`.

**Retarget rule:** when the venue changes, seed and the ladder stay unchanged (venue-FREE); the new venue may demand deeper claims SETTLEMENT (more GAPs resolved, deeper 1d derivations), which is gate work, not content invalidation. Pitch, narrative, display, and section-edit rewrite for the new venue.

**Ladder sweep (`ladder` verb):** dispatch the four rung skills in order (descriptions -> themes -> claims -> advice), each running its own DPRC. Gate batching per the venue's depth (Stage Gate Protocol, `../../haipipe-application/SKILL.md`): light = ONE combined inline gate at 1d (one approval writes four ledger rows); medium = combined gate at 1c + gate at 1d; full = four individual gates. A rung that hits a blocker stops the sweep at its own CHECK. Rungs loop internally (multi-round DPRC, loop-until-dry; Stage Gate Protocol → Rounds within a rung) and may back-route mid-phase (`[ROUTE -> <rung>]` in `_LOG`); the sweep re-enters the routed-to rung, then resumes order -- the ladder is a flywheel, not a one-way climb (README).

Venue-Gated Dispatch
---------------------

Before dispatching stages 3-5, read STATUS.md `stages_skipped`. Dispatching a skipped stage is a routing error: tell the user the pinned venue skips it and offer the frontier instead. Venue examples (authoritative table: each `venue/venue-<name>/README.md`):

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
   1d-advice, venue, 2-pitch, 3-narrative, 4-display, 5-section-edit],
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
advice entry does not follow from its claims → advice (1d)
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
haipipe-application (router + Console)  -- consults venue/venue-<name>
            |
            v
haipipe-application-lifecycle (this orchestrator)
  VENUE-FREE:
  |-- seed (0)
  |-- the evidence ladder (`ladder` = the sweep):
  |     |-- descriptions (1a)   anchored data profile
  |     |-- themes (1b)         grounded patterns
  |     |-- claims (1c)         ledger + campaign
  |     +-- advice (1d)         design advice (deliverable)
  VENUE DECISION:
  |-- venue              (pin modality + stages_skipped + claims_settlement in STATUS.md; write 2-venue/2-venue.md Artifact Principles)
  VENUE-ALIGNED (° = venue-gated):
  |-- pitch (2)
  |-- narrative (3)°
  |-- display (4)°       (content elements + per-unit jobs)
  +-- section-edit (5)°  (sectioned venues; per-section hub dispatching 2-phase/ workers)

Every stage skill runs its phases through the shared 2-phase/ workers
(haipipe-application-draft / -probe / -revise / -check); users never invoke those directly.
Delivery tooling (artifact/review/claim-audit/deploy) lives in 3-deliver/; post-deploy in 4-iterate/.
```

Risk profile
=============

READ-ONLY. Dispatches to stage skills which do the writing.
