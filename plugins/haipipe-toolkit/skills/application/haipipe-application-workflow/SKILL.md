---
name: haipipe-application-workflow
description: >-
  The RUN router of the Application family: drives one Application's TWO boards through six phases in two lanes, InsightBoard SCOPE, CLIMB, HANDOFF and DesignBoard FRAME, COMPOSE, ACCEPT, joined only at the PageX crossing. It owns phase derivation from disk, the dispatch of each page into haipipe-page-workflow, the partition-major climb order, and the three human gates that always block: probe release, handoff signing, and acceptance. It never contains page machinery and never crosses past ACCEPTED, because building and shipping are task-layer work. Use when an Application must be driven forward, when someone asks what the next runnable page is, when a run must stop at the right gate, or when a stalled Application needs its frontier named. Trigger: application workflow, run the application, drive the boards, next page, application frontier, application run, what is runnable, /haipipe-application-workflow.
metadata:
  version: "0.1.0"
  last_updated: "2026-08-23"
  summary: "New on 260823 (JL): the Application-level RUN head, split out as its own skill mirroring haipipe-page-workflow. Six phases in two lanes, three human gates, phase state derived from disk, every page dispatched into the page RUN loop."
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
        ⑤ has nothing to bind until ③ has a signed handoff
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

## Dispatch: one page at a time, into the page RUN

This skill selects a page and hands it to `haipipe-page-workflow` with its Page Type contract; it never runs a phase of a page itself.

```text
select   the frontier phase's first page whose inputs exist and whose gate is open
load     haipipe-page + the matching haipipe-page-for-<type> contract
run      haipipe-page-workflow over that ONE page until CHECK settles or HOLDs
fold     update the register cell or acceptance row the page settles
repeat   until the frontier phase closes or a gate blocks
```

A page whose inputs do not exist yet is not runnable, and naming WHY it is not runnable is this skill's answer, never scaffolding the missing input silently.

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

On a partition-major InsightBoard (`haipipe-application` `ref/partition.md`) phase ② has a fixed order, because the cross group consumes the mirrored ladders and every W page cites the verdict:

```text
1-F-full first  ─▶  partition groups mirror, in parallel  ─▶  X group
                                                               │ XI → XK → the verdict
                                                               ▼
                                              W pages last, all citing XK02
```

A rung-major board has no such constraint beyond each chain's own D→I→K→W order.

## Stop rules

- STOP at ⑥: ACCEPTED ends the Application. Building, shipping, and running the experiment are task-layer work, and this workflow never dispatches them.
- STOP at any gate: report and end, never wait in a loop.
- STOP on contradiction: a frontier that derives to two phases at once (a register says answered, the page says 🔴) is reported as a defect, never repaired silently.

## Receipt

Each run appends one line to `<application-root>/_runs/application/log.md`: date, frontier at entry, pages dispatched, gate that ended the run. One line per run; the page-level receipts under each board's `_runs/page/` remain the detailed record.

## Return

Return the frontier phase per lane, the pages dispatched this run with their CHECK outcomes, the gate now blocking (if any) with the person's owed decision, and the next runnable page once that gate clears.
