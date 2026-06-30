# Nature Medicine Methods -- Section Style Guide

Extracted from 14 Nature Medicine exemplar papers (2025-2026). Supplements `style-profile.md`.

## Word budget

- 1,500-5,000+ words, spanning 3-8 pages. Highly variable by study type.
- bean-2026: ~1,800w (12 subsections). brinton-2026: ~2,500w (11 subsections). saab-2026: ~3,000w (8 subsections). varoquaux-2026: ~2,000w (9 subsections). tao-2026: ~2,000w (6 subsections with nested sub-headings). osullivan-2026: ~1,500w (4 subsections). lang-2026: ~2,000w (9 subsections). nijman-2026: ~3,500w (14 subsections). lu-2026: ~2,000w (7 subsections). khasentino-2025: ~4,000w (13 subsections). bedi-2026: ~5,000w (extensive taxonomy listing). zhou-2026: ~3,000w (8 subsections). restrepo-2026: ~600w (6 subsections, Brief Communication). levine-2026: ~600w (single continuous section, Brief Communication).
- Methods is often the longest section, frequently exceeding Results in word count. Much additional detail is deferred to Supplementary Information.

## Placement

Methods is placed AFTER Discussion at the end of the main text. This is mandatory Nature-family ordering:

```
... -> Discussion -> Methods -> Reporting summary -> Data availability -> Code availability -> References
```

All 14 exemplars confirm this placement. The section is labeled **"Methods"** (not "Online Methods").

## The "Online content" convention

Many Nature Medicine papers include a standard boilerplate paragraph before the References that reads:

> "Any methods, additional references, Nature Portfolio reporting summaries, source data, extended data, supplementary information, acknowledgements, peer review information, details of author contributions and competing interests; and statements of data and code availability are available at [DOI URL]."

This does NOT mean the Methods are absent from the main text. Papers include Methods in the main text AND have this Online content pointer. The pointer signals that supplementary methods exist at the URL.

## Arc

```
Study design / overview (what type of study, how structured)
  -> Participants / eligibility (who was included, how recruited)
  -> Intervention / system description (what was tested)
  -> Randomization, allocation, blinding (for RCTs)
  -> Outcomes (primary, secondary, how defined)
  -> Sample size calculation
  -> Data collection and monitoring
  -> Statistical analysis (pre-specified and post hoc)
  -> Ethics and oversight
  -> Reporting summary (Nature checklist)
  -> Data availability
  -> Code availability
```

The Methods section reads as a clinical study protocol: study design first, then participants, then intervention, then analysis. For AI system papers, the system architecture replaces the intervention description, and dataset provenance replaces participants.

## Signature moves

1. **Structured clinical study design subsections.** RCT papers follow a near-standardized subsection hierarchy:
   - "Design" / "Participants" / "Interventions" / "Randomization, allocation and blinding" / "Outcomes" / "Sample size" / "Data collection, management and monitoring" / "Statistical analysis" [brinton-2026]
   - "Study design" / "Participants" / "AI algorithm" / "Safety and discordance" / "Sample size" / "Statistical analysis" / "Ethical and safety considerations" [varoquaux-2026]
   - "Ethics approval" / "Co-designed architecture and clinical integration" / "Randomized controlled trial" / "Statistical analysis" [tao-2026]

2. **Explicit clinical trial reporting standards referenced.** Papers name the reporting guideline:
   - "Reporting followed the Consolidated Standards of Reporting Trials (CONSORT)-AI extension for clinical trial reports for interventions involving artificial intelligence and the CONSORT 2010 statement: extension to cluster randomised trials." [brinton-2026]
   - "This review was conducted and reported in accordance with the Preferred Reporting Items for Systematic Reviews and Meta-Analyses (PRISMA) 2020 guidelines." [lu-2026]
   - TRIPOD guidelines for prediction model studies [nijman-2026]

3. **Detailed ethics and oversight subsections.** Ethics coverage is more extensive than NMI:
   - Named ethics committee with approval number: "The study received ethics approval from the Amref Health Africa Ethical and Scientific Review Committee (P1817/2025), with additional authorization from Nairobi (NCCG/HWN/REC/752) and Kiambu (HRDU/PAA/04/2025) counties and from the National Commission for Science, Technology and Innovation (P/25/416731)." [brinton-2026]
   - Regulatory body determination: "The Kenyan medical device regulator (the Pharmacy and Poisons Board) determined that the product fell outside its oversight scope, and thus no local equivalent to an 'investigational device exemption' was submitted." [brinton-2026]
   - Informed consent statement: "Written informed consent was obtained from clinical officers before enrollment." [brinton-2026]
   - Data Safety Monitoring Board (DSMB) described: "The DSMB conducted scheduled safety reviews during the study, including an early review after enrollment of the first 1,000 participants." [brinton-2026]
   - Declaration of Helsinki: "This study adhered to the principles outlined in the Declaration of Helsinki." [osullivan-2026]

4. **Ethics and inclusion statement (separate subsection).** Some papers include an explicit equity statement:
   - "This study was codesigned and implemented with local researchers and clinicians in Kenya, who were actively involved in study conception, protocol development, contextual adaptation of the intervention, data collection and analysis, interpretation and manuscript writing." [brinton-2026]

5. **Sample size calculation with power analysis.** RCTs include explicit sample size rationale:
   - "The sample size calculation accounted for clustering at the clinical officer level and was powered to detect a 50% relative reduction in treatment failure within 14 days, from an expected failure proportion of 2% in the control arm to 1% in the intervention arm. Assuming a design effect of 1.5, 80% power, a two-sided alpha of 0.05 and 10% loss to follow-up, the target enrollment was 9,000 patient encounters..." [brinton-2026]
   - "Based on data from previous work, the median time to lung cancer diagnosis was 63 days in the standard reporting group and using a conservative reduction of 10 days, we calculated that 265 cases per group would be needed to detect a difference with 95% power." [varoquaux-2026]

