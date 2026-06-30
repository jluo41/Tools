# ISR Results Style Guide

Distilled from two ISR exemplars. Quote the SHAPE, not the content.

## Word budget

- Target: 2,000-4,000 words for main results; robustness checks add 1,500-3,000 words.
- Bao 2021: ~2,000 words for main results (S6.2), ~3,500 words for endogeneity + robustness (S6.3-6.4, S7).
- Zhang 2026: ~1,500 words for main results (S6.1), ~1,500 words for robustness (S6.2).
- ISR results sections are LONG because they include extensive robustness checks in the same or adjacent section.

## Section naming conventions

```
Pattern A [Bao 2021]:
  6. Empirical Analyses
    6.1. Baseline Models [method description, placed here not in Methods]
    6.2. Estimation Results
    6.3. Endogeneity Concerns
    6.4. Difference-in-Differences Analysis
  7. Robustness Checks
    7.1. Internal and External Information Integration
    7.2. Falsification Tests
    7.3. Heterogeneity Analyses

Pattern B [Zhang 2026]:
  6. Results
    6.1. Results of Primary Empirical Models
    6.2. Robustness Checks
      6.2.1. Difference in Difference with Propensity Score Matching
      6.2.2. Impact of Review Recency
      6.2.3. Impact of Review Sentiment Asymmetry
```

## Effect reporting pattern

### Coefficient + p-value + interpretation in one sentence
- [Bao 2021] "the coefficient of MU Achievement is positive and significant (coeff. = 0.048; p-value < 0.01), suggesting that a 1% increase in meaningful use among ACO providers is associated with 0.05% improvement in average ACO quality."
- [Bao 2021] "The significant interaction term (coeff. = 0.309; p-value = 0.03) indicates that MU Achievement positively influences the relationship between ACO efficiency and quality."
- [Zhang 2026] "the number of reviews received (which includes both positive and negative reviews, beta = 0.50), thank-you letters (beta = 0.17), and virtual gifts (beta = 0.14) are all statistically significant."
- [Zhang 2026] "effectiveness has the largest impact (beta = 0.78), followed by patient-centeredness (beta = 0.66), timeliness (beta = 0.23), efficiency (beta = 0.18), and safety (beta = 0.11)."
- SHAPE: `The coefficient of [variable] is [positive/negative] and [significant/insignificant] (coeff. = [X]; p-value [< threshold / = value]), [suggesting/indicating] that [interpretation in substantive terms].`

### Hypothesis support verdict: one clean sentence
- [Bao 2021] "Hence, our results do not support H1." / "Hence, our main results support hypotheses H2 and H3..."
- SHAPE: `Hence, our results [support / do not support] H[N] with respect to [what the hypothesis predicted].`
- State the verdict explicitly. Do not leave the reader to infer whether H is supported.
- When a hypothesis is NOT supported, state it plainly and briefly note the implication.

### Stepwise model building (hierarchical regression)
- [Zhang 2026] Three models in sequence: Model 1 (controls only), Model 2 (+ numerical ratings), Model 3 (+ SEPTE service quality scores). Each adds variables and shows incremental R-squared.
- [Bao 2021] Two columns: baseline (eq. 1), interaction (eq. 2). Plus Heckman correction columns.
- SHAPE: Report models in sequence, noting what each column adds. Comment on how coefficients change across specifications ("the coefficient for review volume decreased from 0.50 to 0.26 in Model 2, suggesting that...").

### Guarded language throughout
- [Bao 2021] Uses "we observe that" (6 times), "suggesting that," "indicating that." Never "we prove" or "we establish."
- [Zhang 2026] Uses "show," "indicate," "suggest." Never "demonstrate causally" for observational findings.
- ISR-safe verbs for results: observe, find, show, suggest, indicate, note. Reserve "demonstrate" for method performance.

## Significance conventions

- Stars: `*p < 0.10; **p < 0.05; ***p < 0.01` (two-tailed test). Stated in table notes.
- [Bao 2021] Uses this exact convention. Standard errors in parentheses below coefficients.
- [Zhang 2026] Uses `***p < 0.001; **p < 0.01; *p < 0.05` (slightly different thresholds).
- Report both the coefficient and the standard error (or p-value). Never report stars alone without the coefficient magnitude.

