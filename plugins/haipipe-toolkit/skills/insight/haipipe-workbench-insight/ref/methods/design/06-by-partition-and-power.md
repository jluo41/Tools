By partition and power
======================

One design method card. The Insight workbench shows it in Scope › Methods › Design
methods; its papers are the rows of `../../insight-papers.md` whose `group` is
`by partition and power`. A claim names its source in brackets; "(ours)" marks the
workbench's own judgment.

family: From the population: where the question is asked and how strong the answer
  must be
move: Before any outcome is seen, declare the partitions (the cuts of the data a
  question is asked on), why the question keeps its meaning in each, and the smallest
  effect worth acting on; then compute each partition's minimum detectable effect.
taxonomy: Information and Knowledge; a difference between partitions is effect
  modification [Schandelmaier 2020].
comes from: Sun 2010, subgroup credibility; Button 2013, power failure
reads: ask · partitions · the n of each
returns: the partitions, each with its meaning; the power rule (smallest effect worth
  acting on, alpha, target power) and each partition's minimum detectable effect; one
  cross-partition heterogeneity question
test now: T3 powered · T2 agreed
test in use: T4 reproduced


What the literature says
------------------------

rationale: A subgroup effect is more believable when it was specified first with its
  direction, is one of few tested, is supported by a test of interaction and is
  consistent across studies [Sun 2010]. Low power lowers not only the chance of
  finding a true effect but also the chance that a significant result is true, and
  it inflates effect sizes [Button 2013]. The difference between a significant and a
  non-significant result is not itself significant [Gelman 2006].
context: Randomised trials and meta-analyses [Schandelmaier 2020]; neuroscience [Button
  2013]; the behavioural sciences [Cohen 1992].
steps: 1. Name each partition and why the question keeps or loses its meaning in it.
  2. Set the smallest effect worth acting on, alpha and target power [Lakens 2022].
  3. Compute the minimum detectable effect at each partition's n [Cohen 1992]. 4.
  Answer only where it is at most the smallest effect worth acting on. 5. Ask whether
  partitions differ as one question, tested by interaction [Schandelmaier 2020].
strengths: ICEMAN rates the credibility of a claimed effect modification with 5 core
  questions for trials and 8 for meta-analyses [Schandelmaier 2020].
limitations: Of 64 trials claiming subgroup effects, 84% of the claims met four or
  fewer of 10 credibility criteria [Sun 2012]. Of 117 subgroup claims in trial
  abstracts, 39% had a significant interaction test, and all 5 later tested again
  failed to corroborate [Wallach 2017].


Applied to AI
-------------

agent: The drafter declares the partitions and the power rule from the ask and the
  partition sizes, before any outcome column is read.
steps: 1. List the partitions and what the question means in each. 2. Write the power
  rule. 3. Compute each minimum detectable effect from n alone. 4. Mark a partition
  underpowered where it is too large, and refuse its answer there. 5. Write the
  heterogeneity question that compares the partitions directly.
returns: A power table, one row per partition, and the cross-partition question.
verify: A second agent recomputes each minimum detectable effect from n and the rule
  (T3) and checks that no claim compares p-values across partitions [Gelman 2006].
risk: An agent that sees the outcomes first can choose the cuts that show an effect,
  the subgroup problem in another form (ours).
evidence on ai: No study tests an AI declaring partitions or a power rule yet (ours).
skill: haipipe-insight-question
