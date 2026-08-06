# Agent topology: preserve human authority and single-writer artifacts
state: ✅ SETTLED · agent authority and access contracts migrated
owner: CC
method: Assign one human-facing calibrator, narrow technical agents, independent weak executors, and one canonical writer for each artifact family.

## Opening
Which agents run the revised workflow, and what must remain outside each agent's authority?
The old topology treated persona-panel consensus as an adjudicator and allowed the human to see only selected disagreements.
The revised system keeps the human in every calibration batch and uses weak models only as sealed executors.
Proposal, semantic ruling, canonical writing, and evaluation stay separate.
This page fixes roles, calls, writes, blind access, and failure escalation.

**Where this page sits**: QF1 defines commands, QF2 defines artifacts, and every agent file must implement the authority declared here.

**Why it matters**: A correct sequence can still fail if the same agent predicts, reveals, adjudicates, rewrites gold, and approves its own checkpoint.

## Writing Style
**Language and sentences**: State what each role reads, writes, proposes, decides, and must not access.

**Authority**: Use human semantic authority, strong calibration agent, weak executor, and keeper consistently.

**Independence**: Separate builders, semantic deciders, and evaluators where their incentives or evidence differ.

## Diagram
**Revised topology**: the human works through one calibrator while narrow agents operate behind explicit access and write boundaries.

```text
🧑 human semantic authority
          ↕
🤖 strong calibration agent
  ├── 🧠 embedder
  ├── 🔎 candidate selector
  ├── 🧪 weak executors
  ├── ⚖️ comparison auditor
  ├── 📜 guideline optimizer
  ├── 📌 checkpoint keeper
  ├── 📊 final evaluator
  └── 🏭 production + audit keepers
```

## Content

### 1 · Human-facing authority
**One conversation door**: the strong calibration agent organizes interaction but cannot make the human's semantic decisions.

```text
🧑 decides class · region · meaning · signoff
🤖 asks · contrasts · drafts · records · warns
```

#### 1.1 · Human semantic authority
JL confirms final class and region for reviewed items, accepts substantive policy rules, classifies concept revision, signs stopping, and accepts bounded risk.
These decisions require durable human evidence.

#### 1.2 · Strong calibration agent
The calibrator presents item text, elicits reasons, protects the blind period, proposes general rules, tracks concept impacts, and routes checkpoint work.
It may not disclose P_t before the first-pass lock or auto-confirm a semantic ruling.

### 2 · Selection and execution agents
**Narrow services**: retrieval, scoring, and weak-model execution produce evidence without writing gold.

```text
🧠 embedder          vectors + neighborhoods
🔎 candidate selector C_t + B_t manifest proposal
🧪 weak executors    sealed P_t
⚖️ comparison auditor signatures + error taxonomy
```

#### 2.1 · Embedder and candidate selector
The embedder owns deterministic vectors, indexes, clusters, and distances.
The selector combines region scores, diversity, novelty, quotas, and random audit sampling into manifests.

#### 2.2 · Weak executors
Each weak executor applies one closed policy independently and writes only its own pre-label or final prediction record.
Executor consensus never writes human gold.

#### 2.3 · Comparison auditor
The auditor compares sealed predictions with human records, identifies disagreement and shared-error strata, and proposes error categories.
It does not decide the final class or policy patch.

### 3 · Policy and checkpoint writers
**Single-writer rule**: one keeper closes gold and policy versions only from inspectable human and agent evidence.

```text
📜 optimizer  proposes policy diff
🧑 human      accepts semantic changes
📌 keeper     validates package + closes checkpoint
```

#### 3.1 · Guideline optimizer
The optimizer drafts smallest general patches, wrapper changes, regression sets, and backward-impact candidates.
It cannot accept its own semantic patch.

#### 3.2 · Checkpoint keeper
The keeper is the sole writer of closed round state, cumulative human gold, and closed policy versions.
It verifies human evidence, seals, manifests, metrics, diffs, and unresolved ownership before close.

### 4 · Final and production agents
**Post-freeze separation**: evaluation remains read-only over G* and T*, while production writes attempts under a chosen policy.

```text
🔒 test custodian  access seal + human-gold release
📊 evaluator       predictions + scorecards
🏭 production      attempts + risk queue
🎲 audit keeper    final sample + repair status
```

#### 4.1 · Final evaluator
The evaluator cannot modify G*, T*, wrappers, candidates, or selection rules.
It writes frozen predictions and scorecards from registered inputs.

#### 4.2 · Production and audit
The production agent writes attempts and routes risk but cannot waive thresholds.
The audit keeper samples independently, records human findings, and reopens affected scope when acceptance fails.

## Aims

### A1 · 🧑 Human-facing authority
- A1.1 · Human decisions and strong-agent assistance remain asymmetric and traceable.
  **Done when:** Moderator or calibrator instructions enforce all human gates and blind access.

### A2 · 🔎 Selection and execution agents
- A2.1 · Retrieval, ranking, pre-labeling, and comparison produce evidence but never gold.
  **Done when:** Every technical agent's write and access boundaries match this page.

### A3 · 📌 Policy and checkpoint writers
- A3.1 · Accepted semantic evidence reaches canonical gold and policy through one keeper.
  **Done when:** Optimizer proposal, human acceptance, and checkpoint writing are separate.

### A4 · 📊 Final and production agents
- A4.1 · Final evaluation, production, and audit cannot approve their own changed systems.
  **Done when:** Post-freeze agent contracts enforce read-only evaluation and independent audit.

## States

### A1 · 🧑 Human-facing authority
- ✅ A1.1 · Moderator is now the Strong Calibration Agent and enforces human-first events, blinding, and semantic acceptance.

### A2 · 🔎 Selection and execution agents
- ✅ A2.1 · Selector, weak committee, auditor, classifier, embedder, and optional prober produce evidence without gold authority.

### A3 · 📌 Policy and checkpoint writers
- ✅ A3.1 · Gallery Keeper is now the Checkpoint Keeper and promotes only inspectable human-confirmed records.

### A4 · 📊 Final and production agents
- ✅ A4.1 · Validator is the sealed Final Evaluator; production and audit authority boundaries are fixed by the agent, reference, and completion-skill contracts.

## Files

### Contracts · what this Page changes
- `../../ref/ref-architecture.md`
  The shared topology, call graph, access, and write authority contract.
- `../../agents/moderator-agent.md`
  The human-facing calibration agent.
- `../../agents/sampler-agent.md`
  Candidate and audit selection.
- `../../agents/labeler-panel-agent.md`
  The weak-executor committee rather than semantic panel authority.
- `../../agents/disagreement-analyzer-agent.md`
  Comparison, consensus audit, and error diagnosis.
- `../../agents/gallery-keeper-agent.md`
  Checkpoint and cumulative-gold single writer.
- `../../agents/validator-agent.md`
  Sealed final evaluator.

## Law
- 260806 JL · 🔐 Human decision, model evidence, policy proposal, canonical write, and evaluation are separate authorities
      No agent may turn its own prediction or proposal into human gold or approve a changed system on the same final test.

## Glossary
- 🤖 **Strong calibration agent**: the only human-facing agent that elicits, drafts, records, and routes without semantic authority.
- 🧪 **Weak executor**: a candidate language model that applies a closed policy independently and produces sealed evidence.
- 📌 **Checkpoint keeper**: the sole canonical writer of closed round state, human gold, and policy versions.

## Log
260806 · Created QF3 to govern the agent topology and write-authority migration.
260806 · Migrated all nine agent prompts to human-grounded evidence, access, single-writer, evaluation, and HOLD boundaries.
