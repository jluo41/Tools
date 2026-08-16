# One subjective-labeling project: the contract every run must preserve
state: ✅ SETTLED · approved conception and six-group migration roster
owner: JL
method: Translate QA0's approved conception into one project-level contract while keeping numeric choices in versioned configuration.

## Opening
What exact inputs, outputs, authority hierarchy, and non-goals define one subjective-labeling project?
A project means one corpus, one vague trait, and one identified human whose judgments define correctness.
Models can help calibrate and execute that meaning, but their agreement cannot replace it.
This contract fixes what enters, what leaves, who may decide, how every label is traced, and which numeric choices remain configuration.

**Where this page sits**: QA1 turns QA0's approved end-to-end conception into the base contract that later method and engine pages must preserve.

**What a project means**: One project binds a declared corpus and trait to one human semantic authority, such as one person deciding whether reviews show perceived empathy.

**Why it matters**: Without one fixed authority and artifact boundary, model votes, guideline text, and corpus labels can silently claim different meanings.

**Covered elsewhere**: QA0 governs the calibration rounds, stopping gates, sealed evaluation lifecycle, and production sequence that realize this contract.

**Settled versus configured**: The semantic contract is settled, while batch sizes, quotas, thresholds, model counts, and test size remain versioned numeric settings.

## Diagram
**The project contract**: six declared inputs pass through one authority hierarchy and produce one traceable output package.

```text
📥 SIX INPUTS
├── 🗄 C       corpus
├── 🔢 N       item count
├── 💭 z       vague trait
├── 🧑 h       semantic authority
├── 🤖 a       strong calibration agent
└── 🧠 M       optional weak LMs
        │
        ▼
⚖️ AUTHORITY
├── 🧑 h       semantic rulings
├── 🤖 a       calibration support
└── 🧠 M       execution evidence
        │
        ▼
📤 OUTPUT PACKAGE
├── 🗄 D*      labels + provenance
├── 📜 Θ*      executable policy
├── 📖 G*      core guideline
├── 🧪 T*      sealed human-gold test
├── 📊 S*      model scorecards
└── 🧾 A*      audit ledger
```

## Content

### 1 · Project unit
**One project**: the fixed semantic unit joins its declared inputs to one auditable output package.

```text
🧩 PROJECT P
├── 📥 I       C · N · z · h · a · M
├── 📤 O*      D* · Θ* · T* · S* · A*
├── 🏷 Y       HIGH · LOW · NONE
└── 🔐 key     corpus scope · trait · human
```

One project externalizes one person's decision policy for one vague trait over one declared corpus.
It does not discover an objective label that already exists outside that authority.

#### 1.1 · Semantic identity
(Defines which choices make this one project rather than another subjective target.)
The semantic identity is the combination of corpus scope, vague trait z, label schema, and identified human h.
Replacing h or changing the meaning of z creates a new semantic project, even if every model and file stays the same.
A material change to C or N creates a new corpus version that retains its relation to the earlier project record.

#### 1.2 · Label space
(Fixes the final class vocabulary without mixing class absence with uncertainty.)
Every completed item receives HIGH, LOW, or NONE under the human's accepted policy.
HIGH and LOW refer to trait-specific evidence rather than general positive or negative sentiment.
NONE means that the item lacks enough evidence of the trait, while uncertainty remains a separate field.

#### 1.3 · Project manifest
(Names the record that freezes the contract before calibration begins.)
The project manifest records the six inputs, corpus population, label schema, artifact locations, configuration version, and creation date.
Every round and final artifact points back to that manifest.
An implementation change may remain inside the same project only when it preserves the semantic identity and receives a new recorded version.

### 2 · Six-entry input roster
**The input roster**: each project declares six entries before any model-generated label can be interpreted.

```text
📥 INPUT ROSTER
├── ① 🗄 C      stable corpus items
├── ② 🔢 N      exact size of C
├── ③ 💭 z      vague trait seed
├── ④ 🧑 h      one semantic authority
├── ⑤ 🤖 a      strong calibration agent
└── ⑥ 🧠 M      zero or more weak LMs
```

The roster separates the object being labeled, the meaning being elicited, and the actors that assist with calibration or execution.
No outcome label, region label, prototype, or executable guideline is required at entry.

#### 2.1 · Corpus C and item count N
(Defines the data boundary and the one quantity derived directly from it.)
C is the declared collection of target items, written as C = {x_i} from i = 1 through N.
Each x_i has a stable item identifier and source metadata sufficient to reconstruct its place in the corpus.
N equals the exact number of items in C and becomes factual once the project manifest freezes the corpus version.

