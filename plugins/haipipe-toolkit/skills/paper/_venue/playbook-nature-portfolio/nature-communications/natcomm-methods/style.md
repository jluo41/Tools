# NatComm Methods -- Section Style Guide

Extracted from 11 Nature Communications exemplar papers (healthcare AI / clinical ML / LLM in medicine / prescribing). Supplements `style-profile.md`.

## Word budget

- 850-5,500 words, spanning 2-8 pages. Widest variance of any section.
- buckley-2026: ~850w (evaluation-only paper). li-2026-benchmark: ~1,500w. salvatore-2026: ~2,200w. ho-2026: ~2,200w. larcher-2026: ~2,200w. gaudio-2026: ~2,500w. li-2026-memorization: ~3,300w. chen-2026: ~3,500w. adetunji-2026: ~3,000w. abdallah-2026: ~4,500w. zhou-2026: ~4,500w. xu-2026: ~5,500w.
- Methods length scales with the novelty of the technical contribution. Papers proposing new architectures/algorithms have extensive Methods (4,000-5,500w). Evaluation-only papers have moderate Methods (850-1,500w).

## Placement

Methods is placed AFTER Discussion, at the very end of the main text. This is mandatory Nature-family ordering:

```
... -> Discussion -> Methods -> Data availability -> Code availability -> References
```

All 11 exemplars confirm this placement. Methods is never between Introduction and Results.

## Arc

```
Ethics / IRB statement (first subsection in many papers)
  -> System/model architecture (what it is)
  -> Training / optimization details (how it was trained)
  -> Data sources and preprocessing (where data came from, how it was cleaned)
  -> Evaluation methodology (metrics, baselines, test protocol)
  -> Statistical analysis / reproducibility (tests used, sample sizes)
  -> Reporting summary (Nature checklist reference)
  -> Data availability
  -> Code availability
```

The Methods section reads as a recipe: ethics first (when applicable), then architecture, training, data, evaluation, statistics. Data and Code availability always appear as the final subsections.

## Signature moves

1. **Ethics / IRB statement as opening.** Many NatComm papers open Methods with an ethics statement before any technical content:
   - "This study was conducted in accordance with all relevant ethical regulations. The use of de-identified data from the participating cohorts was approved by the relevant institutional review boards." [ho-2026]
   - "This research was conducted in accordance with all relevant ethical regulations. The study protocol was reviewed and approved by the institutional review boards (IRBs) or ethics committees of the participating institutions." [zhou-2026]
   - This is more prominent in NatComm than in NMI, reflecting the journal's clinical scope.

2. **Numbered subsection hierarchy.** Methods is divided into 5-15+ subsections, often with sub-subsections. Common numbering: 4.1, 4.2, 4.3... or unnumbered bold headers:
   - xu-2026: 4.1-4.6 with 4.2.1-4.2.2, 4.3.1-4.3.2, 4.5.1-4.5.5, 4.6.1-4.6.5
   - chen-2026: 14 unnumbered bold-headed subsections
   - li-2026-memorization: 5.1-5.3
   - salvatore-2026: 4.1-4.9
   - zhou-2026: 10+ subsections with sub-subs

3. **Equations appear here, not in Results.** Formal numbered equations are placed in Methods:
   - 0 equations: buckley-2026, li-2026-benchmark (evaluation papers)
   - 1-5 equations: zhou-2026, salvatore-2026
   - 5-16 equations: ho-2026 (16 equations for loss functions), xu-2026 (DPO objective, loss functions)
   - Equations are presented as centered display equations, introduced with prose setup, followed by variable definitions.

4. **Exhaustive hyperparameter specification.** Training details are precise enough for exact replication:
   - "Qwen2.5-72B was selected as the foundation for ClinDiag-GPT due to its optimal diagnostic performance." [chen-2026]
   - "Python v.3.10.13, scikit-sksurv library, MCCV 100 simulations" [larcher-2026]
   - "Python 3.11. NumPy v1.26.4 and pandas v2.3.1 for data processing, scikit-learn v1.7.1 for machine-learning utilities and model evaluation, XGBoost v3.0.0 for gradient-boosted tree classification" [ho-2026]
   - "LoRA hyperparameters" specified [chen-2026, xu-2026, abdallah-2026]
   - GPU model and memory reported when relevant: "NVIDIA A100" [xu-2026]

5. **Dataset provenance with split rationale.** Dataset descriptions include source, size, preprocessing pipeline, and split strategy:
   - "17,267 adults with T2D who received a qualifying drug prescription on or after January 1, 2018" [salvatore-2026]
   - "The primary dataset was derived from the National Alzheimer's Coordinating Center (NACC)...We additionally included participants from the SCAN cohort...For external validation, we incorporated two independent cohorts" [ho-2026]
   - "7,616 real-world cases" for training, "4,421 clinical cases" for testing [chen-2026]
   - Subject/patient-wise splitting to prevent data leakage explicitly noted.

