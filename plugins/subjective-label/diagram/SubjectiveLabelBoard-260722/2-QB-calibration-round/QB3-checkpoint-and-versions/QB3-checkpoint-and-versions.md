# The round checkpoint: one immutable handoff
state: ✅ SETTLED
owner: JL
method: Define the six required artifact groups, their closure checks, and the only valid handoff to the next Calibration Round.

## Opening
What exactly closes Calibration Round t and permits Round t+1 to begin?
A checkpoint is the immutable package that gives one version to every round output.
It binds the human record and policy to the selection lineage, measurements, and remaining risks.
A finished chat or a saved guideline draft cannot close the round because either can disagree with the other artifacts.
This page settles the six required groups, their closure checks, and the rule that only a closed checkpoint may become next-round input.

**Where this page sits**: The Human-AI Session produces judgments and policy changes, while this page turns those outputs into the sole stable input for later candidate generation and pre-labeling.

**What is settled**: Closure requires all six groups, immutable identifiers and digests, referential checks, a closure receipt, and an explicit backward-impact queue.

**Configurable settings**: Batch sizes, audit sample sizes, quotas, metric thresholds, confidence levels, stability tolerances, consecutive-round counts, and risk limits remain numeric configuration fields recorded in the package.

## Diagram
**The six-group checkpoint**: one validated package closes a round and becomes the only next-round handoff.

```text
💬 session outputs
        │
        ▼
📦 CP_t DRAFT
├── 1️⃣ identity + closure receipt
├── 2️⃣ human gold + history pointers
├── 3️⃣ closed policy + policy diff
├── 4️⃣ candidate + pre-label + batch manifests
├── 5️⃣ audit + challenge metrics
└── 6️⃣ backward impact + transition gate
        │
        ├── ✅ valid     🔒 CP_t CLOSED → Round t+1 input
        └── ❌ invalid   ⛔ Round t OPEN
```

## Content

### 1 · Checkpoint identity and closure receipt
**The closure record**: stable identity and validation evidence give one package transition authority.

```text
🔁 Round t
   │
   ▼
📦 CP_t
├── 🆔 checkpoint_id · round_id · prior_checkpoint_id
├── 🕒 closed_at · closed_by
├── #️⃣ schema_version · artifact digests
└── 🧾 closure receipt · CLOSED
```

#### 1.1 · Closure is an event
(Separates a completed conversation from the method-level event that ends a round.)
A Calibration Round ends only when the closure process validates one complete checkpoint package and writes a CLOSED receipt.
The receipt names the checkpoint, the round, the prior checkpoint, the human authority, the closure time, the schema version, and every validation result.
Round 1 records a null prior checkpoint under the same schema rather than inventing an earlier state.
A session ending, a batch being labeled, or a policy draft being saved records progress but has no closure authority.

#### 1.2 · Immutability preserves lineage
(Defines how a closed package stays reproducible when a later correction is necessary.)
Every closed artifact receives a stable version identifier and a content digest.
Closed artifacts are append-only and cannot be changed in place.
A correction creates a new package that names the checkpoint it supersedes and preserves the earlier package for audit.

### 2 · Human gold and history pointers
**The human record**: current decisions close as Y*_t and D_t while their conversational lineage remains reachable.

```text
💬 session ids + history digests
             │
             ▼
🏷 Y*_t for B_t
             │
             ▼
🗄 D_(t-1) + Y*_t + approved revisions = D_t CLOSED
```

#### 2.1 · Y*_t and D_t close together
(Binds the current human batch to the cumulative human-confirmed dataset.)
Y*_t contains the final human decision for every item in B_t, including its class, region, uncertainty record, reason, provenance, and revision lineage.
An item that cannot receive a final class carries an explicit unresolved disposition instead of a forced consensus label.
D_t records the deterministic update from D_(t-1), Y*_t, and any approved backward revisions, so the cumulative gold set and current batch cannot drift apart.

#### 2.2 · Chat and history are pointers, not hidden dependencies
(Keeps the decision trace inspectable without making the final policy depend on a transcript.)
The package records immutable pointers and digests for every Human-AI Session transcript, human decision event, label revision, and adjudication note used in the round.
Each pointer names its access location, session identity, participant identity, and captured version.
The closed policy must remain executable without opening these histories, while the histories preserve why each decision and rule changed.

### 3 · Closed policy and policy diff
**The policy record**: the full annotation policy and its core guideline freeze with an explicit account of every change.

```text
📜 Θ_(t-1) CLOSED
        │
        ├── 🧾 policy diff
        │
        ▼
📜 Θ_t CLOSED
└── 📖 G_t CLOSED · core guideline
```

#### 3.1 · Θ_t and G_t freeze as one policy version
(Locks the complete executable policy rather than only its visible prose.)
Θ_t closed contains the core guideline G_t, boundary rules, canonical casebook, ordered decision procedure, uncertainty policy, and referenced execution wrappers.
The checkpoint records stable identifiers and digests for Θ_t and G_t and forbids any next-round consumer from reading their draft forms.
The human authority confirms that the closed policy expresses the intended construct before the closure receipt is written.

