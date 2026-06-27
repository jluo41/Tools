Subjective-Label Init: Design
==============================

How a vague labeling idea becomes a deployable guideline, a validated gold
dataset, and a performance proof — with evaluation at every stage.


The Core Insight
----------------

The user does NOT know what they want at the start. The guideline cannot be
designed in the abstract. It must be ELICITED through a three-way conversation
between human intuition, LLM general knowledge, and the actual corpus.


Overview (IPO + Evaluation)
---------------------------

```
  INPUT                PROCESS              OUTPUT               EVALUATION
  ─────                ───────              ──────               ──────────

  Human Intent    ─┐                     ┌─ Guideline        ┌─ E1: Guideline
    (vague seed,   │   Three-way         │    (guideline.md   │     (clarity,
     reactions,    │   conversation      │     + changelog)   │      completeness,
     judgments,    ├─→ + intent      ──→ ├─ Gold Dataset      │      reproducibility)
     hidden prefs) │   excavation        │    (gallery.json   ├─ E2: Gold Dataset
                   │   + strategic       │     + labels       │     (coverage,
  LLM Knowledge  ─┤   corpus search     │     + reasoning)   │      balance,
    (language,     │   + disagreement    │                    │      boundary density)
     concepts,     │   analysis          └─ Performance Proof ├─ E3: System
     patterns)     │                         (kappa, F1         │     (kappa vs ceiling,
                   │                          per label)        │      per-label F1,
  Corpus          ─┘                                           │      failure analysis)
    (the texts                                                 └─ E4: Process
     to label)                                                       (convergence,
                                                                      efficiency,
                                                                      intent capture)
```


INPUT
=====

Three sources, each contributing something the others cannot:

```
  Source             Contributes                Cannot provide
  ──────             ────────────               ──────────────
  Human Intent       Judgment, purpose,         Scale, consistency,
                     "what matters to me"       exhaustive sampling

  LLM Knowledge      Concept vocabulary,        User's actual intent,
                     dimension proposals,       corpus-specific patterns
                     pattern naming

  Corpus             The actual texts,          Labels, rules,
                     real diversity,            what "matters"
                     edge cases that exist
                     in THIS data
```

The system mediates between all three. None alone can produce the guideline.


PROCESS
=======

Two layers running simultaneously:

### Surface layer: Three-way conversation

```
  Seed  →  Expose  →  React  →  Extract  →  Challenge  →  Refine
    │         │          │          │            │            │
    │         │          │          │            │            │
  User      System     User      LLM turns    System       User
  gives     samples    labels    reactions    searches     resolves
  vague     diverse    examples  into draft   corpus for   boundary
  idea      examples   + explains rules       cases that   cases,
            from       WHY                    BREAK the    guideline
            corpus                            draft rules  updates
                                    │
                                    ↓
                              Loop until guideline stabilizes
```

### Underneath: Intent excavation (always on)

The LLM accumulates observations about the user and surfaces them at natural
breakpoints (after a batch of 5-10 labels, or when a pattern emerges):

```
  Signal type          Example                         Action
  ───────────          ───────                         ──────
  Hidden intention     User labels for "empathy" but   "What will you DO with
                       real goal is doctor training     these labels? That might
                                                       change what we measure."

  Hidden preference    User consistently rates short   "You've rated short
                       sentences higher than long       sentences higher 7 out
                       ones — unstated pattern          of 8 times. Is brevity
                                                       part of empathy for you?"

  Hidden boundary      User hesitates, hedges,         "You hesitated on this
                       changes answer — signals         one. What made it hard?
                       the guideline's weak spot        Should we split this
                                                       category?"
```

### Corpus search strategy

The system actively mines the corpus. Not random sampling — strategic:

