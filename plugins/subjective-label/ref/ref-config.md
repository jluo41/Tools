# Reference: project configuration

`config.yaml` contains tunable and declared project choices.
It does not contain runtime state, observed scores, human decisions, or mutable artifact pointers.

## 1. Full conceptual schema

```yaml
schema_version: subjective-label/v2

project:
  id: example-project
  description: "One human-grounded subjective-labeling project"

corpus:
  path: reviews.jsonl
  id_field: id
  text_field: text
  metadata_fields: []
  population: "reviews in the declared target study"

construct:
  name: openness
  seed: "a vague initial human idea"
  scope: "what texts and behaviors the project intends to judge"

authority:
  human_id: JL
  mode: single_human_semantic_authority

labels:
  type: ordinal
  values: [high, low, none]
  none_value: none

regions:
  values: [H, L, N, HL, LN, HN, HLN]

uncertainty:
  levels: [low, medium, high]
  unresolved_is_label: false

embedding:
  backend: sentence-transformers
  model: sentence-transformers/all-MiniLM-L6-v2
  device: cpu
  index: faiss-flat

rounds:
  round1:
    sampling: random
    human_batch_size: 60
  later:
    candidate_pool_size: 200
    human_batch_size: 50
    region_quotas: {}
    novelty_quota: null
    consensus_audit_fraction: null
    seed: 0

region_scorer:
  backend: prototype | linear | classifier | mlp
  validation: {}

weak_executors:
  models: []
  independent: true
  structured_reason: true
  sealed_before_human: true

metrics:
  class: [macro_f1, balanced_accuracy, per_class, confusion, kappa]
  ordinal: [quadratic_weighted_kappa, mae]
  uncertainty_interval: bootstrap

stopping:
  quality_floor: {}
  epsilon: null
  consecutive_rounds_k: null
  coverage_minima: {}
  unresolved_risk_max: null
  require_human_signoff: true

final_test:
  source: corpus_holdout | fresh_same_population
  size: null
  representative: true
  diagnostic_supplement: false
  seed: 0
  custodian: null

evaluation:
  minimal_instruction: null
  heldout_executor_required: true
  repeated_runs: 1

production:
  policy: single | ensemble | validated_routing
  quality_floor: {}
  risk_rules: {}
  human_capacity: null
  cost_budget: null
  final_audit: {}

external_validation:
  enabled: false
  datasets: []
```

Values shown above are schema examples, not universal defaults.
Project-specific numeric settings are chosen from pilot evidence, desired uncertainty, budget, and intended use.

## 2. Required inputs

The minimum project input is:

- one corpus path with stable ids and text;
- one vague construct seed and scope;
- one identified human semantic authority;
- the label and region schema, using the default H/L/N plus seven regions unless explicitly changed;
- a sealed-test sampling frame and custodian;
- an embedding model for retrieval.

An objective function, public dataset, classifier, model panel, and automatic construct selector are not required.

## 3. Round settings

Round 1 uses random sampling from the eligible development pool.
Later rounds separate candidate-pool size from human-batch size.

`region_quotas`, `novelty_quota`, and `consensus_audit_fraction` are versioned per round when they change.
The actual batch manifest records resolved quotas, seed, strata, and inclusion probabilities.

## 4. Executor settings

Every weak executor registry entry must include:

```yaml
- id: weak-a
  provider: "..."
  model: "..."
  version: "..."
  family: "..."
  wrapper: wrappers/weak-a.yaml
  decoding: {temperature: 0}
  role: seen | heldout | production_candidate
```

The held-out role cannot participate in guideline optimization before final evaluation.

## 5. Stopping settings

Stopping is a conjunction, not a weighted score.
The config records thresholds, while each checkpoint records observed evidence and pass or fail.

`epsilon` and `consecutive_rounds_k` apply only to comparable audit series.
A failed quality floor cannot be overridden by a small improvement.

## 6. Final-test settings

`final_test.source` names whether items are held out from the original corpus or collected separately from the same population.
The manifest, not config, stores protected ids and access logs.

The final-test size must support the intended confidence interval and protected-stratum claims.
Diagnostic enrichment is reported separately from the representative headline sample.

## 7. Runtime state

`.state.json` is written by authorized keepers and may contain:

```json
{
  "schema_version": "subjective-label/state-v2",
  "project_status": "calibrating",
  "open_round": "round-02",
  "round_phase": "candidate | prelabel | batch | session | checkpoint",
  "closed_policy": "G_1",
  "cumulative_gold": "D_1",
  "sealed_test_status": "reserved",
  "latest_checkpoint": "checkpoint-01",
  "implementation_holds": []
}
```

State points to immutable artifacts by id or checksum.
It does not duplicate their contents.

## 8. Migration from v1

| old field or assumption | v2 treatment |
|---|---|
| `topic` | `construct.name`, `construct.seed`, and `construct.scope` |
| `objective` required | optional extension outside the core human-grounded workflow |
| `panel` as authority | `weak_executors` as sealed evidence producers |
| `gallery` as mixed gold | migrate rows by inspectable human provenance |
| fixed anchor and fresh heldout used during development | round audit protocol plus separately sealed final test |
| public dataset convergence | optional external validation only |
| `scale.routing=cascade` with k-NN inheritance | validated production policy with explicit risk and audit |

Migration never infers human gold from panel unanimity, majority, or missing provenance.
