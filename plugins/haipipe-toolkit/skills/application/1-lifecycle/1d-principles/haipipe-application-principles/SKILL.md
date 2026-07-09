---
name: haipipe-application-principles
description: "Stage orchestrator for the intervention's 0-lifecycle/1d-principles/1d-principles.md: rung 1d of the venue-FREE evidence ladder (1a-descriptions -> 1b-themes -> 1c-claims -> 1d-principles) and the ladder's DELIVERABLE. Design principles: actionable directives (W-shaped), each derived from >=1 claim in the 1c ledger. Downstream venue-ALIGNED stages (pitch/narrative/display/artifact) read THIS doc as their primary input. Distinct from venue Artifact Principles (channel-how); these are content-what. Markdown only. Trigger: principles, design principles, social norms, message principles, what should the message do, /haipipe-application principles."
argument-hint: "[intervention-path] [--deposit <Pnn>]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.0.0"
  last_updated: "2026-07-09"
  summary: "New rung skill from the ladder restage (SOP-ladder-restage.md): 1d = the W rung and the ladder's deliverable. Paper delivers K, application delivers W: principles are directives derived from claims, actionability-tested, venue-FREE."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-application-principles
======================================

Stage orchestrator for **rung 1d** of the evidence ladder (venue-FREE) -- the ladder's **deliverable rung**. The user invokes this skill (or the `ladder` sweep); it drives the phases internally.

It answers one question:

```text
Which design principles should shape this intervention, and which claims ground each?
```

The evidence ladder (stage-1 family, all venue-FREE):

```text
1a-descriptions   what the data looks like
1b-themes         what patterns/topics emerge
1c-claims         what generalizes (the ledger)
1d-principles     what to do (the deliverable)   <- THIS RUNG
```

Paper delivers K (defended claims); application delivers W (an artifact that acts). This rung climbs the last step: it turns the ledger's claims into directives the artifact work can execute. A principle without a claim behind it is vibes -- the exact fabrication mode the ladder exists to prevent.

**Not the venue's Artifact Principles.** `2-venue.md` Artifact Principles are channel-HOW (length, cadence, format for THIS modality; venue-ALIGNED, rewritten on retarget). This doc is content-WHAT (what the intervention's content should do to work; venue-FREE, survives retarget). Downstream stages read both; they never merge.

## Artifact Spec

**Files produced:**
- `0-lifecycle/1d-principles/1d-principles.md` -- the design-principles ledger
- `0-lifecycle/1d-principles/_LOG_1d-principles.md` -- phase progress journal
- `0-lifecycle/1d-principles/_PROBE/PPNN_*.md` -- probe cards (rare; + index row in `1-probe-plans/README.md`)

**Canonical template (source of truth for section order + placeholders):** `ref/principles-template.md`

**Content structure (1d-principles.md):**

```text
Principles        one **P<n>** per directive: the directive in one sentence,
                  derivation (>=1 C id), scope/boundary, status
Rejected          directives considered and dropped, with the refuting C id or reason
```

- **One principle, one sub-item:** `**P1 - majority framing where compliance is high - active**` / `Use descriptive-norm framing only where cohort compliance > 50%.` / `Derivation: C1 (supported), C2 (weak - boundary caveat).` / `Scope: adult cohort; revisit if C2 settles.`
- **W-actionability test:** a principle must be executable -- "could the artifact stage write the exact message move from this line?" If not, it is a claim restated, not a principle; push it back to 1c.
- A principle citing only `weak` claims carries the caveat inline; whether that passes the gate is venue-scaled (see gate below).
- Ids `P<n>` are ladder-local; artifact/claim-audit trace artifact -> P -> C -> anchor.

**Formatting:** `=====` title, `-----` sections, `**bold**` sub-items, one sentence per line. No `#`/`##`/`###`.

## Phase Orchestration

```
principles invoked
  |
  v
DRAFT --> read 1c-claims.md (statuses + campaign) and 1b-themes.md; elicit
          taste on directive priorities; derive one P per load-bearing claim
          cluster; record Rejected candidates with reasons
          (internally calls haipipe-application-draft with this artifact spec)
  |
  v
PROBE --> rarely fires: derivation is in-stage work. A principle exposing a
          NEW evidence gap routes back as a 1c-claims/_PROBE/ card, never
          gathers here (internally calls haipipe-application-probe when it does)
  |
  v
REVISE -> actionability pass (every P survives the test), scope tightening,
          caveat wording (internally calls haipipe-application-revise)
  |
  v
CHECK --> the LADDER GATE lands here for light/medium venues (batched per
          wiki/08-stage-gate.md): every P derived from >=1 C at/above the
          venue's settlement bar? actionability passed? no unresolved STALE
          tags? user confirms -> Gate Ledger row(s) -> advance to venue/pitch
          (internally calls haipipe-application-check)
```

Phase visibility: announce every phase boundary (reply line + `[PHASE]` entry in `_LOG`); skip a phase only by an explicit logged verdict; CHECK is never implicit.

## Settlement coupling (venue-scaled, read at CHECK)

The venue's `claims_settlement` bar applies through the derivation chain:

```
light    a P may cite weak claims with inline caveat; GAP-derived P forbidden
medium   load-bearing P cite supported-or-weak-with-caveat; others may caveat
full     every P cites supported claims (judged verdicts) only
```

> CC: these derivation bars are CC defaults (no ruling) — confirm the three levels, especially "GAP-derived forbidden even at light".
> CC: P status vocabulary `active | caveated | stale` (see ref/principles-template.md) is also invented — confirm or rename.

## Done-criteria

- [ ] Every `**P<n>**` has a directive sentence, derivation (>=1 resolving C id), scope, status
- [ ] Every P passes the W-actionability test
- [ ] Derivations meet the venue's settlement bar (or the provisional `light` bar if unpinned)
- [ ] Rejected section lists dropped directives with reasons (may be empty)
- [ ] No unresolved `[STALE ...]` tags in this doc

## Principles

1. Derivation is mandatory: no P without a C. The ladder's whole point.
2. Actionable or it is not a principle -- push claim-restatements back to 1c.
3. Venue-FREE: what the content should do survives retarget; only HOW it renders (venue Artifact Principles) rewrites.
4. Negative wisdom is first-class: a Rejected entry with a refuting claim saves the next round from re-deriving it.
5. Deposit to the insight KB is ON-REQUEST only (`--deposit <Pnn>` files a W card via the insight door); the ladder doc is the primary record (ladder restage R7).

## Handoff

On CHECK confirm (this is usually the ladder gate): `promote -> /haipipe-application venue` (pin modality), or `-> /haipipe-application pitch` if venue already pinned. End the reply with the closing block (stage line via `../../../haipipe-application/stage-strip.sh`).
