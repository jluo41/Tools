# Model scorecards: test policy transfer across candidate executors
state: ✅ SETTLED
owner: JL
method: Run every candidate under the same G* and T*, compare with human gold, estimate guideline uplift, and include at least one held-out executor family.

## Opening
How should the final guideline and several smaller language models be evaluated after calibration ends?
Every candidate must receive the same frozen semantic policy and unseen human-gold test under a versioned execution protocol.
The scorecard must separate raw model capability from the value added by G* and must test whether the policy transfers beyond models used during optimization.
This page fixes the executor registry, final metrics, guideline-uplift comparison, held-out transfer, and selection boundary.

**Where this page sits**: QE1 supplies T*; QA3 supplies G* and wrappers; QE3 uses the scorecard to choose a production executor policy.

**Why it matters**: A high score from one model used throughout development may reflect model-specific prompt tuning rather than a portable annotation policy.

## Writing Style
**Language and sentences**: Name model, version, provider, wrapper, decoding, run count, test set, and policy checksum for every score.

**Comparison**: Keep absolute performance, guideline uplift, held-out transfer, stochastic stability, cost, and latency separate.

**Selection**: Report evidence before recommending a production executor and never modify the scored system from T* results without invalidation.

## Diagram
**Common executor exam**: one policy and one test produce comparable per-model records.

```text
📜 G* + 🧪 T*
       │
       ├──▶ 🧠 LM A ──▶ 📊 S_A
       ├──▶ 🧠 LM B ──▶ 📊 S_B
       └──▶ 🧠 LM C ──▶ 📊 S_C

comparison ruler = 🧑 human gold Y*_T
```

## Content

### 1 · Executor registry and freeze
**Run identity**: candidates and baselines are registered before final predictions are opened.

```text
🧾 executor record
├── model + version
├── seen | held-out status
├── core policy checksum
├── wrapper checksum
├── decoding + tools
└── run count + seed
```

#### 1.1 · Seen executors
Seen executors participated in pre-labeling, error diagnosis, wrapper tuning, or other development work.
Their results remain valid absolute scores but do not alone prove model-family portability.

#### 1.2 · Held-out executors
At least one model or model family has no role in guideline optimization and receives G* only at final evaluation.
Its transfer result tests whether the policy is executable beyond the optimization committee.

#### 1.3 · Frozen protocol
All candidate lists, wrappers, decoding settings, retry rules, and aggregation logic are locked before outcomes are inspected.
Any post-result change follows QE1's invalidation rule.

### 2 · Absolute performance
**Human-fidelity score**: each executor prediction is compared with the same final human-gold record.

```text
📊 absolute score
├── macro-F1 + balanced accuracy
├── per-class precision and recall
├── confusion matrix
├── agreement statistic
├── region diagnostics
└── uncertainty interval
```

#### 2.1 · Primary metrics
Categorical H, L, and N results include macro-F1, balanced accuracy, per-class precision and recall, confusion, and a declared agreement statistic.
Ordinal treatment may add weighted kappa or distance-sensitive error when the project contract justifies ordering.

#### 2.2 · Diagnostic metrics
The scorecard reports performance by human region, especially HL, LN, HN, and HLN.
It also reports NONE overuse, wrong-reason cases when available, and uncertainty calibration.

#### 2.3 · Statistical uncertainty
Every headline score includes a confidence interval or explicit small-sample limitation.
Paired comparisons use the same test items and preserve per-item predictions.

### 3 · Guideline uplift
**Policy contribution**: the same executor is run with G* and with one predefined minimal instruction.

```text
🧠 same executor
├── minimal instruction ──▶ score_base
└── frozen G*           ──▶ score_policy

📈 uplift = score_policy - score_base
```

#### 3.1 · Baseline freeze
The minimal instruction is fixed before final results and contains only the trait name, label names, and required output shape.
It cannot be weakened after seeing G* results to inflate uplift.

#### 3.2 · Paired uplift
Uplift is computed per executor on identical T* items and run conditions.
The report shows absolute baseline, absolute policy score, paired difference, and uncertainty.

