Related papers
==============

The papers behind the Page Workbench's methods (`page-method.md`): the plan before the
prose and the logic tree under it, sentences written where readers look (Draft), every
value bound to the Result it came from with its provenance (Evidence), one source built
as a web page, LaTeX and Word and checked by an agent that did not write it (Delivery).
Guide › Related Paper shows this file; each `group` is one method card, so a card lists
its own papers.

Shape and check: `skills/0_utils/table-papers/SKILL.md`. Each row is one paper, standard
or documentation page. `group` is the method card it supports; `role` is
`classic`, `review`, `evidence` or `practice` (a guideline, documentation or engineering
article); `key` is ★ for the ones that part rests on most; `doi` is the DOI, or the page of
a work that has none; `pdf` is empty (no full text is kept here). Kept to the most relevant
and most recent (JL 261003). Rows with a DOI were checked with `check_papers_table.py
--online` on 2026-10-03; the PROV-DM and Pandoc pages were fetched for their title, author
and date the same day. The Pandoc User's Guide carries no date of its own and writes
`n.d.`. Each `why here` line was judged from the abstract or the page only, not from the
full text; Kellogg 1988 has no abstract open to an automated fetch, so its line says only
what its title states.

Added 2026-10-03 with the method cards: Toulmin 2003 and Gopen & Swan 1990, copied from
`paper-papers.md`, and Panickssery et al. 2024 and Huang et al. 2023, copied from
`insight-papers.md`; their `why here` lines are rewritten for this workbench, and the
DOI rows were checked again with `--online` the same day.

| group | role | key | paper | venue | doi | why here | pdf |
| --- | --- | --- | --- | --- | --- | --- | --- |
| by outline first | classic | ★ | Flower & Hayes 1981 · A Cognitive Process Theory of Writing | College Composition and Communication | 10.2307/356600 | composing as a series of decisions and what guides them: the Draft Space settles the outline's decisions before prose is drafted from it |  |
| by outline first | evidence |  | Kellogg 1988 · Attentional overload and writing performance: Effects of rough draft and outline strategies | Journal of Experimental Psychology: Learning, Memory, and Cognition | 10.1037/0278-7393.14.2.355 | tests an outline strategy against a rough-draft strategy as ways to ease attentional overload while writing |  |
| by logic tree | classic | ★ | Toulmin 2003 · The Uses of Argument | Cambridge University Press | 10.1017/CBO9780511840005 | claim, grounds and warrant: the RoadMap Draw puts the Page claim on top, its reasons under it and its Bullets as leaves |  |
| by reader expectations | classic | ★ | Gopen & Swan 1990 · The Science of Scientific Writing | American Scientist | https://openalex.org/W1642165138 | readers look for the known at the start of a sentence and the new at its end: how each Draft sentence is written from its Bullet |  |
| by bound value | classic | ★ | Knuth 1984 · Literate Programming | The Computer Journal | 10.1093/comjnl/27.2.97 | a program and its documentation written as one WEB source: the Page and its evidence are kept and built together |  |
| by bound value | classic |  | Gentleman & Temple Lang 2007 · Statistical Analyses and Reproducible Research | Journal of Computational and Graphical Statistics | 10.1198/106186007X178663 | dynamic documents whose figures and tables are recomputed from a source document: values come from results, never typed in |  |
| by provenance | practice | ★ | Moreau & Missier 2013 · PROV-DM: The PROV Data Model | W3C Recommendation | https://www.w3.org/TR/prov-dm/ | entities, activities and agents linked by derivation: each evidence item records the Run and result it was derived from |  |
| by provenance | classic | ★ | Groth, Gibson & Velterop 2010 · The anatomy of a nanopublication | Information Services & Use | 10.3233/ISU-2010-0613 | a core statement published with its context and provenance: a VALUE, CITE or DISPLAY item travels with the result that supports it |  |
| by single source | practice | ★ | MacFarlane n.d. · Pandoc User's Guide | pandoc.org | https://pandoc.org/MANUAL.html | one markup source converted to HTML, LaTeX and Word: the Delivery Space's three exports |  |
| by single source | practice |  | Allaire, Teague, Xie et al. 2022 · Quarto | Zenodo | 10.5281/zenodo.5960048 | an open scientific publishing system built on Pandoc: the maintained publishing practice the Delivery Space's exports follow |  |
| by independent check | evidence | ★ | Panickssery, Bowman & Feng 2024 · LLM evaluators recognize and favor their own generations | arXiv | 10.48550/arXiv.2404.13076 | T4: a model evaluator scores its own outputs higher than others that human raters judge equal: the writer of a Page never checks it |  |
| by independent check | evidence |  | Huang, Chen, Mishra et al. 2023 · Large language models cannot self-correct reasoning yet | arXiv | 10.48550/arXiv.2310.01798 | T4: without outside feedback models struggle to correct their own reasoning and sometimes get worse |  |
