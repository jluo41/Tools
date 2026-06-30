# NatComm Results -- Section Style Guide

Extracted from 11 Nature Communications exemplar papers (healthcare AI / clinical ML / LLM in medicine / prescribing). Supplements `style-profile.md`.

## Word budget

- Results is typically the longest section. 1,500-5,000+ words, spanning 4-10+ pages.
- larcher-2026: ~1,500w (compact clinical ML). xu-2026: ~3,500w. chen-2026: ~2,500w. li-2026: ~4,000w. salvatore-2026: ~3,500w. zhou-2026: ~4,000w. ho-2026: ~3,000w. abdallah-2026: ~4,500w. lin-2026: ~4,500w. adetunji-2026: ~2,800w. gaudio-2026: ~2,800w.
- Results occupies roughly 35-50% of the main text.

## Placement

Results comes BEFORE Methods in every NatComm paper. This is the mandatory Nature-family section order:

```
Abstract -> Introduction -> Results -> Discussion -> Methods -> References
```

All 11 exemplars confirm this ordering without exception.

## Arc

```
(Optional) System/method overview subsection (conceptual, not detailed)
  -> Cohort / data description (sample, datasets, baseline characteristics)
  -> Core performance (main accuracy/benchmark comparison)
  -> Fine-grained analysis (subgroup, department, category-level)
  -> Advanced analysis (ablation, error analysis, interpretability, external validation)
  -> (Optional) Real-world deployment / clinical utility demonstration
```

The arc escalates from setup through proof of performance to clinical relevance. Each subsection is a self-contained "question + evidence" unit.

## Signature moves

1. **Descriptive subsection headings (not declarative claims).** Unlike NMI which uses declarative claim headings ("System X achieves Y"), NatComm predominantly uses descriptive topic headings:
   - "Overview of DxDirector-7B and Training Method" [xu-2026]
   - "Accuracy of Clinical Diagnosis" [xu-2026]
   - "Quantitative Analysis of Human Physicians' Workload" [xu-2026]
   - "Diagnostic Accuracy" [chen-2026]
   - "Error Analysis" [chen-2026]
   - "Descriptive evaluation of the data" [salvatore-2026]
   - "Cox proportional hazards PheWAS" [salvatore-2026]
   - "Memorization results of continued pretrained LLMs" [li-2026]
   - "Memorization results of LLMs fine-tuned over standard medical benchmarks" [li-2026]
   - "Performance Discrepancies across Multi-Racial and Multi-Ethnic Groups" [ho-2026]
   - "Trade-off Between Accuracy and Fairness" [ho-2026]
   - "Validation of the GAME algorithm" [zhou-2026]
   - "Mapping codes between EHR systems" [zhou-2026]
   - "Feature selection" [zhou-2026]
   - "Ablation study results" [zhou-2026]
   - "TrialMatchAI: A Modular AI System for Patient-Trial Matching" [abdallah-2026]
   - "Population characteristics" [adetunji-2026]
   - "Identifying subgroups at high-risk for T2D in Agincourt" [adetunji-2026]
   - Some papers use longer descriptive-declarative hybrids: "Benchmarking TrialMatchAI: Synthetic Patient Evaluation TrialMatchAI Achieves High Recall and Accurate Ranking on Synthetic Benchmarks" [abdallah-2026]

2. **Method overview as first Results subsection.** Many NatComm papers open Results with a conceptual overview of the system before showing results. This subsection describes the architecture/pipeline at a conceptual level, references Fig. 1, and sets up the reader to understand subsequent results:
   - "Overview of DxDirector-7B and Training Method" [xu-2026]
   - "ClinDiag-Framework" / "ClinDiag-Benchmark" / "ClinDiag-GPT" [chen-2026]
   - "TrialMatchAI: A Modular AI System for Patient-Trial Matching" [abdallah-2026]
   - "Overview of this study" [lin-2026]
   - This pattern is especially common in system/method papers. Empirical studies (salvatore-2026, ho-2026, adetunji-2026) skip this and open with cohort description.

3. **Both figures AND tables in main text.** Unlike NMI which avoids standalone tables, NatComm papers frequently include tables in the main text for cohort demographics, model comparisons, and result summaries:
   - Table 1 (cohort demographics): salvatore-2026, ho-2026, adetunji-2026, zhou-2026
   - Table 1 (system components): abdallah-2026
   - Table 1 (AUROC comparison): lin-2026
   - Tables 2-6 (memorization ratios, accuracy comparisons): li-2026
   - Tables are used for structured numeric comparisons; figures for visual patterns (Manhattan plots, heatmaps, bar charts, ROC curves).

4. **Inline statistics with full reporting.** All statistics are reported inline within prose. NatComm reports statistics more exhaustively than NMI, including p-values, confidence intervals, and effect sizes:
   - "accuracy at 36.23%. This represents a 3.27% absolute advantage over the strongest commercial LLM (o3-mini: 32.96%)" [xu-2026]
   - "diagnostic accuracy ranged from 29.32% to 39.76%, with ClinDiag-GPT outperforming all other models" [chen-2026]
   - "hazard ratio (HR) (95% confidence interval (CI)): 1.54 (1.25, 1.90)" [salvatore-2026]
   - "mean BA for NHW was similar across methods, with CR yielding the highest mean NHW BA: 85.19% +/- 3.48%, p = 0.546" [ho-2026]
   - "GAME achieved AUCs of 0.916 for similarity relationships and 0.914 for relatedness relationships" [zhou-2026]
   - "30-token memorization ratio of 10.48%, compared to 1.23% for its direct baseline" [li-2026]

