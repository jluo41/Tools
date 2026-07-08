---
name: haipipe-application-revise
description: "REVISE phase worker (internal). Called by application stage skills after PROBE to bring the stage doc (or artifact text) to venue+audience quality: weave in the evidence PROBE landed, tighten wording, enforce the venue style-profile and audience profile (tone, reading level, length limits). Agent-only -- changes the text directly, leaves why-comments, no comment-first. Users invoke stage skills, not this skill directly."
argument-hint: "[stage <stage-name>] [intervention-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: "1.0.0"
  last_updated: "2026-07-06"
  summary: "NEW thin REVISE worker (paper parity, single worker — paper's content/humanizer/weaving split deferred until application artifacts demand it). Venue style-profile + audience profile are the quality spec."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-application-revise (internal phase worker)
==========================================================

REVISE phase worker. Runs after PROBE, before CHECK. Agent-only: change the text directly and leave a short why-comment in `_LOG`; never switch to comment-first mode.

## What REVISE means

```
1. WEAVE      fold PROBE's landed evidence into the text: replace flagged
              NEEDs with the anchored takeaway or verdict-backed statement;
              a NEED that PROBE could not fill stays flagged for CHECK
2. TIGHTEN    one job per paragraph/element; cut filler; concrete over vague
3. CONFORM    venue style-profile (_venue/venue-<name>/style-profile.md):
              length limits, structure, register; audience profile
              (_audience/profile-<name>): tone, reading level, citation form
4. GUARD      claims language never outruns the ledger: a weak claim reads
              hedged, a GAP claim does not appear as fact
```

## Boundaries

- Never introduce new claims or numbers -- REVISE rearranges and polishes what DRAFT + PROBE settled.
- Venue-FREE stages (seed, claims): skip step 3's venue half; clarity rules still apply.
- Do not resolve CHECK-level questions (approval, scope changes) here.

## Return contract

```
status:    ok | blocked
stage:     <stage-name>
artifact:  <path revised>
open:      <count of NEEDs still flagged for CHECK>
next:      CHECK
```
