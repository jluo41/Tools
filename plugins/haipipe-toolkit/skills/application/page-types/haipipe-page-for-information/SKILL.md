---
name: haipipe-page-for-information
description: >-
  The Page Type contract for one INFORMATION page on an InsightBoard: rates, contrasts, segments and distributions derived from named Data rows. It organises; it does not yet claim. Use when observations must be turned into a comparable pattern, when several Data pages must be combined, or when a Knowledge page is about to assert something with no derivation behind it. Trigger: information page, rates, contrasts, segments, derived pattern, page-type information, /haipipe-page-for-information.
metadata:
  version: "0.2.1"
  last_updated: "2026-08-23"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
  group-token: "I"
  outline:
    mode: fixed
    source: "this SKILL.md"
    shape: "Question → Data Cited → Derivation → Patterns → Null and Contradiction; the X contrast page reads Information Cited at division 2"
  parent: haipipe-page-for-task
---

# /haipipe-page-for-information · derive the pattern, from named Data rows

Load `haipipe-page`, then `haipipe-page-for-task`, then this contract. Load `haipipe-plugin-probe` when reaching Task or Discovery sources and `haipipe-plugin-pagex` when citing another page on this board.

Declare `page-type: information`. On a rung-major board this page lives in `<InsightBoard>/2-I-information/I<NN>-<slug>/`; on a partition-major board (`haipipe-application` `ref/partition.md`) it lives in its partition group, `<NN>-<L>-<slug>/<L>I<NN>-<slug>/`, and the group token is the partition letter.

One page owes a reader exactly this: **what pattern the observations form**.

## Fixed Content outline

```text
### 1 · Question            the bounded question this derivation serves
### 2 · Data Cited          which D pages and which D rows, by id
### 3 · Derivation          how each figure was computed, reproducibly
### 4 · Patterns            I<n> ids · rates, contrasts, segments, trends
### 5 · Null and Contradiction   what did NOT differ, and what disagrees
```

- **Question** restates the register question in derivable terms, with unit and window.
- **Data Cited** binds D pages through PageX. It never restates their counts. On an X contrast page (partition-major only) this division is **Information Cited** instead: a delta of rates has no D row of its own, so its parents are the MIRRORED I rows it subtracts, cited across partition groups. That is the one legal same-rung citation on the board.
- **Derivation** says how each figure was computed, so a reader can reproduce it.
- **Patterns** carries `I<n>` rows, each naming the D rows it came from.
- **Null and Contradiction** is required and may not be empty without a sentence saying nothing null was found. A pattern page that reports only what differed is selecting on the outcome.

## Closing rule

This page closes when every I row derives from named D rows and the nulls are visible.

## Closing checks

- Every I row names the D rows it derives from; on an X contrast page, the two mirrored I rows it subtracts.
- No I row asserts strength, cause, or a recommendation.
- Division 5 is populated or explicitly says nothing null was found.
- Every figure has a stated derivation a reader could repeat.

## Chain law

```text
source/run → D<n> → I<n> → K<n> → W<n> → Design Handoff
```

Every page cites its parent page by id in its Source Map, and every ROW cites the parent ROW it derives from. No level cites a later level as evidence. Nulls, negatives and contradictions survive upward; a level may narrow what its parent said and may never broaden it.

A parent page changing REOPENS every child row that cited it. That propagation is why the levels are separate pages: one re-run touches one D page, and staleness travels by citation rather than by hand.

## Register

The question this page answers is registered once on `MT02-question-information`, the register facing this rung; the board rollup on `MT04-question-wisdom` is what reassembles a chain spanning four pages. When the page is created, the LAP'S REGISTER PEN records this page's id in its question's Queue row (`⬜ <id>`): the write is the register's even when the mint occasions it, so the three pens stay uncrossed.

This variant owns no scripts.
