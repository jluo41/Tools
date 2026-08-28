---
name: haipipe-page-for-wisdom
description: >-
  The Page Type contract for one WISDOM page on an InsightBoard: what a Knowledge claim means for this application's audience, context and risk, plus the Design Handoff that is the only thing a DesignBoard may bind. It counsels; it never writes message copy. Use when a settled claim must become guidance, when a design need must be released, or when deployment data has refreshed a claim and the counsel built on it must be re-read. Trigger: wisdom page, counsel, design handoff, applicability, forbidden overreach, page-type wisdom, /haipipe-page-for-wisdom.
metadata:
  version: "0.3.2"
  last_updated: "2026-08-27"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
  group-token: "W"
  outline:
    mode: fixed
    source: "this SKILL.md"
    shape: "Context → Knowledge Cited → Counsel → Forbidden Overreach → Design Handoff"
  parent: haipipe-page-for-task
---

# /haipipe-page-for-wisdom · say what it means here, and hand it to design

Load `haipipe-page`, then `haipipe-page-for-task`, then this contract. Load `haipipe-plugin-probe` when reaching Task or Discovery sources and `haipipe-plugin-pagex` when citing another page on this board.

Declare `page-type: wisdom`. On a rung-major board this page lives in `<InsightBoard>/4-W-wisdom/W<NN>-<slug>/`; on a partition-major board (`haipipe-application` `ref/partition.md`) it lives in its partition group, `<NN>-<L>-<slug>/<L>W<NN>-<slug>/`, and the group token is the partition letter.

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
- **Counsel** carries `W<n>` rows, each naming its K parent. A counsel useful in practice still fails if no K parent warrants it. The verbs are do, avoid, leave undecided, or, on a partition-major non-template page only, defer to `<W id>`. A counsel may be CONDITIONED on the pooling-verdict K page, which counts as a K parent.
- **Forbidden Overreach** is required. It is the clause that stops a designer asserting a cause the data never established.
- **Design Handoff** exports finding, strength, boundary, source versions, design consequence, forbidden overreach, unresolved gaps, the `serves:` need id, and a `signed:` row. It contains no message copy. The `signed:` row is the handoff's human gate made testable: it reads `signed: ⬜` until a person's decision puts `signed: ✅ <initials> <YYMMDD>` there — written by the person, or RECORDED verbatim by the machine on the person's stated decision, the release/kill precedent — and a DesignBoard may bind ONLY a signed handoff. Its SEAT is the handoff block's LAST line, below SERVES, and its lowercase colon form is deliberate against the block's uppercase labels: it is a machine token a gate greps, not a content row. A deferring W page has no `signed:` row, because it exports no handoff.

**Only a W page carries a Design Handoff.** A question that stopped at K is not yet usable by a DesignBoard, and its register's Queue row shows exactly that.

**The deferral close (partition-major only).** Under a POOL verdict every non-template W page closes as a DEFERRAL: its Counsel is one row, defer to the template W by id, citing the pooling-verdict K page as its parent, and its Design Handoff division is a pointer to the template W's handoff. A deferring W page exports NO handoff of its own, so nothing downstream can bind it, which is the point. The deferral close is legal only when a POOL verdict page is cited, and the template W page may never defer.

## Closing rule

This page closes when every counsel names a K parent, the forbidden clause is written, and the handoff reads standalone. A deferral close instead requires exactly one counsel row deferring to the template W by id and citing a POOL verdict page.

## Closing checks

- Every W row names the K row it rests on.
- The counsel never exceeds what its K parent's strength and boundary support.
- Forbidden Overreach is populated.
- The handoff carries finding, strength, boundary, sources, consequence, forbidden, gaps, serves and a `signed:` row; a deferring W page instead points at the template W's handoff and exports none.
- `signed:` is `⬜` or a person's `✅ <initials> <YYMMDD>`; a machine writing it is a reported error.
- No final message copy appears anywhere on the page.
- A fresh Design agent can use the handoff without opening any D, I or K page.

## Chain law

```text
source/run → D<n> → I<n> → K<n> → W<n> → Design Handoff
```

Every page cites its parent page by id in its Source Map, and every ROW cites the parent ROW it derives from. No level cites a later level as evidence. Nulls, negatives and contradictions survive upward; a level may narrow what its parent said and may never broaden it.

A parent page changing REOPENS every child row that cited it. That propagation is why the levels are separate pages: one re-run touches one D page, and staleness travels by citation rather than by hand.

## Register

The question this page answers is registered once on `MT04-question-wisdom`, the register facing this rung, whose Queue division also carries the board rollup that reassembles a chain spanning four pages. When the page is created, the LAP'S REGISTER PEN records this page's id in its question's Queue row (`⬜ <id>`): the write is the register's even when the mint occasions it, so the three pens stay uncrossed.

This variant owns no scripts.