#### 2.2 · Vague trait z and human h
(Defines the subjective seed and the person whose meaning the system must reproduce.)
The trait seed z may begin as a short phrase without operational thresholds, boundary rules, or complete examples.
The identified human h owns what HIGH, LOW, and NONE mean for z in this project.
The project records h as one person rather than averaging that person's judgment with model predictions.

#### 2.3 · Strong agent a and optional weak LMs M
(Separates calibration support from the optional models that execute or test the policy.)
The strong calibration agent a organizes dialogue, compares cases, drafts candidate rules, tracks versions, and proposes checks.
M is the configured set of weak language models that may pre-label items, expose disagreement, or receive final scorecards.
M may be empty, and every nonempty M records each model identity, version, prompt wrapper, and decoding settings.

### 3 · Output package
**The final package**: labels, policy, test evidence, model scores, and audit history remain distinct artifacts.

```text
📤 OUTPUT PACKAGE
├── 🗄 D*      completed corpus
├── 📜 Θ*      frozen policy
│   └── 📖 G* core guideline
├── 🧪 T*      sealed human-gold test
├── 📊 S*      scorecard collection
└── 🧾 A*      provenance + audit ledger
```

The star marks the frozen final version used for the project's completion and final claims.
No output may erase which human, policy version, model, or audit route produced it.

#### 3.1 · Completed corpus D*
(Defines the data product without pretending that every accepted row has identical evidence.)
D* contains every item identifier, final class or accepted non-label disposition, diagnostic region when used, uncertainty record, and provenance state.
It is distinct from `D_cal*`, the cumulative human-confirmed development gold frozen at the calibration stop.
Human-confirmed labels, audited-machine labels, validated machine-accepted labels, and unresolved items remain distinguishable.
The corpus is complete only when every item has a final class or an explicitly accepted unresolved disposition that is not misreported as a label.

#### 3.2 · Frozen policy Θ* and core guideline G*
(Makes the full executable policy and its concise human-readable core unambiguous.)
Θ* is the final structured annotation policy containing G*, boundary rules, a compact casebook, an ordered decision procedure, and uncertainty handling.
G* is the frozen core guideline inside Θ*, not a separate source of meaning.
Both forms must be usable without access to the development chat history.

#### 3.3 · Test T*, scorecards S*, and ledger A*
(Defines the evidence package that supports model and corpus claims.)
T* is a sealed set of unseen items with human-gold labels created after Θ* freezes.
S* contains one scorecard for every configured weak LM under the same frozen policy and test protocol, and S* is an empty declared collection when M is empty.
A* preserves the manifest, round history, reasons, versions, sampling probabilities, model records, audits, and final provenance needed to reconstruct each claim.

### 4 · Authority hierarchy
**The authority hierarchy**: the human decides meaning, the accepted policy carries it, and every model remains subordinate evidence or support.

```text
🧑 h
├── ⚖️ final semantic rulings
├── 🏷 human-gold labels
└── 📜 acceptance of Θ* / G*
        │
        ├── 🤖 a   proposals · checks · memory
        ├── 🧠 M   predictions · reasons · scores
        └── 📊 A*  audits · uncertainty · estimates
```

Authority concerns who may define correctness, not which component is most capable or confident.
The hierarchy remains fixed even when a model outperforms another model or predicts most items correctly.

#### 4.1 · Human semantic authority
(States which decisions cannot be delegated without changing the project.)
Only h may confirm the final meaning of the trait, adjudicate a reviewed item as human gold, and accept a semantic change to Θ* or G*.
The human may reconsider an earlier judgment, but a concept revision triggers a recorded impact review of affected rules and labels.
Replacing this authority requires a new semantic project or an explicit multi-human study contract.

#### 4.2 · Strong calibration agent
(Defines high-capability assistance without transferring semantic control.)
Agent a may elicit reasons, compare counterexamples, detect contradictions, generalize candidate rules, and identify earlier items affected by a proposed change.
Its drafts become binding only after h accepts them.
An agent-generated label remains a model output until the human confirms it or an approved production policy accepts it with machine provenance.

#### 4.3 · Weak LMs and statistical audits
(Places optional executors and measurements at the evidence level.)
Weak LMs may apply a frozen policy, rank risk, disagree with one another, and receive comparable scores.
Statistical audits estimate error, coverage, and uncertainty under a declared sampling design.
Neither a model vote nor an audit statistic can redefine the trait or create human gold.

