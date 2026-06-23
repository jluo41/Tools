---
name: haipipe-application-gate
description: "Phase-transition gate for the intervention lifecycle. Venue-gated: required for complex venues (dashboard, report), optional for medium venues (email, checklist), skip for simple venues (sms, push, reminder). Reviews stage artifacts and proposes approve / revise / done. Supports persona presets and attendance modes. Trigger: gate, review stage, approve, revise, /haipipe-application gate."
argument-hint: "[stage: seed|pitch|claims|narrative|display|minimap|draft] [--persona strict|balanced|creative|lenient] [--auto]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "2.0.0"
  last_updated: "2026-06-23"
  summary: "Phase-transition gate — venue-gated, persona-driven."
  changelog:
    - "2.0.0 (2026-06-23): venue-gated; updated stage names to paper vocabulary; simplified for lifecycle model."
    - "1.0.0 (2026-05-31): baseline."
---

Skill: haipipe-application-gate
================================

Phase transition gate. Reviews the artifacts produced during one
lifecycle stage and proposes the next move:

```
approve   → proceed to next stage
revise    → loop back with feedback
done      → jump to draft (early exit)
```


When gates fire (venue-driven)
================================

```
venue complexity    gate behavior
────────────────    ─────────────────────────────────
simple (sms,        SKIP — lifecycle flows seed → pitch
push, reminder)     → claims → draft without gates.
                    The stages are lightweight enough
                    that user review between stages
                    is sufficient.

medium (checklist,  OPTIONAL — user can request gates
email)              at any stage boundary. Default: no
                    gates unless --gate flag is passed.

complex (dashboard, REQUIRED — gate fires between every
ui-card, report)    stage. Full persona + attendance
                    machinery applies.
```

The venue profile's README.md can declare:
```yaml
gate: skip | optional | required
```


Gate outcomes
==============

```
approve   → next stage
revise    → loop back to the stage with feedback
done      → skip remaining stages, jump to draft
```

`revise` always loops back to the **current stage**, not to an
earlier one. If the problem is upstream (e.g., claims are wrong
during narrative), the user should explicitly run the upstream
stage command.


Per-stage checks
=================

```
G-seed:      kill criteria present? audience specific?
G-pitch:     one-sentence goal testable? mechanism plausible?
G-claims:    (light) K/W coverage complete?
             (full) all primary claims supported or weak?
             no GAP claims without probe plans?
G-narrative: arc follows venue rules? all claims mapped?
G-display:   every primary claim has a display unit?
G-minimap:   every display unit decomposed? jobs assigned?
G-draft:     venue self-review checklist passes?
             audience constraints met?
```


Persona presets
================

```
preset       strictness  ambition  default outcome
─────────    ──────────  ────────  ───────────────
strict       8           4         revise
balanced     5           5         revise
creative     3           8         approve
lenient      2           3         approve
```

Default: `balanced` for new interventions.

See `../haipipe-application/ref/gate-persona.md` for full schema
and `ref/attendance-modes.md` for attended/timed/unattended.


Risk profile
=============

READ-ONLY on stage artifacts. May append gate history to
STATUS.md. Does NOT modify lifecycle artifacts.
