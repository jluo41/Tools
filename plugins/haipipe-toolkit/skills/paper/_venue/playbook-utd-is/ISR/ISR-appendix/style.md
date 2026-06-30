# ISR Online Appendix Style Guide

Distilled from two ISR exemplars. Quote the SHAPE, not the content.

## Naming convention

- ISR uses "Online Appendix" (two words, capitalized) as the standard label [mousavi-2026, wang-2026].
- Each appendix section is lettered: Online Appendix A, Online Appendix B, ... Online Appendix O [mousavi-2026 uses A-O; wang-2026 uses A-G].
- The front-page metadata line reads: "Supplemental Material: The online appendix and supplemental material are available at [DOI URL]." [mousavi-2026] or "Supplemental Material: The online appendices are available at [DOI URL]." [wang-2026].
- SHAPE: `Supplemental Material: The online appendix/appendices [and supplemental material] are available at [DOI].`

## Separate file, not same document

- The Online Appendix is a separate PDF uploaded as supplemental material, not part of the main manuscript [mousavi-2026, wang-2026].
- The main text is self-contained at the journal's page limit. All appendix material is hosted externally at the paper's DOI.
- Authors compile one consolidated Online Appendix PDF (not multiple files per section).

## Triage rule: what goes in appendix vs main text

Main text retains:
- Core tables that directly test hypotheses (main regression results, key mechanism tests) [wang-2026 Tables 1-10; mousavi-2026 Tables 1-10].
- The primary framework figure [mousavi-2026 Figure 1].
- Summary statistics table [wang-2026 Table 1; mousavi-2026 Table 5].
- Central theoretical arguments and all hypothesis statements.

Online Appendix absorbs:
- Matching/identification procedure details (PSM balance tables, matching outcomes) [wang-2026 Appendix A: Tables A2, A3].
- Extended robustness tables (alternative measures, stratified analyses, alternative samples, time-weighting schemes) [wang-2026 Appendix B: Tables B1-B7].
- Detailed methodology for ancillary procedures (mediation construction, variable construction, classification models) [wang-2026 Appendices C-G].
- Implementation details for each method paradigm or case study [mousavi-2026 Appendices A-E].
- Prompting strategy comparisons and hyperparameter details [mousavi-2026 Appendix F].
- Instrument validity checks and additional psychometric analyses [mousavi-2026 Appendix H].
- Supplementary theoretical elaborations (detailed literature surveys, theoretical construct definitions) [mousavi-2026 Appendices K, L, M].
- Additional data set analyses and robustness checks [mousavi-2026 Appendices N, O].
- Attention weight methodology or other computational details [mousavi-2026 Appendix J].
- Practical tools for readers (e.g., a "researcher-friendly cookbook") [mousavi-2026].

Rule of thumb: if a result directly tests a numbered hypothesis, it belongs in the main text. If it supports, elaborates, or provides robustness for a main-text finding, it belongs in the Online Appendix.

## Numbering and lettering scheme

- Appendix sections: uppercase letters (A, B, C, ...) [mousavi-2026, wang-2026].
- Tables inside the appendix: prefix = appendix letter + arabic number. Examples: Table A2, Table A3 [wang-2026]; Table B1, Table B2, Table B3a, Table B3b [wang-2026].
- Sub-lettering (a, b) is used for panel variants of the same table [wang-2026: Table B3a, Table B3b].
- Figures inside the appendix follow the same convention (Figure A1, Figure B1, etc.) when present.
- Main-text tables and figures use simple sequential numbering (Table 1, Table 2, ...; Figure 1, Figure 2, ...) with no prefix [mousavi-2026, wang-2026].

## How the main text references appendix material

- Pattern 1 -- parenthetical direction: "(details are in Online Appendices A, B, and C)" [mousavi-2026].
- Pattern 2 -- inline with "see": "see Online Appendix K for detailed analysis" [mousavi-2026].
- Pattern 3 -- specific table citation: "Tables A2 and A3 of Online Appendix A" [wang-2026]; "Table B3a and Table B3b in Online Appendix B" [wang-2026].
- Pattern 4 -- clause-level reference: "A robustness check ... is detailed in Online Appendix N" [mousavi-2026].
- Pattern 5 -- parenthetical with table: "(reported in Table B2 in Online Appendix B)" [wang-2026].
- SHAPE: `[see / details in / reported in] Online Appendix [LETTER] [for ...].` When citing a specific exhibit, include both the table/figure number and the appendix letter.

## Typical content and organization

A typical ISR Online Appendix contains 5-15 lettered sections. Content clusters into these categories:

1. Identification/matching details -- balance tables, matching procedures, first-stage results [wang-2026 Appendix A].
2. Extended results -- robustness tables, alternative specifications, stratified/subsample analyses, falsification tests [wang-2026 Appendix B; mousavi-2026 Appendices D, E, N, O].
3. Variable/measure construction -- how key variables were operationalized, NLP pipelines, classification models [wang-2026 Appendices D-G; mousavi-2026 Appendices A-C].
4. Methodology elaboration -- mediation framework, instrument validity, attention-weight analysis [wang-2026 Appendix C; mousavi-2026 Appendices H, J].
5. Theoretical supplements -- literature surveys, detailed construct definitions, theoretical proofs [mousavi-2026 Appendices K, L, M].
6. Practical supplements -- implementation guides, cookbooks, replication material [mousavi-2026].

Ordering convention: procedural/data appendices first (A, B), then robustness and extended results, then theoretical supplements last.

## Length norms

- No hard page limit is stated for the Online Appendix. Both exemplars use extensive appendices.
- [mousavi-2026] uses 15 appendix sections (A through O), suggesting substantial supplementary material (likely 20-40 pages).
- [wang-2026] uses 7 appendix sections (A through G) with multiple multi-page tables in section B alone (Tables B1-B7, plus B3a, B3b variants).
- The Online Appendix can exceed the main text in length. ISR reviewers expect thorough supplementary documentation.
- Each appendix section is typically 1-5 pages, combining prose explanation with tables or figures.

## Endnotes (distinct from appendix)

- Both papers use numbered endnotes for brief clarifications that would interrupt prose flow but do not warrant a full appendix section [mousavi-2026: 7 endnotes; wang-2026: 11 endnotes].
- Endnotes appear at the end of the main manuscript, before References.
- Endnotes handle definitional clarifications, calculation formulas, brief methodological notes, and data-source details.
- SHAPE: If the aside is one paragraph or less, use an endnote. If it requires a table, figure, or multi-paragraph explanation, use an Online Appendix section.
