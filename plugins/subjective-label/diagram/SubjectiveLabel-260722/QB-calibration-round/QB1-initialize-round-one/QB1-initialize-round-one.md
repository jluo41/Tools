# Round 1 initialization: a clean start without inherited labels
state: ✅ SETTLED
owner: RA
method: Validate one corpus snapshot, reserve the sealed test, and draw Round 1 randomly before semantic labeling begins.

## Opening
How is a project initialized so Round 1 can begin without labels or region guesses leaking into its first evidence?
The corpus must become a stable, valid snapshot before any semantic work starts.
Sealed-test IDs leave development early, while frozen embeddings support retrieval without deciding labels.
A random development batch then gives the human and strong agent a clean basis for producing the first gold, regions, reasons, and closed guideline.

**Where this page sits**: QA0 defines the governing conception, while this page turns its cold-start rule into the initialization and Round 1 handoff contract.

**Why it matters**: A selector that uses class or region guesses before the first human judgments would make the evidence confirm the assumptions that selected it.

## Diagram
**The clean cold start**: initialization isolates the final test, prepares retrieval, and lets human judgment create the first semantic artifacts.

```text
🗄 CORPUS
  │ 🧪 mechanical validation
  ▼
📌 C0 accepted snapshot
  │
  ├──▶ 🔒 T* sealed IDs · no calibration access
  │
  └──▶ 🧰 development IDs
          ├──▶ 🧠 E0 frozen embeddings · retrieval only
          └──▶ 🎲 random B1 · configured 50 to 60
                    │ 🚫 no y · no r · no G0 · no P1
                    ▼
              💬 human + strong agent
                    ▼
       🏷 Y*1 · 🗺 regions · 🧾 reasons · 📜 G1 closed
                    ▼
             📦 Round 2 handoff
```

## Content

### 1 · Validate one corpus snapshot
**The corpus gate**: mechanical checks produce one accepted item universe before any semantic selection begins.

```text
📥 raw review rows
        │
        ▼
🧪 VALIDATION
├── 🆔 stable unique item IDs
├── 📄 readable non-empty text
├── 🔗 source provenance
├── 👥 duplicate-family IDs
└── 🚫 prior outcome fields quarantined
        │
        ▼
📌 C0 · snapshot hash · acceptance report
```

#### 1.1 · Mechanical acceptance gate
(Defines what must pass before the project can split or sample the corpus.)
Every accepted review has one stable item ID, readable non-empty text, source provenance, and a content hash.
Exact or linked duplicates receive one duplicate-family ID so related copies cannot cross development and test.
Malformed rows and unresolved identifier collisions leave the eligible universe with a recorded reason.
Any existing class, region, score, or model outcome is quarantined outside the calibration schema and cannot seed Round 1.

#### 1.2 · Immutable corpus identity
(Makes every later artifact traceable to the same accepted input.)
The accepted rows, excluded rows, duplicate families, schema version, and snapshot hash define corpus snapshot C0.
Later corrections create a new snapshot version rather than rewriting C0 in place.
Every split, embedding, sample, label, and checkpoint names the C0 version it used.

### 2 · Reserve sealed-test IDs before development
**The early holdout**: an ID-only probability draw removes final-test items before any item-level semantic work.

```text
📌 eligible C0 IDs
        │ 🎲 recorded probability draw
        ▼
🔀 SPLIT MANIFEST
├── 🔒 T* IDs · sealed
└── 🧰 Cdev IDs · active

🛑 duplicate family · one side only
```

#### 2.1 · Reserve early
(Fixes the final-test membership before development can adapt to its contents.)
The initializer draws sealed-test IDs from eligible C0 before embedding retrieval, Round 1 selection, guideline work, or semantic item review.
The configured test count `n_test` is written before the draw, together with the sampling frame, random seed, selected IDs, and selection probabilities.
The test count is a project setting chosen from evaluation precision and labeling budget, not a blocking conceptual decision.

#### 2.2 · Keep the test outside calibration
(Prevents the reserved holdout from becoming development evidence.)
The active development manifest excludes every T* item and every member of its duplicate family.
Calibration loaders cannot open, retrieve, embed, pre-label, sample, or use T* in stopping decisions.
The test text receives blind human gold only after the final guideline G* freezes.
If any test result changes the guideline, wrapper, threshold, or executor choice, that test becomes validation data and a new sealed test is required.

### 3 · Freeze embeddings for retrieval only
**The representation boundary**: a versioned development index makes search repeatable without assigning semantic truth.

```text
🧰 Cdev text
     │ 🧠 frozen encoder + preprocessing
     ▼
📐 E0 development index
├── 🔎 neighbor retrieval
├── 🧹 duplicate diagnostics
├── 🗺 coverage diagnostics
└── 📊 later candidate ranking

🚫 E0 outputs · class · region · gold
```

#### 3.1 · Stable representation
(Defines the representation record that later rounds may reuse.)
Each development item receives one sentence embedding keyed by its stable item ID.
The index records the encoder identifier and version, preprocessing version, vector dimension, corpus snapshot, and checksum.
Changing the encoder or preprocessing creates a new migration version and never silently overwrites E0.

