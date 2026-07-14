---
name: haipipe-application-iterate
description: "Post-deploy iteration for the intervention lifecycle. Ingests A/B test results, engagement metrics, or user feedback and routes findings back into the lifecycle for refinement. Opens a new round with performance data and triages to claims/pitch/display/artifact. Trigger: iterate, A/B results, performance review, refine, /haipipe-application iterate."
argument-hint: "[intervention-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.2.2"
  last_updated: "2026-07-14"
  summary: "Post-deploy iteration — A/B results, performance, refinement. Paper-alignment sweep: re-homed to 4-iterate/; triage targets on the new spine (design/variants/rationale words retired); ask-kind reference removed. v1.2.0 (probe redesign, Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3 approved JL 2026-07-14): A/B results bearing on a claim raise a question SECTION in 1-probes/ (serves: 1-claims); the settled judgment is the CLAIM's status in 1-claims.md — the probe 'verdict' is retired. v1.2.1: the BODY still said 'the gateway does the work, the PP card carries the verdict' — it dispatched a RETIRED agent to write a RETIRED artifact. Deployment evidence now routes the section's `commission:` block straight to Agent(haipipe-task-orchestrator-agent) / Agent(haipipe-discovery-orchestrator-agent), returns as a QA file the `target:` points at, and settles in 1-claims.md. v1.2.2: the 'Feeding deployment evidence back' topic sentence no longer names the retired evidence GATEWAY — deployment evidence enters through the PROBE phase, the ONE door (the mechanism block below it already said so; the topic sentence had been left on the dead noun)."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-application-iterate
=====================================

Post-deploy iteration. The intervention lifecycle does not end at
deployment — performance data flows back to refine the intervention.


Iteration triggers
===================

```
A/B test results landed       → ingest, compare to success metrics
Engagement metrics available  → check against guardrails
User/clinician feedback       → capture in round
Kill criterion met            → flag for intervention shutdown
```


Workflow
=========

```
Step 1: Open a new round via /haipipe-application round new.
        Source = "A/B results" or "performance review" or "feedback".

Step 2: Ingest performance data into discussion.md.
        - Click-through rates per variant
        - Conversion / adherence rates
        - Opt-out rates
        - Guardrail metrics

Step 3: Compare to the seed's expected impact + kill criteria (0-seed) and
        the pitch's testable goal (2-pitch).
        - Primary met?     → note in decisions.md
        - Guardrail breach? → flag for immediate action
        - Version comparison → identify winner/loser

Step 4: Extract decisions:
        - Drop underperforming artifact versions
        - Adjust timing, tone, or content
        - Add new segments or artifact versions
        - Update claims with real-world evidence

Step 5: Triage decisions to lifecycle stages:
        - "v2 outperformed v1"          → artifact (promote v2, re-draft losers)
        - "48h too early, 24h better"   → pitch (theory of change) or display (element spec)
        - "click rate validates C02"    → claims (GAP → supported, cite the A/B result)
        - "no effect on adherence"      → pitch (re-examine theory) or claims
        - "opt-out rate too high"       → artifact (frequency/tone re-compose)

Step 6: Route to /haipipe-application round triage.

Step 7: If kill criterion met:
        Update STATUS.md maturity = "retired" with reason.
```


Feeding deployment evidence back
==================================

Performance results from real-world deployment are evidence like any other:
they enter the project through the PROBE phase — the ONE door — never through
a side door written from this skill's context.

```
A/B results bear on a claim    → raise a question SECTION in 1-probes/ (serves: 1-claims);
                                 `probe run` MATCHes the bank, then commissions it
Real-world effect size          → same route; the number lands in _VALUES_
Settled judgment                → the CLAIM's status in 1-claims.md (there is no probe
                                 verdict any more — the word is retired)
```

Deployment evidence is dispatched, not filed: the intervention records the
NEED as a question SECTION in `1-probes/PPNN_<topic>.md`, and the PROBE phase
hands that section's `commission:` block, verbatim, straight to
`Agent(haipipe-task-orchestrator-agent)` / `Agent(haipipe-discovery-orchestrator-agent)`
— there is NO probe gateway agent any more (retired 2026-07-14). The answer comes
back as a QA file the section's `target:` points at; the section's `reading:` says
what it MEANS, and the claim's STATUS lands in 1-claims.md (ask-gated per the
copilot policy).


Risk profile
=============

WRITES round files. READ-ONLY on lifecycle artifacts (changes routed
through lifecycle skills); evidence needs leave via the PROBE phase.