5. **Bold inline sub-headings for finer granularity.** Within Results subsections, NatComm uses bold inline labels to segment analyses:
   - "**Overview of DxDirector-7B.** The overall workflow..." / "**Training Method.** Our training method..." [xu-2026]
   - "**Comparisons with baselines.** Overall, the results show..." [li-2026]
   - "**Factors influencing memorization ratio.** We also examine..." [li-2026]
   - "**Position analysis on where memorization occurs.** We further analyze..." [li-2026]
   - "**Manual examination on what is memorized.** We further conduct a manual examination..." [li-2026]
   - "**Baseline Evidence of Inter-group Performance Discrepancy.** To evaluate..." [ho-2026]
   - "**GLP-1 RA vs. SGLT2i:** In our intention-to-treat PheWAS..." [salvatore-2026]

6. **Figure-subsection mapping (flexible).** Unlike NMI's strict 1:1 figure-subsection mapping, NatComm is more flexible. Some subsections reference multiple figures; some figures span multiple subsections:

   | Paper | Subsections | Main figures | Tables |
   |-------|------------|-------------|--------|
   | xu-2026 | 6 | 7 | 0 |
   | chen-2026 | 5 | 5 | 1 |
   | li-2026 | 3 (with many sub-sections) | 3 | 6 |
   | salvatore-2026 | 4 | 2 | 1 |
   | ho-2026 | 4 | 3 | 2 |
   | zhou-2026 | 6 | 5 | 3 |
   | abdallah-2026 | 7 | 5 | 2 |
   | lin-2026 | 8 | 6 | 1 |
   | adetunji-2026 | 5 | 9 | 1 |
   | larcher-2026 | 2 | 5 | 4 |

7. **Validation / ablation as standard subsection.** Nearly every paper includes an explicit validation or ablation subsection:
   - "Ablation study results" [zhou-2026]
   - "Component Contributions: Hybrid Retrieval, Re-ranking, and CoT Improve Precision (Ablation Study)" [abdallah-2026]
   - "Evaluating and validating discovered subgroups" [adetunji-2026]
   - "Influence of fine-tuning dataset on ECG-LFM performance" [lin-2026]
   - "Error Analysis" [chen-2026]

## Exemplar sentences (shape, not content)

**Subsection opening** (purpose statement + setup):
- "In this section, we first give an overview of DxDirector-7B and its training method. Then, we present the experimental results." [xu-2026]
- "We evaluated seven large language models, including ClinDiag-GPT, GPT-4o-mini, GPT-4o, Claude-3-Haiku..." [chen-2026]
- "The analytic cohort comprised 17,267 adults with T2D who received a qualifying drug prescription on or after January 1, 2018." [salvatore-2026]
- "We performed a wide range of validation studies to evaluate the quality and clinical utility of GAME embeddings." [zhou-2026]

**Result claim with inline statistics**:
- "DxDirector-7B achieves the highest accuracy at 36.23%. This represents a 3.27% absolute advantage over the strongest commercial LLM (o3-mini: 32.96%)" [xu-2026]
- "GLP-1 RA was associated with a reduced risk for 11% (n=9) and an increased risk for 89% (n=75), relative to individuals prescribed SGLT2i" [salvatore-2026]
- "GAME achieved a TOP1 accuracy of 74.2%, whereas no other approach exceeded 62.2%." [zhou-2026]

**Literature comparison in Results**:
- "Compared to existing state-of-the-art LLMs, DxDirector-7B achieves superior diagnostic accuracy while markedly reducing both the clinical workload and expertise required." [xu-2026]

## Anti-patterns

- Do NOT use purely generic headings ("Experiment 1", "Experiment 2"). Use descriptive topic headings that name what is being evaluated.
- Do NOT place Methods before Results. Nature-family convention is Results first.
- Do NOT omit tables when structured numeric comparisons are needed. NatComm uses both tables AND figures in the main text (unlike NMI which defers tables to supplement).
- Do NOT write result paragraphs without figure/table references. Every result paragraph should point to at least one figure or table.
- Do NOT front-load all benchmarks before clinical results. Interleave technical validation with clinical utility.
- Do NOT omit ablation or validation studies. NatComm expects explicit evidence of component contributions and generalizability.

## Paragraph structure

Each subsection typically contains 2-6 paragraphs, each 100-300 words. The internal structure of each subsection follows a micro-arc:

1. **Purpose statement** (1 sentence): What was tested/assessed and why
2. **Setup** (1-3 sentences): Dataset, comparison conditions, metrics
3. **Results** (3-6 sentences): Findings with figure/table references and inline statistics
4. **Interpretation** (0-2 sentences): Brief contextualization (what the result means, not discussion-level)

## Contrast with NMI

- NMI uses declarative claim headings ("CSFM generalizes across different healthcare tasks"). NatComm uses descriptive topic headings ("Diagnostic Accuracy", "Ablation study results").
- NMI avoids standalone tables in main text; figures dominate. NatComm uses both tables and figures freely.
- NMI has a strict 1:1 figure-subsection mapping. NatComm is more flexible.
- NMI papers are predominantly system/method papers. NatComm also accommodates empirical studies (PheWAS, cohort analyses) with different Results structures (e.g., cohort description + association analysis).
- Both use inline statistics rather than standalone result tables.

## Contrast with IS journals

- IS Results sections follow Methods. NatComm Results precede Methods.
- IS journals use extensive regression/coefficient tables in the main text. NatComm uses a mix of tables and figures with inline stats.
- IS journals organize results around hypotheses (H1, H2, H3). NatComm organizes around demonstrations, evaluations, or analyses.
- IS journals use separate "Robustness Checks" subsections. NatComm integrates robustness evidence within result subsections or has explicit "Ablation" subsections.
- IS journals use descriptive subsection headings (like NatComm, unlike NMI).
- IS Results are typically shorter than Introduction. NatComm Results are the longest section.
