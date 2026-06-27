---
name: sl-init
description: "Initialize a subjective-labeling project through a three-way conversation (human intent + LLM knowledge + corpus). Elicits a labeling guideline from a vague seed idea — the user does NOT need to know what they want upfront. Produces: versioned guideline + gold dataset (gallery) + performance trajectory. Use when starting a new labeling project or when the researcher says /sl-init."
---

Skill: sl-init
==============

Elicit a labeling guideline from a vague seed idea through a three-way
conversation between human intuition, LLM general knowledge, and the actual
corpus. The user does NOT need to know what they want at the start.

See: skills/subjective-label/INIT.md for the full design (IPO + Evaluation).

Outputs:
  {project_dir}/
  ├── config.yaml                  topic + label schema + embedding config
  ├── .state.json                  project state machine
  ├── guideline/
  │   ├── guideline.md             current version (latest)
  │   ├── changelog.md             full history of all changes
  │   └── versions/
  │       ├── v01.md               snapshot after round 1
  │       └── ...
  ├── gallery/
  │   ├── gallery.json             gold dataset (growing)
  │   └── guideline.md             (symlink → ../guideline/guideline.md)
  ├── eval/
  │   ├── anchor_set.jsonl         fixed eval set (20-30 items, created round 2)
  │   ├── trajectory.jsonl         per-version: {version, kappa, f1, ...}
  │   └── per_version/
  │       └── v01_results.jsonl    per-item predictions
  └── cache/
      ├── embeddings/              cached vectors + FAISS index
      └── sampler/                 sampling artifacts


Protocol
--------

### Step 1. Setup

  Read: ref/ref-architecture.md, ref/ref-assets.md, ref/ref-schema.md
  Read: skills/subjective-label/INIT.md (the design doc)
  If arg provided, use as project_dir. Otherwise ask.
  Create directory scaffold (all folders above).

### Step 2. Seed — accept the vague idea

  Invoke Moderator (subagent_type: moderator, mode: "init_seed").

  Moderator asks the researcher:
    "What subjective dimension do you want to label?"
    (Accept vague answers — "empathy", "actionability", "clinical usefulness")

    "What is the PURPOSE? What decision will these labels support?"
    (This shapes granularity: paper → clean categories; intervention → thresholds)

    "Point me at your corpus."
    (Path to csv / jsonl / txt. Moderator loads and profiles: N items, length
     distribution, any metadata columns.)

  DO NOT ask for label schema yet. Labels emerge from seeing data.

  Output: config.yaml with topic, purpose, corpus_path. No labels yet.

### Step 3. Expose — show diverse examples from the corpus

  Invoke Sampler (subagent_type: sampler, mode: "init_map").
    Sampler calls Embedder to cluster the corpus (12-20 clusters).
    Picks ~30-40 items: centroid + edge from each cluster.
    Output: cache/sampler/init_map.jsonl

  Moderator presents 10-15 items to researcher (most diverse subset):
    "Here are examples from across your corpus. For each one, tell me:
     how would you label this on your dimension? Just react — there are
     no wrong answers yet."

  Collect reactions. The researcher's words ARE the draft labels.

### Step 4. Extract — turn reactions into draft guideline v01

  Moderator + LLM analyze the researcher's reactions:
    - What label categories emerged? (may be 2, 3, or more)
    - What reasoning patterns appeared? ("I said HIGH because...")
    - What dimensions matter? (intent vs words, brevity vs elaboration, etc.)

  Write:
    guideline/versions/v01.md — draft guideline from reactions
    guideline/guideline.md — copy of v01
    guideline/changelog.md — "v01: initial draft from seed reactions"
    gallery/gallery.json — the 10-15 items with researcher labels + reasoning

  Intent excavation (running underneath):
    Track patterns the researcher showed but didn't state:
    - Consistent preferences (short sentences rated higher?)
    - Hesitation patterns (which items took longer to decide?)
    - Implicit dimensions (caring about tone? formality? directness?)
    DO NOT surface yet — accumulate for Step 6.

