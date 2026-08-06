# Artifact contract: make every round, test, and label reconstructable
state: ✅ SETTLED · v2 reference contracts migrated
owner: CC
method: Define immutable project, round, policy, test, evaluation, production, audit, and provenance records before engine implementation.

## Opening
Which files and fields must exist so another agent can resume the workflow and an auditor can reconstruct every final label?
The old gallery-centered layout cannot represent the revised round or its final test.
Selection evidence, human gold, and production provenance need separate records.
The revised layout must also distinguish configuration from runtime state and immutable records from human-readable views.
This page fixes the artifact tree, identities, ownership, writes, and migration.

**Where this page sits**: QB3 defines checkpoint contents, QE4 defines the final reliability package, and QF1 tells skills which artifacts they may produce.

**Why it matters**: Without stable ids and checksums, a later score cannot prove which corpus, guideline, model, or human decision it measured.

## Writing Style
**Language and sentences**: Name path, owner, mutability, schema version, and parent identity for every artifact family.

**Separation**: Keep config, runtime state, immutable event records, caches, and rendered views distinct.

**Migration**: Never promote old panel consensus to human gold during schema conversion.

## Diagram
**Artifact tree**: project-level contracts contain immutable round, evaluation, and production packages.

```text
project/
├── config.yaml + state.json
├── corpus/ + cache/embeddings/
├── policy/versions/
├── rounds/round-N/
├── gold/cumulative.jsonl
├── test/sealed/ + test/final/
├── evaluation/scorecards/
├── production/
└── audit/ + REPORT.md
```

## Content

### 1 · Project and policy records
**Stable identity**: one project manifest joins corpus, trait seed, human authority, schemas, models, and configuration.

```text
🧾 project manifest
├── project + schema version
├── corpus checksum + fields
├── human authority id
├── label + region schema
├── model registry
└── test custodian + access policy
```

#### 1.1 · Configuration
`config.yaml` stores tunable sampling, model, threshold, budget, and metric choices.
Runtime status, observed scores, and current phase do not belong in configuration.

#### 1.2 · Annotation policy
Every G_t version includes core guideline, boundary rules, decision procedure, uncertainty policy, compact casebook, wrappers, checksum, parent, and typed diff.
Closed versions are immutable.

### 2 · Round package
**Checkpoint source**: one round folder contains every input and output needed to reproduce its close.

```text
rounds/round-N/
├── candidate-pool.jsonl
├── prelabels/<executor>.jsonl
├── human-batch.jsonl
├── sessions/
├── human-final.jsonl
├── policy-draft/
├── metrics.json
└── checkpoint.json
```

#### 2.1 · Selection and prelabels
Candidate and batch manifests preserve source pools, scores, strata, probabilities, seeds, policy identity, and access state.
Pre-label records preserve executor, wrapper, run, prediction, uncertainty, reason, and seal checksum.

#### 2.2 · Human records
Session artifacts preserve chat, item order, first-pass human record, reveal time, revisions, final record, change type, and backward-impact flags.
`gold/cumulative.jsonl` contains only human-confirmed records and links each row to its checkpoint.

#### 2.3 · Checkpoint
The checkpoint names all checksums, dispositions, metrics, policy diff, risk changes, and next state.
It is the only event that closes G_t and makes it available to the next round.

### 3 · Test, evaluation, and production
**Final packages**: sealed access, scorecards, execution attempts, and corpus audits remain independently inspectable.

```text
test/sealed/manifest
test/final/human-gold
evaluation/scorecards/<executor>
production/run-manifest + labels + risk-queue
audit/final-sample + findings + repairs
```

#### 3.1 · Test separation
The sealed manifest exists from initialization, while final human labels appear only after G* freezes.
Access logs and invalidation status live beside the manifest.

#### 3.2 · Production attempts
Production stores every attempt and one reconciled terminal record per item.
Final labels include provenance tier, policy, executor, wrapper, route, confidence, human authority when applicable, and audit linkage.