```
  Search mode          Purpose                         When
  ───────────          ───────                         ────
  Diverse sample       Cover the spread of what        Early (first 2 rounds)
                       exists in the data

  Confirming           Validate current rules          After each rule addition
                       ("find more like this")

  Breaking             Challenge current rules         After guideline stabilizes
                       ("find cases that don't fit")   within a round

  Discovery            Surface patterns not yet        Periodically
                       encountered ("find unlike
                       anything we've seen")
```


OUTPUT
======

Three artifacts. Each validates the others — none is meaningful alone.

### Output 1: Guideline (guideline.md + changelog.md)

The labeling rules, built bottom-up from evidence.

```
guideline.md
  - Label definitions (emerged from conversation, not imposed)
  - Decision rules (each tied to specific examples that motivated it)
  - Boundary cases (explicitly addressed, not left ambiguous)
  - When-in-doubt defaults

changelog.md
  - Dated entries: which rule changed, what example triggered it, why
  - The user's reasoning in their own words
  - Shows how the guideline evolved from vague seed to precise spec
  - IS the provenance chain: for any rule, trace back to the moment
    and example that created it
```

### Output 2: Gold Dataset (gallery.json)

Human-validated labeled examples that emerged from the process.

```
gallery.json
  Per example:
  - text: the actual sentence
  - label: the human-assigned label
  - reasoning: WHY this label (in the user's words)
  - rule_applied: which guideline rule governs this case
  - iteration: when this was labeled
  - difficulty: easy | boundary | hard (from hesitation signal)
  - changelog_ref: link to the changelog entry if this example
    triggered a rule change
```

### Output 3: Performance Proof

The guideline used as an LLM prompt to label the gold dataset.

```
  Guideline (as system prompt)
      +
  LLM
      ↓
  Label each example in gold dataset
      ↓
  Compare LLM labels vs human labels
      ↓
  Agreement metrics (kappa, F1, per-label P/R)

  If kappa >= human ceiling → READY to scale
  If kappa < threshold      → BACK to process
```


EVALUATION
==========

Four evaluation blocks. E1-E3 evaluate the three outputs. E4 evaluates the
process itself.

### E1: Guideline Evaluation

Does the guideline clearly and completely capture the user's intent?

```
  Dimension              How to measure                Pass
  ─────────              ──────────────                ────
  Clarity                Give guideline to LLM         LLM can label without
                         without examples — can         asking clarifying
                         it label unambiguously?        questions

  Completeness           Check gold dataset for         Every example in gold
                         examples not covered by        dataset is covered by
                         any rule                       at least one rule

  Reproducibility        Give guideline to a            Second LLM's labels
                         DIFFERENT LLM (or same         agree with first LLM
                         LLM, different run) —          (kappa > 0.8)
                         same labels?

  Stability              Remove one rule at a time      Removing any rule
                         — does performance drop?       causes measurable
                         (ablation)                     performance drop
                                                       (no dead rules)

  Conciseness            Count rules vs gold dataset    No redundant rules
                         size — is the guideline        (no two rules that
                         as simple as possible?         always fire together)
```

### E2: Gold Dataset Evaluation

Is the gold dataset representative, balanced, and dense at the boundaries?

```
  Dimension              How to measure                Pass
  ─────────              ──────────────                ────
  Coverage               Embed gold dataset +          Gold examples are
                         full corpus — do gold          spread across the
                         examples cover the             embedding space, not
                         embedding space?               clustered in one region

  Balance                Label distribution in          No label < 10% of
                         gold dataset                   gold dataset (unless
                                                       the corpus is genuinely
                                                       imbalanced — then match
                                                       corpus distribution)

  Boundary density       Proportion of gold             >= 20% of gold dataset
                         examples marked                is boundary/hard cases
                         "boundary" or "hard"           (these are what make
                                                       the guideline precise)

  Size sufficiency       Performance on gold            Performance stabilizes
                         dataset as function of         before gold dataset is
                         gold dataset size              exhausted (learning
                         (learning curve)               curve plateaus)
```

### E3: System Evaluation (Guideline + LLM vs Gold Dataset)

