# MS-IS Methods Style Guide

MS-IS methods sections emphasize causal identification and economic reasoning about
the identification strategy. The section title varies by paper type: "Empirical
Strategy," "Data and Methodology," "Setting and Experiments," or "Estimation." The
key differentiator is that MS expects the identification strategy to be motivated by
economic theory, not just executed as a statistical technique.

## Section title conventions

| Paper type | Typical title |
|------------|--------------|
| RCT / Field experiment | "Setting and Experiments" + "Empirical Strategy & Main Results" |
| Natural experiment / IV / DiD | "Data" + "Empirical Strategy" or "Identification Strategy" |
| Structural estimation | "Model" (already covered) + "Estimation" |
| Observational + robustness | "Data and Methodology" |

## Word budget

1,500-3,000 words (3-6 double-spaced pages), including data description. Proofs,
robustness tables, instrument details, and extended variable definitions go to the
Online Appendix.

## Arc (subsection structure)

### For RCT / Field experiment papers (Cui et al. pattern)

```
2.   SETTING AND EXPERIMENTS
     2.1  Context description (what is the technology/market/intervention?)
          Enough detail for replication; no unnecessary institutional background.
     2.2  Experimental design
          Randomization unit, sample size, treatment/control, timeline.
          Balance table (Table N) referenced here.
     2.3  Variables and outcome measures
          Primary outcome, secondary outcomes, quality proxies.
          Each variable defined operationally in 1-2 sentences.

4.   EMPIRICAL STRATEGY & MAIN RESULTS
     4.1  Empirical strategy
          Formal specification (numbered equation).
          y_it = beta * D_it + mu_i + gamma_t + epsilon_it    (1)
          Define every term. Name the estimator (OLS, 2SLS, DiD).
          Discuss threats to identification (compliance, spillovers, attrition).
```

### For natural experiment / IV / DiD papers

```
3.   DATA
     3.1  Data source and sample construction
          Name the data provider, coverage, time period, sample restrictions.
          Summary statistics (Table N).
     3.2  Key variables
          Dependent variable, treatment/exposure, controls.
          Each defined with its economic interpretation.

4.   EMPIRICAL STRATEGY
     4.1  Identification strategy
          Name the variation exploited and why it is plausibly exogenous.
          Formal specification with numbered equation.
     4.2  Threats and robustness
          Each endogeneity concern stated in the reviewer's voice:
          "One may argue that [X] is endogenous because [reason]."
          Then the response: "To address this, we [strategy]."
```

### For structural estimation papers

```
3.   ESTIMATION
     3.1  Identification
          Which parameters are identified, and from which variation.
          "The [parameter] is identified from variation in [X] conditional on [Z]."
     3.2  Estimation procedure
          Maximum likelihood, GMM, simulated moments, etc.
          Computational details to Online Appendix.
     3.3  Model fit
          Compare model-predicted moments to data moments.
```

## Signature moves

### Formal specification with every term defined
MS-IS always presents the estimating equation as a numbered display equation, then
defines every variable in the sentence immediately following.

From Cui et al.: "This leaves us with the following regression specification as our
main specification: y_it = beta * D_it + mu_i + gamma_t + epsilon_it. (1) Here,
beta is the coefficient of interest, D_it is an adoption dummy that turns on after a
developer first uses GitHub Copilot, mu_i is a developer fixed effect, and gamma_t is
a week fixed effect."

### Identification strategy as economic argument
Not just "we use IV" but WHY the instrument satisfies exclusion and relevance,
grounded in the economics of the setting.

From Cui et al.: "We exploit the experimental variation and address imperfect
compliance by using assignment to treatment as an instrument for GitHub Copilot
adoption. Hence, we estimate a local average treatment effect (LATE)..."

### Threats stated in the reviewer's voice
Name each endogeneity concern as if a referee raised it, then address it.

Pattern: "One may argue that [X is endogenous / violates parallel trends / suffers
from selection] because [reason]. To [mitigate / address / rule out] this concern,
we [strategy]. [Table/Figure N] shows that [result of the check]."

### Balance and summary statistics tables
Standard displays:
- **Summary statistics table**: Mean, SD, min, max for all variables.
- **Balance table** (for experiments): Mean (control), Mean (treatment), Difference,
  p-value. Report by experiment/site if multi-site.
- **First-stage table** (for IV): Show F-statistic > 10 (Stock-Yogo).

### Online Appendix for heavy machinery
MS-IS moves proofs, extended robustness, additional specifications, instrument
construction details, and data appendix details to the Online Appendix. The body
stays readable. Reference format: "See Online Appendix [A/B/C] for [details]."

