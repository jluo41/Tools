# Nature Medicine Related Work -- Section Style Guide

Extracted from 14 Nature Medicine exemplar papers (2025-2026). Supplements `style-profile.md`.

## The core rule: Nature Medicine has NO separate Related Work section

None of the 14 exemplar papers contain a standalone "Related Work", "Literature Review", "Background", or "Prior Work" section. This is a firm Nature-family convention, shared with NMI. All prior-work positioning is distributed across three locations:

1. **Introduction** (primary): background paragraphs that survey current clinical practice and prior studies to identify the evidence gap
2. **Discussion** (secondary): positioning against specific prior clinical trials and studies when comparing results
3. **Supplementary Information** (tertiary): extended literature review when the background is extensive

## How related work is embedded in the Introduction

### The clinical-gap-identification pattern

Prior work in the Introduction serves one purpose: to establish that the clinical evidence needed does not yet exist. Each existing approach or prior study is characterized in 1-3 sentences, immediately followed by its limitation. The pattern is:

```
[Clinical practice / prior studies] have shown [promising results / demonstrated X] [refs].
  However, [limitation: no prospective evidence / not tested in real-world / limited to text-only].
  -> (repeat for 2-3 categories)
  -> Gap statement: "...remains limited / untested / poorly characterized."
```

### Organization: by evidence tier, not chronologically

Related work in the Introduction is organized by evidence type or approach category, progressing from strongest prior evidence to the current gap:

| Paper | Prior work categories surveyed | Gap statement |
|-------|-------------------------------|--------------|
| brinton-2026 | Primary care in LMICs -> LLMs in clinical vignettes -> Rule-based CDSS limitations -> LLM-CDSS promise | "prospective interventional evidence from real-world clinical studies, particularly in LMICs, remains limited" |
| saab-2026 | AMIE text-based studies -> Telehealth promise -> Multimodal data in clinical practice | "evidence validating the capabilities of LLMs for diagnostic conversations involving such multimodal data is scarce" |
| bean-2026 | LLM benchmarks -> Physician-AI collaboration studies -> LLM chatbot adoption | "this does not necessarily translate to accurate performance in real-world settings" |
| varoquaux-2026 | Lung cancer pathways -> CXR screening -> AI for CXR -> NICE review | "NICE concluded that there was insufficient evidence to make any recommendations" |
| osullivan-2026 | Subspecialist shortage -> LLMs as clinical tools -> LLM integration in clinical tasks | "It remains unclear whether LLMs possess the nuanced understanding...required to effectively replicate the decision-making process of experts" |
| nijman-2026 | Paediatric early warning scores -> WHO IMCI -> Vital signs in LMICs -> Biomarkers | "Neither vital signs nor danger signs reliably stratify risk" |
| zhou-2026 | Oculomics studies -> Foundation models -> Multi-disease frameworks | "Key gaps persist, including the underrepresentation of multi-ethnic populations" |
| yao-2026 | GLP-1 trials -> BMI limitations -> ML risk prediction | "no framework for guiding the allocation of interventions...has been developed in a data-driven, risk-based manner" |
| perez-2026 | CPET -> 6MWT -> Wearable fitness estimates -> Apple Watch in HF | "it remains unclear whether wearable-derived algorithms validated in nondiseased populations can be reliably translated to patients with HF" |
| lu-2026 | Prior systematic reviews -> Manual review limitations | "the real-world clinical impact of LLMs remains poorly characterized" |

### Reference density in Introduction

Nature Medicine introductions contain fewer references than NMI because they are shorter and more clinically focused:

| Paper | Total intro refs | Typical clustering |
|-------|-----------------|-------------------|
| brinton-2026 | ~25 | 3-5 per gap-identification claim |
| bean-2026 | ~22 | 2-4 per approach category |
| saab-2026 | ~14 | 2-3 per evidence tier |
| varoquaux-2026 | ~20 | 2-4 per policy reference |
| osullivan-2026 | ~15 | 2-3 per capability claim |

### Brevity of individual work descriptions

Prior works are cited but not reviewed in depth. Each gets at most 1-2 clauses, often as evidence of a trend rather than individual analysis:

- "Vignette-based comparisons suggest that LLMs can match or exceed provider performance on some diagnostic and triage tasks." [brinton-2026] -- category-level, not per-paper
- "Large language models (LLMs) have demonstrated the ability to interpret clinical information and produce context-appropriate recommendations consistent with clinical guidelines." [brinton-2026] -- capability summary with clustered refs
- "Although large language models (LLMs) have shown promise in diagnostic dialogue, their evaluation has been largely restricted to text-only interactions." [saab-2026] -- one clause characterizing the entire prior literature

