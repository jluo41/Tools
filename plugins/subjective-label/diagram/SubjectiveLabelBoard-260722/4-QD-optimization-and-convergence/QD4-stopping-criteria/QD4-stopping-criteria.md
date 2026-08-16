# Stopping calibration: require quality, stability, coverage, and controlled risk
state: ✅ SETTLED
owner: JL
method: Stop only when four gates pass for K consecutive comparable checkpoints and the human confirms the concept is ready to freeze.

## Opening
When may repeated Calibration Rounds stop without confusing diminishing returns with success?
A small improvement is meaningful only after quality is already high enough, important regions are covered, and unresolved risk is bounded.
The decision must hold across consecutive comparable checkpoints rather than one convenient batch.
This page fixes the four-part gate, consecutive-round rule, human signoff, and the separation between calibration stop and corpus completion.

**Where this page sits**: QD2 supplies comparable audit evidence, QD3 supplies coverage and stability evidence, and QE1 begins the final test only after this page passes.

**Why it matters**: A stable score near 0.60 is a failed plateau, while labeling every row with an untested executor is completion without reliability.

## Writing Style
**Language and sentences**: State each threshold, population, version, and consecutive-round count explicitly.

**Logic**: Use conjunction across gates and never replace a failed gate with strong performance elsewhere.

**Status**: Distinguish continue, hold, stop calibration, ready for final test, and corpus complete.

## Diagram
**Stop gate**: four conditions and a human ruling must pass together across K checkpoints.

```text
📊 quality floor ─────┐
📉 stability plateau ├──▶ K consecutive rounds ──▶ 🧑 signoff
🗺 coverage gate ─────┤                                  │
🚨 risk gate ─────────┘                                  ▼
                                                🛑 stop calibration
                                                        │
                                                        ▼
                                                  QE1 sealed test
```

## Content

The four gates below are ANDed, never traded off against one another, and QD4-Display1 states that rule exactly.

### 1 · Quality gate
**Minimum performance**: representative audit evidence must clear the project threshold before plateau can matter.

```text
📊 quality
├── macro or balanced score
├── human correction rate
├── per-class minimum
├── key-region minimum
└── uncertainty interval
```

#### 1.1 · Comparable audit only
The quality floor uses QD2's probability or weighted audit protocol.
Raw challenge-batch error, model internal agreement, and public-dataset analogy cannot substitute for project-specific human correction evidence.

#### 1.2 · Distributional protection
The gate checks per-class and high-risk region performance, especially NONE confusion and known consensus-failure strata.
A high overall score cannot hide one failed class or unmeasured boundary.

### 2 · Stability gate
**Diminishing returns**: policy and audit improvement must remain small for a configured number of comparable rounds.

```text
📉 stability for K rounds
├── audit gain ≤ epsilon
├── few substantive policy edits
├── low new-boundary yield
└── no unresolved concept revision
```

#### 2.1 · Consecutive checkpoints
K and epsilon are project configuration chosen before the final stopping sequence is interpreted.
Changing the audit protocol, target population, executor, or semantic construct restarts the comparable sequence.

#### 2.2 · Low plateau fails
A plateau below the quality floor does not pass.
It triggers redesign, more evidence, a stronger executor investigation, a bounded claim, or an explicit project hold.

#### 2.3 · Policy stability
Most recent edits should be editorial or wrapper-only, with few new semantic rules or boundary changes.
One unresolved concept revision prevents a stability pass.

### 3 · Coverage and risk gates
**Safety condition**: the current evidence map and risk ledger must support the intended use.

```text
🗺 coverage
├── H · L · N
├── HL · LN · HN · HLN
├── corpus strata
└── novelty search

🚨 risk
├── shared errors
├── impact queue
└── unresolved items
```

#### 3.1 · Coverage disposition
Every required class, region, and material corpus stratum meets its evidence minimum or has an accepted scarcity explanation.
Search failure is not evidence that a region does not exist.

