---
name: haipipe-application-check
description: "CHECK phase worker (internal) -- the only human-involved phase, run by every application stage skill after REVISE. Opens with a mechanical Run step (./checks.sh markdown checks + the probe-card checker) whose ❌/FAIL blocks the gate green, seeds > CHECK: comments in stage docs (0-artifacts/*.md stay clean; artifact findings go to the Gate Ledger notes), presents the stage's exit criteria with per-item marks, proposes approve / revise / done, and on explicit approval writes the Gate Ledger row in STATUS.md and advances current_layer. Venue-scaled depth: simple venues confirm inline, complex venues get a full CHECK report. Persona presets + attendance modes let a stand-in approve ONLY in unattended runs. Renamed from haipipe-application-gate (paper-alignment 2026-07-06). Trigger: check, gate, approve stage, exit criteria, /haipipe-application check."
argument-hint: "[stage: seed|descriptions|themes|claims|advice|pitch|narrative|display|section-edit|draft] [--persona strict|balanced|creative|lenient] [--unattended[=Ns]]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "4.1.0"
  last_updated: "2026-07-07"
  summary: "Paper-check 1.7.0 enforcement port (alignment round 2, R2): step 1 Run executes ./checks.sh (markdown-safe subset) + the probe-card checker, any ❌/FAIL blocks the gate green; > CHECK: comments seeded in 0-lifecycle stage docs ONLY (R2c RULED: artifacts stay clean, artifact findings → Gate Ledger notes); revise reads the threads + > USER: replies. Persona/attendance, venue-scaled depth, and the Gate Ledger row format unchanged."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-application-check (CHECK phase worker)
======================================================

CHECK phase worker -- the 🧑 phase. Reviews the artifacts produced during one lifecycle stage's DRAFT-PROBE-REVISE and proposes the next move:

```
approve   → Gate Ledger row + advance current_layer to the next non-skipped stage
grow      → GROW-loop rungs (1a-1d) only (JL 2026-07-09: "after the check, they
            can think about adding more probes in the draft"): the gate ASKS
            "which data topics / probes are still missing?" -- the user's
            questions are the strongest lens; grow converts them to new slots
            + planned probe skeletons and re-opens DRAFT as [ROUND n+1].
            Approve at these rungs means: saturated AND the user added nothing.
revise    → loop back with feedback (same stage; the restarted phase reads the
            stage-doc > CHECK: threads + > USER: replies; upstream problems are
            named as loopback suggestions, the user decides)
done      → early exit: jump to draft (artifact) with remaining stages waived
            (recorded in the ledger notes)
```

A stage is only "done" when this approval is EXPLICIT. The system never auto-advances. Full protocol: `../../../wiki/08-stage-gate.md`.

Before any of that, CHECK opens with a MECHANICAL Run step (next section): a ❌ from `./checks.sh` or a FAIL from the probe-card checker means the gate CANNOT go green -- at any venue depth, under any persona.

Mechanical checks (step 1 -- Run)
==================================

Two checkers open every CHECK, before the judgment ask. They fire at EVERY venue depth -- venue scaling governs how the report is presented (inline vs full), never whether the checkers run.

1. Deterministic markdown checks -- `./checks.sh <artifact-or-dir> [--md <working-doc>] ...` (this folder; `--md` repeatable, `--depth N` widens the dir scan). Em-dash (❌, house rule), AI-voice tells (⚠️), TODO/FIXME (❌), bibtex-in-markdown (❌). Paste its ✅/⚠️/❌ lines into the CHECK report verbatim; exit 0 = no ❌. Paper's tex checks (`\cite`/`\ref`/`\label`, Pn.Sn, `--compile`) are deliberately absent -- application artifacts are markdown.

2. Probe-card invariants -- `sh ../../1-probe/haipipe-application-probe/check-probe-cards.sh <intervention_root>`. Any FAIL line (a `status: planned|dispatched|failed` card, a dangling ref, a `harvest: OWED` lane) means the gate CANNOT go green: a planned card surviving to CHECK is a probe that never ran.

A mechanical ❌/FAIL is not a judgment call: no persona preset, no `--unattended` timeout, and no venue-profile override can approve over it. Fix (revise), re-run, then proceed to the judgment ask.

`> CHECK:` comment seeding (stage docs ONLY)
=============================================

Every flagged item that lives in a 0-lifecycle stage doc (0-seed.md, 1a-descriptions.md, 1c-claims.md, ...) is planted as ONE `> CHECK:` comment at its exact spot -- one line stating the issue + the judgment needed, with concrete values, never an abstract description. The chat report is the map; the in-file threads are what the human walks.

