# JAMA Flagship -- Supplementary Material Style

Patterns extracted from two JAMA Original Investigation exemplars.

Sources:
- [mathioudakis-2025] Mathioudakis et al. "An AI-Powered Lifestyle Intervention vs Human Coaching in the Diabetes Prevention Program." JAMA 2025;334(23):2079-2089.
- [krebs-2018] Krebs et al. "Effect of Opioid vs Nonopioid Medications on Pain-Related Function." JAMA 2018;319(9):872-882.

---

## Naming convention

JAMA uses numbered **Supplements**, not "Appendix" or "eAppendix."
Each Supplement is a separate file uploaded alongside the main manuscript.
The label is always "Supplement N" (capitalized, no article): Supplement 1, Supplement 2, etc.

## Multiple Supplements convention

JAMA RCTs typically use 3-4 Supplements with fixed roles:

| Supplement | Content | Source |
|---|---|---|
| Supplement 1 | Trial protocol and statistical analysis plan (SAP) | [mathioudakis-2025], [krebs-2018] |
| Supplement 2 | All supplementary data: eTables, eFigures, eMethods | [mathioudakis-2025], [krebs-2018] |
| Supplement 3 | Study group / investigator list (if applicable) | [mathioudakis-2025] |
| Supplement 4 | Data sharing statement | [mathioudakis-2025] |

Non-RCT papers may use fewer Supplements. Supplement 1 always contains the protocol/SAP for trials.

## The "e" prefix system

All supplementary display items and methods sections carry a lowercase "e" prefix.
The numbering is independent from the main text and sequential within each type:

- **eTables**: eTable 1, eTable 2, ... eTable 20 [mathioudakis-2025]; eTable 1 through eTable 10 [krebs-2018]
- **eFigures**: eFigure 1, eFigure 2, eFigure 3, eFigure 4 [mathioudakis-2025]
- **eMethods**: eMethods (singular, not numbered) [mathioudakis-2025]

Main-text items use plain labels: Table, Table 1, Figure 1, Figure 2.
Supplementary items use the "e" prefix: eTable 1, eFigure 1.
The two numbering streams never overlap.

## How the main text references supplementary material

The main text always specifies both the item and the Supplement number.
The pattern is: **"eItem N in Supplement M"**.

Examples from the papers:
- "eTable 2 in Supplement 2" [mathioudakis-2025]
- "eFigure 1 in Supplement 2" [mathioudakis-2025]
- "eMethods and eFigures 1 and 2 in Supplement 2" [mathioudakis-2025]
- "eFigure 3, eTables 16-19 in Supplement 2" [mathioudakis-2025]
- "eTables 1-2 in Supplement 2" [krebs-2018]
- "eTable 6 in Supplement 2" [krebs-2018]
- "eTables 7-8 in Supplement 2" [krebs-2018]

For the protocol or SAP, the reference is just the Supplement number:
- "available in Supplement 1" [mathioudakis-2025]
- "are in Supplement 1" [krebs-2018]

For study group listings or data sharing: "appears in Supplement 3" [mathioudakis-2025].

Never write "in the Supplement" (no article, no definiteness). Always "in Supplement N."

## What goes in the main text vs the supplement

**Main text** (strict space constraint, ~3000 words for Original Investigations):
- 1 main baseline characteristics table (Table or Table 1) [both papers]
- Primary outcome results with 1-2 key figures (Figure 1 = CONSORT/flow; Figure 2 = primary result) [both papers]
- Secondary outcome tables with core timepoints (Table 2, Table 3) [krebs-2018]
- Key sensitivity/subgroup results stated in prose, referencing supplement for details

**Supplement 2** (no strict length limit; all supplementary data):
- Extended baseline characteristics by subgroup (eTable 4-7) [mathioudakis-2025]
- Eligibility criteria prevalence by group (eTable 4) [mathioudakis-2025]
- Site-level comparisons (eTable 5) [mathioudakis-2025]
- Sensitivity and subgroup analyses (eTables 12-19) [mathioudakis-2025]
- Adverse events detail (eTable 20) [mathioudakis-2025]
- Intervention description and visuals (eMethods, eFigures 1-2) [mathioudakis-2025]
- Medication dosing and adherence details (eTables 6-10) [krebs-2018]
- Actigraphy processing details [mathioudakis-2025]
- Any analysis that supports but does not carry the primary finding

**Triage rule**: if the result directly answers the primary or secondary hypothesis, it goes in the main text. Everything else -- robustness checks, subgroup breakdowns, intervention implementation details, protocol-level measurement descriptions, additional baseline stratifications -- goes in Supplement 2.

## Length norms

- **Main text**: 11 pages typeset, ~3000 words excluding abstract/references, 4 figures + 1 table [mathioudakis-2025]; 11 pages, 4 tables + 1 figure [krebs-2018].
- **Supplement 2**: typically 15-30 pages. Up to 20 eTables and 4 eFigures observed [mathioudakis-2025]; 10 eTables observed [krebs-2018]. No hard cap but reviewers expect concise, well-organized supplements.
- **Supplement 1** (protocol/SAP): variable length, often 30-80 pages; this is a standalone document.

## File structure

Each Supplement is a separate PDF file uploaded during submission.
They are not appended to the main manuscript.
JAMA assigns the Supplement numbers during production.
Authors label items within each Supplement (eTable 1, eFigure 1, etc.) but do not control Supplement numbering until the editorial office confirms it.

## Practical checklist for authors

1. Label all supplementary tables as eTable 1, eTable 2, ... (sequential, no gaps).
2. Label all supplementary figures as eFigure 1, eFigure 2, ... (sequential, no gaps).
3. Label supplementary methods as eMethods (singular unless multiple distinct sections).
4. In the main text, always cite as "eTable N in Supplement M" -- never bare "eTable N."
5. Place the trial protocol and SAP in Supplement 1 (required for RCTs).
6. Place all eTables, eFigures, and eMethods together in Supplement 2.
7. If applicable, place investigator/study group lists in Supplement 3.
8. Place the data sharing statement in the final Supplement.
9. Number main-text items (Table 1, Figure 1) and supplementary items (eTable 1, eFigure 1) as two independent sequences.
