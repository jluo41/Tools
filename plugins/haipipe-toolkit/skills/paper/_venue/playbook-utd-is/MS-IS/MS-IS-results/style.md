# MS-IS Results Style Guide

MS-IS results sections are structured around the identification strategy, not around
hypotheses. The primary result leads; supporting results, heterogeneity, and robustness
follow in decreasing importance. Many MS papers merge the empirical strategy and
results into one section ("Empirical Strategy & Main Results") and include an inline
Discussion subsection.

## Section title conventions

| Paper type | Typical title |
|------------|--------------|
| RCT / Field experiment | "Empirical Strategy & Main Results" (merged) |
| Natural experiment | "Results" or "Empirical Results" |
| Analytical | "Analysis" or "Main Results" (propositions + comparative statics) |
| Hybrid | "Model" (propositions) + "Empirical Results" (validation) |

## Word budget

2,000-4,000 words (4-8 double-spaced pages), including tables and figures. Robustness
checks and secondary analyses may add 1,000-2,000 words, but MS-IS tends to push
extensive robustness to the Online Appendix.

## Arc (subsection structure)

### For empirical papers (Cui et al. pattern)

```
4.   EMPIRICAL STRATEGY & MAIN RESULTS
     4.1  Empirical strategy (see Methods style guide)
     4.2  Results on [primary outcome]
          Lead with the main table. State the primary coefficient, SE, and
          significance. Interpret economically: "a [X]% increase corresponds
          to [Y] additional [units] per [period]."
     4.3  Results on [secondary outcomes / quality / mechanisms]
          Additional outcomes that support or qualify the main finding.
     4.4  Discussion (inline)
          Limitations of the identification strategy (LATE vs ATE, external
          validity, threats). Stated before the heterogeneity section.

5.   HETEROGENEITY ANALYSIS
     Break results by subgroups (tenure, skill, geography, pre-treatment
     characteristics). Each subgroup gets 1-2 paragraphs with a table panel.

6.   ROBUSTNESS (if not in Online Appendix)
     Alternative specifications, different samples, placebo tests.
     Often: "In Online Appendix [X], we show that..."
```

### For analytical papers

```
3.   ANALYSIS / MAIN RESULTS
     3.1  Equilibrium characterization
          State the main Proposition/Theorem. Provide the intuition.
     3.2  Comparative statics
          How the equilibrium changes with key parameters.
          State each as a numbered Corollary or part of a Proposition.
     3.3  Welfare analysis
          Consumer surplus, producer surplus, total welfare.
          Compare across regimes (benchmark vs. main model).
     3.4  Extensions
          Relax one assumption at a time. State as additional Propositions.
```

## Signature moves

### Primary result first
The first results paragraph states the main finding with full statistical detail. No
"before we present our main results, we first discuss [preliminary analysis]." The
primary result leads.

From Cui et al.: "We present our results in Table 3, split by experiment... on
average, the number of weekly pull requests made by developers increases by 26.08%
(SE: 10.3%), the number of weekly commits increases by 13.55% (SE: 10.0%), and the
number of weekly builds increases by 38.38% (SE: 12.55%)."

### Effect sizes as percentage of control mean
MS-IS expresses coefficients as percentage effects relative to the control group mean,
making magnitudes interpretable across different outcome scales.

From Cui et al.: "To aid interpretation, we express coefficients as percentage effects
by dividing each by the pre-treatment mean in the control group and multiplying by 100."

### Inline Discussion subsection
Many MS papers include a short Discussion (2-4 paragraphs) within or immediately after
the main results section, addressing identification limitations BEFORE moving to
heterogeneity or robustness. This is distinct from the final Discussion/Conclusion.

From Cui et al. (Section 4.4 Discussion): "Before proceeding, we provide a discussion
of the interpretation of our results and potential limitations. First, due to imperfect
compliance, we rely on instrumental variables (IV) estimation, which identifies a
LATE..." Then addresses LATE vs ATE, ITT vs LATE, and learning effects.

### Results-to-reader translation
After stating the statistical result, translate it into economic terms the reader can
evaluate: "This corresponds to approximately [N] additional [units] per [period],
or [comparison to baseline/benchmark]."

### Heterogeneity as a separate section
MS papers often elevate heterogeneity analysis to a standalone section (not buried in
robustness). This reflects the MS expectation that results should reveal WHERE effects
are strongest/weakest, not just whether they exist.

From Cui et al.: "5. Heterogeneity Analysis: Previous literature has noted that
productivity enhancements driven by large language models are heterogeneous across
skill level and education... we now break out results by (i) the tenure, (ii) the
level, and (iii) the pre-treatment productivity of the developer."

