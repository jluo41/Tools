# NatComm Related Work -- Section Style Guide

Extracted from 11 Nature Communications exemplar papers (healthcare AI / clinical ML / LLM in medicine / prescribing). Supplements `style-profile.md`.

## The core rule: NatComm has NO separate Related Work section

None of the 11 exemplar papers contain a standalone "Related Work", "Literature Review", "Background", or "Prior Work" section. This is a firm Nature-family convention. All prior-work positioning is distributed across three locations:

1. **Introduction** (primary): background paragraphs that survey existing approaches and identify the gap
2. **Discussion** (secondary): positioning against specific prior methods when comparing results
3. **Supplementary Materials** (tertiary): extended literature review deferred from main text

## How related work is embedded in the Introduction

### The gap-identification pattern

Prior work in the Introduction serves one purpose: to identify the gap that this paper fills. Each existing approach is characterized in 1-3 sentences, immediately followed by its limitation. The pattern is:

```
[Approach category] has been proposed/developed/shown promise [refs].
  However, [approach] [limitation].
  -> (repeat for 2-4 approach categories)
  -> Gap statement: "...remains understudied / unexplored / challenging / a key question remains."
```

### Organization: by approach type, not chronologically

Related work in the Introduction is organized by method category, not by publication date. Each paragraph covers one approach cluster:

| Paper | Approach categories surveyed | Gap statement |
|-------|------------------------------|--------------|
| xu-2026 | LLMs for diagnosis (general) -> LLMs as physician tools | "the role of LLMs in real-world diagnosis is limited to functioning merely as tools for physicians" |
| chen-2026 | LLMs for medical exams -> LLMs for clinical workflows | "few studies have systematically evaluated LLMs within the context of real-world diagnostic workflows" |
| li-2026-memorization | Foundation LLMs -> Continued pretraining -> Fine-tuning -> Memorization risks | "a key question remains: to what extent do LLMs memorize medical training data" |
| salvatore-2026 | GLP-1 RA mechanisms -> Clinical trials on cardiovascular/kidney -> Prior PheWAS (Xie et al.) | "there exists a paucity of real-world data examining their downstream health effects" |
| ho-2026 | AI for dementia -> Racial/ethnic disparities in ML -> Biomarker differences | "AI-driven diagnostic systems may not generalize equally across racial and ethnic groups" |
| zhou-2026 | ICD/LOINC ontologies -> Knowledge graph embeddings -> EHR-derived embeddings -> LLM integration | "current models fall short of producing embeddings that simultaneously capture standardized biomedical knowledge, linguistic semantics, and real-world clinical usage" |
| abdallah-2026 | Rule-based systems -> Deep learning approaches -> LLM-based matching -> Open-source alternatives | "most existing LLM-based trial matching systems...rely heavily on proprietary, API-driven models" |
| adetunji-2026 | Traditional risk scores (FINDRISC, ADA) -> Epidemiological studies in Africa -> Risk factor interactions | "existing risk models miss interactions between risk factor cutoffs" |
| gaudio-2026 | LLMs for omics -> LLMs for biomarker discovery | "systematic testing in omics-driven biomarker discovery remains limited" |
| lin-2026 | ECG deep learning models -> Foundation models (HeartBEiT, RETFound) | "existing models lack interpretability and fail to capture relationships between genotype and ECG representations" |
| buckley-2026 | Text-based LLM evaluation -> Multimodal model performance | "the prioritization of images compared to text in multimodal diagnosis...remain poorly understood" |

### Reference density in Introduction

References are densely clustered in background paragraphs, sparse in the contribution paragraph. NatComm uses superscript numbered citations:

| Paper | Total intro refs | Background | Contribution para |
|-------|-----------------|------------|-------------------|
| xu-2026 | ~55 | ~50 | ~5 |
| chen-2026 | ~14 | ~12 | ~2 |
| zhou-2026 | ~35 | ~32 | ~3 |
| abdallah-2026 | ~55 | ~50 | ~5 |
| li-2026-memorization | ~37 | ~34 | ~3 |
| salvatore-2026 | ~65 | ~60 | ~5 |

### Brevity of individual work descriptions

Prior works are cited but not reviewed in depth. Each gets at most 1-3 sentences:

- "Most existing benchmarks for LLMs still rely on exam-style formats." [li-2026-benchmark] -- category-level, not per-paper
- "Federated learning (FL) methods address this limitation by enabling model co-training without transferring individual-level data." [zhou-2026] -- one sentence for an entire field
- "Early automation efforts relied on rule-based logic and probabilistic systems, which, while effective for structured scenarios, struggled with the semantic diversity and contextual nuances of clinical text." [abdallah-2026] -- one sentence for an approach family
- Prior works are cited as evidence of a trend or approach category, not individually analyzed.

### Occasional inline author naming

Unlike NMI (which almost never names authors inline), NatComm occasionally positions directly against a specific named prior study:

- "Using the US Department of Veterans Affairs databases, Xie, Choi & Al-Aly (2025) systematically tested for associations across 175 clinical outcomes..." [salvatore-2026]
- "Our study extends beyond the work of Xie and colleagues by examining an even broader range of clinical outcomes (up to 974 phenotypes)." [salvatore-2026]
- This is the exception, used only when the paper is directly building on or contrasting with a specific prior study. Most citations remain numbered-only.

