# Diabetes Care -- Research Design and Methods Style Guide

Distilled from 10 Diabetes Care papers: Galindo 2026 (RCT/Brief), Reaven 2026 (TTE), Bergenstal 2026 (GRADE), Lehmann 2026 (ML/Brief), Zheng 2025 (NLP), Kahkoska 2025 (e-Letter), He 2026 (e-Letter), Godneva 2026 (TIR), Ajjan 2026 (gDAC), Dupenloup 2026 (cost-effectiveness).

## Section heading

Always **RESEARCH DESIGN AND METHODS** (all caps). Never "Methods" alone, never "Materials and Methods", never "Study Design". This is the most distinctive Diabetes Care convention.

## Word budget

- Original Article: 1500-2500 words. The range depends on study complexity; RCTs and target trial emulations with complex designs run longer; NLP/ML methods papers with pipeline descriptions run at the high end; observational cohort descriptions can be shorter.
- Brief Report: 500-800 words. Compressed methods with heavy offloading to Supplementary Material.
- e-Letters/Observations: ~300-500 words woven into the body text (no section heading).

### Contrast with JAMA

JAMA IM methods sections run 1200-2500 words and almost always name a reporting guideline (STROBE/CONSORT) in the opening sentences. Diabetes Care papers rarely name reporting guidelines explicitly in the main text (only 1 of 10 papers named CHEERS). Diabetes Care uses bold title-case subsection headers (not colored formatting like JAMA IM). The mandatory terminal subsection "Data and Resource Availability" is unique to Diabetes Care.

## Subsection structure

Methods are organized under **bold, title-case** subheadings. The order varies by study design.

### Observational studies (typical order)

1. **Overview** or **Study Design** -- names the data source, design, and dates.
2. **Eligibility Criteria** or **Study Population** -- inclusion/exclusion criteria.
3. **Data Extraction Procedures** or **Variable Measurement** -- defines exposure, covariates.
4. **Outcomes** -- primary and secondary outcomes defined.
5. **Statistical Analysis** -- models, sensitivity analyses, software.
6. **Data and Resource Availability** -- data sharing statement (mandatory).

Reaven 2026 subsections: Overview / Eligibility Criteria / Data Extraction Procedures / Outcomes / Statistical Analysis / Sensitivity, Subgroup, and Additional Analyses / Data and Resource Availability.

### RCTs (typical order)

1. **Intervention** or **Study Design** -- trial name, registration, design.
2. **Study Population** -- eligibility, enrollment.
3. **Intervention** -- detailed description of each arm.
4. **Study Outcomes** -- primary and secondary outcomes.
5. **Statistical Analysis** -- models, intent-to-treat, power.
6. **Data and Resource Availability** -- mandatory.

Galindo 2026 (Brief Report): Intervention / Study Outcomes / Statistical Analysis / Data and Resource Availability.

### ML/AI/NLP studies (typical order)

1. **Study Design and Population** -- data source, population.
2. **Procedures** or **Steps for [task]** -- pipeline description, often using numbered steps.
3. **Outcome and Sample Size** -- primary metric defined.
4. **Analysis and ML** or **Methods Evaluation** -- model selection, training, evaluation.
5. **Data and Resource Availability** -- mandatory.

Lehmann 2026 subsections: Study Design and Population / Procedures / Outcome and Sample Size / Analysis and ML.
Zheng 2025 subsections: Steps for Extracting Glucose Data From CGM AGP Reports / Methods Evaluation.

### Cost-effectiveness studies

Dupenloup 2026 subsections: Overview / Setting and Study Population / Markov Model / Efficacy of CGM Versus CGM With RPM / Complications / Mortality, Costs, and Quality of Life / Analyses / Data and Resource Availability.

## Opening paragraph pattern

The first paragraph names the study design, data source, and IRB/ethics status.

Exemplar openers:
- "This study was a crossover RCT of people with T2D and ESKF undergoing hemodialysis (ClinicalTrials.gov identifier: NCT04473430). The study was performed at Emory Healthcare dialysis centers in Atlanta, Georgia... The Institutional Review Board at Emory University approved the study protocol." (Galindo).
- "Target trial emulation (TTE) is a systematic approach to emulate a hypothetical randomized clinical trial (the target trial), using longitudinal observational data (11,12). In this study we emulate a randomized clinical trial of initiation of CGM (vs. no initiation) using observational CGM data from national VHA electronic health care files." (Reaven).
- "We conducted two studies at the University Hospital Bern (from November 2022 to January 2023 and from January 2024 to April 2024) to record voice data in standardized euglycemia and hypoglycemia in people with type 1 diabetes." (Lehmann).
- "We analyzed CGM reports stored as PDF files from the electronic health record at New York University Langone Health." (Zheng).