#### 3.2 · Retrieval authority only
(Stops vector similarity from becoming a circular label source.)
Embeddings may support retrieval, diversity, duplicate checks, coverage diagnostics, and candidate ranking after Round 1.
An embedding score may be called retrieval confidence or region score only after human-confirmed region evidence exists.
It is never called label quality, and it never creates class, region, or gold.
Round 1 B1 is drawn without consulting E0.

### 4 · Draw a random Round 1 development batch
**The first sampling frame**: a recorded random draw selects ordinary development items before a learned selector exists.

```text
🧰 eligible Cdev IDs
        │ 🎲 uniform draw without replacement
        ▼
📦 B1 · n_round1 items
├── 🔢 configured range · 50 to 60
├── 🧾 seed + frame + probabilities
└── 🕳 class + region + reason · blank
```

#### 4.1 · Random selection rule
(Gives the first concept-elicitation batch a visible sampling basis.)
The exact `n_round1` value is configured as an integer from 50 to 60 before selection.
The initializer draws B1 uniformly without replacement from eligible development IDs and records the seed, frame, selected IDs, and inclusion probabilities.
Neither embeddings, trait words, model scores, source semantics, nor anticipated difficulty may influence the draw.

#### 4.2 · Zero semantic priors
(Names the absent objects that make the first batch non-circular.)
B1 begins with no prior class labels, diagnostic region labels, prototypes, classifier, guideline G0, or sealed model pre-label record P1.
Its class, region, reason, and review-state fields are blank when the Human-AI Session opens.
The strong agent may organize the session, but it may not assign or suggest a region before dialogue establishes the human interpretation.

### 5 · Let dialogue create the first semantic record
**The Round 1 item loop**: human-first judgment produces class, region, reason, and reusable policy evidence together.

```text
📄 one random B1 item
        │
        ▼
🧑 initial human judgment
        │
        ▼
🤖 evidence question + alternative + flip test
        │
        ▼
🏷 H | L | N
🗺 H | L | N | HL | LN | HN | HLN
🧾 reason + revision trace
📜 keep | revise | add guideline rule
```

#### 5.1 · Human-first item decision
(Keeps semantic authority with the identified person during the cold start.)
The human gives the initial class judgment before the strong agent offers comparisons or rule language.
The agent asks which evidence matters, why the strongest alternative fails, and what smallest change would flip the decision.
The human confirms the final H, L, or N class and then the diagnostic region that explains what the item tests.
NONE remains semantic absence, while uncertainty stays in confidence, reason, and review state.

#### 5.2 · Co-created Round 1 outputs
(Turns concrete judgments into the first executable policy without hiding their history.)
Each reviewed item gains a final class or explicit unresolved state, one human-confirmed region, a decisive reason, and a revision trace.
Repeated reasons become proposed definitions, boundary tests, exclusions, decision steps, and compact canonical examples.
The human accepts, rejects, or reframes every substantive guideline rule.
The session retains earlier labels and rule drafts in history while only the final checkpoint values enter Y*1 and G1.

### 6 · Close Round 1 and hand off one auditable state
**The checkpoint packet**: six versioned artifact groups let Round 2 start from human-confirmed evidence rather than reconstructed chat.

```text
💬 Round 1 session
        │
        ▼
📌 CHECKPOINT 1
├── 🗄 corpus + split packet
├── 🧠 retrieval packet
├── 🎲 selection packet
├── 🏷 gold packet
├── 📜 policy packet
└── 🧾 audit packet
        │
        ▼
🔎 Round 2 may create C2 and P2
```

#### 6.1 · Checkpoint gate
(Defines when conversation output becomes a stable prior state.)
Every B1 item has a final class or explicit unresolved state before the checkpoint closes.
Each region and reason is checked against the final human decision, and substantive guideline changes receive human confirmation.
The checkpoint freezes cumulative gold D1 and guideline G1 closed under stable version identifiers.
No mutable chat draft may serve as the prior state for Round 2.

#### 6.2 · Six-part artifact handoff
(Names the complete Round 1 output that a later process may consume.)
The corpus packet contains C0, the active development manifest, the sealed T* ID manifest, exclusions, hashes, and duplicate-family assignments.
The retrieval packet contains E0 plus its encoder, preprocessing, snapshot, dimension, and checksum record.
The selection packet contains the B1 frame, configured count, random seed, selected IDs, inclusion probabilities, and empty-at-entry semantic fields.
The gold packet contains Y*1 and cumulative D1 with final class, human-confirmed region, reason, confidence, review state, and provenance.
The policy packet contains G1 closed, its structured guideline parts, accepted rule changes, and version identifier.
The audit packet contains the session trace, label and rule revisions, unresolved register, human confirmations, and checkpoint receipt.

