# Nature Medicine -- Appendix / Supplementary Material Style

Source exemplars: bean-2026-natmed (Article, 7pp main text) and restrepo-2026-natmed (Brief Communication, 4pp main text).

## Three-tier system

Nature Medicine uses three distinct tiers of supporting material. The boundaries are strict.

| Tier | Peer-reviewed | Location | Max items | Numbering |
|---|---|---|---|---|
| Main text | Yes | In manuscript | No fixed cap | Fig. 1, Table 1 |
| Extended Data | Yes | Same PDF, after References | 10 items total (figs + tables combined) | Extended Data Fig. 1, Extended Data Table 1 |
| Supplementary Information | No (editorial check only) | Separate file, hosted online | No cap | Supplementary Fig. 1, Supplementary Table 1, Supplementary Note 1 |

Extended Data and Supplementary Information have independent numbering sequences. Figures and tables are numbered separately within each tier (both start at 1).

## Naming conventions

- Main text: `Fig. 1`, `Table 1` [bean-2026, restrepo-2026]
- Extended Data: `Extended Data Fig. 1`, `Extended Data Table 1` [bean-2026, restrepo-2026]
- Supplementary: `Supplementary Fig. 1`, `Supplementary Table 1`, `Supplementary Note 1` [bean-2026]
- Caption format uses a pipe separator: `Extended Data Table 1 | Title in sentence case.` [bean-2026, restrepo-2026]
- Panel labels within multi-panel figures: lowercase bold (**a**, **b**, **c**) is standard [bean-2026, restrepo-2026]

## How main text references each tier

Parenthetical inline references. Always spell out the tier prefix; never abbreviate "Extended Data" to "ED".

- `(Fig. 2a)` or `(Fig. 2a,b)` -- main-text figures [bean-2026, restrepo-2026]
- `(Extended Data Fig. 1a,b)` or `(Extended Data Table 1)` -- Extended Data [restrepo-2026]
- `(Supplementary Tables 5-8)` or `(Supplementary Fig. 6)` -- Supplementary Information [bean-2026]
- Ranges use an en-dash for consecutive items: `Supplementary Tables 5-8` [bean-2026]
- Cross-references from Extended Data captions back to Supplementary are allowed: "see the Supplementary Materials" [bean-2026]

## Content triage rules

**Main text** holds the core argument: study-design schematic, primary outcome figures, key comparison plots. Both exemplars place 2-4 main-text figures and zero main-text tables. Brief Communications allow at most 2 main-text display items [restrepo-2026]; Articles allow more [bean-2026].

**Extended Data** holds peer-reviewed supporting analyses that a reviewer must see but that would interrupt the main narrative. Typical content:
- Sub-group breakdowns and secondary analyses (accuracy by organ system, by theme) [restrepo-2026]
- Evaluation rubrics and instruments (clinician scoring rubric) [restrepo-2026]
- Representative qualitative examples (interaction transcripts) [bean-2026]
- Descriptive reference tables (scenario list, entry-point definitions, cost comparison) [bean-2026, restrepo-2026]
- Platform screenshots [restrepo-2026]
- Pairwise statistical comparison panels [restrepo-2026]

**Supplementary Information** holds everything else: full scenario texts, detailed demographics, hyperparameter tables, power analyses, inference cost breakdowns, question-filtering procedures, and exhaustive per-condition results [bean-2026]. The Supplementary file is a separate PDF uploaded alongside the manuscript. It is not paginated with the main article.

## Extended Data specifics

- Hard cap: 10 items total across Extended Data Figures and Extended Data Tables combined. Both exemplars stay within this limit (bean-2026: 1 fig + 6 tables = 7 items; restrepo-2026: 6 figs + 2 tables = 8 items).
- Each Extended Data item occupies one full page in the published PDF [bean-2026, restrepo-2026].
- Extended Data Figures can be complex multi-panel composites with detailed captions (up to ~150 words) [restrepo-2026].
- Extended Data Tables are typeset, not screenshots of spreadsheets [bean-2026, restrepo-2026].
- The main text must explicitly cite every Extended Data item at least once [bean-2026, restrepo-2026].

## Supplementary Information specifics

- Submitted as a separate file. The main article ends with a statement: "Supplementary information The online version contains supplementary material available at [DOI]." [bean-2026, restrepo-2026]
- Supplementary tables can use higher numbering that continues past the Extended Data tables (e.g., Supplementary Tables 5-10 when Extended Data Tables 1-4 exist) or start at 1 with a separate sequence. Bean-2026 uses Supplementary Tables starting above the Extended Data count, suggesting a single continuous sequence across tiers for tables [bean-2026].
- No cap on length or number of items.
- Content is checked editorially but not sent to peer reviewers as a mandatory read.

## Reporting Summary

Both exemplars include a Nature Portfolio Reporting Summary (3-page structured form) covering statistics, software, data availability, human-participants reporting, and field-specific study design. This is a required separate document, not part of Supplementary Information [bean-2026, restrepo-2026].

## Length norms

- Main text: Articles ~3,000-5,000 words; Brief Communications ~1,500-2,500 words [bean-2026 vs restrepo-2026].
- Extended Data: no word limit, but each item = one page. Captions can be substantial (100-200 words).
- Supplementary Information: no length limit. Typically 10-30 pages for data-heavy papers.

## Additional information block

Both exemplars end with a standardized block containing, in order: Online content, References, Reporting summary, Data availability, Code availability, Acknowledgements, Author contributions, Funding, Competing interests, Additional information (Extended data link, Supplementary information link, Correspondence, Peer review information, Reprints) [bean-2026, restrepo-2026].
