# JAMA Internal Medicine -- Methods Style Guide

Distilled from 11 JAMA IM original investigations (Williams 2025, Desai 2026, Kurlander 2026, Fournier 2026, Hirshberg 2025, Berkowitz 2025, Boone 2026, Seamans 2018, Wen 2020, Taylor 2025, Kroenke 2015, Masterson 2025, Zhang 2026).

## Word budget

- 1200-2500 words. The range is wide because RCTs with complex interventions require more (Taylor 2025 ~2200 words; Kroenke 2015 ~2500 words with detailed intervention protocol), while observational studies with simpler designs can be shorter (Zhang 2026 ~1400 words; Wen 2020 ~1200 words).
- JAMA IM Methods sections are moderate length -- longer than JAMA flagship Original Investigations (which are constrained to ~2500 total text) but not as exhaustive as specialty journals.
- Heavy use of Supplement/eMethods references to offload details (variable definitions, sensitivity analysis specifications, additional protocol information).

### Contrast with JAMA flagship

- JAMA IM allows slightly longer Methods, especially for intervention description in RCTs.
- JAMA IM methods more frequently include explicit subsection headers with colored formatting.
- JAMA IM observational studies almost always name a reporting guideline (STROBE) in the opening of Methods; JAMA flagship sometimes omits this.

## Subsection structure

Methods are organized under colored subheadings. The order and naming vary by study design:

### Observational studies (typical order)

1. **Data Sources** or **Study Setting and Sample** -- names the database/data source, coverage, dates, IRB status.
2. **Study Population** or **Study Sample** -- inclusion/exclusion criteria, cohort construction.
3. **Exposure** or **Variable Measurement** -- defines the primary independent variable.
4. **Outcome Assessment** or **Main Outcomes and Measures** -- defines the primary outcome variable.
5. **Covariates** -- lists confounders and how they were measured.
6. **Statistical Analysis** or **Statistical Analyses** -- models, sensitivity analyses, software.

### RCTs (typical order)

1. **Study Design** -- trial name, type (pragmatic, efficacy, stepped-wedge), registration, IRB, CONSORT adherence.
2. **Trial Setting** or **Study Setting and Sample** -- sites, dates, health system description.
3. **Identification and Recruitment** or **Trial Participants** -- eligibility criteria, enrollment process.
4. **Randomization** -- method, blinding, allocation concealment.
5. **Trial Arms** or **Intervention** / **Usual Care** -- detailed description of each arm.
6. **Outcomes** -- primary and secondary outcomes defined.
7. **Sample Size Calculation** or **Statistical Analysis** -- power calculation, analytic approach.
8. **Statistical Analysis** -- models, intent-to-treat, adjustments, software.

## Opening paragraph pattern

The first paragraph of Methods names the data source, IRB approval, reporting guideline, and consent status in a compact block.

Exemplar openers:
- "We used the 2000-2014 Truven Health Analytics MarketScan Commercial Claims and Encounters databases covering the years 2000 to 2014." (Seamans 2018)
- "Our ED and hospital discharge data came from the Healthcare Cost and Utilization Project FastStats -- a database query tool published by the Agency for Healthcare Research and Quality." (Wen 2020)
- "We conducted the ENCOMPASS trial, a stepped-wedge cluster randomized clinical trial comparing usual care with the STAR program... The protocol was approved by the Advarra Institutional Review Board with a waiver of informed consent." (Taylor 2025)
- "This study was reviewed by the Mass General Brigham Institutional Review Board. Informed consent was waived due to the use of deidentified data. The Strengthening the Reporting of Observational Studies in Epidemiology (STROBE) reporting guideline was followed." (Zhang 2026)

**Signature move**: Reporting guideline is named within the first 2-3 sentences, often parenthetically: "(STROBE)" or "(CONSORT)". This is near-universal in JAMA IM. Other reporting guidelines used: TREND for nonrandomized quality improvement studies (Kurlander 2026), DECIDE-AI for AI decision support (Desai 2026).