**Signature move**: The study design is named in the first sentence. Clinical trial registration numbers appear early. IRB/ethics approval is stated within the first 2-3 sentences. Unlike JAMA, Diabetes Care does not always name a reporting guideline here.

## Study population paragraph

Defines inclusion/exclusion criteria. For Brief Reports and e-Letters, criteria may be compressed into one sentence.

Exemplar:
- "We included adults (aged 18-80 years) with T2D, and hemoglobin A1c (HbA1c) between 5% (31.1 mmol/mol) and 12% (107.7 mmol/mol); undergoing hemodialysis three times per week for at least 3 months; and receiving treatment with basal insulin alone... or in combination with prandial insulin..." (Galindo).
- "Veterans were considered eligible for inclusion if they were >30 and <85 years of age, had T1D, and were receiving insulin and checking their blood glucose with home blood glucose monitors in the year prior to their enrollment." (Reaven).

## Statistical Analysis paragraph

Always includes:
1. The primary analytic model named explicitly.
2. What was adjusted for (covariates listed or referenced to a supplementary table).
3. Software and version: "All statistical analyses were performed using R version 4.4.1 (Supplementary Material Methods)" (Reaven). "SAS version 9.4" or "Stata" etc.
4. Two-sided testing and significance threshold when applicable: "P values < .05 were considered statistically significant" or significance threshold stated.

Exemplar:
- "We used means with SDs or their corresponding 95% CIs or medians and their interquartile range (IQR) for continuous variables and frequencies with proportions for discrete variables. Continuous outcomes between the two glycemic monitoring methods were compared using Wilcoxon nonparametric tests, assuming that the carryover effects were the same for both groups." (Galindo).
- "Weighted pooled logistic regression models with restricted cubic splines for time were then fitted within each treatment strategy to estimate the probability of death at each interval." (Reaven).

**Signature move**: Software/version is always stated. For ML papers, model architecture details (features, hyperparameters, cross-validation scheme) are reported: "logistic regression (LR) with ridge regularization (C = 1, class weights = 1.0), random forest (number of estimators = 100), and support vector machine (kernel = rbf, C = 1.0)" (Lehmann).

## Data and Resource Availability (mandatory terminal subsection)

Every Diabetes Care paper ends the Methods section with this subsection. Standard patterns:
- "Deidentified participant data will be made available 24 months after publication and for up to 12 months after upon reasonable request for meta-analysis purposes and with an institutional review board-approved protocol to the corresponding author." (Galindo).
- "The VA supports that data (deidentified participant data) from approved studies be made publicly available upon request. However, this is contingent on robust review and approval processes to ensure privacy and confidentiality of Protected Health Information." (Reaven).
- "The data sets generated during and analyzed in the current study are available from the corresponding author upon reasonable request." (standard template).

## Supplementary Material offloading

Diabetes Care papers offload methodological details to Supplementary Material:
- "additional inclusion and exclusion criteria are provided in the Supplementary Methods" (Lehmann).
- "as previously described (2)" with citation to prior methods paper (Reaven).
- "(full inclusion/exclusion criteria provided in the Supplementary Material)" (Galindo).

**Cross-reference pattern**: "(Supplementary Material)", "(Supplementary Fig. 1)", "(Supplementary Methods)".

## Signature moves

1. **Pipeline description with numbered steps**: ML/NLP papers describe algorithms as numbered steps: "the steps of our algorithm pipeline consist of 1) performing OCR... 2) determining the type of CGM document... 3) extracting variables... and 4) storing the extracted glucose data" (Zheng).

2. **CGM device specification**: Device names include manufacturer and model: "Dexcom G6 rtCGM (intervention group)", "Abbott Freestyle Libre Pro Flash (FSL) CGM device".

3. **CGM metric definitions**: Outcomes are defined using International Consensus thresholds: "percentage time below range (%TBR) <70 mg/dL", "%TIR 70-180 mg/dL", "%TAR >180 mg/dL and >250 mg/dL" (Galindo).

4. **Clinical trial registration**: Stated parenthetically: "(ClinicalTrials.gov identifier: NCT04473430)" (Galindo), "(ClinicalTrials.gov reg. no. NCT05189938)" (Ajjan).

5. **Active-comparator justification**: RCTs and observational studies justify the comparator: "capillary blood glucose (CBG) testing (standard of care [SOC] group)" (Galindo).

## Anti-patterns

- Using "Methods" or "Materials and Methods" as the section heading (must be "RESEARCH DESIGN AND METHODS").
- Omitting the Data and Resource Availability subsection.
- Describing statistical methods without naming the specific model.
- Omitting the software and version.
- Including results (effect sizes, p-values) in the Methods section.
- Using future tense ("We will analyze...") instead of past tense.
- Omitting CGM threshold definitions when CGM metrics are outcomes (e.g., just saying "TIR" without specifying 70-180 mg/dL).
- Omitting the clinical trial registration number for registered studies.
