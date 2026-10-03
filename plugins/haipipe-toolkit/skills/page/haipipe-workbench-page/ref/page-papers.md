Related papers
==============

The papers behind the Page Workbench: an outline planned before prose is drafted (Draft
Space), every value, citation and display bound to the result that supports it with its
provenance kept (Evidence Space), a document whose numbers are recomputed from its source
rather than pasted in, and one source published as a web page, LaTeX and Word (Delivery
Space). Guide › Related Paper shows this file.

Shape and check: `skills/0_utils/table-papers/SKILL.md`. Each row is one paper, standard
or documentation page. `group` is the part of the Page Workbench it supports; `role` is
`classic`, `review`, `evidence` or `practice` (a guideline, documentation or engineering
article); `key` is ★ for the ones that part rests on most; `doi` is the DOI, or the page of
a work that has none; `pdf` is empty (no full text is kept here). Kept to the most relevant
and most recent (JL 261003). Rows with a DOI were checked with `check_papers_table.py
--online` on 2026-10-03; the PROV-DM and Pandoc pages were fetched for their title, author
and date the same day. The Pandoc User's Guide carries no date of its own and writes
`n.d.`. Each `why here` line was judged from the abstract or the page only, not from the
full text; Kellogg 1988 has no abstract open to an automated fetch, so its line says only
what its title states.

| group | role | key | paper | venue | doi | why here | pdf |
| --- | --- | --- | --- | --- | --- | --- | --- |
| outline before drafting | classic | ★ | Flower & Hayes 1981 · A Cognitive Process Theory of Writing | College Composition and Communication | 10.2307/356600 | composing as a series of decisions and what guides them: the Draft Space settles the outline's decisions before prose is drafted from it |  |
| outline before drafting | evidence |  | Kellogg 1988 · Attentional overload and writing performance: Effects of rough draft and outline strategies | Journal of Experimental Psychology: Learning, Memory, and Cognition | 10.1037/0278-7393.14.2.355 | tests an outline strategy against a rough-draft strategy as ways to ease attentional overload while writing |  |
| claim–evidence provenance | practice | ★ | Moreau & Missier 2013 · PROV-DM: The PROV Data Model | W3C Recommendation | https://www.w3.org/TR/prov-dm/ | entities, activities and agents linked by derivation: each evidence item records the Run and result it was derived from |  |
| claim–evidence provenance | classic | ★ | Groth, Gibson & Velterop 2010 · The anatomy of a nanopublication | Information Services & Use | 10.3233/ISU-2010-0613 | a core statement published with its context and provenance: a VALUE, CITE or DISPLAY item travels with the result that supports it |  |
| literate documents | classic | ★ | Knuth 1984 · Literate Programming | The Computer Journal | 10.1093/comjnl/27.2.97 | a program and its documentation written as one WEB source: the Page and its evidence are kept and built together |  |
| literate documents | classic |  | Gentleman & Temple Lang 2007 · Statistical Analyses and Reproducible Research | Journal of Computational and Graphical Statistics | 10.1198/106186007X178663 | dynamic documents whose figures and tables are recomputed from a source document: values come from results, never typed in |  |
| single-source publishing | practice | ★ | MacFarlane n.d. · Pandoc User's Guide | pandoc.org | https://pandoc.org/MANUAL.html | one markup source converted to HTML, LaTeX and Word: the Delivery Space's three exports |  |
| single-source publishing | practice |  | Allaire, Teague, Xie et al. 2022 · Quarto | Zenodo | 10.5281/zenodo.5960048 | an open scientific publishing system built on Pandoc: the maintained publishing practice the Delivery Space's exports follow |  |
