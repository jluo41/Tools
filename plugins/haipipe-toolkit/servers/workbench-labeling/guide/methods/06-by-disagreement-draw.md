By disagreement draw
====================

One labeling method card. Guide › Method shows it among its step's cards; its papers are
the rows of `../labeling-papers.md` whose `group` is `by disagreement draw`. A claim names
its source in brackets; "(ours)" marks the workbench's own judgment.

family: Step 4 · Rounds: which items a round draws, and how each gets its label
move: In later rounds, draw the items where the models disagree or sit between labels, so
  each round teaches the most.
comes from: Settles 2012, uncertainty sampling; Ein-Dor 2020, active learning for BERT
reads: the models' sealed labels · the regions
returns: the next round's batch
test now: T3 sealed
test in use: T5 audit


What the literature says
------------------------

rationale: Labeling the items a model is least sure of improves it faster than random
  items [Settles 2012]; with BERT the gain is largest when labels are few [Ein-Dor 2020].
context: Text classification [Settles 2012; Ein-Dor 2020].
steps: 1. Find disagreement and boundary items. 2. Mix in some random ones. 3. Release the
  round.
strengths: Each human label is spent where it changes the guideline most (ours).
limitations: A round of only hard items can skew the guideline; a random share keeps it
  honest (ours).


Applied to AI
-------------

agent: sampler-agent, with the disagreement-analyzer-agent
steps: 1. Read the last round's measures. 2. Rank candidates. 3. Compose the batch with a
  random share.
returns: the round manifest and how each item was chosen
verify: no test item is drawn (T3); the random share is recorded
risk: Models that agree on a mistake are never drawn; the random share and the audit catch
  some (ours).
evidence on ai: Active learning helps BERT at small budgets [Ein-Dor 2020].
skill: haipipe-labeling-rounds
