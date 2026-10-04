By sealed test
==============

One labeling method card. Guide › Method shows it among its step's cards; its papers are
the rows of `../labeling-papers.md` whose `group` is `by sealed test`. A claim names its
source in brackets; "(ours)" marks the workbench's own judgment.

family: Steps 5 and 6 · Check and deliver: is it right, and what is released
move: Open the held-back test once: models predict it, and their labels are scored against
  the person's blind answers on it.
comes from: Kapoor 2023, leakage; Søgaard 2021, random splits
reads: the sealed test · the frozen guideline
returns: the models' scores on unseen items
test now: T3 sealed
test in use: T4 independent


What the literature says
------------------------

rationale: Only data never used in development shows how a method does on new data [Kapoor
  2023]; harder splits give more honest estimates [Søgaard 2021].
context: Machine-learning evaluation [Kapoor 2023; Søgaard 2021].
steps: 1. Lock the person's blind answers. 2. Run the models. 3. Score once.
strengths: The score is a fair forecast of the scan (ours).
limitations: A small test gives wide uncertainty (ours).


Applied to AI
-------------

agent: gallery-keeper-agent locks; labeler-panel-agent predicts
steps: 1. Lock the answers. 2. Predict per model. 3. Hand to the scorer.
returns: locked answers and closed predictions
verify: the test was never opened before (T3)
risk: Rerunning until a model passes turns the test into tuning (ours).
evidence on ai: Leaked tests overstate models [Kapoor 2023].
skill: subjective-label-test
