---
name: haipipe-application-workflow
description: >-
  The crossing orchestrator for an Application's InsightBoard and DesignBoard.
  It does not invent P0-P4 phases: Insight I0-I5 and Design D0-D5 remain owned
  by their sibling workflows. This skill resolves the two frontiers, validates
  need and signed-handoff crossings, delegates one runnable unit, records the
  cross-board receipt, and stops at the owning workflow's gate. Use for whole
  Application status, next-board routing, or cross-board trace repair.
  Trigger: application workflow, run application, cross boards, next board,
  application frontier, signed handoff crossing, /haipipe-application-workflow.
metadata:
  version: "1.0.5"
  last_updated: "2026-08-31"
---

# /haipipe-application-workflow · cross two workflows without renaming them

Load `haipipe-application` and `haipipe-folder` first. Then load
`haipipe-insight-workflow` and `haipipe-design-workflow`. Those workflows own
all interior phases, gates, dispatch, and receipts. This skill owns only the
crossings between them.

## Ownership

```text
haipipe-insight-workflow   I0–I5 · one register cell at a time
haipipe-design-workflow    D0–D5 · one design thread at a time
haipipe-application-workflow
                           crossing state · delegation · cross-board receipts
haipipe-page-workflow      OUTLINE…CHECK inside one Folder's Page Face
```

There is no Application P0–P4 vocabulary. A status that compresses I/D phases
into a third phase machine loses the exact phase skill that owns each Folder.

## The crossing graph

```text
Design D0 Brief need
        │  X0 need-out
        ▼
Insight I1 Question → I2 Data → I3 Information → I4 Knowledge → I5 Wisdom
        │  X1 signed-handoff
        ▼
Design D0/D1/D4 consumption → D5 sealed → accepted candidate
        │  X2 leaves Application to task/fielding
        ▼
measured effect → X3 read-back → new/reopened Insight I2 Data Folder
```

X0 and X1 are inside the Application. X2 and X3 describe the outer handoff
boundary; implementation, allocation, execution, and measurement remain task
work.

## Crossing assertions

### X0 · Brief need to Insight question

- BR00 owns one neutral need id and target rung.
- Exactly one Insight register owns the corresponding QD/QI/QK/QW id.
- Both rows point to each other; neither contains a preferred answer.
- The need stays open until that register reaches a legal terminal.

### X1 · Wisdom handoff to Design

- The W Folder is closed under I5 and its `signed:` token records a person.
- When I5 used a pre-climbed Task RF parent, the I1 QW row and W PageX card pin
  that exact RF version. The RF itself is not a crossing artifact: X1 still
  starts from the local, contextual, signed Application W Folder.
- The owning I1 register cell is terminal under GI6 and its settlement receipt
  cites this exact signed W Folder; GI5 alone is not crossing-ready.
- PageX binds the exact W handoff path/version; no D/I/K prose crosses.
- The DesignBoard's `reads:` authorizes the source.
- The consuming Brief/Card/Division names why the handoff applies.

### X2 · accepted candidate outward

- The D4 division is accepted against current handoff and render versions.
- D5 sealed the round.
- The caller or Brief roster names one target executable Task Folder, its
  `task_type`, and one `requested_action`; this crossing never guesses or
  scaffolds the downstream owner.
- The target is an addressable Task Folder with `<task-stem>.md`,
  `workflow/`, and a PageX primary list at
  `evidence/pagex/<task-stem>.md`.
- The crossing writer stores
  `<target-task-folder>/workflow/inbox/application/<DS-id>-<division-id>-v<N>.yaml`
  and adds a whole-Folder PageX binding back to the exact DS Folder/version.
- The DS Folder's `outline/<DS-stem>-log.md` records the same packet path and
  target Folder. This skill does not accept the packet on the Task owner's
  behalf and does not build, ship, allocate, execute, or measure it.

