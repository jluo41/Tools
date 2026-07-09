---
name: haipipe-application-narrative
description: "Stage 3 of the intervention lifecycle (venue-GATED: fires per STATUS.md stages_skipped — required for email/dashboard/ui-card/report, optional for checklist, skipped for sms/push/reminder). Answers 'how do claims compose into a coherent message/experience?' Maps claim flow to the output's arc structure. Output: 0-lifecycle/3-narrative/3-narrative.md + _LOG_3-narrative.md. Markdown only. Trigger: narrative, arc, story flow, message structure, /haipipe-application narrative."
argument-hint: "[intervention-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "4.0.0"
  last_updated: "2026-07-06"
  summary: "Paper-aligned: stage FOLDER paths (1c-claims/, 3-narrative/), gating read from STATUS.md stages_skipped (not venue profile directly), DPRC phases via 2-phase/ workers, precondition restated against the settlement bar."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-application-narrative
======================================

Stage 3 of the intervention lifecycle (venue-GATED, venue-ALIGNED). How claims compose into a coherent output structure -- the evidence-backed arc that determines the flow of the final deliverable. Same role as paper's narrative.

Question answered
==================

"How do claims compose into a coherent message/experience?"

When this stage fires
======================

Read `STATUS.md | stages_skipped |`: if `narrative` is listed, this stage is skipped (simple venues -- the venue template defines a fixed arc). `optional` venues (checklist) pull it in on user request. If invoked while skipped: say so and offer the frontier.

Input
======

- `0-lifecycle/1d-principles/1d-principles.md` (always -- the directives the arc composes)
- `0-lifecycle/1c-claims/1c-claims.md` (the evidence backstop)
- `0-lifecycle/2-pitch/2-pitch.md` (the primary claim + theory of change anchor the arc)
- `_venue/venue-<name>/` (arc structure rules) + `_audience/profile-<name>/` (register)

Output
=======

```
<intervention-root>/0-lifecycle/3-narrative/3-narrative.md
<intervention-root>/0-lifecycle/3-narrative/_LOG_3-narrative.md
```

Narrative artifact schema (venue-dependent)
=============================================

Canonical template (source of truth for section order + placeholders): `ref/narrative-template.md`.

> CC: the schema blocks below use `#`/`##` headings while the formatting note + template are ascii — align or bless as example-only.

**venue-email:**
```markdown
# Narrative: <intervention name>

## Arc structure
1. Context paragraph     ← C01 (why this matters now)
2. Finding paragraph     ← C02, C03 (what the evidence shows)
3. Recommendation        ← C04 (what to do)
4. Next steps            ← (standard)

## Claim → arc mapping
C01 → Section 1 (context)
C02 → Section 2 (finding, lead)
C03 → Section 2 (finding, support)
C04 → Section 3 (recommendation)
```

**venue-dashboard:**
```markdown
# Narrative: <intervention name>

## Arc structure (drill-down)
Level 1: Summary KPIs      ← C01, C02 (headline metrics)
Level 2: Detail panels      ← C03, C04 (supporting evidence)
Level 3: Action items       ← C05 (recommendations)

## Probes
<narrative-level needs (rare): a beat exposing a NEW evidence gap routes
back to claims; one line per PP with status if any exist>
```

Artifact formatting: `=====` title / `-----` sections (no `#` headings); one sentence per line. Narrative reads the venue stage doc's Artifact Principles (2-venue.md) for arc rules.

Precondition
=============

The arc leans only on claims that meet the venue's settlement bar (STATUS.md `claims_settlement`): a load-bearing GAP claim cannot anchor a beat. If one does → BLOCK with a loopback suggestion to claims.

Phases
=======

```
DRAFT   map claims to arc positions per venue rules (haipipe-application-draft)
PROBE   rarely fires; a beat exposing a NEW evidence gap routes it back to
        claims as a _PROBE/ card, never gathers here (haipipe-application-probe)
REVISE  arc coherence + register pass (haipipe-application-revise)
CHECK   exit criteria below → Gate Ledger row (haipipe-application-check)
```

Definition of done
===================

```
[ ] 0-lifecycle/3-narrative/3-narrative.md exists (when the venue requires it)
[ ] Every load-bearing claim mapped to an arc position; no beat on a GAP claim
[ ] Arc structure follows the venue pack's rules
```

Handoff: `promote -> /haipipe-application display`. End the reply with the closing block (stage line via `../../../haipipe-application/stage-strip.sh`).

Risk profile
=============

WRITES the 3-narrative/ stage folder only.
