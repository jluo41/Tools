---
name: haipipe-narrative
description: "Story layer (narrative) — the outer sandwich in the Narrative/Probe/Discovery/Task stack. Narrative-open defines the story and claim gaps; Probe sandwiches run underneath and may dispatch discoveries plus tasks; Narrative-post reads probe verdicts, fills the claims ledger, and decides ignite/handoff. Insights/insight are deferred. Trigger: narrative, story, angle, ignite, what story, sell this, which claims, gap, /haipipe-narrative."
argument-hint: "[verb] [args...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill, Workflow
metadata:
  version: "2.2.0"
  last_updated: "2026-06-19"
  summary: "Story layer — outer sandwich over Probe/Discovery/Task; insights deferred."
  changelog:
    - "1.0.0 (2026-05-31): baseline — scope A (narrative as first-class citizen, 4 manual verbs)."
    - "2.0.0 (2026-06-11): 6-stage lifecycle (Idea/Discovery/Probes&Tasks/Insights/Fill/Ignite + Handoff). Narrative owns ALL insight filing. discover integration. Batch probes per round. Three-layer pyramid model (DO/CLAIM/ARGUE)."
    - "2.1.0 (2026-06-19): focus core stack on Narrative/Probe/Task. Narrative becomes outer sandwich; Insights/insight deferred."
    - "2.2.0 (2026-06-19): add discoveries/ as external-evidence work, sibling to tasks/ and referenced by probes."
---

Skill: haipipe-narrative (story layer — ARGUE)
=================================================

The **ARGUE layer** in the three-layer research pyramid.

```
📖 ARGUE   (narrative)     "why does this matter?"     months    ← THIS SKILL
📊 CLAIM   (probe)         "does the hypothesis hold?" weeks
💼 DO      (task)          "did this run work?"        hours
```

Discoveries produce external evidence. Tasks produce internal execution
artifacts. Probes produce verdicts. The narrative decides which verdicts fill
the story gaps and when the story is ready.

See **MENTAL_MODEL.md** for the full three-layer pyramid model.

```
   probes/ + discoveries/ + tasks/ ⇄[ignite]⇄  narrative (story)
   claim verdicts                                 narratives/<NN>_<slug>/
```

- Probe verdicts → Narrative (induction): external/internal evidence fills or weakens a claim slot.
- Narrative → Probe (deduction): a story GAP becomes a probe contract.

Insights/insight are intentionally parked while this core stack is shaped.


Simple Mental Model
====================

Use the stack as one outer sandwich with smaller sandwiches inside:

```
Narrative-open
  "What story do we want to tell, and what evidence is missing?"

  Probe-open
    "Which claim would fill one gap, and what evidence would test it?"

    Discovery / Task
      "Check the outside world and/or run our internal work."

  Probe-post
    "Did the task evidence support the claim?"

Narrative-post
  "Which closed probe verdicts now belong in the story?"
```

The operating rule:

```
Narrative opens the problem.
Probe opens the claim.
Discoveries check outside evidence.
Tasks run internal work.
Probe closes the claim.
Narrative closes or reopens the story.
```

So a normal use looks like:

1. Start with `/haipipe-narrative open <slug>` to write the story angle and claim gaps.
2. Run `/haipipe-narrative probes <narrative>` to turn current gaps into probe sandwiches.
3. Let each probe dispatch discoveries and/or task contracts; both run independently.
4. Run `/haipipe-probe post <probe>` after required evidence artifacts exist.
5. Run `/haipipe-narrative post <narrative>` to fill claims and decide ignite vs another round.

Discovery output is outside-world evidence. Task output is internal-run
evidence. Probe output is a claim verdict. Narrative output is the story
decision.


NOT to be confused with narrative-report
=========================================

```
narrative (THIS) = living story, mutates, reads probe verdicts
paper/narrative-report = one-shot snapshot: freeze a ready story → paper contract
```

1 narrative : N papers. Strictly upstream → downstream.


Commands
--------

```
/haipipe-narrative                          dashboard (list narratives + ignite state)
/haipipe-narrative <narrative>              full outer sandwich + loop
/haipipe-narrative <narrative> --auto       autonomous mode (batch probes, auto-fill)

/haipipe-narrative open <slug|id>           Narrative-open: idea + discovery + gap plan
/haipipe-narrative probes <narrative>       Middle stack: spawn probes for GAPs
/haipipe-narrative post <narrative>         Narrative-post: fill + ignite after probes close
/haipipe-narrative idea <slug>              Open substage: create story.md
/haipipe-narrative discovery <narrative>    Open substage: discover landscape
/haipipe-narrative fill <narrative>         Post substage: check claims ledger from probe verdicts
/haipipe-narrative ignite <narrative>       Post substage: judge readiness
/haipipe-narrative handoff <narrative>      render → paper + application

/haipipe-narrative status [<id>]            read-only overview
/haipipe-narrative "<natural language>"     infer, dispatch
```


