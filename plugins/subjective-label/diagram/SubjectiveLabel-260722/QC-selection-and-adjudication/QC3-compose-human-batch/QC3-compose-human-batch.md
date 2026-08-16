# Human-batch composition: challenge the policy and audit its consensus
state: ✅ SETTLED
owner: JL
method: Compose B_t from disagreement, mismatch, novelty, coverage, and a stratified random consensus audit under a recorded human budget.

## Opening
How should the system reduce a broad pre-labeled candidate pool to the smaller batch a human will actually review?
The batch must spend most of its limited capacity on cases that can improve the policy while still checking whether unanimous models are jointly wrong.
Disagreement priority alone misses shared blind spots, and random sampling alone wastes the chance to learn difficult boundaries.
This page fixes the source pools, stratified consensus audit, quota logic, and selection provenance for B_t.

**Where this page sits**: QC1 creates C_t, QC2 seals P_t, and QC4 conducts blind human adjudication on the composed B_t.

**Why it matters**: The composition rule determines what the human learns, what can be measured, and whether later reliability claims have a probability sample behind them.

## Writing Style
**Language and sentences**: Use source-pool names consistently and state when a metric is representative or adaptively selected.

**Authority**: Selection may use model signatures, but it may not assign human gold or reveal votes to the human.

**Settings**: Express capacity and source quotas as recorded configuration with planning examples only.

## Diagram
**Batch mixer**: challenge sources and one probability audit share a finite human-review capacity.

```text
📦 C_t + 🔒 P_t
        │
        ├──▶ 🔴 class or rule disagreement
        ├──▶ 🟡 geometry-model mismatch
        ├──▶ 🌱 novelty and sparse coverage
        └──▶ 🟢 consensus strata ──▶ 🎲 random audit
                              │
                              ▼
                         💬 human batch B_t
```

## Content

### 1 · Source pools
**Evidence branches**: each source enters B_t for a named reason rather than through one blended uncertainty score.

```text
🔴 disagree  policy stress
🟡 mismatch  selector stress
🌱 novelty   coverage stress
🟢 consensus shared-error audit
```

#### 1.1 · Disagreement pool
Class disagreement and incompatible rule use receive high priority because they directly expose execution ambiguity.
If the pool exceeds capacity, sampling spreads across predicted classes, diagnostic regions, confidence bands, and disagreement patterns.

#### 1.2 · Mismatch and novelty pools
Items enter mismatch when retrieval geometry, predicted region, class votes, or cited evidence conflict.
Novel items and under-covered regions receive protected slots so the selector cannot repeatedly mine one familiar edge.

#### 1.3 · Consensus pool
Consensus items are grouped by predicted class, predicted region, confidence band, executor family, and any known risk stratum.
They remain eligible for human review even when all required executors agree.

### 2 · Consensus audit
**Probability sample**: a stratified random draw from consensus measures shared error instead of assuming it away.

```text
🟢 consensus pool
        │ stratify
        ▼
🏷 class × 🗺 region × 🌡 confidence
        │ random seed + inclusion probability
        ▼
🎲 consensus-audit slice
```

#### 2.1 · Random within declared strata
Items are selected randomly after strata and quotas are fixed and before human outcomes are known.
The manifest records inclusion probability or enough counts to reconstruct it.

#### 2.2 · Adaptive audit expansion
One consensus failure triggers a local search and larger audit in the affected class, region, executor, or language neighborhood.
This expansion is reported separately from the original probability sample.

#### 2.3 · No automatic gold path
Consensus items not sampled for human review remain model predictions with their provenance.
They may later receive a production disposition, but they do not enter D_t as human gold.

### 3 · Capacity and quotas
**Human budget**: source allocations are chosen before item identities are finalized and are reported with the round purpose.

```text
💬 capacity m_t
├── 🔴 challenge majority
├── 🟢 consensus audit minimum
├── 🌱 novelty and sparse coverage
└── 🔁 carryover unresolved items
```