Can the guideline, used as an LLM prompt, reproduce the human labels?

```
  Dimension              How to measure                Pass
  ─────────              ──────────────                ────
  Overall agreement      Cohen's kappa between         kappa >= human inter-
                         LLM labels and gold           annotator ceiling
                         labels                        (from public dataset
                                                       benchmark if available)

  Per-label quality      Precision / recall / F1       No label below F1 = 0.6
                         for each label category       (if one label is weak,
                                                       the guideline is unclear
                                                       for that category)

  Failure analysis       Confusion matrix —            Failures cluster at
                         where does the LLM            known boundary cases,
                         disagree with gold?           not at "easy" examples
                                                       (easy failures = bad
                                                       guideline)

  Difficulty curve       Accuracy on easy vs           Easy >= 0.95
                         boundary vs hard              Boundary >= 0.70
                         examples separately           Hard >= 0.50
                                                       (graceful degradation)

  Cross-LLM stability   Same guideline, different     kappa between LLMs
                         LLMs (GPT-4, Claude,          > 0.75 (the guideline
                         Gemini) — same labels?        is LLM-agnostic)

  Public benchmark       If a public dataset with      Agent kappa >= human
  (optional)             human kappa ceiling            kappa ceiling on the
                         exists for this domain         public dataset
```

### E4: Process Evaluation

Did the init process itself work well? (Meta-eval — evaluates the method.)

```
  Dimension              How to measure                Pass
  ─────────              ──────────────                ────
  Convergence            Changelog entry frequency     Entries per round
                         over rounds — is the          decreasing; last 2
                         guideline stabilizing?        rounds have <= 1 change

  Efficiency             Number of human decisions     Guideline converges
                         to reach convergence          in <= 60 decisions
                                                       (3-6 iterations ×
                                                       5-10 decisions each)

  Intent capture         Ask the user: "does this      User confirms without
                         guideline match what you      major revisions
                         wanted?" (explicit check)

  Discovery rate         New labels / categories       Most categories emerge
                         discovered during process     by iteration 3; none
                         vs imposed at seed            after iteration 5

  Excavation yield       Hidden intentions /           At least 1 hidden
                         preferences surfaced          intention surfaced
                         during the process            that changed the
                                                       guideline
```


TOOLS (how the agent communicates with the corpus)
=====

The agent needs concrete tools to make the three-way conversation evidence-based.
These form a zoom hierarchy — cheap/broad at the top, expensive/focused at the
bottom:

```
  Layer              Tool                     Purpose
  ─────              ────                     ───────

  STORAGE
    corpus loader    Read raw texts            csv / jsonl / txt → internal format
    gallery.json     Store labeled examples    Human-validated labels + reasoning
    guideline.md     Store current rules       Versioned, with changelog

  GEOMETRY (cheap, covers whole corpus)
    embedder embed   Vectorize sentences       Represent as dense vectors
    embedder index   Build FAISS index         Fast similarity search
    embedder cluster Find natural groups       Discover corpus structure
    embedder nearest "More like this"          Find similar to a labeled example
    embedder stratify Diverse sample           Cover all clusters

  CLASSIFICATION (mid-cost, focuses on uncertain regions)
    classifier train Train small model         On growing gallery
    classifier uncertainty Find hard cases     Near decision boundary
    classifier hard_mining Active learning     Top-k hardest unlabeled items

  LLM JUDGMENT (expensive, focuses on hardest cases)
    guideline-as-prompt Pre-label batch        Current guideline → LLM → labels
    persona panel    Multiple perspectives     3-5 personas label in parallel
    intent excavation Surface hidden prefs     Observe user patterns, ask at
                                               breakpoints

  ORCHESTRATION
    sampler          Stage-aware sampling      Combines geometry + classification
                     (init_map mode for init)  to pick the right examples
```

### Corpus search strategies (used during PROCESS)

