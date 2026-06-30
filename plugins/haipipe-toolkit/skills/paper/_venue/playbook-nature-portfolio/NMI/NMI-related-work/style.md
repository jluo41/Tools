# NMI Related Work -- Section Style Guide

Extracted from 8 Nature Machine Intelligence exemplar papers. Supplements `style-profile.md`.

## The core rule: NMI has NO separate Related Work section

None of the 8 exemplar papers contain a standalone "Related Work", "Literature Review", "Background", or "Prior Work" section. This is a firm Nature-family convention. All prior-work positioning is distributed across two locations:

1. **Introduction** (primary): background paragraphs that survey existing approaches and identify the gap
2. **Discussion** (secondary): positioning against specific prior methods when comparing results

Some papers defer extended literature review to the **Supplementary Information**.

## How related work is embedded in the Introduction

### The gap-identification pattern

Prior work in the Introduction serves one purpose: to identify the gap that this paper fills. Each existing approach is characterized in 1-3 clauses, immediately followed by its limitation. The pattern is:

```
[Approach category] has been proposed [refs].
  However, [approach] [limitation].
  -> (repeat for 2-3 approach categories)
  -> Gap statement: "...remains underexplored / unexplored / challenging."
```

### Organization: by approach type, not chronologically

Related work in the Introduction is organized by method category, not by publication date. Each paragraph covers one approach cluster:

| Paper | Approach categories surveyed | Gap statement |
|-------|------------------------------|--------------|
| qiao-2025 | Discriminative models -> Generative models (general) -> Cardiac generative models | "their application to personalized normative modelling...remains underexplored" |
| gu-2026 | Standard cardiac sensing -> Channel-dependent CNNs -> Existing foundation models (12-lead only) | "existing foundation models are predominantly...largely confined to standard 12-lead" |
| chen-w-2025 | Univariate interpretable ML -> Interaction discovery methods -> FDR control gaps | "no existing method provides error-controlled interaction discovery" |
| mon-williams-2025 | RL/imitation learning -> LLM-based robotics -> RAG gap | RAG for robotics unexplored |
| mataraso-2025 | Early/intermediate/late fusion -> EHR-omics integration challenges | "late fusion approaches struggle to learn cross-modal interactions" |
| serapio-garcia-2025 | LLM personality measurement attempts -> Construct validity gaps | "so far, no work has addressed how to systematically measure and psychometrically validate" |
| pontikos-2025 | IRD genetics -> Imaging modalities -> Limited AI application | "wider access to this expertise could be deployed via an AI system" |
| doerig-2025 | Object recognition in visual cortex -> Scene-level information gap -> LLMs as bridge | "a quantitative approach...has remained elusive" |

### Reference density in Introduction

References are densely clustered in background paragraphs, sparse in the contribution paragraph:

| Paper | Total intro refs | Background paragraphs | Contribution paragraph |
|-------|-----------------|----------------------|----------------------|
| serapio-garcia-2025 | ~35 | 30+ | 2-3 |
| qiao-2025 | ~43 | ~38 | ~3 |
| gu-2026 | ~16 | ~14 | ~2 |
| chen-w-2025 | ~24 | ~22 | ~2 |
| mon-williams-2025 | ~53 | ~50 | ~3 |
| doerig-2025 | ~45 | ~42 | ~3 |

### Brevity of individual work descriptions

Prior works are cited but not reviewed in depth. Each gets at most 1-2 clauses:

- "Xia et al. proposed a method that integrates statistical shape priors with deep learning for four-chamber cardiac shape reconstruction from images" [qiao-2025] -- one clause, then move on
- "efforts have been made to extend interpretable ML methods to discover interactions among features" [chen-w-2025] -- category-level, not per-paper
- Prior works are cited as evidence of a trend, not individually analyzed

## How related work appears in Discussion

The Discussion contains a secondary positioning layer where this paper's results are compared directly against prior methods:

- "So far, only four previous studies have tried to apply AI to IRDs, all in much smaller datasets of fewer than 150 patients and across substantially fewer genes." [pontikos-2025]
- "Our approach based on LLM embeddings should not be seen as a competitor to these lines of work, but rather as synergistic." [doerig-2025]
- "The only published exploration of personality and psychodemographics in LLMs..." [serapio-garcia-2025] (this comparison also appears within a Results subsection)

This is positioning-by-contrast: the prior work is characterized by its dataset, scope, or capability, and this paper's advantage is stated implicitly.

## How related work appears in Results

Some papers embed a mini-related-work subsection within Results for direct head-to-head comparisons:

- "Eye2Gene predictions outperform other AI approaches" [pontikos-2025] -- a Results subsection that names and compares against 4 prior methods
- "Diamond overview" [chen-w-2025] -- opens Results with a conceptual positioning against existing interaction-discovery methods

This is the NMI convention for detailed method comparison: it belongs where the evidence is (Results), not in a standalone literature review.

## Supplement as extended literature review

When the related work is extensive, papers defer to supplementary material:

- "we further detail related work in Supplementary Note A.2" [serapio-garcia-2025]
- "Supplementary Section 1 provides more background on state-of-the-art approaches and their current limitations" [mon-williams-2025]

This allows the main text to stay concise while providing comprehensive literature coverage for specialist readers.

## Exemplar sentences (shape, not content)

**Gap-identification pattern**:
- "While ratings have become ubiquitous and influential on the Internet, surprisingly little empirical research has investigated..." [intro-style gap]
- "Machine learning techniques have received increasing attention...but their application to personalized normative modelling of the heart from population data remains underexplored." [qiao-2025]
- "Existing foundation models are predominantly based on ECG data and are largely confined to standard 12-lead configurations." [gu-2026]
- "so far, no work has addressed how to systematically measure and psychometrically validate LLM personality." [serapio-garcia-2025]

**Positioning-by-contrast in Discussion**:
- "So far, only four previous studies have tried to apply AI to IRDs, all in much smaller datasets of fewer than 150 patients and across substantially fewer genes." [pontikos-2025]

## Anti-patterns

- Do NOT create a standalone "Related Work" or "Literature Review" section in an NMI paper. This is a structural violation of Nature-family conventions.
- Do NOT review each prior work in a full paragraph. Use 1-2 clause characterizations.
- Do NOT organize related work chronologically. Organize by approach category.
- Do NOT use author-year citations inline. Use superscript numbered citations.
- Do NOT front-load all related work in the Introduction. Distribute comparison evidence across Introduction (gap), Results (head-to-head), and Discussion (positioning).
- Do NOT discuss individual paper contributions at length. Characterize approach categories and their shared limitations.

## Contrast with IS journals

- IS journals (MISQ, ISR, MS) have a dedicated "Related Work" or "Literature Review" section, often 2,000-4,000 words with sub-sections organized by theoretical stream. NMI has NO such section.
- IS journals review individual papers in 3-5 sentences each, summarizing their contribution and limitation. NMI characterizes approach categories in 1-2 clauses.
- IS journals use related work to establish theoretical grounding. NMI uses it purely to identify the technical gap.
- IS journals position the paper against theories (RBV, TAM, signaling theory). NMI positions against method categories (discriminative models, generative models, foundation models).
- IS journals cite 30-60 papers in the literature review section alone. NMI's Introduction contains 15-50 references total, covering both background AND gap identification.
- The IS "Related Work" section is a separate, complete document. The NMI "related work" is a distributed narrative across Introduction + Discussion + Results.