0-artifacts/*.md are NEVER annotated: the artifact IS the deliverable text (unlike paper's .tex, where % comments never render), so a seeded comment would ship. Artifact-level findings go into the Gate Ledger notes column instead, quoted with file:line so they stay actionable (R2c RULED, JL 2026-07-07).

The human replies `> USER:` under each thread. On revise, the restarted phase (DRAFT/PROBE/REVISE) reads the stage-doc `> CHECK:` threads + their `> USER:` replies and responds to each -- an unanswered `> CHECK:` comment is surfaced back, never silently dropped. Resolved threads archive to the stage `_LOG`.

Gate Ledger (STATUS.md)
========================

On approve, append/update the row and bump `current_layer`:

```
## Gate Ledger

| Stage | Confirmed | Date | By | Notes |
|-------|-----------|------|----|-------|
| seed | yes | 2026-07-06 | JL | kill criteria set |
| claims | yes | 2026-07-06 | JL | settlement: light met |
| draft | yes | 2026-07-07 | JL | artifact: em-dash sms.md:4 fixed pre-approve |
```

`By` records who approved: the human (copilot mode) or `persona:<preset>` (unattended mode). The stage strip's ✅ means "confirmed in this ledger", NOT "artifact exists on disk". The Notes column is also where artifact-level checker findings land (0-artifacts/*.md are never annotated in-file -- see comment seeding above).

Venue-scaled depth (when CHECK fires)
======================================

```
simple (sms, push, reminder)      INLINE — present the exit criteria as one short
                                  checklist in the reply; user's "ok" = approve.
medium (checklist, email)         INLINE by default; full report on request (--report).
complex (dashboard, ui-card,      FULL — render the complete CHECK report (criteria
report)                           + evidence spot-checks + flags) before the ask.
```

The venue profile's README can override with `gate: inline | report`. Depth scales the REPORT, not the mechanics: `./checks.sh` + the probe-card checker run even for inline/simple venues (an sms message text still gets the em-dash/AI-voice/TODO scan).

Per-stage exit criteria
========================

```
seed:          kill criteria present? audience hunch specific? >=1 evidence path named?
descriptions:  every **D<n>** entry anchored (statistic + resolving pointer + as-of
               date)? no raw data / inline computation? no unconsumed
               [FORWARD -> CLAIMS] pointer in seed's _LOG?
themes:        every **T<n>** grounded (>=1 D id or project-side source)? hooks or
               context-only note per theme? Parked honest? no unresolved [STALE] tags?
claims:        every claim a **C<n>** line with theme tag + role + status + → PP ref?
               theme tags resolve to 1b? every probe a **PP<nn>** plan? Evidence
               Campaign complete (dispatch order + deps, no load-bearing GAP without a
               row)? settlement bar met against the campaign for the pinned depth
               (light/medium/full — claims skill §Settlement Gate)? no [STALE] tags?
advice:        every **A<n>** derived from >=1 resolving C id at/above the settlement
               bar? W-actionability passed? Rejected section honest? no [STALE] tags?
               (the LADDER GATE lands here for light/medium venues — batching per
               wiki/08; one approval writes the batched rungs' ledger rows)
pitch:         one-sentence goal testable? mechanism (theory of change) plausible?
               venue + audience named?
narrative:     arc follows venue rules? all load-bearing claims mapped to beats?
display:       every primary claim has a content element? every element has a job +
               evidence anchor? materialization routed (task refs) where needed?
section-edit:  every section's prose does its assigned job? flagged NEEDs resolved
               or explicitly parked?
draft:         venue self-review checklist passes? audience constraints met? artifact
               cites only adopted advice entries (adopted_A resolve: A -> C -> anchor)?
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
status:     approved | revise | done | awaiting-user
stage:      <stage-name>
mechanical: checks.sh <n ✅ / n ⚠️ / n ❌> · probe-cards <PASS | FAIL>
seeded:     <n> > CHECK: comments (stage docs; artifact findings → ledger notes)
criteria:   <n passed> / <m total> (+ per-item marks in the report)
ledger:     <row written or "pending user">
next:       <next stage command or the revise instruction>
```

Risk profile
=============

READ-ONLY on 0-artifacts/*.md -- the deliverable text is never annotated or modified. Writes: `> CHECK:` comments in 0-lifecycle stage docs (at flag sites), the STATUS.md Gate Ledger + current_layer (on approve), and a `[CHECK]` entry in the stage `_LOG`.