### Robustness signposting to Online Appendix
The body mentions the robustness check and states the conclusion; the table lives in
the Online Appendix. Pattern: "In Online Appendix [X], we show that [result] is
robust to [alternative specification]. The point estimate is [similar/slightly
larger/smaller]."

## Table and figure conventions

### Results tables
- One table per major result, not one mega-table.
- Columns = specifications (OLS, IV, with/without controls).
- Rows = outcomes or independent variables.
- Stars: * 10%, ** 5%, *** 1% (standard across INFORMS).
- Standard errors in parentheses below coefficients.
- Table notes explain: sample, clustering, controls, how to read each column.
- Coefficients expressed as percentage of control mean when possible.

### Panels for multi-site / multi-experiment
From Cui et al.: Table 3 uses columns for Microsoft/Accenture/Anonymous/Pooled,
showing DiD and W-IV side by side. Table 2 uses Panel A/B/C for each experiment's
balance statistics.

### Figures
- Event-study plots (coefficient + 95% CI by period) for DiD.
- Adoption curves (cumulative adoption rate over time) for technology experiments.
- Histograms of outcome distributions.
- Comparative statics plots (parameter on x-axis, outcome on y-axis) for analytical.

## Paragraph structure

Each results paragraph has this shape:

1. **Reference the table/figure** (1 sentence): "We present our results in Table N."
   or "Figure N shows..."
2. **State the primary finding** (1-2 sentences): coefficient, SE, significance,
   direction. Use precise numbers.
3. **Interpret economically** (1-2 sentences): translate the coefficient into
   magnitude that a manager/policymaker can evaluate.
4. **Note qualifications** (0-1 sentence): "though the effect is not statistically
   significant for [subgroup/outcome]" or "consistent with [mechanism]."

## Anti-patterns

- **No results without a table reference.** Every empirical claim must point to a
  specific table and column/row.
- **No vague significance language.** Not "we find a significant effect" but "the
  coefficient is 26.08% (SE: 10.3%), significant at the 5% level."
- **No overclaiming causality.** Match the claim to the design. If DiD: "we estimate
  that..." If observational: "we find a positive association between..."
- **No burying null results.** If an outcome is non-significant, state it clearly:
  "The effect on [outcome] is small and not statistically significant (coefficient,
  SE)." MS referees respect honest nulls.
- **No re-interpreting results beyond the identification strategy.** If the design
  estimates a LATE, discuss LATE vs ATE in the inline Discussion, not in the main
  results paragraph.
- **No robustness-as-results.** Robustness checks confirm the main finding; they are
  not new results. State the main result first, then note robustness.

## Contrast with MISQ/ISR results

| Dimension | MS-IS | MISQ | ISR |
|-----------|-------|------|-----|
| Organized by | Identification strategy / outcomes | Hypotheses (H1, H2, ...) | Hypotheses or outcomes |
| Primary display | Regression table | Research model path coefficients | Regression / SEM table |
| Effect size reporting | Percentage of control mean | Standardized coefficients | Raw or standardized |
| Inline Discussion | Common (4.4 Discussion) | Rare | Rare |
| Heterogeneity | Standalone section | Moderation hypotheses | Post-hoc analysis |
| Robustness location | Online Appendix + signposting | In body | In body or appendix |
| Null results | Stated explicitly | Sometimes hedged | Stated explicitly |

## Enrichment needs

- [x] Mine a published MS-IS results section to capture exact table formatting
  (column headers, note text, star conventions) as rendered by INFORMS.
  **RESOLVED**: See table conventions below from all 8 papers.
- [x] Mine an analytical MS-IS paper to capture how Propositions/Theorems are
  presented with comparative statics plots.
  **RESOLVED**: See Feng 2025 event study and counterfactual patterns below.
- [x] Mine Shukla et al. (2021) for a healthcare-domain MS-IS results section to see
  how clickstream/appointment outcomes are reported.
  **RESOLVED**: See Chao/Larkin 2022 and Huesmann 2025 healthcare results below.

---

## Enriched from additional exemplars (2026-06-29)

Sources: 8 published MS papers (Huesmann 2025, Chao/Larkin 2022, Feng 2025, Cui 2025,
Krakowski 2026, de Kok 2025, Chen 2025, Burtch 2026).

### Section title conventions (additional from published papers)