#### 3.2 · The policy diff explains semantic movement
(Makes clarification, concept revision, and editorial change distinguishable.)
The policy diff compares Θ_(t-1) with Θ_t by added, removed, and changed rules, examples, procedures, and wrappers.
Every entry is classified as editorial, clarification, or concept revision and names the accepting human decision.
Clarifications and concept revisions identify the earlier labels, regions, rules, and cases that may need backward review.

### 4 · Candidate, pre-label, and batch manifests
**The selection lineage**: three manifests reconstruct how the remaining corpus became the human-reviewed batch.

```text
🔎 C_t candidate manifest
        │
        ▼
🧠 P_t sealed pre-label manifest
        │
        ▼
💬 B_t human-batch manifest
```

#### 4.1 · Candidate manifest
(Records the broad pool before committee reading or human-batch composition.)
The C_t manifest records candidate item identifiers, source eligibility, region and novelty scores, retrieval reasons, exclusions, random seeds, and the prior checkpoint used to generate the pool.
It also records the candidate-pool size and every numeric quota as configuration values.
For Round 1, this manifest records the random sampling frame and B_1 draw instead of learned region retrieval.

#### 4.2 · Pre-label manifest
(Preserves independent model execution and the seal used for blind human judgment.)
The P_t manifest records every candidate pre-label, structured reason, confidence, executor identity and version, prompt wrapper, decoding settings, run time, and the exact Θ_(t-1) or G_(t-1) identifier applied.
It records when predictions were sealed and when they were opened after Y*_t locked.
For Round 1, the manifest records that no prior policy or pre-labeling existed and marks those fields not applicable.

#### 4.3 · Human-batch manifest
(Explains why each item entered B_t and how its selection affects later estimates.)
The B_t manifest records item identifiers, source pool, selection reason, stratum, inclusion probability, batch composition, and any replacement or exclusion.
After Round 1, every B_t item must occur in C_t, and every human decision in Y*_t must resolve to exactly one B_t item in every round.

### 5 · Audit and challenge metrics
**The measurement record**: comparable audit evidence and adaptive challenge evidence close in separate lanes.

```text
🟢 audit slice      🔴 challenge slice
     │                    │
     ▼                    ▼
📊 weighted quality   📈 discovery yield
     └──────────┬─────────┘
                ▼
          🧾 metrics bundle
```

#### 5.1 · Audit metrics support quality claims
(Preserves the denominator and weighting needed for comparison across rounds.)
The audit record names its target population, sampling strata, inclusion probabilities, weights, denominators, class and region results, correction loss, unresolved rate, and uncertainty interval.
Consensus-audit failures remain identifiable so unanimous shared errors cannot disappear inside an overall score.

#### 5.2 · Challenge metrics support learning claims
(Prevents an adaptively difficult batch from being reported as population quality.)
The challenge record reports disagreement yield, mismatch yield, novelty yield, new-rule yield, new-boundary yield, consensus-failure yield, and unresolved cases.
Audit and challenge values are stored separately and are never merged into one round accuracy.

#### 5.3 · Numeric choices are frozen configuration
(Keeps unresolved numbers explicit without reopening the conceptual checkpoint contract.)
Audit sample sizes, batch allocations, score thresholds, confidence levels, stability tolerances, consecutive-round counts, and risk limits are numeric configuration fields.
The checkpoint copies the values used in Round t together with the metric specification, code version, and calculation status.
A metric that cannot exist in Round 1 is marked not applicable with its reason rather than omitted from the bundle.

### 6 · Backward impact and next-round gate
**The transition gate**: impact obligations travel with the checkpoint, and only CLOSED status unlocks later use.

```text
🧾 policy diff
      │
      ▼
🔁 backward-impact queue
      │
      ▼
🔍 six-group closure checks
      │
      ├── 🔒 CLOSED   D_t + Θ_t/G_t + open risks → Round t+1
      └── ⛔ OPEN     no next-round use
```

#### 6.1 · The backward-impact queue is part of closure
(Carries every possible effect of policy change into an owned and traceable disposition.)
Each queue row names the changed policy entry, affected prior item or rule, impact reason, required action, owner, status, and disposition.
Closure does not require every low-risk row to be finished when the configured acceptance policy permits an explicit deferral.
Closure does require every known impact to be present, classified, and linked to the D_t derivation or to a carried next-round obligation.

#### 6.2 · Closure checks bind the six groups
(Defines the integrity tests that prevent a partial package from crossing the round boundary.)
The closure process verifies required fields, digests, schema versions, manifest membership, policy references, metric provenance, D_t derivation, unresolved dispositions, and impact-queue links.
Any missing group, failed digest, stale draft reference, or broken cross-artifact link leaves Round t OPEN.
The CLOSED receipt records the exact checks and the artifact digests that passed them.

