# npj Digital Medicine Results -- Section Style Guide

Extracted from 9 npj Digital Medicine exemplar papers. Supplements `style-profile.md`.

## Word budget

- 1500-4000 words. Median ~2500 words. Highly variable by study scope.
- wang-2026 (brief comm): ~1500w. momenzadeh-2026: ~3500w. lai-2026: ~3500w. johnson-2026: ~3500w. xian-2026: ~4000w. he-2026: ~2500w. yuan-2026: ~3000w. zhuang-2026: ~2500w. iqbal-2026: ~1500w.
- Placed BEFORE Methods (Nature house style). This is the critical structural distinction.

## Arc

```
Subsection 1: System/data overview (what was built or collected)
Subsection 2: Primary validation (headline performance on main task)
Subsection 3-N: Secondary analyses (subgroups, ablations, case studies, additional tasks)
Final subsection: Robustness / sensitivity / fairness checks
```

The arc is **claim-escalation**: each subsection establishes a stronger claim, building from descriptive characterization through primary validation to robustness. Clinical case studies and qualitative examples are interspersed to make technical results tangible.

## Signature moves

1. **Descriptive subsection headings.** Results use bolded or formatted subsection titles that are full phrases describing the finding, not generic labels:
   - "Framework of AI4Doctor" [zhuang-2026]
   - "Unsupervised clustering of 100,272 patients in the eMERGE cohort" [xian-2026]
   - "Topic analysis stratifies patients with unique phenotype patterns" [xian-2026]
   - "A comprehensive clinical knowledge graph for medical codes" [johnson-2026]
   - "Embedding space reveals clinically grounded symptom patterns" [johnson-2026]
   - "Use case 1 and 2: Recognition capability" [lai-2026]
   - "Model Training and Optimization" [momenzadeh-2026]
   - "Prevalence of Human - AI Collaborative Design" [he-2026]

2. **Results-first reporting.** Each subsection opens with the finding, not the method. The analysis that produced the finding is described just enough for comprehension, with full methodological detail deferred to Methods:
   - "The retrospective cohort comprised 16,428 adults...Among these patients, 5,210 (31.7%) were diagnosed with ACS..." [wang-2026]
   - "We developed three complementary graphs: an established medical knowledge graph, a dynamic clinical data graph, and a hybrid graph..." [lai-2026]
   - "A total of 6,426,254 prediction windows were generated across all admissions." [momenzadeh-2026]

3. **Dense statistical reporting.** Results paragraphs are packed with specific numbers, always including confidence intervals, p-values, or effect sizes:
   - "TriageMaster-70B showed higher discrimination than clinician and model comparators (area under the curve (AUC) 0.935, 95% confidence interval (CI) 0.928-0.942), exceeding a ChatGPT-based comparator (AUC 0.875, 95% CI 0.869-0.881, p<0.001) and a 20-cardiologist panel (AUC 0.890, 95% CI 0.884-0.896, p=0.008)." [wang-2026]
   - "The best model (5-day LB, CW, 1 LSTM layer with 112 units and dropout 0.5, learning rate 0.0003) achieved the highest mean F1 score of 0.30 (95% CI: 0.296-0.305), with mean precision of 0.23 and mean recall of 0.44..." [momenzadeh-2026]
   - "The strongest association was observed for essential hypertension (phecode 401.1, p = 1.31 x 10^-163, coefficient = -0.095)." [xian-2026]

4. **Clinical case vignettes.** After quantitative results, many papers include a clinical case example that makes the numbers tangible:
   - "For example, after evaluating symptoms and vital signs, it might state, 'The chest pain is pressure-like, radiates to the left arm, and is accompanied by diaphoresis and hypotension, which strongly suggest ACS.'" [wang-2026]
   - "Clinical case analyses further illustrate the KnDAgent system's value. For instance, established guidelines recommend combined aspirin and clopidogrel therapy for patients with acute myocardial infarction and diabetes. However, dynamic analysis of EHR data (DCDG) revealed that in patients with concurrent chronic kidney disease, this combination substantially increased bleeding risk." [lai-2026]

