---
name: haipipe-narrative
description: "Story layer (N_narrative) — the ARGUE layer in the DO/CLAIM/ARGUE pyramid. 6-stage lifecycle: Idea → Discovery → [Probes&Tasks → Insights → Fill → Ignite]* → Handoff. Owns ALL E_insight filing (sole writer). Reads tasks + probes, curates what becomes permanent knowledge, judges when the story is ready. Handoff → F_paper + G_application. Trigger: narrative, story, angle, ignite, what story, sell this, which claims, gap, /haipipe-narrative."
argument-hint: "[verb] [args...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill, Workflow
metadata:
  version: "2.0.0"
  last_updated: "2026-06-11"
  summary: "Story layer — 6-stage lifecycle, ARGUE layer of DO/CLAIM/ARGUE pyramid."
  changelog:
    - "1.0.0 (2026-05-31): baseline — scope A (narrative as first-class citizen, 4 manual verbs)."
    - "2.0.0 (2026-06-11): 6-stage lifecycle (Idea/Discovery/Probes&Tasks/Insights/Fill/Ignite + Handoff). Narrative owns ALL E_insight filing. A_discover integration. Batch probes per round. Three-layer pyramid model (DO/CLAIM/ARGUE)."
---

Skill: haipipe-narrative (story layer — ARGUE)
=================================================

The **ARGUE layer** in the three-layer research pyramid.

```
📖 ARGUE   (narrative)     "why does this matter?"     months    ← THIS SKILL
📊 CLAIM   (probe)         "does the hypothesis hold?" weeks
💼 DO      (task)          "did this run work?"        hours
```

Tasks produce evidence. Probes produce verdicts. The narrative decides
what's worth filing as permanent knowledge and when the story is ready.

See **MENTAL_MODEL.md** for the full three-layer pyramid model.

```
   🧠 KB (facts)  ⇄[🔥 ignite]⇄  📖 N_narrative (story)
   probes/ tasks/                  narratives/<NN>_<slug>/
```

- KB → Narrative (induction): a probe's claim ignites a story angle.
- Narrative → KB (deduction): a story's GAP says which probe to crack next.


NOT to be confused with narrative-report
=========================================

```
N_narrative (THIS) = living story, mutates, ⇄ double arrow with KB
F_paper/narrative-report = one-shot snapshot: freeze a ready story → paper contract
```

1 narrative : N papers. Strictly upstream → downstream.


Commands
--------

```
/haipipe-narrative                          dashboard (list narratives + ignite state)
/haipipe-narrative <narrative>              full lifecycle (all 6 stages + loop)
/haipipe-narrative <narrative> --auto       autonomous mode (batch probes, auto-fill)

/haipipe-narrative idea <slug>              Stage 1 only (create story.md)
/haipipe-narrative discovery <narrative>    Stage 2 only (A_discover landscape)
/haipipe-narrative probes <narrative>       Stage 3 only (spawn probes for GAPs)
/haipipe-narrative insights <narrative>     Stage 4 only (harvest → file DIKW)
/haipipe-narrative fill <narrative>         Stage 5 only (check claims ledger)
/haipipe-narrative ignite <narrative>       Stage 6 only (judge readiness)
/haipipe-narrative handoff <narrative>      render → F_paper + G_application

/haipipe-narrative status [<id>]            read-only overview
/haipipe-narrative "<natural language>"     infer, dispatch
```


Six-Stage Lifecycle + Loop
----------------------------

Orchestrated by `ref/narrative-lifecycle.workflow.js`.

