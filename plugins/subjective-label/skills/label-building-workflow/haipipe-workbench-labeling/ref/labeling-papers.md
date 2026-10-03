Related papers
==============

The papers behind the Labeling Workbench: one subjective-labeling job whose label meaning a
human decides. They support four parts of it: what a label means and how a written
guideline carries that meaning from round to round (Labeling: gate G0 and the guideline),
weak LLM executors that pre-label and are checked against a human rather than taken as
gold (Labeling and Quality), a random first batch followed by selected disagreement and
boundary batches (the sampler), and an evaluation that cannot leak (Data: items split by
source group, a sealed test set; Quality: executors scored against locked human gold).
Guide › Related Paper shows this file.

Shape and check: `skills/0_utils/table-papers/SKILL.md`. Each row is one paper, book or
article. `group` is the part of the Labeling Workbench it supports (`a; b` when it serves
two; it shows under the first); `role` is `classic`, `review`, `evidence` or `practice` (a
guideline, documentation or engineering article); `key` is ★ for the ones that part rests
on most; `doi` is the DOI, or the page of a work that has none; `pdf` is empty (no full
text is kept here). Kept to the most relevant and most recent. Rows were
checked with `check_papers_table.py --online` on 2026-10-03. Pustejovsky & Stubbs 2012 is
an O'Reilly book with no DOI, and the publisher's page refused an automated fetch that
day, so its row points to its OpenAlex record, which was fetched for title, authors, year
and description; Open Library lists its O'Reilly Media editions (2012). Settles 2012 is
cited by the DOI of its Springer reissue in the Synthesis Lectures series (first published
by Morgan & Claypool, 2012). Each `why here` line was judged from the abstract or the
publisher's page only, not from the full text.

| group | role | key | paper | venue | doi | why here | pdf |
| --- | --- | --- | --- | --- | --- | --- | --- |
| label meaning and guidelines | classic | ★ | Pustejovsky & Stubbs 2012 · Natural Language Annotation for Machine Learning | O'Reilly Media | https://openalex.org/W1594247117 | the annotation cycle from task and specification through guidelines to a gold standard corpus: the Labeling Space's confirmed label meaning (G0) and its guideline revised round by round |  |
| label meaning and guidelines | review | ★ | Plank 2022 · The "Problem" of Human Label Variation: On Ground Truth in Data, Modeling and Evaluation | Proceedings of EMNLP 2022 | 10.18653/v1/2022.emnlp-main.731 | human label variation as genuine disagreement and subjectivity, not noise, across data, modeling and evaluation: why disagreement stays visible and a human decides what a subjective label means |  |
| label meaning and guidelines; evaluation without leakage | review |  | Artstein & Poesio 2008 · Inter-Coder Agreement for Computational Linguistics | Computational Linguistics | 10.1162/coli.07-034-R2 | agreement coefficients (Krippendorff's alpha, Scott's pi, Cohen's kappa) and their assumptions: how agreement between executors and human gold is measured and read |  |
| human-AI labeling and LLM annotators | evidence | ★ | Gilardi, Alizadeh & Kubli 2023 · ChatGPT outperforms crowd workers for text-annotation tasks | Proceedings of the National Academy of Sciences | 10.1073/pnas.2305016120 | zero-shot ChatGPT beat crowd workers on relevance, stance, topic and frame annotation at a fraction of the cost: why LLM executors pre-label each batch |  |
| human-AI labeling and LLM annotators | evidence | ★ | Wang, Kim, Rahman et al. 2024 · Human-LLM Collaborative Annotation Through Effective Verification of LLM Labels | Proceedings of the CHI Conference on Human Factors in Computing Systems | 10.1145/3613904.3641960 | LLMs label and explain, a verifier flags doubtful labels, and humans re-annotate those: LLM labels are checked by a human rather than taken as gold |  |
| human-AI labeling and LLM annotators | review |  | Tan, Li, Wang et al. 2024 · Large Language Models for Data Annotation and Synthesis: A Survey | Proceedings of EMNLP 2024 | 10.18653/v1/2024.emnlp-main.54 | how LLM annotations are generated, assessed and used, and their limits: where the weak executors and their evaluation sit in the wider field |  |
| sampling and active selection | review | ★ | Settles 2012 · Active Learning | Synthesis Lectures on Artificial Intelligence and Machine Learning | 10.1007/978-3-031-01560-1 | the scenarios and query-selection algorithms of active learning: the sampler's disagreement- and boundary-focused batches after a random first round |  |
| sampling and active selection | evidence |  | Ein-Dor, Halfon, Gera et al. 2020 · Active Learning for BERT: An Empirical Study | Proceedings of EMNLP 2020 | 10.18653/v1/2020.emnlp-main.638 | with a small budget and skewed classes, active learning lifts BERT classifiers, most when the starting set is biased: selected later rounds reach rare label values |  |
| evaluation without leakage | review | ★ | Kapoor & Narayanan 2023 · Leakage and the reproducibility crisis in machine-learning-based science | Patterns | 10.1016/j.patter.2023.100804 | a taxonomy of eight types of leakage found across 17 fields, with model info sheets to test for each: why a source group stays in one split and the test set is sealed before executors are compared |  |
| evaluation without leakage | evidence |  | Søgaard, Ebert, Bastings et al. 2021 · We Need To Talk About Random Splits | Proceedings of EACL 2021 | 10.18653/v1/2021.eacl-main.156 | random splits, like standard splits, overestimate performance; independent test sets or biased splits are more realistic: items are split by source group, not at random |  |
