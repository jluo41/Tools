# Library map: reuse useful engines and name every missing capability
state: ✅ SETTLED · implementation intentionally deferred
owner: CC
method: Map each revised workflow responsibility to current library evidence, required adaptation, or a new implementation unit without changing code in this migration.

## Opening
Which current libraries remain useful, which old behaviors conflict with the revised method, and what must be built later?
Embedding, sampling, labeling, metrics, and classification contain reusable primitives.
Their current orchestration still assumes model-consensus gold, public-license convergence, and label inheritance.
This Board and skill migration is not authorized to rewrite implementation code.
This page maps reuse, retired paths, missing engines, and the later code gate.

**Where this page sits**: QF1 through QF3 settle contracts; QF5 tests documentation behavior; a separate implementation task begins from this map.

**Why it matters**: Updating prose without naming engine gaps would make canonical skills promise a sealed workflow that current scripts cannot actually execute.

## Writing Style
**Language and sentences**: Mark each unit reuse, adapt, replace, new, or optional with concrete evidence.

**Honesty**: Do not call a contract implemented when no script writes or validates its artifacts.

**Scope**: Record code work but make no `lib/*.py` change on this page.

## Diagram
**Implementation map**: reusable primitives feed a later orchestration layer, while retired authority paths stay disabled.

```text
✅ reuse      embed · basic sample · label · metrics · classifier primitives
🔧 adapt      schemas · scoring contexts · manifests · provenance
🆕 build      seal · round checkpoint · final test · production audit
🚫 retire     model consensus gold · public κ stop · raw k-NN inheritance
```

## Content

### 1 · Reusable primitives
**Keep with contract changes**: several libraries solve narrow technical problems without needing semantic authority.

```text
embed.py     vectors · cache · nearest · cluster
sample.py    seeded selection primitives
label.py     model execution primitive
kappa.py     agreement and metric primitive
classify.py  optional scorer and executor primitive
```

#### 1.1 · Embeddings and sampling
`embed.py` remains the vector and retrieval engine after label-inheritance callers are removed.
`sample.py` can support seeded strata and candidate manifests after it gains seven-region and inclusion-probability outputs.

#### 1.2 · Labeling and metrics
`label.py` can execute one frozen policy when outputs include model, wrapper, policy, reason, and run provenance.
`kappa.py` remains one metric primitive but cannot define convergence by itself.

#### 1.3 · Classifier
`classify.py` may rank regions or serve a validated production executor.
Its confidence does not create gold and its automatic-acceptance role requires direct validation and final audit evidence.

### 2 · Required adaptations
**Contract migration**: current scripts need schema and context changes before canonical skills may call them as revised engines.

```text
🔧 adaptations
├── class + region + uncertainty records
├── C_t/P_t/B_t manifests
├── audit versus challenge metrics
├── policy and wrapper identity
└── item-level provenance
```

#### 2.1 · Selection and scores
Selection outputs need source pools, strata, ranker identity, seed, inclusion probability, and blind-access state.
Metric outputs need population, weights, confidence intervals, and comparison context.

#### 2.2 · Model execution
Weak-model runs need independent registry entries, immutable outputs, structured reasons, seal checksums, and failure states.
Production attempts need idempotent run keys and terminal reconciliation.

### 3 · New implementation units
**Missing engines**: no current library provides the complete revised artifact or gate.

```text
🆕 seal manager
🆕 round state and checkpoint validator
🆕 policy version and regression manager
🆕 final-test custodian and evaluator
🆕 production router and reconciler
🆕 probability audit and provenance reporter
```

#### 3.1 · Calibration infrastructure
The later code plan needs state transitions, seal access, human-first records, checkpoint validation, cumulative-gold writing, and policy diffs.

#### 3.2 · Final and production infrastructure
It also needs test reservation and invalidation, executor registry and scorecards, production attempts, risk routing, final sampling, repair loops, and provenance reports.

### 4 · Retired and optional paths
**Forbidden shortcuts**: old outputs may remain as evidence but cannot drive the revised authority or stop logic.

```text
🚫 panel unanimous → gold
🚫 Category D majority → gold
🚫 public dataset κ → project convergence
🚫 embedding neighbors → final label
🚫 final test → policy tuning without replacement

optional: external license · construct auto-selection · auto lexicon
```

#### 4.1 · Retired core behavior
`license.py`, `construct.py`, and old cascade rules cannot govern the human-grounded core workflow.
They may be retained for separate optional research claims only when routing makes that scope explicit.

#### 4.2 · Later implementation gate
Code work begins only from approved QF1 through QF4 contracts and receives its own plan, tests, and migration safety review.
Until then, canonical skills HOLD at missing engine boundaries and may operate only through inspectable manual artifacts.

## Aims

### A1 · ✅ Reusable primitives
- A1.1 · Every current library has an evidence-backed retained role or no retained role.
  **Done when:** The map distinguishes technical utility from semantic authority.

### A2 · 🔧 Required adaptations
- A2.1 · Schema and context changes are named before any code edit begins.
  **Done when:** Selection, execution, metrics, and provenance gaps have target contracts.

### A3 · 🆕 New implementation units
- A3.1 · Every revised artifact and gate without an engine is visible.
  **Done when:** Calibration, final-test, production, and audit units have named responsibilities.

### A4 · 🚫 Retired and optional paths
- A4.1 · Legacy shortcuts cannot silently remain on the canonical route.
  **Done when:** Retired behaviors and optional extensions have explicit routing boundaries.

## States

### A1 · ✅ Reusable primitives
- ✅ A1.1 · Met; division 1 maps current libraries to narrow retained roles.

### A2 · 🔧 Required adaptations
- ✅ A2.1 · Met; division 2 lists contract adaptations.

### A3 · 🆕 New implementation units
- ✅ A3.1 · Met; division 3 names missing engines.

### A4 · 🚫 Retired and optional paths
- ✅ A4.1 · Met; division 4 records forbidden shortcuts and deferred scope.

## Files

### Engines · what a later implementation plan inspects
- `../../lib/embed.py`
  Reusable vector and retrieval primitive.
- `../../lib/sample.py`
  Seeded sampling primitive requiring revised manifests and strata.
- `../../lib/label.py`
  Model-execution primitive requiring policy, wrapper, reason, and seal provenance.
- `../../lib/kappa.py`
  Metric primitive requiring new contexts rather than convergence authority.
- `../../lib/classify.py`
  Optional scorer or validated production executor.
- `../../lib/converge.py`
  Existing stop logic requiring replacement by the four-gate contract.

### 🔗 Related Board Pages · what this Page READS BY SCOPE
- `constrained by · ALL` · [QF1 page](QF-execution-contract/QF1-skill-command-contract.md)
  QF1 prevents commands from claiming unimplemented automation.
- `constrained by · ALL` · [QF2 page](QF-execution-contract/QF2-artifact-schema-config.md)
  QF2 defines the records later code must write and validate.

## Law
- 260806 JL · 🔧 Contract migration precedes implementation migration
      Existing technical primitives may be reused, while missing seals, checkpoints, final tests, production routing, and audits remain explicit HOLDs until separately implemented.

## Glossary
- 🔧 **Adapt**: retain a technical primitive after changing its schema, caller, or authority context.
- 🆕 **Implementation unit**: a separately testable engine responsibility missing from the current library.
- 🚫 **Retired path**: behavior preserved only as history or optional research and excluded from the canonical workflow.

## Log
260806 · Created QF4 as the no-code implementation map approved by the migration plan.
