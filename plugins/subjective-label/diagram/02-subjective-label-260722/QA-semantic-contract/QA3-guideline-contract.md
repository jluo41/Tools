# The annotation policy: one contract people and weaker models can execute
state: ✅ SETTLED
owner: JL
method: Convert the approved conception into a versioned policy schema, execution wrapper, and change-control contract.

## Opening
What makes an evolving annotation policy readable to a person and executable by a weaker language model?
Annotation policy Θ is the versioned contract that turns JL's trait boundary into repeatable HIGH, LOW, or NONE decisions.
A weaker model cannot recover hidden chat context or repair loose prose by intuition.
Its semantic rules, examples, and decision order must be explicit.
Its uncertainty handling, wrapper, and version history must work without the development corpus.

**Where this page sits**: QA0 establishes the human-grounded annotation policy as the object improved across Calibration Rounds, while QA3 specifies the document that an executor actually receives.

**What is settled**: The policy has five semantic components, the execution wrapper cannot change their meaning, and every closed version is self-contained and immutable.

**What stays configurable**: The few unresolved numeric limits, such as the casebook cap and escalation cutoff, live in versioned configuration and do not block this conceptual decision.

**What this replaces**: The previous QA3 treated a weak-model gallery exam as the page's purpose, while executor scoring now belongs after the policy freezes.

## Diagram
**The executable policy**: the human-approved semantic contract passes through a formatting wrapper to produce one auditable item record.

```text
🧑 authority   H_t
      │
      ▼
📜 closed policy Θ_t
├── 📖 G_t   core definitions + evidence
├── ⚖️ R_t   boundary rules
├── 🔢 Q_t   ordered decision procedure
├── 🚨 U_t   uncertainty + escalation
└── 📚 E_t   compact canonical casebook
      │
      ▼
🧩 execution wrapper   model-specific format
      │
      ▼
🧠 weaker LM → 🏷 class · 🗺 region · 🌡 uncertainty · 🧾 trace
      │
      ▼
🔁 next version   Θ_(t+1) after a human checkpoint
```

## Content

### 1 · Annotation policy Θ
**The policy boundary**: one portable semantic contract is distinct from its evidence history and model-specific wrapper.

```text
🧑 semantic source      human boundary H_t
📜 portable contract   Θ_t = {G_t, R_t, Q_t, U_t, E_t}
🧩 execution wrapper   formatting + run controls
🧾 development record  cases + dialogue + audits
```

📌 Annotation policy Θ_t is the smallest complete artifact that can reproduce the human's current labeling boundary without private context.

#### 1.1 · Complete semantic object
(Defines the five components that must travel together under one closed policy identifier.)
The core guideline G_t defines the trait, labels, admissible evidence, exclusions, and default interpretations.
The boundary rules R_t distinguish confusable labels and state how competing rules are resolved.
The decision procedure Q_t fixes the order in which an executor applies those definitions and rules.
The uncertainty policy U_t separates a final class from confidence, diagnostic region, and escalation.
The canonical casebook E_t demonstrates a small set of rules and boundaries without replacing them.
Removing any one component makes Θ_t incomplete.

#### 1.2 · Human semantic authority
(Keeps executor compatibility subordinate to the meaning accepted by the identified human.)
JL's accepted judgment defines the meaning of HIGH, LOW, and NONE for this project.
The calibration agent may simplify language, expose contradictions, and propose patches, but it cannot change the construct to suit a model.
JL decides whether a patch is an editorial edit, a clarification, or a concept revision.

#### 1.3 · Self-contained boundary
(Names the material that supports development but never becomes a hidden policy dependency.)
A closed policy does not depend on the Human-AI chat, committee votes, private chain-of-thought, the full development corpus, or undocumented model knowledge.
Those materials remain in the audit record and may justify a change, but an executor receives only the declared policy, wrapper, and item.
When the round notation uses G_t for the frozen guideline artifact, that artifact carries the complete Θ_t contract rather than only its core-guideline component.

