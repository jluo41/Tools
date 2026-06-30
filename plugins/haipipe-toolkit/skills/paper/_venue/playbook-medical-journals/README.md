# Medical Specialty Journals (paper/_venue)

A **medical-specialty-journal** style + structure exemplar pack for the paper pipeline. Currently covers **Diabetes Care** (American Diabetes Association). Its main job is to hold the CONTENT of real Diabetes Care papers so we can **imitate their language style and preferences**, alongside a distilled style profile and concrete lifecycle-stage mappings.

## Relationship to the venue layer

- `playbook-jama-portfolio` = general-medicine journals (JAMA, JAMA IM, JAMA Network Open). Structured abstract uses IMPORTANCE / OBJECTIVE / DESIGN, SETTING, AND PARTICIPANTS / EXPOSURES / MAIN OUTCOMES / RESULTS / CONCLUSIONS AND RELEVANCE. Key Points box (Question / Findings / Meaning).
- `playbook-medical-journals` (here) = **medical specialty journals** that follow their own society conventions. Diabetes Care uses ADA-specific abstract headings (OBJECTIVE / RESEARCH DESIGN AND METHODS / RESULTS / CONCLUSIONS) and the ADA Article Highlights box instead of Key Points.

Key differences from JAMA portfolio:
- Abstract headings are ADA format, not JAMA format (no IMPORTANCE, no DESIGN/SETTING/PARTICIPANTS block).
- Article Highlights replaces Key Points (4 narrative bullets instead of 3 labeled one-liners).
- "RESEARCH DESIGN AND METHODS" (not just "Methods").
- "Supplementary Material" or "Supplementary Data" (not numbered Supplements).
- Vancouver numbered references (not JAMA superscript).
- ADA Standards of Care is a near-mandatory citation.
- CGM-specific terminology (TIR, TBR, TAR, GMI, MARD, AGP) is domain vocabulary.
- Figures/tables use em-dash separator: "Figure 1--Caption text." (not period or colon).

No duplication: cross-family principles live in the parent `_venue/`; exemplars + stage mappings live here.

## Structure

```
playbook-medical-journals/
  README.md              this hub + the lifecycle-stage mappings
  style-profile.md       distilled language style + preferences to imitate
  diabetes-care/         per-section style guides for Diabetes Care
    diabcare-abstract/style.md
    diabcare-introduction/style.md
    diabcare-methods/style.md
    diabcare-results/style.md
    diabcare-discussion/style.md
    diabcare-appendix/style.md
  exemplars/             stored CONTENT (PDFs / extracted text) of same-venue papers
  references/            citation candidates (secondary; verify before citing)
```

## How to use

At the claims / display / minimap stages, consult this playbook for (a) the Diabetes Care-shaped target for that artifact and (b) the nearest exemplar paper in `exemplars/`. The target venue is set in the paper's `STATUS.md` (`venue`).

---

## Maps to lifecycle stages

### -> Claims (`0-lifecycle/2-claims`)

- Exactly ONE `[primary]` clinical claim: an association, prediction, or technology-validation finding on a diabetes-relevant outcome (glycemic control, complications, mortality, cost-effectiveness).
- 2-4 supporting claims: mechanism, dose-response, subgroup heterogeneity, safety, robustness.
- CGM/technology papers: the clinical outcome is the claim; the technology (CGM, ML, NLP) is an **enabler** in Methods, NOT a claim.
- Observational data => associational language ("was associated with"), never causal verbs. RCTs can use stronger language but still hedge ("resulted in improved" not "caused").
- ADA Standards of Care should be cited when the claim connects to a current recommendation.
- Prediction/ML papers: primary claim is diagnostic accuracy (AUROC, sensitivity/specificity); clinical utility is the supporting claim.

### -> Display (`0-displays`)

Diabetes Care standard display set:
- **Graphical abstract / visual abstract** (increasingly common; appears on the journal cover page before the text).
- **Article Highlights** (mandatory): 4-bullet box before the abstract.
- **Table 1** baseline / cohort characteristics (mandatory for Original Articles).
- **Cohort flow diagram** (CONSORT for RCTs; STROBE-style for observational): selection from source to analytic sample.
- **Primary-outcome display** (the HERO, tied to `[primary]` claim): CGM metrics comparison (stacked bar for TIR/TAR/TBR ranges), survival curves, forest plot, or accuracy ROC curves.
- **Ambulatory glucose profile (AGP)** figure when CGM data are the exposure or outcome.
- **Subgroup / sensitivity analysis** (forest plot or supplementary table).
- Mapping rule: each claim -> one display; `[primary]` claim -> hero display; Table 1 + flow diagram are always present for Original Articles.

### -> Minimap (`0-lifecycle/5-minimap`)

Diabetes Care IMRAD with ADA-specific headings:
- **Abstract**: OBJECTIVE / RESEARCH DESIGN AND METHODS / RESULTS / CONCLUSIONS (4 headings, not 7-9 like JAMA).
- **Article Highlights**: 4 bullets (Why did we undertake this study? / What is the specific question? / What did we find? / What are the implications?).
- **Introduction** (~3-5 paragraphs): clinical burden -> what is known -> the gap ("however") -> what we did.
- **Research Design and Methods**: study design, population, exposure/intervention, outcomes, statistical analysis (subsections with bold headings).
- **Results**: cohort description + Table 1 -> primary outcome -> secondary outcomes -> subgroup/sensitivity analyses.
- **Discussion**: principal findings -> comparison to prior work -> mechanisms -> ADA Standards context -> Limitations -> future directions.
- **Conclusions**: separate paragraph or final Discussion paragraph restating the main finding with clinical implication.
- Mapping rule: the `[primary]` claim drives the abstract CONCLUSIONS, the lead Results paragraph, and the first Discussion interpretation.

### -> Write / Edit (language style & preferences)  [the main purpose]

Imitate how Diabetes Care papers actually read:
- Consult `style-profile.md` for the distilled style rules.
- Read the nearest paper in `exemplars/` and mirror its sentence shapes and section moves (its style), not its content.
- Apply at the write/edit stages, and to the pitch and abstract.
- Per-section style guides in `diabetes-care/diabcare-{section}/style.md` provide word budgets, arc, signature moves, exemplar sentences, and anti-patterns.

---

## Outlets (per-journal delta)

Currently this pack covers one outlet: **Diabetes Care**. The pack is extensible to other ADA-family journals (Diabetes, Diabetes Spectrum) and other specialty societies (e.g., Endocrine Society journals) by adding per-outlet subdirectories.

### Article types in Diabetes Care

| Type | Abstract | Word limit | Tables/Figures | Refs |
|---|---|---|---|---|
| Original Article | Structured (4 headings) | ~4000 text | Up to 6 total | ~40 |
| Brief Report | Structured (4 headings, shorter) | ~2500 text | Up to 3 total | ~20 |
| e-Letters -- Observations | Unstructured (running text, no section headers) | ~1000 text | 1-2 total | ~5 |
| Review / Consensus | Structured or unstructured | Variable | Variable | Variable |

---

## references/ (citation candidates, secondary)

Verified, real papers that could be CITED in related work. See `references/README.md`. Always re-verify with `citation-audit` before any enters the manuscript.
