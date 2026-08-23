---
name: haipipe-page-for-data
description: >-
  The Page Type contract for one DATA page on an InsightBoard: a run-bound set of observations with no interpretation. One page per coherent observation set, normally one task folder or one QA answer, cited by many Information pages so the same counts are never restated. Use when a task or discovery has produced numbers that other pages will cite, when a source re-runs and its observations must be refreshed in one place, or when an Information page is about to inline counts it does not own. Trigger: data page, observations, run-bound counts, page-type data, /haipipe-page-for-data.
metadata:
  version: "0.1.0"
  last_updated: "2026-08-20"
  summary: "Observed, run-bound, uninterpreted. Shared upward: many I pages cite one D page, so a re-run refreshes one file."
  group-token: "D"
  outline:
    mode: fixed
    source: "this SKILL.md"
    shape: "Origin → Source and Run → Observations → Coverage and Gaps"
  parent: haipipe-page-for-task
---

# /haipipe-page-for-data · record what was observed, and name the run that produced it

Load `haipipe-page`, then `haipipe-page-for-task`, then this contract. Load `haipipe-plugin-probe` when reaching Task or Discovery sources and `haipipe-plugin-pagex` when citing another page on this board.

Declare `page-type: data`. This page lives in `<InsightBoard>/1-D-data/D<NN>-<slug>/`.

One page owes a reader exactly this: **what was observed, and from which run**.

## Fixed Content outline

```text
### 1 · Origin              which task, discovery or QA answer produced this
### 2 · Source and Run      run identity, extract date, the exact query or script
### 3 · Observations        the rows · D<n> ids · counts, values, distributions
### 4 · Coverage and Gaps   who is in, who is excluded, what is missing
```

- **Origin** names the producing task folder or QA file. It states no finding.
- **Source and Run** pins run identity and extract date, inherited from `MT00-meta`'s Freshness row. A number with no resolvable run is a defect, not a row.
- **Observations** carries `D<n>` rows: counts, values, distributions. No rate that compares two groups, because a comparison is Information.
- **Coverage and Gaps** states exclusions with reasons and what this set cannot show.

## Closing rule

This page closes when every D row names a resolvable run and a person has read the numbers against the origin's own question.

## Closing checks

- Every D row resolves to a run identity and an extract date.
- No row compares, ranks, rates or explains: those are Information.
- Exclusions carry reasons.
- A re-run of the named source visibly reopens this page and only this page first.

## Chain law

```text
source/run → D<n> → I<n> → K<n> → W<n> → Design Handoff
```

Every page cites its parent page by id in its Source Map, and every ROW cites the parent ROW it derives from. No level cites a later level as evidence. Nulls, negatives and contradictions survive upward; a level may narrow what its parent said and may never broaden it.

A parent page changing REOPENS every child row that cited it. That propagation is why the levels are separate pages: one re-run touches one D page, and staleness travels by citation rather than by hand.

## Register

The question this page answers is registered once on `MT01-question-data`, the register facing this group; the board rollup on `MT04-question-wisdom` is what reassembles a chain spanning four pages. Write this page's id into its question's Queue row when the page is created.

This variant owns no scripts.
