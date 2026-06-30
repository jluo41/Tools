# Diabetes Care -- Supplementary Data / Appendix Style Guide

Distilled from 10 Diabetes Care papers: Galindo 2026 (RCT/Brief), Reaven 2026 (TTE), Bergenstal 2026 (GRADE), Lehmann 2026 (ML/Brief), Zheng 2025 (NLP), Kahkoska 2025 (e-Letter), He 2026 (e-Letter), Godneva 2026 (TIR), Ajjan 2026 (gDAC), Dupenloup 2026 (cost-effectiveness).

## Naming convention

Diabetes Care uses **Supplementary Material** or **Supplementary Data** (not "Supplement 1/2" as JAMA uses, not "Supporting Information" as some other journals use). There is no numbered supplement system; all supplementary items belong to a single supplementary package.

## Hosting

Supplementary material is hosted on **figshare** through the ADA's arrangement:
- "This article contains supplementary material online at https://doi.org/10.2337/figshare.[ID]."
- This statement appears in the author information block on the first text page, not in the Methods or back matter.

## Item labeling (the "Supplementary" prefix system)

All supplementary items use a capitalized "Supplementary" prefix, followed by the item type and a sequential number within each type. The numbering is independent from main-text items.

- **Supplementary Fig.** (abbreviated): Supplementary Fig. 1, Supplementary Fig. 2, etc.
- **Supplementary Table**: Supplementary Table 1, Supplementary Table 2, etc.
- **Supplementary Methods**: Not numbered unless there are multiple distinct method sections.
- **Supplementary Material Methods**: Used as a variant (Reaven).

Main-text items use plain labels (Fig. 1, Table 1). Supplementary items use the "Supplementary" prefix. The two numbering streams never overlap.

### Contrast with JAMA

JAMA uses numbered "Supplements" (Supplement 1 = protocol, Supplement 2 = data, Supplement 3 = data sharing) with "e" prefix items (eTable 1, eFigure 1, eMethods). Diabetes Care uses a single supplementary package with "Supplementary" prefix items. No "e" prefix is used.

## How the main text references supplementary material

The main text always uses the "Supplementary" prefix in parentheses:

Observed forms:
- "(Supplementary Fig. 1)" (Galindo, Lehmann)
- "(Supplementary Table 1)" (Galindo, Zheng, He)
- "(Supplementary Material)" (Galindo, Lehmann)
- "(Supplementary Material Methods)" (Reaven)
- "(Supplementary Methods)" (Lehmann)
- "(Supplementary Figs. 1 and 2)" (Godneva)
- "(Supplementary Tables 2-11)" (Dupenloup)
- "see Supplementary Material for details" (various)
- "additional details provided in the Supplementary Methods" (Lehmann)

Never write "in the supplement" or "in the online supplement". Always use the capitalized "Supplementary" prefix.

## What goes in the main text vs. supplementary material

**Main text** (Original Articles: ~6-10 typeset pages):
- Core tables answering primary/secondary outcomes (up to 4 tables).
- Key figures: flow diagram, primary outcome figure, ambulatory glucose profiles.
- Primary and secondary outcome results stated in prose.

**Supplementary material:**
- Extended methods: detailed inclusion/exclusion criteria, statistical model specifications, sensitivity analysis protocols.
- Flow diagrams (when the primary figure is a results figure): Supplementary Fig. 1 = cohort flow in Galindo.
- Additional CGM metrics: on/off dialysis comparisons (Galindo Supplementary Table 1).
- Extended baseline characteristics or balance tables (Reaven Supplementary Tables 1-5).
- Sensitivity and robustness analyses: alternative grace periods, additional adjustments (Reaven Supplementary Figs. 2-4).
- Algorithm details, hyperparameters, feature sets (ML papers).
- CHEERS checklists, Impact Inventories (cost-effectiveness papers: Dupenloup Supplementary Tables 12-13).

**Triage rule**: If the result directly answers the primary or secondary research question, it goes in the main text. Extended methods, robustness checks, subgroup breakdowns, measurement definitions, and additional analyses go in the Supplementary Material.

## Typical supplementary item counts by paper type

| Paper type | Supp Tables | Supp Figures | Supp Methods |
|---|---|---|---|
| RCT Brief Report (Galindo) | 1 | 3 | 0 |
| TTE Original (Reaven) | 5 | 4 | 1 (Material Methods) |
| Trial substudy (Bergenstal) | 8 | 5 | 0 |
| ML Brief Report (Lehmann) | 0 | 1 | 1 |
| NLP Original (Zheng) | 1 | 0 | 0 |
| e-Letter (He) | 3 | 0 | 1 |
| e-Letter (Kahkoska) | 0 | 0 | 0 |
| Observational (Godneva) | 9 | 2 | 0 |
| Observational (Ajjan) | 2 | 3 | 0 |
| Cost-effectiveness (Dupenloup) | 17 | 5 | 0 |

Original Articles can have extensive supplementary material (Dupenloup: 17 tables + 5 figures). Brief Reports and e-Letters have minimal or no supplementary material.

## Data and Resource Availability

The **Data and Resource Availability** subsection at the end of RESEARCH DESIGN AND METHODS serves as the data sharing statement. This is separate from the supplementary material hosting.

Standard patterns:
- "Deidentified participant data will be made available 24 months after publication and for up to 12 months after upon reasonable request for meta-analysis purposes and with an institutional review board-approved protocol to the corresponding author." (Galindo).
- "The VA supports that data (deidentified participant data) from approved studies be made publicly available upon request." (Reaven).
- "The data sets generated during and analyzed in the current study are available from the corresponding author upon reasonable request." (standard).

## Back matter sections (in order, after CONCLUSIONS)

Every Diabetes Care paper includes these back matter sections in this exact order, each with a **bold** label followed by a period:

1. **Acknowledgments.** -- thanks participants, staff, administrative support.
2. **Funding.** -- grant numbers and funding agencies, stated in full.
3. **Duality of Interest.** -- conflict of interest disclosures. Clean: "No potential conflicts of interest relevant to this article were reported."
4. **Author Contributions.** -- who did what, using author initials. Includes the **guarantor statement**: "[Initials] is the guarantor of this work and, as such, had full access to all the data in the study and takes responsibility for the integrity of the data and the accuracy of the data analysis."
5. **Prior Presentation.** (optional) -- conference presentations of preliminary data: "Parts of this study were presented in abstract form at the [meeting name], [location], [dates]."
6. **Handling Editors.** -- names the action editor(s): "The journal editors responsible for overseeing the review of the manuscript were [names]."
7. **References** -- Vancouver numbered list.

### Contrast with JAMA

JAMA uses "Conflict of Interest Disclosures" (not "Duality of Interest"). JAMA does not include a "Handling Editors" section. JAMA's "Data Sharing Statement" is a separate numbered Supplement (the last one), not a Methods subsection.

## Anti-patterns

- Using "Supplement 1" or "eTable" (JAMA convention) instead of "Supplementary Table 1".
- Omitting the Data and Resource Availability subsection.
- Using lowercase "supplementary" (always capitalize).
- Writing "in the supplement" or "in the online supplement" instead of "(Supplementary Table 1)" with the specific item.
- Omitting the guarantor statement from Author Contributions.
- Listing back matter sections in the wrong order.