### 2 · Core definitions and boundary rules
**The semantic hierarchy**: label meanings establish the centers, then explicit tests separate every pairwise boundary and the triple junction.

```text
📖 LABEL CENTERS
├── 🟢 HIGH   qualifying trait evidence
├── 🔵 LOW    qualifying contrasting evidence
└── ⚪ NONE   insufficient trait evidence
        │
        ▼
⚖️ BOUNDARY TESTS
├── 🟡 H-L    direction or intensity
├── 🟡 L-N    weak evidence or absence
├── 🟡 H-N    apparent evidence or confound
└── 🔴 H-L-N  missing prerequisite or rule conflict
```

📌 Definitions tell the executor what each class means, while boundary rules tell it what evidence changes one plausible answer into another.

#### 2.1 · Core definition schema
(Makes each trait-specific definition explicit enough to inspect and execute.)
The policy names the target trait, target population, unit of text, and whose judgment it represents.
Each class definition states qualifying evidence, disqualifying evidence, exclusions, and at least one contrast with its nearest alternative.
HIGH and LOW describe trait-specific evidence rather than positive and negative sentiment.
NONE means insufficient evidence of the trait and never means that the executor feels uncertain.

#### 2.2 · Evidence rule schema
(Gives every reusable rule a stable address and an observable application condition.)
Every evidence rule has a stable rule id, a condition visible in the item, its effect on a label, its scope, and any exception.
Rules cite text spans or permitted text implications rather than unsupported facts about the author.
An implication that requires outside knowledge is inadmissible unless the policy explicitly permits that knowledge source.
Broad impressions cannot overrule a specific accepted exclusion or boundary rule.

#### 2.3 · Boundary roster
(Covers the complete seven-region geometry without turning a diagnostic region into a class.)
The H-L rule distinguishes direction or intensity after the policy has established that trait evidence is present.
The L-N rule distinguishes weak qualifying LOW evidence from true absence of trait evidence.
The H-N rule distinguishes qualifying HIGH evidence from irony, irrelevant praise, quotation, or another stated confound.
The H-L-N rule handles cases where all three labels remain plausible because a prerequisite or precedence rule is missing.
The H, L, and N centers provide prototypes for clear cases, while the four boundary regions diagnose why a case is difficult.

#### 2.4 · Precedence and conflict
(Prevents a weaker executor from inventing its own tie-break when accepted rules collide.)
The policy applies scope and exclusion rules before positive label rules, then applies the most specific relevant boundary rule.
Every intentional override names the rule it overrides.
If two accepted rules still point to different labels and no precedence is declared, the executor records the conflict and escalates rather than improvising.

### 3 · Ordered decision procedure
**The execution path**: one fixed sequence turns an item and a closed policy into a class, diagnostic metadata, and an inspectable reason.

```text
📄 item + 📜 closed Θ_t
          │
          ▼
🔎 admissible evidence
          │
          ▼
⚪ sufficiency gate ── no ──▶ 🏷 NONE
          │ yes
          ▼
⚖️ boundary tests
          │
          ▼
🏷 HIGH | LOW | NONE
          │
          ▼
🌡 uncertainty + 🚨 escalation → 🧾 structured record
```

📌 The procedure keeps a weaker model from jumping from a general impression to a label before checking evidence sufficiency and the relevant boundary.

#### 3.1 · Fixed inputs
(Prevents hidden context and committee answers from entering an individual execution.)
One execution receives one item, one closed policy id, one declared wrapper version, and no other model's prediction.
The executor verifies those identifiers before applying any semantic rule.
Missing or mismatched inputs produce an invalid-run record rather than a guessed label.

#### 3.2 · Decision sequence
(States the order that every executor follows before emitting a result.)
1. Read the item as the declared unit of analysis and ignore metadata that the policy does not permit.
2. Extract the exact text spans that may provide admissible trait evidence.
3. Apply scope and exclusion rules to remove irrelevant, quoted, hypothetical, or otherwise barred evidence.
4. Test whether sufficient trait evidence remains, and choose NONE when it does not.
5. When evidence remains, compare HIGH and LOW using the relevant pairwise or triple boundary rule.
6. Choose exactly one required final class and assign the diagnostic region separately.
7. Apply the uncertainty and escalation policy without changing NONE into an uncertainty bucket.
8. Emit the required structured record and validate it against the wrapper schema.

