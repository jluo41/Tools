---
name: haipipe-application-revise
description: "Application-specific REVISE phase worker (internal). Called whenever the Page router enters REVISE to improve a stage doc under fixed purpose and Aims: weave any landed evidence, tighten wording, and enforce applicable venue and audience profiles. A changed promise routes to DRAFT and a new unknown routes to EVIDENCE. Users invoke stage skills, not this skill directly."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  argument_hint: "[stage <stage-name>] [intervention-path]"
  version: "0.1.2"
  last_updated: "2026-08-04"
  summary: "Application-specific REVISE worker layered on haipipe-page-revise, adding venue and audience quality under fixed Aims."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-application-revise (internal phase worker)
==========================================================

REVISE phase worker. Runs whenever the Page router selects REVISE. Agent-only: change the text directly and leave a short why-comment in `_LOG`; never switch to comment-first mode.

**LOAD THE PAGE LAYERS FIRST:** `../../../../board/page-types/haipipe-page-for-stage/SKILL.md`, then `../../../../board/page-workflows/haipipe-page-revise/SKILL.md`.
This file adds application quality rules to that fixed-promise authority.

## What REVISE means

```
1. WEAVE      fold EVIDENCE's landed evidence into the text: replace flagged
              NEEDs with the stage doc's a-consumer (the Q-consumer `Answer:`
              line) or an evidence-backed statement;
              a NEED that EVIDENCE could not fill stays flagged for CHECK
2. TIGHTEN    one job per paragraph/element; cut filler; concrete over vague
3. CONFORM    the venue pack (venue/venue-<name>/style-profile.md):
              length limits, structure, register, and tone-by-audience
              (tone, reading level, citation form per the target audience)
4. GUARD      claims language never outruns the ledger: a weak claim reads
              hedged, a GAP claim does not appear as fact
```

## Boundaries

- Never introduce new claims or numbers -- REVISE rearranges and polishes what DRAFT + EVIDENCE settled.
- If purpose or an Aim must change, return to DRAFT and begin a new round; if a consequential answer is missing, route to EVIDENCE.
- Venue-FREE stages (seed + the 1a-1d ladder: descriptions, themes, claims, advice): skip step 3's venue half; clarity rules still apply.
- Do not resolve CHECK-level questions (approval, scope changes) here.

## Return contract

```
status:    ok | blocked
stage:     <stage-name>
artifact:  <path revised>
open:      <count of NEEDs still flagged for CHECK>
next:      <CHECK | EVIDENCE | DRAFT | REVISE, chosen by the Page router>
```
