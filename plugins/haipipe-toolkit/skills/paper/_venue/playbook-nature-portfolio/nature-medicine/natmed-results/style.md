# Nature Medicine Results -- Section Style Guide

Extracted from 14 Nature Medicine exemplar papers (2025-2026). Supplements `style-profile.md`.

## Word budget

- Results is typically 1,500-3,500 words, spanning 3-6 pages.
- bean-2026: ~1,500w, 5 subsections, 4 figures. brinton-2026: ~1,200w, 6 subsections, 3 figures + 2 tables. saab-2026: ~2,500w, 6 subsections, 6 figures. varoquaux-2026: ~1,800w, 4 subsections, 5 tables + 1 figure. tao-2026: ~2,000w, 7 subsections, 4 figures + 1 table. khasentino-2025: ~2,500w, 3 subsections, 3 figures + 2 tables. bedi-2026: ~3,500w, 3 first-level subsections with many nested sub-headings, 5 figures + 1 table. zhou-2026: ~3,000w, 6 subsections, 4 figures + 1 table. lang-2026: ~2,500w, 6 subsections, 2 figures + 4 tables.
- Results occupies roughly 30-45% of the main text (less than NMI's 40-50%).

## Placement

Results comes BEFORE Methods in every Nature Medicine paper. This is the mandatory Nature-family section order:

```
Abstract -> Introduction -> Results -> Discussion -> Methods -> References
```

All 14 exemplars confirm this ordering without exception. Brief Communications blend Results into the body text without a labeled section heading.

## Arc

```
(RCTs) Patient disposition / CONSORT summary
  -> Primary outcome (with full statistical reporting)
  -> Secondary outcomes (clinical documentation, safety, satisfaction)
  -> Post hoc analyses / sensitivity analyses
  -> Safety / adverse events

(AI system evaluations) System overview / evaluation setup
  -> Main performance comparison (vs humans / vs baselines)
  -> Subgroup analyses (modality, difficulty, specialty)
  -> Robustness / ablation studies
  -> User experience / clinical integration
```

The arc varies by study type. For RCTs, it follows the CONSORT structure (patient flow, primary outcome, secondary outcomes, safety). For AI evaluations, it escalates from main comparison to subgroup analyses to robustness. Unlike NMI which always starts with the hero finding, Nature Medicine RCTs start with patient disposition.

## Signature moves

1. **Descriptive subsection headings (not declarative claims).** This is a KEY difference from NMI. Nature Medicine Results subsections use neutral procedural headings, not claim headings:
   - "Task validation" / "Experimental performance" / "Performance in user interactions" [bean-2026]
   - "Patient disposition" / "Primary outcome" / "Secondary outcomes" [brinton-2026]
   - "Descriptive statistics and consort diagram" / "Primary outcomes" / "Secondary outcomes" [varoquaux-2026]
   - "Patient flow and baseline data" / "Outpatient workflow" / "Patient-centeredness and care coordination" [tao-2026]
   - "Estimating the true number of clinical LLM studies" / "Trends across time, tiers, tasks and specialties" [lu-2026]
   - "Clinician validation of the taxonomy" / "Overview of the benchmark suite" [bedi-2026]
   - Some AI system papers use declarative headings (zhou-2026: "Reti-Pioneer enables longitudinal risk stratification"; khasentino-2025: "PH-LLM exceeds expert performance on multiple-choice examinations"), but descriptive headings are the dominant pattern.

2. **Bold inline sub-headings within subsections.** Fine-grained results within a subsection use bold inline headings ending with a period:
   - **"Clinical documentation quality."** / **"Clinical safety."** / **"Sentinel conditions."** / **"Patient satisfaction."** [brinton-2026]
   - **"Diagnostic accuracy of multimodal AMIE and PCPs."** [saab-2026]
   - **"State-aware reasoning improves dialogue quality."** / **"History-taking improves diagnostic accuracy."** [saab-2026]
   - **"Expert evaluation of PH-LLM and expert responses."** / **"Automatic evaluation and ablation experiments."** [khasentino-2025]

3. **Tables ARE used in main text (especially for RCTs).** This is a KEY difference from NMI, which avoids main-text tables. Nature Medicine clinical trial papers regularly include:
   - Table 1: baseline patient characteristics (demographics, diagnoses)
   - Table 2: primary outcome by study arm (with aOR, 95% CI, P)
   - Additional tables: secondary outcomes, subgroup analyses, diagnostic performance
   - Papers observed with main-text tables: brinton-2026 (2 tables), varoquaux-2026 (5 tables), lang-2026 (4 tables), tao-2026 (1 table), nijman-2026 (3 tables), khasentino-2025 (2 tables), bedi-2026 (1 table), zhou-2026 (1 table).
   - Papers with NO main-text tables: bean-2026, saab-2026, restrepo-2026 (AI evaluation papers tend to use figures instead).

4. **CONSORT flow diagram as Fig. 1 (RCTs).** Clinical trial papers use Fig. 1 for the CONSORT/participant flow:
   - "Fig. 1 | CONSORT flow diagram of participant and cluster progression throughout the trial." [brinton-2026]
   - "Fig. 1 | Study population for CXRs CONSORT diagram." [varoquaux-2026]
   - "Fig. 1 | CONSORT flow diagram." [tao-2026]
   - AI system papers use Fig. 1 for the system/evaluation overview instead.

5. **Full statistical reporting inline.** Statistics are reported with exhaustive detail in the text:
   - Adjusted odds ratio: "adjusted odds ratio (aOR) 0.77, 95% CI 0.55 to 1.08, P = 0.13" [brinton-2026]
   - Chi-squared: "chi-squared(1), P < 0.001, n1 = n2 = 600" [bean-2026]
   - Ratio of geometric means: "ratio of geometric means of 0.97 (95% confidence interval (CI) = 0.93-1.02; P = 0.31)" [varoquaux-2026]
   - Odds ratio with bootstrap CI: "odds ratio (OR) = 11.7, 95% confidence interval (CI) = 3.7-36.6" [levine-2026]
   - AUROC with CI: "0.833 (95% CI 0.810-0.856)" [zhou-2026]
   - Cohen's kappa: "Cohen's kappa of 0.741 (95% confidence interval (CI) 0.685-0.796)" [lu-2026]
   - Sensitivity/specificity: "sensitivity 74.7% (95% CI: 59.4-88.1); specificity 99.1% (95% CI: 97.7-99.7)" [nijman-2026]
   - Mixed-effects model: "P < 0.001, based on a mixed-effects model accounting for scenario difficulty" [saab-2026]

6. **CI format varies but follows two main patterns:**
   - Words: "95% CI 0.55 to 1.08" [brinton-2026] -- common for RCTs
   - Parenthetical dash: "95% CI 0.810-0.856" or "(0.93-1.02)" -- common for AI evaluation papers
   - Colon: "95% CI: 59.4-88.1" [nijman-2026]

7. **P value conventions:**
   - Exact values: P = 0.13, P = 0.023, P = 0.84
   - Threshold: P < 0.001, P < 0.0001
   - Scientific notation (rare, for very small): P = 6.6 x 10^-23 [lu-2026]
   - Significance markers in figures: *P < 0.05, **P < 0.01, ***P < 0.001; NS [saab-2026]

8. **Null results reported plainly with clinical interpretation.** Nature Medicine does not shy from negative findings:
   - "Treatment failure occurred in 102/4,693 patients (2.2%) in the intervention arm and 94/4,654 (2.0%) in the control arm (adjusted odds ratio (aOR) 0.77, 95% CI 0.55 to 1.08, P = 0.13, in both the intention-to-treat (ITT) and per-protocol analysis)." [brinton-2026]
   - "There was no significant difference in the time from CXR acquisition to CT scan according to AI prioritization, with a ratio of geometric means of 0.97 (95% confidence interval (CI) = 0.93-1.02; P = 0.31)." [varoquaux-2026]

## Exemplar sentences (shape, not content)

**Subsection opening** (setup + purpose):
- "To assess the risks of the public using LLMs for medical advice, we conducted a randomized study where we asked participants to make decisions about a medical scenario as though they had encountered it at home." [bean-2026]
- "Treatment failure occurred in 94 patients (2.0%) in the control group and 102 (2.2%) in the intervention group..." [brinton-2026]
- "Between 17 July 2023 and 31 December 2024, a total of 97,731 CXRs were performed across five diverse National Health Service (NHS) Trusts..." [varoquaux-2026]

**Result claim with inline statistics**:
- "The primary outcome did not differ significantly between groups, extending emerging evidence from recent randomized evaluations in other clinical settings." [brinton-2026]
- "participants identified relevant conditions in fewer than 34.5% of cases and disposition in fewer than 44.2%, both no better than the control group." [bean-2026]
- "multimodal AMIE consistently outperformed PCPs across the full range of k (1-10 diagnoses)." [saab-2026]
- "Median (interquartile range) times to CT were 53 days (17-145) and 53 days (19-141), with and without AI prioritization." [varoquaux-2026]

## Anti-patterns

- Do NOT use declarative claim headings as the default style ("System X outperforms Y"). Use descriptive headings ("Primary outcome", "Secondary outcomes", "Performance comparison"). The occasional declarative heading appears in AI system papers, but descriptive is the dominant pattern.
- Do NOT avoid tables in the main text. Nature Medicine uses main-text tables extensively for clinical trial results, unlike NMI which avoids them.
- Do NOT omit the CONSORT flow diagram for RCTs. Fig. 1 must be the participant flow.
- Do NOT report only positive findings. Null results are reported plainly with full statistics.
- Do NOT omit CIs when reporting effect sizes. Nature Medicine expects CI with every effect estimate.
- Do NOT separate safety reporting from the Results section. Safety/adverse events are reported as a subsection within Results.
- Do NOT front-load all AI benchmarks before clinical results. For clinical validation papers, clinical outcomes come first.

## Paragraph structure

Each subsection typically contains 1-4 paragraphs, each 100-300 words. The internal structure of each subsection follows a micro-arc:

1. **Setup** (1 sentence): What was assessed and the study parameters
2. **Result** (2-4 sentences): Findings with figure/table references and inline statistics
3. **Interpretation** (0-1 sentences): Brief clinical contextualization (not discussion-level)

For RCTs, the primary outcome subsection follows a strict pattern:
1. Event rates in each arm
2. Effect estimate (aOR, RR, HR) with 95% CI and P value
3. Sensitivity analyses (ITT, per-protocol, covariate-adjusted)
4. Brief statement of what the result means clinically

## Contrast with NMI

- NMI uses declarative claim headings ("System X achieves Y"). Nature Medicine predominantly uses descriptive headings ("Primary outcome", "Patient disposition").
- NMI avoids main-text tables (all figures). Nature Medicine uses tables extensively for clinical trial data (baseline characteristics, outcome tables).
- NMI organizes results around system capabilities. Nature Medicine organizes around clinical outcomes (primary, secondary, safety).
- NMI uses zero or near-zero tables. Nature Medicine papers average 1-5 main-text tables.
- NMI Reports inline statistics without structured hypothesis testing. Nature Medicine reports pre-specified primary and secondary outcomes with formal statistical tests.
- Both venues place Results before Methods.
- NMI Results are the longest section (40-50% of text). Nature Medicine Results are shorter relative to Methods (30-45% of text).
- NMI never reports null results as a primary finding. Nature Medicine regularly does.
- NMI does not use CONSORT diagrams. Nature Medicine RCTs require CONSORT flow diagrams.
