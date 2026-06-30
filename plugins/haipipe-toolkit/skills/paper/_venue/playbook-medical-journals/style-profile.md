# Diabetes Care Style Profile (imitate this)

Distilled language style to imitate when writing or editing a Diabetes Care manuscript. Patterns below are pulled from real exemplars in `exemplars/` (Galindo 2026 RCT, Reaven 2026 TTE, Bergenstal 2026 GRADE trial, Lehmann 2026 ML, Zheng 2025 NLP, Kahkoska 2025 claims, He 2026 CGM profiles, Godneva 2026 TIR, Ajjan 2026 gDAC, Dupenloup 2026 cost-effectiveness). Each template names its source.

## Title

Diabetes Care titles are descriptive noun phrases or gerund phrases, often including the study design. Real patterns:

- "Real-Time Continuous Glucose Monitoring Among People With Type 2 Diabetes and End-Stage Kidney Failure Undergoing Maintenance Hemodialysis: A Randomized Clinical Trial" (Galindo 2026).
- "Continuous Glucose Monitoring (CGM) Initiation Is Associated With Reduced Mortality in Older-Onset Type 1 Diabetes Patients: A Target Trial Emulation Study Within the Veterans Health Administration" (Reaven 2026).
- "Listening to Hypoglycemia: Voice as a Biomarker for Detection of a Medical Emergency Using Machine Learning" (Lehmann 2026).
- "Natural Language Processing for Automated Extraction of Continuous Glucose Monitoring Data" (Zheng 2025).
- "Use of a Claims-Based Algorithm to Characterize Uptake of Continuous Glucose Monitoring Among Older Adults..." (Kahkoska 2025).

Title conventions:
- Include the study design after a colon: "A Randomized Clinical Trial", "A Target Trial Emulation Study".
- Associational language is preferred for observational studies: "Is Associated With" not "Causes" or "Reduces".
- Capitalize all major words (title case).
- Abbreviations are defined parenthetically on first use in the title: "Continuous Glucose Monitoring (CGM)".

## Article Highlights box (Diabetes Care signature)

Appears on the graphical abstract page, BEFORE the abstract. Four labeled bullet points, each a question + answer pair:

- **Why did we undertake this study?** -- 1-2 sentences stating the clinical need or gap.
- **What is the specific question we wanted to answer?** -- 1 sentence, the research question.
- **What did we find?** -- 2-3 sentences with the key results including numbers.
- **What are the implications of our findings?** -- 1-2 sentences with clinical/research implication.

### Exemplar Article Highlights

Galindo 2026:
> **Why did we undertake this study?** There is limited evidence on the use of real-time continuous glucose monitoring (rtCGM) in people with type 2 diabetes (T2D) treated with hemodialysis.
> **What is the specific question we wanted to answer?** Would the use of rtCGM improve glycemic outcomes in patients with insulin-treated T2D undergoing hemodialysis?
> **What did we find?** In this randomized controlled trial, we found that percentage time below range was low and not significantly affected by rtCGM use. Compared with capillary blood glucose testing, percentage time in range, percentage time above range, and mean glucose improved during the rtCGM intervention.
> **What are the implications of our findings?** Our results support expanding the use of rtCGM to improve glycemia in people with insulin-treated T2D undergoing hemodialysis.

Reaven 2026:
> **Why did we undertake this study?** Use of continuous glucose monitors (CGM) has been linked with improved glucose control as well as reduced episodes of hypoglycemia and hospitalization in type 1 diabetes. However, there has been little investigation of its possible role in reducing mortality.
> **What is the specific question we wanted to answer?** We examined whether initiation of CGM in the real-world environment in people with type 1 diabetes is associated with changes in mortality.
> **What did we find?** Initiation of CGM in the Veterans Health Administration was associated with lower mortality in people with type 1 diabetes.
> **What are the implications of our findings?** These results reveal that CGM has far more wide-ranging benefits than previously anticipated and provide further support for CGM initiation as standard of care for adult-onset type 1 diabetes.

**Contrast with JAMA**: JAMA uses a 3-item Key Points box (Question / Findings / Meaning) with labeled one-liners. Diabetes Care uses 4 narrative bullets with full-sentence answers.

## Abstract (structured, ADA format)

Four headings in order: **OBJECTIVE** / **RESEARCH DESIGN AND METHODS** / **RESULTS** / **CONCLUSIONS**.

