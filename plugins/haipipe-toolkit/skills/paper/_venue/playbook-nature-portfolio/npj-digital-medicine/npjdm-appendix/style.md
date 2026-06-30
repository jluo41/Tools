# npj Digital Medicine -- Supplementary Material Style Guide

Extracted from two exemplar papers published in npj Digital Medicine (2026).
Sources: [zhuang-2026] Zhuang et al., Clinical large language model centered
on electronic medical records; [lai-2026] Lai et al., An autonomous AI agent
for knowledge and data cooperation in ED clinical decision support.

## Naming convention

The supplement is called **Supplementary Materials** (not "Supplementary
Information" as in Nature flagship journals, and not "Appendix").
Both papers use this label consistently in the main text when referring
to the supplementary file as a whole [zhuang-2026, lai-2026].

## Separate file or same document

The supplementary material is a **separate file** uploaded alongside the
main manuscript. It is not appended to the main article PDF. The main
text refers to it by name without page numbers [zhuang-2026, lai-2026].

## Extended Data

npj Digital Medicine does **not** use the Extended Data mechanism found in
Nature flagship journals. Neither exemplar references Extended Data figures
or tables. All supplementary display items live in the Supplementary
Materials file [zhuang-2026, lai-2026].

## Numbering scheme

### Tables

- [lai-2026] uses an "S" prefix: Supplementary Table S1, Supplementary
  Table S11, Supplementary Table S24, up through S56.
- [zhuang-2026] uses lettered sections with internal table numbers:
  Supplementary Materials Table 5, Supplementary Materials Table 6,
  and refers to entire lettered blocks (Supplementary Materials B,
  Supplementary Materials D, Supplementary Materials E).
- The "S" prefix style (S1, S2, ...) is the more standard Nature-family
  convention. Use sequential Arabic numerals with S prefix:
  Supplementary Table S1, Supplementary Table S2, etc.

### Figures

- Follow the same S-prefix convention: Supplementary Fig. S1,
  Supplementary Fig. S2.
- Neither exemplar had heavy use of supplementary figures; both papers
  placed all main figures in the article body.

### Notes and text sections

- [zhuang-2026] organizes supplementary prose into lettered sections
  (Supplementary Materials B, D, E), each covering a distinct
  methodological topic (benchmark construction, data preprocessing,
  instruction tuning details).
- Use "Supplementary Note 1", "Supplementary Note 2" for extended
  prose sections when needed. Lettered sections are acceptable but
  less conventional across the Nature family.

## How the main text references supplementary material

Inline parenthetical or sentence-level references. Observed forms:

- "...detailed in the Supplementary Materials" (general) [zhuang-2026]
- "...illustrated in Supplementary Materials B" (specific section) [zhuang-2026]
- "...in the supplementary materials (Supplementary Table S1 to S10)" [lai-2026]
- "Supplementary Table S24-S34 for 7-day and Table S35-S45 for 30-day" [lai-2026]

Abbreviation after first use: spell out "Supplementary Table" and
"Supplementary Fig." in full each time. Do not abbreviate to "Suppl."
or "SI".

## What goes in supplementary vs main text (triage rule)

### Main text keeps

- Core results tables and figures that support the primary claims.
- Summary statistics for main experiments.
- Key architectural and method diagrams.

### Supplementary receives

- Detailed evaluation criteria, scoring rubrics, and weighting
  coefficients [zhuang-2026].
- Extended benchmark construction details and data preprocessing
  pipelines [zhuang-2026].
- Instruction tuning implementation details and data statistics
  [zhuang-2026].
- Full bootstrap confidence-interval tables and paired hypothesis-
  testing results across all model comparisons [lai-2026].
- Per-baseline statistical significance breakdowns (e.g., S1-S10 for
  one task, S11-S23 for another) [lai-2026].
- Hyperparameter sensitivity supplementary tables [lai-2026].
- Robustness checks, ablation sub-results, and per-metric breakdowns
  that are referenced but not central to the narrative.

**Rule of thumb**: if a table or figure is needed to verify a specific
number cited in the main text but is not needed to follow the paper's
argument, it belongs in the supplement.

## Typical content inventory

1. Extended statistical tables (confidence intervals, p-values,
   per-comparison breakdowns).
2. Data preprocessing and pipeline implementation details.
3. Evaluation framework specifics (scoring dimensions, weights).
4. Additional ablation and sensitivity analysis results.
5. Dataset construction methodology and statistics.
6. Training configuration and hyperparameter details.

## Length norms

- [lai-2026] has 56 supplementary tables (S1-S56), indicating that
  large supplements are acceptable and common for methods-heavy papers.
- [zhuang-2026] uses multiple lettered sections (at least B through E)
  with embedded tables.
- There is no strict page limit for supplementary materials.
  Supplements of 10-30 pages are typical; exhaustive statistical
  appendices can run longer.
- The supplement should be self-contained enough that a reviewer can
  verify claims without external materials, but concise enough to
  avoid redundancy with the main text.
