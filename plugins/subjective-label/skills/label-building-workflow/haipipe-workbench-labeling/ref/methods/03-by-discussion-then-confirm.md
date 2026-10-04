By discussion then confirm
==========================

One labeling method card. Guide › Method shows it among its step's cards; its papers are
the rows of `../labeling-papers.md` whose `group` is `by discussion then confirm`. A claim
names its source in brackets; "(ours)" marks the workbench's own judgment.

family: Step 3 · Meanings: what each label means, confirmed before any round
move: Discuss what each label means, with examples and outside sources, then have the
  person confirm the exact wording before any round (G0).
comes from: Pustejovsky 2012, the annotation cycle; Plank 2022, human label variation
reads: the question · outside evidence · the person's view
returns: the confirmed meanings (G0)
test now: T0 meaning
test in use: T2 person is gold


What the literature says
------------------------

rationale: Annotation runs as a cycle of specification, guidelines and labeling
  [Pustejovsky 2012]; for subjective labels, disagreement is real, so whose meaning counts
  must be decided [Plank 2022].
context: Linguistic annotation [Pustejovsky 2012]; subjective NLP tasks [Plank 2022].
steps: 1. Draft each meaning. 2. Discuss edge cases. 3. The person confirms the exact
  text.
strengths: Every later label can be read against one fixed meaning (ours).
limitations: The first meaning is a guess; rounds will refine it as new versions (ours).


Applied to AI
-------------

agent: moderator-agent
steps: 1. Lay out drafts and outside evidence. 2. Ask the person about edge cases. 3.
  Record the confirmed text.
returns: the G0 receipt with the confirmed meanings
verify: the engine refuses any round before G0 (T0)
risk: The agent can steer the meaning toward what models already label well; the person
  writes the final words (ours).
evidence on ai: No study tests agent-led definition of label meanings (ours).
skill: subjective-label-definition
