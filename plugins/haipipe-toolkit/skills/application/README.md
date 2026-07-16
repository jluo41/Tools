# Application Skill

Canonical reference. This file + `wiki/` win over anything elsewhere. Structural twin of `../paper/` (same spine, same phases, same probe door); deltas listed at the bottom.

An intervention is a delivery contract, not a drafting folder. It owns one deliverable's story, the stage-1 evidence ladder (1a-descriptions → 1b-themes → 1c-claims → 1d-advice, echoing D→I→K→W: paper delivers K, application delivers W), displays, and artifact text. Evidence lives in tasks/discoveries at the project level (insights = optional deposit layer); open questions accumulate in the flat probe pool `1-probes/PPNN_<topic>.md` (one file per TOPIC), each a SECTION carrying the question + its bound bank answer. Claim status lives in `0-lifecycle/1c-claims/1c-claims.md`, not in the probe file. Each stage's PROBE phase binds every section to an answer through the stake-free collector agent (never calling task/discover directly). Direct task/discover for non-claim utility work only.

## The ladder is a flywheel (insight discovery, not a one-way climb)

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
│   │   (1a: anchored data summaries + _DESCRIPTIONS/ DS profile sheets; 1b: grounded themes; 1c: Claims/Probes/Campaign
│   │    + _VALUES_; 1d: design advice A←C — the ladder's deliverable)
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

```text
application/
├── haipipe-application/   router + Intervention Console front door + stage-strip.sh
├── 0-enter/               Intervention Console (haipipe-application-enter) + haipipe-application-round
├── 1-lifecycle/           stage procedures, one numbered folder per stage
│                          0-seed / 1a-descriptions / 1b-themes / 1c-claims / 1d-advice [venue-FREE]
│                          · venue · 2-pitch / 3-narrative / 4-display / 5-section-edit [venue-ALIGNED]
├── 2-phase/               shared phase workers: DRAFT-PROBE-REVISE-CHECK (DPRC)
│                          haipipe-application-{draft,probe,revise,check}
├── 3-build-deploy/        haipipe-application-{artifact,review,claim-audit,deploy}
├── 4-iterate/             post-deploy refinement (A/B results -> refine)
├── _venue/                venue profiles (knowledge, not verbs) — output modality
├── _audience/             audience profiles (knowledge) — tone within structure
└── wiki/                  lifecycle, dashboard, skill-structure, stage-gate, delivery-need
```

## References

| File | Read it for |
|---|---|
| `wiki/03-intervention-lifecycle.md` | stage spine, venue gating, maturity ladder, loopback rule, evidence handoff |
| `wiki/06-application-skill-structure.md` | skill-tree target, router rule, stage-to-procedure map |
| `wiki/08-stage-gate.md` | Gate Ledger protocol, venue-scaled gate depth, exit criteria |
| `wiki/11-delivery-need.md` | application <-> probe/evidence interface |
| `../paper/wiki/00-evidence-principles.md` | the four evidence principles (shared root doctrine) |

## Deltas vs paper (intentional, not drift)

| paper | application |
|---|---|
| stage 1 = single claims ledger (Hypotheses play the theme role; the manuscript's Methods/Results carry D/I) — paper delivers K | stage 1 = the evidence ladder 1a-descriptions/1b-themes/1c-claims/1d-advice (the artifact carries no D/I body; data is dynamic) — application delivers W |
| venue = journal playbook | venue = output modality (sms/email/dashboard/report/...) + `_audience/` axis |
| all stages always fire; claims always fully settled | venue gates stages 3-5, sets claims SETTLEMENT depth (light/medium/full), and batches the ladder's gates |
| insights = first-class deposit | insights = optional deposit (judgment lives in 1c-claims status; 1d deposits W on-request) |
| 0-sections/ TeX -> compile -> submit | 0-artifacts/ markdown -> draft(artifact) -> review -> deploy |
| respond (rebuttal) / present | iterate (A/B results -> refine; fresh data backfills 1a, staleness propagates A←C←T←D) |
| papers repo-backed inside Project-* repos | interventions are plain in-project folders |

## Retired names

| Retired | Use instead |
|---|---|
| `haipipe-application-ask` (+ SESSION_STATE machinery) | `/haipipe-application enter` console; ad-hoc questions -> `/haipipe-probe "<question>"` |
| `haipipe-application-minimap` (stage 5) | unit jobs live in `4-display` per-unit contracts |
| `haipipe-application-gate` | `2-phase/3-check/haipipe-application-check` (the CHECK phase) |
| `haipipe-application-draft` as artifact generator | `3-build-deploy/haipipe-application-artifact` (verb stays `draft`) |
| spine `seed → pitch → [venue] → claims → ... → minimap` | `seed → 1a-1d ladder → [venue] → pitch → narrative → display → section-edit` |
| flat `0-lifecycle/N-stage.md` files | stage FOLDERS `0-lifecycle/N-stage/` (md + _LOG) |
| per-stage `_PROBE/PPNN_*.md` cards; `1-probe-plans/README.md` index; `/haipipe-probe plan from-need` | flat pool `1-probes/PPNN_<topic>.md` (one file per TOPIC, one SECTION per question, states `planned\|commissioned\|answered\|read\|answered-local\|failed`); `/haipipe-application probe "<q>"` raises a section + `probe run` |
| verdict word `confirmed`; PP-card `## Verdict` / G1-G2-G3 | claim status `supported \| weak \| GAP` in `0-lifecycle/1c-claims/1c-claims.md` (no `## Verdict`, no gate) |
| `applications/ask/<NN>/` case files | dead history: nothing reads, nothing writes |
| stage folder `1-claims/` (single stage-1 ledger) | the ladder `1a-descriptions/ 1b-themes/ 1c-claims/ 1d-advice/` (SOP-ladder-restage, 2026-07-09); legacy interventions: `enter` offers the confirm-gated one-shot migration (rename to `1c-claims/`, scaffold rungs, re-file probes by shape) on next open |
| `1d-principles` / `haipipe-application-principles` / `P<n>` ids / maturity `principled` (hours-old, same restage) | `1d-advice` / `haipipe-application-advice` / `A<n>` / `advised` (JL ruling 2026-07-09: advice = counsel downstream stages adopt or decline; `principles` survives only as a verb alias) |
