# The revised conception: how a subjective labeling system learns and stops
state: ✅ SETTLED · accepted by JL; numeric settings remain project configuration
owner: JL
method: Distill the 260806 discussion into one end-to-end contract before reconciling the older method and engine pages.
session: c1557d40-09e4-4887-8dc9-6a0b9bfce1c8

## Opening
How should a subjective-labeling system turn one person's initially vague trait concept into a reliable labeled corpus, a stable executable guideline, and comparable scores for several smaller language models?
The system enters with no outcome labels, and the human is the semantic authority.
Each calibration round must refine the human boundary, the guideline, and the labeled evidence together.
This page fixes the revised end-to-end conception before the older method pages are reconciled.

**Where this page sits**: This is the governing conception for the current edition, and QA1 through QF5 now decompose its contract into independently checked responsibilities.

**Why it matters**: The earlier edition assigned more authority to model consensus, rejected a random first batch, and mixed guideline development with evaluation in ways that the revised design no longer accepts.

**What is settled here**: The page fixes the input and output, the round lifecycle, Batch 2 generation, consensus auditing, co-adaptation, stopping logic, sealed final test, full-corpus completion, and final deliverables.

**What remains open**: Numeric thresholds, exact batch sizes, model choices, executor count, and final test size remain configuration decisions rather than hidden assumptions.

## Writing Style
**Language and sentences**: Use plain English, one sentence per source line, and define every project-specific term before relying on it.

**Conceptual level**: Describe the method and its artifacts without committing to code, model vendors, or one classifier architecture.

**Authority**: State clearly whether a judgment belongs to the human, the strong labeling agent, a small language model, or a statistical audit.

**Evidence status**: Separate settled design decisions, provisional defaults, open numeric choices, and claims that require an empirical run.

**Examples**: Generalize rules from examples and keep only a small canonical casebook, rather than copying the development corpus into the core guideline.

## Diagram
**The revised system**: one human concept is elicited through repeated rounds, frozen, tested, and then used to complete the corpus.

```text
📥 INPUTS
  🗄 corpus C · 💭 vague trait · 🧑 human · 🤖 labeling agent
       │
       ▼
🔁 CALIBRATION ROUNDS
  🎲 B1 random → 🧭 seven regions → 🔎 later candidate pools
  🧠 pre-label → 💬 human session → 📌 checkpoint → 📜 guideline update
       │
       ├──▶ 🧑 human concept H_t becomes clearer
       ├──▶ 📜 annotation policy Θ_t becomes executable
       └──▶ 🏷 human-confirmed data D_t grows
       │
       ▼
🛑 QUALITY + STABILITY + COVERAGE GATES
       │
       ▼
🔒 freeze G* → 🧪 sealed test T* → 📊 LM scorecard S*
       │
       ▼
🏭 label remaining corpus → 🚨 review risk queue → 📦 final D*
```

## Content

### 1 · The revised conception
**The center of the method**: the system elicits and externalizes a subjective decision function rather than discovering an existing objective label.

```text
💭 vague human concept
        │  concrete cases + dialogue
        ▼
🧑 clearer internal boundary H_t
        │  externalization
        ▼
📜 executable annotation policy Θ_t
        │  unseen-item execution
        ▼
🏷 labels that match the human authority
```

#### 1.1 · What is being learned
(Defines the target as a human-grounded decision policy rather than a hidden natural truth.)
The corpus does not arrive with an objective outcome label that the system can recover.
The target is the judgment of one identified human for one subjective trait in one stated labeling project.
The process learns how that person distinguishes HIGH, LOW, and NONE, including the boundaries and exceptions that were initially hard for the person to verbalize.
The final guideline is the external, inspectable form of that learned decision policy.

#### 1.2 · Why interaction is necessary
(Explains why neither an initial definition nor a model-only pass is sufficient.)
A vague trait name does not specify what evidence counts, how strong evidence must be, or what to do when two interpretations compete.
Concrete reviews force those hidden choices to become visible.
The strong labeling agent uses dialogue to ask for the reason behind a judgment, test counterexamples, and turn repeated judgments into general rules.
The human remains the semantic authority throughout this process.

#### 1.3 · What convergence means
(Defines the fixed point sought by the iterative process.)
The process approaches convergence when the human's stable judgment, the written annotation policy, and a model's execution of that policy agree on unseen items.
This agreement must coexist with adequate quality, boundary coverage, and low unresolved risk.
A stable but poor guideline is not converged.

### 2 · What changed from the previous edition
**The edition change**: the revised system moves authority from model consensus to one human and moves evaluation onto sealed unseen data.

```text
📘 PREVIOUS EDITION              📗 REVISED EDITION
🤖 panel stands in for people   🧑 one human is semantic authority
🔎 model chooses first cases    🎲 Round 1 starts random
✅ consensus auto-passes        🎲 consensus receives random audit
📦 one gallery score            🧪 audit + challenge + sealed test
⚙️ cascade decides labels       🔎 scorer first ranks candidates
```

#### 2.1 · Authority changed
(States the most important break from the existing skill contract.)
The previous skill description framed a panel of language models as a substitute for a team of human annotators.
The revised conception does not accept model agreement as the source of semantic truth.
One human defines the target construct through repeated judgments, and every model is evaluated against that person's final decisions.

#### 2.2 · Cold start changed
(Records that the first batch is now random rather than model-retrieved.)
The previous QA1 rejected a random first batch and asked a strong model to retrieve relevant items before the concept existed.
The revised design starts Round 1 with a random development batch of roughly 50 to 60 items.
Those items have no prior class labels or region assignments.
Their labels, regions, reasons, and first guideline draft are produced during Human-AI dialogue.

#### 2.3 · Consensus handling changed
(Replaces automatic passage with a measurable audit mechanism.)
The previous QA2 allowed unanimous model labels to pass without human attention.
The revised design treats unanimity as committee consensus, not as gold.
A stratified random sample from the consensus pool enters every human review batch so that shared model blind spots can be measured.

#### 2.4 · Evaluation changed
(Separates development feedback from the final claim.)
The previous design relied heavily on gallery agreement and an external engine-level license.
The revised design keeps round-level audit and challenge measurements for development, then reserves a sealed item test for the final guideline and model scorecard.
External public-data validation may remain useful, but it answers a different generalization question and does not replace the project-specific human gold test.

### 3 · Inputs
**The complete input contract**: the process begins with a corpus, a vague concept, one human, and a labeling agent rather than with labels.

```text
🗄 C = {x1 ... xN}   💭 trait seed z
         \             /
          \           /
           ▼         ▼
            🧑 human h
                +
            🤖 strong agent a
                │
                ▼
          🔁 calibration system
```

#### 3.1 · Corpus
(Defines the large N object being labeled.)
The corpus is a collection of N review texts drawn from one stated target population.
Each review has a stable item identifier and may carry source metadata, but it has no required outcome label at entry.
The corpus must be large enough that only a small fraction can receive direct human attention during calibration.

#### 3.2 · Subjective trait seed
(Defines how little may be known at entry.)
The trait seed may be only a phrase such as openness, empathy, dismissiveness, or perceived conscientiousness.
It may include an initial intuition, but it need not contain operational thresholds or complete boundary rules.
The process is responsible for turning that vague seed into an executable policy.

