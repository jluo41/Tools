Related papers
==============

The papers behind the Task Workbench: a Question card that states its question, hypothesis
and acceptance test before any work runs (Logic); a Block → Job → Task → Run tree whose
every Run is a shell ticket that runs one config and writes a Result folder with its
runtime receipt (Task Work, Runs panel); and a Report that answers the question from those
exact Results, with Evidence, Limits and Next. Guide › Related Paper shows this file on
the Task Workbench.

Shape and check: `skills/0_utils/table-papers/SKILL.md`. Each row is one paper or article.
`group` is the part of the Task Workbench it supports:

- `questions first`: ask the question, state the hypothesis and the acceptance test
  before running anything (the Logic cell).
- `runs and receipts`: a computational Run that can be rerun, and a record of what made
  each Result (the Run ticket, the Result folder and its runtime receipt).
- `analysis pipelines`: tracking many experiments across a pipeline without hidden debt
  (the Block → Job → Task → Run tree and the Runs panel).
- `reports from results`: writing the answer from exact Results, and where notebook-style
  analysis goes wrong (the Report cell).

`role` is `classic`, `review`, `evidence` or `practice` (a guideline, documentation or
engineering article); `key` is ★ for the ones that part rests on most; `doi` is the DOI,
or the page of a work that has none; `pdf` is empty (no full text is kept here). Kept to
the most relevant and most recent, general rather than about one dataset. Rows with a DOI
were checked with `check_papers_table.py --online` on 2026-10-03; each page without a DOI
was fetched for its title, author and date the same day. The findings in `why here` were
read from the abstracts only.

| group | role | key | paper | venue | doi | why here | pdf |
| --- | --- | --- | --- | --- | --- | --- | --- |
| questions first | classic | ★ | Leek & Peng 2015 · What is the question? | Science | 10.1126/science.aaa6146 | the question's type sets which analysis can answer it: the Logic cell names it first |  |
| questions first | evidence | ★ | Nosek, Ebersole, DeHaven & Mellor 2018 · The preregistration revolution | PNAS | 10.1073/pnas.1708274114 | fixing hypothesis and analysis before seeing results separates confirmation from exploration: Logic's hypothesis and acceptance test |  |
| questions first | review |  | Chambers & Tzavella 2021 · The past, present and future of Registered Reports | Nature Human Behaviour | 10.1038/s41562-021-01193-7 | judging the question and method before results: a Question is accepted on its Logic, not its outcome |  |
| runs and receipts | practice | ★ | Sandve, Nekrutenko, Taylor & Hovig 2013 · Ten Simple Rules for Reproducible Computational Research | PLOS Computational Biology | 10.1371/journal.pcbi.1003285 | record how every result was produced and keep the exact scripts: one Run ticket per config, rerun not hand-edited |  |
| runs and receipts | classic |  | Moreau & Missier 2013 · PROV-DM: The PROV Data Model | W3C Recommendation | https://www.w3.org/TR/prov-dm/ | entity, activity and agent: a Result folder, the Run that made it, and who ran it in the runtime receipt |  |
| runs and receipts | review |  | Pimentel, Freire, Murta & Braganholo 2019 · A Survey on Collecting, Managing, and Analyzing Provenance from Scripts | ACM Computing Surveys | 10.1145/3311955 | capturing provenance from scripts as they run: what a Run's runtime receipt keeps |  |
| runs and receipts | classic |  | Wilkinson, Dumontier, Aalbersberg et al. 2016 · The FAIR Guiding Principles for scientific data management and stewardship | Scientific Data | 10.1038/sdata.2016.18 | findable, accessible, reusable outputs: Results kept at stable paths with metadata a Report can cite |  |
| analysis pipelines | classic | ★ | Sculley, Holt, Golovin et al. 2015 · Hidden Technical Debt in Machine Learning Systems | NeurIPS 2015 | https://papers.nips.cc/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html | glue code, pipeline jungles and untracked configs: why work is held as declared Jobs, Tasks and Runs |  |
| analysis pipelines | practice |  | Zaharia, Chen, Davidson et al. 2018 · Accelerating the Machine Learning Lifecycle with MLflow | IEEE Data Engineering Bulletin | https://sites.computer.org/debull/A18dec/p39.pdf | tracking each experiment's params, code and outputs: the Runs panel lists Runs by type with their Results |  |
| analysis pipelines | evidence |  | Shankar, Garcia, Hellerstein & Parameswaran 2022 · Operationalizing Machine Learning: An Interview Study | arXiv | 10.48550/arXiv.2209.09125 | practitioners rely on experiment velocity, validation and versioning: the Task Work tree keeps every Run in view |  |
| reports from results | evidence | ★ | Kery, Radensky, Arya, John & Myers 2018 · The Story in the Notebook: Exploratory Data Science using a Literate Programming Tool | CHI 2018 | 10.1145/3173574.3173748 | exploratory notebooks are messy and lose their story: the Report is written apart from the Runs that feed it |  |
| reports from results | evidence | ★ | Pimentel, Murta, Braganholo & Freire 2019 · A Large-scale Study about Quality and Reproducibility of Jupyter Notebooks | MSR 2019 | 10.1109/MSR.2019.00077 | most public notebooks do not rerun to the same results: a Report cites Results from tickets, not notebook state |  |
| reports from results | evidence |  | Rule, Tabard & Hollan 2018 · Exploration and Explanation in Computational Notebooks | CHI 2018 | 10.1145/3173574.3173606 | notebooks rarely explain their analysis: the Report states Evidence, Limits and Next in prose |  |
| reports from results | practice |  | Wilson, Bryan, Cranston et al. 2017 · Good enough practices in scientific computing | PLOS Computational Biology | 10.1371/journal.pcbi.1005510 | keep raw data, code and results apart and write down what was done: Results stay generated, Reports cite them |  |
