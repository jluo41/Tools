---
name: haipipe-page-for-wisdom
description: >-
  The Page Type contract for one WISDOM page on an InsightBoard: what a Knowledge claim means for this application's audience, context and risk, plus the Design Handoff that is the only thing a DesignBoard may bind. It counsels; it never writes message copy. Use when a settled claim must become guidance, when a design need must be released, or when deployment data has refreshed a claim and the counsel built on it must be re-read. Trigger: wisdom page, counsel, design handoff, applicability, forbidden overreach, page-type wisdom, /haipipe-page-for-wisdom.
metadata:
  version: "0.1.0"
  last_updated: "2026-08-20"
  summary: "Contextual counsel plus the Design Handoff. The only level a DesignBoard may bind, and the only one that may mention an audience."
  group-token: "W"
  outline:
    mode: fixed
    source: "this SKILL.md"
    shape: "Context → Knowledge Cited → Counsel → Forbidden Overreach → Design Handoff"
  parent: haipipe-page-for-task
---

# /haipipe-page-for-wisdom · say what it means here, and hand it to design

Load `haipipe-page`, then `haipipe-page-for-task`, then this contract. Load `haipipe-plugin-probe` when reaching Task or Discovery sources and `haipipe-plugin-pagex` when citing another page on this board.

Declare `page-type: wisdom`. This page lives in `<InsightBoard>/4-W-wisdom/W<NN>-<slug>/`.

One page owes a reader exactly this: **what to do about it here, and what must not be concluded**.

## Fixed Content outline

```text
### 1 · Context             the audience, venue and decision this counsel serves
### 2 · Knowledge Cited     which K pages and which K rows, by id
### 3 · Counsel             W<n> ids · do, avoid, or leave undecided
### 4 · Forbidden Overreach what the evidence does NOT support concluding
### 5 · Design Handoff      the exported block a DesignBoard binds
```

- **Context** is the first place an audience or a venue may be named. Everything below D through K stayed about the world; this division is where the application enters.
- **Counsel** carries `W<n>` rows, each naming its K parent. A counsel useful in practice still fails if no K parent warrants it.
- **Forbidden Overreach** is required. It is the clause that stops a designer asserting a cause the data never established.
- **Design Handoff** exports finding, strength, boundary, source versions, design consequence, forbidden overreach, unresolved gaps and the `serves:` need id. It contains no message copy.

**Only a W page carries a Design Handoff.** A question that stopped at K is not yet usable by a DesignBoard, and its register's Queue row shows exactly that.

## Closing rule

This page closes when every counsel names a K parent, the forbidden clause is written, and the handoff reads standalone.

## Closing checks

- Every W row names the K row it rests on.
- The counsel never exceeds what its K parent's strength and boundary support.
- Forbidden Overreach is populated.
- The handoff carries finding, strength, boundary, sources, consequence, forbidden, gaps.
- No final message copy appears anywhere on the page.
- A fresh Design agent can use the handoff without opening any D, I or K page.

## Chain law

```text
source/run → D<n> → I<n> → K<n> → W<n> → Design Handoff
```

Every page cites its parent page by id in its Source Map, and every ROW cites the parent ROW it derives from. No level cites a later level as evidence. Nulls, negatives and contradictions survive upward; a level may narrow what its parent said and may never broaden it.

A parent page changing REOPENS every child row that cited it. That propagation is why the levels are separate pages: one re-run touches one D page, and staleness travels by citation rather than by hand.

## Register

The question this page answers is registered once on `MT04-question-wisdom`, the register facing this group, whose Queue division also carries the board rollup that reassembles a chain spanning four pages. Write this page's id into its question's Queue row when the page is created.

This variant owns no scripts.