#### 3.2 · Risk disposition
No open high-severity risk lacks an owner, mitigation, or explicit JL acceptance.
Accepted risk narrows the claim and remains visible in the final report.

### 4 · Decision states
**Lifecycle separation**: stopping calibration opens final evaluation; it does not declare the full corpus reliable.

```text
🔁 continue round   one or more gates fail with a useful next batch
⏸ hold             quality cannot improve under current design
🛑 stop calibration all gates pass + human signoff
🧪 final ready      G* frozen and QE1 protocol opened
📦 complete         production + final corpus audit pass
```

#### 4.1 · Human signoff
JL reviews the gate packet and confirms that the current policy matches the intended concept closely enough for final testing.
The agent may recommend a state but cannot supply this semantic signoff.

#### 4.2 · Freeze boundary
The accepted checkpoint becomes G* and the development pool closes.
Any later semantic change invalidates the stop and returns the project to calibration.

#### 4.3 · Separate completion signal
Corpus exhaustion may end item processing, but it cannot waive the final-test and audit gates.
Full-corpus completion is settled only under QE3 and QE4.

## Aims

### A1 · 📊 Quality gate
- A1.1 · Calibration cannot stop on a low or unrepresentative plateau.
  **Done when:** Comparable audit quality and protected strata clear configured floors.

### A2 · 📉 Stability gate
- A2.1 · Diminishing returns hold across K consecutive comparable checkpoints.
  **Done when:** Audit gain, semantic edits, and discovery yield meet the stability settings.

### A3 · 🗺 Coverage and risk gates
- A3.1 · Material gaps are closed, accepted, or visibly blocking.
  **Done when:** QD3's coverage matrix and risk ledger satisfy the project policy.

### A4 · 🛑 Decision states
- A4.1 · Human signoff freezes G* without claiming that production is complete.
  **Done when:** Stop, final readiness, and corpus completion remain separate states.

## States

### A1 · 📊 Quality gate
- ✅ A1.1 · Met; division 1 requires project-specific comparable quality.

### A2 · 📉 Stability gate
- ✅ A2.1 · Met; division 2 fixes consecutive-round plateau logic.

### A3 · 🗺 Coverage and risk gates
- ✅ A3.1 · Met; division 3 makes coverage and risk conjunctive.

### A4 · 🛑 Decision states
- ✅ A4.1 · Met; division 4 separates calibration, final evaluation, and completion.

## Files

### 🔗 Related Board Pages · what this Page READS BY SCOPE
- `reads · ALL` · [QD2 §2](4-QD-optimization-and-convergence/QD2-round-metrics/QD2-round-metrics.md)
  QD2 supplies the comparable quality series.
- `reads · ALL` · [QD3 page](4-QD-optimization-and-convergence/QD3-coverage-and-stability/QD3-coverage-and-stability.md)
  QD3 supplies coverage, stability, and risk evidence.
- `continues · ALL` · [QE1 page](5-QE-final-evaluation-and-completion/QE1-sealed-final-test/QE1-sealed-final-test.md)
  QE1 begins only after G* freezes.

### Contracts · what must carry this rule
- `../../ref/ref-contract.md`
  The metric contract must expose all four gates and comparable rounds.
- `../../ref/ref-stages.md`
  The lifecycle must keep calibration stop distinct from completion.

## Law
- 260806 JL · 🛑 Calibration stops only through a four-part consecutive gate
      Quality, stability, coverage, and risk must all pass for K comparable checkpoints, followed by human semantic signoff.

## Glossary
- 📊 **Quality floor**: the minimum project-specific audit performance required before stability can support stopping.
- 📉 **Stability plateau**: configured small improvement and low substantive policy change across consecutive comparable checkpoints.
- 🛑 **Calibration stop**: the freeze of G* and closure of development, not the completion of all corpus labels.

## Log
260806 · Reopened QD4 in DRAFT and replaced automatic lexicon generation with the approved stopping contract.