#### 6.3 · Only checkpoint closure permits next-round use
(Makes the checkpoint identifier the exclusive dependency for every later round.)
Round t+1 must name CP_t and obtain D_t, Θ_t, G_t, configuration, manifests, metrics, and carried risks through that closed package.
No consumer may use a session workspace, mutable draft, detached metric export, or unclosed dataset as prior round state.
If a closed checkpoint is later revoked or superseded, every dependent round enters HOLD until its lineage is explicitly rebased.

## Aims

### A1 · 🧾 Checkpoint identity and closure receipt
- A1.1 · Round closure has one immutable identity and inspectable receipt.
  **Done when:** Section 1 names the identity, lineage, digest, validation, closure, and supersession records.

### A2 · 🏷 Human gold and history pointers
- A2.1 · Y*_t, D_t, and their human decision histories close without contradiction.
  **Done when:** Section 2 defines complete human decisions, deterministic cumulative data, unresolved dispositions, and immutable history pointers.

### A3 · 📜 Closed policy and policy diff
- A3.1 · Θ_t and G_t freeze with a human-confirmed, impact-bearing diff.
  **Done when:** Section 3 defines the closed policy contents, identifiers, digests, diff classes, and human acceptance.

### A4 · 📦 Candidate, pre-label, and batch manifests
- A4.1 · C_t, P_t, and B_t preserve complete selection and execution lineage.
  **Done when:** Section 4 defines each manifest and the membership links from candidates through human decisions.

### A5 · 📊 Audit and challenge metrics
- A5.1 · Round measurements remain reproducible and keep audit quality separate from challenge learning.
  **Done when:** Section 5 defines both metric families, their provenance, and their configurable numeric fields.

### A6 · 🔒 Backward impact and next-round gate
- A6.1 · Known impacts are carried forward and only a CLOSED checkpoint can feed the next round.
  **Done when:** Section 6 defines the impact queue, closure checks, exclusive dependency rule, and supersession response.

## States

### A1 · 🧾 Checkpoint identity and closure receipt
- ✅ A1.1 · Met; Section 1 defines one append-only checkpoint identity and its closure receipt.

### A2 · 🏷 Human gold and history pointers
- ✅ A2.1 · Met; Section 2 closes Y*_t and D_t together and preserves inspectable chat and decision-history pointers.

### A3 · 📜 Closed policy and policy diff
- ✅ A3.1 · Met; Section 3 freezes Θ_t and G_t and classifies every policy change for impact review.

### A4 · 📦 Candidate, pre-label, and batch manifests
- ✅ A4.1 · Met; Section 4 specifies the candidate, pre-label, and human-batch manifests with membership checks.

### A5 · 📊 Audit and challenge metrics
- ✅ A5.1 · Met; Section 5 separates audit quality from challenge yield and records numeric choices as configuration.

### A6 · 🔒 Backward impact and next-round gate
- ✅ A6.1 · Met; Section 6 makes the impact queue part of closure and gives transition authority only to CP_t CLOSED.

## Files

### 🔗 Related Board Pages · what this Page READS BY SCOPE
- `constrained by · ALL` · [QA0 §11](1-QA-semantic-contract/QA0-the-revised-conception/QA0-the-revised-conception.md)
  Use the approved names and lifecycle for C_t, B_t, P_t, Y*_t, D_t, and closed guideline states.
- `constrained by · ALL` · [QA0 §12](1-QA-semantic-contract/QA0-the-revised-conception/QA0-the-revised-conception.md)
  Preserve the distinction between a Calibration Round, its Human-AI Sessions, and its Checkpoint.
- `continues · ALL` · [QA0 §15](1-QA-semantic-contract/QA0-the-revised-conception/QA0-the-revised-conception.md)
  Turn the governing checkpoint concept into a complete immutable package and transition gate.

## Law
- 260806 JL · 🔒 A Calibration Round closes only through an immutable checkpoint
      Round t+1 may use Round t only through a CLOSED package whose six required groups passed the recorded closure checks.
      A completed session, a draft policy, or a partial artifact bundle has no transition authority.

## Glossary
- 📌 **Checkpoint package CP_t**: the immutable six-group artifact bundle and closure receipt for Calibration Round t.
- 📜 **Θ_t and G_t closed**: the frozen full annotation policy at Round t and its frozen core guideline component.
- 📦 **Manifest**: a versioned record of item membership, selection or execution settings, provenance, and identifiers for one round object.
- 🧾 **Policy diff**: the classified record of changes from Θ_(t-1) to Θ_t and the human decisions that accepted them.
- 🔁 **Backward-impact queue**: the owned list of earlier labels, regions, rules, or cases that a policy change may affect.
- #️⃣ **Artifact digest**: a content-derived value used to detect any change to a versioned artifact.

## Log
260806 · This DRAFT round replaced QB3's previous-edition external-license purpose with the immutable six-group checkpoint package and its exclusive next-round transition rule.