```
  Strategy           When                     How
  ────────           ────                     ───
  Diverse sample     Early rounds (1-2)       embedder cluster + stratify
                                              → representatives from each cluster

  Confirming         After a rule addition    embedder nearest
                                              → "find more like the ones user
                                                 labeled HIGH"

  Breaking           After guideline          classifier uncertainty
                     stabilizes in a round    → items near decision boundary
                                              → "find cases that don't fit"

  Discovery          Periodically             embedder cluster
                                              → items far from ALL labeled
                                                clusters → "find unlike
                                                anything we've seen"

  Pre-label check    After each guideline     guideline-as-prompt → LLM labels
                     version                  batch → compare vs user labels
                                              → find disagreements
```

### The zoom hierarchy in action

```
  Whole corpus (100K sentences)
      │
      │  embedder: cluster + stratify (cheap, broad)
      ▼
  Diverse sample (~40 sentences)
      │
      │  user labels + LLM pre-labels (mid-cost)
      ▼
  Disagreements (~10 sentences)
      │
      │  user resolves → guideline updates (expensive, focused)
      ▼
  Next round: classifier finds new uncertain region
      │
      │  repeat
      ▼
  Convergence
```


GUIDELINE VERSIONING + PERFORMANCE TRAJECTORY
==============================================

The guideline evolves through versions. Each version is a checkpoint that can be
evaluated. The performance trajectory across versions IS the evidence that the
process is working.

### Guideline as model checkpoint

```
  Version   Change (from changelog)              Eval set    Kappa
  ───────   ───────────────────────              ────────    ─────
  v1        Seed: "label empathy"                anchor-20   0.35
  v2        Added: "intent matters, not words"   anchor-20   0.52
  v3        Added: "sarcasm + empathy words      anchor-20   0.68
                    = LOW"
  v4        Split: cognitive vs affective         anchor-20   0.61 ← dropped
  v5        Reverted split, added boundary        anchor-20   0.74
            examples
  v6        Added: "brief acknowledgment          anchor-20   0.78
                    without follow-up = LOW"
```

### What the trajectory tells you

```
  Trajectory shape       Meaning                     Action
  ────────────────       ───────                     ──────
  Monotonically up       Process is working           Keep going
  Plateau                Guideline has converged      Ready for /sl-validate
  Drop after a change    That change hurt             Revert or investigate
  Oscillating            Rules contradict each other  Step back, simplify
```

### Per-change attribution

The changelog maps versions to specific rule changes. Combined with the
performance trajectory, you get ablation for free:

```
  "Which rule caused the biggest jump?"
  → v1→v2: +0.17 (intent vs words distinction)

  "Which rule actually hurt?"
  → v3→v4: -0.07 (cognitive/affective split was premature)

  "Which rule had no effect?"
  → check: any version where kappa didn't change → that rule
    may be redundant (or the anchor set doesn't test it)
```

### Anchor set vs full gold set

Two evaluation sets, serving different purposes:

```
  Set              When created         Size     Changes?    Purpose
  ───              ────────────         ────     ────────    ───────
  Anchor set       Early in init        20-30    FIXED       Clean version-to-
                   (round 1-2),                  (never      version comparison.
                   human-labeled,                 grows)     Same test for every
                   diverse sample                            guideline version.

  Gold dataset     Grows throughout     20→200+  GROWS       Absolute quality
  (gallery.json)   the process,                  (every      measurement. Full
                   human-validated                round)     coverage of what the
                                                            guideline handles.
```

Why both?
  - Anchor set answers: "is this version BETTER than the last one?" (fixed test)
  - Gold dataset answers: "is this version GOOD ENOUGH overall?" (full test)
  - If you only use the gold set, you can't tell whether improvement came from
    a better guideline or a changed eval set.

### The Prompt LLM Labeler

The tool that turns each guideline version into a measurable prediction:

