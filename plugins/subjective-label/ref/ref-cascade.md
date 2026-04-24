Reference: Three-Tier Cascade
==============================

The cost-reduction machine for /sl-scale. Built on the principle that
most items are easy and a small minority are hard.


The tiers
---------

```
   ┌────────────────────────────────────────┐
   │ Tier 0 — Embedding k-NN                │   cheapest
   │   ~$0.00001 per item (CPU only)        │   fastest
   │   handles:   similar-to-gallery items  │   ~60-80%
   └────────────────────┬───────────────────┘
                        │ unresolved
                        ▼
   ┌────────────────────────────────────────┐
   │ Tier 1 — Trained small classifier      │   cheap
   │   ~$0.0001 per item                    │   fast
   │   handles:   easy-but-not-identical    │   ~10-30%
   └────────────────────┬───────────────────┘
                        │ unresolved
                        ▼
   ┌────────────────────────────────────────┐
   │ Tier 2 — LLM panel (3-5 personas)      │   expensive
   │   ~$0.05-0.20 per item                 │   slow
   │   handles:   genuinely hard cases      │   ~5-15%
   └────────────────────────────────────────┘
```


Tier 0 — Embedding k-NN
------------------------

**Invariant:** if the top-5 gallery neighbors all share the same label AND
average cosine similarity is high, the item is effectively already in the
gallery. Inherit.

**Algorithm:**
```
neighbors = embedder.nearest(item, gallery_index, k=5)
top_labels = [n.gallery_label for n in neighbors]
avg_sim    = mean(n.sim for n in neighbors)

if all_same(top_labels) and avg_sim >= cascade_inherit_sim:
    assign: label = top_labels[0], method = "tier0", confidence = avg_sim
else:
    escalate to Tier 1
```

**Config:**
```yaml
embedding:
  thresholds:
    cascade_inherit_sim: 0.85   # default; raise for safety, lower for speed
    cascade_k: 5
```

**Failure modes:**
- Items whose surface is similar but whose subtle signal differs → wrong
  label inherited. Mitigation: Tier 2 will catch these because we also
  validate κ against public datasets.
- Items in a label region the gallery doesn't cover → escalate to Tier 1.


Tier 1 — Trained classifier
----------------------------

**Invariant:** if the classifier's top-probability is high AND the margin
to second-best is wide, the decision boundary is clear. Use the label.

**Algorithm:**
```
pred = classifier.predict(item)  # {label, prob, margin, entropy}

if pred.margin >= accept_margin and pred.prob >= accept_prob:
    assign: label = pred.label, method = "tier1", confidence = pred.prob
else:
    escalate to Tier 2
```

**Config:**
```yaml
classifier:
  backend: logreg             # or setfit
  thresholds:
    accept_margin: 0.30
    accept_prob:   0.70
```

**Retrain trigger:** classifier is retrained at the end of every
/sl-iterate. Before /sl-scale, Moderator optionally invokes SetFit backend
for a one-time higher-quality train, if the researcher opts in.

**Failure modes:**
- Classifier can be wrong with high confidence if training data is biased
  (small, gallery-only). Tier 2's panel catches these during validation.
- If classifier CV F1 is low (< 0.6), tighten thresholds or skip Tier 1
  entirely (all non-Tier-0 items go straight to panel).


Tier 2 — LLM panel
-------------------

**Invariant:** the item is genuinely on the boundary. Use the full panel.

**Algorithm:**
```
panel_labels = labeler_panel.label(item, personas=config.panel.personas)
majority = mode(panel_labels)
support = count(panel_labels == majority) / len(panel_labels)

if support >= 0.6:
    assign: label = majority, method = "tier2", confidence = support
else:
    queue to human_review_queue.jsonl (flagged for researcher)
```

Items that even the panel can't resolve (support < 60%) are surfaced for
researcher review. These become candidates for the next /sl-iterate.


Configurable cost target
-------------------------

Researcher sets a target cost budget for /sl-scale. Example:

```yaml
scale:
  target_budget_usd: 100
  hard_cap_budget_usd: 200
```

The Sampler `scale_preflight` mode estimates the tier distribution on a
500-item sample and projects total cost. If projected > target_budget,
Moderator warns the researcher and suggests:
- Raise `cascade_inherit_sim` (more Tier 0 acceptance, less cost but more risk)
- Switch classifier to SetFit (more Tier 1 acceptance, higher quality)
- Reduce panel size from 5 to 3 (30-40% Tier 2 cost saving)


Tier routing decisions are logged
----------------------------------

Every item's annotation records its tier:

```json
{"id": "c123", "label": "high", "confidence": 0.87, "method": "tier0"}
{"id": "c456", "label": "medium", "confidence": 0.78, "method": "tier1"}
{"id": "c789", "label": "low", "confidence": 0.80, "method": "tier2",
 "votes": {"low": 4, "medium": 1}}
```

This lets the researcher audit: "show me all items resolved by Tier 0 —
are any obviously wrong?" (spot-check Tier 0 is the cheapest audit).


Skipping tiers
--------------

For diagnostic or research runs:
- `routing=panel`: skip Tier 0 + 1, use panel everywhere (expensive, baseline)
- `routing=single`: skip Tier 0 + 1, use one persona (cheapest LLM option)
- `routing=cascade`: default 3-tier

Researchers typically use `panel` on the validation set, `cascade` at scale.


Convergence and drift
---------------------

When the cascade is well-calibrated, Tier 2 load should be roughly
constant across scale runs. If Tier 2 load spikes on a new batch:
- Possible data drift — the new data differs from gallery's coverage
- Possible classifier drift — retrain with fresh examples
- Possible guideline drift — /sl-iterate a few more rounds on the new data
