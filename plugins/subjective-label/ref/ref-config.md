# Reference: Project config.yaml (the general contract)

The single source of truth for a subjective-label project's `config.yaml`.
**Construct-agnostic and zero-hardcoding** — nothing physician / openness /
Big-Five appears in the engine; a task expresses itself entirely through these
fields. See `ref-contract.md` (schema+metrics), `ref-datasets.md` (license
battery), `note-update.md` (why each field exists).

---

## Full schema

```yaml
task:
  corpus_path: "..."               # jsonl of {id, text, ...}
  text_field: text
  id_field: id
  metadata_fields: [...]           # optional passthrough (platform, rating, ...)

construct:                         # WHAT to label (the target dimension)
  name: "..."                      # short handle, e.g. "openness"
  mode: auto | seed                # auto = multi-LLM propose + objective-select (S2); seed = human one-liner
  definition: null | "..."         # required iff mode=seed
  discriminant_from: [...]         # sibling constructs to stay distinct from → confound strata + discriminance objective

objective:                         # the selection/stop criterion — the irreducible human input (S2)
  kind: downstream | discriminance | dataset_match
  spec: {...}                      # downstream: a regression/target; discriminance: sibling labels; dataset_match: a public set

labels:                            # see ref-contract.md §1 (categorical | ordinal now)
  type: categorical | ordinal
  values: [...] | null             # 2–6 (ordered iff ordinal); null → elicited in dialogue
  none_value: <value|null>         # the "signal absent" catch-all, if any
  tie_break: none_loses | first    # majority-vote tie rule (default: none_loses if none_value set else first)

labeler:                           # the LABELER (multi-LLM panel) — reliability, NOT ground truth
  engines:
    claude_sdk: {model: haiku}
    codex:      {model: gpt-5.5}
  validator_model: null            # engine used for validation MUST differ from labeler (anti-circular, F1)
  personas: [close-reader, plain-reader, skeptic]   # for persona-panel mode

sampling:                          # two pools, distinct jobs (F6)
  representative: {size: 120, base_rate_aware: true, none_quota: 0.33}   # honest metrics
  enriched:       {per_stratum: 8}                                       # guideline refinement (discriminant_from-driven)

embedding: {backend: sentence-transformers | openai, model: "..."}       # openai/text-embedding-3-large ok
classifier: {backend: logreg | setfit | lora-bert, thresholds: {accept_margin: 0.3, accept_prob: 0.7}}

eval:                              # three sets, distinct jobs (F7)
  anchor:  {size: 120, frozen: true,  pool: representative}   # fixed → version comparison
  heldout: {size: 60,  fresh: true, never_trained: true}     # fresh each round → honest generalization + anti-circular

metrics: [reliability_panel_kappa, executor_independence, generalization_gap, objective_score]  # auto by labels.type; ref-contract §2

license: {battery: [popquorn, dices, ...], require_ceiling: true}        # engine-level, one-time (F2/F3; ref-datasets)

convergence: {objective_plateau: 0.02, stability: true, heldout_gap_max: 0.05}   # incl held-out gate (F8)
escape_hatch: {extreme_case_review: on | off}                            # optional human on extreme cases only
```

`.state.json` holds runtime state (status, iteration, versions) — NOT config.

---

## Field notes

- **construct.mode=auto** defers "what exactly to measure" to S2 (multi-LLM
  propose → select by `objective`). `mode=seed` takes a one-line human definition.
  Either way the objective is the only mandatory human input (already in the
  research design for the physician instance: "predict opioid Rx + be discriminant").
- **objective.kind=discriminance** needs no external data (works now).
  `downstream` needs the target regression (may be PHI-gated). `dataset_match`
  needs a public labeled set.
- **labeler ≠ ground truth.** Panel agreement is a reliability signal. Correctness
  comes from the license battery (public per-rater sets), not from the panel.
- **labels.values: null** is valid — elicited during init; once fixed it must obey
  `ref-contract.md` (2–6, ordered iff ordinal, exhaustive with a catch-all).

---

## Migration from the old shape (B01–B03)

The engine reads the new schema; keep a compatibility shim while tasks migrate:

| old | new |
|-----|-----|
| `topic` | `construct.name` + `construct.definition` |
| `purpose` | folded into `construct.definition` / `objective` |
| `corpus:` | `task:` |
| `label_schema: null` | `labels: {type, values: null}` |
| `panel:` | `labeler:` |

`lib/label.py` / `lib/kappa.py` already accept `--labels`/`--type` overrides, so a
not-yet-migrated task still runs by passing them on the CLI.

---

## Minimal example (a NON-physician instance, to prove generality)

```yaml
task: {corpus_path: reviews.jsonl, text_field: text, id_field: id}
construct: {name: sarcasm, mode: seed, definition: "is the comment sarcastic?", discriminant_from: [sentiment]}
objective: {kind: discriminance, spec: {siblings: [sentiment]}}
labels: {type: categorical, values: [sarcastic, sincere, unclear], none_value: unclear}
labeler: {engines: {claude_sdk: {model: haiku}, codex: {model: gpt-5.5}}}
eval: {anchor: {size: 100, frozen: true}, heldout: {size: 50, fresh: true}}
```