### Step 5. Create anchor set

  From the labeled items so far, set aside a diverse subset (20-30 items) as
  the FIXED anchor set. This set never changes — it's used to compare guideline
  versions cleanly.

  Sampler picks: balanced across labels, includes boundary cases, covers
  embedding space.

  Write: eval/anchor_set.jsonl

  Run first performance measurement:
    Prompt LLM Labeler: guideline_v01 (as system prompt) → label anchor set
    Record: eval/trajectory.jsonl ← {version: "v01", kappa: X, f1: Y, ...}
    Write: eval/per_version/v01_results.jsonl

### Step 6. Challenge — find cases that break the draft

  Moderator uses strategic corpus search to find:

    BREAKING examples (classifier uncertainty or LLM pre-label disagrees
    with guideline):
      "The guideline says X, but this sentence seems to contradict that.
       How would you label it?"

    DISCOVERY examples (far from all labeled clusters):
      "Here's something unlike anything we've seen. How does it fit?"

  Surface accumulated intent observations:
    "I noticed you consistently rated short, direct sentences as HIGH.
     Is brevity part of [your dimension] for you, or coincidence?"

    "You hesitated on sentences with sarcasm. Should we add a rule for
     sarcastic [dimension], or is it just hard to read?"

    "You mentioned this is for doctor training — does that mean we should
     weight intent-to-act over emotional resonance?"

  Collect responses → update guideline → snapshot as v02.

### Step 7. Measure — evaluate guideline v02

  Prompt LLM Labeler: guideline_v02 → label anchor set
  Record in trajectory.jsonl
  Compare: did kappa improve from v01?

  Report to researcher:
    "Guideline v02 scores kappa={X} on the anchor set (v01 was {Y}).
     The change that helped most: [from changelog].
     The biggest remaining confusion: [from confusion matrix]."

### Step 8. Iterate rounds 3-N

  Repeat Steps 6-7 until convergence:

  Each round:
    a. Strategic corpus search (breaking + discovery + pre-label check)
    b. Researcher labels + resolves boundary cases
    c. Intent excavation surfaces observations
    d. Guideline updates → snapshot as vNN
    e. Prompt LLM Labeler → measure on anchor set
    f. Record in trajectory

  Convergence signals (check after each round):
    - Performance trajectory plateaus (kappa change < 0.02 for 2 rounds)
    - Changelog entries per round decreasing (< 1 rule change last round)
    - Researcher confirms: "yes, this matches what I want"

### Step 9. Init complete — report + handoff

  Report to researcher:
    "Init complete after {N} rounds, {M} human decisions.
     Guideline: v{N} (kappa = {X} on anchor set)
     Gold dataset: {K} labeled examples
     Performance trajectory: [v01: 0.35 → v02: 0.52 → ... → vN: 0.78]

     Next: /sl-iterate for panel-based refinement, or
           /sl-validate for public dataset benchmarking."

  Update .state.json:
    status: "initialized"
    iteration: 0
    guideline_version: N
    init_rounds: N
    anchor_kappa: X


Performance trajectory (the key artifact)
------------------------------------------

The trajectory across guideline versions is the proof that the process worked:

```
  kappa
  0.80 ┤                                          ●── v06
  0.75 ┤                                    ●── v05
  0.70 ┤                              ●── v03
  0.65 ┤                        ○── v04 (drop → reverted)
  0.55 ┤                  ●── v02
  0.35 ┤            ●── v01
  0.00 ┤──────┬──────┬──────┬──────┬──────┬──────┬──
       seed   r1     r2     r3     r4     r5     r6
```

If the trajectory goes up: the three-way conversation is working.
If it drops: the last change hurt → investigate + revert.
If it plateaus: the guideline has converged → ready for /sl-iterate.
