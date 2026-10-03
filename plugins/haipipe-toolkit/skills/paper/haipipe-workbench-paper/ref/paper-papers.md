Related papers
==============

The papers behind the Paper Workbench: a paper built from research questions down to
claims and the warrant each claim needs (Story), sections written in the order a reader
expects (Sections), evidence fixed before the claim is written and kept reproducible (the
Story's roadmap and each section's release gate), and reviewer rounds answered point by
point (Delivery). Guide › Related Paper shows this file.

Shape and check: `skills/0_utils/table-papers/SKILL.md`. Each row is one paper, book or
article. `group` is the part of the Paper Workbench it supports; `role` is `classic`,
`review`, `evidence` or `practice` (a guideline, documentation or engineering article);
`key` is ★ for the ones that part rests on most; `doi` is the DOI, or the page of a work
that has none; `pdf` is empty (no full text is kept here). Kept to the most relevant and
most recent (JL 261003). Rows with a DOI were checked with `check_papers_table.py --online`
on 2026-10-03. Gopen & Swan 1990 has no DOI, and its publisher and JSTOR pages refused an
automated fetch that day, so its row points to its OpenAlex record, which was fetched for
title, authors, year and issue (American Scientist 78(6):550-558). Toulmin is cited in the
2003 updated edition, the one with a DOI (first published 1958). Each `why here` line was
judged from the abstract or the publisher's page only, not from the full text.

| group | role | key | paper | venue | doi | why here | pdf |
| --- | --- | --- | --- | --- | --- | --- | --- |
| questions and claims | classic | ★ | Toulmin 2003 · The Uses of Argument | Cambridge University Press | 10.1017/CBO9780511840005 | how an assertion is rationally justified by the norms of its field: each Story claim names the evidence and reasoning that justify it |  |
| questions and claims | practice | ★ | Mensh & Kording 2017 · Ten simple rules for structuring papers | PLOS Computational Biology | 10.1371/journal.pcbi.1005619 | rules for communicating a paper's main idea, built on how readers consume it: the Story's question → claim → contribution spine and its Section Narrative |  |
| reader-ordered writing | classic | ★ | Gopen & Swan 1990 · The Science of Scientific Writing | American Scientist | https://openalex.org/W1642165138 | rhetorical principles that make complex science clear without oversimplifying it: how a Section turns its bound evidence into prose |  |
| evidence before claims | review | ★ | Chambers & Tzavella 2022 · The past, present and future of Registered Reports | Nature Human Behaviour | 10.1038/s41562-021-01193-7 | questions and methods are reviewed before results exist: the Story fixes what evidence each claim needs before the Task work runs |  |
| evidence before claims | practice | ★ | Sandve, Nekrutenko, Taylor et al. 2013 · Ten Simple Rules for Reproducible Computational Research | PLoS Computational Biology | 10.1371/journal.pcbi.1003285 | reproducibility as the minimum standard for a claim, with a protocol clear enough to repeat the analysis: each evidence item a Section binds comes from a recorded Run |  |
| review and response | practice | ★ | Noble 2017 · Ten simple rules for writing a response to reviewers | PLOS Computational Biology | 10.1371/journal.pcbi.1005730 | a response that quotes the reviews and summarizes each change made for them: the Delivery Space's reviewer rounds and responses |  |
