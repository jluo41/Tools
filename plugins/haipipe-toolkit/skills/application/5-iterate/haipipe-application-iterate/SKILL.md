---
name: haipipe-application-iterate
description: "Post-deploy iteration for the intervention lifecycle. Ingests A/B test results, engagement metrics, or user feedback and routes findings back into the lifecycle for refinement. Opens a new round with performance data and triages to claims/design/variants. Trigger: iterate, A/B results, performance review, refine, /haipipe-application iterate."
argument-hint: "[intervention-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.0.0"
  last_updated: "2026-06-22"
  summary: "Post-deploy iteration — A/B results, performance, refinement."
  changelog:
    - "1.0.0 (2026-06-22): initial version."
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

Step 3: Compare to success metrics in 5-delivery-plan.md.
        - Primary met?     → note in decisions.md
        - Guardrail breach? → flag for immediate action
        - Variant comparison → identify winner/loser

Step 4: Extract decisions:
        - Drop underperforming variants
        - Adjust timing, tone, or content
        - Add new segments or variants
        - Update claims with real-world evidence

Step 5: Triage decisions to lifecycle stages:
        - "V02 outperformed V01"        → variants (promote V02)
        - "48h too early, 24h better"   → design (update timing)
        - "click rate validates C02"    → claims (GAP → supported)
        - "no effect on adherence"      → rationale (re-examine theory)
        - "opt-out rate too high"       → design (change frequency)

Step 6: Route to /haipipe-application round triage.

Step 7: If kill criterion met:
        Update STATUS.md maturity = "retired" with reason.
```


Integration with insight
==========================

Performance results from real-world deployment can feed back into
the project's KB:

```
A/B results confirm a claim   → file K card via /haipipe-insight
Real-world effect size         → file D card
Unexpected pattern             → file I card
New recommendation             → file W card
```

This is the application → insight write-back path, same as the
ask kind. The iterate skill is authorized to trigger
`/haipipe-insight-*` to file cards from deployment evidence.


Risk profile
=============

WRITES round files. May trigger /haipipe-insight-* to file KB cards
from deployment evidence. READ-ONLY on lifecycle artifacts (changes
routed through lifecycle skills).
