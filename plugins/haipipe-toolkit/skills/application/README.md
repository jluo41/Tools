# Application Skill

Canonical reference for the application skill family's STRUCTURE. This file wins over anything elsewhere on layout, routing, and maturity vocabulary; the three operating contracts live with their owners (References, below). Structural twin of `../paper/` (same spine, same phases, same probe door); deltas listed at the bottom.

An intervention is a delivery contract, not a drafting folder. It owns one deliverable's story, the stage-1 evidence ladder (1a-descriptions → 1b-themes → 1c-claims → 1d-advice, echoing D→I→K→W: paper delivers K, application delivers W), displays, and artifact text. Evidence lives in tasks/discoveries at the project level; open questions accumulate in the flat probe pool `1-probes/PPNN_<topic>.md` (one file per TOPIC), each a SECTION carrying the question + its bound bank answer. Claim status lives in `0-lifecycle/1c-claims/1c-claims.md`, not in the probe file. Each stage's PROBE phase binds every section to an answer through the stake-free collector agent (never calling task/discover directly). Standalone utility goes to the bank's own door (`/haipipe-task qa` | `/haipipe-discovery qa`), never proxied by the intervention.

## The ladder is a flywheel (a growth loop, not a one-way climb)

The ladder is drawn 1a→1d but RUNS as routing rounds: downstream work keeps exposing what upstream didn't know to look for, and every back-edge is a discovery event, not a failure. Deploy itself is a probe — A/B results flow back into 1a as fresh data.

```text
        🌱 seed ──▶ 📊 1a ──▶ 🧩 1b ──▶ ⚖️ 1c ──▶ 🎯 1d ──▶ 📌 venue ──▶ 🚀 deploy
                     ▲ ▲       │ ▲       │ ▲       │  │                     │
                     │ └───────┘ └───────┘ └───────┘  │                     │
                     │  "theme     "hook     "A exposes gap" → new 1c probe │
                     │   needs a    needs     · refuted C → re-theme        │
                     │   number"    ground"                                 │
                     └────── 🔁 iterate: new data → refresh D → [STALE] stamps ◀─┘
```

Three nested loops give breadth AND depth; only CHECK gates involve the user:

```text
  ┌─ 🔁 OUTER (weeks) ── deploy/iterate → new data → 1a refresh ──────────┐
  │  ┌─ 🌀 MIDDLE (days) ── routing rounds ACROSS rungs (mid-phase legal) ─┐ │
  │  │  ┌─ 🔂 INNER (hours) ── multi-round DPRC WITHIN a rung ──────────┐ │ │
  │  │  │   draft → probe → revise → self-assess → dry? → check         │ │ │
  │  │  └───────────────────────────────────────────────────────────────┘ │ │
  │  └─────────────────────────────────────────────────────────────────────┘ │
  └───────────────────────────────────────────────────────────────────────────┘
```

Breadth is systematic, not mood-dependent — each rung sweeps its LENSES and banks what it drops in a RESERVOIR that the next round re-mines:

```text
rung    lenses (sweep each or waive)                          reservoir (re-mined at DRAFT)
────    ─────────────────────────────────────────────         ─────────────────────────────
1a      schema disposition · 6 facets · question-storm lenses   waived facets
1b      data patterns · field/lit · counter-hunt               Parked patterns
1c      confirm · refute-capable probe · rival explanation     Declined hooks
1d      exploit (proven) · explore (bet) · negative advice     Rejected entries
```

Contract (encoded in each rung skill): REVISE ends with a self-assessment; a round that surfaced anything new triggers another DRAFT→PROBE→REVISE lap (`[ROUND n]` in `_LOG`), and CHECK fires only when a round comes up dry (venue-scaled: light may stop after one round, full loops-until-dry everywhere). Mid-phase back-routing is legal — file the upstream slot/card immediately and log `[ROUTE -> <rung>]`; never wait for a gate to report a discovery.

