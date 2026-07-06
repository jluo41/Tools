# Intervention Lifecycle

The intervention lifecycle is the stage spine for application
deliverables. Uses the **same stage vocabulary** as the paper
lifecycle (paper/ref/paper-lifecycle.md). The venue profile
determines which stages fire.


Stage spine
============

```
Stage 0  seed         "why might this intervention work?"
Stage 1  pitch        "what is this intervention trying to achieve?"
(venue)               pinned in STATUS.md — reshapes everything downstream
Stage 2  claims       "which K/W entries inform this?" (light)
                      "what must be true for this to work?" (full)
Stage 3  narrative    "how do claims compose into a coherent arc?"
Stage 4  display      "what content element carries each claim?"
Stage 5  minimap      "what job does each piece of the output do?"
───────  draft        "realize the output as deployable artifact"
───────  review       "audience fit + claim traceability"
───────  round        "stakeholder/clinician feedback"
───────  iterate      "A/B results → refine"
───────  deploy       "ship to channel"
```

Same stage names as paper: seed, pitch, claims, narrative, display,
minimap. The only difference is what each stage produces — that is
determined by the venue.


Stage requirements per venue
==============================

The venue profile declares which stages are required, optional,
or skip. Seed, pitch, and claims are always required.

```
                    seed   pitch   claims   narrative   display   minimap
                    ─────  ─────   ──────   ─────────   ───────   ───────
venue-sms           req    req     req      skip        skip      skip
venue-push          req    req     req      skip        skip      skip
venue-reminder      req    req     req      skip        skip      skip
venue-checklist     req    req     req      optional    skip      skip
venue-email         req    req     req      req         optional  skip
venue-dashboard     req    req     req      req         req       req
venue-ui-card       req    req     req      req         req       optional
venue-report        req    req     req      req         req       req
```

Simple venues (SMS, push, reminder): seed → pitch → claims → draft.
Complex venues (dashboard, report): all 6 stages before draft.


Claims depth per venue
========================

```
claims_depth    venues                     meaning
────────────    ──────────────────────     ────────────────────────────
light           sms, push, reminder        SELECT from existing K/W.
                                           Map K/W to venue template
                                           slots. No probe planning.

medium          checklist, email           SELECT + gap check.
                                           Verify coverage. Optional
                                           probe if gap is load-bearing.

full            dashboard, ui-card,        Full claim ledger.
                report                     GAP/weak/supported per claim.
                                           Probe plans for GAPs.
```


Venue template (simple venues)
================================

For venues that skip narrative/display/minimap, the venue profile
includes a fixed template that replaces those stages:

```yaml
# venue-sms template
template:
  - slot: greeting     ← personalization
  - slot: benefit      ← primary claim (K/W)
  - slot: CTA          ← action claim (W)
  - slot: close        ← reassurance / opt-out
```

The draft skill reads this template directly. No intermediate
lifecycle artifacts needed.


Stage → file mapping
=====================

```
stage        file                            skill
────────     ────────────────────────         ──────────────────────────
seed         0-lifecycle/0-seed.md            haipipe-application-seed
pitch        0-lifecycle/1-pitch.md           haipipe-application-pitch
(venue)      STATUS.md venue: field           haipipe-application-venue
claims       0-lifecycle/2-claims.md          haipipe-application-claims
narrative    0-lifecycle/3-narrative.md       haipipe-application-narrative
display      0-lifecycle/4-display.md         haipipe-application-display
minimap      0-lifecycle/5-minimap.md         haipipe-application-minimap
draft        0-artifacts/<slug>-v{N}.md       haipipe-application-draft
review       0-artifacts/REVIEW-*.md          haipipe-application-review
round        1-rounds/vYYMMDD/               haipipe-application-round
iterate      (via round)                     haipipe-application-iterate
deploy       (channel-specific)              haipipe-application-deploy
```


Maturity ladder
================

Maturity is derived from disk, not declared.

```
maturity             condition
──────────           ───────────────────────────────────
prospect             0-seed.md exists
pitched              1-pitch.md exists
venue-pinned         STATUS.md has venue: <name>
claim-ledger         2-claims.md exists
narrated             3-narrative.md exists (if required by venue)
display-mapped       4-display.md exists (if required by venue)
minimapped           5-minimap.md exists (if required by venue)
drafted              0-artifacts/ has at least one artifact
reviewed             review pass completed
deployed             artifact shipped to channel
iterating            post-deploy round open
retired              kill criterion met; no further work
```

For simple venues, maturity jumps from `claim-ledger` straight to
`drafted` (skipping narrated/display-mapped/minimapped).


Loopback rule
==============

```
symptom                                  → loop back to
─────────────────────────────────────────────────────────
evidence missing for claim               → claims
theory of change wrong                   → pitch
output structure wrong                   → narrative (or venue)
content element doesn't fit              → display
stakeholder review rejects               → round → target stage
A/B test shows no effect                 → pitch or claims
kill criterion met                       → STATUS.md → retired
venue wrong for audience                 → venue (invalidates claims+)
```


Evidence flow (full claims only)
==================================

```
Claim GAP in 2-claims.md
    ↓
Buffer in 1-probe-plans/PP##_*.md
    ↓
/haipipe-probe plan from-intervention
    ↓
probe.Gather():
  ├── task (internal data): cohort HTE, engagement, click rates
  └── discovery (external): literature, benchmarks
    ↓
probe.Judge() → verdict
    ↓
/haipipe-insight files K/W cards
    ↓
Backfill claims → advance to narrative
```

Light claims: no evidence flow — select from existing KB only.


Paper ↔ application comparison
================================

```
paper                     application
─────                     ──────────────
same stage names          same stage names
_venue/ (journal)         _venue/ (output modality)
venue reshapes all        venue reshapes all + skips stages
0-sections/ (TeX)         0-artifacts/ (markdown)
claims always full        claims depth scales with venue
1-rounds/                 1-rounds/
1-probe-plans/            1-probe-plans/ (full depth only)
Paper Console             Intervention Console
compile + submit          review + deploy
rebuttal                  iterate (A/B results)
```


Intervention folder schema
============================

```
applications/interventions/<NN>_<slug>/
├── STATUS.md                          venue, maturity, active round
├── .intervention-console.yaml
├── 0-lifecycle/
│   ├── 0-seed.md                      always
│   ├── 1-pitch.md                     always
│   ├── 2-claims.md                    always (depth varies)
│   ├── 3-narrative.md                 if venue requires
│   ├── 4-display.md                   if venue requires
│   └── 5-minimap.md                   if venue requires
├── 0-artifacts/
│   ├── <slug>-v{N}.md
│   ├── REVIEW-<slug>.md
│   └── CLAIM_AUDIT.md
├── 1-rounds/
│   ├── latest.md
│   └── vYYMMDD/
├── 1-probe-plans/                     full claims only
│   └── PP##_<slug>.md
├── data/
│   └── contract.yaml
└── report.md                          final DIKW-spine summary
```