## Paragraph structure

Each methods paragraph has one job:

1. **Data paragraph**: Source, coverage, sample restrictions, link to table.
2. **Variable paragraph**: Define the variable, state its economic interpretation,
   cite its use in prior work if novel.
3. **Specification paragraph**: Display equation, define terms, state what the
   coefficient estimates.
4. **Identification paragraph**: Why the variation is plausibly exogenous, what
   the instrument/shock/discontinuity is.
5. **Threat paragraph**: State the concern, describe the robustness check, point
   to the table.

## Anti-patterns

- **No "we use [software] to estimate..."** MS readers do not care about Stata vs. R vs.
  Python. State the estimator (2SLS, maximum likelihood, GMM), not the software.
- **No methods without economic motivation.** "We use propensity score matching" is
  insufficient; state WHY matching addresses the specific selection concern in this
  setting and what the identifying assumption is.
- **No claiming causality without naming the identification strategy.** If the design
  is observational with controls, say "conditional association" or "correlational
  evidence," not "effect."
- **No unreported first-stage.** If you use IV, the first-stage F-statistic must appear
  in the body or a table footnote.
- **No burying the identification assumption.** The exclusion restriction (for IV) or
  parallel trends assumption (for DiD) must be stated explicitly, not implied.
- **No measurement method details that belong in the Data section appearing in the
  Theory section.** The theory takes the construct as given; the methods section explains
  how it is measured.

## Contrast with MISQ/ISR methods

| Dimension | MS-IS | MISQ | ISR |
|-----------|-------|------|-----|
| Identification emphasis | Central; must name strategy | Important but secondary to theory | High; DiD/IV/RD expected |
| Formal equation | Always (numbered) | Sometimes | Usually |
| Balance / first-stage tables | Standard | Rare (unless archival) | Standard |
| Psychometric reporting | Rare (not survey-driven) | CFA, AVE, CR, HTMT standard | Sometimes |
| Online Appendix use | Heavy (proofs, robustness) | Light | Moderate |
| Estimator naming | Economic name (2SLS, MLE, GMM) | Statistical name OK | Economic name preferred |

## Enrichment needs

- [x] Mine Shukla et al. (2021) for a clickstream-data MS-IS methods section (online
  physician reviews, appointment booking) to see how digital-trace data is described.
  **RESOLVED**: See healthcare-data patterns below (Chao/Larkin 2022, Huesmann 2025).
- [x] Mine an MS-IS structural estimation paper to capture the Identification +
  Estimation + Model Fit subsection pattern.
  **RESOLVED**: See Feng 2025 structural estimation pattern below.
- [x] Capture the exact balance-table and first-stage-table formats from a published
  MS-IS paper.
  **RESOLVED**: See table formats below (Cui 2025, Krakowski 2026, Huesmann 2025).

---

## Enriched from additional exemplars (2026-06-29)

Sources: 8 published MS papers (Huesmann 2025, Chao/Larkin 2022, Feng 2025, Cui 2025,
Krakowski 2026, de Kok 2025, Chen 2025, Burtch 2026).

### Section title conventions (additional from published papers)

| Paper | Section title | Design |
|-------|-------------|--------|
| Huesmann 2025 | "3. The Experiment" | Lab-in-field experiment |
| Chao/Larkin 2022 | "3. Empirical Approach and Data" | DiD quasi-experiment |
| Feng 2025 | "3. Descriptive Evidence..." then "5. Structural Analysis..." | Descriptive + structural estimation |
| Cui 2025 | "2. Setting and Experiments" | Multi-site RCT |
| Krakowski 2026 | "4. Research Design, Data, and Method" | Field experiment with DiD |
| de Kok 2025 | "3. A Framework for Using GLLMs..." then "4. Case Study..." | Framework + case study |
| Chen 2025 | "3. Model" then "4. Estimation" | Statistical model + estimation |
| Burtch 2026 | "3. Empirical Evaluations" | Simulation + real-data evaluation |

### Lab-in-field experiment methods (Huesmann 2025)

Healthcare lab-in-field experiments follow a specific subsection arc:

