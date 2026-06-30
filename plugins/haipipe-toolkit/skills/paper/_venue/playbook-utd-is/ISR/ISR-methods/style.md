# ISR Methods / Data Style Guide

Distilled from two ISR exemplars. Quote the SHAPE, not the content.

## Word budget

- Target: 2,500-4,000 words.
- Bao 2021: ~3,500 words across "Data and Variable Construction" (S5) + "Empirical Analyses" (S6.1 baseline models).
- Zhang 2026: ~3,000 words across "Methods" (S4, language modeling) + "Data" (S5, preprocessing + descriptive stats).
- ISR sometimes splits this into two sections (Data, then Empirical Model); sometimes merges them.

## Section naming conventions

```
Pattern A [Bao 2021]:
  5. Data and Variable Construction
    5.1. ACO Quality
    5.2. ACO Efficiency
    5.3. Effective Health IT Use
    5.4. Control Variables
  6. Empirical Analyses
    6.1. Baseline Models

Pattern B [Zhang 2026]:
  4. Methods
    4.1. Language Modeling Methods
    4.2. Our Small Language Model: Doc-BERT
  5. Data
    5.1. Data Preprocessing
    5.2. Algorithm Performance Evaluation
    5.3. Descriptive Statistics
```

## Data description pattern

### Opening: data source + scope + time period
- [Bao 2021] "We draw on the MSSP public use file from CMS to obtain longitudinal data on ACO-specific operating characteristics and financial performance... Overall, our data set consists of 2,343 ACO-year observations across six years from 2013 to 2018."
- [Zhang 2026] "We assembled a data set from HaoDF.com... which includes millions of reviews on 936,975 physicians from 10,526 major hospitals across China. Data were collected via web crawling over a 24-month period from February 2022 to February 2024."
- SHAPE: `We [draw on / assemble] [data source] to obtain [what kind of data]. [Matching/merging steps]. Overall, our data set consists of [N observations] across [time period].`

### One subsection per key variable
- [Bao 2021] Separate subsections for each variable group: DV (ACO Quality), IV (ACO Efficiency), moderator (Effective Health IT Use), controls.
- SHAPE: `[Variable name] is defined as [definition]. We operationalize [variable] using [measure] because [justification grounded in prior work (cite)]. [Construction details].`

### Variable table: definitions + descriptive statistics
- [Bao 2021] Table 1: three-column format (Variable | Definition | Mean (St. Dev.)) with sections for each model stage.
- [Zhang 2026] Table 2: five-column format (Variable | Mean | SD | Median | Min | Max) organized by variable group.
- SHAPE: One combined table with variable name, full definition, and descriptive statistics. Group variables by role (DV, IV, controls).

### Sample construction transparency
- [Bao 2021] "We eliminated ACOs with missing values... Since a binary method does not accurately measure the true quality of ACOs, we excluded the first year and used the remaining five-year period from 2014 to 2018 for our main analyses."
- SHAPE: State every exclusion criterion and the resulting sample size. Justify each exclusion.

## Identification strategy presentation

### Model specification: numbered equation + verbal explanation
- [Bao 2021] Equation (1): `ACO_Quality_it = alpha_0 + alpha_1*MUAchievement_it + alpha_2*ACOEfficiency_it + beta*X_it + gamma_i + mu_t + epsilon_it`
- [Zhang 2026] Equation (2): `OnlineDemand_i,t = beta_1*Safety + beta_2*Effectiveness + ... + gamma*Controls + alpha_i + delta_t + epsilon_i,t`
- SHAPE: `[DV]_it = [coefficients on IVs] + [controls vector] + [entity FE] + [time FE] + [error]. Where i indicates [unit] and t denotes [time period].`
- Always include entity and time fixed effects; state what each absorbs.

### Fixed effects and clustering stated explicitly
- [Bao 2021] "For our main analyses, we include fixed effects to capture unobserved ACO heterogeneity and yearly ACO program changes." "We clustered standard errors at the ACO level in all models."
- [Zhang 2026] "The term alpha_i denotes physician fixed effects and delta_t denotes time fixed effects. All standard errors are clustered at the physician level to account for within-physician correlation over time."
- SHAPE: `We include [entity] and [time] fixed effects. Standard errors are clustered at the [entity] level.`

### Multi-stage methods: describe each stage sequentially
- [Bao 2021] Two-stage: (1) DEA to compute efficiency scores, (2) panel regression with efficiency as IV.
- Each stage gets its own paragraph block: "In the first stage, we deployed DEA... In the second stage, we used the ACO_Quality score as the dependent variable..."

