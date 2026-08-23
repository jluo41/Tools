---
name: haipipe-page-for-knowledge
description: >-
  The Page Type contract for one KNOWLEDGE page on an InsightBoard: a supported proposition carrying strength, rival explanations and boundary conditions, derived from named Information rows. It claims; it does not advise. Use when a pattern must become something the design can lean on, when rivals must be recorded before a claim travels, or when a Wisdom page is about to counsel from an unstated claim. Trigger: knowledge page, proposition, strength, rivals, boundary conditions, page-type knowledge, /haipipe-page-for-knowledge.
metadata:
  version: "0.1.0"
  last_updated: "2026-08-20"
  summary: "A proposition with strength, rivals and boundary. The last level that is still about the world rather than about this application."
  group-token: "K"
  outline:
    mode: fixed
    source: "this SKILL.md"
    shape: "Claim → Information Cited → Strength → Rivals → Boundary"
  parent: haipipe-page-for-task
---

# /haipipe-page-for-knowledge · state the proposition, with its strength and its boundary

Load `haipipe-page`, then `haipipe-page-for-task`, then this contract. Load `haipipe-plugin-probe` when reaching Task or Discovery sources and `haipipe-plugin-pagex` when citing another page on this board.

Declare `page-type: knowledge`. This page lives in `<InsightBoard>/3-K-knowledge/K<NN>-<slug>/`.

One page owes a reader exactly this: **what is true, how strongly, and where it stops being true**.

## Fixed Content outline

```text
### 1 · Claim               K<n> ids · one proposition each, stated plainly
### 2 · Information Cited   which I pages and which I rows, by id
### 3 · Strength            STRONG | MODERATE | WEAK, with the reason
### 4 · Rivals              other explanations, and which are not eliminated
### 5 · Boundary            population, window, unit, and what it cannot cover
```

- **Claim** states one proposition per `K<n>`. A claim spanning two mechanisms is two claims.
- **Strength** is one of three words plus the reason, never a number implying precision the design cannot use.
- **Rivals** is required. A claim with no rivals listed has not been tested, it has been asserted.
- **Boundary** is what travels downstream with the claim and constrains every Wisdom row built on it.

A claim may be WEAK and still belong here. What it may not do is reach Wisdom without its strength travelling with it.

## Closing rule

This page closes when the proposition names its Information parents, its strength, its unelimimated rivals and its boundary.

## Closing checks

- Every K row cites the I rows it rests on.
- Strength is one of STRONG, MODERATE, WEAK, with a stated reason.
- Rivals are listed and each is marked eliminated or not.
- No K row recommends an action: that is Wisdom.
- The boundary is specific enough that a Wisdom page can test applicability against it.

## Chain law

```text
source/run → D<n> → I<n> → K<n> → W<n> → Design Handoff
```

Every page cites its parent page by id in its Source Map, and every ROW cites the parent ROW it derives from. No level cites a later level as evidence. Nulls, negatives and contradictions survive upward; a level may narrow what its parent said and may never broaden it.

A parent page changing REOPENS every child row that cited it. That propagation is why the levels are separate pages: one re-run touches one D page, and staleness travels by citation rather than by hand.

## Register

The question this page answers is registered once on `MT03-question-knowledge`, the register facing this group; the board rollup on `MT04-question-wisdom` is what reassembles a chain spanning four pages. Write this page's id into its question's Queue row when the page is created.

This variant owns no scripts.