## Endogeneity subsection (the ISR signature move)

### Dedicated subsection, stated in the reviewer's voice
- [Bao 2021] S6.3 "Endogeneity Concerns": "One may argue that MU achievement is endogenous with ACO quality, since high-quality ACOs may be more likely to invest in EHRs..."
- SHAPE: `One may argue that [IV] is endogenous with [DV], since [reverse causality story]. [Omitted variable concern]. To mitigate endogeneity concerns, we deploy [identification strategy].`
- The endogeneity threat is stated in the reviewer's voice, not the author's. This shows the authors anticipated the critique.

### IV approach: name instruments, justify relevance + exogeneity
- [Bao 2021] "We utilized two instruments - the number of rural health clinics (RHC) and number of critical access hospitals (CAH). [Relevance justification: 3 sentences]. [Exogeneity justification: 3 sentences]."
- SHAPE: `We deploy an instrument variable (IV) approach. We utilized [N] instruments: [instrument 1] and [instrument 2]. [Why they are relevant to the endogenous variable]. [Why they satisfy the exclusion restriction].`

### Report diagnostic statistics
- [Bao 2021] "The Sargan statistic equals 2.20, with a p-value of 0.14... The test statistic [Anderson canonical correlations] equals 15.64 with p-value < 0.01."
- [Zhang 2026] "The Arellano-Bond test for second-order autocorrelation (p = 0.594) and the Sargan-Hansen test for instrument validity (chi = 1.04, p = 0.31) support the model specification."
- SHAPE: Report Hansen/Sargan overidentification test + weak instrument F-statistic (first-stage F or Anderson). State what each test shows.

## Robustness checks (layered identification)

ISR expects MULTIPLE robustness strategies, not just one. The standard toolkit:

```
[Bao 2021 robustness stack]:
1. IV approach (two instruments, Sargan + Anderson tests)
2. Heckman two-step correction (inverse Mills ratio)
3. Difference-in-Differences (PSM-matched treatment/control)
4. Alternative variable operationalizations (info integration)
5. Falsification tests (placebo outcomes)
6. Heterogeneity analyses (subgroup splits)

[Zhang 2026 robustness stack]:
1. DiD with Propensity Score Matching
2. Coarsened Exact Matching (CEM)
3. Generalized Method of Moments (GMM)
4. Review recency moderation
5. Sentiment asymmetry analysis
```

### Robustness subsection structure
- Each check gets its own numbered subsection with: (1) why this check is needed, (2) how it is implemented, (3) result, (4) one-sentence verdict.
- [Bao 2021] Falsification test subsection (7.2): explains the logic (information sharing should NOT affect communication quality), names the placebo outcomes, reports insignificant coefficients, concludes "These results mitigate potential confounding concerns."
- SHAPE: `[Why this check]. [Implementation]. [Result]. [Verdict: "consistent with / supports our main findings"].`

### Balance diagnostics for matching
- [Zhang 2026] "We verify covariate balance after matching and find that the standardized differences for all matching variables fall below the 5% threshold."
- SHAPE: Report balance table or state the balance threshold is met.

## Tables

### Regression table format
- [Bao 2021] Table 4: columns = model specifications, rows = variables, cells = coefficient (SE). Bottom rows: N, R-squared, FE indicators (Yes/No), clustering note.
- SHAPE: `DV: [variable name] | (1) Baseline | (2) Interaction | (3) IV/Heckman | (4) ...`
- Table note: "Standard errors are clustered at the [level]. *p < 0.10; **p < 0.05; ***p < 0.01 (two-tailed test)."

## Anti-patterns

- Reporting robustness checks in a single paragraph. Each check warrants its own subsection.
- Not stating the endogeneity threat before presenting the remedy.
- Reporting only stars without coefficient magnitudes or standard errors.
- Claiming causal language in results when the identification is observational ("the effect of X on Y" without IV/DiD).
- Failing to state whether each hypothesis is supported or not after reporting the estimates.
- Burying the weak-instrument test or overidentification test in a footnote.

## Enriched from additional exemplars (2026-06-29)

Sources: Mousavi 2026, Saifee 2020, Yang 2022, Wang 2026, Wu 2025, Liu 2025, Zhang-j 2026, Schecter 2025.

