# Diabetes Care -- Results Style Guide

Distilled from 10 Diabetes Care papers: Galindo 2026 (RCT/Brief), Reaven 2026 (TTE), Bergenstal 2026 (GRADE), Lehmann 2026 (ML/Brief), Zheng 2025 (NLP), Kahkoska 2025 (e-Letter), He 2026 (e-Letter), Godneva 2026 (TIR), Ajjan 2026 (gDAC), Dupenloup 2026 (cost-effectiveness).

## Word budget

- Original Article: 1000-2000 words. RCTs and TTE studies with subgroup/sensitivity analyses run longer; NLP accuracy papers are shorter.
- Brief Report: 400-700 words.
- e-Letters: ~300-600 words woven into body text (no section heading).

## Section heading

**RESULTS** (all caps).

## Subsection structure

Results use **bold, title-case** subheadings. Typical patterns:

### Clinical/observational studies
1. **Participant Characteristics** or **Study Population** -- N, demographics, reference to Table 1 and flow diagram.
2. **[Primary analysis heading]** -- named for the specific outcome (e.g., "Mortality Outcomes", "Primary Outcomes").
3. **[Secondary outcomes]** -- each secondary analysis.
4. **Subgroup Analyses** or **Sensitivity Analyses** -- heterogeneity, robustness.

Reaven 2026: Participant Characteristics / Mortality Outcomes / Interim Events and Negative Outcomes.
Godneva 2026: Study Population / Time Spent in Glycemic Ranges in Adults Without Diabetes / Relationship of TIR and TITR With Other CGM-Derived Measures / Time Across Glycemic Ranges and Its Association With Clinical Parameters / Time Across Glycemic Ranges and Its Association With Long-term Outcomes.

### ML/NLP studies
1. **Clinical Results** -- sample description, demographics.
2. **[Model performance by task/condition]** -- results for each experiment or pipeline component.

Lehmann 2026: Clinical Results / Proof-of-Concept and Exploratory Results (Spilot) / Voice-Based Detection of Hypoglycemia (Smain).

### Cost-effectiveness studies
1. **Base Case** -- primary cost-effectiveness results.
2. **Sensitivity Analyses** -- one-way, two-way, probabilistic.

### Brief Reports and e-Letters
No subsection headers. Results flow as continuous paragraphs.

## Opening paragraph: sample description

The first paragraph always reports:
1. Final analytic sample size.
2. Key demographics (age as mean +/- SD or median [IQR]; sex distribution; race/ethnicity if reported).
3. Reference to Figure 1 (flow diagram) and Table 1 (baseline characteristics).

Exemplar opening sentences:
- "Among 52 participants enrolled, 39 were included in the analysis. We excluded 13 participants who lost the CGM sensors or devices, were hospitalized, had acute illness, or could not complete the required CGM data collection or study procedures (Supplementary Fig. 1). The sample's mean age was 57.15 +/- 9.3 years, 63% (n = 33) were women, and mean HbA1c was 7.18% +/- 1.3 (54 mmol/mol) (Table 1)." (Galindo).
- "The flow of participants from eligibility to the final cohort is shown in Fig. 1. Participants included people with diabetes who had their second endocrine visit occurring between 2017 and 2020. Of these, 11,180 were identified as T1D. After applying inclusion and exclusion data (noted above), 8,423 remained and were enrolled as clones assigned to both treatment groups." (Reaven).
- "Twenty-two participants (Spilot n = 6, Smain n = 16) (Table 1) provided 540 voice recordings." (Lehmann).

**Signature move**: Sample size is always the very first number in Results. Demographics follow immediately. Table 1 and flow diagram are cross-referenced in the opening paragraph.

## Primary result reporting

The primary result gets its own paragraph or subsection. It is reported with:
1. The effect estimate in clinical units.
2. The 95% CI or P value.
3. Comparison groups clearly identified.

### Number formatting conventions

- **Mean +/- SD**: "57.15 +/- 9.3 years" (Galindo), "37.3 +/- 12.4 years" (Lehmann).
- **n (%)**: "33 (63)" (Galindo), "19 (37) male" (Galindo).
- **P values**: "P = 0.28" (Galindo), "P < 0.001" (Galindo), "P = 0.015" (Reaven). Always italic *P*, no leading zero.
- **95% CI**: "95% CI 0.71-0.97" (Reaven), "(95% CI 0.72, 0.97)" (Reaven -- comma-separated variant).
- **Risk ratios**: "adjusted risk ratios of 0.90 (95% CI 0.71-0.97) to 0.84 (CI 0.72-0.97)" (Reaven).
- **Odds ratios**: "odds ratio [OR] 3.25; 95% CI 2.94-3.60" (Kahkoska).
- **AUROC**: "AUROC 0.90 +/- 0.12" (Lehmann).
- **Accuracy**: "99.87% for Libre and 100.00% for Dexcom" (Zheng).
- **CGM metrics**: "%TIR was higher (63.4% +/- 24 vs. 54.5% +/- 23)" (Galindo).
- **Cost-effectiveness**: "$27,400 per QALY gained" (Dupenloup).