### 5 · Provenance and model agreement
**The evidence ladder**: every label states how it was obtained, and agreement never conceals the rung it occupies.

```text
🥇 HUMAN-CONFIRMED     gold relative to h
🥈 AUDITED MACHINE     accepted + audited
🥉 MODEL CONSENSUS     provisional evidence
🚨 UNRESOLVED          no final quality claim
```

Provenance is part of the label record rather than a footnote added after the corpus is complete.
The evidence ladder allows strong reliability claims without calling every machine-produced row gold.

#### 5.1 · Required provenance record
(Lists the minimum trace needed to reconstruct one final label.)
Each record preserves the item identifier, final class, decision authority, human-review status, policy version, model identity and version when used, selection route, round, timestamp, and audit disposition.
Any revision preserves the prior value and the reason for change in A*.
D* may summarize this record, but the underlying trace cannot be discarded.

#### 5.2 · Agreement is evidence, not gold
(Fixes the rule that model consensus raises confidence without becoming semantic truth.)
Agreement among weak LMs is evidence that the current policy may be executable.
It is not gold because models can share data, architecture, prompt, and cultural blind spots.
A consensus label remains provisional until human confirmation or acceptance through a declared production policy and probability-based audit, and even then its provenance remains machine rather than human.

#### 5.3 · Claims allowed by each tier
(Prevents one evidence tier from supporting a stronger claim than it earned.)
Human-confirmed gold supports item-level fidelity to h, subject to the human's own consistency.
Audited machine labels support corpus-level reliability claims under the sealed test, risk routing, and final audit that accepted them.
Provisional consensus and unresolved items support diagnosis and review routing, not final correctness claims.

### 6 · Non-goals and configurable settings
**The contract boundary**: semantic exclusions stay fixed while numeric operating choices remain visible configuration.

```text
🚫 NON-GOALS
├── 🌍 objective natural truth
├── 👥 population consensus
├── 🤖 model-vote gold
├── ⚙️ one vendor or architecture
└── 🔁 full round algorithm

🎚 CONFIGURATION
└── 🔢 sizes · quotas · thresholds · K · test size
```

Non-goals prevent downstream implementation choices from quietly widening the meaning of one project.
Configuration exposes numeric choices without turning them into blocking semantic decisions.

#### 6.1 · Semantic non-goals
(Names the claims and authorities that this one-human project does not create.)
The project does not claim an objective natural truth, a population-wide trait definition, or agreement among several human annotators.
It does not treat majority vote, unanimity, confidence, embedding distance, or benchmark performance as semantic authority.
It does not use NONE as an uncertainty bucket or allow an accepted machine label to masquerade as human gold.

#### 6.2 · Method and implementation non-goals
(Keeps this base contract separate from the lifecycle and engine choices that realize it.)
QA1 does not choose the calibration-round algorithm, retrieval method, region scorer architecture, production executor, model vendor, storage schema, or deployment system.
Those choices may vary while this contract remains intact, provided their identities and versions are recorded.
QA0 and its downstream method pages govern the lifecycle that produces the outputs named here.

#### 6.3 · Configurable numeric settings
(Lists the genuine numeric openings without asking the human to reopen the conception.)
Versioned configuration sets development and human-batch sizes, candidate-pool size, region quotas, consensus-audit fraction, novelty allocation, quality floors, epsilon, consecutive stable rounds K, unresolved-risk limits, confidence levels, weak-LM count, and final test size.
N is not an open threshold after C freezes because it is the observed size of the declared corpus.
Concrete model identities are recorded implementation selections rather than unresolved semantic decisions, so no Decision Now row blocks this settled page.

## Aims

### A1 · 🧩 Project unit
- A1.1 · One project has a stable semantic identity and manifest.
  **Done when:** A reader can distinguish a change of project meaning from a versioned implementation or corpus update.

### A2 · 📥 Six-entry input roster
- A2.1 · The project declares C, N, z, h, a, and optional M before calibration outputs are interpreted.
  **Done when:** Every input has one role, one recorded identity, and no hidden outcome-label prerequisite.

### A3 · 📤 Output package
- A3.1 · D*, Θ*/G*, T*, S*, and A* have separate inspectable meanings.
  **Done when:** A reader can identify the completed corpus, frozen policy, sealed human-gold test, model scorecards, and audit ledger without consulting chat history.

### A4 · ⚖️ Authority hierarchy
- A4.1 · The human, strong agent, weak LMs, and audits have non-overlapping authority roles.
  **Done when:** Only h can define semantic correctness, while every model contribution remains support, execution, or evidence.