### Word budget (revised)

The original 2,000-4,000 (main) + 1,500-3,000 (robustness) underestimates. Across new papers:

| Paper | Main results | Robustness | Combined |
|---|---|---|---|
| Mousavi 2026 | ~4,200 | (within main) | ~4,200 |
| Saifee 2020 | ~2,200 | ~2,800 (10 checks) | ~5,000 |
| Wang 2026 | ~7,000 (including mechanisms) | (within main) | ~7,000 |
| Wu 2025 | ~4,500 | ~1,200 (supplementary) | ~5,700 |
| Liu 2025 | ~4,500 | ~2,500 (11 checks) | ~7,000 |

**Revised target: 4,000-7,000 words** total for results + robustness. Results is typically the largest section in the paper (30-42% of body).

### Progressive-funnel argumentation

[Wang 2026] demonstrates the most structured results architecture in the sample:
```
4.1 Main effects
4.2 Rule out alternatives
  4.2.1 Patient-side (sorting, adherence)
  4.2.2 Physician-side positive evidence (which commitments, content relevance)
  4.2.3 Boundary conditions (cost exposure, audience convergence)
4.3 Robustness (spillovers, reputation, market position)
```
- Transition device: "Having established X, we now turn to Y."
- This is the strongest ISR results architecture: establish -> rule out -> positive mechanism -> boundary conditions -> robustness. Each subsection builds on the conclusion of the previous one.
- SHAPE: `Having established that [prior finding], we now turn to [next question].`

### Named mechanism subsections

[Liu 2025] gives each mechanism its own bolded subsection heading:
- "5.2.1. The Sampling Effect."
- "5.2.2. The Spillover Effect."
- "5.2.3. The Matching Effect."
- SHAPE: Name each mechanism as a subsection, test it with its own regression/analysis, report verdict.

### If-then falsification prediction pattern

Before each mechanism test, state the falsifiable prediction explicitly:
- [Liu 2025] "If the sampling mechanism influences subsequent visits, we anticipate a stronger effect among users experiencing greater uncertainty..."
- [Wang 2026] "If patient sorting were the primary mechanism, we would expect online information provision to predict patient severity, and controlling for it would substantially attenuate the treatment effects."
- [Liu 2025] "If the Q&A service does facilitate matching users with the right type of medical care, the specialty of the medical care sought after the Q&A session may differ..."
- SHAPE: `If [alternative mechanism] were the primary driver, we would expect [specific pattern]. In contrast, [our mechanism] predicts [different pattern]. [Test]. [Results are consistent with our mechanism.]`
- This turns defensive robustness into offensive theory support. [Wang 2026]

### Effect size reporting (expanded)

Beyond "coefficient + p-value + interpretation," new patterns:

- **Percentage + raw number pairing** [Liu 2025, Wu 2025]: "an average increase of 2% (or 0.033 visits per month)" / "an average increase of 6.6% (or 0.57 yuan per month)"
- **Exponential transformation shown** [Wu 2025]: "a 3.87% (1 - e^{-0.0397}) reduction in the relative risk of mortality"
- **Column-specific table references** [Wang 2026, Liu 2025]: "in the first two columns of Table 4" / "presented in the last two columns of Table 4"
- **Panel-specific references** [Wang 2026]: "Table 6, Panels A and B, presents the results"
- **Ranked effects** [Mousavi 2026]: "effectiveness has the largest impact (beta = 0.78), followed by patient-centeredness (beta = 0.66), timeliness (beta = 0.23)..."
- SHAPE: Always translate the coefficient into a substantive effect size (percentage change, dollar amount, or ranking). Never report only the coefficient and stars.

### Calibrated hypothesis support language

Beyond "Hence, our results support/do not support H[N]":
- **Full support** [Mousavi 2026]: "supporting Hypothesis 1(b)"
- **Partial support** [Mousavi 2026]: "partially supporting Hypothesis 1(a)"
- **Overall verdict** [Mousavi 2026]: "Overall, these results support our hypothesis regarding the cognitive-affective spectrum of annotation tasks."
- **With mechanism validation** [Wu 2025]: "supporting Hypothesis 1" followed by "supporting Hypothesis 2" in the mediation subsection
- SHAPE: Use "supporting" for confirmed, "partially supporting" for mixed, "our results do not support" for rejected. "Partially supporting" is stronger than "mixed support."