#### 3.3 · Deterministic tie handling
(Defines safe behavior when the written hierarchy does not yield one supported answer.)
The executor follows declared precedence and never resolves a tie by sentiment, frequency, or an unstated personal prior.
If the policy requires a class despite unresolved uncertainty, the executor emits its best supported class as provisional and marks escalation.
If the wrapper permits abstention, abstention remains a review state and never becomes NONE.

#### 3.4 · Compact justification
(Makes the result auditable without requesting hidden chain-of-thought.)
The executor returns decisive evidence spans, applied rule ids, the strongest rejected alternative, and a concise uncertainty reason.
This structured justification is sufficient for diagnosis and does not require private reasoning traces.

### 4 · Uncertainty and escalation policy
**The four-field result**: semantic class, diagnostic region, confidence, and review routing remain independent records.

```text
🏷 class       HIGH | LOW | NONE
🗺 region      H | L | N | HL | LN | HN | HLN
🌡 confidence  configured scale + reason
🚨 review      yes | no + named trigger
```

📌 Uncertainty changes how a result is reviewed, not what NONE means and not which diagnostic boundary the item probes.

#### 4.1 · Separate uncertainty record
(Protects semantic absence from procedural doubt.)
Every result carries a final class, region, confidence value, and uncertainty reason even when review is not required.
Low confidence in HIGH or LOW remains low-confidence HIGH or LOW unless the evidence rules independently support NONE.
An H-N region may end with HIGH or NONE, while the region continues to record the boundary that was tested.

#### 4.2 · Escalation triggers
(Names the conditions under which machine execution cannot pass without added review.)
Escalation is required when accepted rules conflict, no rule covers a material pattern, required evidence cannot be located, or the output cannot satisfy the schema.
It is also required when confidence crosses the configured review cutoff or the item belongs to a recorded consensus-failure neighborhood.
Novel language alone is a review signal only when it weakens rule application or evidence support.

#### 4.3 · Escalation packet
(Gives the human the smallest complete record needed to resolve the case.)
The packet carries the provisional class when one is required, region, confidence, cited spans, competing rule ids, rejected alternative, and one focused question.
The human confirms or changes the class and decides whether the case exposes a local execution error, a missing rule, or a concept revision.
Any accepted semantic change enters a new policy draft and never edits the closed policy in place.

#### 4.4 · Configured thresholds
(Keeps empirical numeric choices visible without reopening the settled semantic contract.)
Confidence cutoffs and any confidence-margin rule are named configuration values attached to the policy and wrapper versions.
Their exact values are selected from pilot and audit evidence, not embedded as unexplained prose constants.
Changing a cutoff creates a new configuration record but needs a semantic policy version only if the meaning of a label changes.

### 5 · Compact generalized casebook
**The example filter**: development cases become generalized rules, and only cases with unique teaching value remain beside the policy.

```text
📄 development case
        │
        ▼
🔍 decisive evidence + rejected alternative
        │
        ▼
⚖️ generalized rule + counterfactual flip
        │
        ▼
📚 canonical case?   prototype | boundary | counterexample
        │
        ├── ✅ keep minimal record in E_t
        └── 🗄 archive full case outside Θ_t
```

📌 The casebook teaches how a rule behaves at its center and edges without letting surface similarity replace the decision procedure.

#### 5.1 · Canonical case schema
(Makes every retained example explain one rule rather than merely display a label.)
Each case has a stable case id, minimal item text, final class, diagnostic region, decisive evidence, applied rule ids, strongest rejected label, human reason, and counterfactual flip.
The case also states why it remains in the casebook and which unique pattern it teaches.
Sensitive or needlessly long source text is replaced by the shortest faithful excerpt or approved paraphrase that preserves the decision.

