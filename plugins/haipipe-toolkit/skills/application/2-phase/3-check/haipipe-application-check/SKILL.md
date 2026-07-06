---
name: haipipe-application-check
description: "CHECK phase worker (internal) -- the only human-involved phase, run by every application stage skill after REVISE. Presents the stage's exit criteria with per-item marks, proposes approve / revise / done, and on explicit approval writes the Gate Ledger row in STATUS.md and advances current_layer. Venue-scaled depth: simple venues confirm inline, complex venues get a full CHECK report. Persona presets + attendance modes let a stand-in approve ONLY in unattended runs. Renamed from haipipe-application-gate (paper-alignment 2026-07-06). Trigger: check, gate, approve stage, exit criteria, /haipipe-application check."
argument-hint: "[stage: seed|claims|pitch|narrative|display|section-edit|draft] [--persona strict|balanced|creative|lenient] [--unattended[=Ns]]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "3.0.0"
  last_updated: "2026-07-06"
  summary: "Gate skill re-homed as the CHECK phase worker (2-phase/3-check). Adds the Gate Ledger protocol (STATUS.md, ✅ = approved-by-whom); keeps venue-scaled firing + persona/attendance as the application delta. Stage list updated to the new spine (minimap out, section-edit in)."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-application-check (CHECK phase worker)
======================================================

CHECK phase worker -- the 🧑 phase. Reviews the artifacts produced during one lifecycle stage's DRAFT-PROBE-REVISE and proposes the next move:

```
approve   → Gate Ledger row + advance current_layer to the next non-skipped stage
revise    → loop back with feedback (same stage; upstream problems are named
            as loopback suggestions, the user decides)
done      → early exit: jump to draft (artifact) with remaining stages waived
            (recorded in the ledger notes)
```

A stage is only "done" when this approval is EXPLICIT. The system never auto-advances. Full protocol: `../../../wiki/08-stage-gate.md`.

Gate Ledger (STATUS.md)
========================

On approve, append/update the row and bump `current_layer`:

```
## Gate Ledger

| Stage | Confirmed | Date | By | Notes |
|-------|-----------|------|----|-------|
| seed | yes | 2026-07-06 | JL | kill criteria set |
| claims | yes | 2026-07-06 | JL | settlement: light met |
```

`By` records who approved: the human (copilot mode) or `persona:<preset>` (unattended mode). The stage strip's ✅ means "confirmed in this ledger", NOT "artifact exists on disk".

Venue-scaled depth (when CHECK fires)
======================================

```
simple (sms, push, reminder)      INLINE — present the exit criteria as one short
                                  checklist in the reply; user's "ok" = approve.
medium (checklist, email)         INLINE by default; full report on request (--report).
complex (dashboard, ui-card,      FULL — render the complete CHECK report (criteria
report)                           + evidence spot-checks + flags) before the ask.
```

The venue profile's README can override with `gate: inline | report`.

Per-stage exit criteria
========================

```
seed:          kill criteria present? audience hunch specific? >=1 evidence path named?
claims:        every claim a ### C<n> prose subsection with role + status? no load-bearing
               GAP without a _PROBE/ card? settlement bar met for the pinned depth
               (light/medium/full — see claims skill §Settlement Gate)?
pitch:         one-sentence goal testable? mechanism (theory of change) plausible?
               venue + audience named?
narrative:     arc follows venue rules? all load-bearing claims mapped to beats?
display:       every primary claim has a content element? every element has a job +
               evidence anchor? materialization routed (task refs) where needed?
section-edit:  every section's prose does its assigned job? flagged NEEDs resolved
               or explicitly parked?
draft:         venue self-review checklist passes? audience constraints met? artifact
               cites only ledger-backed claims (cited_K/W resolve)?
```

Persona presets (unattended stand-in ONLY)
============================================

```
preset       strictness  ambition  default outcome
─────────    ──────────  ────────  ───────────────
strict       8           4         revise
balanced     5           5         revise
creative     3           8         approve
lenient      2           3         approve
```

In copilot mode (default) the human decides and personas only SHAPE the report's recommendation. In `--unattended[=Ns]` runs the persona decides after the timeout and the ledger records `persona:<preset>`. Full schema: `./gate-persona.md`; attendance modes: `./attendance-modes.md`.

Return contract
================

```
status:    approved | revise | done | awaiting-user
stage:     <stage-name>
criteria:  <n passed> / <m total> (+ per-item marks in the report)
ledger:    <row written or "pending user">
next:      <next stage command or the revise instruction>
```

Risk profile
=============

READ-ONLY on stage artifacts. Writes ONLY the STATUS.md Gate Ledger + current_layer (on approve) and a `[CHECK]` entry in the stage `_LOG`. Does NOT modify lifecycle artifacts.
