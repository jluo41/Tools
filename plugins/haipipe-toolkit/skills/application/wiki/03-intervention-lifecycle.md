# Intervention Lifecycle

The application lifecycle is a delivery lifecycle. It owns the intervention-specific story, claim wording, content elements, and artifact text. Project-level evidence lives in discoveries and tasks. Same stage vocabulary and spine ORDER as paper (`../../paper/1-lifecycle/ref/03-paper-lifecycle.md`); the venue profile gates which stages fire.

## Folder Contract

```text
<intervention-root>/
├── STATUS.md                 venue, stages_skipped, claims_settlement, current_layer, maturity, Gate Ledger
├── 0-lifecycle/
│   ├── 0-seed/           venue: FREE      0-seed.md + _LOG
│   ├── 1-claims/         venue: FREE      1-claims.md (Claims/Probes/Campaign — AND the home of
│   │                                      every claim's STATUS) + _LOG + _VALUES_ (+ _CITATION_ sectioned venues)
│   ├── 2-venue/          venue: PIN       2-venue.md (choice + Artifact Principles) + _LOG
│   ├── 2-pitch/          venue: ALIGNED   2-pitch.md + _LOG
│   ├── 3-narrative/      venue: GATED     3-narrative.md + _LOG          (if venue requires)
│   ├── 4-display/        venue: GATED     4-display.md + _LOG            (if venue requires)
│   └── 5-section-edit/   venue: GATED     per-section scaffolds + _LOG   (sectioned venues)
├── 0-sections/               sectioned-venue prose
├── 0-artifacts/              <slug>-v{N}.md · REVIEW-* · CLAIM_AUDIT.md
├── 1-probes/PPNN_<topic>.md  the probe FILES: one per TOPIC, question SECTIONS inside
│                             (serves/target/state/q-executor/a-consumer + one `## Why`)
├── 1-rounds/vYYMMDD/         work rounds
└── data/contract.yaml        input-data contract (data-consuming venues)
```

Stage docs are markdown + `_LOG` (argument documents need no compilation). `0-` = source of truth, `1-` = process.

## Lifecycle Stages

| Stage | Job | Main question | Venue | Typical handoff |
|---|---|---|---|---|
| `0-seed` | Keep the intervention possibility alive | Why might this work? | FREE | claims or drop |
| `1-claims` | Maintain the claim ledger (and every claim's STATUS) | What must be true? Which answer settles it? | FREE | venue → pitch |
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

The venue pin (between claims and pitch) writes three STATUS.md rows the whole system reads:

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

Authoritative per-venue table: each `_venue/venue-<name>/README.md`. Simple venues: seed → claims → venue → pitch → draft. Complex venues: all stages before draft.

## Venue-FREE / Venue-ALIGNED Boundary

Seed and claims are venue-FREE: written before the pin, unchanged on retarget (the ledger's truth does not change with the channel). Pitch, narrative, display, and section-edit are venue-ALIGNED: they rewrite on retarget. Retargeting (sms → dashboard) re-runs venue + pitch and may DEEPEN the claims settlement requirement — it never invalidates the ledger. Slot-mapping (which supported claim fills which template slot) is venue-ALIGNED work and happens in draft/display, never in claims.

## Phase Dimension

Stages × phases is a two-axis model. Each stage skill in `1-lifecycle/` defines WHAT the stage delivers; the `2-phase/` workers define HOW: DRAFT → PROBE → REVISE → CHECK (`haipipe-application-{draft,probe,revise,check}`). The PROBE phase runs the five-step loop (ORGANIZE → MATCH → DISPATCH → POINT → INTERPRET) via the `haipipe-application-probe` worker — the ONLY door — matching the bank's QA corpus before it commissions anything, and dispatching straight to the task/discovery orchestrators (the probe gateway is retired). It ends with a VERIFY step: `check-probe-cards.sh` FAILs `planned` sections, dangling targets, `harvest: OWED` lane debts, OVERDUE commissioned builds, and either LAW-2 leak (the stake crossing into a commission; our claim ids appearing in a bank QA file). The CHECK gate re-runs the same checker (its teeth) and runs `checks.sh` (markdown-safe deterministic checks); `> CHECK:` threads are seeded in stage docs only, and artifact-level findings go to the Gate Ledger notes. CHECK is the only human-involved phase, venue-scaled (inline for simple venues, full reports for complex). Users invoke stage skills only, never phases.

## Maturity Ladder

Maturity is derived from disk, not declared. Orthogonal to the current stage.

```text
maturity           condition
──────────         ─────────────────────────────────────────────
prospect           0-seed/ exists
claim-ledger       1-claims/ has C-slots
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
| evidence missing for claim | `1-claims` |
| theory of change wrong | `2-pitch` |
| output structure wrong | `3-narrative` (or venue) |
| content element doesn't carry its claim | `4-display` |
| section prose fails its job | `5-section-edit` |
| stakeholder/clinician review rejects | `1-rounds` then target stage |
| A/B test shows no effect | `2-pitch` or `1-claims` |
| venue wrong for audience | `venue` (re-pin; pitch+ re-couple; claims SURVIVES) |
| kill criterion met | STATUS.md → `retired` |

