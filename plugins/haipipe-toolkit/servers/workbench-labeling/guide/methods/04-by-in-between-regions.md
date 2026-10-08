By in-between regions
=====================

One labeling method card. Guide › Method shows it among its step's cards; its papers are
the rows of `../labeling-papers.md` whose `group` is `by in-between regions`. A claim
names its source in brackets; "(ours)" marks the workbench's own judgment.

family: Step 3 · Meanings: what each label means, confirmed before any round
move: Let the person place an item between labels (HL, LN, HN, HLN) instead of forcing
  one, and use those items to write the next rule.
comes from: Plank 2022, human label variation; Aroyo 2015, disagreement as signal
reads: each judgment
returns: a region per judgment, and where rules are missing
test now: T2 person is gold
test in use: T5 audit


What the literature says
------------------------

rationale: Disagreement among annotators often reflects real ambiguity, not error, and is
  information worth keeping [Aroyo 2015; Plank 2022].
context: Crowd annotation [Aroyo 2015]; NLP data and evaluation [Plank 2022].
steps: 1. Record a region with every label. 2. Collect the in-between items. 3. Write a
  rule for each pattern.
strengths: Ambiguity becomes a list of rules to write, not noise (ours).
limitations: Too many in-between items mean the question itself is unclear (ours).


Applied to AI
-------------

agent: moderator-agent and disagreement-analyzer-agent
steps: 1. Ask for the region with the label. 2. Group the in-between items. 3. Draft
  candidate rules.
returns: regions per item and candidate rules
verify: the person accepts each rule before it enters the guideline
risk: An agent may resolve ambiguity itself; only the person settles it (ours).
evidence on ai: No study tests regions in agent-assisted labeling (ours).
skill: haipipe-labeling-rounds
