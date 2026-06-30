# MISQ Results -- Section Style Guide

Extracted from MISQ Research Article exemplars. Supplements `style-profile.md`.

Called "Results of Hypotheses Testing," "Analysis," "Data Analysis and Results," or embedded within "Methodology and Results." The results section in MISQ is hypothesis-driven: it walks through each H and reports whether it is supported, with what evidence.

## Word budget

- 1,500-3,000 words (3-6 published pages two-column) for a single-study paper.
- Multi-study papers (Yin 2014) spread results across per-study subsections.
- Liu (2021): ~2,000w for "Results of Hypotheses Testing" + "Predictive Power" (pp. 1124-1128).
- Gao (2015): ~2,500w for "Analysis" subsections within "Methodology and Results" (pp. 16-20).
- Yin (2014): ~1,000w per study results subsection.

## Arc

```
main results (regression table walk-through, H-by-H)
  -> effect direction and significance for each H
  -> controls noted briefly
  -> robustness checks / alternative specifications
  -> [optional: additional analyses -- predictive power, subgroup, etc.]
```

## Signature moves

1. **H-by-H verdict reporting.** Results are organized around hypotheses, not around tables. Each hypothesis is explicitly named and its support status stated: "Thus, the results support all our hypotheses (H1-H5)." [Liu 2021] or "providing support for H1b." [Gao 2015]

2. **Multiple specifications in one table.** The main results table shows 2-4 columns representing different estimation approaches (OLS, IV, GMM, Tobit, etc.) applied to the same model. The text notes that results are "fairly consistent" across specifications, demonstrating robustness through triangulation of methods.
   - "The three columns show that the three different estimations -- (1) IV regression as our base mode, (2) IV regression with GMM and robust error terms but without clustering in errors, and (3) IV regression with both GMM and clustered robust error terms -- yielded fairly consistent results." [Liu 2021, Table 4]
   - "We first estimate a set of simple models... Column 1 of Table 5 reports the OLS estimation. ... Second, ... we employ a Tobit model, reported in Column 2. ... Third, ... we estimate an ordered logit model reported in Column 3." [Gao 2015]

3. **Coefficient + significance + direction sentence pattern.** Each IV's result is reported in a consistent sentence pattern that names the coefficient direction, significance level, and what hypothesis it supports.
   - "As Table 4 shows, we found positive coefficients for openness, conscientiousness, extraversion, and agreeableness and a negative coefficient for emotional stability." [Liu 2021]
   - "Physician Quality is positively and strongly correlated (p<0.01) with the likelihood of rating." [Gao 2015]

4. **Controls reported briefly.** Control variables get a footnote or one summary sentence, not a per-variable discussion: "As for the controls, most are significant and have expected signs." [Liu 2021, footnote 10]

5. **Robustness as layered specifications, not a separate section.** In MISQ, robustness checks are often embedded as additional columns in the main table or as additional model specifications in the narrative, not quarantined into a separate "Robustness Checks" section. The text walks through each alternative spec.
   - "We further ensured the robustness of our regression results by using a holdout sample validation and the k-fold cross-validation." [Liu 2021]
   - Gao (2015) tests OLS, Tobit, ordered logit, quantile regression, and linear spline models -- all presented as successive columns.

6. **Descriptive evidence before formal tests.** MISQ papers often present descriptive/visual evidence (histograms, means comparisons, distribution plots) before the formal regression test. This establishes the pattern informally, then the regression confirms it formally.
   - "We first explore our data visually. Figure 1 plots the Physician Quality distributions for physicians with and without online ratings. ... These descriptive patterns are inconsistent with Hypothesis 1a ... but provide initial support for Hypothesis 1b." [Gao 2015]
   - "The pattern of means for perceived helpfulness is illustrated in Figure 2." [Yin 2014]

7. **Effect magnitude in interpretable units.** Results include substantive interpretation of coefficient magnitudes, not just significance: "A 10-point increase in Physician Quality (measured on a 100 point scale) leads to a 0.466 point increase in the Online Rating (measured on a 5 point scale)." [Gao 2015]

## Exemplar sentences (shape, not content)

**Opening the results**:
- "We randomly assigned two thirds of all reviewers (and their reviews) to the training sample and the remaining one third to the testing sample. Table 4 reports the results of our model estimations on the training sample." [Liu 2021]
- "Despite the recent growth in online consumer ratings of physicians, a substantial portion of doctors (~44% in our sample) have yet to receive an online rating." [Gao 2015]

**H-support verdict**:
- "Thus, the results support all our hypotheses (H1-H5)." [Liu 2021]
- "Our finding suggests that as Physician Quality increases there is a corresponding increase in the probability of the physician receiving an online rating, thereby providing support for H1b." [Gao 2015]
- "Therefore, as predicted by H1, review content indicative of anxiety was more strongly associated with helpfulness ratings than review content indicative of anger." [Yin 2014]

