narrative — The Story Layer (DESIGN)
========================================

Status: v2.3.0 (2026-06-20) — narrative as control envelope over Probe/Discovery/Task/Insight;
        paper/application as downstream delivery layers.
Owner:  jluo41
Scope:  narrative lifecycle (Open → [Probe/Discovery/Task/Insight stack → Post]* → Handoff).
        The ARGUE layer in the DO/CLAIM/ARGUE pyramid.


Why this layer exists
=====================

The Probe/Discovery/Task workspace is a pile of work and verdicts. By itself it is
"a heap of outputs nobody sells". The Narrative is the **living story** that
selects a subset of those verdicts and argues "here is the angle, here is why
it matters, here is what I still need to make it sell".

For a concrete end-to-end project shape, see
`../../blueprints/end-to-end-sandwich-run.md`.

```
   probes/ + discoveries/ + tasks/ + insights/ ⇄[ignite]⇄  narrative (story)
   verdicts + synthesis                              story + claims + ignite-log + decision-tree
```


Control Envelope, Not Filesystem Parent
=======================================

Narrative can "contain" Probe, Discovery, Task, and Insight in the control
sense. It should not contain their folders.

```
Narrative Session / Control Envelope
|
|-- Probe contracts
|   |-- Discovery evidence
|   `-- Task evidence
|
`-- Insight synthesis
```

On disk, these remain sibling folders:

```
narratives/
probes/
discoveries/
tasks/
insights/
paper/
applications/
```

The narrative records scope by reference:

```yaml
# narratives/N001_example/status.yaml
scope_refs:
  probes:
    - probes/P001_first-check/probe.yaml
  discoveries:
    - discoveries/P01_first-check/01_prior-art/discovery.yaml
  tasks:
    - tasks/T001_baseline/status.yaml
  insights:
    - insights/I001_candidate-lift/insight.yaml
```

Paper and application are downstream delivery layers. They are outside the
narrative folder but inside the narrative session's control scope once the
narrative reaches Handoff.


The Three-Layer Pyramid
========================

See **MENTAL_MODEL.md** (sibling file) for the full three-layer model.

```
📖 ARGUE   (narrative)     "why does this matter?"     weeks–months
📊 CLAIM   (probe)         "does the hypothesis hold?" days–weeks
🔍 FIND    (discovery)     "what does the world know?" hours–days
💼 DO      (task)          "did this run work?"        hours

ARGUE opens N × CLAIM contracts; each CLAIM opens N × FIND/DO contracts and
may produce N × Insight summaries after Probe-post. The narrative is the
outermost sandwich and session control envelope.
```

Key principle: **discoveries produce external evidence, tasks produce internal
evidence, probes produce verdicts, insights produce reusable synthesis, and
the narrative decides which verdicts and insights fill the story.**


CRITICAL: two "narratives" — do not confuse them
=================================================

```
narrative/  (THIS layer)                paper/1-narrative/narrative-report (exists)
─────────────────────────────             ───────────────────────────────────────────
the living story, runs the whole time     a one-shot snapshot: the paper's design contract
⇄ double arrow with KB; holds ignite      one-way downstream: KB → it → paper
1 narrative : N papers                    "one narrative per paper"
lives in examples/<proj>/narratives/      emits NARRATIVE_REPORT.md beside the paper
the NOUN (the story itself)               the ACT of freezing a story into a paper contract
```


The Outer Sandwich Lifecycle + Loop
====================================

```
1. 💡 Idea             what story are we telling?              ┐ NARRATIVE-OPEN
2. 🔍 Discovery        what would make it true?                ┘
3. 📊 Probes + Evidence settle current GAPs (batch)        ┐
4. 🧠 Insight          synthesize reusable meaning         │
5. 📋 Fill             check claims: have / weak / GAP     │  NARRATIVE-POST
6. 🔥 Ignite           is the story ready? steelman        │
                        YES → Handoff                      │
                        NO  → back to Probes + Evidence ───┘

🚀 Handoff             render → paper + application     (after ignite=YES)
```


Stage Details
==============

**Stage 1: 💡 Idea** — what story are we telling?

```
creates:  narratives/<NN>_<slug>/story.md
          angle + why it matters + core claim
mode:     🧑 human only (the angle is an editorial decision)
```


**Stage 2: 🔍 Discovery** — what does the world know?

```
calls:    discover 3_review (landscape survey)
          discover 4_idea novelty-check (is angle novel?)
updates:  story.md (sharpen angle based on landscape)
creates:  claims.md (claim slots + GAP/weak/have ledger)
```


**Stage 3: 📊 Probes + Evidence** — settle current gaps (batch)

```
reads:    claims.md GAP/weak rows from previous Fill
batch:    ALL current GAPs in parallel (batch size = number of GAPs)
per GAP:
  🔍 discover filter first:
    ✅ lit confirms → mark slot as literature-supported (no probe)
    ❌ lit contradicts → revise claim or angle
    ❓ lit silent → spawn CLAIM lifecycle:
       📊 probe: Probe-open → discoveries/tasks → Probe-post
         dispatches: 🔍 discoveries/ for outside evidence
         dispatches: 💼 tasks/ for Plan → Build → Execute → Report
writes:   probe.yaml result/claim/verdict sidecars;
          discovery sources stay in discoveries/; task metrics stay in tasks/
```


**Stage 4: 🧠 Insight** — make the verdict reusable

