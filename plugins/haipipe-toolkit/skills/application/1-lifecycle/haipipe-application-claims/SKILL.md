---
name: haipipe-application-claims
description: "Stage 2 of the intervention lifecycle. Answers 'what must be true for this to work?' (full) or 'which K/W entries inform this output?' (light). Depth is venue-driven: light = select from existing KB, medium = select + gap check, full = claim ledger with probe plans. Always required. Output: 0-lifecycle/2-claims.md. Trigger: claims, claim ledger, what must be true, which K/W, evidence, /haipipe-application claims."
argument-hint: "[intervention-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "2.0.0"
  last_updated: "2026-06-23"
  summary: "Stage 2 — claims with venue-driven depth (light/medium/full)."
  changelog:
    - "2.0.0 (2026-06-23): added claims_depth (light/medium/full) driven by venue profile."
    - "1.0.0 (2026-06-22): initial version modeled on paper-claims."
---

Skill: haipipe-application-claims
==================================

Stage 2 of the intervention lifecycle. Always required, but its
**depth** scales with venue complexity.


Claims depth (venue-driven)
=============================

The venue profile's `claims_depth` field determines how deep the
claims stage goes:

```
claims_depth   venues                    what happens
────────────   ─────────────────────     ──────────────────────────────
light          sms, push, reminder       SELECT from existing K/W.
                                         List which K/W entries inform
                                         each slot of the venue template.
                                         No probe planning. If KB is
                                         empty, use common knowledge
                                         or trigger ask session first.

medium         checklist, email          SELECT + GAP CHECK.
                                         Verify K/W covers all items/
                                         sections. Flag gaps. Optional
                                         probe if gap is load-bearing.

full           dashboard, ui-card,       FULL CLAIM LEDGER.
               report                    Every claim gets status
                                         (supported/weak/GAP). GAPs
                                         get probe plans in
                                         1-probe-plans/.
```


Question answered (depth-dependent)
=====================================

```
light:   "Which K/W entries inform this message?"
medium:  "Do we have evidence for every part of this output?"
full:    "What must be true for this intervention to work?"
```


Input
======

- `0-lifecycle/1-pitch.md` (required)
- `0-lifecycle/0-seed.md`
- `STATUS.md` → venue → claims_depth
- Venue profile from `_venue/venue-<name>/` (template if light)
- Project KB: insights/INDEX.md, K_knowledge/, W_wisdom/
- Existing probe plans in `1-probe-plans/` (if any, full only)


Output
=======

```
<intervention-root>/0-lifecycle/2-claims.md
<intervention-root>/1-probe-plans/PP##_<slug>.md   (full depth only)
```


Light claims artifact
======================

For SMS, push, reminder — just map K/W to venue template slots:

```markdown
# Claims (light): <intervention name>

## K/W selection
- **Benefit slot** draws on: K03 (timing sensitivity in refill)
- **CTA slot** draws on: W02 (recommend refill action at T-48h)
- **Greeting slot**: personalization (common knowledge, no K needed)
- **Close slot**: standard opt-out (no K needed)

## Coverage
All template slots covered. No gaps.

## Cited
- cited_K: [K03]
- cited_W: [W02]
```


Medium claims artifact
========================

For checklist, email — selection + gap check:

```markdown
# Claims (medium): <intervention name>

## Coverage check
| Section / Item | K/W source | Status |
|----------------|------------|--------|
| Context paragraph | K03 | covered |
| Finding 1 | K05, D01 | covered |
| Finding 2 | (none) | gap — non-critical, proceed |
| Recommendation | W02 | covered |

## Gaps
- Finding 2: no K/W entry covers this. Low priority —
  use directional language ("emerging evidence suggests...").
  Optional: trigger ask session to gather evidence.

## Cited
- cited_K: [K03, K05]
- cited_W: [W02]
- cited_D: [D01]
```


Full claims artifact
=====================

For dashboard, ui-card, report — same as paper's claim ledger:

```markdown
# Claim Ledger: <intervention name>

## Summary
N claims: M supported, P weak, Q GAP

## Claims

### C01: <claim statement>
- **Status:** supported | weak | GAP
- **Evidence:** K03, D01 (or "none — GAP")
- **Role:** primary | enabling | assumption
- **Notes:** <why this matters>
- **Probe plan:** PP01_... (if GAP)

### C02: ...
```


Workflow (all depths)
======================

```
Step 1: Read 1-pitch.md. If missing → BLOCK.
        Read STATUS.md → venue → claims_depth.

Step 2: Read venue profile. Get claims_depth and template (if light).

Step 3: Scan KB for K/W entries relevant to the pitch.

Step 4: Per depth:

        LIGHT:
          Map K/W to venue template slots.
          If slot has no K/W → mark "common knowledge" or flag.
          Write 2-claims.md (light format).

        MEDIUM:
          Map K/W to sections/items.
          Gap check: any section with no backing → flag.
          Decide: proceed with caveat OR trigger ask.
          Write 2-claims.md (medium format).

        FULL:
          Extract every testable claim from pitch.
          Check KB per claim → supported/weak/GAP.
          For each GAP → write probe plan in 1-probe-plans/.
          Write 2-claims.md (full format).

Step 5: Present summary to user.
Step 6: Write (atomic).
```


Claim status vocabulary (full depth only)
==========================================

```
supported   K/W entry exists and backs the claim
weak        K/W entry exists but incomplete or narrow scope
GAP         no evidence; must gather before advancing
```


Claim roles (full depth only)
===============================

```
primary     core value proposition depends on this
enabling    intervention works without it but better with it
assumption  taken as given; not worth probing unless challenged
```


GAP → probe plan buffer (full depth only)
===========================================

For each GAP claim, write:

```
1-probe-plans/PP01_<slug>.md
```

```markdown
# Probe Plan: PP01_timing_effect

- **Source claim:** C02
- **Question:** <what evidence is needed>
- **Route:** /haipipe-probe plan from-need
- **Status:** planned | dispatched | returned
- **Verdict:** <filled on return>
```


Backfill on probe return (full depth)
=======================================

1. Read verdict from probes/<id>/probe.yaml.
2. Update claim status in 2-claims.md.
3. Update probe plan status in 1-probe-plans/.


Definition of done
===================

```
LIGHT:
  [ ] 2-claims.md exists with K/W → slot mapping
  [ ] cited_K / cited_W listed

MEDIUM:
  [ ] 2-claims.md exists with coverage check table
  [ ] Gaps flagged with decision (proceed/ask)
  [ ] cited_K / cited_W listed

FULL:
  [ ] 2-claims.md exists with all claims
  [ ] Every claim has status (supported/weak/GAP)
  [ ] Every GAP has probe plan in 1-probe-plans/
  [ ] Claim roles assigned
```


Risk profile
=============

WRITES: `0-lifecycle/2-claims.md`.
FULL depth also writes: `1-probe-plans/PP##_*.md`.
READ-ONLY on KB and probes.