### Exemplar primary result sentences

- "The %TBR <70 mg/dL was not significantly different between groups (mean 1.17% +/- 1.8 vs. 1.29% +/- 2.7; P = 0.28)." (Galindo).
- "Mortality was lower with CGM initiation, yielding adjusted risk ratios of 0.90 (95% CI 0.71-0.97) to 0.84 (CI 0.72-0.97) over 1-4 years of follow-up." (Reaven).
- "This translated into an AUROC of 0.90 +/- 0.12 for the read-aloud task (Fig. 3A) and 0.87 +/- 0.15 for the diadochokinetic task (Fig. 3B), with high sensitivity and specificity (Fig. 3C)." (Lehmann).
- "When comparing algorithm accuracy with manual review, the accuracy for Libre was 99.87% and, for Dexcom, 100.00%." (Zheng).
- "CGM with RPM cost $27,400 per QALY gained compared with SMBG and dominated CGM alone in the base case." (Dupenloup).

## Null results reporting

Diabetes Care reports null results plainly:
- "The %TBR <70 mg/dL was not significantly different between groups" (Galindo).
- "but effects did not vary by HbA1c, race or ethnicity, or frailty" (Reaven).
- "We found that sustained vowels were ineffective for hypoglycemia detection" (Lehmann).

**Signature move**: Null results include the CI or P value explicitly so the reader can assess precision. No spinning.

## Table/figure cross-reference conventions

- Tables: "(Table 1)", "(Table 2)", "Table 1 depicts the characteristics..."
- Figures: "(Fig. 1A)", "(Fig. 2A and B)", "(Supplementary Fig. 1)"
- "Fig." is abbreviated in both main-text and supplementary references.
- Multi-panel figures referenced with letter: "Fig. 1A", "Fig. 3A and B".
- Caption format: "Figure 1--Description text." with em-dash separator.
- Caption format: "Table 1--Description text." with em-dash separator.

### Exemplar caption
- "Figure 1--Comparison of %TIR during rtCGM (intervention) and CBG testing (SOC) periods in patients with T2D undergoing hemodialysis. A: %TBR <70 mg/dL and <54 mg/dL, %TIR 70-180 mg/dL, and %TAR >180 mg/dL and >250 mg/dL. B: %TAR >180 mg/dL and >250 mg/dL. C: %TBR <70 mg/dL and <54 mg/dL." (Galindo).

## Table conventions

- Table footnote format: "Data are mean +/- SD or n (%)." or "Data are mean +/- SD or n (%) unless otherwise indicated."
- Footnote symbols: *, dagger, double-dagger, section, paragraph marks.
- Continued tables: "Continued on p. XXXX" and "Table 1--Continued" header.
- P values in a dedicated column for comparison tables.

## Signature moves

1. **One result per sentence**: Each sentence carries exactly one effect estimate or comparison.

2. **CGM stacked bar chart as hero display**: The signature Diabetes Care display for CGM papers is a stacked bar chart showing time spent in each glycemic range (Very Low <54, Low 54-70, Target 70-180, High 180-250, Very High >250 mg/dL), color-coded with standardized colors (red/yellow/green/orange).

3. **Table/figure cross-references without repeating every number**: "Changes in glycemic variability parameters are presented in Table 2 and Supplementary Fig. 3." (Galindo).

4. **Past tense throughout**: All results are in past tense. Present tense is never used in Results.

5. **Negative control outcomes**: TTE/observational studies report negative control outcomes to assess residual confounding: "Risk ratios did not differ between groups for incident nondiabetes outcomes, including outpatient and inpatient diagnoses of musculoskeletal or gastrointestinal conditions." (Reaven).

## Anti-patterns

- Interpreting results in the Results section (interpretation belongs in CONCLUSIONS).
- Using "significant" without specifying "statistically significant" or providing the CI/P value.
- Reporting only P values without effect sizes.
- Including methods information ("we adjusted for...") in Results paragraphs.
- Using causal language ("reduced", "caused", "prevented") for observational results. Use "was associated with".
- Spinning null results as positive ("although not significant, there was a trend toward...").
- Burying the primary outcome after secondary analyses.
- Omitting the CGM threshold ranges when reporting TIR/TBR/TAR results.