5. **Figure and table callouts are woven into findings text.** Results refer to figures/tables parenthetically at the point of the finding, not as standalone sentences:
   - "As shown in Fig. 2, we observed a clear and meaningful clustering of phenotype categories (Fig. 2a, b)." [xian-2026]
   - "As shown in Table 1, the ED-Triage dataset was derived from 98,719 emergency department visits at Sun Yat-sen Memorial Hospital." [lai-2026]

## Exemplar sentences (shape, not content)

**Subsection opening** (finding-first):
- "We identified 7,653 records across six databases of which 160 systematic reviews consisting of 3,974 primary studies were included." [iqbal-2026]
- "We developed three complementary graphs: an established medical knowledge graph, a dynamic clinical data graph, and a hybrid graph integrating the above two graphs." [lai-2026]
- "Models were trained and tested on 143,124 inpatient admissions collected between May 14, 2014 and March 26, 2025." [momenzadeh-2026]

**Head-to-head comparison** (with statistical detail):
- "For distinguishing ACS from non-ACS, TriageMaster-70B showed higher discrimination than clinician and model comparators (area under the curve (AUC) 0.935, 95% confidence interval (CI) 0.928-0.942), exceeding a ChatGPT-based comparator (AUC 0.875, 95% CI 0.869-0.881, p<0.001)..." [wang-2026]
- "The LSTM model, which explicitly modeled temporal dependencies, achieved a significantly higher F1 score of 0.30, as assessed by Mann-Whitney U testing of bootstrapped F1 distributions." [momenzadeh-2026]

**Subgroup or fairness result**:
- "No significant performance differences were observed between males and females, Asian and White patients, or Hispanic and Non-Hispanic patients." [momenzadeh-2026]
- "Across all evaluated models, no statistically significant differences are observed between pooled and subgroup-specific performance after correction." [yuan-2026]

## Anti-patterns

- Do NOT bury key findings deep in a paragraph. Lead each subsection with the main finding.
- Do NOT report results without confidence intervals or p-values for inferential claims. npjDM expects rigorous statistical reporting.
- Do NOT use generic subsection headings like "Main Results" or "Additional Analyses." Use descriptive headings that communicate the finding.
- Do NOT defer cohort description entirely to Methods. The Results section in npjDM often opens with a cohort overview subsection (sample sizes, demographics, data characteristics).
- Do NOT skip clinical case examples when the system is for clinical decision support. npjDM values concrete clinical vignettes alongside quantitative metrics.
- Do NOT separate system description from results. In npjDM, the first Results subsection often describes the system/framework before presenting validation.

## Paragraph structure

The Results section is organized by subsections, each with a descriptive heading. Typical patterns:

**For model/system papers** (e.g., wang-2026, zhuang-2026, lai-2026, momenzadeh-2026):
1. System/framework overview (architecture, data pipeline) -- 1 subsection
2. Primary task performance (main comparison) -- 1 subsection
3. Ablation or component analysis -- 1 subsection
4. Additional task / external validation -- 1-2 subsections
5. Robustness / fairness / calibration -- 1 subsection

**For observational/discovery papers** (e.g., xian-2026, johnson-2026):
1. Dataset characterization (what was built, scale) -- 1 subsection
2. Primary finding (clusters, embeddings, patterns) -- 1 subsection
3. Validation (internal, external, expert panel) -- 1-2 subsections
4. Downstream application (clinical utility demonstration) -- 1-2 subsections

**For review/evidence-mapping papers** (e.g., he-2026, iqbal-2026):
1. Search results (PRISMA numbers, included studies) -- 1 subsection
2. Distribution descriptives (by intervention, condition, geography) -- 1-2 subsections
3. Outcome analysis (effects, quality assessment) -- 1-2 subsections
4. Reporting quality / risk of bias -- 1 subsection

## Contrast with NMI

- NMI Results subsections are often organized by experimental setup. npjDM organizes by clinical question or use case.
- NMI may omit confidence intervals for non-clinical metrics. npjDM expects CIs for all primary findings.
- NMI rarely includes clinical case vignettes. npjDM frequently includes them to demonstrate clinical face validity.
- NMI Results are typically shorter (1000-2000 words). npjDM Results are longer (1500-4000 words) because they combine system description with validation.
- In both journals, Results appear BEFORE Methods (Nature house style).
