---
name: haipipe-page-for-knowledge
description: >-
  The Page Type contract for one KNOWLEDGE page on an InsightBoard: a supported proposition carrying strength, rival explanations and boundary conditions, derived from named Information rows. It claims; it does not advise. Use when a pattern must become something the design can lean on, when rivals must be recorded before a claim travels, or when a Wisdom page is about to counsel from an unstated claim. Trigger: knowledge page, proposition, strength, rivals, boundary conditions, page-type knowledge, /haipipe-page-for-knowledge.
metadata:
  version: "0.2.1"
  last_updated: "2026-08-23"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
  group-token: "K"
  outline:
    mode: fixed
    source: "this SKILL.md"
    shape: "Claim → Information Cited → Strength → Rivals → Boundary; the pooling-verdict page reads Knowledge Cited at division 2"
  parent: haipipe-page-for-task
---

# /haipipe-page-for-knowledge · state the proposition, with its strength and its boundary

Load `haipipe-page`, then `haipipe-page-for-task`, then this contract. Load `haipipe-plugin-probe` when reaching Task or Discovery sources and `haipipe-plugin-pagex` when citing another page on this board.

Declare `page-type: knowledge`. On a rung-major board this page lives in `<InsightBoard>/3-K-knowledge/K<NN>-<slug>/`; on a partition-major board (`haipipe-application` `ref/partition.md`) it lives in its partition group, `<NN>-<L>-<slug>/<L>K<NN>-<slug>/`, and the group token is the partition letter.

One page owes a reader exactly this: **what is true, how strongly, and where it stops being true**.

## Fixed Content outline

```text
### 1 · Claim               K<n> ids · one proposition each, stated plainly
### 2 · Information Cited   which I pages and which I rows, by id
### 3 · Strength            STRONG | MODERATE | WEAK, with the reason
### 4 · Rivals              other explanations, and which are not eliminated
### 5 · Boundary            population, window, unit, and what it cannot cover
```

- **Claim** states one proposition per `K<n>`. A claim spanning two mechanisms is two claims. On the pooling-verdict page (partition-major only) division 2 is **Knowledge Cited**: the verdict's subject is the heterogeneity claim itself, so its parent is that K row, one step and no further. Its verdict states exchangeability, POOL or SPLIT; the W-page obligations that follow are imposed by `ref/partition.md`, never asserted by the row.
- **Strength** is one of three words plus the reason, never a number implying precision the design cannot use.
- **Rivals** is required. A claim with no rivals listed has not been tested, it has been asserted.
- **Boundary** is what travels downstream with the claim and constrains every Wisdom row built on it.

A claim may be WEAK and still belong here. What it may not do is reach Wisdom without its strength travelling with it.

## Closing rule

This page closes when the proposition names its Information parents, its strength, its uneliminated rivals and its boundary.

## Closing checks

- Every K row cites the I rows it rests on; the pooling-verdict K row instead cites the heterogeneity K row, one step and no further.
- Strength is one of STRONG, MODERATE, WEAK, with a stated reason.
- Rivals are listed and each is marked eliminated or not.
- No K row recommends an action: that is Wisdom. A POOL/SPLIT verdict is a claim about exchangeability, not a recommendation; its consequences for W pages are `ref/partition.md`'s rules.
- The boundary is specific enough that a Wisdom page can test applicability against it.

## Chain law

```text
source/run → D<n> → I<n> → K<n> → W<n> → Design Handoff
```

Every page cites its parent page by id in its Source Map, and every ROW cites the parent ROW it derives from. No level cites a later level as evidence. Nulls, negatives and contradictions survive upward; a level may narrow what its parent said and may never broaden it.

A parent page changing REOPENS every child row that cited it. That propagation is why the levels are separate pages: one re-run touches one D page, and staleness travels by citation rather than by hand.

## Register

The question this page answers is registered once on `MT03-question-knowledge`, the register facing this rung; the board rollup on `MT04-question-wisdom` is what reassembles a chain spanning four pages. When the page is created, the LAP'S REGISTER PEN records this page's id in its question's Queue row (`⬜ <id>`): the write is the register's even when the mint occasions it, so the three pens stay uncrossed.

This variant owns no scripts.
