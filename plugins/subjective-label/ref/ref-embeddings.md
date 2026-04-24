Reference: Embedding Integration
=================================

How the plugin uses sentence embeddings. Embeddings are a **speed tool**,
not a judgment tool — they help pick candidates, deduplicate, and scale, but
never decide a label.


Core principle
--------------

| Question                           | Who answers              |
|------------------------------------|--------------------------|
| "Which items should the panel see?"| Embedder (distance, clusters) |
| "Is this gallery entry redundant?" | Embedder (cos-sim) + Gallery Keeper (final decision) |
| "Can we skip LLM labeling at scale?" | Embedder (k-NN) + Panel (fallback when sim low) |
| "What label does this item get?"   | Panel only               |

Embedding is **read-only** from the labeling perspective — the label for each
item comes from panel reasoning, never from vector math.


Where embeddings enter the pipeline
------------------------------------

```
  /sl-init        (optional) cluster the sample → show researcher a "map"
                  before they define labels
       │
       ▼
  /sl-iterate     Prober uses embedder to:
                    - embed new sample items (one-time, cached)
                    - cluster the sample
                    - for each cluster, pick items far from gallery
                    - score candidates by (distance, cluster novelty)
                  Hand Prober a ~100-item candidate pool;
                  Prober's LLM judgment picks the final 20-30.
       │
       ▼
  Gallery Keeper  uses embedder `nearest` to check:
                    if new entry's cos-sim to existing same-label entries > 0.9
                    AND reasoning overlaps: skip (redundant).
       │
       ▼
  /sl-validate    stratified sampling of held-out items:
                    cluster, then sample N per cluster — avoids biased benchmarks.
       │
       ▼
  /sl-scale       Tier 0 cascade (the big cost savings):
                    for each corpus item, find top-5 gallery k-NN
                    if top-5 unanimous label AND avg sim > 0.85: inherit
                    else: escalate to Tier 1 (fast-patterns + cascade)
```


Model choices
-------------

| Model | Size | Dim | Speed (CPU) | Quality | When to use |
|-------|------|-----|-------------|---------|-------------|
| `sentence-transformers/all-MiniLM-L6-v2` | 22M | 384 | ~2K/sec | good | default, English, any scale up to 10M |
| `BAAI/bge-small-en-v1.5` | 33M | 384 | ~1.5K/sec | better | English, quality-sensitive |
| `BAAI/bge-base-en-v1.5` | 109M | 768 | ~500/sec | best (local) | research, < 1M items |
| `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` | 118M | 384 | ~800/sec | good | non-English or mixed |
| OpenAI `text-embedding-3-small` | (API) | 1536 | API-bound | best | budget allows, quality-critical |
| OpenAI `text-embedding-3-large` | (API) | 3072 | API-bound | SOTA | small corpus, best possible quality |
| `dmis-lab/biobert-base-cased-v1.1` | 110M | 768 | ~400/sec | domain | medical text |
| `nlpaueb/legal-bert-base-uncased` | 110M | 768 | ~400/sec | domain | legal text |

Rule of thumb:
- < 100K items & English & you just want it to work → `all-MiniLM-L6-v2`
- Need best quality & corpus > 500K → OpenAI `text-embedding-3-small`
- Domain-specific (medical/legal) → corresponding *-BERT


config.yaml
-----------

```yaml
embedding:
  model: sentence-transformers/all-MiniLM-L6-v2
  backend: sentence-transformers      # or: openai
  device: cpu                          # or: mps (Apple Silicon GPU), cuda
  dim: 384
  index: faiss-flat                   # < 100K items
                                      # use faiss-ivf for > 100K
```

Change model → change `model` + `dim`. Old cache stays valid (keyed by model hash); new model triggers re-embedding on first use.


Cache layout
------------

```
{project_dir}/cache/embeddings/
├── vectors/{sha1(model + text)}.npy   # one file per unique (model, text)
├── manifest.jsonl                      # append-only: id, sha1, model, created_at
├── gallery_index.faiss                 # FAISS index over current gallery vectors
└── gallery_index.meta.json             # maps FAISS row → gallery entry id
```

- Vectors are stored per (model, text) hash, so swapping models invalidates nothing.
- FAISS index is rebuilt whenever the gallery changes (Gallery Keeper signals Embedder).
- First-time embed of 10K items: ~5 seconds on CPU with `all-MiniLM-L6-v2`.
- First-time embed of 5M items: ~30-40 minutes single-CPU; parallelize if needed.


Thresholds used in code
------------------------

Set in `config.yaml` under `embedding.thresholds`. Defaults:

```yaml
embedding:
  thresholds:
    gallery_dedup_sim: 0.90         # Gallery Keeper: ≥ this + same label → redundant
    cascade_inherit_sim: 0.85       # /sl-scale Tier 0: ≥ this + unanimous k-NN → inherit label
    cascade_k: 5                    # how many gallery neighbors to consult
    prober_novelty_percentile: 0.80 # Prober: pick items whose distance-to-gallery is above this percentile
```

These thresholds are conservative. Researchers can tune them per project — raising
`cascade_inherit_sim` means fewer embedding-only inherits and more LLM calls
(safer, more expensive); lowering it means faster but risks mis-label propagation.


Dependencies
------------

Install once in the researcher's venv:

```bash
pip install -r lib/requirements.txt
# sentence-transformers, faiss-cpu, scikit-learn, numpy, pyyaml, (optional) openai
```

For Apple Silicon GPU acceleration:
```bash
# sentence-transformers uses PyTorch backend; mps just works
# set device: mps in config.yaml
```

For CUDA:
```bash
# install torch with CUDA first; then set device: cuda in config.yaml
```


Why not everything-embeds?
--------------------------

Common failure modes when embeddings drive labeling directly:

1. **Semantic conflation** — "I feel alive" and "I feel nothing" are embedding-close, labels opposite.
2. **Register confusion** — sarcasm, irony, genre mimicry look like the target in vector space.
3. **Scale drift** — embedding of "extremely high" vs "very high" collapses; ordinal distinctions are lost.
4. **Opacity** — when the label is wrong, you can't point to which phrase drove it.

These are exactly the failure modes the multi-persona panel is designed to catch.
So: embedders FIND candidates, panel JUDGES them.


Summary
-------

- One module (`lib/embed.py`), one agent (`embedder`), one config section (`embedding:`)
- Used by Prober, Gallery Keeper, Labeler Panel (scale), Validator
- Never used for final labeling decisions
- Swap model by changing one config line; cache-friendly
- Default model works offline, free, fast enough for 10M-scale corpora
