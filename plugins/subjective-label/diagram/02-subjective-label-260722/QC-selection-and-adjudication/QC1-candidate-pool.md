# Candidate generation: find broad evidence before choosing the human batch
state: ✅ SETTLED
owner: JL
method: Use seven-region retrieval, lightweight ranking, novelty, and explicit quotas to form C_t without assigning gold.

## Opening
How should a later Calibration Round search the remaining corpus before deciding which items deserve human attention?
The candidate pool C_t is a broad retrieval product, not the smaller human batch B_t and not a labeled dataset.
Its job is to cover seven known regions while still exposing language that the current policy has never handled.
This page fixes the ranking evidence, exclusions, diversity controls, and authority boundary that make C_t auditable.

**Where this page sits**: QB3 supplies the prior closed policy and cumulative gold; QC2 applies that policy to the pool; QC3 later composes the human batch.

**Why it matters**: A narrow uncertainty list can repeatedly mine one familiar boundary, while geometric label inheritance can turn a retrieval shortcut into false gold.

## Writing Style
**Language and sentences**: Use plain English, one sentence per source line, and keep class, region, and retrieval score names distinct.

**Authority**: Describe rankers as candidate selectors only; human confirmation remains the source of gold.

**Settings**: Treat pool size, quotas, and scorer thresholds as versioned configuration rather than universal constants.

## Diagram
**Candidate funnel**: several retrieval signals produce one broad pool, which remains unlabeled until later stages.

```text
🗄 remaining corpus
        │
        ├──▶ 🗺 seven-region similarity
        ├──▶ 📏 class and region margins
        ├──▶ 🌱 novelty and sparse coverage
        └──▶ 🎲 random coverage reserve
                    │
                    ▼
              📦 candidate pool C_t
                    │
                    ▼
              QC2 sealed pre-labeling
```

## Content

### 1 · Eligible corpus
**Eligibility**: candidate generation begins from one frozen remainder with explicit exclusions.

```text
🗄 corpus snapshot
├── 🚫 sealed-test ids
├── 🚫 already closed items
├── 🚫 duplicate ids
└── ✅ eligible remainder U_t
```

#### 1.1 · Frozen input
The selector reads the corpus snapshot, D_(t-1), G_(t-1), current region anchors, and the round configuration.
An item is eligible only when its identifier is outside the sealed test and it has no closed human disposition for the current policy version.

#### 1.2 · No semantic filtering before retrieval
Metadata filters may enforce population scope, language, minimum text quality, or duplicate removal.
They may not remove a case merely because a model thinks it is NONE or easy.

### 2 · Seven-region retrieval
**Region search**: three centers, three pairwise boundaries, and one triple junction each receive an explicit search route.

```text
🟢 centers     H · L · N
🟡 boundaries  HL · LN · HN
🔴 junction    HLN
🌱 reserve     novel · sparse · random
```

#### 2.1 · Center candidates
Center candidates rank high when they resemble confirmed examples for one class and have a clear margin over alternatives.
They support prevalence checks, simple-rule verification, and production auditing.

#### 2.2 · Boundary and junction candidates
Pairwise candidates have similar scores for two labels and weaker support for the third.
HLN candidates have small margins across all three labels or incompatible evidence patterns.

#### 2.3 · Region coverage is provisional
The selector predicts where an item may be informative.
Its region name is a retrieval hypothesis and never overwrites the later human region judgment.

### 3 · Ranking models
**Scorer role**: the smallest defensible ranker is preferred while human-confirmed data remain sparse.

```text
🧠 embeddings
   │
   ├──▶ 📍 prototype similarity
   ├──▶ 📐 linear margin
   ├──▶ 🌲 optional classifier
   └──▶ 🧠 optional MLP after more gold
             │
             ▼
        📊 ranked lists only
```

#### 3.1 · Data-efficient default
Prototype distance, nearest confirmed neighbors, or a linear probe are the default after Round 1.
An MLP or other learned ranker is justified only after cumulative gold supports held-out validation.

