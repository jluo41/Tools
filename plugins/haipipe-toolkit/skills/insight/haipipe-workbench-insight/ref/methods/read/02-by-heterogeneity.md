By heterogeneity
================

One question-results reading method card. The Insight workbench shows it in the shared Guide › Method,
under Question-results reading methods; its papers are the rows of `../../insight-papers.md` whose
`group` is `by heterogeneity`. A claim names its source in brackets; "(ours)" marks the
workbench's own judgment.

family: Question-results reading
move: Ask whether the answer differs across partitions, and test the difference itself,
  not each partition's significance.
taxonomy: Inferential or causal, across groups [Leek 2015]; description across cuts, or
  causal inference when the effect is causal [Hernán 2019].
comes from: Gelman 2006, a difference in significance is not a significant difference;
  Kent 2020, predictive heterogeneity
reads: question · the partitions · the answer on each
returns: the answer per partition, the difference with its interval, and a verdict: pool,
  split or undetermined
test now: T7 one test of the difference, not two separate tests
test in use: T8 the split found again in new data


What the literature says
------------------------

rationale: A significant effect in one group and a non-significant one in another is not
  evidence that they differ; large changes in significance can match small,
  non-significant differences [Gelman 2006]. Effects can be examined one variable at
  a time, or by modelling the risk or the effect across all attributes at once [Kent
  2020].
context: Randomised trials [Rothwell 2005; Kent 2020]; judging clinical evidence [Sun
  2010]; personalised medicine and marketing [Wager 2018].
steps: 1. Name a few subgroups in advance, each with its reason [Rothwell 2005]. 2.
  Estimate the answer in each. 3. Test the difference between them [Gelman 2006]. 4.
  Judge its credibility with a checklist [Sun 2010]. 5. Pool, split, or say it is
  undetermined.
strengths: Risk modelling and effect modelling use all attributes at once instead of one
  at a time [Kent 2020]. Causal forests estimate heterogeneous effects with valid
  confidence intervals [Wager 2018].
limitations: Of 117 subgroup claims in trial abstracts, 46 had a significant interaction
  test, and all 5 later attempts to corroborate one found no subgroup effect
  [Wallach 2017]. Post-hoc subgroups should be treated with scepticism whatever
  their significance [Rothwell 2005].


Applied to AI
-------------

agent: The agent reads each partition's answer from its run and computes the contrast
  between them (ours).
steps: 1. Collect each partition's answer and interval. 2. Compute the difference and its
  interval [Gelman 2006]. 3. Return pool, split or undetermined.
returns: The contrast table and the verdict, on the cross page.
verify: A different agent checks that the verdict rests on the difference, not on one
  partition being significant and another not (T6).
risk: With many partitions, a split by chance is likely, and a post-hoc split is suspect
  [Rothwell 2005].
evidence on AI: No study tests an AI agent judging heterogeneity across partitions yet
  (ours).
skill: haipipe-insight its cross group's POOL, SPLIT or UNDETERMINED verdict
