discovery — Agent Roster
=========================

Three agents forming the orchestrator / creator / reviewer triad,
plus one Haiku-tier mechanical worker for search fan-out.
The orchestrator is THE dispatch target for every discovery-shaped
commission — a consumer's PROBE phase calls it DIRECTLY, and its clean
context is the wall. Creator produces artifacts. Reviewer evaluates.

```
haipipe-discovery-orchestrator-agent   🎯 ORCHESTRATE — dispatch target, coordinates lifecycle
haipipe-discovery-creator-agent        🤖 CREATE      — searches, reads, analyzes, generates ideas
haipipe-discovery-reviewer-agent       🔍 REVIEW      — sources real? verdict grounded? ideas novel?
haipipe-discovery-search-worker-agent  ⚡ WORKER      — Haiku; one channel sweep / verify batch per dispatch
```

Orchestrator dispatches creator + reviewer in loops. Creator never
reviews. Reviewer never creates. They loop until reviewer says pass.

The worker is the only agent NOT on `model: inherit` — it is pinned to
Haiku because its job is judgment-free (harvest hits, transcribe
metadata, resolve ids) and fans out wide. Creator (Execute) and
orchestrator (ENRICH) dispatch it in parallel, one job per channel,
then curate and write the ledger themselves. The worker has no
Write/Edit tools — its return text is its entire product; it never
touches the discovery folder.


The lifecycle (uniform across 3 types)
--------------------------------------

```
Stage 1: PLAN      creator writes discovery.yaml   → reviewer checks plan
Stage 2: BUILD     creator authors instrument (opt) → reviewer checks instrument
Stage 3: EXECUTE   creator runs bucket workers      → reviewer checks output
Stage 4: REPORT    creator writes report block      → reviewer checks report
                   + the QA file, when this run     → + the QA-file gate + the
                     answered a question               bank-purity check
```


The 3 types (Axis 2)
---------------------

```
Search (source)    search + read → sources.md, notes.md
Review (analyze)   judge claim → verdict.md, or synthesize field → landscape.md
Idea (generate)    generate novel angles → ideas.md
```


Cross-layer dispatch — DIRECT, and the context is the wall
----------------------------------------------------------

```
📄 a paper/application PROBE phase                  ⚙️ this layer
   holds the question + the STAKE                      never saw a paper
   ("## Why: C6 dies if …")            🧱 WALL
        │                                │
        └── hands ONE commission ────────┴──▶ discovery-orchestrator-agent
            (general language,                    │  runs the qa gate:
             VERBATIM, nothing else)               │  ① QA SCAN ② DIGEST ③ lifecycle
             never ## Why                          ├── discovery-creator   (writes)
             never the probe file                  └── discovery-reviewer  (gates)
             never a PP id                         │
                                                   ▼
        ◀───── returns ONE PATH ──────  discoveries/<leaf>/QA/<n>-<slug>.md
```

The orchestrator's **clean context IS the mechanism**. It is not told who asked
or why, so it cannot shape the evidence around anyone's story — which is exactly
what makes the answer reusable by the next consumer, with a different stake.

💀 RETIRED 2026-07-14: `haipipe-probe-orchestrator-agent` (the probe GATEWAY). It
no longer exists. Its SWEEP became the paper-side MATCH; its dispatch became the
direct `Agent(haipipe-discovery-orchestrator-agent)` call drawn above. And the
`_ASK/` stub bridge went with it: no stub folders, no `answers:` field, no PP ids
anywhere under `discoveries/`. The probe CAUSES a QA file; **the executor AUTHORS
it**. Constitution: `probe/haipipe-probe/SKILL.md` (v8.0.0).


Registration
------------

Real files live here (toolkit source of truth). `.claude/agents/` holds
symlinks to these files so each is callable as a `subagent_type` by the
harness.
