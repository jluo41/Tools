---
name: haipipe-page-for-data
description: >-
  The Page Type contract for one DATA page on an InsightBoard: a run-bound set of observations with no interpretation. One page per coherent observation set, normally one task folder or one QA answer, cited by many Information pages so the same counts are never restated. Use when a task or discovery has produced numbers that other pages will cite, when a source re-runs and its observations must be refreshed in one place, or when an Information page is about to inline counts it does not own. Trigger: data page, observations, run-bound counts, page-type data, /haipipe-page-for-data.
metadata:
  version: "0.2.0"
  last_updated: "2026-08-28"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
  group-token: "D"
  outline:
    mode: fixed
    source: "this SKILL.md"
    shape: "Origin → Source and Run → Observations → Coverage and Gaps"
  parent: haipipe-page-for-task
---

# /haipipe-page-for-data · record what was observed, and name the run that produced it

Load `haipipe-page`, then `haipipe-page-for-task`, then this contract. Load `haipipe-plugin-probe` when reaching Task or Discovery sources and `haipipe-plugin-pagex` when citing another page on this board.

Declare `page-type: data`. On a rung-major board this page lives in `<InsightBoard>/1-D-data/D<NN>-<slug>/`; on a partition-major board (`haipipe-application` `ref/partition.md`) it lives in its partition group, `<NN>-<L>-<slug>/<L>D<NN>-<slug>/`, and the group token is the partition letter. Row ids stay `D<n>` either way: the partition letter belongs to the PAGE id, never to a row.

One page owes a reader exactly this: **what was observed, and from which run**.

## Boundary

```text
MT00-meta            what data EXISTS, at what grain     describes, never asks
MT01-question-data   what is ASKED of this rung          asks, never concludes
D page               what was OBSERVED, and whence       counts, never compares
I page               what pattern the observations form  rates, contrasts, segments
```

**A D page never compares.** A count, a value or a distribution is a D row; a rate, a ratio, a rank, a delta, a trend or an explanation is an I row, and writing one here does not cross the boundary so much as erase it. The test is mechanical: a row naming TWO groups, or carrying a denominator that is not its own population's, belongs one rung up. This is the most-broken rule on the board precisely because a rate feels like an observation.

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
- A re-run of the named source visibly reopens this page first, and on a partition-major board its partition mirrors with it, because one extract feeds every partition's D pages through different configs.
- If a register cell names this page `🟡 <id> final`, a `## Log` row here names that question id and why the remainder cannot close.

## Chain law

This rung sits in the six-level lifting chain stated ONCE for the family, at `haipipe-insight` §The Climb Law: MT00's extract → D → I → K → W → a signed Handoff, each rung citing only named ROWS of the rung below, nulls and contradictions surviving upward, a level free to narrow what its parent said and never to broaden it, and a parent's change REOPENING every child row that cited it. It is cited here and deliberately not copied: four contracts restating one law in four places is how a patch comes to contradict itself.

This rung owns no exception to it. A D row's parent is a RUN, never another page on this board, which is why staleness enters the chain here and travels outward by citation rather than by hand.

## Register

The question this page answers is registered once on `MT01-question-data`, the register facing this rung; the board rollup on `MT04-question-wisdom` is what reassembles a chain spanning four pages. When the page is created, the LAP'S REGISTER PEN records this page's id in its question's Queue row (`⬜ <id>`): the write is the register's even when the mint occasions it, so the three pens stay uncrossed.

**The 🟡 receipt duty.** When this page closes part of its question and cannot close the rest, its register cell reads `🟡 <this page> final` (`haipipe-page-for-question`) and THIS page owes the sentence licensing it: a `## Log` row naming the question id and why the remainder cannot close. The register pen writes the cell, the page writes the reason, and neither may write the other's half. A cell reading final over a page carrying no such row is the defect the pair exists to prevent, because settled-partial and abandoned are indistinguishable on disk otherwise.

This variant owns no scripts.
