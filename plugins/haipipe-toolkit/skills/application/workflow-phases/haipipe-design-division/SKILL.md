---
name: haipipe-design-division
description: >-
  DesignBoard workflow phase D4 and Folder contract for the Design Page's
  reader-facing unit divisions, renders, acceptance-or-emit terminals, and
  optional promoted principles. This phase owns the legacy design Page Face.
  Trigger: design division, accept a unit, emit insight need, promoted
  principle, D4, folder-kind design-division, /haipipe-design-division.
metadata:
  version: "1.0.4"
  last_updated: "2026-09-01"
  workflow: haipipe-design-workflow
  phase: D4
  folder_kind: design-division
  primary_face: page
  page_ruling: domain-gate
  legacy_page_type: design
  outline:
    mode: grammar
    source: "GD0-closed Brief + landed Insight Evidence Items + venue pack"
    shape: "design contract → insight use → principles → unit map → repeated message/unit divisions → rails → render/acceptance"
---

# /haipipe-design-division · make each judged unit decidable

Load `haipipe-folder`, `haipipe-page`, the Design door/workflow,
`haipipe-plugin-design`, `haipipe-plugin-outline/ref/item-table.md`, and the venue pack. Existing
Design Pages may retain `page-type: design`; new work resolves this phase as
`folder-kind: design-division`.

## Position

D4 follows GD3/GD4 and ends at the human GD5 decision. It grows the parent
Design Page at
`2-DS-design/DS<NN>-<audience>-<job>-<venue>/`, one page per audience ×
behavior job × primary venue. Venue is part of identity, never hidden in an
optional slug.

## Folder Kind

The Design Page is the reader-facing delivery system. Each landed Unit earns
one repeated division. The Page composes exact content and rails; it never
builds, ships, allocates an experiment, or measures an effect.

An optional promoted Principle is a subordinate D4 Folder role, not a workflow
phase and not a Page-Type skill. Default warrant stays inline on the card's
`stance:`. Promote only when the same warrant serves two or more Design Pages
or two InsightBoards conflict. The promoted rule is exactly:

```text
because <signed W handoff>, do <move>, within <rail>
```

It uses this phase's two faces with `role: promoted-principle` and never gains
an independent lifecycle.

## Input

The GD0-closed Brief and roster row; board `reads:`; judged unit; released card
and stance/grant; signed handoff versions; venue rails; current render; and any
promoted principle.

## Page Face

Expose Design contract, Insight use, principle use, ordered Unit map, one
division per unit, cross-unit rails, and exact render. Every unit division
carries id, recipient moment, audience job, refs, design move, exact content,
variants, rail, next trigger, and exactly one terminal:

```text
accepted: <reviewer> <YYMMDD> · handoff <W-id>@v<N> · render v<N>
emitted:  <YYMMDD> · <BR00 need id> · <what was missing>
```

## Task Face

Map the judged unit into one division; verify warrant/grant boundaries; build a
current render; present it to a person; record only that person's acceptance,
or emit the missing insight to BR00 and its register. A changed handoff,
content, venue constraint, or render clears only affected acceptance rows.
The Unit README remains `state: judged`; the division's `accepted:` row is the
single acceptance authority and Folder/PageX surfaces derive status from it.
Promoted principles carry one pinned W warrant, scope, rail, and declined
alternatives; a changed W reopens every citing division.

## Plugins

- `design` required for cards and units;
- `render` required before acceptance;
- `pagex` required for Brief, signed handoffs, and accepted prior Design;
- `outline` required for the Design Page;
- `runs` optional only when the designed unit itself owns a declared
  Run/Result pair; scripts remain optional.

## Gate and Closure

GD5 passes per division on a valid person's `accepted:` row with current
handoff/render, or an `emitted:` row whose BR00 need and register question
exist. Killed cards are terminal before this phase. The round may advance only
when every thread is accepted, emitted, killed, or still merely proposed.

## Handoff

Hand D5 the complete Design Page, terminal thread ledger, current renders,
promoted principles, receipts, and all prose surfaces changed this round.
Accepted units then leave Design only through the task/fielding layer.

## Files

- Design Page: `2-DS-design/DS<NN>-<audience>-<job>-<venue>/<stem>.md`
- Threads: `design/DU<NN>-<slug>/`
- Visible versions: `delivery/render/`
- Optional promoted principles: `1-P-principle/P<NN>-<slug>/`, owned here