| Paper | Results section title | Subsections |
|-------|---------------------|-------------|
| Huesmann 2025 | "4. Results" | 4.1 Comparison of Ranking Systems; 4.2 Comparison... vs. Baseline |
| Chao/Larkin 2022 | "4. Results" | 4.1 Statistical Method; 4.2 Regression Results; 4.3 Pretrends; 4.4 Robustness; 4.5 Mechanisms |
| Feng 2025 | "6. Counterfactuals" | 6.1 Role of PBMs; 6.2 Role of Formulary Structure; 6.3 Role of Inertia |
| Cui 2025 | "4. Empirical Strategy & Main Results" | (merged with methods) |
| Krakowski 2026 | "5. Results" | 5.1 Descriptive Statistics; 5.2 Model Specification; 5.3 Main Analysis; 5.4 Counterintuitive Findings |
| Burtch 2026 | "3. Empirical Evaluations" + "4. Benchmarking" | 3.1 Simulation; 4.1 Benchmarking vs. [X] |

### Healthcare DiD results subsection arc (Chao/Larkin 2022)

```
4.   RESULTS
     4.1  Statistical Method
          State the estimator (OLS DiD). Justify the functional form
          ("linear model in part for ease of interpretability, also
          because it can more easily handle the many physician-drug-
          month observations with zero prescriptions").
          State clustering choice and justify.

     4.2  Regression Results
          Main table with progressively richer fixed-effects specs.
          "Table 4 shows the results as we introduce more fixed effects."
          Report linear combinations of coefficients for interpretability.
          State the economic magnitude: "the sunshine law decreased branded
          prescriptions by an average 0.140 scripts per physician-drug-
          month... This extrapolates to approximately 248,625 fewer
          prescriptions."

     4.3  Pretrends and Timing of Effects
          Event-study plot (Figure 1): coefficients + 95% CI by month.
          "Figure 1 demonstrates that there is no significant trend
          between groups prior to the omitted month, but a clearly
          decreasing trend afterward."
          Test with law-signed date vs. implementation date.

     4.4  Robustness Checks
          Multiple clustering levels (physician, state, block-bootstrap).
          Placebo test: "randomly assigning half of the counterfactual
          doctors to the treatment group... repeat 100 times" (Figure 2).
          Appendix tables A.1-A.16 for additional specs.

     4.5  Mechanisms
          Heterogeneity by drug characteristics (sales force presence).
          Heterogeneity by physician characteristics (prescribing volume).
          Test patient-driven vs. physician-driven mechanism by excluding
          post-data-release observations.
```

### Lab experiment results format (Huesmann 2025)

Experimental MS papers present results using a combination of figures and formal
statistical tests, often using nonparametric methods:

**Pairwise comparison matrices** (Figure 3, Figure 4):
A matrix where each cell above the diagonal shows the percentage change if
switching from row to column ranking system, with significance stars. Diagonal
cells show mean effort and SD. Below-diagonal cells show the reverse comparison.
This is a distinctive MS experiment visualization.

**Formal Result blocks** in the body text:
```
**Result 1** (Ranking System Design and Ability). *A subject's effort
level depends on the ranking system design and on the subject's
ability type.*
  a. *Effort is increasing in the number of achievable thresholds...*
  b. ...
  c. ...
```

**Nonparametric then parametric**:
"In this section, we first test our behavioral predictions using nonparametric
statistics and then use parametric regressions to test the robustness of our main
results." The nonparametric tests come first (Wilcoxon signed-rank, Mann-Whitney U),
followed by OLS with controls.

### DiD results table format (from Chao/Larkin 2022, Krakowski 2026)

**Chao/Larkin Table 4** (OLS, Physician-Drug-Month):
```
|                              | (1)        | (2)        | ... | (6)        |
| N (physician-drug-month)     | 17,013,810 | 17,013,810 |     | 17,013,810 |
| Adjusted R^2                 | 0.060      | 0.060      |     | 0.189      |
|                              |            |            |     |            |
| Main Effects                 |            |            |     |            |
| 1. Sunshine Implementation   | 0.474***   | 0.284***   |     | 0.292***   |
|                              | (0.090)    | (0.097)    |     | (0.104)    |
| 2. Branded                   | -0.116     | -0.129     |     |            |
|                              | (0.078)    | (0.079)    |     |            |
| Interactions                 |            |            |     |            |
| 3. Sunshine*Branded          | -0.584***  | -0.571***  |     | -0.562***  |
|                              | (0.159)    | (0.159)    |     | (0.182)    |
| Controls                     |            |            |     |            |
| Month FE                     | No         | Yes        |     | No         |
| Drug FE                      | No         | No         |     | No         |
| Physician FE                 | Yes        | Yes        |     | Yes        |
| ...                          |            |            |     |            |
| Linear combinations          |            |            |     |            |
| a.) 1 + 3                    | -0.110     | -0.288***  |     | -0.271***  |
|                              | (0.072)    | (0.069)    |     | (0.083)    |
```

