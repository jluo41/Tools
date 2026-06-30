# JAMA Flagship Methods -- Section Style Guide

Extracted from JAMA Original Investigation exemplars. Supplements `style-profile.md`.

## Word budget

- 1,500-3,000 words for RCTs; 800-1,500 for observational studies. JAMA Methods sections are EXTREMELY detailed. They are typically the longest section in the paper.
- Krebs (2018): ~2,800w across 10+ subsections. Mathioudakis (2025): ~2,200w across 8 subsections. Cipriani (2026): ~2,000w across 6 subsections. Rotenstein (2026): ~1,500w across 7 subsections.
- Methods are divided into many titled subsections (red subheadings in JAMA's published format).

## Arc

```
study design + ethics + reporting standard (opening paragraph)
  -> setting + population + eligibility (Participants)
  -> randomization + blinding (RCTs)
  -> interventions described in detail (Interventions)
  -> outcomes defined precisely (Outcomes)
  -> statistical analysis (always last subsection)
```

## Subsection headings (from exemplars)

### RCT pattern (Krebs 2018, Mathioudakis 2025, Cipriani 2026):
- **Study Design** (or unnamed opening paragraph)
- **Pragmatic Trial Design** [Krebs] / **Participants** [Mathioudakis, Cipriani: "Trial Population"]
- **Participants**
- **Randomization** (and Blinding)
- **Intervention Delivery** [Krebs] / **Interventions** [Mathioudakis, Cipriani: "Trial Design, Treatments, and Assessments"]
  - Sub-subsections for each arm (e.g., "Opioid Prescribing Strategy" / "Nonopioid Prescribing Strategy" [Krebs]; "AI-Based DPP" / "Human Coach-Based DPP" [Mathioudakis])
- **Intervention Adherence** [Krebs]
- **Data Collection and Management** [Mathioudakis]
- **Descriptive Measures** [Krebs]
- **Main Outcomes** / **Study Outcomes** / **Outcomes**
- **Secondary Health Outcomes** [Krebs] / **Secondary Outcomes** [Mathioudakis]
- **Assessment for Adverse Events** [Krebs]
- **Assessment of Study Treatment Received** [Krebs]
- **Sample Size Calculation** [Mathioudakis]
- **Statistical Analysis** (always the final subsection)

### Observational study pattern (Rotenstein 2026):
- **Study Setting and Population**
- **Variables**
- **Main Analytic Approach**
- **Subgroup Analyses**
- **Sensitivity Analyses**
- **Revenue Analysis**

## Signature moves

1. **Opening paragraph names design, ethics, and reporting standard.** The first paragraph of Methods states the study design, names the IRB/ethics approval, and cites the reporting guideline.
   - "The Minneapolis Veterans Affairs (VA) institutional review board approved the trial protocol and patients provided written informed consent. Recruitment details and the trial protocol have been published. The trial protocol and statistical analysis plan are in Supplement 1." [Krebs 2018]
   - "The original trial protocol, statistical analysis plan, and amendments are available in Supplement 1... We received approval from the institutional review boards at each site and adhered to the Consolidated Standards of Reporting of Trials (CONSORT) reporting guideline." [Mathioudakis 2025]
   - "This randomized clinical trial was performed in accordance with the principles of Good Clinical Practice and the Declaration of Helsinki. ... This report followed the Consolidated Standards of Reporting of Trials (CONSORT) reporting guideline." [Cipriani 2026]
   - "This study was approved by the University of California, San Francisco institutional review board." [Rotenstein 2026]

2. **Eligibility criteria given as inclusion then exclusion, with clinical specificity.** Inclusion criteria are stated first, with clinical thresholds, followed by exclusion criteria as a list.
   - "Eligible patients had chronic back pain or hip or knee osteoarthritis pain that was moderate to severe despite analgesic use. Chronic pain was defined as pain nearly every day for 6 months or more. ... Patients on long-term opioid therapy were excluded." [Krebs 2018]
   - "Eligible participants had prediabetes diagnosed using standard laboratory criteria and overweight or obesity using race-specific body mass index (BMI) cutoffs. Exclusion criteria included a prior diabetes diagnosis, severe cardiovascular conditions..." [Mathioudakis 2025]

3. **Interventions described with protocol-level detail.** Each intervention arm gets its own sub-subsection with step-by-step description of what was delivered, by whom, and how.
   - Krebs (2018) describes opioid and nonopioid prescribing strategies in separate subsections, listing Step 1, Step 2, Step 3 medications, dose escalation rules, and maximum dosages.
   - Mathioudakis (2025) describes the AI-based DPP (app features, push notification examples, Bluetooth scale) and the human-coached DPP (CDC curriculum, session frequency) in separate subsections.

4. **Outcomes defined with instrument names, score ranges, and MCID.** Each outcome variable is defined by naming the measurement instrument, stating its range and direction (higher = worse), and citing the minimal clinically important difference.
   - "The primary outcome was pain-related function, assessed with the 7-item Brief Pain Inventory (BPI) interference scale. ... Both BPI scales yield 0 to 10 scores (higher score = worse function or intensity). A prior study of chronic pain in primary care estimated a minimal clinically important difference (MCID) of 0.7 points for both BPI interference and BPI severity." [Krebs 2018]
   - "The primary outcome was treatment discontinuation due to any cause at 8 weeks. This binary outcome indicates whether the participant was still taking the antidepressant prescribed at randomization." [Cipriani 2026]

5. **Statistical Analysis is the last subsection, opens with power calculation (RCTs) or analytic framework (observational).** RCTs state alpha, power, effect size, and target N. Observational studies name the primary analytic approach (DiD, logistic regression, mixed models). Software is named.
   - "Assuming a 2-sided alpha level of .05 and a standard deviation of 2.7, 115 patients completing the study per group were required for 80% power to detect a 1-point between-group difference... SAS (SAS Institute), version 9.2, was used for statistical analysis." [Krebs 2018]
   - "A sample of 276 participants (138 per group) was calculated to provide 80% power at a 1-sided significance level of .05. ... All analyses were conducted using R (R Foundation for Statistical Computing) and Stata version 17.0 (StataCorp)." [Mathioudakis 2025]
   - "The primary analytic approach was a difference-in-differences framework using multivariable ordinary least-squares models." [Rotenstein 2026]

6. **Sensitivity analyses listed explicitly.** JAMA papers enumerate sensitivity/robustness checks, often in a numbered list.
   - "Five post hoc sensitivity analyses were conducted: (1) an analysis that included multiple imputation... (2) an analysis that adjusted for baseline covariates... (3) analyses that applied alternative assumptions... (4) a pattern mixture model... (5) analyses using cluster-robust standard errors..." [Mathioudakis 2025]

## Exemplar sentences (shape, not content)

**Design statement**:
- "This phase 3, parallel-group, pragmatic, noninferiority, randomized clinical trial was conducted from [date] to [date] at [N] [sites] in [locations]." [Mathioudakis 2025]
- "This multicenter, randomized clinical trial included persons between the ages of [X] and [Y] with [condition]." [Cipriani 2026]

**Eligibility**:
- "Eligible [patients/participants] had [condition] [defined as clinical threshold]. [Exclusion criteria]." [general pattern]

**Outcome definition**:
- "The primary outcome was [clinical outcome], assessed with the [instrument] ([abbreviation]; range, [X]-[Y]; higher scores = [direction])." [general pattern]

**Power calculation**:
- "Assuming a [X]-sided alpha level of [value] and a standard deviation of [SD], [N] patients completing the study per group were required for [X]% power to detect a [effect size] between-group difference in [outcome]." [general pattern]

## Anti-patterns

- Do NOT skip the reporting standard citation (CONSORT for trials, STROBE for observational). JAMA requires it.
- Do NOT describe results in Methods. Methods describes what was planned; Results describes what happened.
- Do NOT combine Statistical Analysis with another subsection. It is always standalone and always last.
- Do NOT skip the power/sample-size calculation for RCTs.
- Do NOT use vague outcome descriptions ("we measured outcomes"). Name the instrument, range, direction, and MCID.
- Do NOT bury intervention details in supplementary material alone. The main text must contain enough detail for the reader to understand what was done.

## Paragraph structure

| Subsection | Paragraphs | Job |
|-----------|-----------|-----|
| Study Design | 1-2 | Design name, ethics, reporting standard, protocol reference |
| Participants | 1-2 | Inclusion criteria with thresholds, exclusion criteria |
| Randomization | 1 | Method, stratification, blinding (RCTs) |
| Interventions | 2-4 | Each arm described in detail, sub-subsections per arm |
| Outcomes (Primary) | 1-2 | Instrument, range, direction, MCID |
| Outcomes (Secondary) | 1-2 | List of secondary measures |
| Adverse Events | 1 | How assessed, instruments used |
| Sample Size | 1 | Alpha, power, effect size, target N, attrition adjustment |
| Statistical Analysis | 2-4 | Primary analysis approach, sensitivity analyses, software |
