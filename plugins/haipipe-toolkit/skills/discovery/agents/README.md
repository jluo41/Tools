discovery — Agent Roster
=========================

Three agents forming the orchestrator / creator / reviewer triad,
plus one Haiku-tier mechanical worker for search fan-out.
The orchestrator is the dispatch target for cross-layer calls
(probe-orchestrator dispatches during Gather when external evidence
is needed). Creator produces artifacts. Reviewer evaluates.

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
```


The 3 types (Axis 2)
---------------------

```
Search (source)    search + read → sources.md, notes.md
Review (analyze)   judge claim → verdict.md, or synthesize field → landscape.md
Idea (generate)    generate novel angles → ideas.md
```


Cross-layer dispatch
--------------------

```
probe-orchestrator ──▶ discovery-orchestrator
                         │
                         ├── discovery-creator
                         └── discovery-reviewer
```

Discovery-orchestrator is dispatched during probe Gather when the
probe needs external evidence (literature, outside claims, field
landscape). It returns terminal files that the probe creator links.


Registration
------------

Real files live here (toolkit source of truth). `.claude/agents/` holds
symlinks to these files so each is callable as a `subagent_type` by the
harness.
