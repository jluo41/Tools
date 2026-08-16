# Guideline optimization: improve execution without moving the human concept
state: ✅ SETTLED
owner: JL
method: Diagnose human-model differences, propose the smallest general patch, require human semantic acceptance, and regression-check affected gold.

## Opening
How should correction evidence improve the annotation policy when a weak model repeatedly misunderstands a rule?
The strong agent may study structured model reasons and propose clearer definitions, boundary tests, ordering, or examples.
The human must decide whether a patch expresses the existing concept or changes what the trait means.
This page fixes the error taxonomy, patch path, generalization rule, and regression gate that protect that authority.

**Where this page sits**: QC4 supplies human-confirmed corrections; QA3 defines the policy parts; QB3 freezes only accepted and checked changes.

**Why it matters**: Patching every error can bloat the guideline, overfit development wording, or make a model easier to satisfy by changing the target itself.

## Writing Style
**Language and sentences**: Describe one error cause and one smallest fix at a time.

**Authority**: Separate agent diagnosis, agent proposal, human semantic ruling, and checkpoint freeze.

**Reasoning**: Use concise structured reasons and visible evidence rather than hidden model chain-of-thought.

## Diagram
**Optimization loop**: one correction becomes a diagnosis, a guarded patch, and a regression-tested policy version.

```text
🏷 human gold + 🧠 sealed prediction
             │
             ▼
       🔍 error diagnosis
             │
             ▼
       🤖 smallest patch
             │
             ▼
       🧑 semantic ruling
             │
             ▼
       🧪 regression check
             │
             ▼
       📜 G_t draft for checkpoint
```

## Content

### 1 · Error diagnosis
**Taxonomy**: the system edits the core policy only when the observed failure is policy-addressable.

```text
🔍 causes
├── 📜 unclear definition
├── ⚖️ missing boundary test
├── 📚 misleading example
├── ⚙️ wrapper or schema failure
├── 🧠 executor capability limit
└── 🎲 stochastic or isolated error
```

#### 1.1 · Human-model comparison
The diagnosis compares final human evidence and rejected alternatives with each executor's cited evidence and applied rule.
It also checks whether the error repeats across items, models, classes, or regions.

#### 1.2 · Patch eligibility
Definitions, boundary rules, procedure order, escalation policy, and canonical examples are valid core-patch targets.
Formatting failures belong in an executor wrapper, while incapability and random errors remain scorecard findings rather than policy prose.

### 2 · Patch proposal and authority
**Guarded edit**: the strong agent proposes, while the human rules on meaning.

```text
🤖 proposal
├── changed policy part
├── evidence cases
├── scope + exclusions
├── counterexample
└── expected regression surface
        │
        ▼
🧑 accept · reject · reframe
```

#### 2.1 · Smallest general patch
The proposal states the minimal change that should prevent the error class rather than only the observed item.
It names which policy component changes and which components remain unchanged.

#### 2.2 · Semantic ruling
The human confirms whether the proposal clarifies existing intent, revises the concept, or merely improves wording.
A model-readability gain cannot override a human rejection.

#### 2.3 · Core versus wrapper
The core policy holds portable meaning and decision order.
Output JSON, token limits, model-specific reminders, and parser repairs belong in versioned execution wrappers.

### 3 · Generalization and casebook control
**Example transformation**: development cases produce transferable rules, while only unique teaching cases remain attached.

```text
📄 case
  ↓
🔍 decisive evidence + rejected label
  ↓
🔁 counterfactual flip condition
  ↓
📜 general rule
  └──▶ 📚 retain only if canonical
```

#### 3.1 · Rule extraction
The agent records decisive evidence, the strongest rejected label, and the smallest change that would flip the human decision.
Repeated structures become one scoped rule with exclusions and a named boundary.

#### 3.2 · Casebook pruning
An example remains only when it uniquely anchors a center, counterexample, pairwise boundary, or triple junction.
Near duplicates and source-specific wording are removed from the prompt-facing casebook while their audit records remain preserved.

