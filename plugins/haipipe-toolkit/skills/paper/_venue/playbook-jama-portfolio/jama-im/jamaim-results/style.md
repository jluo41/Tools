# JAMA Internal Medicine -- Results Style Guide

Distilled from 11 JAMA IM original investigations (Williams 2025, Desai 2026, Kurlander 2026, Fournier 2026, Hirshberg 2025, Berkowitz 2025, Boone 2026, Seamans 2018, Wen 2020, Taylor 2025, Kroenke 2015, Masterson 2025, Zhang 2026).

## Word budget

- 800-1500 words. Observational studies with many subgroup analyses run longer; RCTs with clean primary/secondary reporting are shorter.
- JAMA IM Results tend to be moderate-length -- the emphasis is on reporting the primary result clearly and early, then secondary/subgroup/sensitivity results in declining order of importance.
- Heavy use of tables and figures to carry quantitative detail, keeping the text narrative rather than data-dump.

### Contrast with JAMA flagship

- JAMA IM Results sections are structured nearly identically to JAMA flagship.
- JAMA IM is slightly more tolerant of subgroup analyses, especially for policy-relevant heterogeneity (by age, region, insurance status).
- JAMA IM papers more frequently use forest plots for subgroup analyses (Masterson 2025, Taylor 2025).

## Subsection structure

Results use colored subheadings. Typical order:

### Observational studies
1. **Characteristics of the Study Sample** or **Study Population** -- N, demographics, covariate balance.
2. **[Primary analysis heading]** -- named for the specific analysis (e.g., "Unadjusted Analysis", "Inverse Probability-Weighted Analysis").
3. **Subgroup Analyses** -- heterogeneity across prespecified subgroups.
4. **Sensitivity Analyses** -- robustness checks.

### RCTs
1. **Participants** or **Participant Flow** -- enrollment, randomization, follow-up completion (references CONSORT flow diagram).
2. **Baseline Characteristics** -- balance across arms (references Table 1).
3. **[Intervention implementation]** (optional) -- engagement, adherence, dose delivered.
4. **Primary Study Outcomes** or **[named outcome]** -- primary endpoint result.
5. **Secondary Outcomes** -- each secondary outcome.
6. **Heterogeneity of Treatment Effect** or **Subgroup Analyses** -- prespecified effect modification.
7. **Sensitivity Analyses** (if applicable).

## Opening paragraph: sample description

The first paragraph always reports:
1. Final analytic sample size.
2. Key demographics (age as median [IQR] or mean [SD]; sex/gender distribution; race/ethnicity if reported).
3. Reference to Figure 1 (flow diagram) and Table 1 (baseline characteristics).

Exemplar opening sentences:
- "The study sample comprised 12 695 280 members of 5 871 003 opioid households and 6 359 639 members of 3 015 932 NSAID households, after excluding 84 810 households (1%) without information on geographic region (Figure 1)." (Seamans 2018)
- "A total of 1524 observations of ED data and 2219 observations of opioid-related inpatient hospitalizations were analyzed." (Wen 2020)
- "Among 19 151 hospitalizations for patients 18 years or older, 3548 (18.5%) were enrolled in the trial population (Figure 1; eTable 8 in Supplement 2). Baseline characteristics were balanced across the usual care (n = 1426) and STAR program (n = 2122) groups (Table 1)." (Taylor 2025)
- "The analysis included 2003 of the 2012 patients randomized between January 4, 2021, and September 27, 2024 (1005 patients to MIH and 998 to TOCC). Median (range) age was 67 (19-98) years, with 1040 (52%) female and 963 male (48%) participants." (Masterson 2025)
- "The sample included 191 269 visits across 311 physicians (eTable 4 in Supplement 1), including 170 526 regular time pressure visits and 20 743 reduced time pressure visits (Table)." (Zhang 2026)

**Signature move**: Sample size is always the very first number in Results. Demographics follow immediately. The flow diagram and Table 1 are cross-referenced in the same paragraph.

## Primary result reporting

The primary result gets its own paragraph or subsection. It is reported with:
1. The effect estimate in clinical units.
2. The 95% CI.
3. The P value (for RCTs) or just the CI (for observational, where non-overlap with null is the signal).

### Number formatting conventions

- Percentages: "11.83% (95% CI, 11.81%-11.85%)"
- Risk differences: "0.71% (95% CI, 0.68%-0.74%)"
- Odds ratios: "adjusted odds ratio [aOR], 1.05; 95% CI, 0.90-1.24; P = .53"
- Mean differences: "mean difference, 1.83; 95% CI, -0.75 to 4.40; P = .16"
- Between-group differences: "between-group difference, -1.9 [95% CI, -3.2 to -0.7] points; P = .002"
- Percentage changes: "9.74% (95% CI, -18.83% to -0.65%) reduction"
- Adjusted SMDs: "adjusted SMD, -0.24; 95% CI, -0.32 to -0.16; P < .001" (Hirshberg 2025)
- Absolute percentage points: "by 1.90 (95% CI, 0.70-3.10) percentage points (pp)" (Boone 2026)
- Crude rates: "1710 of 11 442 patients [14.9%] vs 825 of 11 732 [7.0%]; adjusted absolute difference, 6.9%; 95% CI, 5.7%-8.3%" (Fournier 2026)

