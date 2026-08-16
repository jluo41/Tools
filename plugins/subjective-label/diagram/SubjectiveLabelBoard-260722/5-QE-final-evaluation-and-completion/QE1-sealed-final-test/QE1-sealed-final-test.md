# Sealed final test: reserve early, label after the policy freezes
state: ✅ SETTLED
owner: JL
method: Isolate unseen item identifiers at initialization, prohibit all development access, and create blind human gold only after G* is frozen.

## Opening
How should the project create a final human-gold test when the human concept itself becomes clearer during calibration?
Test identifiers must be reserved before development, while their human labels must wait until the mature annotation policy G* is frozen.
Neither weak executors nor the human may inspect those texts during round selection, policy optimization, or stopping.
This page fixes the sampling frame, access seal, late human labeling, diagnostic supplement, and invalidation rule.

**Where this page sits**: QB1 reserves the identifiers, QD4 authorizes the freeze, and QE2 uses the resulting T* under one final protocol.

**Why it matters**: A test labeled too early uses an immature concept, while a test inspected during development becomes another training set.

## Writing Style
**Language and sentences**: State timing, access roles, sampling frame, and invalidation conditions explicitly.

**Blindness**: Separate unseen item text, unseen model output, and unavailable prior human labels.

**Claims**: Keep representative population estimates distinct from region-stratified diagnostic results.

## Diagram
**Reserve-early label-late design**: the test stays sealed through calibration and receives mature human gold afterward.

```text
🗄 target corpus snapshot
├── 🔁 development pool
└── 🔒 sealed ids
        │ no text access during calibration
        ▼ after G* freeze
   🧑 blind human labeling
        │
        ▼
   🧪 T* human gold
```

## Content

### 1 · Sampling frame and reservation
**Test manifest**: identifiers are sampled from a declared target population before semantic development begins.

```text
🧾 sealed manifest
├── corpus version
├── sampling frame
├── random seed
├── item ids or encrypted handles
├── strata + inclusion probability
└── access-control record
```

#### 1.1 · Primary representative test
The primary T* is a random or probability sample from the target production population.
Its size is chosen for the desired uncertainty, class prevalence, human budget, and minimum meaningful difference.

#### 1.2 · External or fresh source option
The test may come from a separately collected same-population corpus when its sampling and comparability are documented.
Being outside the original N does not make it valid if the source population differs materially.

#### 1.3 · Reservation boundary
Only the manifest custodian may resolve sealed identifiers to text before the freeze.
Embeddings, clusters, retrieval, pre-labeling, and human browsing exclude them.

### 2 · Access seal
**Leakage prevention**: every development component receives an explicit deny rule and the seal records attempted access.

```text
🔒 T* before freeze
├── 🚫 candidate selector
├── 🚫 weak committee
├── 🚫 strong calibration agent
├── 🚫 human development sessions
└── 🚫 stopping metrics
```

#### 2.1 · No indirect use
Test texts cannot enter embedding prototypes, classifier training, casebook selection, prompt examples, or corpus summaries shown during calibration.
Metadata used for sampling is limited to variables declared safe before reservation.

#### 2.2 · Seal audit
The project records manifest reads, text resolution, exports, and failed access attempts.
Any unauthorized exposure opens an invalidation review.

### 3 · Late human gold
**Mature adjudication**: after G* freezes, the human labels T* without seeing executor predictions.

```text
📜 G* frozen + 📄 unseen test item
              │
              ▼
        🧑 class + region + uncertainty + reason
              │
              ▼
          🧪 final human gold
```

#### 3.1 · Policy availability
The human may use G* because it is the external form of the finalized concept.
No test outcome may change G* during the final claim.

#### 3.2 · Blind executor boundary
All candidate-model predictions remain sealed until the human test record is complete.
The human may take a second blind pass or resolve missing context, but model answers cannot adjudicate the gold.

#### 3.3 · Human consistency
A blind repeat sample may estimate intra-rater stability on T*.
Changed labels remain visible with reasons rather than being silently overwritten.

### 4 · Representative and diagnostic results
**Two test roles**: one estimates the target distribution; an optional supplement examines rare boundaries.