6. **Software version pinning.** Exact software versions are listed, typically in a dedicated paragraph or the Statistics subsection:
   - "Python 3.11. The main software packages used in this study included NumPy v1.26.4 and pandas v2.3.1..." [ho-2026]
   - "Python v.3.10.13" [larcher-2026]
   - R packages and versions when applicable [salvatore-2026, adetunji-2026]

7. **Data and Code availability as mandatory closing subsections.** Every NatComm paper ends Methods with these two labeled subsections:
   - Data availability: URL or access instructions (often tiered: public subset + restricted full data via DUA)
   - Code availability: GitHub URL + Zenodo DOI for archival
   - "Code and data for this work are available via GitHub...and archived on Zenodo" [zhou-2026]
   - "The code is publicly available on GitHub (AIPrimaryCare)" [li-2026-benchmark]
   - GitHub + Zenodo is the dominant pattern (used by 9 of 11 papers).

8. **Statistics & Reproducibility subsection.** A standard subsection (sometimes called "Statistical Analysis") specifying the statistical tests used:
   - "Two-sided Welch's t-tests, Benjamini-Hochberg correction" [gaudio-2026]
   - "McNemar's test, power analysis" [chen-2026]
   - "Bonferroni correction, Schoenfeld residuals, Firth correction" [salvatore-2026]
   - "ANOVA, chi-squared, Fisher's exact tests, two-sided t-tests" [ho-2026]

9. **Reporting summary reference.** A brief "Reporting summary" subsection points to the Nature Portfolio Reporting Summary checklist:
   - "Further information on research design is available in the Nature Portfolio Reporting Summary linked to this article." (standard language across papers)

10. **Heavy use of supplement for extended details.** When Methods would become too long, detail is deferred:
    - "Detailed fine-tuning results are presented in Supplementary Table 1." [chen-2026]
    - "See Supplementary Materials 'Literature Review' section H for additional details." [abdallah-2026]
    - "Details about this can be found in Section 4.1." (cross-references within the paper) [xu-2026]

## Exemplar sentences (shape, not content)

**Architecture description**:
- "The GAME algorithm is built upon the Graph Attention Network (GAT), a variant of GNNs, which serves as the core architecture for harmonizing multi-institutional EHR code embeddings." [zhou-2026]
- "The proposed framework consists of three main components. (a) First, T1-weighted MRI scans were preprocessed through reorientation, bias correction, skull stripping, and MUSE-based region extraction." [ho-2026]

**Ethics subsection**:
- "This study was conducted in accordance with all relevant ethical regulations." [ho-2026, zhou-2026]
- "Ethical compliance: All experiments were conducted in accordance with..." [abdallah-2026]

**Data availability**:
- "Data are available via the All of Us Research Program (https://allofus.nih.gov/)" [salvatore-2026]
- "Data from NACC is available upon request at https://www.alz.washington.edu/" [ho-2026]

## Anti-patterns

- Do NOT place Methods before Results. Nature-family ordering puts Methods at the end.
- Do NOT combine Methods with Results in a single section. They are always separate.
- Do NOT omit hyperparameters. NatComm expects exact reproducibility details (learning rate, batch size, optimizer, GPU, epochs) for ML papers.
- Do NOT omit Data/Code availability subsections. These are mandatory.
- Do NOT omit the ethics/IRB statement for papers involving human data.
- Do NOT put primary equations in Results. Equations belong in Methods (or supplement).
- Do NOT write Methods in passive voice exclusively. NatComm Methods uses a mix: "We trained the model using..." and "The model was evaluated on..."
- Do NOT omit the Statistics & Reproducibility subsection. This is standard across NatComm papers.

## Paragraph structure

Methods subsections are typically 1-4 paragraphs each, 100-400 words per paragraph. Each subsection covers one methodological component completely. The internal structure:

1. **What** (1 sentence): name the component
2. **How** (3-8 sentences): describe the implementation with hyperparameters/details
3. **Why** (0-1 sentences): optional rationale for design choices (often deferred to supplement)

## Contrast with NMI

- NMI Methods are typically 1,200-3,000 words. NatComm Methods have a wider range (850-5,500 words), scaling with technical novelty.
- NMI rarely opens Methods with an ethics statement. NatComm frequently does, reflecting its broader clinical scope.
- Both journals require Data/Code availability and Reporting Summary subsections.
- Both place Methods after Discussion.
- NatComm includes more extensive statistical analysis subsections, particularly for epidemiological papers.

## Contrast with IS journals

- IS Methods sections appear between Introduction/Theory and Results. NatComm Methods appear after Discussion.
- IS Methods focus on research design, variable operationalization, and econometric specification. NatComm Methods focus on architecture, training protocol, dataset provenance, and statistical analysis.
- IS journals rarely include equations in Methods (equations appear in Theory). NatComm puts equations in Methods.
- IS journals do not have Data/Code availability subsections. NatComm requires them.
- IS Methods do not include IRB/ethics statements. NatComm frequently does.
- IS Methods do not include a Reporting Summary. NatComm includes a standardized Nature checklist.