#### 3.2 · Embedding boundary
Embeddings may retrieve, rank, cluster, and deduplicate.
Semantic similarity cannot assign a class or region as gold because surface similarity can hide negation, irony, or intensity differences.

#### 3.3 · Recorded score semantics
Every score names its model, version, feature source, calibration set, and meaning.
Similarity, margin, entropy, and novelty remain separate fields rather than one unexplained confidence number.

### 4 · Pool composition
**Composition contract**: quotas preserve coverage without pretending every region has equal corpus prevalence.

```text
📊 region-ranked lists
        │
        ├──▶ 🗺 configured region quotas
        ├──▶ 🌱 novelty and sparse-region reserve
        ├──▶ 🎲 random coverage reserve
        └──▶ 🔁 diversity and duplicate control
                    │
                    ▼
               📦 C_t manifest
```

#### 4.1 · Broad before small
C_t should be materially larger than B_t, with about 200 versus about 50 serving only as an initial planning example.
The exact sizes depend on corpus scale, human budget, model count, and region prevalence.

#### 4.2 · Diversity and novelty
Near duplicates are limited within each source, cluster, and retrieval neighborhood.
Items far from every known anchor receive a novelty slot even when their predicted class is uncertain.

#### 4.3 · Reproducibility
The manifest records the eligible population, random seed, quota table, ranker versions, raw scores, selection reason, and inclusion probability where available.
Re-running the same frozen inputs and seed must reproduce the pool.

## Aims

### A1 · 🗄 Eligible corpus
- A1.1 · C_t is drawn from a frozen and auditable eligible remainder.
  **Done when:** The manifest identifies the corpus version, exclusions, and sealed-test protection.

### A2 · 🗺 Seven-region retrieval
- A2.1 · Every diagnostic region and the novelty reserve has an explicit route into C_t.
  **Done when:** The quota and score records show how each selected item entered.

### A3 · 📊 Ranking models
- A3.1 · Ranking confidence cannot be mistaken for a gold annotation.
  **Done when:** Every ranker output is typed and the page forbids class or region inheritance.

### A4 · 📦 Pool composition
- A4.1 · C_t is broad, diverse, reproducible, and distinct from B_t.
  **Done when:** Pool size, quotas, seed, diversity controls, and provenance are recorded.

## States

### A1 · 🗄 Eligible corpus
- ✅ A1.1 · Met; division 1 fixes the frozen remainder and exclusions.

### A2 · 🗺 Seven-region retrieval
- ✅ A2.1 · Met; division 2 defines all seven routes and their provisional status.

### A3 · 📊 Ranking models
- ✅ A3.1 · Met; division 3 limits models and embeddings to ranking evidence.

### A4 · 📦 Pool composition
- ✅ A4.1 · Met; division 4 fixes broad-pool composition and reproducibility.

## Files

### 🔗 Related Board Pages · what this Page READS BY SCOPE
- `constrained by · ALL` · [QA0 §16](QA-semantic-contract/QA0-the-revised-conception.md)
  QA0 defines the candidate funnel and broad-pool boundary.
- `continues · ALL` · [QC2 §1](QC-selection-and-adjudication/QC2-prelabel-and-seal.md)
  QC2 consumes C_t under the prior closed guideline.

### Contracts · what must carry this rule
- `../../ref/ref-stages.md`
  The lifecycle reference must keep C_t separate from P_t and B_t.
- `../../ref/ref-embeddings.md`
  The embedding reference must prohibit label inheritance as gold.

## Law
- 260806 JL · 🔎 Candidate scores select evidence but never create gold
      Seven-region retrieval, classifiers, and embeddings may rank the remaining corpus, while human confirmation alone assigns final class and region records.

## Glossary
- 📦 **Candidate pool C_t**: the broad, auditable set retrieved before weak-model pre-labeling and human-batch composition.
- 🌱 **Novelty reserve**: configured capacity for items far from all confirmed semantic anchors.
- 📊 **Region scorer**: a lightweight model that ranks likely diagnostic position without assigning a gold region.

## Log
260806 · Reopened QC1 in DRAFT and replaced the previous stopping question with the approved candidate-pool contract.