### Null result framing

[Saifee 2020] presents a null finding as its primary contribution:
- "Contrary to popular belief, our study finds that there is no clear relationship between online reviews of physicians and their patients' clinical outcomes."
- "Hence, physician and staff ratings are not reliable indicators either as far as their ability to signal care quality is concerned."
- SHAPE for null results: `Contrary to [popular belief / prior findings in related contexts], [our results show no significant relationship]. [Theory explains why: credence goods / information asymmetry / etc.].`
- Never present a null result apologetically. Frame it as theoretically predicted and practically important.

### Concern-and-address pattern

[Liu 2025] systematically names threats and resolves them:
- "One potential concern is that the observed sampling effect may be confounded by browsing behavior. To address this, we include browsing activity as a control..."
- "This self-selection process could introduce biases in the analysis. To address this concern, we match users based on observed static and time-varying attributes."
- SHAPE: `One potential concern is [threat]. To address this [concern], we [remedy].`
- This is more targeted than the existing "One may argue that..." pattern. Both are ISR-standard.

### Interpretive sentence patterns

Several new papers use formulaic interpretive sentences after results:
- [Liu 2025] "This finding suggests that..." / "These findings provide evidence of..." / "These findings align with the previous literature on..."
- [Liu 2025] "Specifically, we estimate that..." (used 15+ times as a zoom-in device)
- [Wang 2026] "This pattern suggests..." / "These results validate..."
- SHAPE: After stating a coefficient, follow with "This finding suggests that [substantive interpretation]." or "Specifically, [percentage/magnitude interpretation]."

### Robustness check count (revised)

The original guide shows 5-6 checks per paper. New exemplars show the upper bound is higher:
- [Saifee 2020]: 10 robustness checks in a dedicated Section 5
- [Liu 2025]: 11 checks (8 in Section 6.1 + placebo + field experiment + IV)
- [Wang 2026]: ~8 checks woven into the results funnel
- **Revised guideline**: 5-11 robustness checks is the ISR range. 8+ signals thoroughness. Each check still gets its own numbered subsection.

### Additional robustness strategies (from new exemplars)

Beyond the existing IV/Heckman/DiD/falsification toolkit:
- **Field experiment as validation** [Liu 2025]: a separate field experiment (Section 6.3) validating the observational findings. Exceptionally strong.
- **Dynamic panel / GMM** [Saifee 2020]: Arellano-Bond and Arellano-Bover/Blundell-Bond estimators
- **Self-selection / manipulation test** [Saifee 2020]: "we test whether there is any evidence that doctors manipulate their online ratings"
- **Digital divide test** [Saifee 2020]: "whether the propensity to write reviews varies with patient demographics"
- **Content relevance moderation** [Wang 2026]: testing whether the effect is stronger when online content is clinically relevant
- **Cross-specialty spillover** [Liu 2025]: testing whether the mechanism creates cross-specialty demand
- **Alternative ML approaches** [Zhang-j 2026, Schecter 2025]: running the same analysis with XGBoost, BERT, GPT to show robustness to the ML method choice
- **Monte Carlo simulation** [Zhang-j 2026, Schecter 2025, Shi 2025]: for methodology papers, simulations with known ground truth validate the proposed estimator before the empirical application

### Table conventions (expanded)

- **No tables in main text** is acceptable for methods papers [Zhang-j 2026] when figures carry the results (8 density/distribution plots). All tables can go to the electronic companion.
- **No figures in main text** is the norm for empirical papers [Wu 2025, Liu 2025]. Tables carry the argument; figures are supplementary.
- **Table-heavy vs. figure-heavy**: Empirical papers average 8-10 tables, 0-3 figures in the main body. Methods papers may reverse this ratio.

### Updated anti-patterns

- **"Additionally" / "Furthermore" / "Moreover" overuse**: [Liu 2025] uses these as paragraph openers ~15 times in Results. Vary the transitions.
- **Not pairing percentage with raw magnitude**: when reporting effect sizes, always give both the percentage change and the raw number. [Liu 2025, Wu 2025]
- **Missing the progressive logic**: results subsections should build on each other ("Having established X, we now turn to Y"), not read as disconnected tests.
