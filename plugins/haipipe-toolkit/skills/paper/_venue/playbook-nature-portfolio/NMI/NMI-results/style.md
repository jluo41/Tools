# NMI Results -- Section Style Guide

Extracted from 8 Nature Machine Intelligence exemplar papers. Supplements `style-profile.md`.

## Word budget

- Results is the longest section in the paper. Typically 2,000-4,000+ words, spanning 5-8 pages.
- mataraso-2025: ~2,500w, 9 subsections, 6 figures. gu-2026: ~3,500w, 6 subsections, 6 figures. serapio-garcia-2025: ~3,000w, 3 first-level + many inline sub-headings, 5 figures. chen-w-2025: ~3,000w, 6 subsections, 6 figures.
- Results occupies roughly 40-50% of the main text.

## Placement

Results comes BEFORE Methods in every NMI paper. This is the mandatory Nature-family section order:

```
Abstract -> Introduction -> Results -> Discussion -> Methods -> References
```

All 8 exemplars confirm this ordering without exception.

## Arc

```
(Optional) Method overview subsection (conceptual, not detailed)
  -> Technical validation (reconstruction, reliability, benchmarks)
  -> Application / clinical utility (disease classification, downstream tasks)
  -> Advanced analysis (interpretability, novel findings, external validation)
  -> (Optional) Accessibility / tooling (web app, code release)
```

The arc escalates from technical proof to clinical/scientific significance. Each subsection is a self-contained "claim + evidence" unit.

## Signature moves

1. **Declarative claim headings.** Every Results subsection heading is a complete sentence asserting the finding, with the system name as subject + active verb:
   - "MeshHeart learns spatio-temporal mesh characteristics" [qiao-2025]
   - "MeshHeart resembles real data distribution" [qiao-2025]
   - "Eye2Gene generalizes across IRD clinics" [pontikos-2025]
   - "Eye2Gene predictions outperforms human expert-level accuracy" [pontikos-2025]
   - "COMET accurately predicted days to the onset of labour" [mataraso-2025]
   - "COMET improved cancer prognosis prediction" [mataraso-2025]
   - "CSFM generalizes across different healthcare tasks" [gu-2026]
   - "Diamond discovers FDR-controlled interactions on simulated datasets" [chen-w-2025]
   - "Diamond reveals drivers of health-related mortality" [chen-w-2025]
   - This is NOT a neutral topic heading ("Reconstruction experiment") but a claim heading ("System X achieves Y").

2. **Strict figure-subsection mapping.** Each Results subsection maps to exactly one figure (multi-panel). The figure carries the quantitative evidence; the prose interprets it. No subsection is figure-free, and no figure is orphaned.

   | Paper | Subsections | Main figures | Mapping |
   |-------|------------|-------------|---------|
   | mataraso-2025 | 9 | 6 | ~1.5 subsections per figure |
   | pontikos-2025 | 7 | 4 | ~2 subsections per figure |
   | qiao-2025 | 4 | 5 | ~1:1 |
   | gu-2026 | 6 | 6 | 1:1 |
   | chen-w-2025 | 6 | 6 | 1:1 |
   | serapio-garcia-2025 | 3 (first-level) | 5 | multi-figure per subsection |
   | doerig-2025 | 3 | 4 | ~1:1 |
   | mon-williams-2025 | 6 | 6 | 1:1 |

3. **Zero or near-zero tables in main text.** Most NMI papers have NO standalone tables in the main text. All detailed quantitative comparisons are in Supplementary Tables. Only pontikos-2025 has 2 main-text tables; serapio-garcia-2025 has 1. The rest have 0.

4. **Inline statistics, never standalone stat tables.** All statistics are reported inline within prose, not separated into result tables. Formatting conventions:
   - Metric + value + CI: "CSFM achieved a macro-F1 of 0.677 (95% confidence intervals (CI): 0.656, 0.699)" [gu-2026]
   - Correlation + p-value: "r = 0.868, 95% confidence interval (CI) [0.825, 0.900], P = 3.9 x 10^-53" [mataraso-2025]
   - Accuracy with range: "top-five accuracy of 83.9% (81.7-86.0%)" [pontikos-2025]
   - Reliability metrics described verbally: "average convergent correlations (r_conv = 0.59, 0.83 and 0.80, respectively)" [serapio-garcia-2025]
   - No asterisks in text; significance stars appear only on figure panels.