## How related work appears in Discussion

The Discussion contains a secondary positioning layer where this paper's results are compared directly against prior methods:

- "Compared to existing state-of-the-art LLMs, DxDirector-7B achieves superior diagnostic accuracy while markedly reducing both the clinical workload and expertise required." [xu-2026]
- "TrialMatchAI outperformed the non-fine-tuned LLM-Match baseline on TREC2021/2022 (e.g., TREC2022 nDCG@10 0.75 vs 0.40)." [abdallah-2026]
- "Our study extends beyond the work of Xie and colleagues..." [salvatore-2026] -- point-by-point comparison across multiple paragraphs
- "Substituting SAPBERT with models such as BGE yields comparable results." [zhou-2026]

This positioning-by-contrast is more extensive in NatComm Discussion than in NMI. Some NatComm papers (salvatore-2026, chen-2026) devote 3-6 Discussion paragraphs to positioning against prior work.

## How related work appears in Results

Some papers embed mini-positioning within Results subsections for direct head-to-head comparisons:

- "Benchmarking TrialMatchAI: Synthetic Patient Evaluation TrialMatchAI Achieves High Recall and Accurate Ranking on Synthetic Benchmarks" [abdallah-2026] -- Results subsection dedicated to benchmarking against TrialGPT, LLM-Match, Panacea
- "Comparisons with baselines. Overall, the results show that medical foundation language models have higher memorization ratios than their corresponding baselines." [li-2026-memorization]
- Benchmark comparisons in Results present prior methods as baselines, not as literature review.

## Supplement as extended literature review

When the related work is extensive, papers defer to supplementary material:

- "See Supplementary Materials 'Literature Review' section H for additional details." [abdallah-2026]
- Supplementary Notes with extended background are common, especially for system papers with many prior approaches to compare.

This allows the main text to stay concise while providing comprehensive literature coverage for specialist readers.

## Exemplar sentences (shape, not content)

**Gap-identification pattern**:
- "However, the role of LLMs in real-world diagnosis is limited to functioning merely as tools for physicians." [xu-2026]
- "Despite their growing utilization and the media's portrayal of expected and unexpected benefits of GLP-1 RAs, there exists a paucity of real-world data examining their downstream health effects." [salvatore-2026]
- "Nevertheless, AI-driven diagnostic systems may not generalize equally across racial and ethnic groups." [ho-2026]
- "However, most existing methods are developed within a single institution or rely on fixed ontologies, and thus lack effective mechanisms for integrating EHR information across multiple healthcare systems." [zhou-2026]

**Positioning-by-contrast in Discussion**:
- "TrialMatchAI achieves this level of performance using lightweight, open-source models, a significant advancement given the computational demands and expense typically associated with high-performance LLMs." [abdallah-2026]
- "Our findings indicate that current LLMs are not suitable for autonomous deployment in clinical general practice and that all realistic applications require continuous human oversight." [li-2026-benchmark]

## Anti-patterns

- Do NOT create a standalone "Related Work" or "Literature Review" section in a NatComm paper. This is a structural violation of Nature-family conventions.
- Do NOT review each prior work in a full paragraph. Use 1-3 sentence characterizations.
- Do NOT organize related work chronologically. Organize by approach category.
- Do NOT use author-year citations as the default format. Use superscript numbered citations. Inline author names are acceptable only when directly positioning against a specific named prior study.
- Do NOT front-load all related work in the Introduction. Distribute positioning across Introduction (gap), Results (benchmarks), and Discussion (interpretation).
- Do NOT discuss individual paper contributions at length. Characterize approach categories and their shared limitations.

## Contrast with NMI

- Both NMI and NatComm have NO separate Related Work section. The convention is identical.
- NMI almost never names specific authors inline. NatComm occasionally does so when directly extending a named prior study.
- NatComm Discussion sections sometimes include more extensive positioning against prior work (3-6 paragraphs of comparison), whereas NMI Discussion positioning is briefer (1-2 paragraphs).
- Both defer extended literature surveys to Supplementary Materials when needed.

## Contrast with IS journals

- IS journals (MISQ, ISR, MS) have a dedicated "Related Work" or "Literature Review" section, often 2,000-4,000 words with sub-sections organized by theoretical stream. NatComm has NO such section.
- IS journals review individual papers in 3-5 sentences each, summarizing their contribution and limitation. NatComm characterizes approach categories in 1-3 sentences.
- IS journals use related work to establish theoretical grounding. NatComm uses it purely to identify the technical/empirical gap.
- IS journals position the paper against theories (RBV, TAM, signaling theory). NatComm positions against method categories (LLMs, foundation models, risk scores, federated learning).
- IS journals cite 30-60 papers in the literature review section alone. NatComm's Introduction contains 14-65 references total, covering both background AND gap identification.
- The IS "Related Work" section is a separate, complete document. The NatComm "related work" is a distributed narrative across Introduction + Discussion + Results + Supplement.
