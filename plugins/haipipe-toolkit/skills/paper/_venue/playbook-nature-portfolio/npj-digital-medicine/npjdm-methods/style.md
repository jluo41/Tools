# npj Digital Medicine Methods -- Section Style Guide

Extracted from 9 npj Digital Medicine exemplar papers. Supplements `style-profile.md`.

## Word budget

- 1000-3500 words. Median ~2000 words. Appears AFTER Discussion (Nature house style).
- wang-2026 (brief comm): ~2000w. momenzadeh-2026: ~3500w. lai-2026: ~3000w. he-2026: ~2000w. johnson-2026: ~1500w. xian-2026: ~1500w (with extensive supplement). iqbal-2026: ~2000w. yuan-2026: ~1500w. zhuang-2026: ~2000w.
- Always divided into clearly labeled subsections. Section is titled "Methods" (not "Materials and Methods").

## Arc

```
Ethics / IRB / consent (lead with this)
Study design and participants (cohort definition, inclusion/exclusion)
Data sources and processing
Model / system architecture (technical detail)
Training, optimization, hyperparameters
Evaluation design (metrics, comparisons, statistical tests)
(optional) Fairness / subgroup / sensitivity analysis protocol
Data availability statement
Code availability statement
```

The arc is **reproducibility-oriented**: it provides enough detail that the study could be replicated, starting with ethical approvals and ending with data/code availability. Technical detail is thorough but defers deep architecture specifics to supplementary materials when possible.

## Signature moves

1. **Ethics statement leads.** The very first subsection or sentence establishes IRB approval, informed consent status, and data governance:
   - "The study was approved by the Cedars Sinai Institutional Review Board (STUDY00002306, MOD00011744) and the Huntington Hospital Clinical Research Committee (MOD00012907). The requirement for informed consent and HIPAA authorization was waived..." [momenzadeh-2026]
   - "This study was conducted in accordance with the Declaration of Helsinki and was approved by the Medical Ethics Committee of Sun Yat-sen Memorial Hospital, Sun Yat-sen University (Approval No. SYSKY-2025-542-01)." [lai-2026]
   - "This study was reviewed and approved by the Ethics Review Board Approval No. S2025-302-01." [zhuang-2026]
   - "Ethical approval was not required as this study analyzed published data." [iqbal-2026]
   - "The prospective study was registered on ClinicalTrials.gov (NCT06493175; first posted September 20, 2024)." [wang-2026]

2. **Precise cohort definition with inclusion/exclusion criteria.** Study populations are defined with specific clinical criteria, time windows, and exclusion rates:
   - "Eligible admissions met the following inclusion criteria: (i) age >=18 years, (ii) length of stay >=24 hours, and (iii) receipt of at least one antihyperglycemic medication during the admission." [momenzadeh-2026]
   - "The retrospective cohort included adults (>=18 years) presenting to the emergency department (ED) with chest pain between June 2021 and June 2024. Cases with incomplete records...were excluded according to a prespecified protocol, yielding an exclusion rate of 3.4%..." [wang-2026]
   - "Only systematic reviews published between 2015 and 2025 that reported DHIs and patient engagement outcomes as either a primary or secondary outcome were selected." [iqbal-2026]

3. **Technical detail in labeled subsections.** Each methodological component gets its own subsection with a descriptive heading:
   - "Model Input Representation and Feature Engineering" [momenzadeh-2026]
   - "Model Architecture, Training and Optimization" [momenzadeh-2026]
   - "Missing Data Handling" [momenzadeh-2026]
   - "Graph construction" [lai-2026]
   - "Task-graph-tool execution chain" [lai-2026]
   - "Leveraging EMR for Advanced Multi-Task Model Optimization and Instruction Fine-Tuning" [zhuang-2026]
   - "Definitions of Categorization" [he-2026]

4. **Statistical analysis protocol.** Methods include explicit description of statistical tests, multiple comparison corrections, and threshold selection:
   - "We used DeLong's test for pairwise AUC comparisons on correlated receiver operating characteristic curves, McNemar's test for paired comparisons of sensitivity and specificity, and chi-square tests for proportions." [wang-2026]
   - "Bootstrap resampling of test prediction windows (100 iterations, each comprising 50% of the test set) were used to estimate 95% CIs." [momenzadeh-2026]
   - "P-values were adjusted for multiple comparisons across features using the Benjamini-Hochberg false discovery rate (FDR) procedure, with FDR < 0.05 considered statistically significant." [momenzadeh-2026]

