---
name: haipipe-application-workflow
description: >-
  The RUN router of the Application family: drives one Application's TWO boards through six phases in two lanes, InsightBoard SCOPE, CLIMB, HANDOFF and DesignBoard FRAME, COMPOSE, ACCEPT, joined only at the PageX crossing. It owns phase derivation from disk, the dispatch of each page into haipipe-page-workflow, the partition-major climb order, and the three human gates that always block: probe release, handoff signing, and acceptance. It never contains page machinery and never crosses past ACCEPTED, because building and shipping are task-layer work. Use when an Application must be driven forward, when someone asks what the next runnable page is, when a run must stop at the right gate, or when a stalled Application needs its frontier named. Trigger: application workflow, run the application, drive the boards, next page, application frontier, application run, what is runnable, /haipipe-application-workflow.
metadata:
  version: "0.3.0"
  last_updated: "2026-08-23"
  summary: "0.2.0 (JL 260823, reviewer audit): every dispatch pins mode: copilot so page-auto cannot defer a gate tick past a gate; an explicit phase-to-frontier mapping table; signed defined as the person's tick on the handoff division; the dataset-first PageX alternative to a local handoff. 0.1.0: six phases, two lanes, three gates."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-application-workflow · six phases, two lanes, three gates

`haipipe-application` is the door and says what an Application IS.
This skill is the head of the Application WORKFLOW: it decides WHICH page runs next and WHERE the run stops for a person. It adds no page machinery of its own; every page it selects is driven by `haipipe-page-workflow`, and everything a probe reaches underneath stays with `haipipe-task` and `haipipe-probe`.

**Who owns what**:

```text
haipipe-application            what an Application IS · the verbs · the page types
haipipe-application-workflow   RUN · phase derivation · gates · the climb order
haipipe-page-workflow          the bounded loop each dispatched page runs
haipipe-task · haipipe-probe   the evidence layer underneath the probes
```

## The six phases, in two lanes

The lanes may start in either order, because Brief and Meta are both head pages and `haipipe-application` rules their order free. A single line would be a lie; the crossing is the only joint.

```text
🔎 InsightBoard lane                    🎨 DesignBoard lane
──────────────────────                  ──────────────────────
① SCOPE    MT00 + the four registers    ④ FRAME    BR00 brief · needs land on registers
② CLIMB    one D→I→K→W chain per        ⑤ COMPOSE  principle pages, then design pages
           registered question
③ HANDOFF  W pages settle               ⑥ ACCEPT   review · per-division acceptance
           ✋ a person signs the handoff             ✋ a person accepts · STOP
                       │                        ▲
                       └──────── PageX ─────────┘
        ⑤ has nothing LOCAL to bind until ③ has a signed handoff; a settled
        scope: task Page bound through PageX is the legal dataset-first
        alternative (door §Dataset-first), under which local ③ may stay empty
```

RUN is deliberately not ADVANCE: a reopened source drops a chain back into ② while ⑥ holds elsewhere, and two questions may sit in different phases of ② at once. The phase names name the FRONTIER, never a completed stage.

## Phase state is derived, never stored

No status file exists. Each invocation derives the frontier from disk, the same way `haipipe-application`'s Status verb does, and the two must never disagree:

```text
phase      done when, on disk
──────────────────────────────────────────────────────────────────────
① SCOPE    MT00 exists past 🔴 · MT01-MT04 exist · every question has a row
② CLIMB    every register cell is ✅, 🚫 with a reason, or an explicit routing
③ HANDOFF  every W page that closes carries a signed Design Handoff
④ FRAME    BR00 exists past 🔴 · every need it raises has a register id
⑤ COMPOSE  every P and DS page the Brief's needs imply exists and closed CHECK
⑥ ACCEPT   every DS division carries its acceptance row · then STOP
```

**Signed, concretely**: a handoff is signed when the W page's Design Handoff division carries the person's tick, the page family's human-gate field written by the person at that page's CHECK. This workflow reads the tick and never writes it.

