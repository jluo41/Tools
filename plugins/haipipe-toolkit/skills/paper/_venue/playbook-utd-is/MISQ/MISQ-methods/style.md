# MISQ Methods -- Section Style Guide

Extracted from MISQ Research Article exemplars. Supplements `style-profile.md`.

Called "Data and Variables," "Methodology and Results," "Empirical Setting and Data," "Data and Measures," or "Study N: Experiment" depending on research design. MISQ methods sections are detailed but subordinate to theory; they exist to convince the reader the theoretical predictions were tested fairly.

## Word budget

- 2,000-4,000 words (4-8 published pages two-column) for a single-study archival paper.
- Multi-study papers (Yin 2014: three studies) repeat the methods block per study, totaling 4,000-6,000 words across all studies.
- Liu (2021): ~2,500w for "Data And Variables" + "Hypotheses Testing" subsections (pp. 1121-1124).
- Gao (2015): ~2,000w for "Methodology and Results: Data and Measures" (pp. 13-16).
- Yin (2014): ~1,500w per study for methods portions of Study 1, 2, and 3.

## Arc

```
data description (source, scope, sample construction)
  -> variable operationalization (DV, IVs, controls, with table)
  -> model specification (equation displayed, estimation method named)
  -> endogeneity / identification discussion
  -> validation checks (for novel measures)
```

## Signature moves

1. **Data description opens with source and sample construction logic.** The first paragraph of the methods section names the data source, the population, the time window, and the sample construction steps (inclusion/exclusion criteria). The rationale for each restriction is stated.
   - "We used the Yelp Academic Dataset, which provides the business profiles, reviewer profiles, and review contents of the closest 250 businesses to 30 universities across 15 states in the U.S. We focused on the 'restaurant' category because it is the top business type on Yelp. We removed reviews with fewer than 50 words because the NLP algorithm requires outputs from the Linguistic Inquiry and Word Count (LIWC) program." [Liu 2021]
   - "We conduct empirical tests of our hypotheses using a novel dataset constructed from four sources of data." [Gao 2015]

2. **Variable operationalization table.** A table (usually Table 2) lists every variable with its operationalization, mean, and SD. This is not optional in MISQ empirical papers. The table is referenced in the text with a sentence like "Table 2 summarizes our variables and provides descriptive statistics." [Liu 2021]
   - Liu (2021): Table 2 -- Variable, Operationalization, Mean, SD.
   - Gao (2015): Variables described in prose with a separate summary statistics table.
   - Yin (2014): Table 6 -- Variable Type, Variable Level, Variable, Operationalization, Notes.

3. **Model equation displayed.** The regression equation is shown as a numbered display equation, not buried in prose. The DV, IVs, and controls are named in the equation.
   - "Helpfulness_ij = beta_0 + beta_1(Openness_ij) + ... + beta_{6-22}(Controls_ij) + epsilon_ij" (Equation 1) [Liu 2021]
   - "log(Pr(Rated Online) / 1-Pr(Rated Online)) = alpha_1 + beta_1 Physician Quality + X'delta_1 + M'theta_1 + v" (Equation 1) [Gao 2015]

4. **Endogeneity discussion as a dedicated subsection or block.** MISQ empirical papers address endogeneity directly, naming the specific threat and the mitigation strategy. This is not buried in a footnote.
   - "Although we have included a comprehensive set of controls, there may be unobservable restaurant factors that influence both personality scores and helpfulness votes. ... We used an instrumental variables (IV) approach to address this concern." [Liu 2021]
   - "To ensure empirical rigor we include a robust set of controls to account for unobserved heterogeneity which may bias estimation." [Gao 2015]

5. **Novel-measure validation.** When the paper introduces a novel measure (e.g., personality inferred from text), a dedicated validation subsection demonstrates that the measure captures the intended construct. This includes within-vs-across variance comparisons, correlation with known benchmarks, or convergent/discriminant validity evidence.
   - "Given that the predicted personality traits are based on the review text, we further conducted a validation test to confirm that those traits measured in this way indeed reflect the reviewer's traits rather than the review's characteristics. We achieved this by comparing the variance of personality scores within the reviewers to that across reviewers." [Liu 2021]

6. **Controls organized by group.** Control variables are presented in logical groups (reviewer characteristics, review characteristics, product/contextual characteristics) rather than as a flat list. Each group gets a brief justification paragraph.
   - "Those controls belong to three groups: reviewer characteristics (other than personality traits), review characteristics, and product (restaurant) characteristics." [Liu 2021]

## Exemplar sentences (shape, not content)

**Data source opening**:
- "We used the Yelp Academic Dataset, which provides the business profiles, reviewer profiles, and review contents of the closest 250 businesses to 30 universities across 15 states in the U.S." [Liu 2021]
- "We conduct empirical tests of our hypotheses using a novel dataset constructed from four sources of data. First, we use data from the consumer advocacy group Consumer's Checkbook which provides a representative sample of patients' perceptions of Physician Quality." [Gao 2015]

