# Coverage and stability: know which parts of the concept remain unsafe
state: ✅ SETTLED
owner: JL
method: Track class, region, novelty, consensus-failure, human-consistency, rule-change, and unresolved-risk evidence separately.

## Opening
How can the project tell whether the current policy covers the corpus and whether the human concept has become stable enough to freeze?
High average agreement can hide an empty boundary region, a recurring unanimous error, or a human rule that changed earlier gold.
Coverage therefore asks where evidence exists, while stability asks whether human judgments and policy rules keep moving.
This page fixes the coverage matrix, human consistency checks, policy stability record, and unresolved-risk ledger.

**Where this page sits**: QD2 supplies round measurements; QD4 combines this page's evidence with the quality floor; QE1 begins only after the combined gate passes.

**Why it matters**: A project that stops after many easy H or NONE items may look large and accurate while remaining unsafe on the boundaries that define the trait.

## Writing Style
**Language and sentences**: Report counts, denominators, versions, and known absence rather than saying coverage is good or complete.

**Separation**: Keep lack of corpus examples distinct from lack of search effort and lack of human agreement.

**Authority**: Human test-retest measures stability but does not average away the identified semantic authority.

## Diagram
**Coverage ledger**: four evidence surfaces combine without collapsing into one score.

```text
🏷 class coverage      H · L · N
🗺 region coverage     H · L · N · HL · LN · HN · HLN
🌱 corpus coverage     clusters · sources · novelty
🧠 stability evidence  test-retest · rule diff · impact queue
             │
             ▼
        🚨 unresolved-risk ledger
```

## Content

### 1 · Semantic coverage
**Coverage matrix**: every class and diagnostic region receives evidence or a documented scarcity disposition.

```text
          H   L   N
centers   n   n   n
HL        n   n   ·
LN        ·   n   n
HN        n   ·   n
HLN       n   n   n
```

#### 1.1 · Count and diversity
Coverage records human-confirmed count, unique evidence patterns, source diversity, and policy rules exercised for each class and region.
Near duplicates do not substitute for distinct boundary evidence.

#### 1.2 · Sparse-region disposition
A region with few examples may be absent in the corpus, poorly retrieved, or genuinely rare.
The page requires search evidence and a reason before scarcity can be accepted.

### 2 · Corpus and failure coverage
**Risk search**: novelty and shared-error neighborhoods show where the current semantic map does not reach.

```text
🗄 corpus map
├── ✅ represented clusters
├── 🌱 novel clusters
├── 🚨 consensus-failure neighborhoods
└── 🕳 unreviewed source strata
```

#### 2.1 · Corpus strata
Coverage is reported across relevant source, time, language, length, metadata, and embedding clusters when those fields exist.
The target population definition determines which strata matter.

#### 2.2 · Consensus failures
Every audited unanimous error creates a named failure neighborhood and an expanded search.
That neighborhood remains open until its error rate and policy treatment satisfy the risk rule.

#### 2.3 · Novelty exhaustion
Later retrieval should produce fewer high-value patterns that no existing rule handles.
A low novelty yield counts only when the search method and eligible corpus remain comparable.

### 3 · Human and policy stability
**Stability evidence**: repeated human judgments and policy diffs reveal whether the target decision function still moves.

```text
🧑 human stability
├── blind test-retest
├── changed-label reasons
└── concept-revision flags

📜 policy stability
├── semantic diff count
├── boundary diff count
└── editorial-only share
```

#### 3.1 · Human test-retest
After the concept matures, the human re-labels a probability or stratified sample of prior items without seeing earlier answers or model predictions.
Agreement, changed reasons, and region-specific inconsistency are reported.

#### 3.2 · Policy stability
The checkpoint trajectory distinguishes semantic, procedural, casebook, wrapper, and editorial changes.
Stability means new rounds produce few substantive changes, not merely that the document length stops growing.

#### 3.3 · Backward impact
Clarification and concept-revision flags identify earlier items that may no longer match the current policy.
The impact queue must be reviewed, explicitly accepted, or remain visible as risk.

### 4 · Unresolved-risk ledger
**Open risk**: every known gap has an owner, severity, affected population, and terminal disposition.

```text
🚨 risk record
├── source + evidence
├── affected class or region
├── estimated scope
├── owner + next gate
└── resolved | accepted | open
```

#### 4.1 · Risk types
The ledger includes missing regions, low human consistency, consensus failures, unresolved items, concept drift, source shift, and model-family fragility.
Each risk links to its evidence rather than repeating a general warning.

#### 4.2 · Accepted risk
JL may accept a bounded residual risk for the stated use case.
The record names the consequence, mitigation, and claim limitation rather than marking the gap as solved.

#### 4.3 · Stopping input
QD4 reads the current ledger and coverage matrix.
An unknown or unowned high-severity risk blocks stopping even when average audit quality is high.

## Aims

### A1 · 🗺 Semantic coverage
- A1.1 · Every class and seven-region cell has evidence or a documented scarcity disposition.
  **Done when:** Counts, diversity, and search evidence are visible.

### A2 · 🌱 Corpus and failure coverage
- A2.1 · Novel strata and unanimous-error neighborhoods remain traceable until closed.
  **Done when:** Each discovered gap has a search and disposition record.

### A3 · 🧠 Human and policy stability
- A3.1 · Stability is measured through blind human retest and typed policy diffs.
  **Done when:** Concept changes and backward impacts cannot disappear inside editorial updates.

### A4 · 🚨 Unresolved-risk ledger
- A4.1 · Every material risk has an owner and terminal status.
  **Done when:** QD4 can inspect severity, scope, mitigation, and acceptance evidence.

## States

### A1 · 🗺 Semantic coverage
- ✅ A1.1 · Met; division 1 fixes the class-region matrix and scarcity rule.

### A2 · 🌱 Corpus and failure coverage
- ✅ A2.1 · Met; division 2 covers strata, novelty, and consensus failures.

### A3 · 🧠 Human and policy stability
- ✅ A3.1 · Met; division 3 fixes test-retest, diffs, and backward impact.

### A4 · 🚨 Unresolved-risk ledger
- ✅ A4.1 · Met; division 4 defines owned and accepted risk.

## Files

### 🔗 Related Board Pages · what this Page READS BY SCOPE
- `reads · ALL` · [QD2 §2](4-QD-optimization-and-convergence/QD2-round-metrics/QD2-round-metrics.md)
  QD2 supplies audit and policy-delta evidence.
- `continues · ALL` · [QD4 page](4-QD-optimization-and-convergence/QD4-stopping-criteria/QD4-stopping-criteria.md)
  QD4 applies the combined quality, stability, coverage, and risk gate.

### Contracts · what must carry this rule
- `../../ref/ref-contract.md`
  The metric contract must define coverage and human-consistency evidence.
- `../../ref/ref-assets.md`
  The artifact layout must preserve coverage matrices and the risk ledger.

## Law
- 260806 JL · 🗺 Item count is not coverage
      Calibration must cover classes, seven diagnostic regions, corpus strata, novelty, shared-error neighborhoods, and known concept impacts.

## Glossary
- 🗺 **Coverage matrix**: counts and evidence diversity indexed by final class and diagnostic region.
- 🧠 **Human test-retest**: blind re-annotation of prior items by the same semantic authority after concept maturation.
- 🚨 **Risk ledger**: versioned records of unresolved, accepted, and resolved threats to labeling reliability.

## Log
260806 · Reopened QD3 in DRAFT and replaced the classifier-training question with the approved coverage-and-stability contract.