**The mapping to the door's Status vocabulary** (the door's `frontier:` is one scalar; this table is what "never disagree" means):

```text
this skill        door frontier reads
──────────────────────────────────────────────────────────────
① SCOPE           meta
② CLIMB           insight:<id>       the frontier chain page
③ HANDOFF         insight:<id>       that id is a W page; the door has no
                                     handoff token, so ③ is CLIMB's last stop
④ FRAME           brief
⑤ COMPOSE         design:<id>
⑥ ACCEPT          review, then accepted
lanes diverged    the door's scalar reads the insight lane until ③ closes,
                  then the design lane
```

The door's second axis, `maturity:`, stays solely the Status verb's output; this skill neither reads nor writes it.

## Dispatch: one page at a time, into the page RUN

This skill selects a page and hands it to `haipipe-page-workflow` with its Page Type contract; it never runs a phase of a page itself.

```text
select   the frontier phase's first page whose inputs exist and whose gate is open
load     haipipe-page + the matching haipipe-page-for-<type> contract
run      haipipe-page-workflow over that ONE page · the packet ALWAYS sets
         mode: copilot, because auto defers approved:/accepted: onto the --owed
         ledger and would mechanically pass gates 1 and 3
fold     update the register cell or acceptance row ONLY on CLOSE; every other
         terminal (HOLD, missing input, version mismatch, human gate, a step or
         round limit) is a named non-settlement and the cell does not move
repeat   until the frontier phase closes or a gate blocks
```

A page whose inputs do not exist yet is not runnable, and naming WHY it is not runnable is this skill's answer, never scaffolding the missing input silently.

## The design lane delegates (0.3.0)

Phases ④⑤⑥ keep their places in this map, but their interior law is `/haipipe-design`'s since 260824: FRAME resolves `born-of:`, COMPOSE runs the card → release → arm-agent → judge cycle, and ACCEPT is the per-division row. This skill still derives the lane's frontier and still stops at its gates; it no longer states design-side rules of its own.

## The three gates always block

This workflow has no auto mode at the gates, because all three are a person's by contract:

```text
✋ probe release   inside ② per page: cards are PRESENTED after drafting and
                   dispatched only on explicit approval (JL ruling, standing)
✋ handoff         at ③: a Design Handoff is signed by a person, never ticked
✋ acceptance      at ⑥: the exact visible version is explicitly accepted
```

A blocked gate is a clean stop: report the frontier, the waiting artifact, and the person's owed decision, then end the run.

## Partition-major climb order

On a partition-major InsightBoard phase ② has a fixed order, because the cross group consumes the mirrored ladders and every W page cites the verdict. The order is THIS skill's rule; `ref/partition.md` rules the grammar only:

```text
F's D/I/K first  ─▶  each partition's D/I/K mirror, in parallel  ─▶  X group
                                                                      │ XI → XK → the verdict
                                                                      ▼
                                                     every W page last, template
                                                     included, all citing XK02
```

A rung-major board has no such constraint beyond each chain's own D→I→K→W order.

## Stop rules

- STOP at ⑥: ACCEPTED ends the Application. Building, shipping, and running the experiment are task-layer work, and this workflow never dispatches them.
- STOP at any gate: report and end, never wait in a loop.
- STOP on contradiction: a frontier that derives to two phases at once (a register says answered, the page says 🔴) is reported as a defect, never repaired silently.

## Receipt

Each run appends one line to `<application-root>/_runs/application/log.md`: date, frontier at entry, pages dispatched, gate that ended the run. One line per run. This location is new with this skill and has NO auditor; the page-level JSON receipts under each board's `_runs/page/` remain the audited, detailed record. Application phases are written ①-⑥ here; when a page phase (also ①-⑦) could be confused, prefix the lane emoji: 🔎② is CLIMB, plain ② in a page context is PROBE.

## Return

Return the frontier phase per lane, the pages dispatched this run with their CHECK outcomes, the gate now blocking (if any) with the person's owed decision, and the next runnable page once that gate clears.