Outer Sandwich Lifecycle + Loop
--------------------------------

Orchestrated by `ref/narrative-lifecycle.workflow.js`.

```
NARRATIVE-OPEN A: IDEA — "what story are we telling?"
  🧑 human writes angle + why matters + core claim
  creates: narratives/<NN>_<slug>/story.md

NARRATIVE-OPEN B: DISCOVERY / GAP PLAN — "what would make this story true?"
  discover 3_review (landscape) + 4_idea novelty-check
  updates: story.md (sharpen angle)
  creates: claims.md (claim slots + GAP/weak/have ledger)

─── THE LOOP repeats until ignite = YES ───────

MIDDLE STACK: PROBES, DISCOVERIES & TASKS — "settle the current gaps" (batch)
  for each GAP from Fill:
    discover filter first:
      ✅ lit confirms → mark slot as literature-supported
      ❓ lit silent → spawn CLAIM lifecycle (probe, weeks)
        → which may spawn discoveries/ external evidence work
        → which may spawn tasks/ internal execution work

NARRATIVE-POST A: FILL — "which claim slots are now filled?"
  read closed probes directly (probe.yaml result + claim + verdict sidecars)
  update claims.md: have / weak / GAP per slot
  remaining GAPs → next round's batch size

NARRATIVE-POST B: IGNITE — "is the story ready?"
  all claims have? confidence ok? angle sharp?
  steelman: argue NOT ready
  YES → exit loop → Handoff
  NO  → back to Stage 3 (remaining GAPs become next batch)

─── END LOOP ──────────────────────────────────────────────

HANDOFF — render the story into outputs
  → paper scaffold (venue-specific)
  → application report / message / ui
  → decision-tree.md finalized
```


The Loop — Batch Probes per Round
-----------------------------------

Fill determines the batch size. Each round probes ALL current GAPs in parallel
(they're independent — different claims, different arms):

```
Round 1: Fill finds 3 GAPs → spawn 3 probes → Fill → Ignite: NO
Round 2: Fill finds 1 GAP  → spawn 1 probe  → Fill → Ignite: YES → Handoff
```

The batch shrinks naturally. No serial vs batch config needed.


Where narratives live (project-level)
======================================

```
examples/<PROJECT_ID>/
├── narratives/                   📖 narrative manages this
│   ├── INDEX.md                  (auto: all narratives + ignite status)
│   ├── 01_<slug>/                folder-per-narrative (2-digit, no gap)
│   │   ├── story.md              angle + why-it-matters + core claim
│   │   ├── claims.md             K cards needed (BY REFERENCE) + GAP/weak
│   │   ├── ignite-log.md         append-only "am I ignited?" judgments
│   │   └── decision-tree.md      section paths A/B/C/D
│   └── 02_<slug>/
│
├── _haipipe/                     🧭 single project log/status/site
│   ├── project.log.jsonl
│   ├── project.status.yaml
│   └── project.site.md
├── discoveries/                  🔍 external evidence (sources/notes/verdict)
├── tasks/                        💼 internal DO evidence (metrics.json)
├── probes/                       📊 CLAIM verdicts (probe.yaml)
├── insights/                     🧠 deferred export layer (parked for now)
├── paper/                        📰 paper (Handoff → here)
└── applications/                 💬 application (Handoff → here)
```

Discovery package schema authority:
`discover/haipipe-discover/ref/discovery-yaml-schema.md`.


Hard rules
-----------

- NO code, no notebooks, no plots in narratives/. Pure markdown.
- `claims.md` references K cards BY ID, never copies.
- Insights/insight are deferred while focusing on the Narrative/Probe/Discovery/Task stack.
- Discoveries, tasks, and probes NEVER write narrative conclusions; narrative reads probe verdicts.
- 1 narrative : N papers. Papers back-ref via `papers:` in story.md.


Function verb map
------------------

```
idea, new, create, start, angle, story           → idea (Stage 1)
discover, landscape, literature, novelty          → discovery (Narrative-open / discovery work)
probes, tasks, discoveries, work, spawn, do, run   → probes (middle stack)
insights, harvest, file, DIKW, knowledge          → deferred export (not core)
fill, check, claims, gaps, what's missing         → fill (Narrative-post)
ignite, ready?, sellable?, fire, publish?         → ignite (Narrative-post)
handoff, ship, render, paper, application         → handoff
status, list, dashboard, overview                 → status (read-only)
```


Interfaces
-----------

```
calls:    discover     landscape + lit filter + durable discoveries/
          probe        spawn probe sandwiches (Probe-open → discoveries/tasks → Probe-post)
reads:    probes/        probe.yaml result + claim + review sidecars (for Fill)
writes:   narratives/    story, claims, ignite-log, decision-tree
          _haipipe/      project.log.jsonl events for orchestration steps
feeds:    paper        (Handoff → paper scaffold)
          application  (Handoff → report / message / ui)
deferred: insight      optional export layer, outside current N/P/T core
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
