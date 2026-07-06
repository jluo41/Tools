---
name: haipipe-application-seed
description: "Stage 0 of the intervention lifecycle (venue-FREE). Answers 'why might this intervention work?' Documents the opportunity, expected impact, audience, channel hunch, mechanism hypothesis, and kill criteria. Output: 0-lifecycle/0-seed/0-seed.md + _LOG_0-seed.md (+ _PROBE/ for context needs). Markdown only. Modeled on haipipe-paper-seed. Trigger: seed, opportunity, why this intervention, kill criteria, /haipipe-application seed."
argument-hint: "[intervention-path] [intent...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "3.1.0"
  last_updated: "2026-07-06"
  summary: "Stage 0 on the paper-aligned contract: stage FOLDER (0-seed.md + _LOG + _PROBE/), venue-FREE marker, DPRC phases via 2-phase/ workers, scaffold via enter get-or-create (dead ref pointer removed)."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-application-seed
================================

Stage 0 of the intervention lifecycle (venue-FREE). Documents why this intervention might work before investing in evidence gathering. The user invokes this skill; it drives DRAFT → PROBE → REVISE → CHECK internally via the `2-phase/` workers.

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
<intervention-root>/0-lifecycle/0-seed/0-seed.md
<intervention-root>/0-lifecycle/0-seed/_LOG_0-seed.md
<intervention-root>/0-lifecycle/0-seed/_PROBE/          (context probes, when needed)
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

## Channel hunch
<SMS, push, in-app UI, provider dashboard, email — a HUNCH, not a pin;
the venue decision happens after claims via /haipipe-application venue>

## Mechanism hypothesis
<one sentence: why this audience + this content might respond>

## Kill criteria
<conditions under which we abandon this intervention>
- <criterion 1: e.g., "no HTE detected in cohort data">
- <criterion 2: e.g., "click rate < 2% in pilot">
- <criterion 3: e.g., "clinician review rejects tone/content">

## Probes
<seed-level investigation needs, INLINE and visible: landscape, prior
interventions, cohort sanity — one line per PP with status; cards in _PROBE/>
```

Artifact formatting: `=====` title / `-----` sections (no `#` headings); one sentence per line. Venue-FREE: the seed survives retargeting; the channel hunch is context, not a commitment.

Phases
=======

```
DRAFT   settle the six sections with the user (haipipe-application-draft)
PROBE   context needs only, mode light — prior interventions, benchmarks,
        cohort sanity → _PROBE/ cards (haipipe-application-probe); skip only
        by an explicit logged verdict
REVISE  tighten wording (haipipe-application-revise)
CHECK   exit criteria below → Gate Ledger row (haipipe-application-check)
```

If the intervention folder does not exist, route to `/haipipe-application enter <path>` (get-or-create owns scaffolding).

Definition of done
===================

```
[ ] 0-lifecycle/0-seed/0-seed.md exists and has all 6 sections
[ ] Kill criteria has at least 2 concrete conditions
[ ] Audience and channel hunch are specific (not "everyone" / "any channel")
```

Handoff: `promote -> /haipipe-application claims`. End the reply with the closing block (stage line via `../../../haipipe-application/stage-strip.sh`).

Risk profile
=============

WRITES the 0-seed/ stage folder only.