## Intervention-folder layout

```text
<intervention-root>/
├── STATUS.md                 venue, stages_skipped, Gate Ledger, current layer, maturity
├── 0-lifecycle/              maturation spine (md + _LOG)
│   ├── 0-seed/
│   ├── 1a-descriptions/  1b-themes/  1c-claims/  1d-advice/   ← the evidence ladder (venue-FREE)
│   │   (1a: anchored data summaries; 1b: grounded themes; 1c: Claims/Q-consumer/Campaign;
│   │    1d: design advice A←C — the ladder's deliverable)
│   ├── 2-venue/  2-pitch/  3-narrative/  4-display/  5-section-edit/
│   │   (2-venue: choice + Artifact Principles = channel-HOW, vs 1d content-WHAT)
├── 0-sections/               sectioned-venue prose (report/dashboard-like venues only)
├── 0-artifacts/              deliverables: <slug>-v{N}.md, REVIEW-*, CLAIM_AUDIT.md
├── 1-probes/                 the flat probe pool (one file per TOPIC)
├── 1-rounds/vYYMMDD/         work rounds (discussion, decisions, todo, applied)
└── data/contract.yaml        input-data contract (when the venue consumes data)
```

`0-` = source of truth (content). `1-` = process (build + revise). Stages 3-5 exist only when the pinned venue requires them.

## Skill-tree layout

The skill tree mirrors the lifecycle spine on two axes: `1-lifecycle/` holds the STAGE orchestrators (user-facing; define WHAT each stage delivers) and `2-phase/` holds the PHASE workers (internal; define HOW: DRAFT -> PROBE -> REVISE -> CHECK). Inside those two groups each numbered stage/phase folder holds its skills; support groups stay flat.

```text
application/
├── haipipe-application/   router + Intervention Console front door + stage-strip.sh + fn/ + PREFERENCES.md
│                          (also THE home of the Stage Gate Protocol + Delivery Need Routing + Closing Block)
├── README.md              canonical structure (this file)
├── PHILOSOPHY.md          design philosophy
├── 0-enter/               haipipe-application-enter (Console; owns the Dashboard Contract) + haipipe-application-round
├── 1-lifecycle/           STAGE orchestrators, one numbered folder per stage
│     0-seed/haipipe-application-seed                  (venue-FREE)
│     1a-descriptions/haipipe-application-descriptions (venue-FREE, ladder rung: anchored data profile)
│     1b-themes/haipipe-application-themes             (venue-FREE, ladder rung: grounded patterns)
│     1c-claims/haipipe-application-claims             (venue-FREE, ladder rung: ledger + campaign)
│     1d-advice/haipipe-application-advice             (venue-FREE, ladder rung: design advice — deliverable)
│     2-pitch/haipipe-application-pitch                (venue-ALIGNED)
│     3-narrative/haipipe-application-narrative        (venue-GATED)
│     4-display/haipipe-application-display            (venue-GATED; owns per-unit jobs)
│     5-section-edit/haipipe-application-section-edit  (sectioned venues)
│     + haipipe-application-venue (pin modality + stages_skipped + claims_settlement; writes 2-venue/2-venue.md Artifact Principles; after the ladder (1d gate), before pitch)
│     + haipipe-application-lifecycle (orchestrator; owns the Intervention Lifecycle Contract)
├── 2-phase/               PHASE workers (internal; driven by stage skills)
│     README.md + USAGE.md + WIRING.md    (bucket-root docs: architecture, recipes, wiring)
│     0-draft/haipipe-application-draft
│     1-probe/haipipe-application-probe   (the ONLY evidence door; + check-probe-cards.sh, ref/)
│     2-revise/haipipe-application-revise
│     3-check/haipipe-application-check   (+ checks.sh, gate-persona.md, attendance-modes.md)
├── 3-deliver/             haipipe-application-artifact (the `draft` verb) + review + claim-audit + deploy
├── 4-iterate/             haipipe-application-iterate (post-deploy A/B refinement)
└── venue/                 venue packs (knowledge, not stages; README + style-profile [+ exemplars])
```