### Interaction terms: explicit construction
- [Bao 2021] "To mitigate multi-collinearity, we followed Bharadwaj et al. (2007) and used mean-centered values of MU Achievement and ACO Efficiency."
- SHAPE: State the centering strategy when interactions are used.

## Control variables subsection

- [Bao 2021] Dedicated subsection (5.4) defining each control with justification.
- SHAPE per control: `[Variable] is [definition]. [Why it matters for this study (1 sentence)].`
- Group controls by type (organizational, demographic, program characteristics).

## Method validation / justification

### Cite prior use of the method
- [Bao 2021] "DEA has been adopted widely to analyze hospital productivity and is particularly suited to measure the efficiency of complex service organizations for several reasons (Hollingsworth 2008, Huerta et al. 2013)."
- SHAPE: `[Method] has been [widely used / validated] in [domain] for [reasons] (cite, cite).`

### State method assumptions and justify them
- [Bao 2021] "We used the Banker-Charnes-Cooper (BCC) model, which accounts for variable returns to scale in the production function (Banker et al. 1984). Since healthcare organizations typically exercise more control over their deployment of input resources, we adopted an input-oriented BCC model."
- SHAPE: Name the specific model variant, state its assumptions, justify why those assumptions hold in this context.

## Exemplar shapes

```
[Bao methods arc]:
S5: Data + Variables
  P1: Data source + scope + merging steps
  P2-P3: DV construction (quality composite)
  P4-P6: IV construction (DEA efficiency, inputs + outputs)
  P7-P8: Moderator construction (MU achievement)
  P9: Controls (one paragraph, each defined)
S6.1: Empirical Model
  P1: Overview sentence ("we first describe our research design...")
  P2: DEA stage description + justification
  P3: Econometric stage + equation (1) + FE + clustering
  P4: Interaction model + equation (2) + centering

[Zhang methods arc]:
S4: Methods
  P1-P3: NLP landscape (why BERT for this task)
  P4-P8: Doc-BERT architecture (Doc2Vec + BERT + DNN)
S5: Data
  P1: Data source + collection + scope
  P2: Preprocessing + labeling (interrater reliability: kappa = 0.92)
  P3-P4: Performance comparison (19 baselines, Table 1)
  P5: Descriptive statistics (Table 2)
```

## Anti-patterns

- Presenting the model equation without defining every term.
- Omitting the clustering level or fixed effects specification.
- Describing controls as a list without justification for inclusion.
- Not reporting sample size and time period in the data subsection opener.
- For ML/NLP methods: not comparing against baselines or reporting evaluation metrics.
- Burying the identification strategy in a footnote. It belongs front and center.

## Enriched from additional exemplars (2026-06-29)

Sources: Mousavi 2026, Saifee 2020, Yang 2022, Wang 2026, Wu 2025, Liu 2025, Zhang-j 2026, Schecter 2025.

### Word budget (revised)

The original 2,500-4,000 range expands. When Data and Empirical Strategy are separate sections, the combined total can reach 5,500.

| Paper | Data section | Model/Strategy section | Combined |
|---|---|---|---|
| Wang 2026 | ~1,200 (3.1) | ~800 (3.2) | ~2,000 |
| Liu 2025 | ~1,500 (Empirical Setting) | ~1,800 (Model + Strategy) | ~3,300 |
| Saifee 2020 | ~2,500 (Research Framework 3.1-3.4) | embedded | ~2,500 |
| Wu 2025 | ~3,500 (Data + Variables) | ~2,000 (Empirical Strategies) | ~5,500 |
| Yang 2022 | embedded in Framework | ~3,800 (Framework) | ~3,800 |

**Revised target: 2,000-5,500 words** combined. Papers with many variables and complex identification strategies reach the upper end.

### Additional section naming patterns

```
Pattern C [Wang 2026]:
  3. Data and Methodology
    3.1 Data
    3.2 Econometric Model

Pattern D [Wu 2025]:
  3. Data and Variables
    3.1 Data
    3.2 Variables (5 sub-subsections by variable type)
  4. Empirical Strategies
    4.1 Main Estimation
    4.2 Identification

Pattern E [Liu 2025]:
  3. Empirical Setting
    3.1 Data
    3.2 Variables
  4. Model and Empirical Strategy
    4.1 Objective
    4.2 Model
    4.3 Matching
    4.4 Identification

Pattern F [Saifee 2020]:
  3. Research Framework
    3.1 Text Mining
    3.2 Measure Construction
    3.3 Model Specification
    3.4 Variables
```

### Additional data description patterns

Beyond "We draw on / assemble," three more opening shapes:

