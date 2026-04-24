Reference: Project Files and Schemas
=====================================

Every skill reads and writes files under `{project_dir}/`. Plugin source files are never modified.


Directory layout
----------------

```
{project_dir}/
  config.yaml                     topic + label schema + model prefs
  .state.json                     state machine (Moderator-maintained)
  sample/
    sample.jsonl                  raw input texts (one per line)
  gallery/
    gallery.json                  curated labeled examples (Gallery Keeper)
    guideline.md                  annotation rules (Gallery Keeper)
    panel_config.json             panel composition this iteration
    history/
      iter_1.diff
      iter_2.diff
      CHANGELOG.md
  iterations/
    iter_{N}/
      candidate_pool.jsonl        ~100 items from Sampler (novelty + uncertainty + cluster)
      batch.jsonl                 20-30 items after Prober LLM judgment
      panel_labels.jsonl          per-(item, persona) labels
      panel_kappa.json            panel-internal κ
      disagreements.md            Analyzer narrative report
      disagreement_items.jsonl    Analyzer per-item classification
      researcher_decisions.jsonl  researcher adjudications
  cache/
    embeddings/
      vectors/{sha1}.npy          per-text cached embedding
      manifest.jsonl              id → sha1 → model manifest
      gallery_index.faiss         FAISS index over gallery
      gallery_index.meta.json     id → row map
    classifier/
      iter_{N}/
        model.pkl                 (logreg) or model/ (SetFit)
        train_metrics.json        CV F1, n_train, classes
        label_encoder.json
      predictions_iter_{N}.jsonl  classifier.predict output
      hard_items_iter_{N}.jsonl   hard_mining output
      latest -> iter_{N}/         symlink to most recent
    sampler/
      init_map.jsonl              /sl-init data map
      diagnostic_{ts}.jsonl       researcher-triggered snapshots
  validation/
    trajectory.jsonl              κ over iterations
    {dataset}_iter{N}_report.md   per-validation report
    {dataset}_heldout_sample.jsonl  Sampler's validation sample
    _cache/{dataset}/             HF dataset cache
  output/
    preflight_sample.jsonl        /sl-scale pre-flight 500-item sample
    annotations.jsonl             final labels (from /sl-scale)
    human_review_queue.jsonl      items flagged during scale
    scale_report.md               cost + throughput + tier distribution
```


config.yaml
-----------

```yaml
topic: |
  One paragraph describing the subjective dimension being labeled.

label_schema:
  dimension: humanity
  values:
    - name: high
      definition: "Expression shows vulnerability, empathy, specificity, or first-person emotional grounding."
    - name: medium
      definition: "Neutral observation or factual content; neither emotionally present nor absent."
    - name: low
      definition: "Performative, formulaic, detached, or adversarial expression."

panel:
  personas: [close-reader, plain-reader, skeptic]  # optional; default is auto
  domain: null        # or: medical / legal / consumer / social-media / ...

models:
  moderator:    claude-opus-4-7
  panel:        claude-sonnet-4-6
  analyzer:     claude-sonnet-4-6
  scale_fast:   claude-haiku-4-5   # cascade fast-path

embedding:
  model: sentence-transformers/all-MiniLM-L6-v2
  backend: sentence-transformers   # or: openai
  device: cpu                       # or: mps, cuda
  dim: 384
  index: faiss-flat                 # faiss-ivf for > 100K items
  thresholds:
    gallery_dedup_sim: 0.90         # Gallery Keeper: skip if ≥ this + same label
    cascade_inherit_sim: 0.85       # Tier 0: inherit if k-NN unanimous + avg_sim ≥ this
    cascade_k: 5
    prober_novelty_percentile: 0.80

classifier:
  backend: logreg                   # or: setfit, lora-bert
  thresholds:
    accept_margin: 0.30             # Tier 1: use classifier label if margin ≥ this
    accept_prob:   0.70             # and prob ≥ this
  train:
    cv_folds: 5
    val_split: 0.2
    include_panel_labels: true      # augment gallery with confirmed panel labels

scale:
  target_budget_usd: 100            # pre-flight warns if projected > this
  hard_cap_budget_usd: 200          # refuse to start if projected > this
  concurrency: 8
  routing: cascade                  # or: single, panel
```