#### 3.3 · Human semantic authority
(Names the person whose judgment the output is intended to match.)
One person participates repeatedly and owns the meaning of the labels for this project.
The design does not average that person's judgment with the models.
If the project later wants a population-level human consensus, that becomes a different study with multiple annotators and a separate adjudication contract.

#### 3.4 · Strong labeling agent and optional weak executors
(Separates the conversational helper from the models being evaluated.)
The strong labeling agent organizes the dialogue, asks clarifying questions, drafts rules, tracks versions, and proposes checks.
Candidate weak language models execute a frozen guideline during pre-labeling and final evaluation.
The strong agent may analyze their errors, but it cannot override the human's semantic decision.

### 4 · Outputs
**The delivery contract**: the project ends with labels, an executable policy, a test set, model scores, and an audit trail.

```text
📤 FINAL DELIVERIES
├── 🗄 D*   full corpus with labels + provenance
├── 📜 G*   frozen human-readable and machine-readable guideline
├── 🧪 T*   sealed human-gold evaluation set
├── 📊 S*   one scorecard per candidate LM
└── 🧾 A*   round history, reasons, versions, and audits
```

#### 4.1 · Fully labeled corpus
(Defines the primary data artifact without pretending every row is human-reviewed.)
Every corpus item receives a final class label and a provenance state.
Human-confirmed items, audited-machine labels, validated machine-accepted labels, and unresolved items must remain distinguishable.
The project may call the corpus complete only after the unresolved and high-risk queues satisfy the completion policy.

The cumulative human-confirmed development gold at the stopping checkpoint is `D_cal*`.
It is an intermediate calibration artifact and must not be confused with the completed corpus `D*`, which exists only after production, reconciliation, and audit.

#### 4.2 · Final annotation policy
(Defines the guideline as more than prose.)
The final policy must be readable by a person and executable by a model.
It contains label definitions, evidence rules, boundary tests, a decision procedure, uncertainty handling, and a small casebook.
It must not require access to the development chat history in order to be used.

#### 4.3 · Model scorecard
(Defines the comparative model output.)
Each candidate weak language model receives the same frozen guideline and the same sealed test items.
Its predictions are compared with human gold using one shared protocol.
The scorecard reports absolute performance, class and region errors, stability, and guideline uplift over a minimal instruction.

#### 4.4 · Audit record
(Defines the evidence needed to support reliability claims.)
The project preserves round membership, pre-labels, human revisions, reasons, guideline versions, model identities, selection probabilities, and final provenance.
This record makes it possible to reconstruct how a label or rule entered the system.

### 5 · Human semantic authority
**The authority boundary**: models surface patterns and inconsistencies, while the human decides what the trait means.

```text
🤖 propose evidence ─┐
🤖 expose conflicts ─┼──▶ 🧑 human decision ──▶ 🏷 gold label
🤖 draft rule       ─┘          │
                                └──▶ 📜 accepted guideline rule
```

#### 5.1 · What the human decides
(Lists the decisions that cannot be delegated without changing the target.)
The human decides the final HIGH, LOW, or NONE label for reviewed items.
The human decides whether an item is typical, pairwise ambiguous, or ambiguous across all three labels.
The human also decides whether a proposed guideline change clarifies the existing intention or changes the construct itself.

#### 5.2 · What the agent contributes
(Defines assistance without transferring authority.)
The strong agent can compare cases, locate contradictions, propose generalized language, ask counterfactual questions, and record reasons.
It can warn when the same reasoning has produced incompatible labels.
It can also identify which previous items may be affected by a new rule.
These actions improve consistency and memory, but they do not create gold without human confirmation.

#### 5.3 · Clarification versus concept revision
(Separates making an intention explicit from changing the intended meaning.)
Clarification preserves the human's intended construct and makes an implicit boundary explicit.
Concept revision changes what the human means by HIGH, LOW, or NONE.
A concept revision triggers a backward impact review of older labels and guideline rules.
The system must not silently treat a semantic change as a harmless wording edit.

### 6 · Label and uncertainty schema
**Three separate fields**: class, region, and uncertainty answer different questions and must never be collapsed.

```text
🏷 class y      = HIGH | LOW | NONE
🗺 region r     = H | L | N | HL | LN | HN | HLN
🌡 uncertainty  = confidence + reason + review state

🚫 NONE ≠ uncertain
🚫 boundary region ≠ final class
```

#### 6.1 · Final class
(Defines the outcome required for every completed item.)
The final class is one of HIGH, LOW, or NONE.
HIGH and LOW must be defined in trait-specific evidence terms rather than as positive and negative sentiment.
NONE means the review lacks sufficient evidence of the target trait.

#### 6.2 · NONE is not abstention
(Protects the label distribution from uncertainty leakage.)
NONE records absence of trait evidence.
Annotator uncertainty belongs in confidence, rationale, disagreement state, or unresolved status.
Using NONE as an uncertainty bucket would mix semantic absence with procedural doubt and corrupt both training and evaluation.

#### 6.3 · Region is diagnostic metadata
(Explains why the seven-region assignment does not replace the class.)
An H-N boundary item still receives a final class of H or N after human judgment.
The region says why the item was informative and which boundary it probes.
This second label supports sampling, diagnostic scoring, and guideline maintenance.

### 7 · The seven-region map
**The diagnostic geometry**: three centers, three pairwise boundaries, and one triple junction organize evidence discovery.

```text
                  🟢 H center
                 /           \
          🟡 H-L boundary   🟡 H-N boundary
             /                   \
       🔵 L center ─ 🟡 L-N ─ ⚪ N center
                  \   🔴   /
                   H-L-N junction
```

#### 7.1 · Three typical regions
(Defines the center examples that anchor each class.)
The H, L, and N center regions contain cases that clearly instantiate one class under the current human concept.
These examples provide prototypes, simple rules, and sanity checks.
They are useful for coverage and production auditing even though they usually yield less new boundary information.

#### 7.2 · Three pairwise boundaries
(Defines the cases that distinguish adjacent or confusable classes.)
The H-L region contains cases where trait presence is clear but intensity or direction is difficult to distinguish.
The L-N region tests weak evidence against true absence.
The H-N region tests strong apparent evidence against absence, irony, irrelevant praise, or other confounds.

#### 7.3 · Triple junction
(Defines the most globally ambiguous cases.)
The H-L-N region contains cases for which all three labels remain plausible before adjudication.
These items often expose a missing prerequisite in the decision procedure rather than a single bad threshold.
They should be rare but explicitly represented.

#### 7.4 · Region assignments evolve
(Prevents early diagnostic labels from becoming permanent facts.)
Round 1 region assignments are human interpretations formed during dialogue.
As the concept becomes clearer, a previous boundary case may become typical, or a typical case may reveal a hidden ambiguity.
Region changes must be versioned rather than overwritten without history.

### 8 · The dual optimization process
**Two coupled learners**: the human clarifies an internal boundary while the external policy learns to express it.

```text
🧑 H_t  human latent concept
   │         ▲
   │ cases   │ model errors + counterexamples
   ▼         │
📜 Θ_t  external annotation policy
   │
   ▼
🤖 execution on unseen items
```

The figure above shows the coupling; the round that produces it, step by step and in the order it happens, is stated as QA0-Display1.