```
  guideline_vN.md (as system prompt)
      +
  LLM (Claude / GPT-4 / etc.)
      +
  eval set (anchor or gold)
      ↓
  predicted labels
      ↓
  compare vs human labels
      ↓
  kappa, F1, per-label P/R, confusion matrix
```

This runs DURING the process, not just at the end. After each guideline update:
  1. Snapshot the guideline as guideline_vN.md
  2. Run Prompt LLM Labeler on the anchor set
  3. Record performance in the trajectory
  4. If performance dropped → flag to user before continuing

The prompt itself can vary (an experiment within the experiment):

```
  Prompt style     Contents                          When to use
  ────────────     ────────                          ───────────
  Rules only       guideline rules, no examples      Test if rules alone
                                                     are sufficient

  Rules + examples guideline rules + gallery         Test if examples help
                   examples (few-shot)                (usually yes)

  Rules + examples guideline rules + examples +      Test if reasoning
  + reasoning      the reasoning from changelog       context helps
                   ("we added this rule because...")   (for hard cases)
```

### Versioning artifacts

```
  {project_dir}/
  ├── guideline/
  │   ├── guideline.md           ← CURRENT version (symlink or copy)
  │   ├── changelog.md           ← full history of all changes
  │   └── versions/
  │       ├── v01.md             ← snapshot after round 1
  │       ├── v02.md             ← snapshot after round 2
  │       └── ...
  ├── eval/
  │   ├── anchor_set.jsonl       ← fixed eval set (created early)
  │   ├── trajectory.jsonl       ← per-version: {version, kappa, f1, ...}
  │   └── per_version/
  │       ├── v01_results.jsonl  ← per-item predictions for v01
  │       ├── v02_results.jsonl
  │       └── ...
  └── gallery/
      └── gallery.json           ← growing gold dataset
```


The Full Picture

```
  ┌─────────┐   ┌──────────┐   ┌──────────┐   ┌──────────────────────────┐
  │  INPUT   │──→│ PROCESS  │──→│ OUTPUT   │──→│ EVALUATION               │
  │          │   │          │   │          │   │                          │
  │ Human    │   │ 3-way    │   │ Guide-   │   │ E1: Is the guideline    │
  │ Intent   │   │ conver-  │   │ line     │──→│     clear, complete,    │
  │          │   │ sation   │   │          │   │     reproducible?       │
  │ LLM      │   │          │   │ Gold     │   │                          │
  │ Knowledge│   │ Intent   │   │ Dataset  │──→│ E2: Is the gold dataset │
  │          │   │ excav-   │   │          │   │     representative,     │
  │ Corpus   │   │ ation    │   │ Perf.    │   │     balanced, boundary- │
  │          │   │          │   │ Proof    │──→│     dense?              │
  │          │   │ Strategic│   │          │   │                          │
  │          │   │ corpus   │   │          │   │ E3: Does guideline+LLM  │
  │          │   │ search   │   │          │   │     reproduce gold      │
  │          │   │          │   │          │   │     labels? (kappa, F1) │
  │          │   │          │──────────────│──→│                          │
  │          │   │          │   │          │   │ E4: Did the process     │
  │          │   │          │   │          │   │     converge? Was it    │
  │          │   │          │   │          │   │     efficient? Did it   │
  │          │   │          │   │          │   │     capture intent?     │
  └─────────┘   └──────────┘   └──────────┘   └──────────────────────────┘
                                                        │
                                                        ↓
                                                  ALL PASS → /sl-scale
                                                  ANY FAIL → back to PROCESS
```


Exit Condition
--------------

Init is complete when ALL FOUR evaluations pass:
  E1: Guideline is clear, complete, reproducible, stable, concise
  E2: Gold dataset covers the corpus, is balanced, has boundary density
  E3: Guideline + LLM reproduces gold labels at or above human ceiling
  E4: Process converged efficiently, user confirms intent was captured

Then: /sl-iterate (for further refinement) or /sl-scale (for full corpus).