.state.json (Moderator-owned)
-----------------------------

```json
{
  "status": "iterating",
  "iteration": 3,
  "gallery_size": 18,
  "last_validation": {"dataset": "goemotions", "kappa": 0.42, "iter": 3, "verdict": "IMPROVING"},
  "last_guideline_update": 3,
  "created_at": "2026-04-24T13:00:00Z",
  "updated_at": "2026-04-24T16:20:00Z"
}
```


sample.jsonl
------------

One raw item per line. Required: `id`, `text`.

```json
{"id": "r001", "text": "Given the scan results, I think we should..."}
{"id": "r002", "text": "Her survival chances are less than 20%."}
```

Optional: `source`, `metadata`, `speaker`, `timestamp`.


gallery.json (Gallery Keeper writes)
------------------------------------

JSON array. Entries are curated, not every panel-labeled item lands here.

```json
[
  {
    "id": "r042",
    "text": "...",
    "label": "high",
    "reasoning": "First-person emotional disclosure with specific concrete detail; no performative markers.",
    "rule_reference": "first-person + concrete → high (unless sarcastic)",
    "category": "canonical",
    "provenance": "researcher-adjudicated",
    "added_iteration": 3
  }
]
```

Categories: `canonical` | `boundary` | `novel`.
Provenances: `panel-unanimous` | `panel-majority` | `researcher-adjudicated`.


guideline.md (Gallery Keeper writes)
------------------------------------

Human-readable and prompt-ready. Structure:

```markdown
# Guideline: {topic}

## Label schema
(one subsection per value, with definition + canonical example + gallery link)

## Decision rules
- Rule 1: ... (motivated by gallery:r042, r058)
- Rule 2: ... (tie-breaker: when two rules conflict, X wins)

## Boundary cases
- boundary/r071: why it could be misread, correct label, rule

## Quick reference
| Signal | Label | Confidence |
|--------|-------|------------|
```


panel_labels.jsonl (Labeler Panel writes)
------------------------------------------

One row per (item, persona) pair.

```json
{"item_id":"r042","persona":"close-reader","label":"high","confidence":0.9,"reasoning":"..."}
{"item_id":"r042","persona":"skeptic","label":"medium","confidence":0.6,"reasoning":"..."}
```


disagreement_items.jsonl (Analyzer writes)
-------------------------------------------

```json
{"item_id":"r042","category":"A","summary":"Sarcastic vulnerability","surface_to_researcher":true}
{"item_id":"r071","category":"B","summary":"Quotation rule unclear","surface_to_researcher":true}
{"item_id":"r080","category":"C","summary":"Novel pattern not in schema","surface_to_researcher":true}
{"item_id":"r007","category":"D","summary":"Noise: one careless label","surface_to_researcher":false}
```


researcher_decisions.jsonl (Moderator writes after dialogue)
-------------------------------------------------------------

```json
{"item_id":"r042","decision_type":"label","final_label":"medium","reasoning":"Sarcasm negates surface signal."}
{"item_id":"r071","decision_type":"rule_refine","rule_id":"first_person_quotation","new_text":"When first-person is a quotation, the rule does not apply."}
{"item_id":"r080","decision_type":"schema_extend","new_label_name":"ambivalent","definition":"..."}
```


annotations.jsonl (scale output)
--------------------------------

```json
{"item_id":"r100001","label":"high","confidence":0.85,"method":"cascade-single"}
{"item_id":"r100002","label":"medium","confidence":0.62,"method":"cascade-escalated","votes":{"high":1,"medium":3,"low":1}}
```


trajectory.jsonl (Validator appends)
-------------------------------------

```json
{"iter":1,"dataset":"goemotions","kappa":0.31,"alpha":0.30,"f1_macro":0.35,"ceiling":0.46,"gap":-0.15,"verdict":"IMPROVING"}
{"iter":2,"dataset":"goemotions","kappa":0.42,"alpha":0.41,"f1_macro":0.47,"ceiling":0.46,"gap":-0.04,"verdict":"IMPROVING"}
{"iter":3,"dataset":"goemotions","kappa":0.48,"alpha":0.47,"f1_macro":0.53,"ceiling":0.46,"gap":0.02,"verdict":"CONVERGED"}
```
