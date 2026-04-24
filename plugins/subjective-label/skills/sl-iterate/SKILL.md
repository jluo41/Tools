---
name: sl-iterate
description: "Run one full iteration of the subjective-label loop: Boundary Prober picks a batch, Labeler Panel (3-5 persona agents) labels in parallel, Disagreement Analyzer categorizes disagreements, Moderator surfaces hard cases to the researcher for adjudication, Gallery Keeper updates. Use when the researcher says /sl-iterate or wants to advance the labeling loop."
---

Skill: sl-iterate
=================

Main workhorse. Run N times until κ converges on validate.

Protocol
--------

Step 1. Load context.
  Read: ref/ref-architecture.md, ref/ref-assets.md
  Read {project_dir}/.state.json, config.yaml, gallery/guideline.md, gallery/gallery.json
  If .state.json missing: tell researcher to run /sl-init first. Stop.

Step 2. Invoke Moderator (subagent_type: moderator).
  Pass:
    mode: "iterate"
    project_dir: <path>
    iteration: <state.iteration + 1>

  Moderator runs the iteration in 6 steps:

    (a) Sampler (subagent_type: sampler, mode=iterate_batch) calls
        embedder (cluster + nearest) and classifier (uncertainty, if a
        classifier exists from a prior iteration) to produce a candidate
        pool of ~100 items scored by novelty + uncertainty + cluster
        coverage. Outputs: candidate_pool.jsonl.

        Boundary Prober (subagent_type: prober) then applies LLM judgment
        on the candidate pool to pick the final 20-30 items. Outputs:
        batch.jsonl.

    (b) Labeler Panel (subagent_type: labeler-panel) reads
        personas/ directory, picks 3-5 personas matching the topic,
        spawns each persona as a labeling pass. Each persona labels
        all items in batch.jsonl with reasoning. Outputs: panel_labels.jsonl
        (one row per {item, persona} pair).

    (c) Disagreement Analyzer (subagent_type: disagreement-analyzer)
        reads panel_labels.jsonl. For each item where personas
        disagreed, categorizes:
           A = boundary case (genuine subjective edge)
           B = rule ambiguity (guideline underspecifies)
           C = novel pattern (label schema gap)
           D = noise (one persona misread)
        Outputs: disagreements.md with counts per category.

    (d) Moderator decides what to escalate to researcher:
           A → show 3-5 boundary items, ask "which label? why?"
           B → show the ambiguous rule + conflicting examples, ask to refine
           C → show the novel pattern, ask "new label? or existing?"
           D → do not surface (auto-resolved via majority vote)

    (e) Gallery Keeper (subagent_type: gallery-keeper) writes the
        researcher's decisions into gallery.json (new entries) and
        guideline.md (new rules / tie-breakers). Bumps
        .state.json.iteration and writes a diff log under gallery/history/.

    (f) Classifier (subagent_type: classifier, mode=train) retrains the
        small model on the updated gallery + confirmed panel labels.
        Outputs model + CV F1 to cache/classifier/iter_N/.
        If CV F1 dropped > 0.05 from prior iteration, flag possible drift
        to Moderator, who surfaces to researcher.

        Then invokes embedder to rebuild the gallery FAISS index so the
        next Tier 0 / Sampler runs pick up the new entries.

Step 3. Report to researcher.
  Summary:
    - Items labeled this iteration: N
    - Panel-internal κ: {value}
    - Disagreement breakdown: A=X, B=Y, C=Z, D=W
    - Gallery size: before -> after
    - Suggested next step: /sl-iterate again, OR /sl-validate if panel-κ > 0.6