```
reads:    closed probe verdict
          discovery verdicts
          task reports / metrics
writes:   insights/<ID>/insight.yaml
          insights/<ID>/site.md
          insights/<ID>/caveats.md
purpose:  turn "supported_with_caveats" into reusable claim wording,
          caveats, and narrative implications.
```


**Stage 5: 📋 Fill** — check what's filled vs what's missing

```
reads:    closed probes directly:
          probe.yaml result + claim
          review.md
          INTEGRITY_AUDIT.md
          CLAIMS_FROM_RESULTS.md
          insights/<ID>/insight.yaml when present
updates:  claims.md ledger: have / weak / GAP per slot
creates:  Claim Gap Contracts for remaining GAP/weak rows
output:   count of remaining GAPs → next round's batch size
```


**Stage 6: 🔥 Ignite** — is the story ready?

```
checks:   all claims have? confidence ≥ threshold? angle still sharp?
steelman: argue NOT ready — what's the weakest link?
creates:  ignite-log.md entry (append-only, honest YES/NO + why + next)
verdict:
  YES → Handoff (all claims filled, story coherent)
  NO  → back to Stage 3 (remaining GAPs become next batch)
```


**🚀 Handoff** — render the story into outputs (after ignite=YES)

```
→ 📰 paper           snapshot narrative → paper scaffold (venue-specific)
→ 💬 application     stakeholder report / patient message / UI
→ decision-tree.md     finalize section spine
creates:  paper/<Venue>/, applications/*
```


The Loop — Batch Probes per Round
===================================

Fill determines the batch size. Each round probes ALL current GAPs in parallel:

```
Round 1:
  Fill finds 3 GAPs (C2, C3, C4)
  → Probes + Evidence spawns 3 probes in parallel (they're independent)
  → Fill reads the closed probe verdicts
  → Fill rechecks: C2 have, C3 have, C4 still weak
  → Ignite: NO (C4 weak)

Round 2:
  Fill finds 1 GAP (C4)
  → Probes + Evidence spawns 1 probe
  → Fill reads the closed probe verdict
  → Fill rechecks: all have
  → Ignite: YES → Handoff
```

The batch shrinks naturally each round. No need for serial vs batch mode —
Fill tells you how many GAPs remain.


File Schemas
=============

Project-level orchestration files live in `_haipipe/`:

```
_haipipe/
├── project.log.jsonl      single append-only event log
├── project.status.yaml    current project snapshot
└── project.site.md        human-readable project dashboard
```

Discovery packages follow
`discover/haipipe-discover/ref/discovery-yaml-schema.md`.

Four files per narrative — canonical spec in `haipipe-narrative/ref/narrative-schema.md`:

```
narratives/<NN>_<slug>/
├── story.md          angle + why-it-matters + core claim (status: exploring→igniting→ready→shelved)
├── claims.md         claim slots + have/weak/GAP ledger + Claim Gap Contracts
├── ignite-log.md     append-only round-trip judgments (ignited? YES/NO + why + next)
└── decision-tree.md  section paths A/B/C/D; chosen spine ties them together
```

Recommended session file:

```
narratives/<NN>_<slug>/
└── copilot.md        current narrative session frame: open gap, latest probe,
                      latest insight, recommended next action, guardrails
```

Hard rules (mirror insight discipline):
- NO code, no notebooks, no plots. Pure markdown.
- `claims.md` references K cards BY ID, never copies.
- 1 narrative : N papers. Papers back-ref via `papers:` in story.md.
- Do not put `probes/`, `discoveries/`, `tasks/`, `insights/`, `paper/`, or
  `applications/` inside a narrative folder. The narrative owns their scope by
  reference, not by filesystem containment.


Interfaces
==========

```
reads:    probes/      probe.yaml result + claim + review sidecars (for Fill)
          insights/    reusable synthesis + caveats (for Fill/Ignite)
calls:    discover   landscape + novelty + durable discoveries/
          probe      spawn probe sandwiches (Probe-open → discoveries/tasks → Probe-post)
          task       (via probe bridge, not directly)
          insight    draft synthesis after Probe-post when evidence is meaningful
writes:   narratives/<NN>_<slug>/*  (story, claims, ignite-log, decision-tree)
          _haipipe/project.log.jsonl (orchestration events)
feeds:    paper       (when status=ready → narrative-report → paper)
          application (when status=ready → report / message / ui)
```


Decision Log
=============

2026-05-30  Created: DESIGN.md v1.0.0 (scope A — narrative as first-class citizen, manual only).
2026-06-11  Upgraded: DESIGN.md v2.0.0 — 6-stage lifecycle (Idea/Discovery/Probes&Tasks/Insights/Fill/Ignite)
            with loop. Narrative owns ALL insight filing (removed from task and probe lifecycles).
            discover integrated at Discovery + Probes&Tasks (literature filter). Batch probes per round
            (Fill determines batch size). Handoff → paper + application (not just paper).
2026-06-19  Superseded: v2.0 insight ownership parked. Core focus is Narrative/Probe/Discovery/Task:
            Narrative-open defines story gaps, Probe sandwiches settle them via discoveries/tasks, Narrative-post reads
            probe verdicts directly for Fill/Ignite. At this point, insight was treated as a deferred export layer.
2026-06-20  Clarified: narrative is a control envelope, not a filesystem parent. Probe/Discovery/Task/Insight
            are inside narrative scope by reference. Paper/Application stay downstream delivery layers.