#### 3.3 · No corpus copying
The annotation policy cannot rely on the full development corpus or chat transcript.
An executor must be able to apply the frozen policy from its explicit rules and compact casebook alone.

### 4 · Regression and concept impact
**Acceptance gate**: an accepted patch must preserve earlier intended decisions or expose every intended change.

```text
📜 candidate patch
        │
        ├──▶ 🏷 affected prior gold
        ├──▶ ⚖️ neighboring boundaries
        ├──▶ 🧠 seen weak executors
        └──▶ 🚨 concept-impact queue
                    │
                    ▼
               📌 checkpoint decision
```

#### 4.1 · Regression set
The system tests the patch on affected prior gold, nearby counterexamples, and representative audit items.
Any changed prediction receives a reason and human review when semantic intent is uncertain.

#### 4.2 · Concept revision
A concept revision may legitimately change earlier labels.
It opens a backward-impact queue and prevents a silent comparison between policy versions that no longer target the same decision function.

#### 4.3 · Version diff
Every checkpoint classifies edits as semantic, procedural, example, wrapper, or editorial.
The diff links each substantive change to its evidence, human ruling, and regression outcome.

## Aims

### A1 · 🔍 Error diagnosis
- A1.1 · Core policy edits occur only for policy-addressable failures.
  **Done when:** Every proposed patch names one evidence-backed error category.

### A2 · 🧑 Patch proposal and authority
- A2.1 · Model readability improves subject to human semantic fidelity.
  **Done when:** The human accepts, rejects, or reframes every substantive patch.

### A3 · 📚 Generalization and casebook control
- A3.1 · Cases become scoped rules and a compact canonical casebook rather than copied training text.
  **Done when:** Every retained example states its unique teaching role.

### A4 · 🧪 Regression and concept impact
- A4.1 · Policy changes cannot silently invalidate prior gold.
  **Done when:** Regression results and backward-impact dispositions accompany the version diff.

## States

### A1 · 🔍 Error diagnosis
- ✅ A1.1 · Met; division 1 separates policy, wrapper, capability, and noise causes.

### A2 · 🧑 Patch proposal and authority
- ✅ A2.1 · Met; division 2 preserves human semantic authority.

### A3 · 📚 Generalization and casebook control
- ✅ A3.1 · Met; division 3 fixes extraction, pruning, and no-copy rules.

### A4 · 🧪 Regression and concept impact
- ✅ A4.1 · Met; division 4 fixes regression and version evidence.

## Files

### 🔗 Related Board Pages · what this Page READS BY SCOPE
- `constrained by · ALL` · [QA3 page](QA-semantic-contract/QA3-guideline-contract/QA3-guideline-contract.md)
  QA3 defines the policy components that an optimization may change.
- `reads · ALL` · [QC4 §3](QC-selection-and-adjudication/QC4-blind-adjudication/QC4-blind-adjudication.md)
  QC4 supplies correction type and concept-impact evidence.

### Contracts · what must carry this rule
- `../../ref/ref-architecture.md`
  The architecture must separate optimizer proposal from human acceptance and checkpoint writing.
- `../../ref/ref-assets.md`
  The artifact layout must version policy diffs, wrappers, regression sets, and casebook entries.

## Law
- 260806 JL · 📜 Guideline optimization is constrained by human semantic fidelity
      A strong model may diagnose and simplify, but only the human accepts a substantive rule and concept revisions trigger backward review.

## Glossary
- 🧪 **Regression set**: prior gold and counterexamples selected to test whether a policy patch changed unintended decisions.
- ⚙️ **Execution wrapper**: model-specific formatting and interface instructions kept outside the portable core policy.
- 🧠 **Concept revision**: a human-authorized change to label meaning that may require earlier gold to be revisited.

## Log
260806 · Reopened QD1 in DRAFT and replaced the embedding-engine question with the approved guideline-optimization contract.