```
Stage 1: IDEA — "what story are we telling?"
  🧑 human writes angle + why matters + core claim
  creates: narratives/<NN>_<slug>/story.md

Stage 2: DISCOVERY — "what does the world know?"
  A_discover 3_review (landscape) + 4_idea novelty-check
  updates: story.md (sharpen angle)
  creates: claims.md (skeleton: needed K cards from landscape)

─── THE LOOP (stages 3-6 repeat until ignite = YES) ───────

Stage 3: PROBES & TASKS — "do the work" (batch)
  for each GAP from Fill:
    A_discover filter first:
      ✅ lit confirms → straight to Insights (file lit-K)
      ❓ lit silent → spawn CLAIM lifecycle (D_probe, weeks)
        → which spawns DO lifecycles (C_task, hours)

Stage 4: INSIGHTS — "harvest what we learned → file DIKW"
  read completed tasks → file 🟦 D + 🟩 I (per-task level)
  read confirmed probes → file 🟦 D + 🟩 I + 🟨 K + 🟧 W (per-probe level)
  sole writer to E_insight (tasks + probes never touch insights/)

Stage 5: FILL — "check what's filled vs missing"
  read insights/ (now current)
  update claims.md: have / weak / GAP per slot
  remaining GAPs → next round's batch size

Stage 6: IGNITE — "is the story ready?"
  all claims have? confidence ok? angle sharp?
  steelman: argue NOT ready
  YES → exit loop → Handoff
  NO  → back to Stage 3 (remaining GAPs become next batch)

─── END LOOP ──────────────────────────────────────────────

HANDOFF — render the story into outputs
  → F_paper scaffold (venue-specific)
  → G_application report / message / ui
  → decision-tree.md finalized
```


The Loop — Batch Probes per Round
-----------------------------------

Fill determines the batch size. Each round probes ALL current GAPs in parallel
(they're independent — different claims, different arms):

```
Round 1: Fill finds 3 GAPs → spawn 3 probes → Insights → Fill → Ignite: NO
Round 2: Fill finds 1 GAP  → spawn 1 probe  → Insights → Fill → Ignite: YES → Handoff
```

The batch shrinks naturally. No serial vs batch config needed.


Where narratives live (project-level)
======================================

```
examples/<PROJECT_ID>/
├── narratives/                   📖 N_narrative manages this
│   ├── INDEX.md                  (auto: all narratives + ignite status)
│   ├── 01_<slug>/                folder-per-narrative (2-digit, no gap)
│   │   ├── story.md              angle + why-it-matters + core claim
│   │   ├── claims.md             K cards needed (BY REFERENCE) + GAP/weak
│   │   ├── ignite-log.md         append-only "am I ignited?" judgments
│   │   └── decision-tree.md      section paths A/B/C/D
│   └── 02_<slug>/
│
├── tasks/                        💼 DO evidence (metrics.json)
├── probes/                       📊 CLAIM verdicts (probe.yaml)
├── insights/                     🧠 KB (narrative writes here)
├── paper/                        📰 F_paper (Handoff → here)
└── applications/                 💬 G_application (Handoff → here)
```


Hard rules
-----------

- NO code, no notebooks, no plots in narratives/. Pure markdown.
- `claims.md` references K cards BY ID, never copies.
- Narrative is the SOLE E_insight writer (Insights stage).
- Tasks and probes NEVER touch insights/ — narrative harvests their results.
- 1 narrative : N papers. Papers back-ref via `papers:` in story.md.


Function verb map
------------------

```
idea, new, create, start, angle, story           → idea (Stage 1)
discover, landscape, literature, novelty          → discovery (Stage 2)
probes, tasks, work, spawn, do, run               → probes (Stage 3)
insights, harvest, file, DIKW, knowledge          → insights (Stage 4)
fill, check, claims, gaps, what's missing         → fill (Stage 5)
ignite, ready?, sellable?, fire, publish?         → ignite (Stage 6)
handoff, ship, render, paper, application         → handoff
status, list, dashboard, overview                 → status (read-only)
```


Interfaces
-----------

```
calls:    A_discover     landscape + lit filter (Discovery + Probes&Tasks)
          D_probe        spawn probe lifecycles (Probes & Tasks)
          E_insight      file DIKW cards (Insights — sole writer)
reads:    tasks/         metrics.json, runtime.yaml (for Insights)
          probes/        probe.yaml result + claim (for Insights)
          insights/      K + W cards (for Fill)
writes:   narratives/    story, claims, ignite-log, decision-tree
          insights/      D + I + K + W cards (via E_insight agents)
feeds:    F_paper        (Handoff → paper scaffold)
          G_application  (Handoff → report / message / ui)
```


Schema authority
-----------------

Every file under `narratives/` MUST conform to `ref/narrative-schema.md`.


Specialist tail
----------------

```
status:    ok | blocked | failed | converged | budget_exhausted
summary:   2-3 sentences (what narrative, what changed, ignite verdict)
artifacts: [paths created / updated]
rounds:    N (how many Map→Fill→Ignite rounds)
next:      suggested next command
```
