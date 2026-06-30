# npj Digital Medicine Related Work -- Section Style Guide

Extracted from 9 npj Digital Medicine exemplar papers. Supplements `style-profile.md`.

## Key finding: npjDM does NOT have a standalone Related Work section

npj Digital Medicine follows the Nature house style, which does **not** include a separate "Related Work" or "Literature Review" section. Instead, prior work is distributed across two locations:

1. **Introduction** (P2-P3): Prior approaches and their limitations, used to motivate the gap.
2. **Discussion** (P3-P5): Comparison to prior work, used to contextualize findings.

This is a fundamental structural difference from CS/IS venues that dedicate a full section to related work.

## Word budget (across Introduction + Discussion)

- Related work content totals 400-800 words across both sections.
- Introduction devotes 1-2 paragraphs (~200-400 words) to prior approaches.
- Discussion devotes 1-2 paragraphs (~200-400 words) to comparison with prior work.

## Positioning approach

### In Introduction: Prior work as stepping stones

Prior work is cited to establish what is now possible and to define the gap. The tone is constructive:

- "Recent years have witnessed rapid development in medical LLMs across multiple languages and scales." [zhuang-2026]
- "Machine Learning (ML) offers promising capabilities for transforming inpatient diabetes management by leveraging the wealth of electronic health records (EHR)..." [momenzadeh-2026]
- "Evidence Gap Maps (EGMs) use structured visual tools to systematically present the availability and characteristics of evidence on a particular topic." [iqbal-2026]
- "Recent advances in AI, particularly large language models (LLMs), offer new pathways for integrating medical knowledge with clinical data." [lai-2026]

The pattern is: acknowledge the advance, then pivot to what it cannot yet do.

### In Discussion: Prior work as benchmarks

Prior work is cited to compare results quantitatively. The tone is comparative but respectful:

- "In those studies, precision was 0.09 with recall 0.82 (F1 = 0.16) and precision 0.12 with recall 0.72 (F1 = 0.21). While recall was high, precision near 0.1 implies a substantial false-alert burden...In contrast, the LSTM in this study achieved precision 0.23 and recall 0.44 (F1 = 0.30), more than doubling precision..." [momenzadeh-2026]
- "Compared with the graph-free LLM baselines, GPT and DeepSeek yielded substantially lower accuracy and F1-scores..." [lai-2026]
- "As recently argued in Nature Medicine, claims of clinical value for medical AI must be supported by proportionate evidence..." [he-2026]

## Signature moves

1. **Cite-and-differentiate pattern.** A prior approach is described in 1-2 sentences, then the limitation is stated in the next sentence:
   - "Mathioudakis et al. (2021) used a stochastic gradient boosting (SGB) model on 1.6 million POC BG values from 55,000 admissions to predict BG <70 mg/dL within a rolling 24-hour window. The model achieved precision (positive predictive value) 0.09, recall (sensitivity) 0.82, and F1 score 0.16. Similarly, Zale et al. (2022) used a RF model on 4.5 million POC BG values from 185,000 admissions to perform multiclass classification...The low precision (~0.1) in both studies indicates high number of false alerts, contributing to alert fatigue." [momenzadeh-2026]

2. **Table of prior work (rare but present in review papers).** Review papers may include a comparison table:
   - "Table 2. LLMs' improvement in accuracy and efficiency compared to traditional methods in RCTs" [he-2026]

3. **No grouped literature review paragraphs.** Unlike IS journals, there are no paragraphs organized by theme (e.g., "Studies on X", "Studies on Y"). Each citation serves a specific argumentative purpose in the Introduction or Discussion flow.

## Exemplar sentences (shape, not content)

**Introduction positioning** (constructive):
- "Several initiatives standardize clinical vocabularies and medical concepts. For example, OMOP and FHIR provide common data models that harmonize vocabularies into a unified system, while the UMLS Metathesaurus and Disease Ontology organize medical concepts and link clinical vocabularies through cross references." [johnson-2026]

**Discussion comparison** (quantitative):
- "A prior ICU hypoglycemia alert study reported a PPV of 14%, yet was still considered clinically actionable given the severity of hypoglycemia and low risk associated with recommendations." [momenzadeh-2026]
- "We see significant gains in performance for mental disorders, where LLM-based methods struggled to capture clinically meaningful physiological manifestations, such as associating 'chest tightness' with PTSD or 'brain tomography' with Alzheimer's disease." [johnson-2026]

## Anti-patterns

- Do NOT create a standalone "Related Work" section. npjDM does not use this structure.
- Do NOT write themed literature review paragraphs (e.g., "Several studies have examined X"). Each citation should serve a gap-defining or comparison purpose.
- Do NOT cite papers without connecting them to the argumentative arc. Every citation either (a) establishes a stepping stone in the Introduction or (b) provides a benchmark for comparison in the Discussion.
- Do NOT stack citations without differentiation. Instead of "(X; Y; Z)", describe what each approach contributed and where it fell short.
- Do NOT attack prior work. Use constructive framing: "While X advanced Y, it did not address Z."

## Implementation guidance for authors

If your paper has extensive related work to discuss, distribute it as follows:

| Content type | Where it goes | How much |
|---|---|---|
| Prior approaches that motivate the gap | Introduction P2-P3 | 200-400 words |
| Quantitative comparison to prior results | Discussion P3-P5 | 200-400 words |
| Methodological alternatives not compared | Discussion (brief mention) | 50-100 words |
| Detailed technical review of prior systems | Supplementary materials | As needed |

## Contrast with IS journals

- MISQ/ISR devote a full section (1500-2500 words) to literature review organized by theoretical streams. npjDM distributes prior work across Introduction and Discussion totaling 400-800 words.
- IS journals use prior work to build theoretical motivation. npjDM uses prior work to build clinical need and quantitative benchmarks.
- IS journals may cite 30-50 papers in the related work section. npjDM typically cites 5-15 relevant papers across Introduction and Discussion combined.
