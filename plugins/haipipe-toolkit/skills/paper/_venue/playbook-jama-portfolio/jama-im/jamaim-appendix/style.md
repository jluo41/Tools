# JAMA Internal Medicine -- Supplementary Material Style

Patterns extracted from two JAMA Internal Medicine Original Investigation exemplars.

Sources:
- [williams-2025] Williams et al. "Physician- and Large Language Model-Generated Hospital Discharge Summaries." JAMA Intern Med. 2025;185(7):1-8.
- [fournier-2026] Fournier et al. "Deprescribing Intervention and Reduction of Proton Pump Inhibitor Use in Primary Care." JAMA Intern Med. 2026;186(6):668-676.

---

## Naming convention

JAMA IM uses numbered **Supplements**, identical to JAMA flagship.
The label is always "Supplement N" (capitalized, no article): Supplement 1, Supplement 2, etc.
Each Supplement is a separate file uploaded alongside the main manuscript.

## Multiple Supplements convention

The number and role of Supplements depends on study design.

**RCTs** (e.g., [fournier-2026]) use 3 Supplements:

| Supplement | Content |
|---|---|
| Supplement 1 | Trial protocol and intervention materials |
| Supplement 2 | All supplementary data: eMethods, eTables |
| Supplement 3 | Data sharing statement (nonclinical information) |

**Non-RCT studies** (e.g., [williams-2025]) use 2 Supplements:

| Supplement | Content |
|---|---|
| Supplement 1 | All supplementary data: eAppendices, eTables, eFigures |
| Supplement 2 | Data sharing statement (nonclinical information) |

In non-RCT papers, Supplement 1 absorbs the role that Supplement 2 plays in RCTs because there is no standalone protocol document.

## The "e" prefix system

All supplementary items carry a lowercase "e" prefix, numbered sequentially within each type. The numbering is independent from main-text items.

- **eTable**: eTable 1, eTable 2, ... eTable 6 [williams-2025]; eTable 1 [fournier-2026]
- **eFigure**: eFigure 1, eFigure 2, ... eFigure 5 [williams-2025]
- **eAppendix**: eAppendix 1 through eAppendix 4 [williams-2025]. Used for text-heavy supplementary sections (study protocol, prompts, scoring definitions, quantitative metric descriptions).
- **eMethods**: eMethods 1, eMethods 2 [fournier-2026]. Numbered when multiple distinct method sections exist.

Main-text items use plain labels (Table 1, Figure 1). Supplementary items use "e" prefix labels. The two numbering streams never overlap.

## How the main text references supplementary material

The main text always specifies both the item and the Supplement number.
The reference pattern is: **"eItem N in Supplement M"**.

Observed forms:
- "eAppendix 1 in Supplement 1" [williams-2025]
- "eTable 2 and eFigure 3 in Supplement 1" [williams-2025]
- "eTables 3 and 4 in Supplement 1" [williams-2025]
- "eMethods 1 in Supplement 2" [fournier-2026]
- "eMethods 1 and 2 in Supplement 2" [fournier-2026]
- "eTable 1 in Supplement 2" [fournier-2026]
- "eTables 2-3 in Supplement 2" [fournier-2026]
- "eTables 4 and 5 in Supplement 2" [fournier-2026]

For the protocol itself (no e-prefix item), the reference is the bare Supplement number:
- "available in Supplement 1" [fournier-2026]
- "is presented in Supplement 1" [fournier-2026]

Never write "in the Supplement" (no article). Always "in Supplement N."

## What goes in the main text vs the supplement

**Main text** (typically 6-9 typeset pages, strict word limit):
- Core tables answering primary/secondary hypotheses: up to 4 tables [williams-2025] or 3 tables [fournier-2026]
- Key figures: 1 figure [williams-2025]; 2 figures (CONSORT flow + primary outcome trend) [fournier-2026]
- Primary and secondary outcome results stated in prose

**Supplement (data):**
- Study protocol or prespecified protocol details [williams-2025: eAppendix 1]
- Detailed methods (prompts, scoring rubrics, metrics): eAppendix 2-4 [williams-2025]; eMethods 1-2 [fournier-2026]
- Cohort flow diagrams and encounter processing visuals: eFigure 1-2 [williams-2025]
- Extended baseline/demographic/clinical characteristics: eTables 3-4 [williams-2025]; eTable 1 [fournier-2026]
- Sensitivity and robustness analyses: eTables 2-3 [fournier-2026]
- Subgroup analyses: eTables 4-5 [fournier-2026]
- Detailed error examples or edge cases: eTables 5-6 [williams-2025]
- Additional distribution plots: eFigures 4-5 [williams-2025]

**Triage rule**: if the result directly answers a stated hypothesis, it goes in the main text. Robustness checks, subgroup breakdowns, extended baseline tables, measurement definitions, and supplementary process diagrams go in the Supplement.

## Length norms

- **Main text**: 6-9 typeset pages. Williams: 8 pages, 1 figure + 4 tables. Fournier: 9 pages, 2 figures + 3 tables.
- **Supplement (data)**: no hard page cap. Williams used 6 eTables + 5 eFigures + 4 eAppendices. Fournier used 5 eTables + 2 eMethods. Supplements are expected to be organized and concise.
- **Protocol Supplement**: variable length, standalone document. Required for RCTs.

## Differences from JAMA flagship

1. **eAppendix label**: JAMA IM uses numbered "eAppendix N" for text-heavy supplementary sections [williams-2025]. The JAMA flagship exemplars used "eMethods" (singular or numbered) instead.
2. **Supplement allocation for non-RCTs**: JAMA IM non-RCT papers pack all supplementary data into Supplement 1 (no separate protocol). JAMA flagship exemplars were RCTs and always reserved Supplement 1 for the protocol.
3. **Otherwise identical**: the "e" prefix system, "eItem N in Supplement M" citation pattern, data-sharing-as-last-Supplement convention, and separate-file-per-Supplement structure are the same across JAMA IM and JAMA flagship.