**Sample construction rationale**:
- "We removed reviews with fewer than 50 words because the NLP algorithm requires outputs from the Linguistic Inquiry and Word Count (LIWC) program, which calls for 'a certain degree of skepticism' on any text containing fewer than 50 words." [Liu 2021]
- "To further limit unobserved heterogeneity, we restrict the sample to general practitioners and family care physicians." [Gao 2015]

**Variable definition**:
- "Review helpfulness is measured as the total number of helpfulness votes for each review." [Liu 2021]
- "The dependent variable of interest, review helpfulness, was operationalized as follows. Below each review, Yahoo! Shopping presents the question 'Was this review helpful?' along with yes and no options." [Yin 2014]

**Endogeneity threat naming**:
- "Although we have included a comprehensive set of controls, there may be unobservable restaurant factors that influence both personality scores and helpfulness votes. ... Such a difference in writing can result in different personality scores for the same reviewer because the scores are calculated based on the review texts." [Liu 2021]

**IV strategy**:
- "We used an instrumental variables (IV) approach to address this concern. The key to this approach is to find instruments that provide an exogenous source of variation for the endogenous variables (personality traits). We constructed two sets of IVs." [Liu 2021]

## Anti-patterns

- Do NOT skip the endogeneity discussion. Even if the identification strategy is not bulletproof, naming the threat and stating the mitigation is mandatory.
- Do NOT present variables without a summary table. The operationalization table is a MISQ convention.
- Do NOT hide the model equation in prose. Display it as a numbered equation.
- Do NOT describe measurement details in the theory section. The theory derives predictions from constructs; the methods section operationalizes those constructs.
- Do NOT describe results in the methods section (exception: Gao 2015 combines "Methodology and Results" -- this is less common and usually reserved for papers with very short methods).
- Do NOT omit sample construction rationale. Every restriction (time window, minimum observations, category focus) needs a stated reason.

## Paragraph structure

| Subsection | Paragraphs | Job |
|-----------|-----------|-----|
| Data | 2-3 | Source, time window, sample construction, descriptive stats |
| Variables (DV) | 1 | Define and operationalize the dependent variable |
| Variables (IV) | 1-2 | Define and operationalize the independent variables, reference Table 2 |
| Variables (Controls) | 1-2 | Groups of controls with brief justification |
| Validation (if novel measure) | 1-2 | Demonstrate the measure captures what it claims |
| Model Specification | 1-2 | Display equation, name estimation method |
| Endogeneity / Identification | 2-3 | Name threat, describe IV or other mitigation, report first-stage diagnostics |

For multi-study papers, each study gets its own Methods subsection following this pattern at compressed length.

---

## Enriched from additional exemplars (2026-06-29)

Source papers: Zhang (2025), Weng (2026), Ayabakan (2025), Raimi (2025), Liu-EBM (2025), Liu-HMM (2025).

### Section naming variants (expanded)

- "Methodology" with subsections "Research Context" / "The Introductory Incentive Policy" / "Data and Measures" / "Empirical Models" [Zhang 2025]
- "Method" with subsections "Sample and Participants" / "Procedure" / "Measurement" / "Measurement Validity" [Weng 2026]
- "Data and Methodology" with subsections "Data Sources and Measures" / "Empirical Specification" [Ayabakan 2025]
- "Study 1: Effects on Judgmentalness" > "Method" with "Participants" / "Task" / "Treatments" / "Measures" [Raimi 2025]
- "Hidden Markov Model of AI Delegation Dynamics" with subsections "Research Context" / "Model Setting" / "Data and Variable Description" [Liu-HMM 2025]

### Additional signature moves

7. **Research context as a standalone subsection for platform/policy papers.** Healthcare and platform papers dedicate a standalone subsection to describing the institutional context (the OHC platform, the hospital system, the retail company) BEFORE data and variables. This subsection explains how the platform works, the policy mechanism, and why it provides a suitable research setting.
   - Zhang (2025) devotes ~800w to "Research Context" describing how the OHC works (fee structure, consultation process, physician incentives) and then a separate ~400w subsection on "The Introductory Incentive Policy" explaining the specific quasi-experiment.
   - Liu-HMM (2025) describes the retail company's AI replenishment system, how managers interact with it, and the weekly KPI meetings.

