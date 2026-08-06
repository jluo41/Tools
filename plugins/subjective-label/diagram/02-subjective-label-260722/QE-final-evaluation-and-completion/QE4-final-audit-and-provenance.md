# Final corpus audit: state what is reliable and why
state: ✅ SETTLED
owner: JL
method: Blindly re-label a probability sample from production, estimate weighted error, repair failed strata, and publish item-level provenance with bounded claims.

## Opening
What evidence allows the project to call the completed corpus reliable rather than merely fully processed?
A blind human probability audit must test machine-accepted labels across the production distribution and known risk strata.
If error exceeds the acceptance rule, the affected stratum returns to review or production is rerun under a new validated policy.
This page fixes the final audit, corrective loop, provenance tiers, deliverable package, and claim language.

**Where this page sits**: QE3 supplies the completed candidate corpus; QA1 defines the promised D* and audit trail; QF2 turns these records into artifact schemas.

**Why it matters**: Final model accuracy on T* does not prove that a million-item production run stayed within the same distribution or followed every route correctly.

## Writing Style
**Language and sentences**: Give denominators, weights, intervals, provenance shares, and unresolved limitations.

**Claims**: Say reliable relative to the identified human authority and stated population, not objectively correct.

**Repair**: Distinguish audit finding, affected stratum, correction action, and post-repair evidence.

## Diagram
**Reliability closure**: a probability audit can pass the corpus or reopen a bounded production stratum.

```text
📦 completed candidate corpus
          │
          ▼
🎲 blind final audit sample
          │
          ▼
🧑 human re-label
    ├──▶ ✅ error within rule ──▶ 📦 D*
    └──▶ 🚨 error too high ──▶ repair stratum ──▶ re-audit
```

## Content

### 1 · Final audit design
**Probability audit**: the sample supports a declared population estimate and protected-stratum checks.

```text
🎲 audit design
├── target production population
├── strata + oversampling
├── random seed
├── inclusion probability
├── blind human protocol
└── acceptance rule
```

#### 1.1 · Primary random sample
The primary audit is random or probability-based over machine-accepted production items.
Human-reviewed calibration and risk-queue items may be audited separately but do not inflate the machine-label estimate.

#### 1.2 · Protected strata
The design may oversample rare classes, seven-region boundaries, low-confidence bands, model routes, source platforms, and known shared-error neighborhoods.
Weighted population estimates and stratum diagnostics remain separate.

#### 1.3 · Blind labeling
The human applies G* without seeing production labels, confidence, route, or prior reasons.
The audit record preserves first pass, final pass, and any missing-context disposition.

### 2 · Acceptance and repair
**Correction loop**: audit evidence either closes the production policy or reopens the affected scope.

```text
📊 weighted error + interval
├── ✅ below acceptance rule
├── 🟡 uncertain due to sample size
└── 🔴 above rule
       │
       ▼
   repair + new audit
```

#### 2.1 · Acceptance rule
The project defines overall, per-class, and protected-stratum tolerances before interpreting the audit.
An interval that crosses the threshold remains uncertain rather than automatically passing.

#### 2.2 · Local repair
A failed stratum may receive expanded human review, stricter routing, executor change, or a new validated production run.
Only the affected scope is repaired when evidence supports a bounded failure.

#### 2.3 · Semantic failure
If audit errors reveal a missing semantic rule or concept revision, calibration reopens and the existing final-test claim no longer describes the updated policy.
The project follows QE1's invalidation boundary before issuing a new final claim.

### 3 · Provenance tiers
**Item evidence**: every final row states who or what supplied the terminal label and which audits support it.

```text
🥇 human-confirmed gold
🥈 audited machine-accepted
🥉 machine-accepted under tested policy
🚨 accepted unresolved
🚫 excluded or invalid source item
```

#### 3.1 · Human-confirmed
Human-confirmed includes calibration gold, sealed-test gold, risk-queue adjudication, and final-audit labels with their roles preserved.
These records are reliable relative to JL's documented concept and consistency.

#### 3.2 · Machine-accepted
Machine labels identify policy, executor, wrapper, thresholds, run, confidence, route, and applicable audit evidence.
An audited tier indicates direct membership in an audited stratum, not that the exact item was human-reviewed.