#### 8.1 · Human-side adaptation
(Describes the legitimate change occurring inside the annotator.)
The human may begin with only an intuitive sense of the trait.
Repeated comparisons force the person to notice which evidence is decisive, which evidence is irrelevant, and where intensity thresholds lie.
The person's internal decision boundary becomes more explicit and often more consistent.

#### 8.2 · Guideline-side adaptation
(Describes the inspectable optimization target.)
The annotation policy is revised after each round to encode the human's current boundary.
It accumulates definitions, tests, exceptions, and examples only when they improve execution on new cases.
Its quality is judged operationally by transfer to unseen items and unseen executors.

#### 8.3 · Authority asymmetry
(Prevents co-adaptation from becoming model-driven concept drift.)
The two learners are coupled but not equal.
The model may reveal that a rule is unclear, but the human decides whether to rewrite the rule or retain the concept and accept that the model is weak.
The optimization objective is human fidelity, not model convenience alone.

### 9 · The annotation policy as the optimized object
**A structured policy**: the learned object contains rules, cases, procedures, and uncertainty handling rather than one prose block.

```text
Θ_t
├── 📜 G_t   core definitions and evidence rules
├── 🧭 R_t   pairwise and triple boundary rules
├── 📚 E_t   compact canonical casebook
├── 🔢 Q_t   ordered decision procedure
└── 🚨 U_t   uncertainty and escalation policy
```

#### 9.1 · Core guideline
(Defines the part every human and model executor must read.)
The core guideline states the trait definition, label meanings, positive and negative evidence, exclusions, and boundary tests.
It should remain concise enough that a smaller language model can follow it without losing the hierarchy.
It must distinguish semantic rules from model-specific formatting instructions.

#### 9.2 · Canonical casebook
(Defines how examples support rather than replace generalization.)
The casebook contains a small set of typical examples, counterexamples, and boundary pairs.
Each case includes the final label, region, decisive evidence, rejected alternative, and human reason.
The casebook is selected for explanatory value rather than for exhaustive coverage of development items.

#### 9.3 · Decision and uncertainty procedures
(Defines the executable order and safe failure behavior.)
The policy tells an executor which question to ask first, how to apply boundary tests, and when to report uncertainty.
An uncertain executor still predicts H, L, or N when required, but it also reports confidence and a reason.
Production routing may escalate low-confidence or conflicting predictions to human review.

### 10 · Corpus preparation
**The stable preprocessing layer**: embeddings make search cheap and repeatable without defining the labels.

```text
🗄 N reviews
    │
    ▼
🧠 sentence embedding
    │
    ├──▶ 🔎 retrieval
    ├──▶ 🧹 deduplication
    ├──▶ 🗺 coverage
    └──▶ 📐 region scoring

🚫 vector distance alone never creates gold
```

#### 10.1 · One-time vectorization
(Defines the economical representation step.)
Every review is converted into a sentence-level embedding and stored with a stable model identifier and item identifier.
The vectors may be reused across rounds because the representation model is frozen during one project unless an explicit migration occurs.
This step is cheaper than repeatedly asking a language model to read the whole corpus.

#### 10.2 · Permitted uses
(Lists the retrieval jobs that embeddings may perform.)
Embeddings support nearest-neighbor search, diversity sampling, duplicate detection, coverage diagnostics, and candidate ranking.
They also support simple region prototypes or a lightweight classifier trained on human-confirmed items.
These uses decide which items deserve attention, not what their final labels are.

#### 10.3 · Geometry caveat
(Prevents semantic similarity from being mistaken for label similarity.)
Semantically similar sentences can carry opposite trait evidence.
Boundary regions are therefore hypotheses produced by a scorer and confirmed by human judgment.
An embedding score is called region confidence or retrieval confidence, never label quality.

### 11 · Versioned round artifacts
**The round state**: every selected item, model prediction, human decision, and guideline version has a distinct name.

```text
📜 G_(t-1) closed
        │
        ▼
🔎 C_t candidate pool ──▶ 🧠 P_t sealed pre-labels
        │                         │
        └──────────┬──────────────┘
                   ▼
              💬 B_t human batch
                   │
                   ▼
          🏷 Y*_t + 📜 G_t draft
                   │
                   ▼
          📌 D_t + 📜 G_t closed
```

#### 11.1 · Data objects
(Defines candidate, review, and cumulative sets.)
C_t is the broad candidate pool generated for Round t, such as 200 items.
B_t is the smaller set that actually enters Human-AI review, such as 50 items.
Y*_t is the final human-confirmed annotation for B_t.
D_t is the cumulative human-confirmed data after Round t.

#### 11.2 · Guideline states
(Defines the difference between a stable input and a changing output.)
G_(t-1) closed is the frozen guideline used for pre-labeling Round t.
G_t draft changes during the Human-AI session.
G_t closed is frozen at the checkpoint and becomes the input to Round t+1.

#### 11.3 · Pre-label record
(Defines why model predictions are preserved even when hidden from the human.)
P_t contains every weak model's predicted class, confidence, structured reason, and model version.
The predictions are created before Human-AI review and then sealed.
After human labels are locked, P_t is compared with Y*_t to measure transfer and diagnose guideline failure.

### 12 · Round, Session, and Checkpoint
**The unit hierarchy**: a calibration round owns one complete update, while sessions are only conversations inside it.

```text
🔁 CALIBRATION ROUND t
├── 🔎 prepare candidate pool
├── 🧠 create sealed pre-labels
├── 💬 Human-AI Session 1
├── 💬 optional Session 2
└── 📌 checkpoint closes data + guideline
```

#### 12.1 · Calibration Round
(Names the method-level unit that is comparable across iterations.)
A Calibration Round begins with a closed prior state and ends with a new closed state.
It has one candidate-generation policy, one pre-label record, one human-reviewed batch, and one checkpoint.
Round numbers are the primary version axis for the method.

#### 12.2 · Human-AI Session
(Names the conversational unit without giving it lifecycle authority.)
A Session is one continuous interaction between the human and strong agent.
One round may contain one session or several sessions if the batch is split across time.
A session does not close the round until its labels and guideline changes pass the checkpoint.

#### 12.3 · Checkpoint
(Defines the closure event between rounds.)
The checkpoint confirms unresolved cases, freezes the cumulative gold data, freezes the next guideline version, computes round metrics, and records open risks.
Only checkpoint artifacts may be used as the prior state for the next round.

### 13 · Round 1 cold start
**The first batch**: random development items acquire labels, regions, reasons, and the first guideline through dialogue.

```text
🗄 development corpus
        │
        ▼
🎲 random B1, about 50 to 60
        │  no prior y · no prior r · no prior G
        ▼
💬 human + strong agent
        │
        ├──▶ 🏷 Y*_1
        ├──▶ 🗺 seven-region assignments
        ├──▶ 🧾 reasons and chat history
        └──▶ 📜 G_1 draft → closed
```

#### 13.1 · Why Round 1 is random
(Explains the role of randomness before a learned selector exists.)
Before any human-confirmed labels exist, the seven regions are unknown.
A model-guided first batch would encode an unvalidated model interpretation of the vague trait into the evidence the human sees.
A random development batch gives the first concept elicitation a visible sampling basis and exposes ordinary corpus language.

