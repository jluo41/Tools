# Reference: embedding and retrieval

Embeddings are a stable, economical representation layer for corpus navigation.
They help the workflow decide **which items deserve attention**. They never decide
what a subjective label means and never create human gold.

## 1. Authority boundary

| operation | embedding role | semantic authority |
|---|---|---|
| corpus map and clustering | represent and group texts | none |
| region retrieval | rank similarity to human-confirmed examples | human-confirmed examples and current closed guideline |
| novelty search | rank distance from covered items | none |
| duplicate detection | flag likely duplicates | keeper or human confirms treatment |
| batch stratification | provide sampling strata | sampling protocol |
| final label | no direct authority | human gold or separately validated production executor |

Cosine similarity is evidence about representation proximity, not evidence that two
items share a label. No nearest-neighbor, prototype, centroid, or cluster assignment
may be promoted to gold without a human event.

## 2. Lifecycle uses

### Initialization

Embed every eligible corpus item once, cache the vectors, and build an index. Reserve
the sealed-test identifiers before development access. Draw Round 1 randomly from the
remaining eligible pool; do not use the embedding map to manufacture initial labels,
regions, or prototypes.

### Later-round candidate retrieval

After a closed checkpoint supplies human-confirmed region examples, use embeddings to
construct a broad candidate pool `C_t`:

1. retrieve neighbors around representative H, L, N, HL, LN, HN, and HLN examples;
2. retrieve far or under-covered items for novelty and coverage;
3. deduplicate exact and near duplicates;
4. retain retrieval score, source example, region hypothesis, and sampling stratum;
5. pass candidates to weak-executor prelabeling and batch composition.

The region attached at retrieval time is a hypothesis. The human-confirmed final
region and H/L/N label are written only during the Session and checkpoint.

### Audits and final evaluation

Use embeddings to create representative strata, detect corpus neighborhoods missed by
the calibration rounds, and support probability sampling. Diagnostic oversampling of
rare neighborhoods must be reported separately from representative estimates.

### Production

Embeddings may support a production route only if that complete route was registered
and validated on the sealed final test. Raw similarity is never a universal acceptance
rule. A validated route still needs risk thresholds, provenance, and probability audit.

## 3. Candidate-ranking features

Useful features include:

- similarity to one or more human-confirmed region exemplars;
- distance to the cumulative human-gold set;
- cluster or neighborhood rarity;
- local density;
- duplicate score;
- metadata stratum;
- weak-executor disagreement after sealed prelabeling;
- guideline mismatch and reason-code novelty.

These features can feed a transparent ranker, linear model, or MLP. The resulting score
is a selection score, not a calibrated probability that the final label is correct.

## 4. Cache and provenance

A build starts only when a person asks (the page's `Run embedding` button, or
`--started-by <person>` on the command line); its Ticket and manifest record who.

Layout written by `engine/embedding_build.py build` (one folder per embedder):

```text
{job_root}/cache/embeddings/<version>/
├── manifest.json     model, encoder steps, input recipe, example, population, checksums
├── vectors.npy       one length-1 row per development item
├── rows.jsonl        row, item_id, text_hash, input_sha256, tokens, cut
├── map.jsonl         item_id, x, y, group (t-SNE or PCA, for the Board map)
├── map3d.jsonl       item_id, x, y, z (the rotating 3D view)
└── groups.json       k-means groups: size, keywords, silhouette by k
```

The cache holds no item text. A person who wants to see what a group is made of
asks for its typical items (`embedding_build.py examples`, or `Show typical items`
on the Board): the development items nearest the group centre by cosine, with
their text read from `corpus/items.jsonl` at that moment. Items waiting in a
round batch are never returned, and each call appends who saw which items to
`labeling/exposure/group_examples.jsonl`. Typical items often explain a group
better than its keywords: keywords are words that lift a group's average, so a
few items with a rare word can supply them while the centre of the group is
about something else.

Every vector or index row records corpus id, normalized-text checksum, model id and
version, dimensionality, preprocessing version, creation time, and index row. Changing
the model or preprocessing creates a new cache namespace; it does not silently rewrite
the old one.

## 5. Configuration

The embedder is chosen per build, not in `config.yaml` (a P0 authority file).
`engine/embedding_build.py` holds `CATALOG`, the open-weight models a person may
pick on the Board; each carries its size, word-piece limit, license, and
download size. As checked on 2026-09-16:

| model | parameters | numbers per item | reads up to | license |
|---|---:|---:|---:|---|
| `Qwen/Qwen3-Embedding-0.6B` (recommended) | 0.6B | 1024 | 32,768 | Apache-2.0 |
| `BAAI/bge-m3` | 568M | 1024 | 8,192 | MIT |
| `intfloat/multilingual-e5-large-instruct` | 560M | 1024 | 512 | MIT |
| `Qwen/Qwen3-Embedding-4B` (bfloat16) | 4B | 2560 | 40,960 | Apache-2.0 |
| `Qwen/Qwen3-Embedding-8B` (bfloat16) | 8B | 4096 | 40,960 | Apache-2.0 |
| `sentence-transformers/all-mpnet-base-v2` | 110M | 768 | 384 | Apache-2.0 |
| `sentence-transformers/all-MiniLM-L6-v2` | 22M | 384 | 256 | Apache-2.0 |

Per run, the person also chooses the text (`reply_context`, `reply`, or
`context`), an optional instruction for Qwen3 and e5-instruct models (written
in front of every input as `Instruct: <task>` / `Query:`), the group count, the
map method (t-SNE or PCA), and the seed. The manifest records all of them under
`settings`, and a changed setting is a new folder and Run.

Models with non-commercial or custom licenses (for example jina-embeddings-v3,
NV-Embed-v2, KaLM-Embedding-Gemma3-12B) are left out on purpose.

Model, dimensionality, backend, and index type are project choices. Retrieval quotas
and thresholds belong to round manifests when they affect a specific candidate pool.
Do not present example values as empirically justified defaults.

## 6. Failure modes

- **Semantic conflation:** surface-near texts may express opposite judgments.
- **Boundary collapse:** an embedding can blur H/L/N distinctions that the human treats
  as decisive.
- **Coverage illusion:** a dense map can still omit a rare but important region.
- **Duplicate dominance:** repeated templates can crowd out informative variation.
- **Score reification:** a retrieval score can be mistakenly interpreted as certainty.
- **Leakage:** indexing sealed-test content for development retrieval invalidates the
  test even when labels were hidden.

Mitigate these with explicit provenance, deduplication, probability sampling, blind
human adjudication, and access controls on the sealed final test.

## 7. Implementation boundary

The current library may expose embedding, nearest-neighbor, clustering, or classifier
utilities. Their existence does not prove the v2 retrieval contract is implemented.
Commands must verify manifests, sealing, provenance, and role boundaries before using
them. If those capabilities are absent, emit a structured `HOLD`; do not simulate a
valid round or inherit labels from similarity.

Built today: the initialization step (`engine/embedding_build.py build`, P0
`embedding-build`), which embeds, maps, and groups the development pool, plus
read helpers for the Board: `neighbors`, `group_examples`, and `item_text`. Not
built: later-round region retrieval, novelty search, and deduplication review.
