# Round metrics: separate comparable quality from difficult-case learning
state: ✅ SETTLED
owner: JL
method: Report representative or weighted audit measurements apart from adaptive challenge yield and policy-change evidence.

## Opening
Which measurements can show that one annotation-policy version is better when each later human batch deliberately contains harder cases?
Raw error on B_t is not a stationary loss because the selector changes its distribution from round to round.
A probability-based audit slice supports quality and stopping, while challenge cases support policy discovery and boundary diagnosis.
This page fixes those score families, their denominators, and the rule against merging them.

**Where this page sits**: QC3 assigns audit and challenge roles; QC4 supplies human gold; QD4 uses only eligible metrics for stopping.

**Why it matters**: A worsening challenge score may mean the selector found harder evidence, while an improving easy batch may hide a poor policy.

## Writing Style
**Language and sentences**: Name the population, sampling protocol, denominator, policy version, and uncertainty for every metric.

**Separation**: Never put audit and challenge observations into one unlabeled accuracy or kappa value.

**Metric choice**: Use task-appropriate categorical or ordinal metrics and preserve per-class and per-region views.

## Diagram
**Two score families**: one supports claims and stopping; the other supports learning.

```text
🟢 AUDIT SLICE                  🔴 CHALLENGE SLICE
probability or weighted         adaptively selected
comparable protocol             changing difficulty
quality + stopping              discovery + diagnosis
          │                            │
          └────────▶ 📌 round report ◀─┘
```

## Content

### 1 · Correction records
**Pre-post comparison**: sealed P_t and final Y*_t create item-level execution-error evidence.

```text
🔒 P_t prediction
        versus
🏷 Y*_t human gold
        │
        ▼
📉 corrected class · rule · confidence · region
```

#### 1.1 · Correction loss
Correction loss records whether the pre-label class differs from human gold and may be summarized as error rate, macro-F1, balanced accuracy, or kappa.
Per-model results remain separate before any committee summary is reported.

#### 1.2 · Reason and region differences
The report also counts same-class but wrong-reason cases, predicted-region errors, confidence miscalibration, and NONE-specific confusion.
These diagnostic differences may motivate policy work even when class accuracy is unchanged.

### 2 · Audit metrics
**Comparable series**: an audit protocol represents one declared population with known or reconstructable selection weights.

```text
🎲 audit sample
├── population + strata
├── inclusion probability
├── policy and executor version
├── class and region metrics
└── interval or uncertainty
```

#### 2.1 · Fixed protocol
The audit may use a fresh probability sample each round or another weighted design with a stable target population.
The sampling rule must remain comparable even when the selected items change.

#### 2.2 · Required views
The report includes macro and balanced class performance, per-class precision and recall, confusion, consensus error, and key seven-region results.
Population estimates apply weights when the sampling design requires them.

#### 2.3 · Uncertainty
Point estimates include a confidence interval, bootstrap interval, or an explicit small-sample warning.
A sparse region cannot pass from an apparently perfect score with one item.

### 3 · Challenge metrics
**Learning yield**: adaptively selected cases measure what the round discovered, not ordinary corpus performance.

```text
🔴 challenge results
├── new-rule yield
├── new-boundary yield
├── consensus-failure yield
├── concept-revision yield
└── unresolved rate
```

#### 3.1 · Discovery measures
Challenge yield counts substantive new rules, boundary clarifications, shared model failures, novel evidence patterns, and backward-impact cases.
It also reports how many selected items taught nothing new.

#### 3.2 · No stationary-loss claim
Challenge error may rise because later rounds target more difficult cases.
It is shown by round and source stratum but is never treated as a directly comparable training-loss curve.

### 4 · Policy and round deltas
**Change evidence**: the report links metric movement to what changed in the annotation policy and selection process.

```text
📜 G_(t-1) → G_t
├── semantic edits
├── procedure edits
├── casebook edits
├── wrapper edits
└── editorial edits
        │
        ▼
📊 audit delta + 🔴 challenge yield
```

#### 4.1 · Policy diff counts
Each checkpoint counts additions, deletions, rewrites, example changes, and editorial-only changes by policy component.
Semantic and procedural changes are never merged with punctuation or formatting cleanup.

#### 4.2 · Comparable delta
Audit improvement compares the prior and current closed policies under the same declared protocol when possible.
If executor, sampling, or target population changes, the trajectory opens a new series rather than splicing incomparable values.

#### 4.3 · Round report
The report carries both score families, policy deltas, human time, reviewed-item count, and known limitations.
Its headline states whether evidence supports quality, learning, both, or neither.

## Aims

### A1 · 📉 Correction records
- A1.1 · P_t versus Y*_t produces typed class, reason, region, and confidence differences.
  **Done when:** Every comparison names the executor and policy version.

### A2 · 🎲 Audit metrics
- A2.1 · A comparable score series supports quality and stopping claims.
  **Done when:** Population, design, weights, metrics, and uncertainty are reported.

### A3 · 🔴 Challenge metrics
- A3.1 · Hard-case learning is measured without becoming a population estimate.
  **Done when:** Discovery yield and adaptive selection are explicit.

### A4 · 📜 Policy and round deltas
- A4.1 · Metric movement remains linked to policy and protocol changes.
  **Done when:** Every trajectory break or comparable delta is declared.

## States

### A1 · 📉 Correction records
- ✅ A1.1 · Met; division 1 defines pre-post execution differences.

### A2 · 🎲 Audit metrics
- ✅ A2.1 · Met; division 2 defines comparable quality evidence.

### A3 · 🔴 Challenge metrics
- ✅ A3.1 · Met; division 3 defines adaptive learning yield.

### A4 · 📜 Policy and round deltas
- ✅ A4.1 · Met; division 4 fixes policy diffs and trajectory breaks.

## Files

### 🔗 Related Board Pages · what this Page READS BY SCOPE
- `reads · ALL` · [QC3 §4](QC-selection-and-adjudication/QC3-compose-human-batch.md)
  QC3 assigns item roles and preserves selection probabilities.
- `continues · ALL` · [QD4 page](QD-optimization-and-convergence/QD4-stopping-criteria.md)
  QD4 consumes quality and stability evidence without using raw challenge loss.

### Contracts · what must carry this rule
- `../../ref/ref-contract.md`
  The metric contract must define correction, audit, challenge, final-test, and production-audit contexts.
- `../../ref/ref-stages.md`
  The lifecycle must produce one typed report at every checkpoint.

## Law
- 260806 JL · 📊 Audit quality and challenge learning are separate score families
      Only a comparable audit protocol supports round-to-round quality and stopping claims; adaptively selected cases report discovery yield.

## Glossary
- 📉 **Correction loss**: disagreement between a sealed executor pre-label and the final human-confirmed record.
- 🎲 **Audit slice**: a probability or weighted sample used for a declared quality population.
- 🔴 **Challenge slice**: adaptively selected difficult evidence used for policy discovery rather than population estimation.

## Log
260806 · Reopened QD2 in DRAFT and replaced the previous cascade question with the approved round-metric contract.
