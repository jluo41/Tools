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
  ├── config.yaml                  task + construct + objective + labels (see ref/ref-config.md)
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
  Read: ref/ref-output-style.md (BINDING output contract — all files must be
    scannable in one glance; render a .md twin for every human-read artifact)
  If arg provided, use as project_dir. Otherwise ask.
  Create directory scaffold (all folders above).

### Step 2. Seed — accept the vague idea

  Invoke Moderator (subagent_type: moderator-agent, mode: "init_seed").

  Moderator asks the researcher:
    "What subjective dimension do you want to label?"
    (Accept vague answers — "empathy", "actionability", "clinical usefulness")

    "What is the OBJECTIVE? What decision/metric will select a good labeling?"
    (This is the one irreducible human input — it lets the construct be
     auto-refined/selected later. kind = discriminance | downstream | dataset_match.
     See objective in ref/ref-config.md.)

    "Point me at your corpus."
    (Path to csv / jsonl / txt. Moderator loads and profiles: N items, length
     distribution, any metadata columns.)

  DO NOT ask for label schema yet. Labels emerge from seeing data.

  Output: config.yaml per ref/ref-config.md — fill `task`, `construct`
  {name, mode, discriminant_from}, and `objective`; `labels.values: null`
  (elicited later). Nothing physician/construct-specific is hardcoded.

### Step 2b. Construct mode — auto-select vs human seed

  `construct.mode` in config decides how v01 is born (see ref/ref-config.md):

  mode: seed  — a human one-liner defines the construct → proceed to the normal
                Expose → React → Extract path (Steps 3–4).

  mode: auto  — the construct is SELECTED against `objective`, not hand-defined:
    1. Expose the representative sample (Step 3).
    2. Multi-LLM PROPOSE N candidate operational definitions (each = a short
       guideline draft + label schema) from `construct.name` + `discriminant_from`.
       Diverse framings, not consensus (consensus = generic textbook meaning).
    3. Each candidate labels the sample via `lib/label.py`; also label the sample
       with the sibling constructs' guidelines (`discriminant_from`) for scoring.
    4. `lib/construct.py score --objective <kind>` → ranks candidates and picks
       the winner (discriminance × informativeness; degenerate/redundant → 0),
       and returns `divergence_top` = the items candidates most disagree on.
    5. Winner's guideline becomes v01; `divergence_top` are the first ambiguities
       to pin down (surfaced to the human, or resolved by the objective).

  objective.kind: discriminance works now (no external data); downstream needs the
  target regression (PHI-gated); dataset_match needs a public set. The objective is
  the one irreducible human input — everything after it is automated.

### Step 3. Expose — show diverse examples from the corpus

  Invoke Sampler (subagent_type: sampler-agent, mode: "init_map").
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

### Step 5. Create the three eval sets (distinct jobs — never merge)

  Per ref/ref-config.md `eval` + note-update.md Part 5, THREE sets, each with one job:

  | set | size | changes? | job |
  |-----|------|----------|-----|
  | **fixed anchor** | ≥100, `representative` (base-rate-aware, incl. NONE quota) | FROZEN | version-to-version comparison (correctness) |
  | **fresh held-out** | ~50, `representative` | new draw each round, NEVER trained on | honest generalization + anti-circular (F8) |
  | **rolling batch** | 20–30 | new each round | active-learning refinement ONLY — NOT an eval set (F7) |

  Sampler draws anchor + held-out from the `representative` pool (Step S5/lib/sample.py:
  base-rate + NONE quota), balanced across labels, boundary-dense.
  Write: eval/anchor_set.jsonl · eval/heldout.jsonl

  Run first measurement (via lib/label.py + lib/kappa.py):
    label v01 on anchor AND held-out → record correctness (κ vs gold), reliability
    (panel κ), clarity (executor-independence) into eval/trajectory.jsonl +
    heldout_kappa; render eval/trajectory.md (ref/ref-output-style.md).

  Anchor κ alone is optimistic — the held-out gap is what catches over-fit.

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

  Convergence (run `lib/converge.py --project-dir <task>` after each round — F8):
    CONVERGED only when ALL hold —
    - anchor κ plateaus (Δ < anchor_plateau for 2 rounds), AND
    - **held-out gap ≤ heldout_gap_max** (anchor − held-out; a big gap = OVERFIT,
      NOT converged — this is the B03 0.93/0.67 trap the gate catches), AND
    - objective_score plateaus (if tracked), AND
    - researcher confirms "yes, this matches what I want".
    A plateau with no held-out returns CONVERGED_NO_HELDOUT (⚠ gap unchecked) — do
    NOT treat as done. Changelog entries per round should also be decreasing.

### Step 9. Init complete — report + handoff

  Report to researcher:
    "Init complete after {N} rounds, {M} human decisions.
     Guideline: v{N} (kappa = {X} on anchor set)
     Gold dataset: {K} labeled examples
     Performance trajectory: [v01: 0.35 → v02: 0.52 → ... → vN: 0.78]

     Next: /sl-iterate for panel-based refinement, or
           /sl-validate for public dataset benchmarking."

  Write REPORT.md: one-page project dashboard, ≤15 lines (ref/ref-output-style.md).

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
