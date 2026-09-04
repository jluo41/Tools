# The Insight Page: one consumer-neutral DIKW chain
state: 🟡 PARTIAL · contract shipped · fresh-context design passed · open: runtime rerun specimen
page-type: insight
insight-target: wisdom
owner: JL

## Opening
How does executed Task work become knowledge that Paper and Application can reuse without entering the Task Folder?

A Task run produces evidence, not a reusable interpretation. One Insight Page holds a scoped D→I→K→W chain, keeps every step traceable, and exposes a consumer-neutral handoff through PageX. This page is the Task Board specimen for that contract.

**Covered here**: the reusable Page grain and its DIKW trace.

**Covered elsewhere**: QD4 owns the Probe-in/PageX-out boundary; `haipipe-page-for-task` owns one Task Folder and its run-bound reading.

## Writing Style
Use consumer-neutral language, one sentence per line, and name every source by Page or QA path rather than by a downstream claim.

## Diagram
**The knowledge wall**: execution reaches consumers only after DIKW settlement.

```text
Task/Discovery ── Probe ──▶ D ─▶ I ─▶ K ─▶ W ── PageX ──▶ Paper/Application
```

## Content

### 1 · Question and Scope
**Scope gate**: one question fixes the chain's grain before sources enter.
```text
question + population + time + exclusions → one Insight Page
```
What Page contract turns one bounded evidence question into a reusable Insight without inheriting a consumer's stake?

### 2 · Source Map
**Source boundary**: Probe may enter the two evidence banks and nothing downstream.
```text
Task Page / Task QA / Discovery Page / prior Insight → source manifest
```
The contract may read Task Pages, Task `QA/` answers, Discovery Pages, and prior Insight Pages. It never gives a downstream consumer a direct `results/` address.

### 3 · Data
**D row**: an observation stays bound to the run that produced it.
```text
D<n> = observation + unit + date + source pointer
```
Data rows are dated observations bound to a source run or Page. They carry no interpretation.

### 4 · Information
**I row**: a pattern names the exact Data parents it transforms.
```text
D1 + D2 + … → I<n> pattern / null / contradiction
```
Information rows name patterns derived from Data rows, including nulls and contradictions.

### 5 · Knowledge
**K row**: a supported proposition keeps strength, rival, and boundary visible.
```text
I parents → K<n> proposition | strength | rival | boundary
```
Knowledge rows state supported propositions, strength, rivals, and boundaries. Paper normally consumes this level.

### 6 · Wisdom
**W row**: an implication is legal only when a Knowledge parent warrants action.
```text
K parent → W<n> implication | condition | risk
```
Wisdom rows state actionable implications only when a Knowledge parent warrants them. Application normally consumes K/W together.

### 7 · Reusable Handoff
**PageX packet**: the export is bounded knowledge, never a copied evidence folder.
```text
finding + strength + boundary + sources + refreshed + unknowns
```
The handoff carries finding, strength, boundary, source Pages, refresh date, and unknowns in language that names neither Paper nor Application.

## Aims

### A2 · Source Map
- ✅ A2.1 · The contract forbids direct downstream reads of Task results.
  **Done when:** the shipped skill and this specimen both route sources through Task/QA/Page addresses.
  **Now:** Met in `haipipe-page-for-insight` 0.1.0; consumers read settled Page handoffs rather than `results/`.


### A3 · Data
- ⬜ A3.1 · Source reruns reopen dependent rows.
  **Done when:** a runtime specimen demonstrates stale detection against a changed run.
  **Now:** No runtime rerun/staleness specimen exists yet.


### A7 · Reusable Handoff
- ✅ A7.1 · A fresh consumer can use the handoff without Task-folder access.
  **Done when:** a cold agent builds a valid Brief or Narrative source selection from Division 7 alone.
  **Now:** Fresh-context validation on 260817 produced a consumer-neutral Division 7, held settlement on unbound sources, and sent downstream consumers through PageX only.


## Files

### 📋 Contracts
- `../../../../task/page-types/haipipe-page-for-insight/SKILL.md`
  The Page Type contract this specimen exercises.
- `../../../../task/haipipe-task/fn/insight.md`
  The user-facing Task door procedure that creates or resumes the Page.

## Log
260817 · Fresh agent correctly chose `insight-target: knowledge`, preserved Wisdom as `not targeted`, traced D→I→K without cross-level jumps, and routed further evidence through Insight-owned Probe.
260817 · JL ruled that the Insights Board is the Task Board and that DIKW belongs here rather than inside each Paper or Application.

- 260831 0113 · `## States` merged into `## Aims` (tick + `Now:` per Aim; asks and threads kept verbatim), skill 0.148.0