#### 3.1 · Planning default
A capacity near 50 may begin with roughly half for disagreement, a protected consensus-audit share, and the remainder for novelty, coverage, and carryover.
These numbers are examples, not settled universal thresholds.

#### 3.2 · Purpose-specific mix
A refinement round may favor boundaries and rule disagreement.
A reliability round may increase representative or consensus-audit capacity while preserving a minimum challenge slice.

#### 3.3 · Overflow rule
When required source minima exceed capacity, the batch cannot silently drop the audit.
The system either increases human capacity, defers lower-priority challenge cases with provenance, or records a coverage hold.

### 4 · Batch manifest
**Selection record**: every included and deferred item retains the reason and probability attached to its source branch.

```text
🧾 B_t manifest
├── item id + source pool
├── stratum + rank
├── selection reason
├── probability + seed
├── blind-access state
└── deferred disposition
```

#### 4.1 · Pre-session freeze
B_t is frozen before the Human-AI Session begins.
Changing membership after seeing a human label creates a new manifest version and invalidates the original audit denominator.

#### 4.2 · Separate score families
The manifest marks each item as audit, challenge, coverage, carryover, or more than one with a declared primary role.
QD2 uses that role to prevent challenge loss from being reported as a population estimate.

## Aims

### A1 · 📦 Source pools
- A1.1 · B_t draws from disagreement, mismatch, novelty, coverage, and consensus for explicit reasons.
  **Done when:** Every selected item names its source pool and primary role.

### A2 · 🎲 Consensus audit
- A2.1 · Shared model error remains measurable through probability-based human review.
  **Done when:** Consensus strata, random seed, inclusion probabilities, and expansion rules are preserved.

### A3 · 💬 Capacity and quotas
- A3.1 · Human capacity cannot erase the minimum audit or coverage obligations silently.
  **Done when:** The quota table and overflow disposition are closed before item selection.

### A4 · 🧾 Batch manifest
- A4.1 · B_t is frozen, role-typed, and reproducible before the Session.
  **Done when:** Membership and selection provenance validate against one manifest.

## States

### A1 · 📦 Source pools
- ✅ A1.1 · Met; division 1 defines all evidence branches.

### A2 · 🎲 Consensus audit
- ✅ A2.1 · Met; division 2 protects a stratified probability audit.

### A3 · 💬 Capacity and quotas
- ✅ A3.1 · Met; division 3 fixes configurable allocation and overflow behavior.

### A4 · 🧾 Batch manifest
- ✅ A4.1 · Met; division 4 fixes pre-session membership and item roles.

## Files

### 🔗 Related Board Pages · what this Page READS BY SCOPE
- `reads · ALL` · [QC2 §3](QC-selection-and-adjudication/QC2-prelabel-and-seal/QC2-prelabel-and-seal.md)
  QC2 supplies sealed committee signatures for selection.
- `continues · ALL` · [QC4 page](QC-selection-and-adjudication/QC4-blind-adjudication/QC4-blind-adjudication.md)
  QC4 adjudicates the frozen B_t without early prediction exposure.

### Contracts · what must carry this rule
- `../../ref/ref-stages.md`
  The round reference must separate C_t, P_t, and B_t.
- `../../ref/ref-contract.md`
  The metric contract must distinguish audit and challenge roles.

## Law
- 260806 JL · 🎲 Every later human batch includes a stratified random consensus audit
      Disagreement receives priority, but unanimous model predictions never gain an automatic path into human gold.

## Glossary
- 💬 **Human batch B_t**: the frozen set that enters Human-AI review in Calibration Round t.
- 🟢 **Consensus audit**: a probability-based human sample from items with unanimous required executor predictions.
- 🔴 **Challenge item**: an adaptively selected disagreement, mismatch, boundary, or novelty case used for policy learning.

## Log
260806 · Reopened QC3 in DRAFT and replaced autonomous construct selection with the approved human-batch composition contract.