#### 6.3 · Round 2 entry boundary
(States exactly what the next round may inherit and what remains unavailable.)
Round 2 may use D1, G1 closed, E0, and the remaining development IDs to create its broad candidate pool C2.
Weak executors may then create sealed pre-labels P2 under G1 closed.
P1 does not exist, and T* remains unavailable until final evaluation.

## Aims

### A1 · 🧪 Validate one corpus snapshot
- A1.1 · Initialization has one mechanically accepted and immutable corpus identity.
  **Done when:** The contract requires stable IDs, valid text, provenance, duplicate-family control, quarantined prior outcomes, exclusions, and a snapshot hash.

### A2 · 🔒 Reserve sealed-test IDs before development
- A2.1 · Final-test membership is fixed early and cannot influence calibration.
  **Done when:** The contract reserves T* by a recorded ID draw, removes duplicate families from development, blocks all calibration access, and states the invalidation rule.

### A3 · 🧠 Freeze embeddings for retrieval only
- A3.1 · The development embedding index is stable, versioned, and denied labeling authority.
  **Done when:** The contract records the index identity, permitted retrieval uses, migration rule, test exclusion, and prohibition on class, region, or gold creation.

### A4 · 🎲 Draw a random Round 1 development batch
- A4.1 · B1 is a reproducible random sample of 50 to 60 development items with no semantic priors.
  **Done when:** The contract records the configurable count, frame, seed, IDs, probabilities, blank semantic fields, and absence of G0 and P1.

### A5 · 💬 Let dialogue create the first semantic record
- A5.1 · Human-first dialogue produces the first class, region, reason, trace, and guideline evidence.
  **Done when:** The contract assigns semantic authority to the human and keeps uncertainty separate from class and region.

### A6 · 📦 Close Round 1 and hand off one auditable state
- A6.1 · Round 1 closes with a complete six-part packet that can initialize Round 2 without reconstructing chat.
  **Done when:** The contract names the corpus, retrieval, selection, gold, policy, and audit packets and limits Round 2 to checkpoint artifacts.

## States

### A1 · 🧪 Validate one corpus snapshot
- ✅ A1.1 · Met; Section 1 fixes the mechanical corpus gate and immutable C0 identity.

### A2 · 🔒 Reserve sealed-test IDs before development
- ✅ A2.1 · Met; Section 2 fixes early ID reservation, duplicate isolation, calibration exclusion, and test invalidation.

### A3 · 🧠 Freeze embeddings for retrieval only
- ✅ A3.1 · Met; Section 3 fixes E0 versioning, permitted retrieval uses, and the prohibition on semantic outputs.

### A4 · 🎲 Draw a random Round 1 development batch
- ✅ A4.1 · Met; Section 4 fixes a reproducible random B1 of configured size 50 to 60 with no semantic priors.

### A5 · 💬 Let dialogue create the first semantic record
- ✅ A5.1 · Met; Section 5 fixes human-first decisions and the co-created Round 1 record.

### A6 · 📦 Close Round 1 and hand off one auditable state
- ✅ A6.1 · Met; Section 6 fixes the checkpoint gate, six-part handoff, and Round 2 entry boundary.

## Files

### 🔗 Related Board Pages · what this Page READS BY SCOPE
- `constrained by · ALL` · [QA0 §10](QA-semantic-contract/QA0-the-revised-conception/QA0-the-revised-conception.md)
  Use the stable preprocessing layer and its retrieval-only authority boundary.
- `constrained by · ALL` · [QA0 §13](QA-semantic-contract/QA0-the-revised-conception/QA0-the-revised-conception.md)
  Use the approved random cold start and the rule that Round 1 begins without labels, regions, prototypes, or a guideline.
- `constrained by · ALL` · [QA0 §25](QA-semantic-contract/QA0-the-revised-conception/QA0-the-revised-conception.md)
  Use the reserve-early and label-late sealed-test protocol.

## Law
- 260806 JL · 🚫 Round 1 cannot inherit semantic structure
      A project must validate one corpus snapshot, reserve sealed-test IDs, freeze development embeddings for retrieval only, and draw B1 randomly before semantic labeling begins.
      No class, region, prototype, guideline, classifier, or model pre-label may affect the first draw.
      Round 1 closes only when its human-confirmed labels, regions, reasons, closed guideline, and audit trail form one versioned handoff.

## Glossary
- 📌 **Corpus snapshot C0**: the accepted item universe with stable IDs, hashes, exclusions, provenance, and duplicate-family assignments.
- 🔒 **Sealed test T***: item IDs reserved before development whose texts and outcomes remain unavailable to calibration.
- 🧠 **Stable embedding index E0**: a versioned vector index for development retrieval that carries no authority to assign class or region.
- 🎲 **Round 1 batch B1**: the random 50 to 60 development items that enter the first Human-AI Session with blank semantic fields.
- 📦 **Round 1 handoff**: the six versioned packets frozen at Checkpoint 1 for use by Round 2.

## Log
260806 · DRAFT round 2 replaced the previous-edition purpose of growing 60 seeds to 140 hard cases with project initialization and a non-circular Round 1 cold start governed by QA0.
