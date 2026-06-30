# Nature Communications -- Supplementary Material Style

Patterns extracted from two exemplar papers accepted at Nature Communications (Article in Press, 2026).

## Terminology

Nature Communications uses two distinct supplementary categories:

- **Supplementary Information** -- a single PDF containing narrative text (Supplementary Notes), figures (Supplementary Figures), and tables (Supplementary Tables). This is the prose-and-visual supplement. [xu-2026, salvatore-2026]
- **Supplementary Data** -- machine-readable files (typically .xlsx or .csv), each uploaded as a separate numbered file. These hold raw data, code lists, or full result tables too large for the PDF. [salvatore-2026]
- **Source Data** -- per-figure underlying data files (e.g., Figure-3-a.xlsx, Figure-7.xlsx), uploaded as a combined Source Data file or individual files referenced in figure legends. [xu-2026]

These are separate uploads, not sections within the main manuscript PDF.

## Numbering scheme

Supplementary Figures use a continuous integer counter across the entire supplement: Supplementary Figure 1, Supplementary Fig. 2, ..., Supplementary Fig. 35. Abbreviated "Supplementary Fig." after first use. [xu-2026]

Supplementary Tables use a separate continuous integer counter: Supplementary Table 1, Supplementary Table 2, etc. [xu-2026, salvatore-2026]

Supplementary Data files use yet another counter: Supplementary Data 1, Supplementary Data 2, ..., Supplementary Data 10. Each is one downloadable file. [salvatore-2026]

Supplementary Notes, when present, are numbered: Supplementary Note 1, Supplementary Note 2. [salvatore-2026]

Figures in the main text use "Fig." (e.g., Fig. 1, Fig. 2a). Supplementary figures use "Supplementary Fig." or "Supplementary Figure" at first mention. There is no lettering hierarchy within the supplement; sub-panels follow the main-text convention (a, b, c). [xu-2026]

## How the main text references supplementary material

In running text, parenthetical or inline: "see Supplementary Figure 1", "Supplementary Fig. 21", "(Supplementary Data 2)", "(Figure S2)" or "(Figure S2a)". [xu-2026, salvatore-2026]

The salvatore-2026 paper uses the "Figure S1" / "Figure S2a" shorthand for Supplementary Information figures, and "Supplementary Data N" for machine-readable files. [salvatore-2026]

The xu-2026 paper consistently writes "Supplementary Figure N" or "Supplementary Fig. N" for the PDF-based figures. [xu-2026]

Both conventions are accepted; pick one and use it consistently.

## Triage rule: main text vs. supplementary

Content in the main text (typically 3,000-5,000 words for Articles):
- Core results figures and tables (up to ~10 display items in main text).
- Primary experimental comparisons, headline metrics, and key visualizations.

Content in the Supplementary Information PDF:
- Extended methodological detail (prompts, pipelines, data construction steps). [xu-2026]
- Additional experimental results that support but do not carry the main argument (e.g., department-level heatmaps beyond the primary ones, word cloud analyses, additional prompt templates). [xu-2026]
- Sensitivity analyses, robustness checks, alternative model specifications. [salvatore-2026]
- Supplementary figures for secondary comparisons (e.g., per-protocol vs. ITT breakdowns, time-to-event curves). [salvatore-2026]
- Accountability/verification analyses that deepen but do not replace main-text claims. [xu-2026]
- BMI trajectory analyses, coding artifact investigations, exclusion criterion details. [salvatore-2026]

Content in Supplementary Data (machine-readable files):
- Full PheWAS result tables across all comparisons. [salvatore-2026]
- Baseline characteristics for subgroups (e.g., semaglutide vs. non-semaglutide GLP-1 RA). [salvatore-2026]
- ICD code lists, drug concept ID lists, LOINC code lists, CCI condition mappings. [salvatore-2026]
- Source data underlying each main-text figure (one .xlsx per figure panel). [xu-2026]

Content in Source Data:
- Per-figure data files enabling reproduction of plots (e.g., Figure-3-a.xlsx, Figure-5-b.xlsx). Named to match the figure they support. [xu-2026]

## Typical content volume

Supplementary Information PDF: xu-2026 references Supplementary Figs. 1 through 35 plus multiple supplementary tables, indicating a substantial supplement (likely 20-40 pages). salvatore-2026 references Figures S1-S5 and Supplementary Data 1-10, with a more compact supplementary figure set but heavy use of Supplementary Data files. [xu-2026, salvatore-2026]

Supplementary Data: salvatore-2026 uses 10 numbered Supplementary Data files covering cohort characteristics, full PheWAS results across 6 comparisons, code lists, and covariate definitions. [salvatore-2026]

There is no strict page limit for the Supplementary Information PDF, but it should be organized and navigable. Nature Communications does not impose a hard cap on supplementary items.

## File structure

The supplementary material is NOT part of the main manuscript PDF. It is uploaded as separate files during submission:
- One Supplementary Information PDF (all supplementary figures, tables, notes).
- Individual Supplementary Data files (one per numbered item, typically .xlsx).
- Source Data files may be bundled or uploaded individually.

The main manuscript references these by number; the online article links to them as downloadable items. [xu-2026, salvatore-2026]

## Formatting within the Supplementary Information PDF

Each Supplementary Figure gets a bold title line ("Supplementary Figure N. Title.") followed by a legend paragraph, same style as main-text figure legends. [xu-2026]

Supplementary Tables follow the same convention: "Supplementary Table N. Title." with column headers and notes. [xu-2026, salvatore-2026]

Supplementary Notes, when used, carry section-style headers. [salvatore-2026]

## Key distinctions from main-text displays

- Main text: "Fig. 1", "Table 1". Supplementary: "Supplementary Fig. 1" or "Figure S1", "Supplementary Table 1".
- Main text figures appear inline. Supplementary figures appear only in the separate PDF.
- Supplementary Data items are downloadable files, not rendered in any PDF.
- Source Data items are linked from figure legends with explicit file names.
