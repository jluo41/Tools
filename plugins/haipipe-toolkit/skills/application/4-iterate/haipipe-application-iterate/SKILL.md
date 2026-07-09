---
name: haipipe-application-iterate
description: "Post-deploy iteration for the intervention lifecycle. Ingests A/B test results, engagement metrics, or user feedback and routes findings back into the lifecycle for refinement. Opens a new round with performance data and triages to claims/pitch/display/artifact. Trigger: iterate, A/B results, performance review, refine, /haipipe-application iterate."
argument-hint: "[intervention-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.1.0"
  last_updated: "2026-07-06"
  summary: "Post-deploy iteration — A/B results, performance, refinement. Paper-alignment sweep: re-homed to 4-iterate/; triage targets on the new spine (design/variants/rationale words retired); ask-kind reference removed."
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

Step 4: BACKFILL THE LADDER FIRST -- fresh A/B numbers are new data:
        - land each metric as a dated, anchored D entry in
          0-lifecycle/1a-descriptions/1a-descriptions.md (--refresh path);
          the 1a skill stamps [STALE] tags on downstream P/C/T entries that
          cite the refreshed ids -- this is what re-opens exactly the
          affected rungs and nothing else
        Then extract decisions:
        - Drop underperforming artifact versions
        - Adjust timing, tone, or content
        - Add new segments or artifact versions
        - Update claims with real-world evidence

Step 5: Triage decisions to lifecycle stages:
        - "v2 outperformed v1"          → artifact (promote v2, re-draft losers)
        - "48h too early, 24h better"   → pitch (theory of change) or display (element spec)
        - "click rate validates C02"    → claims (GAP → supported, cite the A/B result now anchored in 1a)
        - "no effect on adherence"      → pitch (re-examine theory) or claims
        - "principle P<n> refuted live"  → principles (revise or move to Rejected with the refuting evidence)
        - "opt-out rate too high"       → artifact (frequency/tone re-compose)

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

This is the application → insight write-back path. The iterate skill is
authorized to trigger `/haipipe-insight-*` to file cards from deployment
evidence (ask-gated per the copilot policy).


Risk profile
=============

WRITES round files. May trigger /haipipe-insight-* to file KB cards
from deployment evidence. READ-ONLY on lifecycle artifacts (changes
routed through lifecycle skills).
