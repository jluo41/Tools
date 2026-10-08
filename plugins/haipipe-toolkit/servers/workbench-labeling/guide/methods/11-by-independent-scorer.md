By independent scorer
=====================

One labeling method card. Guide › Method shows it among its step's cards; its papers are
the rows of `../labeling-papers.md` whose `group` is `by independent scorer`. A claim
names its source in brackets; "(ours)" marks the workbench's own judgment.

family: Steps 5 and 6 · Check and deliver: is it right, and what is released
move: A different agent, one that made nothing, scores the models on the locked test by
  metrics fixed beforehand.
comes from: Panickssery 2024, self-preference of model evaluators
reads: locked answers · closed predictions · the registered metrics
returns: the scorecard and the chosen model
test now: T4 independent
test in use: T5 audit


What the literature says
------------------------

rationale: A model evaluator scores its own outputs higher than others that people judge
  equal [Panickssery 2024].
context: Language models as evaluators [Panickssery 2024].
steps: 1. Fix the metrics. 2. Score every model. 3. Choose by the fixed rule.
strengths: No producer grades itself (ours).
limitations: Two agents of one model may share blind spots (ours).


Applied to AI
-------------

agent: validator-agent
steps: 1. Read the registry. 2. Score. 3. Select by the preregistered rule.
returns: scorecards and the selection
verify: the scorer produced nothing it scores (T4)
risk: Changing the metric after seeing scores (ours).
evidence on ai: Self-preference [Panickssery 2024].
skill: haipipe-labeling-evaluation
