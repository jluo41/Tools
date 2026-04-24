Reference: Stage Hierarchy
===========================

The plugin operates at three nested loop scales. Understanding which loop
a piece of logic belongs to is the cleanest way to navigate the code.


The three loops
---------------

```
┌──────────────────────────────────────────────────────────────┐
│ BIG LOOP — Project lifecycle                                 │
│                                                              │
│   /sl-init  →  /sl-iterate × N  →  /sl-validate  →  /sl-scale│
│                      ▲                    │                  │
│                      │    STALLED         │                  │
│                      └────────────────────┘                  │
│                                                              │
│   Cadence:  once per project, total ~3-6 iterations          │
│   Actors:   all agents                                       │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ MEDIUM LOOP — Single iteration of /sl-iterate                │
│                                                              │
│   Sampler (iterate_batch) → Prober → Labeler Panel           │
│     → Disagreement Analyzer → Moderator (talk to researcher) │
│     → Gallery Keeper → Classifier.train                      │
│                                                              │
│   Cadence:  3-6 times per project                            │
│   Actors:   sampler, prober, labeler-panel, analyzer,        │
│             moderator, gallery-keeper, classifier            │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ SMALL LOOP — Classifier cascade inside /sl-scale             │
│                                                              │
│   For each corpus item:                                      │
│     Tier 0: Embedder k-NN   → if unanimous + sim high: done │
│     Tier 1: Classifier pred → if margin + prob high: done   │
│     Tier 2: LLM Panel       → majority vote (expensive)     │
│                                                              │
│   Cadence:  millions of times per /sl-scale run              │
│   Actors:   embedder, classifier, labeler-panel (tier 2)     │
└──────────────────────────────────────────────────────────────┘
```


Why three loops?
----------------

Each loop has a different unit of work and a different cost profile:

| Loop   | Unit of work                | Cost per unit           | Frequency    |
|--------|------------------------------|-------------------------|--------------|
| BIG    | Full project convergence     | hours (researcher time) | 1            |
| MEDIUM | One iteration (~20-30 items) | 10-30 min + $1-3 LLM    | 3-6          |
| SMALL  | One labeled item at scale    | milliseconds or seconds | 100K-10M     |

Separating these lets us optimize the right thing at the right level:
- BIG loop: minimize researcher-decision count (via the Analyzer's A/B/C/D filter)
- MEDIUM loop: maximize information-per-iteration (via Sampler's hard-mining)
- SMALL loop: minimize cost-per-item (via the 3-tier cascade)


Sampling appears at every loop
-------------------------------

Sampling is the common primitive. It shows up at each scale:

| Stage | Sampler mode | What's sampled | Purpose |
|-------|--------------|----------------|---------|
| /sl-init | `init_map` | full sample pool | Show researcher the data distribution |
| /sl-iterate | `iterate_batch` | sample pool minus gallery | Hard-example mining |
| /sl-validate | `validate_heldout` | public dataset held-out | Balanced benchmarking |
| /sl-scale pre-flight | `scale_preflight` | full corpus | Estimate cascade distribution + cost |
| any time | `diagnostic` | recent activity | "where are we?" snapshot |

All five modes live in `agents/sampler.md` and share the same two primitives
underneath: `embedder cluster` + (optional) `classifier uncertainty`.


Classifier appears in two loops
--------------------------------

The classifier is trained in the MEDIUM loop (at the end of each iteration)
and consumed in both the MEDIUM loop (next iteration's Sampler) and the
SMALL loop (Tier 1 of /sl-scale cascade). This is the classic
active-learning pattern:

```
   end of iter N       train classifier on gallery
          │
          ▼
   start of iter N+1   Sampler uses classifier uncertainty for hard mining
          │
          ▼
   /sl-scale           Tier 1 uses classifier to label easy-medium items
```

As iterations progress, the classifier gets better → Sampler mines harder
cases → panel is used more efficiently. When the classifier's CV F1
plateaus, the BIG loop is approaching convergence.


Cold start
----------

The very first /sl-iterate has no trained classifier yet. In this state:
- Sampler falls back to `novelty-only` (embedding distance from an empty /
  tiny gallery + cluster coverage).
- The panel labels ~20 items.
- Gallery Keeper writes them; Classifier trains on the initial ~20 labels.
- From iteration 2 onward, the full hard-mining strategy kicks in.

This mirrors standard active-learning cold-start practice: random/diversity
sampling until a model is trainable, then switch to uncertainty sampling.


What writes / what reads
------------------------

Only three agents WRITE canonical artifacts:
- Gallery Keeper → `gallery/`
- Classifier → `cache/classifier/iter_N/`
- Validator → `validation/`

Everything else READS those artifacts and produces intermediate outputs
under `iterations/iter_N/` or `cache/`. This makes the artifact graph a
clean DAG and makes audit straightforward.
