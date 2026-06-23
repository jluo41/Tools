---
name: haipipe-application-pitch
description: "Stage 1 of the intervention lifecycle. Answers 'what is this intervention trying to achieve?' One-sentence goal + mechanism hypothesis + audience + channel. Same stage name as paper-pitch. Output: 0-lifecycle/1-pitch.md. Trigger: pitch, goal, story, what are we trying to do, /haipipe-application pitch."
argument-hint: "[intervention-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "2.0.0"
  last_updated: "2026-06-23"
  summary: "Stage 1 — one-sentence goal + mechanism hypothesis."
  changelog:
    - "2.0.0 (2026-06-23): renamed from rationale to pitch; match paper vocabulary."
    - "1.0.0 (2026-06-22): initial version as haipipe-application-rationale."
---

Skill: haipipe-application-pitch
==================================

Stage 1 of the intervention lifecycle. The one-sentence story of
what this intervention tries to achieve and why it should work.

Same role as paper's **pitch** — the story you can tell in one
minute that makes someone want to invest further.


Question answered
==================

"What is this intervention trying to achieve?"


Input
======

- `0-lifecycle/0-seed.md` (required — seed must exist)
- Project KB: insights/K_knowledge/, W_wisdom/ (if available)


Output
=======

```
<intervention-root>/0-lifecycle/1-pitch.md
```


Pitch artifact schema
======================

```markdown
# Pitch: <intervention name>

## One-sentence goal
<what this intervention does and for whom>
Example: "A timing-aware refill SMS that increases adherence by
8-12pp among patients whose prescriptions are about to expire."

## Mechanism hypothesis
<why this should work — the causal link>

## Audience
<who receives this>

## Channel
<how it reaches them — suggests venue for next step>

## Why now
<what makes this timely>
```

The channel field in the pitch **suggests** the venue but does not
pin it. Venue is pinned explicitly in the next step via
`/haipipe-application venue`.


Workflow
=========

```
Step 1: Read 0-seed.md. If missing → BLOCK.
Step 2: Scan KB for supporting K/W entries.
Step 3: Draft 1-pitch.md.
Step 4: Present to user for review.
Step 5: Write 1-pitch.md (atomic).
```


Definition of done
===================

```
[ ] 0-lifecycle/1-pitch.md exists
[ ] One-sentence goal is specific (not vague)
[ ] Mechanism hypothesis is testable
[ ] Audience and channel identified
```