## Study population paragraph

Defines inclusion/exclusion criteria in a structured way. Uses a logical sequence: who was eligible, who was excluded, what the final analytic sample was.

Exemplar:
- "This retrospective cohort study included household members of patients who initiated use of prescription opioids or prescription NSAIDs based on outpatient pharmacy dispensing claims... Prescription NSAIDs were chosen as the active comparator group because they have similar indications for treating pain, which minimizes the potential for unmeasured confounding." (Seamans 2018)

**Signature move**: The comparator choice is explicitly justified with a clinical rationale (not just "we used X as controls").

## Exposure/outcome definition

Each variable is defined precisely with data source, codes used, and any validation information. JAMA IM favors one-sentence-per-variable definitions.

Exemplar patterns:
- "Our primary outcome was initiation of prescription opioids by members of the index patient's household." (Seamans 2018)
- "The primary outcome was a dichotomous composite measure of mortality and hospital readmission assessed 90 days after hospital discharge." (Taylor 2025)
- "Our main outcomes were the rates of all opioid-related ED visits and inpatient hospitalizations, measured as the quarterly numbers of treat-and-release ED discharges and hospital discharges related to opioid abuse, dependence, and overdose, per 100 000 state population." (Wen 2020)

## Statistical analysis paragraph

Always includes:
1. The primary analytic model named explicitly.
2. What was adjusted for (covariates).
3. Sensitivity/robustness analyses.
4. Two-sided testing and significance threshold ("P values < .05 were considered statistically significant" or "With 2-sided testing, P values < .05 were considered statistically significant").
5. Software and version ("Analyses were conducted using SAS, version 9.4" or "R version 4.4.1").

Exemplar:
- "All models were weighted by state population and included time-varying control variables that adjusted for state-level health care supply, general economic conditions, and concurrent policies... Standard errors were clustered at the state level to allow for arbitrary correlation within states but assume independence across states." (Wen 2020)
- "All statistical tests were 2-sided, and significance was set at P < .05. Analyses were performed using SAS version 9.4 (SAS Institute)." (Taylor 2025)

**Signature move**: JAMA IM uniformly reports the software/version at the end of Statistical Analysis. This is a house style requirement.

## Supplement offloading

JAMA IM papers aggressively offload methodological details to supplements:
- "see eTable 1 in the Supplement for definitions"
- "Additional details are provided in the eMethods in the Supplement"
- "see eTable 2 in the Supplement for details on the construction of weights"
- "The full study protocol can be found in the trial protocol in Supplement 1."

This keeps the main text focused on the most essential design choices while making full reproducibility information available.

## Signature moves

1. **IRB + consent in one sentence**: "The study was deemed exempt from approval and informed patient consent as using aggregate state-level deidentified data by the University of Kentucky Institutional Review Board." (Wen 2020)

2. **Active-comparator justification**: Observational studies explicitly justify comparator choice clinically, not just statistically.

3. **Causal diagrams mentioned**: Some papers note that "Potential confounders of the association... were identified a priori using subject matter knowledge and causal diagrams" (Seamans 2018). This is increasingly common in JAMA IM.

4. **Power/sample size for RCTs**: Always includes the target effect size, power, alpha, and any re-estimation after protocol changes.

5. **Reporting guideline adherence**: Named in the opening paragraph -- STROBE for observational, CONSORT for RCTs, STARD for diagnostic studies.

## Anti-patterns

- Describing statistical methods without naming the specific model (e.g., saying "regression" without specifying logistic, linear, Cox, GEE, etc.).
- Omitting the software and version.
- Failing to mention the reporting guideline (STROBE/CONSORT).
- Describing the intervention in the Introduction rather than Methods.
- Including results (effect sizes, p-values, sample sizes) in the Methods section.
- Using future tense ("We will analyze...") instead of past tense.
- Failing to justify the choice of comparator group.
- Omitting the significance threshold and sidedness of tests.
