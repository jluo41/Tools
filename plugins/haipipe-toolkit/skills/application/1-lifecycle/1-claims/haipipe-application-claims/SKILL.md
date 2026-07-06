---
name: haipipe-application-claims
description: "Stage orchestrator for the intervention's 0-lifecycle/1-claims/1-claims.md: the venue-FREE claim/evidence inventory that tracks what must be true for this intervention to work and which K/W/evidence backs each claim (supported / weak / GAP). Written BEFORE the venue is pinned and unchanged on retarget; the pinned venue later sets how much of the ledger must SETTLE before artifact work (light/medium/full). Emits probe plans into _PROBE/ for gaps and backfills verdicts. Markdown only, prose subsections, no tables. Trigger: claims, claim ledger, what must be true, which K/W, evidence, supported, GAP, /haipipe-application claims."
argument-hint: "[intervention-path] [--backfill <PPNN>]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "4.0.0"
  last_updated: "2026-07-06"
  summary: "Claims stage on the paper-aligned contract: venue-FREE content (moved BEFORE venue in the spine), stage folder with _LOG + _EVIDENCE_ + _PROBE/ cards + 1-probe-plans/README.md index, settlement-depth-at-gate, enum supported|refuted|inconclusive, `plan from-need` retired. Drives DPRC phases internally."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-application-claims
==================================

Stage orchestrator for the **claims** stage (stage 1, venue-FREE). The user invokes this skill; it drives the phases internally.

It answers one question:

```text
What must be true for this intervention to work, and what evidence settles each claim?
```

Every claim the intervention relies on is its own prose subsection with a status and a source. The application does not produce evidence; it selects judged evidence (insight K/W cards, task results, discovery findings) and tracks what is still missing. Unsupported claims become probe plans; verdicts are backfilled here.

**Venue-FREE.** This ledger is written before the venue is pinned and survives retargeting: the K/W truth does not change when the channel changes. No slot-mapping, no channel framing, no template references here -- those are venue-ALIGNED and live downstream (pitch/display/artifact). What the venue DOES control is the required **settlement depth**, read at the gate (below).

## Artifact Spec

**Files produced:**
- `0-lifecycle/1-claims/1-claims.md` -- claim/evidence inventory
- `0-lifecycle/1-claims/_LOG_1-claims.md` -- phase progress journal
- `0-lifecycle/1-claims/_EVIDENCE_1-claims.md` -- evidence backing per claim
- `0-lifecycle/1-claims/_PROBE/PPNN_*.md` -- probe plans for evidence gaps (+ index row in `1-probe-plans/README.md`)

**Content structure (1-claims.md):** prose only, no tables (JL ruling, shared with paper claims).
- Claims -- one `### C<n> - <title> (<role>) - <status>` subsection per claim; body is a short paragraph: (S1) the claim, (S2) the backing evidence with its concrete anchor (K/W card id, task result path, discovery source), (S3) one-line interpretation for the intervention, (S4) caveat + source ref
- Pending Evidence -- probe plans not yet returned
- Coverage note -- a closing paragraph: which claims are load-bearing for the intended intervention and which are nice-to-have

**Claim roles:** `primary` (value proposition depends on it) · `enabling` (works without it, better with it) · `assumption` (taken as given; probe only if challenged).

**Status vocabulary:** `supported` · `weak` · `GAP`. A claim is `supported` only when it traces to a judged artifact (insight K/W card, probe verdict `supported`, or an equivalently reviewed result) -- never from intuition. Verdict words follow the PPNN enum: `supported | refuted | inconclusive` (the word `confirmed` is retired).

## Phase Orchestration

When the user invokes `/haipipe-application claims`, this skill drives the phases in order. The user does not call phase skills directly.

