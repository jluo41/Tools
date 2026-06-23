probe — Agent Roster
======================

Three agents forming the orchestrator / creator / reviewer triad.
The orchestrator is the dispatch target for cross-layer calls
(/haipipe-paper, /haipipe-application). Creator produces artifacts.
Reviewer evaluates at every stage + runs the merged Judge gates.

```
haipipe-probe-orchestrator-agent   🎯 ORCHESTRATE — dispatch target, coordinates lifecycle
haipipe-probe-creator-agent        🤖 CREATE      — produces probe.yaml, evidence_refs, evidence.md
haipipe-probe-reviewer-agent       🔍 REVIEW      — quality gates + Judge G1/G2/G3 (merged)
```

Orchestrator dispatches creator + reviewer in loops. Creator never
reviews. Reviewer never creates. They loop until reviewer says pass.


The 5-stage lifecycle
---------------------

```
Stage 1: PLAN      creator writes probe.yaml       → reviewer checks plan
Stage 2: GATHER    creator calls/links evidence     → reviewer checks completeness
                     └── dispatches task-orchestrator for task work
Stage 3: READ      creator writes evidence.md       → (reviewer optional)
Stage 4: JUDGE     reviewer runs G1+G2+G3           → verdict.md
Stage 5: DEPOSIT   user confirms                    → deposit.md
```


Cross-layer dispatch
--------------------

```
/haipipe-paper ──▶ probe-orchestrator ──▶ task-orchestrator
                     │                       │
                     ├── probe-creator       ├── task-creator
                     └── probe-reviewer      └── task-reviewer
```


Replaces (retired)
------------------

The unified `haipipe-probe-reviewer-agent` merges 3 agents that were
previously separate:

```
RETIRED                              MERGED INTO
probe-structural-reviewer-agent  →  haipipe-probe-reviewer-agent (G1)
probe-integrity-auditor-agent    →  haipipe-probe-reviewer-agent (G2)
claim-verifier-agent             →  haipipe-probe-reviewer-agent (G3)
```

Benefits: one dispatch instead of three, full cross-gate context,
consistent naming with the task layer pattern.


Knowledge home
--------------

Agents are THIN pointers — judgment logic lives in its canonical home:

```
lifecycle steps + gates       → ../fn/{plan,gather,read,judge,deposit}.md
confound walk                 → ../ref/probe-caveats-checklist.txt
probe.yaml verdict schema     → ../ref/probe-yaml-schema.md
```


Registration
------------

Real files live here (toolkit source of truth). `.claude/agents/` holds
copies so each is callable as a `subagent_type` by the harness.
