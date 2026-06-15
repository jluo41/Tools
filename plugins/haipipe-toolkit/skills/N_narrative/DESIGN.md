N_narrative — The Story Layer (DESIGN)
========================================

Status: v2.0.0 (2026-06-11) — 6-stage lifecycle + loop; narrative owns E_insight filing;
        A_discover integration; batch probes per round.
Owner:  jluo41
Scope:  narrative lifecycle (Idea → Discovery → [Probes&Tasks → Insights → Fill → Ignite]* → Handoff).
        The ARGUE layer in the DO/CLAIM/ARGUE pyramid.


Why this layer exists
=====================

The KB (probes/ + tasks/ + insights/) is a pile of facts. By itself it is
"a heap of cards nobody sells". The Narrative is the **living story** that
selects a subset of those facts and argues "here is the angle, here is why
it matters, here is what I still need to make it sell".

```
   🧠 KB (facts)  ⇄[🔥 ignite]⇄  📖 N_narrative (story)
   probes/ tasks/                  narratives/<NN>_<slug>/
   insights (D/I/K/W)              story + claims + ignite-log + decision-tree
```


The Three-Layer Pyramid
========================

See **MENTAL_MODEL.md** (sibling file) for the full three-layer model.

```
📖 ARGUE   (narrative)     "why does this matter?"     weeks–months
📊 CLAIM   (probe)         "does the hypothesis hold?" days–weeks
💼 DO      (task)          "did this run work?"        hours

ARGUE contains N × CLAIM contains N × DO
The narrative is the outermost loop.
```

Key principle: **tasks produce evidence, probes produce verdicts, the narrative
decides what's worth filing as permanent knowledge.** E_insight filing lives
ONLY in the narrative's Insights stage — not in task or probe lifecycles.


CRITICAL: two "narratives" — do not confuse them
=================================================

```
N_narrative/  (THIS layer)                F_paper/1-narrative/narrative-report (exists)
─────────────────────────────             ───────────────────────────────────────────
the living story, runs the whole time     a one-shot snapshot: the paper's design contract
⇄ double arrow with KB; holds ignite      one-way downstream: KB → it → paper
1 narrative : N papers                    "one narrative per paper"
lives in examples/<proj>/narratives/      emits NARRATIVE_REPORT.md beside the paper
the NOUN (the story itself)               the ACT of freezing a story into a paper contract
```


The 6-Stage Lifecycle + Loop
==============================

```
1. 💡 Idea             what story are we telling?              (one-time)
2. 🔍 Discovery        what does the world know?              (one-time)
3. 📊 Probes & Tasks   do the work (batch of GAPs)        ┐
4. 🧠 Insights         harvest → file DIKW to E_insight    │  THE LOOP
5. 📋 Fill             check claims: have / weak / GAP     │
6. 🔥 Ignite           is the story ready? steelman        │
                        YES → Handoff                      │
                        NO  → back to Probes & Tasks  ─────┘

🚀 Handoff             render → F_paper + G_application     (after ignite=YES)
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
calls:    A_discover 3_review (landscape survey)
          A_discover 4_idea novelty-check (is angle novel?)
updates:  story.md (sharpen angle based on landscape)
creates:  claims.md (skeleton: needed K cards identified from landscape)
```


**Stage 3: 📊 Probes & Tasks** — do the work (batch)

```
reads:    claims.md GAP/weak rows from previous Fill
batch:    ALL current GAPs in parallel (batch size = number of GAPs)
per GAP:
  🔍 A_discover filter first:
    ✅ lit confirms → file lit-sourced K in Insights (no probe)
    ❌ lit contradicts → revise claim or angle
    ❓ lit silent → spawn CLAIM lifecycle:
       📊 D_probe: Design → Materialize → Harvest → Judge
         contains: 💼 C_task: Plan → Build → Execute → Report
writes:   probe.yaml (verdicts), metrics.json (evidence)
```


**Stage 4: 🧠 Insights** — harvest what we learned → file DIKW