- **OBJECTIVE**: 1-3 sentences. Opens with the clinical context or need, then states the study aim. Can combine motivation + aim in a single block. No separate "IMPORTANCE" heading.
  - "There is a need for improved glycemia monitoring tools for people with type 2 diabetes (T2D) and end-stage kidney failure (ESKF). We aimed to..." (Galindo).
  - "Use of continuous glucose monitors (CGM) improves glucose control and reduces hypoglycemia, but data are lacking for its possible role in reducing other serious clinical events." (Reaven).
  - "Hypoglycemia is a hazardous diabetes-related emergency. We aimed to develop a machine learning (ML) approach for noninvasive hypoglycemia detection using voice data." (Lehmann).

- **RESEARCH DESIGN AND METHODS**: 2-5 sentences. Names the study design, data source, population, and key methods. More compressed than the full Methods section.
  - "We conducted a target trial emulation (TTE) analysis in patients with type 1 diabetes (T1D) comparing all-cause mortality between CGM users and non-CGM users using observational health records from the Veterans Health Administration." (Reaven).
  - "We analyzed CGM reports stored as PDF files from the electronic health record at New York University Langone Health." (Zheng).

- **RESULTS**: 3-6 sentences. Opens with sample size and key demographics, then primary result with effect size and CI/P, then secondary results.
  - "Of the 8,423 individuals initially assigned to both treatment groups, 1,039 were prescribed CGM devices, while 7,399 were not censored or assigned CGM during the grace period. Mortality was lower with CGM initiation, yielding adjusted risk ratios of 0.90 (95% CI 0.71-0.97) to 0.84 (CI 0.72-0.97) over 1-4 years of follow-up." (Reaven).
  - "The %TBR <70 mg/dL was not significantly different between groups (mean 1.17% +/- 1.8 vs. 1.29% +/- 2.7; P = 0.28)." (Galindo).

- **CONCLUSIONS**: 1-3 sentences, cautious. Restates the main finding and its clinical implication.
  - "In adults with T2D and ESKF undergoing hemodialysis, TBR was minimal and not influenced by rtCGM use. Compared with CBG testing, %TIR and %TAR improved during the rtCGM intervention." (Galindo).
  - "In this large TTE of CGM initiation in older T1D patients, CGM use was associated with reduced risk for all-cause mortality." (Reaven).

**Abstract word budget**: ~200-300 words for Original Articles; ~150-200 words for Brief Reports.

## Results sentences

- One result per sentence, past tense, effect in clinical units with 95% CI or P value:
  - "Mortality was lower with CGM initiation, yielding adjusted risk ratios of 0.90 (95% CI 0.71-0.97)" (Reaven).
  - "The %TIR was higher (63.4% +/- 24 vs. 54.5% +/- 23) and mean glucose lower (173.6 +/- 37 vs. 187.7 +/- 38 mg/dL) after the rtCGM intervention" (Galindo).
  - "The ML approach detected hypoglycemia noninvasively with high accuracy (area under the receiver operating characteristic curve 0.90 +/- 0.12)" (Lehmann).
- Mean +/- SD for continuous variables: "mean 57.15 +/- 9.3 years" (Galindo).
- n (%) for categorical: "33 (63%) were women" (Galindo).
- CGM metrics use standard ranges: %TIR 70-180 mg/dL, %TBR <70 mg/dL, %TAR >180 mg/dL, %TAR >250 mg/dL.
- Associational verb for observational: "was associated with". RCTs can use "resulted in" or "improved".

## Discussion

- Opens with principal findings, restating the design + main result:
  - "In this RCT, we demonstrated that using rtCGM for just 30 days improved glycemic control compared with CBG testing (SOC) in people with T2D undergoing hemodialysis." (Galindo).
  - "We demonstrate, in a large national cohort, that initiation of CGM was associated with lower mortality in pwT1D" (Reaven).
- Comparison to prior work with ADA Standards of Care context.
- Mechanisms section with hedging: "may", "could", "one possible explanation".
- Limitations paragraph (not always a separate heading in Diabetes Care; sometimes woven into the final Discussion paragraphs): "We acknowledge some limitations, including a small sample size..." (Galindo).
- Conclusions paragraph at the end: "In conclusion, this study demonstrated that..." (Galindo) or integrated as the final paragraph.

## CGM-specific terminology (Diabetes Care house style)