#### 13.2 · What Round 1 does not assume
(Removes circular prerequisites from the cold start.)
Round 1 does not assume class labels, region labels, prototypes, a trained classifier, or a reliable guideline.
The strong agent may organize and compare the random items, but it cannot claim that an item belongs to a region before the dialogue establishes that interpretation.

#### 13.3 · Four simultaneous outputs
(Makes clear that labeling and guideline drafting occur in the same interaction.)
The human and agent assign a final H, L, or N label to each reviewed item.
They also assign a diagnostic region, record the human's reason, and revise a guideline draft.
Chat history preserves the questions, label changes, rule changes, and unresolved points that produced the checkpoint.

### 14 · Inside the Human-AI Session
**The interaction loop**: one item creates a judgment, a reason, a boundary test, and an update candidate.

```text
📄 review x
    │
    ▼
🧑 initial judgment
    │
    ▼
🤖 clarify evidence + contrast alternatives
    │
    ▼
🏷 final class + 🗺 region + 🧾 reason
    │
    └──▶ 📜 keep, revise, or add guideline rule
```

#### 14.1 · Human-first judgment
(Reduces anchoring by making the target decision before showing machine votes.)
For Round 2 onward, weak-model pre-labels remain hidden while the human makes the initial judgment.
The strong agent may ask questions about the review, but it should not reveal the committee vote or confidence before the human label is recorded.
This preserves the value of comparing pre-label with post-session gold.

#### 14.2 · Reason elicitation
(Turns an answer into reusable knowledge.)
The agent asks which words or implications support the chosen label.
It asks why the strongest alternative was rejected and what change to the review would flip the label.
These answers supply evidence rules, exclusions, and boundary tests.

#### 14.3 · Iteration inside an item
(Allows correction without losing the history of how the decision formed.)
The human may revise an initial label after comparing it with another case or noticing an inconsistent rule.
Every revision remains in the trace, while the final human decision becomes Y*_t.
The agent records whether the revision reflects clarification, concept revision, or correction of a momentary mistake.

### 15 · The round checkpoint
**The closure gate**: the checkpoint turns a conversation into stable data, a stable policy, and measurable deltas.

```text
💬 session outputs
      │
      ▼
📌 CHECKPOINT
├── 🧑 adjudicate unresolved items
├── 🏷 lock Y*_t and update D_t
├── 📜 review G_t draft and freeze G_t closed
├── 📊 compare P_t with Y*_t
└── 🚨 record regression and migration risks
```

#### 15.1 · Human confirmation
(Defines what must be closed before the round can advance.)
Every reviewed item must have a final class or an explicit unresolved state.
Boundary assignments and reasons must agree with the final class.
Any unresolved item that affects a general rule remains visible rather than being forced into consensus.

#### 15.2 · Guideline freeze
(Defines how a draft becomes a versioned input.)
The human reviews substantive rule changes and confirms that they preserve the intended concept.
The checkpoint distinguishes semantic edits from editorial edits.
The frozen version receives a stable identifier and cannot be changed in place.

#### 15.3 · Regression and impact review
(Protects earlier labels from new rules.)
Every substantive guideline change is tested against affected earlier gold items.
If the human concept changed, the system identifies old items near the changed boundary for re-review.
The cumulative gold set is versioned with the policy that produced it.

### 16 · Candidate generation after Round 1
**The broad funnel**: later rounds retrieve many region-conditioned candidates before deciding which few deserve human attention.

```text
📌 D_(t-1) + 📜 G_(t-1) + 🗺 region anchors
                         │
                         ▼
                 🗄 remaining corpus
                         │
                         ▼
             🔎 region retrieval and ranking
                         │
                         ▼
                  📦 C_t, about 200
```

#### 16.1 · Candidate pool versus human batch
(Prevents the word batch from hiding two different costs.)
C_t is deliberately larger than the set a human will inspect.
It provides enough candidates for all seven regions, confidence bands, novelty checks, and committee comparison.
B_t is created only after pre-labeling and audit selection.

#### 16.2 · Region-conditioned retrieval
(Defines how previous human judgments guide the next search.)
The system retrieves candidates near each of the seven region prototypes or decision patterns.
Typical regions may contribute many inexpensive candidates, while rare boundaries may contribute fewer but more informative ones.
Quotas remain configurable because corpus prevalence and learning goals differ by round.

#### 16.3 · Coverage and novelty
(Prevents the selector from repeatedly mining one familiar boundary.)
Candidate generation reserves capacity for regions that have little confirmed evidence.
It also includes items far from every known prototype or poorly represented cluster.
Novelty is a diagnostic reason for review, not a new class label.

### 17 · Region scoring and ranking
**The first-stage scorer**: a lightweight model ranks region membership without claiming final correctness.

```text
🧠 frozen embeddings
        +
🏷 D_(t-1) region labels
        │
        ▼
📐 region scorer
├── 🟢 prototype similarity
├── 📏 linear margin
├── 🧠 optional MLP after more data
└── 🔍 novelty distance
        │
        ▼
📊 seven ranked candidate lists
```

#### 17.1 · Data-efficient default
(Explains why a complex neural model is not required after only one round.)
With roughly 50 confirmed items, nearest prototypes, nearest neighbors, or a linear probe are easier to interpret and less likely to overfit than an MLP.
An MLP may become useful after cumulative gold data grows.
Attention is not a default when the input is already one pooled embedding vector.

#### 17.2 · Example scoring logic
(Shows how centers and boundaries can be ranked without pretending the geometry is truth.)
An H-center candidate has high similarity to the H prototype and a large margin over L and N.
An H-L boundary candidate has similar H and L scores, with both stronger than N.
An H-L-N candidate has low margins among all three scores.
The scorer can rank these patterns even before a dedicated seven-class model is trained.

#### 17.3 · Confidence vocabulary
(Prevents retrieval confidence from being reported as annotation quality.)
The scorer may report region score, margin, or prototype similarity.
These numbers describe how strongly an item matches the current selection model.
Only human confirmation creates a gold region and class label.

### 18 · Multi-model pre-labeling
**The second-stage reader panel**: several weak language models independently apply the previous closed guideline to the candidate pool.

```text
📜 G_(t-1) closed
        │
        ├──▶ 🧠 LM A ─┐
        ├──▶ 🧠 LM B ─┼──▶ P_t
        └──▶ 🧠 LM C ─┘

P_t = class · confidence · reason · model/version
```

#### 18.1 · Independent execution
(Defines the committee condition needed for disagreement to mean something.)
Each model receives the same frozen guideline and candidate item without seeing another model's answer.
The models use a fixed output schema.
Their identities, versions, prompt wrapper, and decoding settings are recorded.

#### 18.2 · Structured reasons
(Makes model errors useful for guideline diagnosis.)
Each pre-label includes the predicted class, cited evidence, applied rule, rejected alternative, and confidence.
The system does not require hidden chain-of-thought.
A concise structured rationale is sufficient for comparing the model's interpretation with the human reason.

#### 18.3 · Sealing
(Protects the pre-post comparison from human anchoring.)
P_t is generated before the Human-AI session and hidden from the human during first-pass labeling.
It is opened only after Y*_t is locked.
This turns pre-labeling into both a selection mechanism and a valid transfer measurement.

