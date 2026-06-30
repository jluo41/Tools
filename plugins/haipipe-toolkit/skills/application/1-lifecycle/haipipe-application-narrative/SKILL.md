---
name: haipipe-application-narrative
description: "Stage 3 of the intervention lifecycle. Answers 'how do claims compose into a coherent message/experience?' Maps claim flow to the output's arc structure. Required for complex venues (email, dashboard, ui-card, report); skipped for simple venues. Output: 0-lifecycle/3-narrative/3-narrative.md + _LOG_3-narrative.md + _DISPLAY_3-narrative.md (which display unit serves each beat). Markdown only. Trigger: narrative, arc, story flow, message structure, /haipipe-application narrative."
argument-hint: "[intervention-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "3.0.0"
  last_updated: "2026-06-29"
  summary: "Stage 3 — how claims compose into a coherent output arc. Now with _LOG changelog + _DISPLAY_ tracking (which display unit serves each beat). Borrowed per-stage tracking pattern from paper."
  changelog:
    - "3.0.0 (2026-06-29): added _LOG, _DISPLAY_ tracking file (beat → display unit mapping). Output folder 3-narrative/ (was flat file). Borrowed per-stage tracking pattern from paper."
    - "2.0.0 (2026-06-23): renamed from design to narrative; match paper vocabulary; venue-gated."
    - "1.0.0 (2026-06-22): initial version as haipipe-application-design."
---

Skill: haipipe-application-narrative
======================================

Stage 3 of the intervention lifecycle. How claims compose into a
coherent output structure.

Same role as paper's **narrative** — the evidence-backed arc that
determines the flow of the final deliverable.

**Required for:** email, dashboard, ui-card, report.
**Skipped for:** sms, push, reminder (venue template handles arc).
**Optional for:** checklist.


Question answered
==================

"How do claims compose into a coherent message/experience?"


When this stage fires
======================

Only when the venue profile declares `narrative: required` or
`narrative: optional`. For simple venues, the venue template
defines a fixed arc and this stage is skipped.


Input
======

- `0-lifecycle/2-claims.md` (required)
- Venue profile from `_venue/venue-<name>/` (arc structure rules)
- `_audience/profile-<audience>/` (tone/style)


Output
=======

```
<intervention-root>/0-lifecycle/3-narrative.md
```


Narrative artifact schema (venue-dependent)
=============================================

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

## Claim → panel mapping
C01 → KPI card "Refill Rate"
C02 → KPI card "At-Risk Count"
C03 → Detail panel "Timing Analysis"
```


Precondition
=============

For full-claims venues: all **primary** claims must be `supported`
or `weak` (not GAP). If any primary claim is GAP → BLOCK.

For light-claims venues: this stage is skipped, so not applicable.


Workflow
=========

```
Step 1: Check venue profile — is narrative required?
        If skip → return immediately (no file written).
        If optional → ask user whether to write it.

Step 2: Read 2-claims.md and venue arc structure rules.

Step 3: Map claims to arc positions per venue rules.

Step 4: Draft 3-narrative.md.

Step 5: Present to user. Write (atomic).
```


Definition of done
===================

```
[ ] 0-lifecycle/3-narrative.md exists (if required/optional-and-chosen)
[ ] Every claim mapped to an arc position
[ ] Arc structure follows venue rules
```
