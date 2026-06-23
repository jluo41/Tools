---
name: haipipe-application-lifecycle
description: "Stage orchestrator for the intervention lifecycle. Dispatches to per-stage skills (seed, pitch, venue, claims, narrative, display, minimap) based on verb or frontier detection. Reads venue profile to determine which stages fire (skip/optional/required). Modeled on haipipe-paper-lifecycle. Trigger: lifecycle, advance, next stage, /haipipe-application lifecycle."
argument-hint: "[stage-verb] [intervention-path]"
allowed-tools: Bash, Read, Grep, Glob, Skill
metadata:
  version: "2.0.0"
  last_updated: "2026-06-23"
  summary: "Stage orchestrator — venue-aware dispatch to lifecycle skills."
  changelog:
    - "2.0.0 (2026-06-23): renamed stages to paper vocabulary; venue-aware stage skipping."
    - "1.0.0 (2026-06-22): initial version modeled on paper-lifecycle."
---

Skill: haipipe-application-lifecycle (stage orchestrator)
==========================================================

Dispatches to the correct per-stage skill based on verb or auto-
detected frontier. Reads the venue profile to skip stages that the
venue declares as `skip`.


Stage spine (same vocabulary as paper)
========================================

```
Stage 0  seed         "why might this intervention work?"
Stage 1  pitch        "what is this intervention trying to achieve?"
(venue)               pinned in STATUS.md — determines which stages fire
Stage 2  claims       "which K/W inform this?" or "what must be true?"
Stage 3  narrative    "how do claims compose into a coherent arc?"
Stage 4  display      "what content element carries each claim?"
Stage 5  minimap      "what job does each piece of the output do?"
```

Each stage owns one file under `0-lifecycle/`:

```
0-lifecycle/0-seed.md
0-lifecycle/1-pitch.md
0-lifecycle/2-claims.md
0-lifecycle/3-narrative.md       (if required by venue)
0-lifecycle/4-display.md         (if required by venue)
0-lifecycle/5-minimap.md         (if required by venue)
```


Dispatch rules
===============

```
verb / keyword                             → skill
───────────────────────────────────────────────────────
seed, opportunity, why, kill criteria      → haipipe-application-seed
pitch, goal, story, what are we doing      → haipipe-application-pitch
venue, format, modality, which channel     → haipipe-application-venue
claims, K/W, what must be true, evidence   → haipipe-application-claims
narrative, arc, story flow, structure      → haipipe-application-narrative
display, content elements, panels, widgets → haipipe-application-display
minimap, jobs, widget jobs, paragraph jobs  → haipipe-application-minimap
(no verb)                                  → auto-detect frontier
```


Auto-detect frontier (venue-aware)
====================================

If no verb is given:

```
1. Read STATUS.md for pinned venue.
2. If no venue pinned:
     frontier candidates = [0-seed, 1-pitch, venue]
3. If venue pinned:
     Read venue profile → stages block.
     Build ordered stage list, skipping stages marked `skip`.
4. Find earliest stage without a non-empty artifact file.
5. Dispatch to that stage's skill.
```

Example for venue-sms:
```
stages to check: [0-seed, 1-pitch, 2-claims]
                  (narrative, display, minimap all skip)
if 0-seed.md exists and 1-pitch.md exists and 2-claims.md missing:
  → frontier = claims → dispatch haipipe-application-claims
```

Example for venue-dashboard:
```
stages to check: [0-seed, 1-pitch, 2-claims, 3-narrative,
                  4-display, 5-minimap]
if all present:
  → frontier = post-lifecycle → suggest /haipipe-application draft
```


Venue gate
===========

Between pitch and claims, the orchestrator checks whether venue
is pinned in STATUS.md. If not pinned → dispatch to
`haipipe-application-venue` before proceeding to claims.


Loopback rule
==============

```
symptom                                → loop back to
──────────────────────────────────────────────────────
evidence missing for claim             → claims
theory of change wrong                 → pitch
output structure wrong                 → narrative (or venue)
content element doesn't fit            → display
venue wrong for audience               → venue (invalidates claims+)
stakeholder/clinician review rejected  → round → target stage
```


Risk profile
=============

READ-ONLY. Dispatches to stage skills which do the writing.