### 19 · Disagreement, consensus, and diagnostic pools
**Three branches**: committee disagreement, committee consensus, and geometry-model mismatch carry different information.

```text
📦 C_t + 🧠 P_t
        │
        ├──▶ 🔴 D_t^disagree   models choose different classes
        ├──▶ 🟢 S_t^consensus  models choose the same class
        └──▶ 🟡 M_t^mismatch   scorer, models, or novelty conflict
```

#### 19.1 · Disagreement pool
(Defines the primary challenge source.)
An item enters the disagreement pool when committee members predict different classes or apply incompatible rules.
These cases are likely to reveal unclear boundaries, missing rules, model-specific failure, or genuine ambiguity.
They receive high priority for human review.

#### 19.2 · Consensus pool
(Defines agreement as a testable hypothesis rather than an automatic gold label.)
An item enters the consensus pool when all required committee members predict the same class.
Consensus increases confidence that the current guideline is executable.
It does not prove correctness because models may share training biases, prompt interpretations, or missing rules.

#### 19.3 · Diagnostic mismatch pool
(Captures errors that class disagreement alone would miss.)
An item enters the mismatch pool when the region scorer predicts one area but the committee reasons as if it belongs elsewhere.
It also enters when the item is novel relative to every known region.
These cases diagnose selection-model failure, representation limits, and missing concept coverage.

### 20 · Building the human review batch
**The final Batch t**: challenge cases, consensus audit, and novelty are composed under explicit quotas.

```text
🔴 disagreement sample ─┐
🟡 mismatch/novelty   ──┼──▶ 💬 B_t human review
🟢 consensus audit    ──┘

example capacity 50
  25 to 30 challenge · 10 to 15 consensus audit · remainder novelty/coverage
```

#### 20.1 · Disagreement priority with a capacity limit
(Handles the case where every disagreement cannot fit.)
If the disagreement pool fits within the human budget, all disagreement items may enter.
If it exceeds capacity, the system samples across labels, seven regions, confidence bands, and novel patterns.
No one difficult region should consume the whole round.

#### 20.2 · Stratified random consensus audit
(Defines the protection against unanimous shared error.)
The system randomly samples consensus items within strata defined by predicted class, region, and optionally confidence.
Sampling occurs before human outcomes are known.
Selection probabilities are preserved so consensus error estimates can be weighted back to the candidate pool.

