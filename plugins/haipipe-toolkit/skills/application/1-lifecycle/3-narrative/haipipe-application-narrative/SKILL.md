---
name: haipipe-application-narrative
description: "Stage 3 of the intervention lifecycle (venue-GATED: fires per STATUS.md stages_skipped — required for email/dashboard/ui-card/report, optional for checklist, skipped for sms/push/reminder). Answers 'how do claims compose into a coherent message/experience?' Maps claim flow to the output's arc structure. Output: 0-lifecycle/3-narrative/3-narrative.md + _LOG_3-narrative.md. Markdown only. Trigger: narrative, arc, story flow, message structure, /haipipe-application narrative."
argument-hint: "[intervention-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "5.3.0"
  last_updated: "2026-07-19"
  summary: "Narrative stage (stage 3, venue-GATED + venue-ALIGNED): maps the settled claim/advice flow onto the venue's arc; it composes, never gathers — a beat exposing a NEW evidence gap raises a question SECTION in 1-probes/PPNN_<topic>.md (serves: 3-narrative) routed back to 1c-claims. History: ./CHANGELOG.md."
---

Skill: haipipe-application-narrative
======================================

Stage **3** of the intervention lifecycle, venue-GATED and venue-ALIGNED.
It decides one thing: how the settled claims and advice compose into a coherent arc — the flow of the final deliverable.
Same role as paper's narrative.

```text
[ladder] -> 2-pitch -> 3-narrative -> 4-display -> 5-section-edit
                       ^ THIS STAGE (venue-gated)
```

Read first: `../../../PHILOSOPHY.md`, and the probe layer's `../../../2-phase/1-probe/haipipe-application-probe/ref/per-stage-dispatch.md`.


## What's special: three things frame the arc

**1. It is venue-GATED — it may not fire at all.**
Read `STATUS.md | stages_skipped |`: required for email/dashboard/ui-card/report, optional for checklist (pulled in on user request), skipped for sms/push/reminder (the venue template already defines a fixed arc).
Invoked while skipped: say so and offer the frontier.

**2. It is venue-ALIGNED — the arc shape comes from the pinned venue.**
Arc rules come from `2-venue.md`'s Artifact Principles: sectioned venues (email/report) get a linear arc, drill-down venues (dashboard/ui-card) get levels.
Register comes from the pinned venue pack (tone-by-audience).
Retargeting rewrites the arc; the ladder underneath survives.

**3. It composes, it does not gather.**
The arc maps the 1d advice (A entries) and their backing claims onto positions — it produces no new evidence.
A beat exposing a NEW evidence gap routes BACK to 1c-claims (raises a question SECTION there), never gathers here.


## The four phases, in narrative

```text
DRAFT   read 1d-advice.md (the A entries the arc composes), 1c-claims.md (the evidence backstop),
        2-pitch.md (primary claim + theory of change anchor), 2-venue.md Artifact Principles;
        map each load-bearing claim/advice to an arc position per the venue's arc rules (haipipe-application-draft)
PROBE   rarely fires; a beat exposing a NEW evidence gap raises it as a question SECTION in
        1-probes/PPNN_<topic>.md (serves: 3-narrative), routed back to claims — never gathered here
        (haipipe-application-probe)
REVISE  arc coherence + register pass (haipipe-application-revise)
CHECK   3-narrative.md exists (when the venue requires it); every load-bearing claim mapped to an arc
        position; no beat anchored on a GAP claim; arc follows the venue's rules -> Gate Ledger row in
        STATUS.md (haipipe-application-check)
```

Precondition (before DRAFT commits): the arc leans only on claims meeting the venue's settlement bar (`STATUS.md claims_settlement`) — a load-bearing GAP claim cannot anchor a beat.
If one does, BLOCK with a loopback suggestion to claims.

Probe model: questions live in the FLAT cross-stage pool `1-probes/PPNN_<topic>.md`, one file per TOPIC.
Each ENTRY is one `## QX<n>` q-executor carrying `### q-executor` / `### q-consumer` / `### bank binding` / `### a-executor`; states are `planned|commissioned|answered|read|answered-local|failed`, and the stake stays in this doc's Q-consumer.
Dispatch is `Agent(haipipe-probe-q-executor-agent)`, not a gateway.
Mechanics: the probe layer's `ref/per-stage-dispatch.md`.


## The artifact

`0-lifecycle/3-narrative/3-narrative.md` — full skeleton, with the per-venue templates, in `ref/narrative-template.md`:

```text
Arc structure       one numbered position per beat, each anchored to a C/A id; venue-shaped
                    (linear positions for sectioned venues, levels for drill-down venues)
Claim -> arc mapping one line per load-bearing claim/advice: where it lands + its job there
Q-consumer          rare narrative-level questions, one `## Q-Narr-<n>` block each (Ask / Why / Answer): a beat's NEW gap, routed back to claims
```

Sidecar: `_LOG_3-narrative.md` (phase journal).
Formatting: `=====` title / `-----` sections; content uses no `#`, Q-consumer questions use `## Q-Narr-<n>`; one sentence per line.
Markdown only (argument documents need no compilation).


## Exits

```text
promote -> /haipipe-application display   what content element carries each claim
```

WRITES the `3-narrative/` stage folder only.
End every reply with the closing block (stage line via `../../../haipipe-application/stage-strip.sh`).