```
claims invoked
  │
  ▼
DRAFT ──→ illuminate existing claims, elicit taste, extract testable claims
          from the seed, scan insights/INDEX.md for candidate K/W, write one
          prose subsection per claim
          (internally calls haipipe-application-draft with this artifact spec)
  │
  ▼
PROBE ──→ link evidence to each claim, backfill verdicts, buffer probe plans
          in _PROBE/ for GAPs (+ index rows); dispatch only on `probe run`
          (internally calls haipipe-application-probe)
  │
  ▼
REVISE ─→ refine claim statements and evidence descriptions for clarity
          (internally calls haipipe-application-revise)
  │
  ▼
CHECK ──→ present exit gate (below); user confirms → Gate Ledger row → advance to venue
          (internally calls haipipe-application-check)
```

Phase visibility: announce every phase boundary (reply line + `[PHASE]` entry in `_LOG` + phase-line 🔥 moves); skip a phase only by an explicit logged verdict (`[PROBE] skipped -- <reason>`, phase line shows `--`); CHECK is never implicit.

## Probe Plans Buffer

GAP/weak claims buffer probe plans in `_PROBE/` rather than dispatching immediately. One card per need (`PPNN_<slug>.md`, numbering authority = the `1-probe-plans/README.md` index), statuses `planned | dispatched | read | verdicted`. Card anatomy + buffer convention: `../../../haipipe-application/fn/probe-plans.md` (mirror of paper's). Dispatch happens ONLY through `haipipe-application-probe` (`/haipipe-application probe run [PPNN]`) -- never by calling `/haipipe-probe` from here.

Claims-stage probes default to **mode: full** (the intervention needs committed verdicts, G1/G2/G3-judged); context questions elsewhere in the lifecycle default to light.

On verdict return (TRANSLATE lands it in the card's `## Verdict`): `--backfill <PPNN>` flips the claim's status from the verdict -- `supported` -> supported; `refuted` -> drop or reword the claim (never ship a refuted claim); `inconclusive` -> stays weak/GAP with the caveat recorded.

## Settlement Gate (venue-scaled, read at CHECK)

The ledger's CONTENT is venue-free; how much must be SETTLED before artifact work is venue-scaled. CHECK reads `STATUS.md | claims_settlement |` (written at venue pin; absent = not yet pinned, apply `light` provisionally):

```
light    (sms, push, reminder)      every claim the artifact will lean on is at least
                                    tied to a named K/W or marked "common knowledge";
                                    GAPs allowed if not load-bearing
medium   (checklist, email)         all primary claims supported or weak-with-caveat;
                                    load-bearing GAPs have probe plans (dispatch optional)
full     (dashboard, ui-card,       all primary claims supported (judged verdicts);
          report)                   every GAP has a probe plan, load-bearing ones verdicted
```

Exit criteria (all depths): every claim has a `### C<n>` prose subsection with role + status; no load-bearing GAP without a probe card; `_EVIDENCE_` links resolve; settlement bar (above) met for the pinned or provisional depth. On CHECK confirm, write the Gate Ledger row, set `current_layer` to `venue` (or `2-pitch` if the venue is already pinned).

## Principles

1. One `### C<n>` subsection per claim, prose only, no tables anywhere in the ledger.
2. Never mark `supported` from intuition; cite the judged artifact and its anchor.
3. No aspirational anchors: "the dashboard will show X" is not evidence; a supported claim cites a real value in a real file/card.
4. Overclaim guard: if evidence is I-level (in-sample pattern) but the claim needs K-level (generalizes), keep it `weak` and route a probe.
5. Venue-FREE: retargeting changes the required settlement, never the ledger's truth. If a claim only matters for one venue, say so in its caveat -- do not delete it on retarget.
6. The application reads the project KB (insights/INDEX.md first, bodies only when shortlisted) but never writes insight cards from here -- deposits belong to the probe/insight side.

## Handoff

On CHECK confirm: `promote -> /haipipe-application venue` (pin modality), or `-> /haipipe-application pitch` if venue already pinned. End the reply with the closing block (stage line via `../../../haipipe-application/stage-strip.sh`).