#### 20.3 · Configurable composition
(Keeps the batch aligned with the round's purpose.)
A guideline-refinement round may oversample disagreement and boundaries.
A reliability-estimation round may allocate more capacity to representative consensus audit.
The batch report states its composition so challenge performance is never mistaken for population performance.

### 21 · Guideline update and optimization
**The update mechanism**: human corrections and model reasoning failures become generalized policy changes.

```text
🏷 human gold + 🧾 human reason
          versus
🧠 weak prediction + 📋 applied rule
                │
                ▼
🤖 strong-agent diagnosis
├── unclear definition
├── missing boundary test
├── misleading example
├── executor formatting problem
└── weak-model capability limit
                │
                ▼
🧑 human accepts, rejects, or reframes patch
```

#### 21.1 · Error diagnosis before editing
(Prevents every model error from becoming another guideline sentence.)
The strong agent compares the human reason with the weak model's cited evidence and applied rule.
It classifies whether the error comes from guideline ambiguity, missing knowledge, model incapability, prompt formatting, or random execution.
Only errors that the guideline can legitimately prevent become core guideline patches.

#### 21.2 · Human-protected optimization
(Keeps model readability from changing the intended construct.)
The strong agent may rewrite a rule into simpler language, add an ordered test, or replace a misleading example.
The human confirms that the patch still expresses the intended subjective boundary.
The system optimizes executor compatibility subject to human semantic fidelity.

#### 21.3 · Core guideline versus execution wrapper
(Separates portable policy from model-specific instructions.)
The core guideline contains the stable concept and decision rules.
An execution wrapper may specify output JSON, reasoning fields, token limits, or model-specific formatting.
Improving the wrapper should not silently change the core concept.

### 22 · Generalizing from examples
**The knowledge extraction rule**: development cases motivate rules, while only selected anchors remain in the casebook.

```text
📄 concrete development case
        │
        ▼
🔍 decisive evidence + rejected alternative
        │
        ▼
🔁 counterfactual flip condition
        │
        ▼
📜 generalized boundary rule
        │
        └──▶ 📚 keep case only if it is canonical
```

#### 22.1 · Why raw copying is risky
(Explains how a guideline can memorize the development corpus.)
Copying many training reviews into the prompt lets a model match surface language without learning the intended boundary.
It increases context cost and makes the guideline difficult to inspect.
It may also leak evaluation-like cases into later execution.

#### 22.2 · Rule extraction
(Defines the transformation from one judgment to transferable knowledge.)
For each influential example, the agent records the decisive evidence, strongest rejected label, and smallest counterfactual change that would flip the decision.
Repeated patterns become a concise rule with scope and exceptions.
The rule is tested against earlier confirmed cases before checkpoint closure.

#### 22.3 · Canonical example selection
(Defines which cases deserve to remain attached to the policy.)
A case remains in the casebook when it uniquely demonstrates a typical pattern, a counterexample, or a difficult boundary.
Near-duplicate examples are removed.
Every retained case states why it is needed and which rule it illustrates.

### 23 · Round-level measurements
**Two score families**: audit metrics support quality claims, while challenge metrics support learning.

```text
🟢 AUDIT SLICE                 🔴 CHALLENGE SLICE
representative/weighted        selected for difficulty
comparable across rounds       intentionally changes each round
quality + stopping             discovery + refinement

L_t = 1 - agreement(P_t, Y*_t)
```

#### 23.1 · Correction loss
(Defines the pre-post difference that plays the role of optimization loss.)
Round correction loss is the disagreement between sealed pre-labels and final human labels.
It may be summarized with macro-F1, balanced accuracy, kappa, or a task-appropriate agreement measure.
Human correction rate provides a direct operational interpretation.

#### 23.2 · Audit loss
(Defines the comparable series used for stopping.)
Audit loss is measured on a random or weighted slice that represents a declared population.
The same sampling protocol is used across rounds.
Its improvement estimates whether the prior guideline transfers better to ordinary unseen items.

#### 23.3 · Challenge yield
(Defines the learning signal from adaptively selected hard cases.)
Challenge metrics are reported separately because each round deliberately seeks harder or novel cases.
The important quantities include new-rule yield, new-boundary yield, consensus-failure yield, and unresolved rate.
A falling challenge score may reflect a harder batch rather than a worse guideline.

#### 23.4 · Guideline change metrics
(Measures whether updates remain substantive.)
Each checkpoint counts substantive rule additions, deletions, boundary changes, example changes, and editorial-only changes.
It also records the performance difference between G_(t-1) and G_t on the current audit protocol.
These values make guideline stability observable rather than impressionistic.

### 24 · Stopping criteria
**The double gate**: the system stops calibration only when quality is sufficient and improvement has saturated.

```text
📊 QUALITY GATE                 📉 STABILITY GATE
audit score ≥ target            gain ≤ epsilon
correction ≤ target             few new semantic rules
coverage complete               low new-edge yield
unresolved risk acceptable      repeated for K rounds
             \                 /
              \               /
               ▼             ▼
                 🛑 stop calibration
```

#### 24.1 · Quality gate
(Prevents a low plateau from being called convergence.)
Audit performance must exceed a predefined quality floor.
Human correction and unresolved rates must be acceptably low.
Important classes and seven-region areas must meet minimum coverage and must not hide a systematic NONE error.

#### 24.2 · Stability gate
(Defines diminishing returns across consecutive rounds.)
Audit improvement must remain below epsilon for K consecutive rounds.
New edge cases must produce few substantive rules, and guideline edits must be mostly editorial.
One easy batch cannot close the process.

#### 24.3 · Coverage and risk gate
(Protects rare regions and known failure modes.)
All seven regions require a minimum evidence count or an explicit reason why the corpus does not contain that region.
Consensus-failure clusters and concept-revision impacts must be resolved.
The remaining risk queue must satisfy the project's acceptance policy.

#### 24.4 · Calibration stop versus corpus completion
(Separates ending concept learning from finishing all N labels.)
Calibration stops when the concept and policy are good enough and stable enough.
Corpus completion occurs later when every item has a final label or an explicitly accepted unresolved disposition.
Assigning a machine label to every row is not by itself evidence that the corpus is reliable.

### 25 · The sealed final test set
**Reserve early, label late**: test items are isolated before development and receive human gold only after the concept is stable.

```text
🗄 raw corpus
   ├──▶ 🔁 development pool
   │       B1 ... Bt · guideline updates · stop decisions
   │
   └──▶ 🔒 sealed T item ids
               │  never inspected during calibration
               ▼ after G* freeze
          🧑 blind human labeling
               ▼
          🧪 final gold Y*_T
```

#### 25.1 · Timing
(Combines an early holdout with a late, mature human concept.)
The safest design reserves test item identifiers at project initialization.
Their text is not inspected, retrieved, pre-labeled, or used in any stopping decision.
After calibration terminates and G* is frozen, the human labels them using the mature concept.

#### 25.2 · Blind gold construction
(Protects final human labels from executor predictions.)
The human labels test items without seeing any candidate weak-model output.
The final guideline may be available because it is the external form of the human's finalized concept.
Ambiguous test items may receive a second human pass or adjudication, but model outputs remain sealed until gold is locked.

#### 25.3 · Representative and diagnostic tests
(Separates population claims from boundary diagnosis.)
A representative random test estimates expected performance on the target corpus distribution.
An optional region-stratified diagnostic test ensures that all boundaries receive enough examples for analysis.
Diagnostic oversampling must not be folded into an unweighted population accuracy claim.

#### 25.4 · Test invalidation rule
(Preserves the meaning of a final score.)
If test results are used to revise the guideline, prompt wrapper, thresholds, or executor choice, that test has become validation data.
A new sealed test is required for a new final claim.

### 26 · Final guideline and model evaluation
**The executor exam**: every candidate model applies the same frozen policy to the same unseen human-gold items.

```text
📜 G* + 🧪 T*
       │
       ├──▶ 🧠 LM A ──▶ 📊 Score_A
       ├──▶ 🧠 LM B ──▶ 📊 Score_B
       └──▶ 🧠 LM C ──▶ 📊 Score_C

comparison ruler = 🧑 Y*_T
```

#### 26.1 · Absolute execution score
(Defines the main per-model result.)
Each model's test predictions are compared with human gold using macro-F1, balanced accuracy, per-class precision and recall, confusion matrix, and an agreement statistic.
The report includes class prevalence and uncertainty intervals.
Region-level metrics show where a model fails even when overall accuracy is high.

#### 26.2 · Guideline uplift
(Separates guideline value from raw model capability.)
Each model is also tested under a minimal trait instruction or another predefined baseline.
Guideline uplift is the frozen-guideline score minus the baseline score for the same model.
This difference estimates how much the learned policy contributes beyond the executor's prior knowledge.

#### 26.3 · Seen and held-out executors
(Protects against optimizing the guideline for one model family.)
Models used repeatedly during calibration are seen executors.
At least one model or model family that did not participate in guideline optimization should be held out for final transfer evaluation.
A guideline that works only for the optimization committee is not model-portable.

#### 26.4 · Repeated execution
(Measures stochastic instability when it matters.)
If an executor is stochastic, the evaluation may repeat predictions under a frozen run policy.
The scorecard reports variation across runs and the rate of label flips.
Deterministic settings remain preferable when they are supported and do not reduce task quality.

### 27 · Completing the large N corpus
**The production pass**: final evaluation selects an executor policy, then risk routing completes the remaining items.

```text
📊 final scorecard
        │
        ▼
🧠 choose executor or ensemble
        │
        ▼
🏭 apply G* to remaining corpus
        │
        ├──▶ 🟢 accepted machine labels
        └──▶ 🚨 disagreement / low confidence / novelty
                         │
                         ▼
                    🧑 human review
        │
        ▼
🎲 final random corpus audit → 📦 D*
```

#### 27.1 · Executor selection
(Defines how the scorecard informs production without changing the test claim.)
The production executor may be one model, a committee, or a cost-aware routing policy.
Selection considers test quality, class-specific risk, runtime, cost, and stability.
The selection rule is recorded before the production corpus is labeled.

#### 27.2 · Risk routing
(Defines which machine predictions cannot pass automatically.)
Model disagreement, low confidence, unsupported evidence, novelty, and known consensus-failure neighborhoods enter a human queue.
Thresholds are chosen from validation and audit evidence rather than arbitrary defaults.
The system never converts procedural uncertainty into NONE.

#### 27.3 · Final corpus audit
(Supports the claim that production labels remain reliable.)
A random or stratified probability sample from the completed corpus is labeled blind by the human.
Audit estimates are weighted to the production distribution.
If error exceeds the acceptance threshold, the affected stratum returns to review or the production policy is revised.

### 28 · Reliability claims and provenance
**Three levels of evidence**: human gold, audited-machine labels, and validated machine-accepted labels support different claims.

```text
🥇 human-confirmed gold
      strongest item-level evidence

🥈 audited machine label
      accepted through tested policy + population audit

🥉 validated machine-accepted label
      exact tested route passed its frozen acceptance rule

🚨 unresolved
      no final quality claim
```

#### 28.1 · Dataset reliability
(Defines the evidence required before calling the full corpus reliable.)
The human-confirmed subset is reliable relative to the identified human authority, subject to that person's own consistency.
The machine-labeled remainder is supported by sealed-test performance, risk review, and final corpus audit.
The final report states the share of items in each provenance tier.

#### 28.2 · Human consistency
(Recognizes that the semantic authority can also vary over time.)
After concept stabilization, the human may re-label a random subset of earlier items without seeing prior answers.
Test-retest agreement estimates intra-rater consistency.
Low consistency signals that the concept or decision procedure is not yet stable enough for a strong corpus claim.

#### 28.3 · Guideline quality
(Defines guideline quality as transfer rather than literary polish.)
Guideline quality is the ability of humans and models to reproduce the final human concept on unseen items.
It includes executor accuracy, guideline uplift, model-family transfer, boundary performance, and low ambiguity.
A clear-looking document with poor transfer is not high quality.

### 29 · Failure modes and guardrails
**The main threats**: the system records each failure where it can be detected and corrected.

```text
⚠️ selection bias        → 🟢 representative audit
⚠️ unanimous model error → 🎲 consensus audit
⚠️ concept drift         → 🔁 backward impact review
⚠️ example memorization  → 📜 abstract rules + sealed test
⚠️ model-family overfit  → 🧠 held-out executor
⚠️ test leakage          → 🔒 invalidate and replace test
⚠️ NONE misuse           → 🌡 separate uncertainty field
```

#### 29.1 · Adaptive-batch bias
(Explains why challenge scores cannot estimate corpus-wide quality.)
Later batches are selected because they are difficult, novel, or inconsistent.
Their error rate is expected to exceed the corpus average.
Representative audit samples and known selection probabilities are required for population claims.

#### 29.2 · Shared model blind spots
(Explains why unanimity needs ongoing human checks.)
Models may share training data, architecture families, prompt interpretations, and cultural assumptions.
One consensus failure triggers a local search for similar items and an expanded audit of the affected stratum.
Repeated consensus failures lower the amount of automatic acceptance allowed.

#### 29.3 · Guideline overfitting
(Explains how repeated patching can harm transfer.)
A rule written to fix one review may encode irrelevant wording or source-specific detail.
Every substantive patch should state its scope, counterexample, and regression impact.
The sealed test and held-out executor are the final defenses against development overfitting.

#### 29.4 · Uncomparable round loss
(Explains why the deep-learning analogy needs a validation discipline.)
Each round resembles an optimization step, but the selected data distribution changes.
Raw challenge loss cannot be read like training loss from identical independent batches.
Audit loss supplies the comparable validation series, while challenge yield supplies the active-learning signal.

### 30 · Open settings and migration map
**The remaining work**: the conception is fixed at method level, while numeric settings and older artifacts still need explicit reconciliation.

```text
✅ SETTLED METHOD
  authority · artifacts · round loop · B2 funnel · stop logic · final test

🧠 OPEN SETTINGS
  batch sizes · quotas · thresholds · K · test size · LM panel · risk budget

🔧 MIGRATION TARGETS
  QA1 QA2 QA3 · QB1 QB2 QB3 · QC1 QC2 QC3 · QD1 QD2 QD3 QD4
  subjective-label SKILL.md · architecture · stages · schema · contract
```

#### 30.1 · Numeric settings still to choose
(Lists the parameters that require empirical or budget-based decisions.)
Open settings include Round 1 size, candidate-pool size, human-batch size, seven-region quotas, consensus-audit fraction, and novelty allocation.
They also include quality floors, epsilon, K consecutive stable rounds, unresolved-risk thresholds, final test size, and confidence intervals.
These settings must be recorded in configuration after pilot evidence exists.

#### 30.2 · Model settings still to choose
(Lists executor choices without turning them into conceptual dependencies.)
The project still needs an embedding model, initial region scorer, strong labeling agent, weak pre-label committee, held-out executor, and production executor policy.
The initial region scorer may be prototype-based or linear, with an MLP considered after more human-confirmed data exists.
Model identities and versions must be frozen for every reported comparison.

#### 30.3 · Page reconciliation result
(Records how the largest contradictions were resolved by the six-group migration.)
QA now fixes the human-grounded system, label-region-uncertainty separation, and structured policy.
QB now defines random Round 1, the blind Human-AI Session, and Checkpoint closure.
QC now separates broad candidate pool C_t, sealed pre-labeling, mixed human Batch composition, and blind adjudication.
QD now separates policy optimization, audit versus challenge metrics, coverage, concept stability, and conjunctive stopping.
QE now owns the sealed final test, executor scorecards, validated corpus completion, final audit, and provenance.
QF now owns command skills, artifacts, agent topology, deferred library mapping, and acceptance tests.

#### 30.4 · Skill and reference reconciliation result
(Records the migrated command and reference layer.)
The router now exposes init, round, evaluate, complete, and status under one-human semantic authority.
Iterate, validate, and scale remain thin compatibility aliases rather than active legacy procedures.
The architecture and agent prompts now keep the human in every calibration batch, seal weak evidence, and reserve canonical writes for the checkpoint keeper.
The lifecycle, schema, metric, embedding, production, dataset, configuration, artifact, and output references now carry the seven-region, sealed-test, provenance, and HOLD contracts.
The current libraries are deliberately unchanged and remain mapped as implementation work in QF4.

#### 30.5 · Acceptance of this governing page
(Defines the immediate human gate before migration begins.)
JL confirmed that QA0 captures the discussion closely enough to govern the next edition on 260806.
That acceptance did not choose the remaining numeric settings.
The approved six-group migration now revises each page and skill contract against this source rather than against a disappearing chat transcript.

## Aims

### A1 · 🧭 The revised conception
- A1.1 · The system has one complete, human-grounded conception that a zero-background reader can restate.
  **Done when:** Sections 1 through 9 distinguish the human concept, annotation policy, labels, regions, authority, and outputs without relying on the discussion transcript.

### A11 · 🧾 Versioned round artifacts
- A11.1 · Every round object and guideline state has one stable name and lifecycle.
  **Done when:** A reader can distinguish C_t, B_t, P_t, Y*_t, D_t, G_(t-1) closed, G_t draft, and G_t closed.

### A13 · 🎲 Round 1 cold start
- A13.1 · Round 1 begins without circular labels, regions, prototypes, or guideline assumptions.
  **Done when:** The page states how a random batch produces human labels, seven regions, reasons, chat history, and G_1.

### A16 · 🔎 Candidate generation after Round 1
- A16.1 · Later-round candidate generation and the final human batch are separate and auditable.
  **Done when:** The page defines region scoring, broad candidate pools, independent pre-labeling, disagreement, mismatch, and consensus audit.

### A21 · 📜 Guideline update and optimization
- A21.1 · Guideline optimization improves model execution without transferring semantic authority away from the human.
  **Done when:** The page separates error diagnosis, human-approved core rules, model-specific wrappers, and generalized case extraction.

### A23 · 📊 Round-level measurements
- A23.1 · Development measurements support both learning and comparable stopping decisions.
  **Done when:** Audit loss, challenge yield, correction loss, and guideline change metrics are defined and not merged.

### A24 · 🛑 Stopping criteria
- A24.1 · Calibration stops only through quality, stability, coverage, and risk gates.
  **Done when:** A low plateau cannot pass and calibration stop remains distinct from corpus completion.

### A25 · 🔒 The sealed final test set
- A25.1 · The final evaluation remains independent of guideline development and stopping.
  **Done when:** Test items are reserved unseen, labeled by the mature human concept after G* freezes, and invalidated if reused for optimization.

### A27 · 🏭 Completing the large N corpus
- A27.1 · The final production pass creates a complete corpus with explicit provenance and audit support.
  **Done when:** Executor selection, risk routing, human review, final audit, and provenance tiers are specified.

### A30 · 🔧 Open settings and migration map
- A30.1 · Every known open setting and previous-edition contradiction has an explicit landing place.
  **Done when:** Section 30 names the unresolved parameters and the required QA, QB, QC, QD, skill, and reference migrations.

### P · Page-level
- P1 · JL accepts this page as the governing conception for the next subjective-label edition.
  **Done when:** JL confirms that the page captures the discussion closely enough for reconciliation work to begin.

## States

### A1 · 🧭 The revised conception
- ✅ A1.1 · Met; Sections 1 through 9 define the human-grounded system, outputs, labels, regions, authority, dual adaptation, and annotation policy.

### A11 · 🧾 Versioned round artifacts
- ✅ A11.1 · Met; Sections 11 and 12 define every round object, guideline state, Session, Round, and Checkpoint.

### A13 · 🎲 Round 1 cold start
- ✅ A13.1 · Met; Sections 13 through 15 define random cold start, blind Human-AI interaction, and checkpoint closure.

### A16 · 🔎 Candidate generation after Round 1
- ✅ A16.1 · Met; Sections 16 through 20 define the candidate funnel, scorer, committee, pools, consensus audit, and human Batch composition.

### A21 · 📜 Guideline update and optimization
- ✅ A21.1 · Met; Sections 21 and 22 define error diagnosis, human-protected updates, execution wrappers, rule extraction, and casebook selection.

### A23 · 📊 Round-level measurements
- ✅ A23.1 · Met; Section 23 separates representative audit measurements from adaptive challenge measurements.

### A24 · 🛑 Stopping criteria
- ✅ A24.1 · Met; Section 24 defines the double gate and separates calibration stop from completion.

### A25 · 🔒 The sealed final test set
- ✅ A25.1 · Met; Sections 25 and 26 define reserve-early label-late testing, held-out executors, uplift, and invalidation.

### A27 · 🏭 Completing the large N corpus
- ✅ A27.1 · Met; Sections 27 through 29 define production, risk routing, final audit, provenance, reliability, and guardrails.

### A30 · 🔧 Open settings and migration map
- ✅ A30.1 · Met; Section 30 records numeric, model, page, skill, and reference migrations.

### P · Page-level
- ✅ P1 · Met; JL approved the six-group execution plan grounded in QA0 and instructed CC to run it on 260806.

## Files

### Contracts · what this edition revised
- `../../skills/subjective-label/SKILL.md`
  The router now dispatches the human-grounded lifecycle and explicit compatibility aliases.
- `../../ref/ref-architecture.md`
  The topology now defines one-human authority, blind pre-labeling, consensus audit, checkpoints, and final testing.
- `../../ref/ref-stages.md`
  The lifecycle now defines Round, Session, Checkpoint, stopping, evaluation, and production states.
- `../../ref/ref-schema.md`
  H/L/N, seven-region, uncertainty, event, test, and provenance records are separate.
- `../../ref/ref-contract.md`
  Metric contexts now separate audit from challenge and define sealed gold, held-out executors, and guideline uplift.

## Law
- 260806 JL · 🧑 One human is the semantic authority
      Models may retrieve, pre-label, diagnose, and draft, but human confirmation creates gold and protects the construct's meaning.
- 260806 JL · 🎲 Round 1 begins with a random small batch
      The first 50 to 60 items have no prior labels or regions, and the first labels, seven-region assignments, reasons, and guideline draft emerge together through dialogue.
- 260806 JL · 🗺 Class and region are separate annotations
      Every reviewed item receives H, L, or N plus one of seven diagnostic regions, while uncertainty remains a third field.
- 260806 JL · 🔎 Later rounds use a broad candidate pool before a human batch
      Region-conditioned retrieval creates C_t, committee pre-labeling partitions it, and only the composed B_t enters Human-AI review.
- 260806 JL · 🎲 Consensus is audited rather than trusted as gold
      Disagreement receives priority, while a stratified random sample of unanimous predictions still enters human review.
- 260806 JL · 🙈 Pre-labels remain sealed during first-pass human judgment
      The pre-post comparison is meaningful only when committee predictions do not anchor the human label.
- 260806 JL · 📜 The learned object is a structured annotation policy
      The core guideline, boundary rules, decision procedure, uncertainty policy, and compact casebook are optimized together.
- 260806 JL · 🧠 Human concept and guideline co-adapt
      Clarification is allowed, concept revision triggers backward review, and model convenience cannot override human meaning.
- 260806 JL · 🛑 Plateau requires a quality floor
      Calibration stops only when quality, stability, coverage, and risk gates hold across consecutive rounds.
- 260806 JL · 🔒 Final evaluation uses a sealed unseen test
      Test items remain outside development, receive human gold after G* freezes, and score each candidate executor under one protocol.
- 260806 JL · 📊 Guideline quality is measured by transfer
      Absolute model performance, guideline uplift, held-out model transfer, region errors, and human consistency support the final claim.

## Lesson
- ⚠️ Model agreement is evidence, not authority
      Multiple models can share one blind spot, so consensus requires probability-based human audit.
- ⚠️ Adaptive challenge batches do not form a comparable loss series
      Audit slices support stopping and population claims, while challenge slices support discovery.
- ⚠️ A stable guideline may still be bad
      Diminishing improvement becomes a stop signal only after the quality floor and coverage requirements pass.
- ⚠️ Examples can teach or leak
      Development cases should produce generalized rules, and only canonical examples belong in the casebook.
- ⚠️ Human concept change can invalidate earlier gold
      A semantic revision requires impact analysis and selective relabeling rather than a silent guideline edit.

## Glossary
- 🧑 **Semantic authority**: the identified human whose final subjective judgment defines correctness for this project.
- 🔁 **Calibration Round**: one complete cycle from a prior closed state through candidate selection, pre-labeling, Human-AI review, and checkpoint closure.
- 💬 **Human-AI Session**: one continuous conversation inside a Calibration Round.
- 📌 **Checkpoint**: the event that locks human labels, cumulative gold, metrics, and a closed guideline version.
- 📦 **Candidate pool C_t**: the broad set ranked and pre-labeled before the human review batch is composed.
- 💬 **Human batch B_t**: the smaller set that actually enters Human-AI review.
- 🧠 **Pre-labels P_t**: sealed predictions and structured reasons produced by weak executors under the previous closed guideline.
- 🏷 **Human gold Y*_t**: final human-confirmed labels for the current review batch.
- 🗄 **Cumulative gold D_t**: all human-confirmed items through Round t, versioned with the policy state.
- 🧊 **Frozen calibration gold D_cal***: the final D_t at calibration stopping; it remains smaller than the corpus unless every item was human-reviewed.
- 📦 **Completed corpus D***: one terminal class or accepted non-label disposition plus provenance for every in-scope item after production and final audit.
- 📜 **Annotation policy Θ_t**: the core guideline, boundary rules, casebook, decision procedure, and uncertainty policy at Round t.
- 🟢 **Consensus audit**: a stratified random human review sample drawn from items on which the weak executors agree.
- 🔴 **Challenge slice**: disagreement, boundary, mismatch, and novelty cases selected to refine the policy.
- 🧪 **Sealed test T***: unseen items excluded from development and labeled by the human only after the final policy freezes.
- 📊 **Guideline uplift**: the performance gain from the final guideline over a predefined minimal instruction for the same executor.

## Log
260806 · Completed the Board, reference, command-skill, and agent-contract reconciliation; QF4 implementation remains deliberately deferred.
260806 · JL accepted the QA0-governed six-group migration plan and instructed CC to execute it; QA0 is now SETTLED while numeric settings remain configuration.
260806 · Created QA0 from the detailed Human-AI conception discussion and registered it as the governing page before the previous-edition QA pages.