`N` is the immutable candidate-packet revision for one
`(DS-id, division-id, target Task Folder)` tuple: start at `1`, increment for
each later emission, and never overwrite an earlier packet. It is independent
of design and render versions; those stay pinned inside `source`. Thus an
accepted render v3 normally crosses as packet v1 when it is the tuple's first
candidate.

The packet grammar is fixed:

```yaml
schema: haipipe.application-candidate/v1
packet_id: <DS-id>-<division-id>-v<N>
packet_version: <N>
state: proposed
source:
  application: <application-root>
  design_board: <board-path>
  folder: <DS-folder-path>
  division: <division-id>
  design_version: <hash-or-version>
  handoffs: [<exact W path@version>]
  warrants: [<exact promoted-P path@version>]
  render: <delivery/render/file@version>
  acceptance:
    log: <DS-folder>/outline/<DS-stem>-log.md
    record: "### <YYMMDD HHMM> · <division-id> accepted at <render-version>"
  pagedown: <D5 receipt path@version>
target:
  folder: <target-task-folder>
  task_type: <target contract key>
  requested_action: <build | field | deploy | measure>
```

Missing target, requested action, PageX binding, packet/source version stamp,
acceptance, or PageDown receipt is `X2 HOLD`; no abbreviated packet is a
crossing.

### X3 · measured effect back to Insight

- The Task/QA/report path and run identity resolve.
- I2 records the effect as run-bound Data, not as an updated Design claim.
- Every downstream I/K/W row and Design division citing the old version reopens.

## Frontier

Report the Application as a product of two native frontiers and one crossing,
never one scalar:

```text
insight: <board> · <cell> · I0..I5 · gate GI<n> · next
design:  <board> · <thread> · D0..D5 · gate GD<n> · next
crossing: none | X0 need-out | X1 handoff-ready | X2 outbound | X3 read-back
```

If several units are runnable, preserve each owning workflow's order. Do not
advance one chain past a missing parent or one design thread past a human gate
to make the whole Application appear further along.

## Dispatch

1. Resolve the Application root and paired/readable boards.
2. Ask each sibling workflow for its frontier from disk.
3. Validate any pending crossing assertion before dispatch.
4. If the user named a board/thread/cell, delegate exactly that unit.
5. Otherwise finish a ready crossing first; then delegate the earliest runnable
   native frontier without crossing a human gate.
6. Re-read both frontiers and write one cross-board receipt.
7. Stop on any sibling workflow stop.

Delegation is literal:

```text
Insight unit → /haipipe-insight-workflow
Design unit  → /haipipe-design-workflow
Page Face    → /haipipe-page-workflow, only when the phase asks
```

## Receipts

No central Application ledger is authoritative. Put the receipt on the two
surfaces that own the crossing:

```text
X0  BR00/outline/<BR00-stem>-log.md
    + Question/outline/<Question-stem>-log.md
X1  W/outline/<W-stem>-log.md
    + consuming BR00-or-DS/outline/<stem>-log.md
X2  accepted DS/outline/<DS-stem>-log.md
    + target workflow/inbox packet + reciprocal PageX
X3  Task QA/report + I2/outline/<I2-stem>-log.md
```

Each outline receipt is one `### YYMMDD HHMM · <headline>` record and names
source path/version, target path/version, assertion results, and the person when
a human decision was involved.

## Human gates

This crossing layer adds no human gate. It preserves the four gates owned by
the two native workflows:

```text
Insight  release a new Probe card · sign a W handoff
Design   release/kill a Card       · accept a Division
```

A recorded blanket remains a person's act over named existing artifacts.
Nothing here infers or schedules one.

## Stop rules

- Stop at any unresolved X0/X1/X2/X3 assertion and report both paths.
- Stop at a sibling human gate; never poll or auto-advance it.
- Stop when two phase skills claim the same Folder.
- Stop at accepted/sealed Design: fielding is outside the Application.
- Never create a compatibility Page-Type skill to repair a crossing.

## Return

```text
status: ok | blocked | failed
insight: <native frontier>
design: <native frontier>
crossing: <X state and assertion>
receipt: <paths written, or none>
next: <one delegated unit or one named gate>
```