### 4 · Writes, views, and migration
**Authority map**: only designated keepers write canonical records, while rendered Markdown mirrors remain replaceable views.

```text
📌 checkpoint keeper  rounds + gold + policy close
🔒 test custodian     sealed manifest + access log
📊 evaluator          frozen predictions + scorecards
🏭 production keeper  attempts + terminal labels
🎲 audit keeper       audit + repairs + final report
```

#### 4.1 · Rendered views
REPORT, trajectories, galleries, policy cheatsheets, scorecards, and audit summaries are generated from canonical records.
They never become an alternate source of truth.

#### 4.2 · Old-project migration
Migration classifies old gallery entries as human-confirmed, model-only, or unknown provenance.
Only inspectable human decisions enter cumulative gold; all other rows remain evidence with their original status.

## Aims

### A1 · 🧾 Project and policy records
- A1.1 · Project, corpus, authority, configuration, and policy identities are immutable and linked.
  **Done when:** References define fields, mutability, parent ids, and checksums.

### A2 · 📌 Round package
- A2.1 · Every Calibration Round can be reconstructed from candidate selection through checkpoint.
  **Done when:** All C_t, P_t, B_t, Session, Y*_t, metric, diff, and close records validate.

### A3 · 🧪 Test, evaluation, and production
- A3.1 · Final testing and production remain separate from development and from each other.
  **Done when:** Access, predictions, scorecards, attempts, terminal labels, and audits have distinct schemas.

### A4 · 🔐 Writes, views, and migration
- A4.1 · Canonical write authority and safe old-project conversion are explicit.
  **Done when:** Human gold cannot be created by rendering, migration, or model consensus.

## States

### A1 · 🧾 Project and policy records
- ✅ A1.1 · Configuration, schema, artifact, policy, parent, and checksum contracts are explicit in v2 references.

### A2 · 📌 Round package
- ✅ A2.1 · C_t, P_t, B_t, Session, Y*_t, metric, risk, diff, and checkpoint records are defined and linked.

### A3 · 🧪 Test, evaluation, and production
- ✅ A3.1 · Sealed test, scorecard, production-attempt, terminal-label, and final-audit families have distinct schemas.

### A4 · 🔐 Writes, views, and migration
- ✅ A4.1 · Reference and agent contracts enforce single writers, human-only gold promotion, and provenance-safe migration.

## Files

### Contracts · what this Page changes
- `../../ref/ref-config.md`
  Defines tunable inputs and model choices.
- `../../ref/ref-schema.md`
  Defines item, region, uncertainty, human-first, final, and provenance records.
- `../../ref/ref-assets.md`
  Defines the complete artifact tree and write ownership.
- `../../ref/ref-contract.md`
  Defines metric populations and final claim contexts.

### 🔗 Related Board Pages · what this Page READS BY SCOPE
- `reads · ALL` · [QB3 page](QB-calibration-round/QB3-checkpoint-and-versions.md)
  QB3 supplies the round close package.
- `reads · ALL` · [QE4 §4](QE-final-evaluation-and-completion/QE4-final-audit-and-provenance.md)
  QE4 supplies the final reliability package.

## Law
- 260806 JL · 🧾 Every canonical artifact has one owner, version, checksum, parent, and provenance status
      Rendered views are replaceable, closed records are immutable, and migration cannot infer human gold from model agreement.

## Glossary
- 🧾 **Canonical record**: the machine-readable source of truth from which human views are rendered.
- 🔐 **Write authority**: the one agent or event allowed to create or close a canonical artifact family.
- 🔗 **Parent identity**: the versioned upstream artifact that a record consumes and cites by checksum.

## Log
260806 · Created QF2 to govern schema, configuration, artifacts, views, and migration before code changes.
260806 · Replaced the reference layer with v2 config, schema, lifecycle, artifact, metric, retrieval, evaluation, and production contracts.