```
3.   THE EXPERIMENT
     3.1  Recruitment and Power Analysis
          - Ethics clearance number and preregistration ID
          - A priori power analysis: effect size, power, alpha,
            correction method, resulting sample size
          - "We assumed a medium effect size (Cohen's d = 0.4),
            a conventional power of 0.8, and a statistical significance
            level of alpha = 0.05"

     3.2  General Design and Decision Situation
          - Describe the task framing ("abstract healthcare tasks")
          - Define effort variable, cost function, outcome mapping
          - State the ability-type assignment procedure
          - Payoff structure and exchange rates

     3.3  Treatment Design (here: Ranking System Designs)
          - Table 1 with visual diagrams of each treatment condition
          - Clear labeling of each system (T, M, TM, MB, TMB)

     3.4  Sample and Protocol
          - Total N, site description, randomization procedure
          - Session logistics (duration, physical setup, computer platform)
          - Payment method: "random-choice payment technique"

     3.5  Behavioral Predictions
          - Translate hypotheses into testable ordinal predictions
          - State expected ordering across conditions:
            "e_{i,h}(T) <= e_{i,h}(TM) <= e_{i,h}(TMB)"
```

### Healthcare prescribing data methods (Chao/Larkin 2022)

Administrative claims data sections follow a specific template:

```
3.   EMPIRICAL APPROACH AND DATA
     3.1  Overall Empirical Approach
          - Name the quasi-experiment and the treatment shock
          - Treatment vs. control: state-level comparison
          - Time window: "July 2007 to June 2011, covering two full
            years preintervention and two full years postintervention"

     3.2  Physicians and Affiliations Data
          - Data provider name and coverage
          - Sample construction rules with specific thresholds
          - Final sample size: "our final list included 5,730 study
            physicians"

     3.3  Prescribing Data
          - Data provider (IMS Health) and what it covers
          - Drug class selection criteria: "nine drug classes: statins,
            antihyperglycemics, proton pump inhibitors..."
          - Unit of observation: "physician-drug-month"

     3.4  Marketing Data
          - Sales force data as a proxy for marketing intensity

     3.5  Disclosure Data
          - Merge procedure with IMS physician data
          - Match rate: "rare cases (< 0.5%)"

     3.6  Data Exclusions
          - Each exclusion stated with rationale
          - "We drop all branded drugs where a generic version was
            introduced in the middle of this time period" (rationale
            for each exclusion)

     3.7  Data Summary
          - Table 3: Summary Statistics with prelaw vs. postlaw columns
          - Note the high rate of zeroes and explain why
```

### DiD specification phrasing (from Chao/Larkin 2022)

The DiD specification is presented as a numbered equation with each term defined
in a sentence below:

```
R_ijt = beta_0 + beta_1 * sunshine_st + beta_2 * branded_jt
      + beta_3 * (branded_jt * sunshine_st) + X_ijt + epsilon_ijt   (1)

The *sunshine_st* variable takes a value of 1 if a sunshine law was
in effect (or in alternative specifications, has been signed or
announced) for that physician-month. The *branded_jt* variable
represents whether a drug is branded with no generic available for
a given drug-month.
```

Key convention: "linear combination" of coefficients is reported separately in tables
for interpretability: "To properly interpret the net effect of the sunshine law on a
branded drug, we will evaluate the linear combination of the coefficients for
sunshine_st and branded_jt * sunshine_st."

### Field experiment DiD specification (Krakowski 2026)

```
Y_igt = alpha_i + gamma_t + lambda_q + beta_1 * post_t
      + beta_2 * D2_g + beta_3 * D3_g + beta_4
      * (D2_g x post_t) + beta_5 * (D3_g x post_t)
      + X'_igt * delta + epsilon_igt

where:
  Y_igt denotes the performance outcome for individual i in group g
        at time t
  alpha_i represents individual fixed effects
  gamma_t represents year fixed effects
  lambda_q represents quarter fixed effects
  ...
  beta_4 and beta_5 are the DiD estimators
```

Each Greek letter is defined in a separate line. The "where:" block is a standard
MS convention for complex specifications.

### Structural estimation methods (Feng 2025)

```
5.   STRUCTURAL ANALYSIS OF THE [MARKET]
     5.1  Background and Data
          - Justify the single-market focus: "computationally intensive,
            so we choose a single therapeutic class"
          - State the data sources, time coverage, and why this market
            is suitable (3 specific reasons)
          - Data construction: how net prices are calculated

     5.2  Estimation
          - Name the estimation approach concisely
          - State what moments are matched
          - Computational details to Online Appendix

     5.3  Model Fit (typically in a later section)
          - Compare model-predicted prices/shares to observed
```

### Simulation-based evaluation methods (Burtch 2026)

Methodological papers use simulation + real-data evaluation:

