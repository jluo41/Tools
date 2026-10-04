By written guideline
====================

One labeling method card. Guide › Method shows it among its step's cards; its papers are
the rows of `../labeling-papers.md` whose `group` is `by written guideline`. A claim names
its source in brackets; "(ours)" marks the workbench's own judgment.

family: Step 4 · Rounds: which items a round draws, and how each gets its label
move: After each round, write the rules the person's judgments imply into a versioned
  guideline, so the meaning carries from round to round.
comes from: Pustejovsky 2012, guidelines; Artstein 2008, agreement
reads: the round's judgments and reasons
returns: the next guideline version
test now: T0 meaning
test in use: T5 audit


What the literature says
------------------------

rationale: Guidelines are revised through the annotation cycle until annotators agree
  [Pustejovsky 2012], and agreement shows whether the guideline is clear [Artstein 2008].
context: Corpus annotation [Pustejovsky 2012; Artstein 2008].
steps: 1. Collect the round's reasons. 2. Draft rules. 3. The person accepts them. 4.
  Version the guideline.
strengths: The frozen guideline lets a model label the corpus the person's way (ours).
limitations: Rules written from few items may not generalize; later rounds test them
  (ours).


Applied to AI
-------------

agent: moderator-agent, then gallery-keeper-agent
steps: 1. Draft from accepted judgments. 2. Get the person's acceptance. 3. Close the
  round with the new version.
returns: the guideline version and its diff
verify: every rule traces to accepted judgments; no test item is cited (T3)
risk: A rule drafted from model reasoning, not the person's, drifts the meaning (ours).
evidence on ai: No study tests agent-drafted guidelines (ours).
skill: subjective-label-guideline