**Effect magnitude interpretation**:
- "A 10-point increase in Physician Quality (measured on a 100 point scale) leads to a 0.466 point increase in the Online Rating (measured on a 5 point scale)." [Gao 2015]
- "The results show that if a physician is one standard deviation higher, the ratings will increase by 0.604 on a 1-5 scale." [Gao 2015]
- "The personality model can accurately identify an average of 83.62% of helpful future reviews." [Liu 2021]

**Robustness transition**:
- "We further ensured the robustness of our regression results by using a holdout sample validation and the k-fold cross-validation." [Liu 2021]
- "The above estimation assumes that the relationship between Physician Quality and the likelihood of being rated online is constant over the distribution of Physician Quality. To examine the robustness of our results, we employ another specification..." [Gao 2015]

**ANCOVA/experiment result pattern** (for experimental MISQ papers):
- "A repeated-measure ANCOVA was performed to examine the difference in perceived helpfulness across treatment reviews. ... pairwise comparisons revealed that the difference in perceived helpfulness between anxiety and anger conditions was significant (M = 7.57 versus 7.23, t(77) = 2.59, p < 0.05)." [Yin 2014]

## Anti-patterns

- Do NOT report results without referencing hypotheses. Every coefficient discussion should connect back to "supporting H_n" or "inconsistent with H_n."
- Do NOT over-discuss control variables. They get a footnote or one sentence, not a paragraph each.
- Do NOT present only one model specification. Showing robustness across 2-4 specs is expected.
- Do NOT skip effect magnitude interpretation. Significance alone ("p < 0.01") is insufficient; state the direction and substantive size.
- Do NOT defer all robustness to an appendix. At least one alternative specification should appear in the main text.
- Do NOT present results without a table. Regression results are always tabulated with coefficients, standard errors, and significance indicators.

## Paragraph structure

| Block | Paragraphs | Job |
|-------|-----------|-----|
| Descriptive evidence (optional) | 1-2 | Visual/distributional preview of the main relationship |
| Main results | 2-4 | Walk through Table N column by column, H-by-H verdict |
| Controls summary | 0-1 | Brief note on control variable performance |
| Robustness / alternative specs | 2-3 | Additional columns, model variants, subsample tests |
| Additional analyses (optional) | 2-4 | Predictive power, subgroup analysis, mediation, moderation |

## Table/Figure integration

- Main results table: coefficients, standard errors in parentheses, significance stars. Multiple columns for specification variants. Note at bottom explaining significance levels.
- Bar charts for experimental studies showing means across conditions (Yin 2014, Figures 2-3).
- Comparison figures for predictive models showing performance across parameter values (Liu 2021, Figure 4).
- Tables are referenced by column number in the text: "Column 1 of Table 5 reports..." "As seen in Column 2..."

---

## Enriched from additional exemplars (2026-06-29)

Source papers: Zhang (2025), Weng (2026), Ayabakan (2025), Raimi (2025), Liu-EBM (2025), Liu-HMM (2025).

### Additional signature moves

8. **"Ruling out Alternative Explanations" as a dedicated subsection.** Healthcare/causal-inference MISQ papers now include a dedicated subsection that systematically tests and dismisses specific alternative explanations, each named and addressed separately. This is more structured than the generic "robustness checks" pattern.
   - Zhang (2025) includes "Ruling out Alternative Explanations" with named subsections: "Intrinsic motivation," "Contribution quality," "Patient selection," "Patient herding" -- each with its own regression table and null-result narrative.
   - Each alternative explanation follows: name the threat -> describe the test -> present the table -> conclude it is ruled out.

9. **Percentage-point effect interpretation for binary/count outcomes.** Healthcare papers with binary or count outcomes translate coefficients into percentage-point changes against the sample mean, making the effect size interpretable.
   - "physician contributions increased by about 0.044 per day during the policy window. Given that the mean physician contributions were 0.519 (see Table 2), the increase in contributions was about 0.044/0.519 = 8.48% per day." [Zhang 2025]
   - "the likelihood of claim denial decreased by 1.5%-point (beta_1 = -0.015), translating into a 1.5% reduction in the likelihood of claim denial." [Ayabakan 2025]

10. **Marginal-effects plots for continuous moderators.** Healthcare papers supplement regression tables with predictive-margins plots showing how the predicted outcome varies across the range of a continuous moderator.
    - Ayabakan (2025) Figure 1 shows "Predicted Claim Denial Probabilities over Ranges of EHR_SSadj and EHR_Sim" with 95% confidence intervals.

11. **Parallel-trends test for DID papers.** DID papers in MISQ now routinely include a relative-time model (leads-and-lags) with a coefficient plot showing pre-treatment coefficients are statistically insignificant, confirming the parallel-trends assumption.
    - "The terms in Model (1) for the periods before the policy are all non-significant (p-value > 0.10), indicating the parallel trends of our quantity estimation. ... We visualize the estimation results in Figure 3" [Zhang 2025]

