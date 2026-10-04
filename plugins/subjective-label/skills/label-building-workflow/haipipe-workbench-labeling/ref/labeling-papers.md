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
article. `group` is the method card it supports, as named in `labeling-method.md` (`a; b` when
it serves several; it shows under the first, and Guide › Method lists it on every card it serves); `role` is `classic`, `review`, `evidence` or `practice` (a
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
| by unit recipe; by discussion then confirm; by written guideline | classic | ★ | Pustejovsky & Stubbs 2012 · Natural Language Annotation for Machine Learning | O'Reilly Media | https://openalex.org/W1594247117 | the annotation cycle from task and specification through guidelines to a gold standard corpus: the Labeling Space's confirmed label meaning (G0) and its guideline revised round by round |  |
| by discussion then confirm; by in-between regions | review | ★ | Plank 2022 · The "Problem" of Human Label Variation: On Ground Truth in Data, Modeling and Evaluation | Proceedings of EMNLP 2022 | 10.18653/v1/2022.emnlp-main.731 | human label variation as genuine disagreement and subjectivity, not noise, across data, modeling and evaluation: why disagreement stays visible and a human decides what a subjective label means |  |
| by audit sample; by written guideline | review | ★ | Artstein & Poesio 2008 · Inter-Coder Agreement for Computational Linguistics | Computational Linguistics | 10.1162/coli.07-034-R2 | agreement coefficients (Krippendorff's alpha, Scott's pi, Cohen's kappa) and their assumptions: how agreement between executors and human gold is measured and read |  |
| by weak-model committee | evidence | ★ | Gilardi, Alizadeh & Kubli 2023 · ChatGPT outperforms crowd workers for text-annotation tasks | Proceedings of the National Academy of Sciences | 10.1073/pnas.2305016120 | zero-shot ChatGPT beat crowd workers on relevance, stance, topic and frame annotation at a fraction of the cost: why LLM executors pre-label each batch |  |
| by risk routing; by weak-model committee | evidence | ★ | Wang, Kim, Rahman et al. 2024 · Human-LLM Collaborative Annotation Through Effective Verification of LLM Labels | Proceedings of the CHI Conference on Human Factors in Computing Systems | 10.1145/3613904.3641960 | LLMs label and explain, a verifier flags doubtful labels, and humans re-annotate those: LLM labels are checked by a human rather than taken as gold |  |
| by weak-model committee | review |  | Tan, Li, Wang et al. 2024 · Large Language Models for Data Annotation and Synthesis: A Survey | Proceedings of EMNLP 2024 | 10.18653/v1/2024.emnlp-main.54 | how LLM annotations are generated, assessed and used, and their limits: where the weak executors and their evaluation sit in the wider field |  |
| by disagreement draw; by random first round | review | ★ | Settles 2012 · Active Learning | Synthesis Lectures on Artificial Intelligence and Machine Learning | 10.1007/978-3-031-01560-1 | the scenarios and query-selection algorithms of active learning: the sampler's disagreement- and boundary-focused batches after a random first round |  |
| by disagreement draw | evidence |  | Ein-Dor, Halfon, Gera et al. 2020 · Active Learning for BERT: An Empirical Study | Proceedings of EMNLP 2020 | 10.18653/v1/2020.emnlp-main.638 | with a small budget and skewed classes, active learning lifts BERT classifiers, most when the starting set is biased: selected later rounds reach rare label values |  |
| by sealed test; by group-held test | review | ★ | Kapoor & Narayanan 2023 · Leakage and the reproducibility crisis in machine-learning-based science | Patterns | 10.1016/j.patter.2023.100804 | a taxonomy of eight types of leakage found across 17 fields, with model info sheets to test for each: why a source group stays in one split and the test set is sealed before executors are compared |  |
| by group-held test; by sealed test | evidence | ★ | Søgaard, Ebert, Bastings et al. 2021 · We Need To Talk About Random Splits | Proceedings of EACL 2021 | 10.18653/v1/2021.eacl-main.156 | random splits, like standard splits, overestimate performance; independent test sets or biased splits are more realistic: items are split by source group, not at random |  |
| by in-between regions | review | ★ | Aroyo & Welty 2015 · Truth Is a Lie: Crowd Truth and the Seven Myths of Human Annotation | AI Magazine | 10.1609/aimag.v36i1.2564 | disagreement among annotators as a signal of real ambiguity, not noise to remove: why an item may sit between two labels and why those items become rules |  |
| by blind first judgment | classic | ★ | Tversky & Kahneman 1974 · Judgment under Uncertainty: Heuristics and Biases | Science | 10.1126/science.185.4157.1124 | anchoring: an initial value shown before a judgment pulls the judgment toward it: why the person's first label locks before any model answer shows |  |
| by independent scorer | evidence | ★ | Panickssery, Bowman & Feng 2024 · LLM evaluators recognize and favor their own generations | arXiv | 10.48550/arXiv.2404.13076 | a model evaluator scores its own outputs higher than others that human raters judge equal: why the scorer of the held-back test made nothing it scores |  |
