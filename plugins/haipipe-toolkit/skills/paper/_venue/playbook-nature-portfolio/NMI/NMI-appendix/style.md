# NMI Appendix -- Section Style Guide

Extracted from 2 Nature Machine Intelligence exemplar papers. Supplements `style-profile.md`.

## Two-tier structure: Extended Data vs Supplementary Information

Nature Machine Intelligence uses a strict two-tier system for material beyond the main text. These are distinct in status, review process, and file location.

**Extended Data** (peer-reviewed, in-article):
- Appears at the end of the main article PDF, after References but before the Reporting Summary.
- Limited to at most 10 figures and 10 tables total (Nature portfolio policy).
- Peer-reviewed alongside the main text. Considered part of the published article.
- Used for key supporting evidence that reviewers must evaluate: score distributions, correlation heatmaps, supplementary visualizations that directly support main-text claims. [serapio-garcia-2025: Extended Data Figs. 1-4, Extended Data Tables 1-7]
- Not all NMI papers use Extended Data. Some put everything into Supplementary Information. [gu-2026: no Extended Data used]

**Supplementary Information** (separate file, online-only):
- Published as a separate PDF file linked from the article page.
- Not subject to the same space constraints as Extended Data.
- Used for methodological details, background literature, additional results, prompt examples, full parameter tables, and analyses that support but are not essential to the main narrative. [serapio-garcia-2025: Supplementary Notes A.1-A.11, Supplementary Tables 1-17]
- Numbered sections provide detailed expansions referenced from the main text. [gu-2026: Supplementary Information sections 1-3.7, Supplementary Table 7]

## Naming convention

| Element | Label format | Example |
|---|---|---|
| Extended Data figure | Extended Data Fig. N | Extended Data Fig. 1 [serapio-garcia-2025] |
| Extended Data table | Extended Data Table N | Extended Data Table 3 [serapio-garcia-2025] |
| Supplementary note | Supplementary Note A.N.M | Supplementary Note A.6.3 [serapio-garcia-2025] |
| Supplementary section | Supplementary Information section N.M | Supplementary Information section 3.2 [gu-2026] |
| Supplementary figure | Supplementary Fig. N | (not observed in these exemplars; follows Nature convention) |
| Supplementary table | Supplementary Table N | Supplementary Table 17 [serapio-garcia-2025] |

Numbering is independent per tier: Extended Data Fig. 1 and Supplementary Fig. 1 are separate objects. Within each tier, figures and tables have their own counters (not shared). Supplementary Notes use hierarchical numbering (A.1, A.1.1, A.6.3).

## How the main text references appendix material

References are parenthetical or inline, always using the full label. Observed patterns:

- Parenthetical: "(Extended Data Fig. 1)" or "(Supplementary Table 2)" [serapio-garcia-2025]
- Inline directive: "see Supplementary Note A.1.2 on the background of personality science" [serapio-garcia-2025]
- Clause-integrated: "Further statistical details are available in Supplementary Information section 1." [gu-2026]
- Combined: "results are summarized in Table 1 and raw reliability data are provided in Extended Data Tables 1 and 2" [serapio-garcia-2025]

Never abbreviated after first use (always "Extended Data Fig.", never "ED Fig."). Never bare numbers ("see Note A.6" is wrong; "see Supplementary Note A.6" is correct).

## Triage rule: what goes where

**Main text** (up to ~14 pages of text + figures):
- Core results figures and tables essential to the paper's argument.
- The narrative arc: problem, methods overview, key results, discussion.

**Extended Data** (optional; up to 10 figs + 10 tables):
- Supporting visualizations that directly substantiate main-text claims and that reviewers must inspect.
- Full data tables summarized in the main text (e.g., per-model reliability metrics). [serapio-garcia-2025: Extended Data Tables 1-7]
- Distribution plots, heatmaps, and result breakdowns by condition. [serapio-garcia-2025: Extended Data Figs. 1-4]

**Supplementary Information** (separate file, no hard limit):
- Background and related work expansions. [serapio-garcia-2025: Supplementary Notes A.1-A.2]
- Detailed methodology (prompt design, scoring rationale, implementation). [serapio-garcia-2025: Supplementary Notes A.3-A.4; gu-2026: Supplementary Information sections 2.2-2.3]
- Extended results commentary and per-domain breakdowns. [serapio-garcia-2025: Supplementary Notes A.6-A.8; gu-2026: sections 3.2-3.7]
- Dataset descriptions and statistics. [gu-2026: Supplementary Information section 1]
- Full prompt text, stimuli lists, parameter sweeps. [serapio-garcia-2025: Supplementary Tables 1-3, 17]
- Robustness checks and ablation details.

## Length norms

- Main text: 14-15 pages as published (typically ~3,000-5,000 words of prose plus figures). [serapio-garcia-2025: pp. 1954-1968; gu-2026: pp. 220-233]
- Extended Data: typically 2-6 pages within the article PDF. Contains figures/tables only (captions, no running prose). [serapio-garcia-2025: 4 figures + 7 tables]
- Supplementary Information: unconstrained; commonly 20-60+ pages for methods-heavy NMI papers. Organized as a self-contained document with numbered sections.

## File structure

- The main article PDF contains: main text, references, Extended Data figures/tables (if any), and the Reporting Summary checklist.
- Supplementary Information is a separate PDF file, hosted online and linked from the article's "Additional information" section.
- Both papers include in the "Additional information" section: "Supplementary information The online version contains supplementary material available at [DOI]." [serapio-garcia-2025, gu-2026]
- When Extended Data is present, an additional line appears: "Extended data is available for this paper at [DOI]." [serapio-garcia-2025]

## Anti-patterns

- Do NOT mix Extended Data and Supplementary numbering (they are separate counters).
- Do NOT put running prose in Extended Data (captions and legends only; detailed discussion goes in Supplementary Notes).
- Do NOT abbreviate labels after first use. Always write "Extended Data Fig." and "Supplementary Table" in full.
- Do NOT place essential-to-the-argument figures in Supplementary Information; those belong in Extended Data or main text (reviewers may not examine SI as closely).
- Do NOT exceed 10 figures + 10 tables in Extended Data (Nature portfolio hard cap).