5. **TRIPOD/CONSORT/PRISMA compliance.** Many papers explicitly reference reporting guidelines:
   - "This study was reported in accordance with the Transparent Reporting of a Multivariable Prediction Model for Individual Prognosis or Diagnosis + Artificial Intelligence (TRIPOD+AI) statement." [momenzadeh-2026]
   - "The review was conducted and reported in accordance with the Preferred Reporting Items for Systematic Reviews and Meta-Analyses (PRISMA) guidelines." [he-2026]
   - "Reporting of the EGM is in line with the Nature Portfolio Reporting Summary linked to the article." [iqbal-2026]

## Exemplar sentences (shape, not content)

**Ethics lead**:
- "This study was conducted in accordance with the Declaration of Helsinki and was approved by the Medical Ethics Committee of Sun Yat-sen Memorial Hospital, Sun Yat-sen University (Approval No. SYSKY-2025-542-01). The requirement for informed consent was waived by the committee as the research involved only the analysis of anonymized data..." [lai-2026]

**Cohort definition**:
- "We conducted a retrospective cohort study and a prospective pilot deployment across four tertiary hospitals in China...The retrospective cohort included adults (>=18 years) presenting to the emergency department (ED) with chest pain between June 2021 and June 2024." [wang-2026]
- "We analyzed EHR data from Cedars Sinai Health System hospitals, including Cedars Sinai Medical Center (CSMC; 886 beds) and two affiliate community hospitals, Marina Del Rey Hospital (MDRH; 133 beds) and Huntington Health (HH; 619 beds), spanning May 14, 2014 and March 26, 2025." [momenzadeh-2026]

**Training detail**:
- "Model training consumed approximately 18,000 GPU hours on a 64xNVIDIA H100 cluster, utilizing mixed-precision computation and a maximum sequence length of 6144 tokens..." [wang-2026]
- "Model training was conducted on a high-performance computing cluster equipped with NVIDIA A100 80GB GPUs. Predictions simulate a real-time system that updates every 4 hours as new clinical data becomes available." [momenzadeh-2026]

## Anti-patterns

- Do NOT omit the ethics statement. It is mandatory and typically appears first.
- Do NOT describe the system architecture only in Results. Technical detail belongs in Methods, even if a high-level overview appears in Results.
- Do NOT omit inclusion/exclusion criteria. npjDM expects precise patient selection criteria for clinical studies.
- Do NOT skip the statistical analysis protocol. Readers expect to know which tests were used, how thresholds were selected, and how multiple comparisons were handled.
- Do NOT omit data and code availability statements. npjDM requires these as separate subsections at the end of Methods.
- Do NOT bury hyperparameters in supplementary materials without mentioning the key ones (learning rate, batch size, architecture) in the main text.

## Subsection structure

Methods are organized into clearly labeled subsections. Common subsection patterns:

**For model/system papers**:
1. Ethics statement (1 paragraph)
2. Study design and participants (cohort, inclusion/exclusion)
3. Data sources / data processing
4. Model architecture / system design
5. Training and optimization (hyperparameters, hardware)
6. Evaluation and statistical analysis
7. (Optional) Subgroup / fairness analysis protocol
8. Data availability
9. Code availability

**For review/evidence-mapping papers**:
1. Protocol registration (PROSPERO, etc.)
2. Search strategy and databases
3. Eligibility criteria (inclusion/exclusion)
4. Data extraction and categorization
5. Quality assessment (AMSTAR-2, RoB, CONSORT-AI)
6. Data synthesis / analysis
7. Data availability
8. Code availability

## Contrast with NMI

- NMI Methods often appear as a brief section or are substantially in supplementary materials. npjDM Methods are thorough in the main text (1000-3500 words).
- NMI does not always lead with an ethics statement. npjDM always leads with ethics/IRB.
- NMI rarely includes TRIPOD/CONSORT compliance statements. npjDM frequently references reporting guidelines.
- NMI Methods focus on technical novelty (architecture, loss function, training). npjDM Methods balance technical detail with clinical study design (cohort, endpoints, outcome definitions).
- Both journals place Methods AFTER Discussion (Nature house style), not after Introduction.
