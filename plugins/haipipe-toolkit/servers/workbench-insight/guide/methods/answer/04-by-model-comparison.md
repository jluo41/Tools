By model comparison
===================

One question-answering method card. The Insight workbench shows it in the shared Guide › Method,
under Question-answering methods; its papers are the rows of `../../../related/papers.md` whose
`group` is `by model comparison`. A claim names its source in brackets; "(ours)" marks
the workbench's own judgment.

family: Question-answering
move: Fit an explanatory model and a predictive model to the same question, score both
  on held-out data against a simple benchmark, and say which goal each answers.
taxonomy: Predictive against inferential or causal [Leek 2015]; prediction against causal
  inference [Hernán 2019].
comes from: Breiman 2001, two cultures; Shmueli 2010, explain or predict
reads: question · the extract · a held-out partition
returns: each model's fit, its held-out score against a simple benchmark, and the goal it
  serves
test now: T4 spec · T7 held-out score against a simple benchmark
test in use: T8 the same ranking on another time window


What the literature says
------------------------

rationale: One culture assumes a stochastic data model; the other treats the mechanism as
  unknown and judges an algorithmic model by how well it predicts [Breiman 2001].
  Explanatory and predictive modelling differ at each step, and high explanatory
  power does not imply high predictive power [Shmueli 2010].
context: Statistics [Breiman 2001; Shmueli 2010]; psychology [Yarkoni 2017];
  computational social science [Hofman 2021].
steps: 1. State the goal: explain, predict or both [Shmueli 2010]. 2. Fit a data model
  for explanation. 3. Fit an algorithmic model for prediction [Breiman 2001]. 4.
  Score both on held-out data against a simple benchmark [Salganik 2020]. 5. Report
  each against its own goal [Hofman 2021].
strengths: Theories of mechanism often have little or unknown predictive accuracy, and
  held-out prediction measures it [Yarkoni 2017]. A common task with a benchmark
  shows how much is predictable at all [Salganik 2020].
limitations: In a mass collaboration of 160 teams, the best predictions of six life
  outcomes were only slightly better than a simple benchmark [Salganik 2020]. A
  predictive model's features are not causes; a causal reading needs a Design
  method such as a target trial (ours).


Applied to AI
-------------

agent: The agent fits both models from the spec's columns, and does not look at the
  held-out partition while fitting (ours).
steps: 1. Split by the spec's partition. 2. Fit the benchmark, the explanatory model and
  the predictive model. 3. Score all three on the held-out part. 4. Write which goal
  each serves.
returns: A table of the models, their held-out scores against the benchmark, and the goal
  each answers.
verify: A different agent re-scores the models on the held-out part from the saved
  predictions (T6, T7).
risk: Reporting an accurate predictor as an explanation, or tuning on the held-out part
  (ours).
evidence on AI: On a benchmark of 466 data analysis and 74 data modelling tasks, the best
  agent solved 34.12% of the analysis tasks [Jing 2024].
skill: haipipe-insight-by-model-comparison (proposed)
