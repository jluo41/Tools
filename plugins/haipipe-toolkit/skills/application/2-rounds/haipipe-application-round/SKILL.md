---
name: haipipe-application-round
description: "Round management for the intervention lifecycle. Captures stakeholder/clinician review feedback, A/B test results, or iteration decisions into dated round folders. Triages todo items back to lifecycle stages. Modeled on haipipe-paper-round. Trigger: round, feedback round, review round, iteration, /haipipe-application round."
argument-hint: "[new|enter|triage|close] [intervention-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.0.0"
  last_updated: "2026-06-22"
  summary: "Round management — feedback, triage, iteration cycles."
  changelog:
    - "1.0.0 (2026-06-22): initial version modeled on paper-round."
---

Skill: haipipe-application-round
==================================

First-class working memory for revision cycles. Each round captures
one batch of feedback (stakeholder review, clinician input, A/B test
results) and routes actionable items back to lifecycle stages.


Round folder structure
=======================

```
1-rounds/
├── latest.md                → pointer to active round
└── vYYMMDD/
    ├── README.md            round header (source, date, purpose, status)
    ├── discussion.md        raw review / meeting text / test results
    ├── decisions.md         decisions accepted as intent
    ├── todo.md              open needs, routed to lifecycle stages
    └── applied.md           backfill log: what changed where
```


Commands
=========

```
/haipipe-application round new           create new round folder
/haipipe-application round enter         read current round status
/haipipe-application round triage        route todo items to stages
/haipipe-application round close         mark round closed
```


Round lifecycle
================

```
open → collect discussion → extract decisions → triage todo
     → record applied → close (or keep active)
```


Triage targets
===============

```
symptom in todo                          → route to
──────────────────────────────────────────────────────
"claim X not convincing"                 → claims (update status)
"tone too clinical for patients"         → design (update tone)
"add a variant for Spanish speakers"     → variants (add V-slot)
"timing should be 24h not 48h"          → design (update timing)
"SMS too long"                          → draft (re-draft variant)
"click rate below threshold"            → claims (re-evaluate) or
                                           design (change approach)
"need evidence for X"                   → claims (add GAP + probe plan)
```


README.md schema
=================

```markdown
# Round: vYYMMDD

- **Source:** clinician review | A/B test results | stakeholder mtg
- **Date:** YYYY-MM-DD
- **Purpose:** <one sentence>
- **Maturity at open:** <maturity from STATUS.md>
- **Status:** open | closed
```


Workflow (new round)
=====================

```
Step 1: Create 1-rounds/vYYMMDD/ with 5 empty files.
Step 2: Update 1-rounds/latest.md → vYYMMDD.
Step 3: User pastes discussion content (review text, test data).
Step 4: Extract decisions from discussion.
Step 5: Triage: route each decision to a lifecycle stage.
Step 6: As changes are applied, log in applied.md.
Step 7: When all todo items resolved → close round.
```


Risk profile
=============

WRITES round folder files. Does NOT modify lifecycle artifacts
directly — routes todo items which the lifecycle skills apply.