```text
🧪 T* primary      probability sample
🗺 T*_diag optional region-enriched supplement

🚫 never merge unweighted
```

#### 4.1 · Primary score
The headline model score uses the representative sample and its declared weights.
Class prevalence and uncertainty intervals accompany the result.

#### 4.2 · Diagnostic supplement
An optional region-stratified supplement ensures enough HL, LN, HN, and HLN evidence for analysis.
Its enriched error rates are reported separately or reweighted to a declared population.

### 5 · Invalidation
**One-shot claim**: using test outcomes to improve any scored component turns T* into validation data.

```text
🧪 test result
  ├── used only for final report  ✅ valid
  └── changes policy, wrapper,
      threshold, or executor      🚫 invalid for new final claim
```

#### 5.1 · What invalidates
Changing G*, a model wrapper, decision threshold, ensemble rule, model choice, or risk-routing policy after reading its T* result invalidates that result for the updated system.
The updated claim requires a new sealed test.

#### 5.2 · What remains allowed
The original frozen-system score may still be reported with its protocol and date.
Exploratory analysis is allowed after the final report when it is clearly labeled and not reused as a fresh test claim.

## Aims

### A1 · 🧾 Sampling frame and reservation
- A1.1 · T* begins as a reproducible sample from a declared target population.
  **Done when:** The manifest fixes corpus, seed, strata, inclusion, ids, and custodian.

### A2 · 🔒 Access seal
- A2.1 · Test text cannot influence calibration, stopping, or policy optimization.
  **Done when:** Every development actor is denied and access is auditable.

### A3 · 🧑 Late human gold
- A3.1 · The mature human concept labels T* without model anchoring.
  **Done when:** G* is frozen and all human records close before predictions open.

### A4 · 🗺 Representative and diagnostic results
- A4.1 · Population and boundary claims use separate declared denominators.
  **Done when:** Primary and enriched samples are never merged unweighted.

### A5 · 🚫 Invalidation
- A5.1 · Test-driven optimization cannot masquerade as a final score.
  **Done when:** Any changed scored component requires a new sealed test.

## States

### A1 · 🧾 Sampling frame and reservation
- ✅ A1.1 · Met; division 1 fixes the sampling and reservation contract.

### A2 · 🔒 Access seal
- ✅ A2.1 · Met; division 2 blocks direct and indirect development use.

### A3 · 🧑 Late human gold
- ✅ A3.1 · Met; division 3 fixes mature blind adjudication.

### A4 · 🗺 Representative and diagnostic results
- ✅ A4.1 · Met; division 4 separates the two test roles.

### A5 · 🚫 Invalidation
- ✅ A5.1 · Met; division 5 defines the one-shot claim boundary.

## Files

### 🔗 Related Board Pages · what this Page READS BY SCOPE
- `constrained by · ALL` · [QB1 §2](2-QB-calibration-round/QB1-initialize-round-one/QB1-initialize-round-one.md)
  QB1 reserves the initial sealed identifiers.
- `reads · ALL` · [QD4 §4](4-QD-optimization-and-convergence/QD4-stopping-criteria/QD4-stopping-criteria.md)
  QD4 supplies the G* freeze decision.
- `continues · ALL` · [QE2 page](5-QE-final-evaluation-and-completion/QE2-model-scorecard/QE2-model-scorecard.md)
  QE2 scores executors on the closed T*.

### Contracts · what must carry this rule
- `../../ref/ref-contract.md`
  The evaluation contract must define sampling, blindness, metrics, and invalidation.
- `../../ref/ref-assets.md`
  The artifact layout must protect the manifest and late human-gold records.

## Law
- 260806 JL · 🔒 Final test identifiers are reserved early and labeled late
      T* remains unseen throughout calibration, receives blind mature human gold after G* freezes, and is invalidated by test-driven optimization.

## Glossary
- 🧪 **Sealed test T***: unseen final-evaluation items protected from all development access and labeled by the human after G* freezes.
- 🧾 **Test manifest**: the protected sampling and access record that identifies T* without exposing its text.
- 🚫 **Invalidation**: loss of final-test status after a scored component is changed using test outcomes.

## Log
260806 · Created QE1 from QA0's reserve-early, label-late, blind-gold, and invalidation rules.