**Signature move**: JAMA IM always puts the CI alongside the effect estimate. P values are reported for pre-specified primary comparisons; for observational studies, the CI crossing or not crossing the null is the primary inference mechanism.

### Exemplar primary result sentences

- "The IPW estimated risk of opioid initiation in the subsequent year was 11.83% (95% CI, 11.81%-11.85%) among individuals exposed to prescription opioids in the household, compared with 11.11% (95% CI, 11.09%-11.14%) among individuals exposed to prescription NSAIDs, resulting in a risk difference of 0.71% (95% CI, 0.68%-0.74%)." (Seamans 2018)
- "The post-2014 Medicaid expansions were associated with a 9.74% (95% CI, -18.83% to -0.65%) reduction in the rate of opioid-related inpatient hospitalizations." (Wen 2020)
- "There was no difference in the 90-day composite all-cause readmission or death among patients in the STAR group vs those in the usual care group (1023 [48.2%] vs 684 [48.0%]; adjusted odds ratio [aOR], 1.05; 95% CI, 0.90-1.24; P = .53)." (Taylor 2025)
- "The RMDS score decreased by 1.7 (95% CI, -2.6 to -0.9) points from baseline to 9 months in the usual care group and by 3.7 (95% CI, -4.5 to -2.8) points in the intervention group (between-group difference, -1.9 [95% CI, -3.2 to -0.7] points; P = .002)." (Kroenke 2015)

## Null results reporting

JAMA IM reports null results plainly, without spinning them as positive:
- "We did not find any statistically significant change in the rate of opioid-related ED visits associated with implementation of either the post-2014 Medicaid expansions (-3.98%; 95% CI, -14.69% to 6.72%) or pre-2014 Medicaid expansions (1.02%; 95% CI, -5.25% to 7.28%)." (Wen 2020)
- "There was no difference..." (Taylor 2025)
- "no adjusted differences were observed..." (Masterson 2025)
- "There was no significant difference in the total number of prescriptions..." (Zhang 2026)

**Signature move**: Null results include the CI explicitly so the reader can assess the range of effects compatible with the data. The word "significant" is used in the statistical sense, never the colloquial sense.

## Subgroup analyses

Reported under a separate subheading. For each subgroup:
1. Name the subgroup variable and categories.
2. Report the stratum-specific estimates with CIs.
3. Note whether heterogeneity was statistically significant (interaction P value).

Exemplar:
- "The RD among younger adults ages 18 to 25 years was 0.91% (95% CI, 0.81%-1.01%), compared with 1.26% (95% CI, 1.08%-1.43%) among those ages 26 to 35 years." (Seamans 2018)
- "There was no evidence of effect modification of the STAR treatment effect by patient age, SOFA score, Charlson Comorbidity Index score, or distance from home to nearest hospital." (Taylor 2025)

## Sensitivity analyses

Briefly reported, usually one paragraph. Confirms or qualifies the primary result.
- "In 2-adult households (n = 2 706 922), an opioid prescription to 1 adult was associated with increased risk of opioid initiation in the other (RD, 1.08% [95% CI, 0.90%-1.39%])." (Seamans 2018)
- "Similar results were found for all sensitivity analyses for the primary outcome." (Taylor 2025)

## Signature moves

1. **One result per sentence**: Each sentence carries exactly one effect estimate. No sentence contains two different comparisons or outcomes.

2. **Table/figure cross-references**: Results text points to tables/figures but does not repeat every number in the table. Pattern: "Results varied across characteristics of the index prescription (Table 3)."

3. **Clinical translation**: For RCTs, effect sizes are sometimes translated to clinical meaning: "which translates to approximately 5 fewer hospital discharges per 100 000 population per quarter" (Wen 2020).

4. **Covariate balance summary**: For observational studies, baseline balance is summarized narratively: "Overall, baseline covariates were balanced between household exposure groups." For RCTs: "Baseline characteristics were balanced across groups (Table 1)."

5. **Past tense throughout**: All results are in past tense. Present tense is never used.

## Anti-patterns

- Interpreting results in the Results section (interpretation belongs in Discussion).
- Using "significant" without specifying "statistically significant" or providing the CI/P value.
- Reporting only P values without effect sizes.
- Including methods information (e.g., "we adjusted for...") in Results paragraphs.
- Presenting results in a different order from the Methods section's analytic plan.
- Using causal language ("reduced", "caused", "prevented") for observational results. Use "was associated with".
- Spinning null results as positive (e.g., "although not significant, there was a trend toward..."). Report the estimate and CI plainly.
- Burying the primary outcome result after secondary analyses.
