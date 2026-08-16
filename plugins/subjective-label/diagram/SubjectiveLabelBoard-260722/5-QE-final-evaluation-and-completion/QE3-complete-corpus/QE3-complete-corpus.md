# Corpus completion: execute G* with risk routing and human fallback
state: ✅ SETTLED
owner: JL
method: Choose a frozen production policy from final evidence, label the eligible remainder, and route disagreement, low confidence, novelty, and known failure strata to human review.

## Opening
How should the project complete all N corpus labels after final evaluation identifies viable weak executors?
The production policy may use one model, an ensemble, a lightweight scorer, or cost-aware routing.
Every automatic label must remain traceable to G* and its executor path.
Risky cases must enter a human queue instead of becoming NONE or disappearing behind model consensus.
This page fixes executor selection, production routing, retry and drift behavior, and the definition of completion.

**Where this page sits**: QE2 supplies frozen scorecards; QE4 audits the resulting corpus and closes the reliability package.

**Why it matters**: A fast cascade can label every row while silently propagating a confident shared error from embeddings, classifiers, or related model families.

## Writing Style
**Language and sentences**: Separate production decision, automatic acceptance, human escalation, and final disposition.

**Authority**: No retrieval or model tier creates human gold; provenance states the actual authority behind each row.

**Thresholds**: Use validation-supported, versioned thresholds and state cost or risk tradeoffs explicitly.

## Diagram
**Production route**: a frozen executor policy labels the remainder and sends known risk to the human.

```text
📊 scorecards + 📜 G*
          │
          ▼
⚙️ frozen production policy
          │
          ▼
🏭 eligible corpus remainder
    ├──▶ 🟢 accepted machine disposition
    └──▶ 🚨 risk queue ──▶ 🧑 human final disposition
          │
          ▼
      📦 completed corpus candidate
```

## Content

### 1 · Production policy selection
**Selection record**: the chosen route follows a predefined utility and risk rule without rewriting QE2's final scores.

```text
⚙️ policy choice
├── quality floors
├── protected-stratum risk
├── stability
├── cost + latency
├── capacity for human review
└── executor or ensemble identity
```

#### 1.1 · Eligible executors
Only executors that meet the required final-test and protected-stratum floors may auto-label.
A cheaper failing executor may still serve retrieval or prioritization but not final automatic disposition.

#### 1.2 · Selection without test tuning
The utility rule may choose among already frozen candidates using reported evidence.
Changing wrappers, thresholds, ensemble weights, or candidates because of T* outcomes creates a new system and requires a new validation or test boundary.

#### 1.3 · Lightweight model role
A classifier or embedding score may be part of production only when its acceptance path has direct validation and audit evidence.
Nearest-neighbor similarity alone cannot inherit a gold label.

### 2 · Item routing
**Risk-aware execution**: every item either receives an accepted machine disposition or enters a named escalation branch.

```text
📄 item
├── 🧠 executor prediction
├── 🌡 calibrated risk
├── 🗺 known failure stratum
├── 🌱 novelty check
└── ⚖️ ensemble agreement
        │
        ├──▶ 🟢 accept
        └──▶ 🚨 human queue
```

#### 2.1 · Automatic acceptance
Acceptance requires the production policy's quality, confidence, agreement, and supported-region conditions.
The record preserves prediction, evidence, policy version, executor, wrapper, thresholds, and route.

#### 2.2 · Human escalation
Disagreement, low calibrated confidence, novelty, unsupported evidence, parse failure, and known consensus-failure neighborhoods enter the queue.
Uncertainty cannot be converted into NONE.

#### 2.3 · Human disposition
The human reviews escalated items under G* and records class, region, uncertainty, reason, and any new risk observation.
Production discoveries do not silently change G*; a semantic issue reopens calibration as a new versioned cycle.

### 3 · Operational controls
**Safe run**: preflight, immutable manifests, resumability, and drift monitoring protect a large production pass.

```text
🧪 preflight
  ↓
🧾 frozen run manifest
  ↓
🏭 resumable shards
  ↓
📊 drift + queue monitoring
  ↓
✅ reconciliation
```

