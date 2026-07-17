# Intervention Lifecycle

The application lifecycle is a delivery lifecycle. It owns the intervention-specific story, the stage-1 evidence ladder, content elements, and artifact text. Project-level evidence lives in discoveries and tasks. Same spine ORDER as paper (`../../paper/wiki/03-paper-lifecycle.md`) with one intentional delta: paper's single `1-claims` stage is here the four-rung ladder `1a-1d` (SOP-ladder-restage.md); the venue profile gates which stages fire.

## Folder Contract

```text
<intervention-root>/
├── STATUS.md                 venue, stages_skipped, claims_settlement, current_layer, maturity, Gate Ledger
├── 0-lifecycle/
│   ├── 0-seed/           venue: FREE      0-seed.md + _LOG
│   ├── 1a-descriptions/  venue: FREE      1a-descriptions.md (anchored data summaries + as-of dates) + _LOG
│   ├── 1b-themes/        venue: FREE      1b-themes.md (grounded themes T←D) + _LOG
│   ├── 1c-claims/        venue: FREE      1c-claims.md (Claims/Campaign, C←T + claim STATUS) + _LOG + _VALUES_ (+ _CITATION_ sectioned venues)
│   ├── 1d-advice/        venue: FREE      1d-advice.md (design advice A←C — the ladder's deliverable) + _LOG
│   ├── 2-venue/          venue: PIN       2-venue.md (choice + Artifact Principles) + _LOG
│   ├── 2-pitch/          venue: ALIGNED   2-pitch.md + _LOG
│   ├── 3-narrative/      venue: GATED     3-narrative.md + _LOG          (if venue requires)
│   ├── 4-display/        venue: GATED     4-display.md + _LOG            (if venue requires)
│   └── 5-section-edit/   venue: GATED     per-section scaffolds + _LOG   (sectioned venues)
├── 0-sections/               sectioned-venue prose
├── 0-artifacts/              <slug>-v{N}.md · REVIEW-* · CLAIM_AUDIT.md
├── 1-probes/                 the flat probe pool (one file per TOPIC, PPNN_<topic>.md)
├── 1-rounds/vYYMMDD/         work rounds
└── data/contract.yaml        input-data contract (data-consuming venues)
```

Stage docs are markdown + `_LOG` (argument documents need no compilation). `0-` = source of truth, `1-` = process.

## Lifecycle Stages

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

## Venue Gating

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

Authoritative per-venue table: each `venue/venue-<name>/README.md`. Simple venues: seed → ladder → venue → pitch → draft. Complex venues: all stages before draft. The venue also batches the LADDER's gates (light: one combined gate at 1d; medium: 1c + 1d; full: four) — see `08-stage-gate.md`.

## Venue-FREE / Venue-ALIGNED Boundary

Seed and the evidence ladder (1a-1d) are venue-FREE: written before the pin, unchanged on retarget (data truth, patterns, claims, and content-level design advice does not change with the channel). Pitch, narrative, display, and section-edit are venue-ALIGNED: they rewrite on retarget. Retargeting (sms → dashboard) re-runs venue + pitch and may DEEPEN the ladder's settlement requirement — it never invalidates it. Slot-mapping (which advice entry fills which template slot) is venue-ALIGNED work and happens in draft/display, never in the ladder.

## Phase Dimension

Stages × phases is a two-axis model. Each stage skill in `1-lifecycle/` defines WHAT the stage delivers; the `2-phase/` workers define HOW: DRAFT → PROBE → REVISE → CHECK (`haipipe-application-{draft,probe,revise,check}`). The PROBE phase runs the probe layer's five-step loop — ORGANIZE → MATCH → DISPATCH → POINT → INTERPRET — through the `haipipe-application-probe` worker, the ONLY door. DISPATCH goes through the stake-free collector `Agent(haipipe-probe-q-executor-agent)`, which calls the task/discovery orchestrators in clean context; the stage never calls them itself. A probe is COMMUNICATION, not judgment: it carries a question out and an answer back, and a claim's STATUS is written by the author into `1c-claims.md`, never in the probe file. PROBE ends with a VERIFY step: `check-probe-cards.sh` FAILs `state: planned` sections, dangling refs, `harvest: OWED` lane debts, and dead vocabulary. The CHECK gate re-runs the same checker (its teeth) and runs `checks.sh` (markdown-safe deterministic checks); `> CHECK:` threads are seeded in stage docs only, and artifact-level findings go to the Gate Ledger notes. CHECK is the only human-involved phase, venue-scaled (inline for simple venues, full reports for complex). Users invoke stage skills only, never phases.

## Maturity Ladder

Maturity is derived from disk, not declared. Orthogonal to the current stage.

```text
maturity           condition
──────────         ─────────────────────────────────────────────
prospect           0-seed/ exists
data-described     1a-descriptions/ has anchored D entries
claim-ledger       1c-claims/ has C-slots
advised         1d-advice/ has derived A entries (ladder gate passed)
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

## Loopback Rule

The lifecycle is not linear. When work fails, return to the earliest stage that explains the failure:

| Symptom | Loop back to |
|---|---|
| data profile stale / number unanchored | `1a-descriptions` |
| theme ungrounded / pattern space wrong | `1b-themes` |
| evidence missing for claim | `1c-claims` |
| advice entry does not follow from its claims | `1d-advice` |
| theory of change wrong | `2-pitch` |
| output structure wrong | `3-narrative` (or venue) |
| content element doesn't carry its claim | `4-display` |
| section prose fails its job | `5-section-edit` |
| stakeholder/clinician review rejects | `1-rounds` then target stage |
| A/B test shows no effect | `2-pitch` or `1c-claims` (backfill the A/B data into `1a` first) |
| venue wrong for audience | `venue` (re-pin; pitch+ re-couple; the ladder SURVIVES) |
| kill criterion met | STATUS.md → `retired` |

## Evidence Flow (flat probe pool)

```text
stage DRAFT raises the questions (a Q-consumer list); APPROVE (human) picks which to pursue
    ↓
① ORGANIZE  each approved question → a SECTION in 1-probes/PPNN_<topic>.md (one file per TOPIC),
            with serves / target / state / q-executor (stake stripped) / a-consumer + one ## Why per file
    ↓
② MATCH     scan the bank's QA corpus FIRST — most sections REUSE an existing answer and stop here
    ↓
③ DISPATCH  only the misses, via Agent(haipipe-probe-q-executor-agent) — the stake-free collector,
            which calls the task/discovery orchestrators in clean context (that context IS the wall)
    ↓
④ POINT     target: → the answering QA FILE (verify with ls + the state line)
    ↓
⑤ INTERPRET write the a-consumer; if it serves a claim, the AUTHOR flips that claim's STATUS
            (supported | weak | GAP) in 1c-claims.md — never in the probe file; harvest lanes pay out
    ↓
VERIFY: check-probe-cards.sh — planned sections, dangling refs, OWED lane debts, and dead vocabulary FAIL;
the stage CHECK gate re-runs the same script before it can go green
```

Light settlement venues rarely dispatch — they REUSE from the bank's existing QA corpus; full venues run the whole chain. Probe files live in the flat `1-probes/` pool (one file per TOPIC, one SECTION per question); the per-stage `_PROBE/` folders and the `1-probe-plans/README.md` index are RETIRED — a legacy file is migrated into `1-probes/` on first touch only.

## Paper ↔ Application Comparison

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