- **Collaboration framing** [Liu 2025]: "For this study, we collaborated with an on-demand healthcare platform that operates through a mobile app in China."
- **Institution framing** [Wu 2025]: "Data for this study were collected from a large urban hospital in Northeastern China that is involved with research and clinical care."
- **Summary sentence closing the data subsection** [Liu 2025]: "In summary, the data set comprises 43,987 premium consultation purchases, 1,048,567 appointments, 11,994 Q&A service purchases, and 639,034 browsing activities (refer to Table 2)."
- SHAPE: Always close the data subsection with a concrete count of observations. [Wu 2025, Liu 2025]

### Variable naming conventions

- **Italicized variable names** [Saifee 2020]: *Future30DayReadm*, *SentimentScore*, *OverallRating* -- italicized in running text throughout the paper.
- **Subscript notation** [Wang 2026, Wu 2025]: Variable_{i,t} with entity and time subscripts defined once and reused.
- Both conventions are acceptable in ISR. Pick one and be consistent.

### Identification strategy patterns (expanded)

Beyond IV and multi-stage methods, the new exemplars show these identification strategies:

**DID + PSM matching** [Wang 2026, Liu 2025, Wu 2025]:
- SHAPE: `We employ a difference-in-differences (DID) design with propensity score matching (PSM) to address selection concerns. [Matching variables listed]. [Balance diagnostics reported]. Our estimates should be interpreted as local average treatment effects (LATEs) specific to the subpopulation matched on observed characteristics.`
- [Liu 2025] adds: "our estimates should be interpreted as local average treatment effects (LATEs)" -- state the estimand explicitly.

**Two-way fixed-effects panel model** [Saifee 2020]:
- SHAPE: `We use the following two-way fixed-effects panel model: [equation]. Where gamma_i captures [entity] heterogeneity and mu_t captures [time] trends.`
- Name the model type explicitly ("two-way fixed-effects panel model").

**DML (Double Machine Learning)** [Shi 2025]:
- For methodology papers, the method IS the contribution. Description is detailed, multi-stage, with simulations validating each component.
- SHAPE: `We propose [method name] that addresses [problem]. The key elements are: (1) [element 1], (2) [element 2]. We validate using both simulated and real-world data.`

### Multi-source data merging

[Wu 2025] and [Saifee 2020] merge multiple data sources. The ISR convention:
- Name each data source with its own sentence
- State the merge key and any exclusions from merging
- Report the final merged sample size
- SHAPE: `We combine data from [Source A] with [Source B] using [merge key]. After excluding [criteria], the final sample contains [N] observations.`

### Cost/practicality arguments in methods

[Mousavi 2026] includes cost comparisons as part of the methods justification:
> "Each API request to GPT-4o cost approximately $0.001, yielding a total expenditure of $3.35 for processing a data set of 3,000 items." vs. "$300 for human annotation of the same 3,000-item data set."
- SHAPE: ISR values actionability, so cost arguments strengthen methods papers. State the per-unit cost and total expenditure.

### Online Appendix for methodological overflow

Multiple papers use extensive Online Appendices:
- [Mousavi 2026]: 15 appendices (A through O)
- [Zhang-j 2026]: 21+ electronic companion sections
- [Liu 2025]: referenced ~15 times in main text
- SHAPE: Keep the main methods section focused on the core identification strategy. Detailed derivations, additional specifications, balance tables, and sensitivity analyses belong in the Online Appendix. Reference with: "(see Online Appendix [X] for details)" or "(details in Electronic Companion EC.[X])."

### Design science evaluation framing

[Yang 2022] frames methods through design science:
> "Following the design science approach, we evaluate the operational utility of our proposed artifact in two ways (Gregor and Hevner 2013)."
- For artifact/algorithm papers, the evaluation section replaces the traditional "Empirical Model" section.
- SHAPE: `Following the design science approach, we evaluate [artifact] in [N] ways: (1) [direct performance evaluation], (2) [downstream application/case study].`

### Practitioner recipe section

[Schecter 2025] includes a dedicated section (Section 5) with a step-by-step procedure for applying the proposed method, plus an interpretation template table and a flowchart in the appendix. This is unusual but valued in ISR methodology papers.
- SHAPE for methods papers: after validation, include a "How to Apply" section with numbered steps and/or a decision tree figure.

### Updated anti-patterns

- **Not stating the estimand**: when using matching or quasi-experimental designs, state whether the estimate is ATE, ATT, or LATE. [Liu 2025]
- **Missing cost/resource information for ML methods**: if the paper uses API calls, crowdsourcing, or computational resources, state the cost. [Mousavi 2026]
- **Putting the entire robustness battery in Methods**: robustness checks belong in Results, not Methods. Methods should describe the primary identification strategy only.
