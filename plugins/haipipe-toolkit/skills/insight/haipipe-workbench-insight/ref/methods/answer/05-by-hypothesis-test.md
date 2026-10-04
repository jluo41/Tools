By hypothesis test
==================

One question-answering method card. The Insight workbench shows it in the shared Guide › Method,
under Question-answering methods; its papers are the rows of `../../insight-papers.md` whose
`group` is `by hypothesis test`. A claim names its source in brackets; "(ours)" marks
the workbench's own judgment.

family: Question-answering
move: State the hypothesis, its test, its alpha (the false-positive rate allowed) and its
  power before the run, then report the test's result whatever it is.
taxonomy: Inferential [Leek 2015]; description or causal inference, by what the
  hypothesis is about [Hernán 2019].
comes from: Neyman 1933, most efficient tests; Wagenmakers 2012, purely confirmatory
  research
reads: question · the stated hypothesis · its test, alpha and power
returns: the estimate, its interval, its p-value against the stated alpha, and the number
  of tests run on the question
test now: T4 the run is the test the spec names · T5 the sentence says what the test says
test in use: T8 the same test on another partition or time window


What the literature says
------------------------

rationale: A test fixes its error rate against a stated alternative [Neyman 1933]. Only
  analyses stated in advance are confirmatory, and only for them are the usual
  tests valid [Wagenmakers 2012].
context: Statistics [Neyman 1933]; psychology [Wagenmakers 2012; Scheel 2021];
  neuroscience [Button 2013].
steps: 1. State the hypothesis and its alternative. 2. Choose the test, the alpha and the
  power it needs [Button 2013]. 3. With several tests, control the false discovery
  rate [Benjamini 1995]. 4. Run it once, and report the estimate and its interval
  beside the p-value [Wasserstein 2016].
strengths: When the analysis is fixed before the results are known, positive results are
  rarer: 96% of first hypotheses were supported in standard reports against 44% in
  registered reports [Scheel 2021].
limitations: A p-value does not say how large an effect is or how likely the hypothesis
  is [Wasserstein 2016]. Low power lowers the chance that a significant result is
  true and inflates the effect size [Button 2013]. Writing the plan before the data
  is read is a question-asking method (by analysis plan); this card runs the plan (ours).


Applied to AI
-------------

agent: The agent reads the stated test from the work spec and runs it as written; it may
  not change the test after it sees the data (ours).
steps: 1. Read the hypothesis, test, alpha and power from the spec. 2. Run the test. 3.
  Report the estimate, interval and p-value. 4. Note any deviation from the spec.
returns: The test's result, the number of tests on the question, and any deviation from
  the spec.
verify: A different agent checks that the run is the test the spec names (T4) and that
  each sentence says what the test says (T5, T6).
risk: Choosing a test, a cut or an exclusion after seeing the data makes a false
  hypothesis look supported [Simmons 2011].
evidence on AI: LLM agents that design falsification tests under sequential Type-I error
  control were run in six domains, and matched human scientists on complex
  biological hypotheses in a tenth of the time [Huang 2025].
skill: haipipe-insight-by-hypothesis-test (proposed)