## Evidence Flow (the five-step loop)

```text
stage DRAFT RAISES A QUESTION
    ↓
① ORGANIZE   a SECTION in 1-probes/PPNN_<topic>.md (one file per topic; one `## Why` per file,
             holding the stake — which never leaves it). The `q-executor` is written here:
             the question in GENERAL language, stake stripped, FROZEN.
    ↓
/haipipe-application probe run [PPNN]  →  haipipe-application-probe
    ↓
② MATCH      grep the bank's QA corpus and READ the hits — match ON THE ANSWER, never on the
             topic. T0 JOIN · T1 LOCAL · T2 REUSE. **MOST QUESTIONS STOP HERE.** The bank fills
             autonomously from executor sessions, so most answers exist before anyone asks.
    ↓
③ DISPATCH   T3/T4 only: the `q-executor` block, VERBATIM, and nothing else — never the `## Why`,
             never the probe file — to
                 Agent(haipipe-task-orchestrator-agent)
                 Agent(haipipe-discovery-orchestrator-agent)
             THEIR CLEAN CONTEXT IS THE WALL. Inside, each runs its own `qa` gate:
                 ① QA SCAN (already answered?) ② DIGEST (results/ answer it, no digest?)
                 ③ P-B-E-R at the shallowest depth that answers it
             and WRITES <task-folder>/QA/<n>-<slug>.md itself.
             💀 the probe GATEWAY agent is RETIRED — its SWEEP became step ②.
    ↓
④ POINT      the section's `target:` → the answering QA FILE (the file, never the folder)
    ↓
⑤ INTERPRET  the section's `a-consumer:` → THE CLAIM'S STATUS FLIPS IN 1-claims.md
             (supported | refuted | inconclusive + confidence + claim_type);
             the harvest lanes pay out; sections/rounds backfill from the reading.
             There is no verdict block. "Verdict" is retired as a probe field.
    ↓
VERIFY: check-probe-cards.sh — `planned` sections, dangling targets, OWED lanes, OVERDUE
commissioned builds, and BOTH LAW-2 surfaces (a commission carrying the stake; a bank QA file
carrying our claim ids) all FAIL. The stage CHECK gate re-runs the same script before green.
```

Light settlement venues rarely dispatch — they select from what the bank already holds; full venues run the whole chain. There is NO probes/ folder, NO per-stage `_PROBE/`, NO `1-probe-plans/` index, and NO `_ASK/`/`_ANS/` mailbox anywhere in the bank.

## Paper ↔ Application Comparison

```text
paper                                application
─────                                ──────────────
same stage names, same spine order   same (seed → claims → [venue] → pitch → narrative → display → section-edit)
_venue/ = journal playbooks          _venue/ = output modalities + _audience/ axis
all stages fire; claims fully settle venue gates stages 3-5 + sets claims settlement depth
0-sections/ TeX → compile → submit   0-artifacts/ markdown → draft → review → deploy
respond (rebuttal) / present         iterate (A/B results → refine)
Paper Console                        Intervention Console
papers repo-backed                   interventions = plain in-project folders
```