8. **Platform screenshot or interface figure.** Healthcare platform papers include a Figure showing the actual platform interface (a physician's community page, a consultation screen) to make the institutional context tangible.
   - "Figure 1 shows an example of a physician's community page." [Zhang 2025]

9. **Coarsened exact matching (CEM) as standard identification strategy.** CEM has become a standard identification strategy in MISQ healthcare papers, replacing or supplementing propensity score matching (PSM). Papers describe the matching process, the matching variables, the resulting sample sizes for treatment and control groups, and balance statistics.
   - "Our CEM matching process yielded a total of 1,668 physicians -- 834 enrolled from April to June 2016 (the treated group) and 834 enrolled from April to June 2015 (the control group)." [Zhang 2025]
   - Ayabakan (2025) uses CEM at the hospital level and PSM at the patient-visit level.

10. **DID with temporal variation.** Difference-in-differences designs now commonly exploit temporal policy changes (initiation AND termination) with separate models for each phase.
    - Zhang (2025) displays two DID equations: Equation (1) for policy initiation (Treated x Double) and Equation (2) for policy termination (Treated x AfterDouble).

11. **Multi-level fixed effects specification.** Healthcare claims-data papers specify multiple layers of fixed effects: patient, hospital, year-quarter, with cluster-robust standard errors.
    - "We controlled for patient (mu_p), hospital (phi_h), and year-quarter (lambda_q) fixed effects and cluster error terms (epsilon) at the patient level." [Ayabakan 2025]

12. **Construct definitions table with formal sources.** Survey-based papers include a "Construct Definitions" table that maps each construct to its formal definition and adapted source.
    - Weng (2026) Table 2 lists all 8 constructs (product performance, process performance, requirement risk, project complexity risk, internal/external process control, team stability, team plasticity) with definitions and adapted sources.

13. **Personality measurement operationalization.** For personality-based papers, the methods section specifies: (a) which instrument (NEO-PI-R, Big Five Inventory, LIWC), (b) how individual scores are aggregated to the team level if applicable (mean), (c) reflective vs. formative modeling rationale, and (d) within-group agreement statistics (rwg, ICC).
    - "We used the Big Five scale from Costa and McCrae (1992) ... We aggregated the personality responses to the team level by combining all responses of the team members and using the additive index (mean) approach (Chan, 1998)." [Weng 2026]

14. **PLS-SEM for moderated models.** Weng (2026) uses Partial Least Squares (PLS) instead of OLS/MLE, justified by: (a) no distributional assumptions, (b) ability to handle both formative and reflective measurements. This is a valid alternative estimation method in MISQ for complex moderation models.

15. **Multi-study methods with per-study method sections.** Multi-study experimental papers (Raimi 2025) present a complete "Method" subsection within each Study section, including Participants, Task, Treatments, Measures. Each is self-contained.
    - Raimi (2025) Study 1 methods: participants (N=300 MTurk), task (vignette), treatments (chatbot vs. human), measures (7-point Likert scales + new judgmentalness scale).

16. **Power analysis.** Experimental MISQ papers now routinely report a priori power analysis results.
    - "A power analysis using G*Power (Faul et al., 2007) showed that the design had a power of 95% to find a medium-sized effect (f = 0.25) and 78% to find a small effect (f = 0.15)." [Raimi 2025]

### Design science methods variant

Liu-EBM (2025) uses a fundamentally different methods structure for computational design:
- **Architecture description** replaces variable operationalization: Figure 1 shows the system architecture with named modules.
- **Mathematical formalization** replaces regression equations: equations define the model components (prototypes, distance functions, loss functions).
- **Evaluation strategy** replaces endogeneity discussion: benchmarking + ablation + downstream application.
- **Dataset description** replaces sample construction: training/test splits, labeling procedures, inter-annotator agreement (kappa scores).

### Updated anti-patterns

- Do NOT skip the institutional/research context subsection in healthcare or platform papers. Reviewers need to understand how the platform works before evaluating the identification strategy.
- Do NOT present CEM or PSM matching without reporting balance statistics. Post-matching balance is mandatory.
- Do NOT omit power analysis in experimental MISQ papers. It is now standard.
- Do NOT use PLS without justifying why it is preferred over OLS/MLE for the specific model.

### Exemplar sentences from new papers

**Data source opening (healthcare)**:
- "Our study was conducted in a leading OHC in China. Since launching in 2006, this OHC has attracted about 260,000 physicians from accredited hospitals and medical institutions throughout the country" [Zhang 2025]
- "We utilized a large-scale dataset from the Maryland Health Services Cost Review Commission (HSCRC) outpatient records." [Ayabakan 2025]

**Sample construction rationale**:
- "We focused on the physician's reply to the first patient question only to estimate the policy impact." [Zhang 2025]
- "Since we focused on claim denials, we only considered claims with available payer information (i.e., Medicare, Medicaid, or private insurance). Hence, we excluded claims for patients who paid for care by themselves or did not have insurance." [Ayabakan 2025]

**CEM description**:
- "We further used a coarsened exact matching (CEM) approach with k2k restrictions to construct comparable physicians across the treated and control groups." [Zhang 2025]

**Fixed effects specification**:
- "We also incorporated the month-fixed effect ... and physician-fixed effects." [Zhang 2025]

**Personality measurement**:
- "We used the Big Five scale from Costa and McCrae (1992), which is a widely used measurement. ... Team stability comprises three traits: conscientiousness, agreeableness, and emotional stability (opposite of neuroticism), and team plasticity comprises the two other traits: extraversion and openness to experience." [Weng 2026]
