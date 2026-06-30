---
name: haipipe-application-seed
description: "Stage 0 of the intervention lifecycle. Answers 'why might this intervention work?' Documents the opportunity, expected impact, audience, channel, and kill criteria. Output: 0-lifecycle/0-seed/0-seed.md + _LOG_0-seed.md. Markdown only (argument documents don't need compilation). Modeled on haipipe-paper-seed. Trigger: seed, opportunity, why this intervention, /haipipe-application seed."
argument-hint: "[intervention-path] [intent...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "2.0.0"
  last_updated: "2026-06-29"
  summary: "Stage 0 — intervention possibility + kill criteria. Now with _LOG changelog (borrowed from paper v2.0.0)."
  changelog:
    - "2.0.0 (2026-06-29): added _LOG_0-seed.md changelog; output folder 0-seed/ (was flat file); borrowed .md + _LOG pattern from paper-seed v2.0.0."
    - "1.0.0 (2026-06-22): initial version modeled on paper-seed."
---

Skill: haipipe-application-seed
================================

Stage 0 of the intervention lifecycle. Documents why this
intervention might work before investing in evidence gathering.


Question answered
==================

"Why might this intervention work? What is the opportunity?"


Input
======

- User intent / problem statement
- Existing project KB (insights/INDEX.md if available)
- Domain knowledge about the audience and channel


Output
=======

```
<intervention-root>/0-lifecycle/0-seed.md
```


Seed artifact schema
=====================

```markdown
# Intervention Seed: <name>

## Opportunity
<2-3 sentences: what gap exists, what behavior we want to change>

## Expected impact
<directional estimate: "increase refill adherence by 5-15pp">

## Audience
<who receives this intervention: patient subset, clinician type>

## Channel
<SMS, push notification, in-app UI, provider dashboard, email>

## Mechanism hypothesis
<one sentence: why this channel + this content might work>

## Kill criteria
<conditions under which we abandon this intervention>
- <criterion 1: e.g., "no HTE detected in cohort data">
- <criterion 2: e.g., "click rate < 2% in pilot">
- <criterion 3: e.g., "clinician review rejects tone/content">
```


Workflow
=========

```
Step 1: Parse intent + resolve intervention root.
        If intervention folder does not exist, scaffold it
        (see ../ref/intervention-folder-schema.md).

Step 2: Read existing KB if available (insights/INDEX.md).
        Look for K/W entries that motivate this intervention.

Step 3: Draft 0-seed.md following the schema above.

Step 4: Present seed to user for review.
        User may adjust opportunity, audience, channel, or
        kill criteria.

Step 5: Write 0-seed.md (atomic).
```


Definition of done
===================

```
[ ] 0-lifecycle/0-seed.md exists and has all 6 sections
[ ] Kill criteria has at least 2 concrete conditions
[ ] Audience and channel are specific (not "everyone" / "any channel")
```


Risk profile
=============

WRITES one file: `0-lifecycle/0-seed.md`. May scaffold the
intervention folder if it does not exist.
