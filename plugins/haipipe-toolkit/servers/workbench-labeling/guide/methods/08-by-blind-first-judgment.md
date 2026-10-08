By blind first judgment
=======================

One labeling method card. Guide › Method shows it among its step's cards; its papers are
the rows of `../labeling-papers.md` whose `group` is `by blind first judgment`. A claim
names its source in brackets; "(ours)" marks the workbench's own judgment.

family: Step 4 · Rounds: which items a round draws, and how each gets its label
move: The person labels each item first without any model answer or reference in view; the
  first label locks, then the answers show and the person gives the final label.
comes from: Tversky 1974, anchoring
reads: the item and its context only
returns: a locked first label, then a final label
test now: T1 blind
test in use: T2 person is gold


What the literature says
------------------------

rationale: An initial value shown before a judgment pulls the judgment toward it [Tversky
  1974].
context: Judgment under uncertainty [Tversky 1974].
steps: 1. Show the item. 2. Lock the first label. 3. Reveal the models. 4. Take the final
  label and reason.
strengths: The first label is the person's own; changes after the reveal are visible
  (ours).
limitations: Slower than accepting a pre-label (ours).


Applied to AI
-------------

agent: moderator-agent
steps: 1. Show one item. 2. Record and lock the first label. 3. Reveal. 4. Record the
  final label.
returns: the event chain for each item
verify: the lock event comes before the reveal event (T1)
risk: A chat that hints at the models' view breaks blindness; the moderator shows only the
  item (ours).
evidence on ai: Anchoring is shown for people [Tversky 1974]; no study tests it with model
  pre-labels (ours).
skill: haipipe-labeling-rounds