#### 3.1 · Preflight
A probability or stratified production sample estimates routing share, cost, latency, parse failures, and human-queue load.
The run does not begin when projected human capacity or hard cost caps are violated.

#### 3.2 · Idempotence and retries
Every item has a stable run key derived from item, policy, executor, wrapper, and route version.
Retries append attempts and never create two unexplained final labels.

#### 3.3 · Drift response
Shifts in class distribution, novelty, disagreement, confidence, parse failures, or queue rate trigger review.
A material distribution shift pauses automatic acceptance for the affected stratum.

### 4 · Completion state
**Finished corpus**: every in-scope item has one terminal disposition and an auditable provenance tier.

```text
📦 terminal dispositions
├── 🥇 human-confirmed
├── 🥈 audited machine-accepted
├── 🥉 machine-accepted pending final audit
└── 🚨 accepted unresolved with stated limitation
```

#### 4.1 · Terminal record
Each item has one final class or an explicitly accepted unresolved disposition.
Duplicates, excluded items, missing text, and out-of-scope records receive typed non-label dispositions rather than vanishing.

#### 4.2 · Completion versus reliability
Production completion means every eligible item reached a terminal route.
The corpus is called reliable only after QE4's final probability audit and provenance report pass.

## Aims

### A1 · ⚙️ Production policy selection
- A1.1 · The production route is frozen, eligible, and selected without changing final-test claims.
  **Done when:** Quality, risk, cost, and executor evidence support one immutable manifest.

### A2 · 🚨 Item routing
- A2.1 · Automatic acceptance and human escalation are explicit and auditable.
  **Done when:** Every item records prediction, risk, route, and terminal authority.

### A3 · 🏭 Operational controls
- A3.1 · Large-corpus execution is preflighted, resumable, idempotent, and drift-aware.
  **Done when:** Shards reconcile to the manifest with no duplicate terminal records.

### A4 · 📦 Completion state
- A4.1 · Every in-scope item has one terminal disposition without overstating reliability.
  **Done when:** The completed candidate corpus passes to QE4 with provenance.

## States

### A1 · ⚙️ Production policy selection
- ✅ A1.1 · Met; division 1 fixes eligibility and test-tuning boundaries.

### A2 · 🚨 Item routing
- ✅ A2.1 · Met; division 2 fixes acceptance, escalation, and human disposition.

### A3 · 🏭 Operational controls
- ✅ A3.1 · Met; division 3 fixes preflight, retries, and drift handling.

### A4 · 📦 Completion state
- ✅ A4.1 · Met; division 4 separates terminal processing from reliability.

## Files

### 🔗 Related Board Pages · what this Page READS BY SCOPE
- `reads · ALL` · [QE2 §4](5-QE-final-evaluation-and-completion/QE2-model-scorecard/QE2-model-scorecard.md)
  QE2 supplies eligible executor evidence and failure strata.
- `continues · ALL` · [QE4 page](5-QE-final-evaluation-and-completion/QE4-final-audit-and-provenance/QE4-final-audit-and-provenance.md)
  QE4 audits the completed candidate corpus and closes provenance claims.

### Contracts · what must carry this rule
- `../../ref/ref-cascade.md`
  The production-routing reference must remove unvalidated label inheritance and add risk evidence.
- `../../ref/ref-assets.md`
  The artifact layout must preserve manifests, attempts, accepted labels, and the human queue.

## Law
- 260806 JL · 🏭 Production completion uses a frozen tested route with human fallback
      Every automatic label carries executor and policy provenance, while disagreement, uncertainty, novelty, and known shared-error risk escalate.

## Glossary
- ⚙️ **Production policy**: the frozen executor, wrapper, thresholds, ensemble logic, and escalation rules used to complete the corpus.
- 🚨 **Risk queue**: items withheld from automatic acceptance because of disagreement, uncertainty, novelty, failure, or known error strata.
- 📦 **Terminal disposition**: one final class, accepted unresolved state, exclusion, or data-quality outcome for an in-scope item.

## Log
260806 · Created QE3 from QA0's executor-selection, risk-routing, production, and completion rules.