5. **Two-tier heading hierarchy within Results.** Some papers use first-level subsection headings (bold, separate line) plus bold-inline or italic-inline sub-headings for finer granularity:
   - First-level: "Measuring and validating personality in LLMs" -> bold-inline: "Reliability results." -> italic-inline: "Convergent validity by model size." [serapio-garcia-2025]
   - First-level: "CSFM generalizes across different healthcare tasks" -> bold-inline: "Cardiovascular disease diagnosis (wearable ECG, PPG, 12-lead ECG)." [gu-2026]

6. **Method overview as first Results subsection.** Some papers open Results with a conceptual overview of the method (not detailed enough for Methods, but enough to understand the results):
   - "Diamond overview" [chen-w-2025] -- includes Fig. 1 (method schematic) and even Equation 1
   - Opening paragraph of Results: "In general, COMET can be applied when EHR data are available for a large cohort of patients..." [mataraso-2025]
   - This pattern is common when the method is novel and the reader needs architectural context before seeing results.

7. **"We found that..." / "We show that..." result reporting.** Results prose uses consistent active-voice formulas:
   - "We found that our approach allowed the robot to respond to an abstract high-order verbal prompt" [mon-williams-2025]
   - "We show that COMET achieves state-of-the-art predictive modelling results" [mataraso-2025]
   - "we assessed the ability of MeshHeart to generate 3D+t cardiac meshes" [qiao-2025]

## Exemplar sentences (shape, not content)

**Subsection opening** (purpose statement + setup):
- "We first assessed MeshHeart on the task of mesh reconstruction." [qiao-2025]
- "To quantify how well LLM embeddings of scene captions predict brain activities, we used representational similarity analysis (RSA)." [doerig-2025]
- "We then investigate the potential clinical utility of the learned latent vector." [qiao-2025]

**Result claim with inline statistics**:
- "the faithfulness score increased from 0.74 to 0.88 with RAG" [mon-williams-2025]
- "average precision of 52.5 on the COCO zero-shot transfer benchmark" [mon-williams-2025]
- "AUROC = 0.842, 95% CI: [0.744, 0.922], P = 0" [mataraso-2025]
- "the lowest HD of 4.163 mm and ASSD of 1.934 mm averaged across the time frames" [qiao-2025]

**Literature-validated finding**:
- "So far, only four previous studies have tried to apply AI to IRDs, all in much smaller datasets of fewer than 150 patients" [pontikos-2025] (positioning in a Results subsection titled "Eye2Gene predictions outperform other AI approaches")

## Anti-patterns

- Do NOT use neutral/descriptive subsection headings ("Experiment 1", "Ablation study", "Performance comparison"). Use declarative claim headings.
- Do NOT present results in tables in the main text. Use figures with multi-panel layouts. Defer tables to Supplementary.
- Do NOT separate statistics from prose into standalone tables. Report all stats inline.
- Do NOT place Methods before Results. The Nature-family convention is Results first.
- Do NOT write result paragraphs without a figure/panel reference. Every result paragraph should point to at least one figure panel.
- Do NOT front-load all benchmarks before any clinical/scientific results. Interleave technical validation with application utility.

## Paragraph structure

Each subsection typically contains 1-4 paragraphs, each 100-250 words. The internal structure of each subsection follows a micro-arc:

1. **Purpose statement** (1 sentence): What was tested/assessed and why
2. **Experimental setup** (1-2 sentences): Brief description of the analysis, dataset, or comparison
3. **Result** (2-4 sentences): Findings with figure references and inline statistics
4. **Interpretation** (0-1 sentences): Brief contextualization (not discussion-level, just what the result means)

## Contrast with IS journals

- IS Results sections follow Methods. NMI Results precede Methods.
- IS journals use extensive regression/coefficient tables in the main text. NMI uses no or minimal tables; figures dominate.
- IS journals organize results around hypotheses (H1, H2, H3). NMI organizes around demonstrations (what the system can do).
- IS journals use separate "Robustness Checks" subsections. NMI integrates robustness evidence within result subsections or defers to supplement.
- IS journals use descriptive subsection headings. NMI uses declarative claim headings.
- IS Results are typically shorter than Introduction. NMI Results are the longest section by far.