### A5 · 🧾 Provenance and model agreement
- A5.1 · Every label keeps its evidence tier and model agreement never becomes gold by itself.
  **Done when:** D* and A* can distinguish human-confirmed, audited-machine, validated machine-accepted, and unresolved records.

### A6 · 🚫 Non-goals and configurable settings
- A6.1 · Semantic exclusions are settled and only genuine numeric choices remain configuration.
  **Done when:** No pending human decision is needed to distinguish the project contract from its lifecycle, engine, or numeric settings.

## States

### A1 · 🧩 Project unit
- ✅ A1.1 · Met; Section 1 defines the semantic identity, label space, and versioned project manifest.

### A2 · 📥 Six-entry input roster
- ✅ A2.1 · Met; Section 2 declares C, N, z, h, a, and optional M without circular label assumptions.

### A3 · 📤 Output package
- ✅ A3.1 · Met; Section 3 distinguishes D*, Θ*/G*, T*, S*, and A* and states their freeze and trace requirements.

### A4 · ⚖️ Authority hierarchy
- ✅ A4.1 · Met; Section 4 assigns semantic rulings only to h and keeps agents, models, and audits subordinate.

### A5 · 🧾 Provenance and model agreement
- ✅ A5.1 · Met; Section 5 fixes four evidence tiers and states that model agreement is evidence rather than gold.

### A6 · 🚫 Non-goals and configurable settings
- ✅ A6.1 · Met; Section 6 records the non-goals and routes every unresolved numeric choice to versioned configuration.

## Files

### 🔗 Related Board Pages · what this Page READS BY SCOPE
- `constrained by · ALL` · [QA0 §3](1-QA-semantic-contract/QA0-the-revised-conception/QA0-the-revised-conception.md)
  QA0 §3 supplies the approved input conception for the six-entry roster.
- `constrained by · ALL` · [QA0 §4](1-QA-semantic-contract/QA0-the-revised-conception/QA0-the-revised-conception.md)
  QA0 §4 supplies the approved meanings of the final deliverables.
- `constrained by · ALL` · [QA0 §5](1-QA-semantic-contract/QA0-the-revised-conception/QA0-the-revised-conception.md)
  QA0 §5 supplies the one-human semantic authority boundary.
- `constrained by · ALL` · [QA0 §19](1-QA-semantic-contract/QA0-the-revised-conception/QA0-the-revised-conception.md)
  QA0 §19 supplies the distinction between model disagreement, consensus, and diagnostic evidence.
- `constrained by · ALL` · [QA0 §28](1-QA-semantic-contract/QA0-the-revised-conception/QA0-the-revised-conception.md)
  QA0 §28 supplies the provenance tiers and reliability claims.
- `constrained by · ALL` · [QA0 §30](1-QA-semantic-contract/QA0-the-revised-conception/QA0-the-revised-conception.md)
  QA0 §30 supplies the boundary between settled conception and configurable settings.

## Law
- 260806 JL · 🧑 One human supplies semantic authority
      The identified human's accepted judgments and frozen policy define correctness for this project.
      The strong agent and optional weak LMs may calibrate, execute, compare, and audit, but model agreement is evidence rather than gold and every final label must retain provenance.

## Glossary
- 🗄 **Corpus C**: the declared collection of N target items for one project.
- 🔢 **Item count N**: the exact number of items in the frozen corpus version.
- 💭 **Vague trait z**: the initially underspecified subjective concept that calibration turns into an executable policy.
- 🧑 **Human h**: the one identified person whose accepted judgment defines semantic correctness for the project.
- 🤖 **Strong calibration agent a**: the capable agent that elicits reasons, drafts rules, tracks versions, and proposes checks without creating gold.
- 🧠 **Weak LMs M**: the optional set of language models that execute the frozen policy, provide diagnostic predictions, or receive final scores.
- 🗄 **D***: the completed corpus with final labels, uncertainty information, and preserved provenance.
- 📜 **Θ* and G***: the frozen structured annotation policy and its core guideline component.
- 🧪 **T***: the sealed unseen test whose gold labels come from h after the final policy freezes.
- 📊 **S***: the collection containing one comparable scorecard for each configured weak LM.
- 🧾 **A***: the audit and provenance ledger that reconstructs how every rule, label, score, and claim arose.
- 🪪 **Provenance**: the recorded origin, authority, policy version, model version, review route, and audit status of a label.

## Log
260806 · This DRAFT round replaced QA1's previous-edition cold-start purpose with the approved one-project contract for inputs, outputs, authority, provenance, non-goals, and configurable settings.