#### 5.2 · Inclusion and removal
(Keeps the example set small, diverse, and aligned with the current rules.)
The casebook retains clear class anchors, pairwise boundary contrasts, a triple-junction case when one exists, and counterexamples that prevent a known misread.
Near duplicates, examples explained by an existing stronger case, and cases tied only to one source phrase are removed.
A policy change that alters a retained case triggers case review, replacement, or retirement in the same checkpoint.

#### 5.3 · Generalization before retention
(Forbids patching the prompt with every corrected development item.)
An influential case first yields a rule with scope, exception, rejected alternative, and flip condition.
The rule is checked against earlier human-confirmed items before the case may be selected as canonical.
The full development corpus, full correction gallery, and Human-AI transcript remain outside the policy.

#### 5.4 · Configurable size cap
(Leaves corpus-specific compactness as a measured limit rather than an arbitrary conceptual ruling.)
The maximum number of retained cases is a versioned numeric setting chosen to fit the weakest intended executor's context budget.
The policy records the cap and current count, while inclusion still depends on unique explanatory value rather than filling a quota.

### 6 · Execution wrapper
**The portability layer**: model-specific instructions package one unchanged policy into a bounded input and parseable output.

```text
📥 closed Θ_t + 📄 item
          │
          ▼
🧩 execution wrapper
├── 📌 task + allowed context
├── 🔢 output schema
├── 🚫 prohibited inputs
└── ⚙️ token + decoding controls
          │
          ▼
🧠 weaker LM → 🧾 validated item record
```

📌 The wrapper may make execution easier for one model, but it may not add, remove, reorder, or reinterpret a semantic rule.

#### 6.1 · Wrapper boundary
(Separates portable policy meaning from model-specific delivery mechanics.)
The wrapper names the model and version, prompt layout, allowed context, output schema, decoding settings, and validation behavior.
A wrapper edit is mechanical when it preserves every semantic input and output obligation.
A wrapper instruction that changes a label definition, boundary, precedence rule, or escalation meaning belongs in Θ and requires human acceptance.

#### 6.2 · Bounded prompt packet
(Ensures that a weak executor sees all required context and no development leakage.)
The packet presents the policy id and definitions first, then boundary rules, ordered procedure, uncertainty policy, canonical cases, the one item, and the output schema.
It excludes the full development corpus, chat transcript, hidden human notes, other model predictions, and later gold labels.
Each execution uses the same packet order within one reported run.

#### 6.3 · Required output schema
(Makes every answer parseable, comparable, and traceable to one policy version.)

```json
{
  "policy_version": "<closed-policy-id>",
  "wrapper_version": "<wrapper-id>",
  "item_id": "<stable-item-id>",
  "class": "HIGH|LOW|NONE",
  "region": "H|L|N|HL|LN|HN|HLN",
  "confidence": "<configured-scale-value>",
  "evidence_spans": ["<exact span>"],
  "rule_ids": ["<stable rule id>"],
  "rejected_alternative": "<label and reason>",
  "uncertainty_reason": "<concise reason>",
  "escalate": false
}
```

The wrapper requires every field and allows no free-form answer to replace the record.
Evidence spans and rule ids provide the compact execution trace used for audit and error diagnosis.

#### 6.4 · Validation and failure
(Prevents malformed output from being mistaken for a semantic prediction.)
The validator checks the policy id, required keys, enum values, evidence presence, and agreement between escalation and uncertainty fields.
A malformed response may be retried up to the configured numeric limit under the same policy and wrapper.
Failure after that limit becomes an execution error and enters escalation rather than receiving a repaired label from hidden logic.

### 7 · Versioning and change control
**The immutable lifecycle**: a checkpoint closes one policy, and every later semantic change produces a traceable successor.

```text
✏️ Θ_t draft
      │
      ▼
🧑 human checkpoint
      │
      ▼
🔒 Θ_t closed + 🧩 wrapper version
      │
      ▼
🧪 regression + unseen execution
      │
      ▼
📝 editorial | 🔎 clarification | 🧭 concept revision
      │
      ▼
🔁 Θ_(t+1) draft + impact record
```