## How related work appears in Discussion

The Discussion contains a secondary positioning layer where this paper's results are compared directly against prior clinical evidence:

- "The improvement in process outcomes observed aligns with findings from both controlled and real-world studies." [brinton-2026] -- validation against prior trials
- "Our finding of no significant demographic bias contrasts with ref. 7, which reported race and sex effects in general-purpose LLMs." [levine-2026] -- direct contradiction of a prior finding
- "The estimated effect corresponded to between 13 fewer and 1 additional treatment failures per 1,000 patients, indicating that any true effect, if present, is likely to be modest. The observed event rate was lower than anticipated, resulting in limited precision for detecting modest effects." [brinton-2026] -- contextualizing null results against power expectations
- "So far, only four previous studies have tried to apply AI to IRDs, all in much smaller datasets of fewer than 150 patients." [analogous pattern] -- positioning by dataset scale

This is positioning-by-contrast: the prior work is characterized by its study design, population, or capability, and this paper's advance (or limitation) is stated explicitly.

## How related work appears in Results

Unlike NMI, Nature Medicine RARELY embeds mini-related-work within Results subsections. One exception:

- Benchmark comparison sections may briefly cite the prior benchmark to motivate the comparison: "To assess how well question-answering benchmarks predicted performance in user deployments, we scored the LLMs on a targeted subset of the popular MedQA benchmark." [bean-2026]

## Supplement as extended literature review

When the background literature is extensive, papers defer to supplementary material, though this is less common in Nature Medicine than in NMI because Nature Medicine papers tend to have shorter, more focused introductions.

## Exemplar sentences (shape, not content)

**Gap-identification pattern**:
- "However, prospective interventional evidence from real-world clinical studies, particularly in LMICs, remains limited." [brinton-2026]
- "It remains unclear whether LLMs possess the nuanced understanding and intricate knowledge base required to effectively replicate the decision-making process of experts in highly specialized medical fields." [osullivan-2026]
- "Whether ChatGPT Health inherits these vulnerabilities or has mitigated them remains untested." [levine-2026]
- "Key gaps persist, including the underrepresentation of multi-ethnic populations and the lack of sufficient validation for multidisease risk stratification." [zhou-2026]

**Positioning-by-contrast in Discussion**:
- "The improvement in process outcomes observed aligns with findings from both controlled and real-world studies." [brinton-2026]
- "Our finding of no significant demographic bias contrasts with ref. 7, which reported race and sex effects in general-purpose LLMs." [levine-2026]

## Anti-patterns

- Do NOT create a standalone "Related Work" or "Literature Review" section. This is a structural violation of Nature-family conventions.
- Do NOT review each prior work in a full paragraph. Use 1-2 clause characterizations.
- Do NOT organize related work chronologically. Organize by evidence tier or approach category.
- Do NOT use author-year citations inline. Use superscript numbered citations.
- Do NOT front-load all related work in the Introduction. Distribute comparison evidence across Introduction (gap) and Discussion (positioning).
- Do NOT discuss individual paper contributions at length. Characterize evidence categories and their shared limitations.
- Do NOT cite extensively within the contribution paragraph. The contribution paragraph should have minimal references (0-3), with density concentrated in the background paragraphs.

## Contrast with NMI

- Both NMI and Nature Medicine have NO separate Related Work section. The convention is identical across the Nature family.
- NMI organizes background by method category (discriminative models, generative models, foundation models). Nature Medicine organizes by clinical evidence tier (retrospective studies, vignette comparisons, prospective trials, real-world deployments).
- NMI positions against technical methods ("existing foundation models are largely confined to 12-lead"). Nature Medicine positions against clinical evidence quality ("prospective interventional evidence remains limited").
- Both use 1-2 clause characterizations of prior work, not full-paragraph reviews.
- Both use superscript numbered citations.
- Nature Medicine introductions tend to be shorter (350-1,200w) than NMI (550-1,600w), so the embedded literature review is more compact.
- Nature Medicine Discussion contains more head-to-head comparison with prior clinical trials. NMI Discussion compares against prior technical methods.
- Both may defer extended literature review to Supplementary Information, though NMI does this more frequently.