#### 3.3 · Interpretation
Positive uplift supports the claim that the learned policy adds value beyond model prior knowledge.
Low uplift with high absolute performance may indicate a capable model, while low absolute performance with high uplift may indicate an executor ceiling.

### 4 · Stability, cost, and failure profile
**Deployment evidence**: quality is considered together with run stability and resource requirements.

```text
⚙️ operational profile
├── repeated-run label flips
├── parse and refusal failures
├── latency + throughput
├── token and money cost
└── high-risk error strata
```

#### 4.1 · Repeated execution
When an executor is stochastic, repeated frozen runs estimate label-flip rate and score variation.
Deterministic settings are preferred when they do not reduce task quality.

#### 4.2 · Error profile
The scorecard names which classes, regions, sources, or evidence rules cause systematic failure.
One average score cannot hide a deployment-critical failure stratum.

#### 4.3 · No automatic winner
QE2 reports comparable evidence and a recommended eligible set.
QE3 chooses the production policy using quality, risk, stability, cost, and routing needs without changing any final-test result.

## Aims

### A1 · 🧾 Executor registry and freeze
- A1.1 · Every scored system is fully identified and includes seen or held-out status.
  **Done when:** Policy, wrapper, model, settings, and run protocol are immutable.

### A2 · 📊 Absolute performance
- A2.1 · Candidate quality is measured against the same human gold with protected strata.
  **Done when:** Headline, class, region, confusion, and uncertainty results are present.

### A3 · 📈 Guideline uplift
- A3.1 · Policy value is separated from executor prior capability.
  **Done when:** Each eligible executor has a paired minimal-instruction comparison.

### A4 · ⚙️ Stability, cost, and failure profile
- A4.1 · Deployment tradeoffs remain visible without selecting a winner inside evaluation.
  **Done when:** Repeated-run, failure, cost, latency, and risk results accompany quality.

## States

### A1 · 🧾 Executor registry and freeze
- ✅ A1.1 · Met; division 1 fixes candidate identity and held-out transfer.

### A2 · 📊 Absolute performance
- ✅ A2.1 · Met; division 2 defines common human-gold metrics.

### A3 · 📈 Guideline uplift
- ✅ A3.1 · Met; division 3 defines the paired baseline comparison.

### A4 · ⚙️ Stability, cost, and failure profile
- ✅ A4.1 · Met; division 4 defines operational evidence and the selection boundary.

## Files

### 🔗 Related Board Pages · what this Page READS BY SCOPE
- `reads · ALL` · [QE1 page](QE-final-evaluation-and-completion/QE1-sealed-final-test/QE1-sealed-final-test.md)
  QE1 supplies the valid T* and human gold.
- `constrained by · ALL` · [QA3 page](QA-semantic-contract/QA3-guideline-contract/QA3-guideline-contract.md)
  QA3 supplies G* and separates core policy from wrappers.
- `continues · ALL` · [QE3 page](QE-final-evaluation-and-completion/QE3-complete-corpus/QE3-complete-corpus.md)
  QE3 chooses a production executor policy from the scorecards.

### Contracts · what must carry this rule
- `../../ref/ref-contract.md`
  The evaluation contract must define final metrics, uplift, held-out transfer, and invalidation.
- `../../ref/ref-assets.md`
  The artifact layout must preserve the registry, predictions, metrics, and scorecard.

## Law
- 260806 JL · 📊 Final scorecards use one G*, one T*, human gold, and at least one held-out executor
      Absolute quality, guideline uplift, transfer, stability, cost, and failure strata remain separate and reproducible.

## Glossary
- 📊 **Model scorecard S***: the frozen per-executor record of human-fidelity, uplift, transfer, stability, cost, and errors on T*.
- 🧠 **Held-out executor**: a model or model family excluded from guideline optimization and introduced only for final transfer evaluation.
- 📈 **Guideline uplift**: the paired performance gain from G* over a predefined minimal instruction for the same executor.

## Log
260806 · Created QE2 from QA0's common-protocol, uplift, held-out-executor, and stability requirements.
