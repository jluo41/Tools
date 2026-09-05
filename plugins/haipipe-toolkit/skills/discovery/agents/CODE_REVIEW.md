# Discovery Agent Contract Review

Date: 2026-09-04

Scope: orchestrator, creator, reviewer, workers, and agent README

Canonical authority: `../workflow-phases/haipipe-discovery-inquiry/ref/workflow-table.md`

This file records the current agent-contract audit. It is not an alternate
workflow declaration.

## Current lifecycle

```text
D1 SCOPE -> PREPARE? -> ACQUIRE <-> SYNTHESIZE -> CLOSE
```

- `FULL` follows the whole D1 cycle and dispatches the independent Page
  workflow during SYNTHESIZE.
- `ENRICH` enters D1 ACQUIRE, then D1 SYNTHESIZE; it is not a separate
  allocation path.
- Page `00–04` owns Page mutations. The D1 root skips Page EVIDENCE and Page
  CONTENT creates no local writing Runs.

## Authority review

| Check | Verdict | Evidence |
|---|---|---|
| One domain workflow | PASS | D1 Inquiry owns the canonical Workflow Table; `metadata.workflow` is registry identity only. |
| Run commission | PASS | Only D1 ACQUIRE can allocate local paper/source Runs. |
| Duplicate behavior | PASS | An unchanged canonical Subject reuses its pair; changed analysis opens a new Run with `supersedes:`. |
| Bib mutation | PASS | Only D1 SYNTHESIZE rebuilds the derived aggregate Bib; reviewer comparison is read-only. |
| Page ownership | PASS | Page workflow owns Context, Outline, Content, and Check writes. |
| Closure order | PASS | Page `04 CHECK` closes before D1 CLOSE reconciles the Task Face. |

## Role separation

| Agent | Owns | Must not do |
|---|---|---|
| orchestrator | route cycles, dispatch roles, reconcile handoffs | write through creator or Page-phase authority |
| creator | SCOPE/PREPARE/ACQUIRE/CLOSE Task work and commissioned Results | invent citations or bypass duplicate/admission gates |
| reviewer | read-only validation and backward-route findings | mutate aggregate Bib, Runs, Results, or Page artifacts |
| search worker | candidate/source retrieval | admit Subjects or allocate Runs |

## Result

PASS for the 2026-09-04 contract revision. Fresh-context validation remains
the release gate recorded in the canonical Workflow Table.