6. **Statistical analysis subsections with pre-specification.** The statistical approach is described in detail:
   - Analysis population: "The primary analyses followed the ITT principle at the level of the randomized clinician cluster." [brinton-2026]
   - Missing data handling: "Missing outcomes were handled using complete-case analysis given the low proportion of missing data." [brinton-2026]
   - Model specification: "For binary outcomes (including the primary outcome), a mixed-effects logistic regression model was used to estimate the aOR, with its corresponding 95% CI." [brinton-2026]
   - Multiple testing: "All tests were two-sided at alpha = 0.05." [varoquaux-2026]; "Holm-Bonferroni correction" [restrepo-2026]
   - Software: "Analyses were conducted in R (version 4.5.1)." [brinton-2026]; "STATSMODELS v0.14.3 and SCIPY v1.13.0 packages in Python" [bean-2026]; "Stata/MP 19.5 (StataCorp)." [varoquaux-2026]

7. **Reporting summary as mandatory closing subsection.** Every paper includes:
   - "Reporting summary: Further information on research design is available in the Nature Portfolio Reporting Summary linked to this article." [standard boilerplate]

8. **Data availability and Code availability as mandatory closing subsections.**
   - Data: URL or access instructions, often tiered (public subset + restricted clinical data)
   - Code: GitHub URL, sometimes with Zenodo DOI for archival
   - "All data for the study is stored by the study sponsor. Access to fully anonymised data can be requested from the sponsor at: [address]." [varoquaux-2026]
   - "The datasets generated by the research in the current study are available at https://github.com/am-bean/HELPMed" [bean-2026]
   - "The code supporting this study is publicly available at https://github.com/nyuolab/clinical-llm-benchmarks." [restrepo-2026]

## Exemplar sentences (shape, not content)

**Study design opening**:
- "We conducted a pragmatic, multicenter, parallel-group cluster-randomized controlled trial across a network of 16 primary care facilities operated by Penda Health in Nairobi and Kiambu counties in Kenya..." [brinton-2026]
- "A prospective, multicenter, randomized controlled trial was conducted between July 2023 and December 2024 across five NHS Trusts in England." [varoquaux-2026]
- "The study employed a between-subjects design with three treatment groups and a control." [bean-2026]

**Ethics statement**:
- "The study received ethics approval from the Amref Health Africa Ethical and Scientific Review Committee (P1817/2025)..." [brinton-2026]
- "This study was approved by the NYU Langone Institutional Review Board (i23-00510)." [restrepo-2026]
- "The study protocols followed in this study were approved by the Departmental Research Ethics Committee in the Oxford Internet Institute (University of Oxford) under project number OII_CIA_23_096." [bean-2026]

**Statistical method sentence**:
- "For all analyses, random effects were used to enable clustering by clinical officer and facility." [brinton-2026]
- "Comparisons between proportions were computed using chi-squared tests with 1 d.f., equivalent to a two-sided Z-test." [bean-2026]

## Anti-patterns

- Do NOT place Methods before Results. Nature-family ordering puts Methods at the end.
- Do NOT omit ethics approval details for human subjects research. Name the committee, provide the approval number.
- Do NOT omit sample size calculations for clinical trials. Nature Medicine expects explicit power analysis.
- Do NOT omit Data/Code availability subsections. These are mandatory.
- Do NOT omit the Reporting summary pointer. Nature Medicine requires reference to the Nature Portfolio Reporting Summary.
- Do NOT combine methods into Results ("We did X and found Y"). Methods and Results are strictly separate.
- Do NOT omit software version information. Nature Medicine expects exact software versions and statistical packages.
- Do NOT write Methods in passive voice exclusively. Mix active ("We used", "We conducted") with passive ("was estimated", "were computed").
- Do NOT omit the clinical trial reporting standard reference (CONSORT, STROBE, PRISMA, TRIPOD as appropriate).

## Paragraph structure

Methods subsections are typically 1-4 paragraphs each, 100-400 words per paragraph. Each subsection covers one methodological component completely. The internal structure:

1. **What** (1 sentence): name the design element
2. **How** (2-6 sentences): describe the implementation with specific details
3. **Rationale** (0-1 sentences): why this approach was chosen (optional, often deferred to supplement)

## Contrast with NMI

- NMI Methods focus on neural network architecture, training protocol, and dataset provenance. Nature Medicine Methods focus on clinical study design, participants, interventions, randomization, and ethics.
- NMI includes formal equations in Methods. Nature Medicine rarely includes equations (unless the statistical model is non-standard).
- NMI describes hyperparameters exhaustively (learning rate, batch size, optimizer). Nature Medicine describes clinical protocol details exhaustively (eligibility criteria, blinding procedure, outcome definitions, adverse event monitoring).
- Both venues include Data/Code availability and Reporting summary as mandatory closing subsections.
- NMI Methods never mention ethics committees by name. Nature Medicine Methods always name ethics committees with approval numbers for human subjects research.
- NMI defers extended methods to Supplementary. Nature Medicine also defers but includes more clinical study design detail in the main text.
- Both venues label the section "Methods" (not "Online Methods") and place it after Discussion.
- Nature Medicine uniquely includes sample size calculations, DSMB descriptions, clinical trial registration, and reporting standard references (CONSORT-AI, PRISMA, TRIPOD).
