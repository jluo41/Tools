# Diabetes Care -- Abstract Style Guide

Distilled from 10 Diabetes Care papers: Galindo 2026 (RCT), Reaven 2026 (TTE), Bergenstal 2026 (GRADE trial), Lehmann 2026 (ML/Brief Report), Zheng 2025 (NLP), Kahkoska 2025 (e-Letter), He 2026 (e-Letter), Godneva 2026 (TIR), Ajjan 2026 (gDAC), Dupenloup 2026 (cost-effectiveness).

## Word budget

- Original Article abstract: ~200-300 words.
- Brief Report abstract: ~150-200 words.
- e-Letters/Observations: no abstract (body text begins directly).
- The abstract is strictly structured for Original Articles and Brief Reports; unstructured prose is never accepted for these types.

## Structured abstract headings (in order)

1. **OBJECTIVE** -- 1-3 sentences. Clinical context/need + study aim.
2. **RESEARCH DESIGN AND METHODS** -- 2-5 sentences. Study design, data source, population, key methods.
3. **RESULTS** -- 3-6 sentences. Sample size + demographics, primary result with effect size and CI/P, key secondary results.
4. **CONCLUSIONS** -- 1-3 sentences. Main finding restated + clinical implication.

### Contrast with JAMA

JAMA uses 7-9 headings (IMPORTANCE / OBJECTIVE / DESIGN, SETTING, AND PARTICIPANTS / EXPOSURES / MAIN OUTCOMES AND MEASURES / RESULTS / CONCLUSIONS AND RELEVANCE). Diabetes Care uses only 4 headings. The OBJECTIVE in Diabetes Care absorbs the motivational content that JAMA puts under IMPORTANCE. There is no separate EXPOSURES or OUTCOMES heading.

## Article Highlights box (appears before the abstract)

Four labeled bullet points on the graphical abstract page:
- **Why did we undertake this study?** -- 1-2 sentences stating the clinical need or gap.
- **What is the specific question we wanted to answer?** -- 1 sentence, the research question.
- **What did we find?** -- 2-3 sentences with key results including numbers.
- **What are the implications of our findings?** -- 1-2 sentences with clinical/research implication.

Present on Original Articles and Brief Reports. Absent on e-Letters/Observations.

### Exemplar Article Highlights

Lehmann 2026:
> **Why did we undertake this study?** Hypoglycemia is a dangerous diabetes-related emergency, and previous research has suggested that voice is modulated by hypoglycemia.
> **What is the specific question we wanted to answer?** We asked whether machine learning (ML) applied to voice data can detect hypoglycemia in people with diabetes.
> **What did we find?** In two sequential clinical studies, 540 voice recordings were collected from people with type 1 diabetes during standardized euglycemia and hypoglycemia. ML achieved high accuracy in detecting hypoglycemia (area under the receiver operating characteristic curve up to 0.90).
> **What are the implications of our findings?** Our findings show that voice analysis may enable noninvasive hypoglycemia alerts, supporting the broader potential of ML to detect acute health states through voice.

Galindo 2026:
> **Why did we undertake this study?** There is limited evidence on the use of real-time continuous glucose monitoring (rtCGM) in people with type 2 diabetes (T2D) treated with hemodialysis.
> **What is the specific question we wanted to answer?** Would the use of rtCGM improve glycemic outcomes in patients with insulin-treated T2D undergoing hemodialysis?
> **What did we find?** In this randomized controlled trial, we found that percentage time below range was low and not significantly affected by rtCGM use. Compared with capillary blood glucose testing, percentage time in range, percentage time above range, and mean glucose improved during the rtCGM intervention.
> **What are the implications of our findings?** Our results support expanding the use of rtCGM to improve glycemia in people with insulin-treated T2D undergoing hemodialysis.

## Arc

```
OBJECTIVE: context/need + aim (1-3 sentences)
    |
RESEARCH DESIGN AND METHODS: design + source + population + method (2-5 sentences)
    |
RESULTS: N + demographics -> primary effect (CI/P) -> secondary (3-6 sentences)
    |
CONCLUSIONS: main finding restated + implication (1-3 sentences)
```

## Signature moves

1. **OBJECTIVE opener**: Either starts with a clinical need/gap ("There is a need for..."), a known-then-gap pattern ("CGM improves X, but data are lacking for Y"), or a direct infinitive ("To characterize the distribution of...").
   - "There is a need for improved glycemia monitoring tools for people with type 2 diabetes (T2D) and end-stage kidney failure (ESKF)." (Galindo).
   - "Use of continuous glucose monitors (CGM) improves glucose control and reduces hypoglycemia, but data are lacking for its possible role in reducing other serious clinical events." (Reaven).
   - "To characterize the distribution of time in tight and broader glycemic ranges in adults without diabetes and to examine cross-sectional and longitudinal associations with metabolic health." (Godneva).
   - "Hypoglycemia is a hazardous diabetes-related emergency. We aimed to develop a machine learning (ML) approach for noninvasive hypoglycemia detection using voice data." (Lehmann).

2. **RESEARCH DESIGN AND METHODS design naming**: Always names the study design in the opening sentence: "This prospective, randomized, crossover trial..." (Galindo), "We conducted a target trial emulation (TTE) analysis..." (Reaven), "We collected voice data (540 recordings) with a smartphone..." (Lehmann), "We analyzed CGM reports stored as PDF files..." (Zheng).

3. **RESULTS lead sentence**: Opens with sample size and key demographics: "Of the 8,423 individuals initially assigned to both treatment groups, 1,039 were prescribed CGM devices..." (Reaven). "Twenty-two individuals were included (11 female, age 37.3 +/- 12.4 years, HbA1c 7.1 +/- 0.5%)." (Lehmann).

4. **Effect reporting**: Effect size with 95% CI or P value. Continuous: "mean 1.17% +/- 1.8 vs. 1.29% +/- 2.7; P = 0.28" (Galindo). Risk ratio: "adjusted risk ratios of 0.90 (95% CI 0.71-0.97)" (Reaven). AUROC: "0.90 +/- 0.12" (Lehmann). Accuracy: "99.87% for Libre and 100.00% for Dexcom" (Zheng).

5. **CONCLUSIONS**: Restates design name + main finding, then one sentence of clinical implication. "In adults with T2D and ESKF undergoing hemodialysis, TBR was minimal and not influenced by rtCGM use." (Galindo). "In this large TTE of CGM initiation in older T1D patients, CGM use was associated with reduced risk for all-cause mortality." (Reaven).

## Anti-patterns

- Starting OBJECTIVE with the study description ("We conducted...") before stating the clinical context.
- Using a separate IMPORTANCE heading (Diabetes Care does not have one).
- Reporting p-values without effect sizes.
- Using causal language ("reduced", "caused") for observational designs. Use "was associated with" or "was lower with".
- Writing CONCLUSIONS that extend beyond what the data show. Use "may" and "suggest" for observational studies.
- Burying the sample size in the middle of RESULTS rather than leading with it.
- Including abbreviations without defining them (each abbreviation must be defined on first use in the abstract, independently from the main text).
- Using JAMA-style headers (IMPORTANCE, DESIGN SETTING AND PARTICIPANTS, etc.).

## Paragraph structure

The abstract is a single block under each heading, not multiple paragraphs. Each heading is followed by continuous text until the next heading. All four sections are typically printed in a single column on the first text page.