## Stage to Procedure

```text
enter             -> 0-enter/haipipe-application-enter
0-seed            -> 1-lifecycle/0-seed/haipipe-application-seed
ladder (sweep)    -> haipipe-application-lifecycle ladder (runs 1a->1d; venue-scaled gate batching)
1a-descriptions   -> 1-lifecycle/1a-descriptions/haipipe-application-descriptions
1b-themes         -> 1-lifecycle/1b-themes/haipipe-application-themes
1c-claims         -> 1-lifecycle/1c-claims/haipipe-application-claims
1d-advice         -> 1-lifecycle/1d-advice/haipipe-application-advice
venue (pin)       -> 1-lifecycle/haipipe-application-venue (after the ladder, before pitch; the ladder is venue-free; writes 0-lifecycle/2-venue/2-venue.md)
2-pitch           -> 1-lifecycle/2-pitch/haipipe-application-pitch
3-narrative       -> 1-lifecycle/3-narrative/haipipe-application-narrative      (venue-gated)
4-display         -> 1-lifecycle/4-display/haipipe-application-display          (venue-gated)
5-section-edit    -> 1-lifecycle/5-section-edit/haipipe-application-section-edit (sectioned venues)
draft (artifact)  -> 3-deliver/haipipe-application-artifact
review / audit    -> 3-deliver/haipipe-application-{review,claim-audit}
deploy            -> 3-deliver/haipipe-application-deploy
round             -> 0-enter/haipipe-application-round
iterate           -> 4-iterate/haipipe-application-iterate
```

Every stage drives its phases through the `2-phase/` workers (never user-invoked directly):

```text
DRAFT  -> 2-phase/0-draft/haipipe-application-draft
PROBE  -> 2-phase/1-probe/haipipe-application-probe   (runs the five-step loop; the collector agent is the only door to the bank)
REVISE -> 2-phase/2-revise/haipipe-application-revise
CHECK  -> 2-phase/3-check/haipipe-application-check   (the only human-involved phase; writes the Gate Ledger)
```

## Router Rule

`haipipe-application` should first resolve intervention status through `enter`. Then route actions by the user's intended lifecycle object:

```text
status / enter / preload                    -> 0-enter
seed / ladder / descriptions / themes
  / claims / advice / venue / pitch
  / narrative / display / section-edit      -> 1-lifecycle
round / todo / decisions                    -> 0-enter/haipipe-application-round
draft / write / make the <venue>            -> 3-deliver/haipipe-application-artifact
review / claim-audit / deploy               -> 3-deliver
iterate / A/B                               -> 4-iterate
probe / evidence gap                        -> a section in the flat pool 1-probes/; `run` -> 2-phase/1-probe worker
venue / which channel                       -> 1-lifecycle/haipipe-application-venue
  (the pinned venue's pack                  -> venue/venue-<name>, consulted by each aligned stage)
```

## Maturity Rule

Every application-aware response should report both:

```text
current_layer: 0-seed | 1a-descriptions | 1b-themes | 1c-claims | 1d-advice | venue | 2-pitch | 3-narrative | 4-display | 5-section-edit | draft | review | deploy
maturity: prospect | data-described | claim-ledger | advised | venue-pinned | pitched | narrated | display-mapped | section-edit | drafted | reviewed | deployed | iterating | retired
```

Layer answers "where is the active work?" Maturity answers "how real is the intervention?"

## References

