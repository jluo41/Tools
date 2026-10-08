By protocol reuse
=================

One question-asking method card (`haipipe-question-asking`). The Insight workbench shows it in
the shared Guide › Method, step 1; its papers are the rows of that workbench's
`servers/workbench-insight/related/papers.md` whose `group` is `by protocol reuse`. A claim names its source in brackets; "(ours)" marks the
workbench's own judgment.

family: Question-asking
move: Write the questions and their code once, as a Prototype board, then run the same
  protocol unchanged on each dataset and compare the answers.
taxonomy: Any level; a test of whether an answer holds beyond the dataset it came from
  (ours).
comes from: Hripcsak 2015, one network, one data model; Schuemie 2020, prespecified
  evidence across a network of databases
reads: the Prototype board · a new dataset's extract
returns: the same questions answered on the new dataset, beside the Prototype's
  answers, and a between-dataset heterogeneity summary
test now: T1 specified
test in use: T8 reproduced


What the literature says
------------------------

rationale: An open network of databases mapped to one common data model lets one
  analysis run at every site [Hripcsak 2015]. Answering many questions at once with
  a prespecified, systematic approach guards against publication bias and P hacking,
  and running it in a network of databases with shared open code, without sharing
  patient-level data, shows whether results are consistent [Schuemie 2020].
context: Observational health data in an international network of 11 data sources
  [Hripcsak 2016]; comparative effectiveness of drug classes [Suchard 2019];
  replications in psychology across 125 samples in 36 countries [Klein 2018].
steps: 1. Map each dataset to one data model. 2. Write the protocol and its code once.
  3. Run it unchanged on each dataset. 4. Report each answer, then their
  heterogeneity [Schuemie 2020].
strengths: One network study produced 22,000 calibrated hazard ratios comparing every
  drug class and outcome across databases [Suchard 2019]. With protocols peer
  reviewed in advance, 28 findings were each replicated in about half of 125
  samples [Klein 2018].
limitations: With the design held fixed, estimates across 10 databases ran from a
  significant decrease to a significant increase in risk for 21% of drug-outcome
  pairs in a cohort design [Madigan 2013]. Treatment pathways moved toward
  consistency, but significant heterogeneity remained among sources [Hripcsak 2016].


Applied to AI
-------------

agent: The agent copies the Prototype board's questions, specs and code to a new
  dataset's board and changes nothing but the extract.
steps: 1. Check that the new extract has every column the protocol reads. 2. Run each
  question's code unchanged. 3. Report each answer beside the Prototype's. 4. Ask the
  between-dataset heterogeneity question.
returns: The answers per dataset and their heterogeneity, never a pooled answer alone.
verify: A second agent checks that the specs and code are identical to the
  Prototype's (T1) and that the datasets are compared by heterogeneity, not by which
  ones came out significant (T8).
risk: A protocol quietly adapted to fit a new dataset is a new study under the old
  name (ours).
evidence on ai: A language model pipeline produced shareable analysis code for a
  network's standard study framework from text descriptions [Kim 2026]. No study
  tests an AI reusing one protocol across datasets (ours).
skill: haipipe-insight-by-protocol-reuse (proposed)
