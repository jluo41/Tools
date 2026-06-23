---
name: haipipe-application-minimap
description: "Stage 5 of the intervention lifecycle. Answers 'what job does each piece of the output do?' Assigns a specific job and evidence anchor to every atomic unit (paragraph, panel, widget, row). Required for complex venues (dashboard, report); skipped for most venues. Same stage name as paper-minimap. Output: 0-lifecycle/5-minimap.md. Trigger: minimap, paragraph jobs, panel jobs, widget jobs, /haipipe-application minimap."
argument-hint: "[intervention-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "2.0.0"
  last_updated: "2026-06-23"
  summary: "Stage 5 — job + evidence anchor per output unit."
  changelog:
    - "2.0.0 (2026-06-23): renamed from delivery to minimap; match paper vocabulary; venue-gated."
    - "1.0.0 (2026-06-22): initial version as haipipe-application-delivery."
---

Skill: haipipe-application-minimap
=====================================

Stage 5 of the intervention lifecycle. Assigns a specific job and
evidence anchor to every atomic unit of the output.

Same role as paper's **minimap** — paragraph-level job assignments.
Here: panel-level, widget-level, or section-level job assignments
depending on venue.

**Required for:** dashboard, report.
**Optional for:** ui-card.
**Skipped for:** sms, push, reminder, checklist, email.


Question answered
==================

"What job does each piece of the output do?"


When this stage fires
======================

Only when the venue profile declares `minimap: required` or
`minimap: optional`. For most venues, the display stage or the
venue template already specifies enough granularity.


Input
======

- `0-lifecycle/4-display.md` (required — display must exist)
- Venue profile (atomic unit definition)


Output
=======

```
<intervention-root>/0-lifecycle/5-minimap.md
```


Minimap artifact schema (venue-dependent)
==========================================

**venue-dashboard:**
```markdown
# Minimap: <intervention name>

## Panel: Summary KPIs (D01 + D02)
| Widget | Job | Evidence anchor | Data source |
|--------|-----|-----------------|-------------|
| Refill rate gauge | Show current vs target | K03 | task T01 |
| Trend sparkline | 30-day trajectory | D01 | task T01 |
| At-risk count | Alert if threshold | K05 | task T02 |

## Panel: Timing Analysis (D03)
| Widget | Job | Evidence anchor | Data source |
|--------|-----|-----------------|-------------|
| Line chart | Rate by lead time | K03 | task T02 |
| Annotation | Mark optimal window | W02 | probe P01 |

## Panel: Action Items (D04)
| Widget | Job | Evidence anchor | Data source |
|--------|-----|-----------------|-------------|
| Table row | Patient + action | W02 | endpoint |
| Action button | Trigger SMS | (deployment) | endpoint |
```


Workflow
=========

```
Step 1: Check venue profile — is minimap required?
        If skip → return (no file).
        If optional → ask user.

Step 2: Read 4-display.md.

Step 3: Decompose each display unit into atomic widgets/
        sections with job assignments + evidence anchors.

Step 4: Draft 5-minimap.md.

Step 5: Present to user. Write (atomic).
```


Definition of done
===================

```
[ ] 0-lifecycle/5-minimap.md exists (if required)
[ ] Every display unit decomposed to atomic level
[ ] Every widget has a job and evidence anchor
```
