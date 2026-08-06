# Sealed pre-labeling: measure weak executors without anchoring the human
state: ✅ SETTLED
owner: JL
method: Run independent weak executors under one closed policy, preserve structured outputs, and seal P_t until human first-pass judgments are locked.

## Opening
How should several weaker language models pre-label C_t so their errors help the next round without changing what the human sees first?
Every executor must apply the same closed annotation policy independently and return a typed prediction rather than an informal vote.
The resulting P_t supports batch selection and later correction measurement, but it is neither gold nor an input to the human's initial judgment.
This page fixes the execution packet, output schema, sealing boundary, and failure handling.

**Where this page sits**: QC1 produces C_t; QC3 reads the sealed disagreement signatures to compose B_t; QC4 controls when predictions may be revealed.

**Why it matters**: If executors share answers or the human sees their votes too early, agreement becomes circular and pre-post correction no longer measures guideline transfer.

## Writing Style
**Language and sentences**: Use plain English and distinguish prediction, confidence, reason, and human gold in every example.

**Rationale boundary**: Request concise structured reasons and cited evidence, never hidden chain-of-thought.

**Reproducibility**: Name the policy, wrapper, executor, model version, decoding settings, and run id for every output.

## Diagram
**Sealed committee**: independent runs create P_t, while an access gate protects the human-first decision.

```text
📜 G_(t-1) closed + 📦 C_t
        │
        ├──▶ 🧠 LM A ─┐
        ├──▶ 🧠 LM B ─┼──▶ 🔒 P_t
        └──▶ 🧠 LM C ─┘       │
                              ├──▶ QC3 selection signatures
                              └──▶ open after human first-pass lock
```

## Content

### 1 · Frozen execution packet
**Common packet**: each executor receives the same semantic policy and item fields under a recorded wrapper.

```text
📦 packet
├── 📜 closed policy id
├── 📄 item id + text
├── 🧾 output schema
├── ⚙️ wrapper + settings
└── 🚫 no peer predictions
```

#### 1.1 · Policy identity
Every run names G_(t-1) and its checksum.
A draft guideline, later patch, or unversioned casebook cannot enter the committee packet.

#### 1.2 · Independent execution
Each executor labels every assigned candidate without seeing another executor's output.
Retries are separate run records rather than replacements of an inconvenient answer.

#### 1.3 · Comparable wrappers
The core annotation policy is shared across models.
Model-specific formatting wrappers may differ only when their differences are declared and preserved for the final scorecard.

### 2 · Typed pre-label record
**Record shape**: P_t keeps the predicted class, evidence, rule use, uncertainty, and executor provenance separately.

```text
🧠 pre-label
├── 🏷 predicted H | L | N
├── 🌡 confidence + uncertainty reason
├── 🔍 cited evidence
├── 📜 applied rule
├── ⚖️ rejected alternative
└── 🧾 model + version + run
```

#### 2.1 · Required prediction
The executor returns one of H, L, or N when the run contract requires a class.
Low confidence does not become NONE because NONE means absence of trait evidence.

#### 2.2 · Structured reason
The executor cites the decisive text span or implication, the applied policy rule, and the strongest rejected alternative.
This compact structure is sufficient for error diagnosis without collecting private internal reasoning.

#### 2.3 · Diagnostic region prediction
An optional predicted region may support QC3 selection.
It remains a model hypothesis and must not replace the human region record.

### 3 · Committee signatures
**Comparison layer**: item-level signatures expose disagreement, consensus, and rule divergence without aggregating them into truth.

```text
🧠 executor records
        │
        ├──▶ 🔴 class disagreement
        ├──▶ 🟡 reason or rule disagreement
        ├──▶ 🟢 class consensus
        └──▶ 🌡 confidence spread
```

#### 3.1 · Disagreement is multi-part
Two executors may choose the same class while citing incompatible evidence or rules.
The signature therefore records class agreement, region agreement, rule agreement, and confidence dispersion separately.

#### 3.2 · Consensus remains a hypothesis
Unanimous H, L, or N is a useful stratum for QC3.
It cannot be written into cumulative gold without human review because shared models may share one blind spot.

### 4 · Seal and access control
**Access boundary**: selection logic may read signatures, while the human-facing session cannot reveal predictions before the initial judgment is locked.

```text
🔒 P_t
├── ✅ selector reads derived signatures
├── 🚫 human first pass cannot read votes
├── 🚫 strong agent cannot hint at majority
└── 🔓 reveal after initial human record
```

#### 4.1 · Immutable seal
P_t is content-addressed and closed before B_t is finalized.
Later corrections append comparison records and never rewrite the original prediction.

#### 4.2 · Human blind period
The human and strong calibration agent may discuss the item text and prior closed policy.
They must not reveal committee labels, counts, confidence, or model reasons before the human first-pass record is saved.

#### 4.3 · Failure handling
A missing or malformed executor output is marked failed and excluded from the required-consensus denominator.
The system never imputes the committee majority as the failed model's answer.

## Aims

### A1 · 📦 Frozen execution packet
- A1.1 · Every weak executor applies a comparable, closed policy independently.
  **Done when:** The packet and run provenance identify all semantic and execution inputs.

### A2 · 🧾 Typed pre-label record
- A2.1 · Every successful output separates class, uncertainty, evidence, rule use, and provenance.
  **Done when:** P_t validates against one schema and NONE cannot encode doubt.

### A3 · 🧠 Committee signatures
- A3.1 · Agreement and disagreement guide selection without becoming gold.
  **Done when:** Class, reason, region, and confidence signatures remain distinct.

### A4 · 🔒 Seal and access control
- A4.1 · Human first-pass judgments are protected from committee anchoring.
  **Done when:** P_t closes before B_t and opens only after the initial human record is locked.

## States

### A1 · 📦 Frozen execution packet
- ✅ A1.1 · Met; division 1 fixes common policy identity and independent execution.

### A2 · 🧾 Typed pre-label record
- ✅ A2.1 · Met; division 2 defines the pre-label schema and rationale boundary.

### A3 · 🧠 Committee signatures
- ✅ A3.1 · Met; division 3 treats consensus and disagreement as selection evidence.

### A4 · 🔒 Seal and access control
- ✅ A4.1 · Met; division 4 fixes immutability, blind access, and failures.

## Files

### 🔗 Related Board Pages · what this Page READS BY SCOPE
- `reads · ALL` · [QC1 §4](QC-selection-and-adjudication/QC1-candidate-pool.md)
  QC1 supplies the versioned C_t manifest.
- `continues · ALL` · [QC3 page](QC-selection-and-adjudication/QC3-compose-human-batch.md)
  QC3 consumes committee signatures without opening them to the human.

### Contracts · what must carry this rule
- `../../ref/ref-schema.md`
  The schema reference must define a pre-label separately from human gold.
- `../../ref/ref-architecture.md`
  The architecture must enforce independent executors and the blind-period gate.

## Law
- 260806 JL · 🔒 Weak-model predictions are sealed evidence, not provisional gold
      P_t may guide selection and later diagnosis, while human first-pass judgment remains blind and human confirmation alone creates Y*_t.

## Glossary
- 🔒 **Sealed pre-labels P_t**: immutable weak-executor predictions created under G_(t-1) before human review.
- 🧾 **Structured reason**: a concise record of evidence, applied rule, rejected alternative, and uncertainty without hidden chain-of-thought.
- 🧠 **Committee signature**: the item-level pattern of class, region, rule, and confidence agreement across executors.

## Log
260806 · Reopened QC2 in DRAFT and replaced the previous corpus-scale question with the approved sealed-prelabel contract.