📌 Versioning preserves which meaning and instructions produced every label while allowing the policy to improve between checkpoints.

#### 7.1 · Draft and closed states
(Makes the policy used for execution stable during one Calibration Round.)
Θ_t draft may change during Human-AI Sessions inside Round t.
The checkpoint records human acceptance and freezes Θ_t closed as an immutable artifact.
Round t+1 pre-labeling uses the previous closed version, never the changing draft.

#### 7.2 · Change classes
(Separates wording repair from changes that can invalidate earlier human gold.)
An editorial edit improves spelling or layout without changing an executable instruction.
A clarification makes the accepted boundary more explicit while preserving the intended construct.
A concept revision changes what HIGH, LOW, or NONE means and requires backward impact review of affected labels, rules, and cases.
JL assigns the change class at checkpoint whenever semantic impact is plausible.

#### 7.3 · Version manifest
(Keeps policy, wrapper, configuration, and evidence history independently traceable.)
Every closed policy records its id, parent id, round and checkpoint, human approver, component versions, accepted changes, affected rule and case ids, and content hash.
The wrapper records its own id, target model and version, prompt layout, schema, decoding configuration, and compatible policy id.
Every item record stores both ids so a wrapper update cannot masquerade as a policy update.

#### 7.4 · Regression and migration
(Protects earlier decisions when a rule, case, or procedure changes.)
Each semantic patch is tested against affected human-confirmed items and a stable regression set before closure.
Changed rules identify older labels and canonical cases that require re-review.
A closed policy is never overwritten, and deprecated versions retain their manifests and item provenance.

#### 7.5 · Configurable numeric settings
(Collects the remaining empirical values without turning them into blocking human decisions.)
The casebook cap, confidence and escalation cutoffs, output token cap, and malformed-output retry limit remain versioned configuration values.
Pilot and audit evidence choose their values, and each reported run records them.
No unresolved conceptual decision remains on this page.

## Aims

### A1 · 📜 Annotation policy Θ
- A1.1 · The annotation policy is a complete portable semantic object with an explicit authority and exclusion boundary.
  **Done when:** A reader can distinguish Θ_t, its five components, its wrapper, and its external development record from Section 1 alone.

### A2 · ⚖️ Core definitions and boundary rules
- A2.1 · Every class, evidence rule, pairwise boundary, triple boundary, and precedence failure has an executable contract.
  **Done when:** Section 2 states how a weaker executor distinguishes HIGH, LOW, and NONE without using sentiment or an invented tie-break.

### A3 · 🔢 Ordered decision procedure
- A3.1 · One fixed procedure converts a closed policy and item into a supported final record.
  **Done when:** Section 3 orders evidence extraction, exclusions, sufficiency, boundary tests, class choice, uncertainty, and output validation.

### A4 · 🚨 Uncertainty and escalation policy
- A4.1 · Class, region, confidence, and escalation remain separate and route unresolved risk safely.
  **Done when:** Section 4 forbids uncertainty leakage into NONE and defines triggers and the escalation packet.

### A5 · 📚 Compact generalized casebook
- A5.1 · Canonical examples teach generalized rules without copying development data into the policy.
  **Done when:** Section 5 defines the case schema, retention test, generalization step, removal rule, and configurable size cap.

### A6 · 🧩 Execution wrapper
- A6.1 · A weaker language model receives a bounded packet and returns one validated structured record without changing policy meaning.
  **Done when:** Section 6 separates wrapper mechanics from semantics and fixes the required inputs, outputs, validation, and failure route.

### A7 · 🔒 Versioning and change control
- A7.1 · Every closed policy, wrapper, configuration, change class, and affected label remains traceable.
  **Done when:** Section 7 defines immutable closure, manifests, regression, migration, and the remaining numeric settings.

## States

### A1 · 📜 Annotation policy Θ
- ✅ A1.1 · Met; Section 1 defines Θ_t, its five components, human authority, wrapper boundary, and excluded development context.

