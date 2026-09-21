# Reference: project configuration

`config.yaml` contains tunable and declared project choices plus the immutable
P0 authority binding. It does not contain observed scores, mutable artifact
pointers, or per-item decisions. The `authority.meaning_receipt` written at G0
is a deliberately bound semantic receipt: the canonical `gates/g0/receipt.json`
rehashes it and closes the gate. It is not a general runtime cache and must
never be edited in place. The stored `human_id` and caller attestation are not
authenticated identity evidence; the CLI and local Board currently have no
identity provider. Do not treat this receipt as proof of who acted in a
multi-user or adversarial environment.

## 1. Full conceptual schema

```yaml
schema_version: subjective-label/v2

project:
  id: example-project
  description: "One human-grounded subjective-label project"

corpus:
  path: reviews.jsonl
  id_field: id
  text_field: text
  context_field: context_prev          # optional; folded under the text in the Rounds table
  metadata_fields: []
  population: "reviews in the declared target study"
  source: {name: "...", uri: "...", license: "..."}

construct:
  name: openness
  question: "How open to experience does the reviewer describe the physician?"
  seed: "a vague initial human idea"
  scope: "what texts and behaviors the project intends to judge"

authority:
  human_id: JL
  mode: single_human_semantic_authority
  creates_human_gold: true
  meaning_confirmed: false             # written true only by confirm_meaning
  meaning_receipt: null                # caller-attested; not identity-authenticated

labels:
  type: ordinal
  values: [high, low, none]
  none_value: none
  meanings:
    high: "one plain sentence a new reader can apply"
    low: "..."
    none: "..."

regions:
  values: [H, L, N, HL, LN, HN, HLN]
  meanings:
    H: clearly high
    HL: between high and low
    HLN: all three are plausible

uncertainty:
  levels: [low, medium, high]
  meaning: "how unsure the human is about the class; unsure is never none"
  unresolved_is_label: false

reveal:
  reference_observations:              # optional; omit for no comparison
    label: "Source raters (external observations, not gold)"
    file: path/to/annotations.jsonl    # relative to the repo root
    id_field: item_id
    count_fields: [overall_rating]
    item_fields: [harm_type]

embedding:
  backend: sentence-transformers
  model: sentence-transformers/all-MiniLM-L6-v2
  device: cpu
  index: faiss-flat

rounds:
  round1:
    sampling: random
    human_batch_size: 60               # 1-200; engine default 20
    seed: 42                           # engine default 42
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
- one vague construct seed and scope, plus the one `construct.question` a labeler answers;
- a plain meaning for each class (`labels.meanings`);
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

`engine/calibration.py release_round` reads `rounds.round1.human_batch_size`
and `rounds.round1.seed` when the call names no `n` or seed; the Board's
`Start round 1` button uses the same batch size as its default. The size must
be 1 to 200 and no larger than the development pool. The engine reads no
later-round setting yet, because only round 1 is built.

## 3a. Meaning and reveal settings

These fields carry the words a person reads. The engine reads them as follows:

| field | read by | shown as |
|---|---|---|
| `construct.question` | Board Labeling surface · `engine/fence_source.py` | the one question on `Data → Contract` and at the top of `Labeling → Label` (the label definitions); near the top of the G_00 guideline |
| `labels.meanings` | Board · `fence_source.py` | a map from each value in `labels.values` to one sentence; shown on `Data → Contract`, under each class button, and in the G_00 guideline |
| `regions.meanings` | Board · `fence_source.py` | a map from each region to a short phrase; shown on `Data → Contract` before confirmation, as hover text on the boundary buttons, and in the G_00 guideline |
| `uncertainty.meaning` | Board · `fence_source.py` | one sentence on `Data → Contract` and in the G_00 guideline |
| `corpus.context_field` | Board · `engine/calibration.py` | the earlier turns shown above the item text (default `context_prev`) |

The G0 meaning receipt binds the whole `construct`, `labels`, `regions`, and
`uncertainty` blocks by checksum. Changing any meaning after G0 breaks that
receipt: `status` reports an integrity error and the compatibility tag is P0;
the Workflow still resolves its Run frontier from the declared graph and
receipts.

`authority.human_id` must be set, `authority.creates_human_gold` must be
`true`, `authority.mode` must be `single_human_semantic_authority`, and
`simulation_only` must not be `true`. Otherwise `authority_hold(config)` puts
the job on HOLD.

`reveal.reference_observations` is optional. It names outside observations to
show after the human locks a first answer. They are never gold.

| field | meaning |
|---|---|
| `label` | the heading shown above the comparison |
| `file` | a JSONL file, path relative to the repo root (the folder with `pyproject.toml` and `code/`; the job root when none is found) |
| `id_field` | the field in that file that matches the job's `item_id` |
| `count_fields` | for each item, count every value of these fields across its rows (for example rater votes) |
| `item_fields` | for each item, the first value of these fields |

`engine/calibration.py` builds the index once into `cache/reveal/`, from
`eligible` ids only (`ref-assets.md` §3). The comparison is stored in the
`reveal` event with `not_gold: true`; an item with no row gets `missing: true`.
Without this block the reveal is `kind: none`. Worked example:
`examples-nlp/Project-Subjective-Label/diagram/01-label-runs-260807/pages/S-Label-4-dices-unsafe-response/seed/config.seed.yaml`
(repo-relative).

## 4. Executor settings

Every weak executor registry entry must include:

```yaml
- id: weak-a
  provider: "..."
  model: "..."
  version: "..."
  family: "..."
  wrapper: policy/versions/G_NN/wrappers/weak-a.yaml   # wrappers live inside the policy version
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

`.state.json` is a derived cache written by authorized keepers and may contain:

```json
{
  "schema_version": "subjective-label/state-v3",
  "building_frontier": "Contract | Round | Freeze | HOLD",
  "scanning_frontier": "not-runnable | Test | Scan | Audit | complete | HOLD",
  "handoff_checksum": null,
  "open_round": "round-02",
  "round_step": "prepare | judge | learn | close",
  "closed_policy": "G_1",
  "cumulative_gold": "D_1",
  "sealed_test_status": "reserved",
  "latest_checkpoint": "checkpoint-01",
  "implementation_holds": []
}
```

State points to immutable artifacts by id or checksum and does not duplicate
their contents. The current adapter may expose `phase`/P0-P5 as a compatibility
projection from domain receipts; when this cache disagrees, the receipts win.
That projection is not the Workflow frontier or routing authority. Resolve the
next Run Spec from the Workflow Definition and the allocated Run
Tickets/Results/runtime receipts. Keep legacy fields readable while adapters
are migrated; do not let them authorize allocation or closure.

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