```
reads:    completed tasks (metrics.json, runtime.yaml, report.yaml)
          confirmed probes (probe.yaml result + claim + caveats)
files to E_insight:
  🟦 D_data        per-run observations (from tasks)
  🟩 I_information  cross-run patterns (from tasks)
  🟦 D_data        per-arm observations (from probes)
  🟩 I_information  cross-arm patterns (from probes)
  🟨 K_knowledge    validated claims (from confirmed probes)
  🟧 W_wisdom       actionable next steps (from probes, optional)
agents:   D/I/K/W creator-reviewer pairs from E_insight
          + index-integrity audit
writes:   insights/D_data/, I_information/, K_knowledge/, W_wisdom/
```

The narrative is the SOLE E_insight writer. Tasks and probes produce raw
artifacts; the narrative decides what becomes permanent knowledge.


**Stage 5: 📋 Fill** — check what's filled vs what's missing

```
reads:    insights/ (now up-to-date after Insights stage)
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
→ 📰 F_paper           snapshot narrative → paper scaffold (venue-specific)
→ 💬 G_application     stakeholder report / patient message / UI
→ decision-tree.md     finalize section spine
creates:  paper/<Venue>/, applications/*
```


The Loop — Batch Probes per Round
===================================

Fill determines the batch size. Each round probes ALL current GAPs in parallel:

```
Round 1:
  Fill finds 3 GAPs (C2, C3, C4)
  → Probes & Tasks spawns 3 probes in parallel (they're independent)
  → Insights harvests all completed probes + tasks
  → Fill rechecks: C2 have, C3 have, C4 still weak
  → Ignite: NO (C4 weak)

Round 2:
  Fill finds 1 GAP (C4)
  → Probes & Tasks spawns 1 probe
  → Insights harvests
  → Fill rechecks: all have
  → Ignite: YES → Handoff
```

The batch shrinks naturally each round. No need for serial vs batch mode —
Fill tells you how many GAPs remain.


File Schemas
=============

Four files per narrative — canonical spec in `haipipe-narrative/ref/narrative-schema.md`:

```
narratives/<NN>_<slug>/
├── story.md          angle + why-it-matters + core claim (status: exploring→igniting→ready→shelved)
├── claims.md         needed K cards by reference + have/weak/GAP ledger + Claim Gap Contracts
├── ignite-log.md     append-only round-trip judgments (ignited? YES/NO + why + next)
└── decision-tree.md  section paths A/B/C/D; chosen spine ties them together
```

Hard rules (mirror E_insight discipline):
- NO code, no notebooks, no plots. Pure markdown.
- `claims.md` references K cards BY ID, never copies.
- 1 narrative : N papers. Papers back-ref via `papers:` in story.md.


Interfaces
==========

```
reads:    tasks/       results/<run>/metrics.json (for Insights stage)
          probes/      probe.yaml result + claim (for Insights stage)
          insights/    K_knowledge + W_wisdom (for Fill stage)
calls:    A_discover   landscape + novelty + literature filter (Discovery + Probes&Tasks)
          D_probe      spawn probe lifecycles (Probes & Tasks stage)
          C_task       (via D_probe bridge, not directly)
          E_insight    file DIKW cards (Insights stage — sole writer)
writes:   narratives/<NN>_<slug>/*  (story, claims, ignite-log, decision-tree)
          insights/                 (via E_insight agents in Insights stage)
feeds:    F_paper       (when status=ready → narrative-report → paper)
          G_application (when status=ready → report / message / ui)
```


Decision Log
=============

2026-05-30  Created: DESIGN.md v1.0.0 (scope A — narrative as first-class citizen, manual only).
2026-06-11  Upgraded: DESIGN.md v2.0.0 — 6-stage lifecycle (Idea/Discovery/Probes&Tasks/Insights/Fill/Ignite)
            with loop. Narrative owns ALL E_insight filing (removed from C_task and D_probe lifecycles).
            A_discover integrated at Discovery + Probes&Tasks (literature filter). Batch probes per round
            (Fill determines batch size). Handoff → F_paper + G_application (not just paper).