| File | Read it for |
|---|---|
| `1-lifecycle/haipipe-application-lifecycle/SKILL.md` | Intervention Lifecycle Contract: folder contract, stage spine, venue gating, maturity ladder, loopback rule, evidence flow |
| `haipipe-application/SKILL.md` | Stage Gate Protocol (Gate Ledger, venue-scaled depth, ladder gate batching, rounds) + Delivery Need Routing (probe/evidence interface) + Closing Block |
| `0-enter/haipipe-application-enter/SKILL.md` | Dashboard Contract: derive-from-disk rules, frontier detection, open-needs detection, strip symbols |
| `PHILOSOPHY.md` | design philosophy |

The four evidence principles (land-at-home, review-on-write, layered orders, trim-ceremony-not-principle) are SHARED root doctrine owned by the paper family — see `../paper/1-lifecycle/ref/08-stage-gate.md` ("Evidence Principles"), not a copy here.

## Deltas vs paper (intentional, not drift)

| paper | application |
|---|---|
| stage 1 = single claims ledger (Hypotheses play the theme role; the manuscript's Methods/Results carry D/I) — paper delivers K | stage 1 = the evidence ladder 1a-descriptions/1b-themes/1c-claims/1d-advice (the artifact carries no D/I body; data is dynamic) — application delivers W |
| venue = journal playbook | venue = output modality (sms/email/dashboard/report/...) + tone-by-audience |
| all stages always fire; claims always fully settled | venue gates stages 3-5, sets claims SETTLEMENT depth (light/medium/full), and batches the ladder's gates |
| 0-sections/ TeX -> compile -> submit | 0-artifacts/ markdown -> draft(artifact) -> review -> deploy |
| respond (rebuttal) / present | iterate (A/B results -> refine; fresh data backfills 1a, staleness propagates A←C←T←D) |
| papers repo-backed inside Project-* repos | interventions are plain in-project folders |

## Retired names

| Retired | Use instead |
|---|---|
| `haipipe-application-ask` (+ SESSION_STATE machinery) | `/haipipe-application enter` console; ad-hoc questions -> `/haipipe-probe "<question>"` |
| `haipipe-application-minimap` (stage 5) | unit jobs live in `4-display` per-unit contracts |
| `haipipe-application-gate` | `2-phase/3-check/haipipe-application-check` (the CHECK phase) |
| `haipipe-application-draft` as artifact generator | `3-deliver/haipipe-application-artifact` (verb stays `draft`) |
| spine `seed → pitch → [venue] → claims → ... → minimap` | `seed → 1a-1d ladder → [venue] → pitch → narrative → display → section-edit` |
| flat `0-lifecycle/N-stage.md` files | stage FOLDERS `0-lifecycle/N-stage/` (md + _LOG) |
| per-stage `_PROBE/PPNN_*.md` cards; `1-probe-plans/README.md` index; `/haipipe-probe plan from-need` | flat pool `1-probes/PPNN_<topic>.md` (one file per TOPIC, one SECTION per question, states `planned\|commissioned\|answered\|read\|answered-local\|failed`); `/haipipe-application probe "<q>"` raises a section + `probe run` |
| verdict word `confirmed`; PP-card `## Verdict` / G1-G2-G3 | claim status `supported \| weak \| GAP` in `0-lifecycle/1c-claims/1c-claims.md` (no `## Verdict`, no gate) |
| `applications/ask/<NN>/` case files | dead history: nothing reads, nothing writes |
| stage folder `1-claims/` (single stage-1 ledger) | the ladder `1a-descriptions/ 1b-themes/ 1c-claims/ 1d-advice/` (SOP-ladder-restage, 2026-07-09); legacy interventions: `enter` offers the confirm-gated one-shot migration (rename to `1c-claims/`, scaffold rungs, re-file probes by shape) on next open |
| `1d-principles` / `haipipe-application-principles` / `P<n>` ids / maturity `principled` (hours-old, same restage) | `1d-advice` / `haipipe-application-advice` / `A<n>` / `advised` (JL ruling 2026-07-09: advice = counsel downstream stages adopt or decline; `principles` survives only as a verb alias) |
