By weak-model committee
=======================

One labeling method card. Guide › Method shows it among its step's cards; its papers are
the rows of `../labeling-papers.md` whose `group` is `by weak-model committee`. A claim
names its source in brackets; "(ours)" marks the workbench's own judgment.

family: Step 4 · Rounds: which items a round draws, and how each gets its label
move: Let several small models label each round first, sealed, as fast first readers whose
  answers are compared with the person's and never become gold.
comes from: Gilardi 2023, models as annotators; Tan 2024, LLM annotation
reads: the round · the current guideline
returns: sealed model labels per item
test now: T1 blind
test in use: T4 independent


What the literature says
------------------------

rationale: Language models label some text tasks as well as or better than crowd workers
  [Gilardi 2023], and are widely used to annotate [Tan 2024], but their errors need
  checking [Wang 2024].
context: Text annotation for social science and NLP [Gilardi 2023; Tan 2024].
steps: 1. Run each registered model on the round. 2. Seal the labels. 3. Reveal them only
  after the person's first label.
strengths: Shows at once where the guideline is unclear to a reader (ours).
limitations: Models trained alike share mistakes; agreement is not truth (ours).


Applied to AI
-------------

agent: labeler-panel-agent
steps: 1. Run the frozen wrapper per model. 2. Seal predictions. 3. Write them beside the
  round.
returns: sealed predictions with confidence and reasons
verify: predictions are sealed before the person's first label (T1)
risk: If the person sees model labels first, they anchor on them (ours).
evidence on ai: Models beat crowd workers on several tasks [Gilardi 2023]; verifying their
  labels raises quality [Wang 2024].
skill: subjective-label-rounds