12. **Model-selection table for latent-state models.** Papers using HMM, latent class, or mixture models present a model-selection table comparing models with different numbers of states/classes using BIC, AIC, and log-likelihood.
    - Liu-HMM (2025) Table 2 compares 1-5 state HMMs, selecting the 3-state model based on BIC.

13. **Multi-study results with per-study discussion.** Multi-study experimental papers present results AND a mini-discussion within each study section, not in a single combined results section.
    - Raimi (2025): Study 1 has its own "Results" and "Discussion" sections before Study 2 begins. Each study's discussion interprets findings and motivates the next study.

14. **Mediation analysis using PROCESS macro.** Experimental MISQ papers use Hayes PROCESS macro for mediation/moderation testing, reported with path coefficients, p-values, and R-squared values.
    - "To test our hypotheses, we followed the procedures of Hayes (2017) using the SPSS Hayes PROCESS macro (Model 8)." [Raimi 2025]

15. **Cohen's d and f-squared for effect size reporting.** Experimental papers now report standardized effect sizes alongside significance tests.
    - "The difference in means between the human and the chatbot for judgmentalness is what Cohen (2013) calls a small effect size (d = 0.29)" [Raimi 2025]
    - "The f-squared effect sizes were above 0.15, suggesting medium effects" [Weng 2026]

16. **Nested model comparison.** Structural equation and PLS papers present nested models (controls-only, main effects, interactions) to show incremental explanatory power through delta-R-squared.
    - Weng (2026) Table 3 presents Models 1a through 4b (null -> direct effects -> moderators -> interactions) for both DVs, with delta-R-squared noted.

17. **Benchmarking tables for design science papers.** Computational design papers replace hypothesis-testing tables with benchmarking tables comparing the proposed artifact against multiple baselines across multiple metrics and datasets.
    - Liu-EBM (2025) Tables 7-12 benchmark FastSR against ~10 models (NB, SVM, LSTM, CNN, VAT, fine-tuned BioBERT, GPT-4, ProtoNet, etc.) across 3 datasets with significance indicators.

### Robustness patterns expanded

The new papers reveal a richer taxonomy of robustness checks for MISQ:

| Type | Example |
|------|---------|
| Alternative matching (CEM, PSM, k2k) | Zhang (2025), Ayabakan (2025) |
| Alternative control group | Zhang (2025): physicians from competing OHC XYWY.com |
| Alternative DV measurement | Zhang (2025): FreeQuotas, Gifts as alternative DVs |
| Alternative treatment window | Zhang (2025): 2-month and 4-month enrollment windows |
| Parallel trends / relative time model | Zhang (2025): leads-and-lags with Figure 3 |
| 2SLS / IV estimation | Ayabakan (2025): EHR sourcing in other hospitals as IV |
| Heckman selection | Ayabakan (2025): addresses patient self-selection |
| HLM / multilevel | Ayabakan (2025): random intercept at hospital level |
| Alternative variable construction | Ayabakan (2025): unadjusted EHR single-sourcing |
| Hospital-specific time trends | Ayabakan (2025): hospital x year fixed effects |
| Product-category subsample | Liu-HMM (2025): bakery and dairy subsamples |
| Replication on different sample/measure/vignette | Raimi (2025): Prolific sample + revised measures + new vignette |

### Updated anti-patterns

- Do NOT present robustness checks only in an online appendix. At least the key robustness tests (parallel trends, IV, alternative DV) should appear in the main text. Additional tests can go to the appendix.
- Do NOT skip effect-size interpretation for healthcare papers. The raw coefficient is meaningless without context; always translate to interpretable units (percentage points, probability changes, standard-deviation changes).
- Do NOT omit the ruling-out-alternative-explanations subsection when using quasi-experimental designs. Reviewers expect this.

### Exemplar sentences from new papers

**Results opening**:
- "This section presents empirical evidence on the impact of temporal changes in introductory incentives on physician contributions." [Zhang 2025]
- "Our main estimation results are in Table 2. Column 1 shows that the greater adoption of EHRs led to a decrease in the likelihood of claim denials." [Ayabakan 2025]

**H-support verdict**:
- "This finding supports H1, that introductory incentives improve physician contributions during the policy window." [Zhang 2025]
- "Both our hypotheses were mostly supported." [Weng 2026]
- "H1a, H1b, and H1c are supported." / "Hence, H2 and H3 are not supported." [Raimi 2025]

**Percentage-point interpretation**:
- "physician contributions decreased by 0.055 per day during the four months after the policy window ended (about 0.055/0.519 = 10.6%)." [Zhang 2025]
- "when a hospital's intra-hospital EHR single-sourcing rate increases from 80% to 90%, claim denial probability is reduced from 1.18% to 1.03%, representing a decrease of 0.15 percentage points." [Ayabakan 2025]

**Ruling out alternative explanations**:
- "We found the initiation (0.001, p > 0.10) and termination (0.001, p > 0.10) of introductory incentives did not change (or crowd out) physicians' intrinsic motivation." [Zhang 2025]