```
3.   EMPIRICAL EVALUATIONS
     3.1  Simulation Studies with Synthetic Data
          - Name the public benchmark datasets (UCI Machine Learning
            Repository: bike sharing, bank marketing)
          - State the data generation process formally
          - Three regression sets: biased, unbiased, EnsembleIV
          - Report: mean coefficient, SE, MSE over 100 repetitions

     3.2  Apply [Method] with [Alternative Technique]
          - Test with gradient boosting (not just random forest)
          - Same benchmark datasets, same metrics

     4.   BENCHMARKING AND ROBUSTNESS STUDIES
     4.1  Benchmarking with [Closest Competitor]
          - Head-to-head comparison tables
     4.2  Benchmarking with [Other Methods]
     4.3  Sensitivity Analyses
          - Vary one parameter at a time: |D_label|, M, sigma_epsilon, K
          - Figure with 4 panels (one per parameter)
```

### Balance table format (from Cui 2025, Krakowski 2026)

**Cui 2025 multi-site balance table** (Table 2):
```
|               | Control      | Treatment    |              |         |
| Outcome       | Mean | SD    | Mean | SD    | Difference   | p-value |
|               | Panel A: Microsoft                                   |
| Pull requests | 0.86 | 1.49  | 0.87 | 1.50  | 0.01        | 0.88    |
| Commits       | 9.43 | 14.86 | 9.36 | 14.80 | -0.07       | 0.94    |
```
Panels A/B/C for each experiment site. P-values from clustered SEs.

**Krakowski 2026 balance table** (Table 3):
```
|                      | Mean (SD)                | t statistics (SD)     |
| Variable             | D1    | D2    | D3       | (D2-D1)  | (D3-D1)  |
| Gender               | 0.57  | 0.58  | 0.52     | 0.08     | -0.36    |
|                      | (0.51)| (0.50)| (0.51)   | (1.01)   | (1.02)   |
```
F-test of joint significance reported at the bottom.

### Summary statistics table format (from Chao/Larkin 2022, Feng 2025)

**Chao/Larkin 2022** (Table 3): prelaw vs. postlaw with zero rates
```
|                         | Total obs    | Prelaw mean | Total obs   | Postlaw mean |
|                         | (phys-drug-  | (SD)        | (phys-drug- | (SD)         |
|                         | month)       |             | month)      |              |
| Branded Rx, MA          | 1,712,756    | 0.58 (3.43) | 1,774,890   | 0.55 (2.91)  |
|                         | (90% zeroes) |             | (89% zeroes)|              |
```

**Feng 2025** (Table 1):
```
| Variable                    | Mean | Median | SD   | N     |
| Annual WAC growth           | 0.09 | 0.07   | 0.20 | 7,542 |
| Annual net price growth     | 0.04 | 0.03   | 0.61 | 5,913 |
```

### Clustering and standard error conventions

Published MS papers are explicit about clustering choices:
- "Standard errors are robust and clustered by AMC." (Chao/Larkin)
- "standard errors clustered at the business-unit level" (Krakowski)
- "standard errors clustered at the level of treatment assignment" (Cui)

When clustering is non-obvious, papers justify the choice:
"Although the disclosure policy and thus treatment is at the state level, we only have
five states in the data and clustering over so few states could lead to bias. Instead,
we choose to cluster at the AMC level." (Chao/Larkin)

### Multiple inference reporting (Krakowski 2026)

Krakowski reports four types of standard errors/p-values for each coefficient:
```
D3 * Post    0.84***
             (0.05)      <-- standard errors clustered at business-unit level
             {<0.001}    <-- WCR bootstrap p-value (1,000 replications)
             [<0.001]    <-- jackknifed wild bootstrap p-value (1,000 replications)
             (0.0270)    <-- RI-based p-value (1,000 resamplings)
```

This four-layer inference reporting is used when the number of clusters is small
(here: 12 business units) and is becoming a best practice in MS field experiments.

### Framework paper methods (de Kok 2025)

Methodological/tutorial papers replace the traditional methods section with a
step-by-step framework:

```
3.   A FRAMEWORK FOR USING [TOOLS] TO SOLVE RESEARCH TASKS
     3.1  Define and Understand Your Problem: Step 1
     3.2  Decide on the Approach and Model: Step 2
     3.3  Develop Your Prompt (i.e., Prompt Engineering): Step 3
     3.4  Evaluate the Construct Validity: Step 4

4.   CASE STUDY: [APPLICATION]
     4.1  [Task] Classification
     4.2  Classification of [Task] Dimensions
```

The case study section reports performance metrics in a comparison table:
accuracy, precision, recall, F1, type I/II error, N, mean tokens per observation,
and cost per 1,000 observations.
