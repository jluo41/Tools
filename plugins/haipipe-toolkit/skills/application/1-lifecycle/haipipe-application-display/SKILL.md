---
name: haipipe-application-display
description: "Stage 4 of the intervention lifecycle. Answers 'what content element carries each claim?' Maps claims to specific display units (panels, widgets, charts, sections). Required for complex venues (dashboard, ui-card, report); skipped for simple venues. Output: 0-lifecycle/4-display/4-display.md + _LOG_4-display.md + _PROBE/ subfolder for display-spawned probes. For complex venues, 4-display.tex + PDF for rendered previews. Trigger: display, content elements, panels, widgets, /haipipe-application display."
argument-hint: "[intervention-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "3.0.0"
  last_updated: "2026-06-29"
  summary: "Stage 4 — what content element carries each claim. Now with _LOG changelog + _PROBE/ subfolder for display-spawned probes. Complex venues get .tex + PDF for rendered previews (same SEE-it-rendered rule as paper-display)."
  changelog:
    - "3.0.0 (2026-06-29): added _LOG, _PROBE/ subfolder. Output folder 4-display/ (was flat file). Complex venues (dashboard, report) get .tex + PDF for visual preview. Simple venues stay .md only. Borrowed per-stage tracking pattern from paper."
    - "2.0.0 (2026-06-23): renamed from variants to display; match paper vocabulary; venue-gated."
    - "1.0.0 (2026-06-22): initial version as haipipe-application-variants."
---

Skill: haipipe-application-display
=====================================

Stage 4 of the intervention lifecycle. What specific content
element carries each claim.

Same role as paper's **display** — where claims become figures/
tables. Here: where claims become panels, widgets, chart types,
section headings, or list items.

**Required for:** dashboard, ui-card, report.
**Optional for:** email.
**Skipped for:** sms, push, reminder, checklist.


Question answered
==================

"What content element carries each claim?"


When this stage fires
======================

Only when the venue profile declares `display: required` or
`display: optional`.


Input
======

- `0-lifecycle/3-narrative.md` (required if narrative fired)
- `0-lifecycle/2-claims.md` (always)
- Venue profile (available display element types)


Output
=======

```
<intervention-root>/0-lifecycle/4-display.md
```


Display artifact schema (venue-dependent)
==========================================

**venue-dashboard:**
```markdown
# Display Map: <intervention name>

## Display units

### D01: KPI Card — Refill Rate
- **Type:** metric-card
- **Claim:** C01
- **Content:** current rate, trend arrow, target
- **Data source:** task T01

### D02: Panel — Timing Analysis
- **Type:** line-chart
- **Claim:** C03
- **Content:** refill rate by hours-before-expiry
- **Data source:** task T02

### D03: Action List — Recommended Outreach
- **Type:** table
- **Claim:** C05
- **Content:** patient list with recommended action
- **Data source:** inference endpoint
```

**venue-report:**
```markdown
# Display Map: <intervention name>

### D01: Table 1 — Summary Statistics
- **Claim:** C01, C02
- **Content:** cohort descriptives

### D02: Figure 1 — Effect Size by Segment
- **Claim:** C03
- **Content:** forest plot
```


Workflow
=========

```
Step 1: Check venue profile — is display required?
        If skip → return (no file).
        If optional → ask user.

Step 2: Read narrative (or claims if narrative skipped).

Step 3: Map each claim to a display unit type per venue rules.

Step 4: Draft 4-display.md.

Step 5: Present to user. Write (atomic).
```


Definition of done
===================

```
[ ] 0-lifecycle/4-display.md exists (if required)
[ ] Every primary claim has at least one display unit
[ ] Display types match venue's available element types
```
