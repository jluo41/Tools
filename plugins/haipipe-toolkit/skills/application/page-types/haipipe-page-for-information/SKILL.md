---
name: haipipe-page-for-information
description: >-
  The Page Type contract for one INFORMATION page on an InsightBoard: rates, contrasts, segments and distributions derived from named Data rows. It organises; it does not yet claim. Use when observations must be turned into a comparable pattern, when several Data pages must be combined, or when a Knowledge page is about to assert something with no derivation behind it. Trigger: information page, rates, contrasts, segments, derived pattern, page-type information, /haipipe-page-for-information.
metadata:
  version: "0.3.0"
  last_updated: "2026-08-28"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
  group-token: "I"
  outline:
    mode: fixed
    source: "this SKILL.md"
    shape: "Question → Data Cited → Derivation → Patterns → Null and Contradiction; the X contrast page reads Information Cited at division 2"
  parent: haipipe-page-for-task
---

# /haipipe-page-for-information · derive the pattern, from named Data rows

A value's provenance in Content names its QA anchor by path; the run identity lives in the anchor, never in a bare date code in prose — the attribution rule and the provenance duty stop colliding when the path carries both.

Load `haipipe-page`, then `haipipe-page-for-task`, then this contract. Load `haipipe-plugin-probe` when reaching Task or Discovery sources and `haipipe-plugin-pagex` when citing another page on this board.

Declare `page-type: information`. On a rung-major board this page lives in `<InsightBoard>/2-I-information/I<NN>-<slug>/`; on a partition-major board (`haipipe-application` `ref/partition.md`) it lives in its partition group, `<NN>-<L>-<slug>/<L>I<NN>-<slug>/`, and the group token is the partition letter.

One page owes a reader exactly this: **what pattern the observations form**.

## Boundary

```text
D page                      what was OBSERVED, run-bound      counts, never compares
MT02-question-information   what is ASKED of this rung        asks, never concludes
I page                      what PATTERN the observations     derives, never claims
                            form
K page                      what is TRUE, and how strongly    claims, carries rivals
```

**An I page never claims.** A rate, a contrast, a segment, a distribution or a trend is an I row; strength, cause, because, therefore, mechanism and should are K's words or W's. The test is mechanical: a row a reader could dispute on any ground OTHER than arithmetic has stopped deriving and started claiming, and belongs one rung up with its rivals attached.

An I page is also where a COVARIATE is read. A cut of the data that is not an audience — a ZIP-level attribute, an income band, a drug class, an exposure history — is a column on this page, never a partition group, and `haipipe-insight-workflow`'s partition test routes it here by name.

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
- If a register cell names this page `🟡 <id> final`, a `## Log` row here names that question id and why the remainder cannot close.

## Chain law

This rung sits in the six-level lifting chain stated ONCE for the family, at `haipipe-insight` §The Climb Law: MT00's extract → D → I → K → W → a signed Handoff, each rung citing only named ROWS of the rung below, nulls and contradictions surviving upward, a level free to narrow what its parent said and never to broaden it, and a parent's change REOPENING every child row that cited it. It is cited here and deliberately not copied: four contracts restating one law in four places is how a patch comes to contradict itself.

This rung owns ONE exception, and it is the board's only legal same-rung citation: an X contrast page derives from MIRRORED I rows across partition groups, because a delta of two rates has no D row of its own (division 2 above).

## Register

The question this page answers is registered once on `MT02-question-information`, the register facing this rung; the board rollup on `MT04-question-wisdom` is what reassembles a chain spanning four pages. When the page is created, the LAP'S REGISTER PEN records this page's id in its question's Queue row (`⬜ <id>`): the write is the register's even when the mint occasions it, so the three pens stay uncrossed.

**The 🟡 receipt duty.** When this page closes part of its question and cannot close the rest, its register cell reads `🟡 <this page> final` (`haipipe-page-for-question`) and THIS page owes the sentence licensing it: a `## Log` row naming the question id and why the remainder cannot close. The register pen writes the cell, the page writes the reason, and neither may write the other's half. A cell reading final over a page carrying no such row is the defect the pair exists to prevent, because settled-partial and abandoned are indistinguishable on disk otherwise.

This variant owns no scripts.