### A2 · ⚖️ Core definitions and boundary rules
- ✅ A2.1 · Met; Section 2 defines class semantics, evidence rules, seven-region boundaries, precedence, and conflict escalation.

### A3 · 🔢 Ordered decision procedure
- ✅ A3.1 · Met; Section 3 gives one eight-step decision sequence and compact justification contract.

### A4 · 🚨 Uncertainty and escalation policy
- ✅ A4.1 · Met; Section 4 separates the four result fields and defines triggers, packets, and configured thresholds.

### A5 · 📚 Compact generalized casebook
- ✅ A5.1 · Met; Section 5 defines canonical records, inclusion, removal, generalization, and the ban on corpus copying.

### A6 · 🧩 Execution wrapper
- ✅ A6.1 · Met; Section 6 fixes the packet boundary, structured schema, validation, and execution-error route.

### A7 · 🔒 Versioning and change control
- ✅ A7.1 · Met; Section 7 defines immutable policy closure, change classes, manifests, regression, migration, and versioned settings.

## Files

### 🔗 Related Board Pages · what this Page READS BY SCOPE
- `constrained by · ALL` · [QA0 §6](QA-semantic-contract/QA0-the-revised-conception.md)
  Preserve QA0's separation of class, diagnostic region, and uncertainty.
- `constrained by · ALL` · [QA0 §9](QA-semantic-contract/QA0-the-revised-conception.md)
  Preserve QA0's five-part annotation policy and human-authority boundary.
- `constrained by · ALL` · [QA0 §15](QA-semantic-contract/QA0-the-revised-conception.md)
  Preserve QA0's checkpoint freeze, regression, and impact-review rules.
- `constrained by · ALL` · [QA0 §21](QA-semantic-contract/QA0-the-revised-conception.md)
  Preserve QA0's separation between the core policy and model-specific execution wrapper.
- `constrained by · ALL` · [QA0 §22](QA-semantic-contract/QA0-the-revised-conception.md)
  Preserve QA0's rule extraction and compact canonical casebook contract.

## Law
- 260806 JL · 📜 One closed annotation policy carries the complete semantic contract
      Annotation policy Θ_t contains G_t, R_t, Q_t, U_t, and E_t, while the execution wrapper may format their delivery but may not alter their meaning.
      A weak executor receives the closed policy and one item without the development transcript or full development corpus.
- 260806 JL · 🧹 Development cases become rules before they become policy examples
      The casebook retains only minimal canonical cases with unique teaching value after their general rule, scope, exception, and flip condition are explicit.
      Near duplicates and the full correction gallery remain in the external development record.
- 260806 JL · 🔁 QA3 governs the policy artifact rather than the previous gallery exam
      This DRAFT round replaces QA3's previous-edition purpose of scoring cheap models on the same development gallery.
      Final executor scoring occurs only after the policy freezes, while QA3 owns what every executor must be able to read and run.

## Glossary
- 📜 **Annotation policy Θ_t**: the complete human-approved semantic contract at Calibration Round t, composed of G_t, R_t, Q_t, U_t, and E_t.
- 📖 **Core guideline G_t**: the trait definition, class meanings, evidence rules, exclusions, and default interpretations inside Θ_t.
- ⚖️ **Boundary rules R_t**: the pairwise, triple-junction, precedence, and conflict rules that separate plausible labels.
- 🔢 **Decision procedure Q_t**: the fixed order in which an executor applies the policy to one item.
- 🚨 **Uncertainty policy U_t**: the confidence, reason, trigger, and escalation contract kept separate from the final class.
- 📚 **Canonical casebook E_t**: the compact set of uniquely informative examples that demonstrate accepted rules and boundaries.
- 🧩 **Execution wrapper**: model-specific input, output, and run instructions that package one unchanged closed policy.
- 🔒 **Closed policy**: an immutable policy version accepted at a checkpoint and safe to use as the input to a later round or evaluation.

## Log
260806 · DRAFT reopened QA3 and replaced its previous-edition gallery-exam purpose with the approved annotation-policy contract, execution wrapper, and versioning rules.