| Abbreviation | Full term | Standard range |
|---|---|---|
| TIR | Time in range | 70-180 mg/dL |
| TBR | Time below range | <70 mg/dL (Level 1), <54 mg/dL (Level 2) |
| TAR | Time above range | >180 mg/dL (Level 1), >250 mg/dL (Level 2) |
| GMI | Glucose management indicator | Replaces "estimated A1c" |
| MARD | Mean absolute relative difference | Sensor accuracy metric |
| AGP | Ambulatory glucose profile | Standard CGM summary report |
| rtCGM | Real-time CGM | Vs. intermittently scanned (isCGM) |
| isCGM | Intermittently scanned CGM | E.g., FreeStyle Libre |
| CGM | Continuous glucose monitoring | Generic term |
| HbA1c | Hemoglobin A1c | Glycated hemoglobin; subscript "1c" |
| BG | Blood glucose | Venous or capillary |
| CBG | Capillary blood glucose | Fingerstick testing |
| SMBG | Self-monitoring of blood glucose | Fingerstick-based self-testing |
| CV | Coefficient of variation | Glycemic variability metric; target <=36% |

Always define abbreviations on first use in the abstract AND in the main text (they are independent scopes). Use the International Consensus ranges (Battelino 2019, Diabetes Care 42:1593-1603) when reporting TIR/TBR/TAR.

## Reference style

- Vancouver numbered system: references cited as parenthetical numbers (1), (2,3), (1-5).
- "and Associates" used in running headers for papers with >2 authors: "Galindo and Associates", "Reaven and Associates".
- ADA Standards of Care cited as: "American Diabetes Association Professional Practice Committee. N. [Topic]. Standards of Medical Care in Diabetes--[Year]. Diabetes Care [Year];[Vol](Suppl. 1):S[pages]" (Zheng 2025, ref 7).

## Reporting guidelines

- **CONSORT** for RCTs (Galindo 2026 cites ClinicalTrials.gov registration).
- **STROBE** for observational cohort studies.
- **TRIPOD** for prediction/ML models.
- **STARD** for diagnostic accuracy studies.
- Reporting guideline adherence is mentioned in the Methods opening or noted in the supplementary material, but NOT always called out as prominently as in JAMA.

## Supplementary material conventions

- Label: "Supplementary Material" or "Supplementary Data" (not "Supplement 1/2").
- Items use plain labels: "Supplementary Fig. 1", "Supplementary Table 1", "Supplementary Methods".
- Main-text cross-reference pattern: "(Supplementary Fig. 1)" or "(Supplementary Material)" in parentheses.
- Data availability statement: "This article contains supplementary material online at https://doi.org/10.2337/figshare.[ID]." placed in the author information block.
- Deidentified data availability: "Deidentified participant data will be made available 24 months after publication..." (Galindo).

## Figure/table conventions

- Caption format uses em-dash separator: "Figure 1--Caption describing the figure." "Table 1--Caption describing the table."
- Multi-panel figures use bold capital letters: **A**, **B**, **C**, **D** with descriptive subtitles.
- Table footnotes: "Data are mean +/- SD or n (%)." as the standard lead footnote.
- Stacked bar charts for CGM time-in-range distributions are the signature display type.

## Tone and preferences

- Clinical, evidence-based, measured. Less policy-oriented than JAMA IM; more technology-aware.
- First person plural ("We") throughout: "We conducted...", "We aimed...", "We found...".
- Past tense for results, present tense for established facts and conclusions.
- Define all abbreviations on first use; diabetes-specific abbreviations (T1D, T2D, HbA1c) are assumed familiar in Introduction but still defined.
- No hype for ML/AI: frame as a tool or approach, not a revolution. "Our approach" or "the ML approach" not "AI breakthrough".
- ADA Standards of Care as the authority for clinical context, not opinion.

## Enrichment log (filled from exemplars)

- [x] Abstract structure recorded (Galindo, Reaven, Lehmann, Zheng).
- [x] Article Highlights pattern recorded (Galindo, Reaven, Lehmann).
- [x] Title patterns recorded (Galindo, Reaven, Lehmann, Zheng, Kahkoska).
- [x] Results sentence patterns recorded (Galindo, Reaven, Lehmann).
- [x] Discussion opening pattern recorded (Galindo, Reaven).
- [x] CGM terminology table compiled.
- [x] Reference style recorded.
- [x] Supplementary material conventions recorded.
- [x] Figure/table caption format recorded.
- [ ] Exact word limits per article type: verify against current author instructions before final submission.
