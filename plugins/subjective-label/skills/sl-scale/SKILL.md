---
name: sl-scale
description: "After the gallery has converged (via /sl-validate), batch-label the full dataset using the Labeler Panel or a single strong labeler + gallery few-shot. Handles large corpora (100K-10M items) with cost-aware routing. Use when the researcher says /sl-scale or wants to deploy the converged guideline."
---

Skill: sl-scale
===============

Final step. Use the converged gallery to label at scale. Assumes /sl-validate
reported CONVERGED or near-ceiling κ.

Protocol
--------

Step 1. Load context.
  Read: ref/ref-cascade.md, ref/ref-architecture.md, ref/ref-assets.md
  Read {project_dir}/.state.json, validation/trajectory.jsonl
  If latest κ gap > 0.1: warn researcher, ask to confirm before scaling.

Step 2. Ask researcher for scale config.
  - Input data path (jsonl with {id, text})
  - Routing mode:
      "single"   — one strong labeler + gallery (cheapest, fastest, no tiers)
      "panel"    — full 3-5 persona panel per item (most consistent, 3-5x cost)
      "cascade"  — 3-tier: embedder k-NN → trained classifier → LLM panel
        (RECOMMENDED for large corpora)
  - Output path
  - Concurrency (default 8 parallel)
  - Optional: classifier backend override for this run (e.g. use SetFit
    instead of logreg for higher-quality Tier 1)

Step 3. Pre-flight (cascade mode).
  Invoke Sampler (mode=scale_preflight) to sample 500 items.
  Run the 3-tier cascade on the sample.
  Extrapolate tier distribution + cost for the full run.
  Report to researcher:
    "Pre-flight on 500 items:
       Tier 0: 62% ($0.003)
       Tier 1: 26% ($0.30)
       Tier 2: 12% ($8.40)
     Projected full run (N items):
       Total cost: $X
       Duration:   Y minutes at concurrency=8
     Proceed? (y/n)"

Step 4. Invoke Labeler Panel in scale mode with routing=cascade.

  For each corpus item:
    Tier 0: embedder.nearest(item, gallery_index, k=5)
            → if top-5 unanimous and avg_sim >= cascade_inherit_sim: inherit.
            → method: "cascade-tier0"

    Tier 1: classifier.predict(item)  [uses latest trained model]
            → if margin >= accept_margin and prob >= accept_prob: use classifier label
            → method: "cascade-tier1"

    Tier 2: labeler-panel.label(item, personas=config.panel.personas)
            → majority vote with support >= 0.6: use majority
            → support < 0.6: queue to human_review_queue.jsonl
            → method: "cascade-tier2"

Step 4. Write outputs.
  {project_dir}/output/annotations.jsonl         final labels
  {project_dir}/output/human_review_queue.jsonl  flagged for researcher
  {project_dir}/output/scale_report.md           stats + cost

Step 5. Report to researcher.
  "Scaled N items in T minutes. Estimated cost: $X.
   High-confidence: A%. Panel-resolved: B%. Flagged for review: C%.
   Output: {path}. Review queue: {path} ({C} items)."


Notes
-----

- scale does NOT update the gallery. If researcher wants the flagged items
  to improve the gallery, they should review them and run /sl-iterate with
  those items as the batch.
- For 1M+ items, strongly recommend routing=cascade with a Haiku-tier model
  for the fast path.