#### 3.3 · Unresolved and excluded
Accepted unresolved items carry reason, owner, use limitation, and whether downstream analyses must omit them.
Excluded records preserve the data-quality or population-scope reason.

### 4 · Final deliverables and claims
**Reliability package**: data, policy, tests, scorecards, audits, and limitations close together.

```text
📦 final package
├── 🗄 D* labels + provenance
├── 📜 G* + casebook + wrappers
├── 🧪 T* manifest + human gold
├── 📊 executor scorecards
├── 🎲 production-audit report
├── 🚨 residual-risk ledger
└── 🧾 version and run manifests
```

#### 4.1 · Corpus claim
The report states the fraction of items in every provenance tier and the estimated production error with uncertainty.
It names the target population, human authority, policy version, executor route, and audit date.

#### 4.2 · Guideline claim
The report supports guideline quality through sealed human fidelity, uplift, held-out executor transfer, region performance, and human consistency.
It does not claim universal construct validity from one person's subjective authority.

#### 4.3 · Reproducibility
Checksums and manifests join every output to its corpus, policy, model, configuration, and parent checkpoint.
A reader can trace any final row back to the event that created or accepted it.

## Aims

### A1 · 🎲 Final audit design
- A1.1 · Production reliability is tested through blind probability-based human evidence.
  **Done when:** Population, strata, weights, seed, protocol, and thresholds are frozen.

### A2 · 🔁 Acceptance and repair
- A2.1 · Failed or uncertain audit strata cannot be silently accepted.
  **Done when:** Each finding passes, expands, repairs, or reopens calibration with evidence.

### A3 · 🧾 Provenance tiers
- A3.1 · Every final item states its terminal authority and supporting audit path.
  **Done when:** Human, machine, unresolved, and excluded records remain distinguishable.

### A4 · 📦 Final deliverables and claims
- A4.1 · D*, G*, T*, S*, audit, risk, and manifests form one traceable package.
  **Done when:** Reliability claims name their human, population, policy, uncertainty, and limits.

## States

### A1 · 🎲 Final audit design
- ✅ A1.1 · Met; division 1 fixes final sampling and blind adjudication.

### A2 · 🔁 Acceptance and repair
- ✅ A2.1 · Met; division 2 fixes pass, uncertainty, repair, and semantic reopen paths.

### A3 · 🧾 Provenance tiers
- ✅ A3.1 · Met; division 3 defines item-level evidence states.

### A4 · 📦 Final deliverables and claims
- ✅ A4.1 · Met; division 4 closes the reliability package and bounded claims.

## Files

### 🔗 Related Board Pages · what this Page READS BY SCOPE
- `reads · ALL` · [QE3 §4](QE-final-evaluation-and-completion/QE3-complete-corpus.md)
  QE3 supplies terminal production records and route provenance.
- `constrained by · ALL` · [QA1 §2](QA-semantic-contract/QA1-system-contract.md)
  QA1 defines the final output and authority contract.
- `continues · ALL` · [QF2 page](QF-execution-contract/QF2-artifact-schema-config.md)
  QF2 gives the reliability package machine-readable schemas.

### Contracts · what must carry this rule
- `../../ref/ref-contract.md`
  The metric contract must define production-audit estimates and claim boundaries.
- `../../ref/ref-assets.md`
  The artifact layout must preserve final labels, audit evidence, risk, and manifests.

## Law
- 260806 JL · 🎲 A completed corpus becomes reliable only through final probability audit and provenance
      Failed strata return to bounded repair, and every final row states whether its authority is human, audited machine, machine, unresolved, or excluded.

## Glossary
- 🎲 **Final corpus audit**: blind human probability review of machine-accepted production labels after completion.
- 🧾 **Provenance tier**: the item-level evidence class that identifies who or what supplied and supported a terminal disposition.
- 📦 **Reliability package**: D*, G*, T*, scorecards, audits, residual risks, and manifests delivered together.

## Log
260806 · Created QE4 from QA0's final-audit, provenance, reliability, and bounded-claim rules.
