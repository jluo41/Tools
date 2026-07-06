---
name: haipipe-application-pitch
description: "Stage 2 of the intervention lifecycle (venue-ALIGNED, first stage after the venue pin). Answers 'what is this intervention selling, to whom, through this channel?' One-minute goal + theory of change, framed for the pinned venue + audience. Same stage name as paper-pitch (the cover letter analog). Output: 0-lifecycle/2-pitch/2-pitch.md + _LOG_2-pitch.md. Markdown only. Trigger: pitch, goal, story, theory of change, what are we trying to do, /haipipe-application pitch."
argument-hint: "[intervention-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "4.0.0"
  last_updated: "2026-07-06"
  summary: "Paper-aligned renumber: pitch moves from stage 1 to stage 2 (AFTER claims + venue pin; was before claims in v3). Now venue-ALIGNED: reads the pinned venue + audience packs, re-couples on retarget. Stage folder 0-lifecycle/2-pitch/."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-application-pitch
==================================

Stage 2 of the intervention lifecycle -- the first venue-ALIGNED stage. The one-minute story of what this intervention achieves and why it should work, told FOR the pinned venue and audience. Rewrites on retarget (claims does not).

Question answered
==================

"What is this intervention selling, to whom, through this channel?"

Input
======

- `0-lifecycle/1-claims/1-claims.md` (required -- the ledger feeds the story)
- `0-lifecycle/0-seed/0-seed.md`
- `STATUS.md` -> pinned venue + audience (required; if venue unpinned -> BLOCK: "run /haipipe-application venue first")
- `_venue/venue-<name>/` + `_audience/profile-<name>/` (framing expectations)

Output
=======

```
<intervention-root>/0-lifecycle/2-pitch/2-pitch.md
<intervention-root>/0-lifecycle/2-pitch/_LOG_2-pitch.md
```

Pitch artifact schema
======================

```markdown
# Pitch: <intervention name>

## One-sentence goal
<what this intervention does, for whom, through the pinned channel>
Example: "A timing-aware refill SMS that increases adherence by
8-12pp among patients whose prescriptions are about to expire."

## Theory of change
<why this should work — the causal chain from message to behavior,
anchored in the ledger's supported claims (cite C-ids)>

## Audience frame
<how the pinned audience profile shapes the register and ask>

## Primary claim
<which ledger claim carries the value proposition ([primary] designation
lives HERE, venue-aligned — not in the venue-free ledger)>

## Why now
<what makes this timely>
```

Phases
=======

```
DRAFT   settle goal + theory of change with the user (haipipe-application-draft)
PROBE   rare; anchor evidence for the theory of change if the ledger lacks it,
        mode light (haipipe-application-probe)
REVISE  venue + audience framing pass (haipipe-application-revise)
CHECK   exit criteria below → Gate Ledger row (haipipe-application-check)
```

Definition of done
===================

```
[ ] 0-lifecycle/2-pitch/2-pitch.md exists
[ ] One-sentence goal is specific and testable
[ ] Theory of change cites ledger claims (C-ids), no unanchored assertions
[ ] Primary claim designated; audience frame matches the profile
```

Retarget rule: a venue re-pin rewrites this stage (new framing, possibly a new primary claim); the claims ledger it cites stays unchanged.

Handoff: `promote -> /haipipe-application narrative` (or straight to `draft` for simple venues -- check STATUS.md stages_skipped). End the reply with the closing block (stage line via `../../../haipipe-application/stage-strip.sh`).

Risk profile
=============

WRITES the 2-pitch/ stage folder only.
