By random first round
=====================

One labeling method card. Guide › Method shows it among its step's cards; its papers are
the rows of `../labeling-papers.md` whose `group` is `by random first round`. A claim
names its source in brackets; "(ours)" marks the workbench's own judgment.

family: Step 4 · Rounds: which items a round draws, and how each gets its label
move: Draw round 1 at random from the development items, so the first look at the corpus
  is unbiased.
comes from: Settles 2012, the cold start of active learning
reads: the development items
returns: round 1's batch
test now: T3 sealed
test in use: T5 audit


What the literature says
------------------------

rationale: Selecting items needs a model that already knows something; a first random
  sample avoids choosing from a model's blind spots [Settles 2012].
context: Active learning for classifiers [Settles 2012].
steps: 1. Draw a seeded random batch. 2. Record the seed. 3. Release it as round 1.
strengths: Shows what the corpus really holds, rare cases included by chance (ours).
limitations: Rare kinds of items may be missed in a small batch (ours).


Applied to AI
-------------

agent: sampler-agent
steps: 1. Read the eligible items. 2. Draw with a fixed seed. 3. Write the batch.
returns: the round manifest and its seed
verify: the batch holds no test item (T3)
risk: A non-random first round bakes in the drawer's guess (ours).
evidence on ai: Active selection gains most once a model exists [Ein-Dor 2020].
skill: subjective-label-rounds