Key conventions:
- Columns = progressively richer specifications (more FEs, more interactions)
- Stars: *p < 0.05; **p < 0.01; ***p < 0.001 (some papers use *p < 0.10)
- SEs in parentheses below coefficients
- "Linear combinations of coefficients" row at the bottom for interpretability
- Control indicators as Yes/No rows
- Table note explains: "SEs are robust and clustered by AMC"

### Counterfactual results (Feng 2025)

Structural papers present results as counterfactual simulations:

```
6.   COUNTERFACTUALS
     6.1  The Role of PBMs
          "We find that the total cost of statins would increase by
          almost 50%. Even after accounting for potential PBM fees,
          we find that total spending is almost 40% higher."

     6.2  The Role of Formulary Structure
          "We find that altering the tier structure (e.g., single-tier
          versus multitier formularies) has a small impact on
          equilibrium outcomes..."

     6.3  The Role of Demand Inertia
          "Under this hypothetical scenario, drug manufacturers price
          higher at the beginning of the life-cycle, but reduce prices
          significantly whenever a competitor enters the market."
```

### Mechanism analysis as a standalone subsection

Multiple MS papers elevate mechanism investigation to its own subsection within
Results, not Discussion:

- **Chao/Larkin "4.5. Mechanisms"**: Tests drug-side heterogeneity (sales force) and
  physician-side heterogeneity (prescribing volume) to identify whether effects are
  patient-driven or physician-driven.
- **Krakowski "5.4. Counterintuitive Findings and Mechanisms"**: Uses qualitative
  interview data alongside quantitative analysis to explain why the untailored
  condition produced negative effects.

### Qualitative evidence within quantitative results (Krakowski 2026)

Krakowski embeds direct quotes from field interviews in the results section to
illuminate mechanisms:

"A Danish innovator in D2 acknowledged the AI system's sophistication but also noted:
'The whole work situation was in a way paradoxical. We got this super tool, and at
the same time, I felt like in prison.'"

This mixed-methods integration within the Results section (not in Discussion) is
accepted in MS field experiments, particularly when the quantitative finding is
counterintuitive and requires explanation.

### Mediation analysis within results (Krakowski 2026)

Krakowski presents a Baron-Kenny mediation analysis as part of the results:

```
Table 8. Computation of Direct, Indirect, and Total Effects from
         Mediation Analysis

| Sales meetings  | Coefficient | Bootstrapped SE | P > |z| |
| Direct effect   | 0.22        | 0.05            | <0.001   |
| Indirect effect | 0.83        | 0.04            | <0.001   |
| Total effect    | 1.04        | 0.02            | <0.001   |
```

### Pretrends and event-study plot conventions

**Event-study plot** (Chao/Larkin Figure 1):
- X-axis: months relative to treatment (e.g., "Months from Signing")
- Y-axis: "Point Estimate" (coefficient from month-by-month DiD)
- Vertical bars: 95% confidence intervals
- Vertical dashed line at the treatment date
- Note below: "Omitted month is June 2008... Law implementation occurs at month 11."

**Placebo test plot** (Chao/Larkin Figure 2):
- X-axis: "Placebo Trials, Sorted by Coefficient"
- Y-axis: "Point Estimate"
- Dots for each of 100 placebo trials, with the actual main result marked with an X
- "Statistical significance was achieved in only 3 out of 100 trials."

### Simulation results table format (Burtch 2026)

Methodological papers compare estimators in a standardized table:

```
| Coefficient | True | Biased | Unbiased | EnsembleIV (Top 3) | EnsembleIV (PCA) | EnsembleIV (LASSO) |
| beta_0      | 1.0  | 0.756  | 0.999    | 1.026              | 1.015            | 1.058              |
|             |      | (0.070)| (0.111)  | (0.063)            | (0.063)          | (0.062)            |
| ...         |      |        |          |                    |                  |                    |
| Est. MSE    |      | 0.067  | 0.013    | 0.005              | 0.004            | 0.008              |
```

Key: "Estimation MSE" as the bottom-line comparison metric across all estimators.

### Performance comparison table for ML methods (de Kok 2025)

```
| Table 1                  | (1)    | (2)      | (3)    | (4)    | (5)       | (6)        |
|                          | Manual | Gow 2021 | ChatGPT| GPT-4  | Keyword+  | (5)+ChatGPT|
|                          |        |          |zero shot|zero shot| GPT-3    | FT filter  |
| Accuracy                 |        | 0.86     | 0.91   | 0.93   | 0.94      | 0.96       |
| Nonanswer F1 score       |        | 0.49     | 0.72   | 0.79   | 0.82      | 0.87       |
| N                        | 500    | 500      | 500    | 500    | 500       | 500        |
| Costs per 1,000          | $0     | $0       | $0.66  | $16.98 | $0.48     | $1.06      |
```

The cost row is a distinctive feature of LLM methodology papers in MS.
