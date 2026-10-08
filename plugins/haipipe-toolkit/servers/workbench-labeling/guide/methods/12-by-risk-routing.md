By risk routing
===============

One labeling method card. Guide › Method shows it among its step's cards; its papers are
the rows of `../labeling-papers.md` whose `group` is `by risk routing`. A claim names its
source in brackets; "(ours)" marks the workbench's own judgment.

family: Steps 5 and 6 · Check and deliver: is it right, and what is released
move: While the chosen model labels the corpus, send the items it is least sure of, or
  that sit between labels, back to the person.
comes from: Wang 2024, verifying LLM labels
reads: the model's labels and confidence
returns: a queue the person labels
test now: T2 person is gold
test in use: T5 audit


What the literature says
------------------------

rationale: Judging which model labels to trust, and giving the rest to people, improves
  annotation quality [Wang 2024].
context: Human-LLM collaborative annotation [Wang 2024].
steps: 1. Score each label's risk. 2. Route the risky ones. 3. The person labels them.
strengths: Human time goes where the model is weakest (ours).
limitations: Confidently wrong labels are not routed; the audit samples them (ours).


Applied to AI
-------------

agent: classifier-agent routes; moderator-agent runs the review
steps: 1. Score uncertainty. 2. Build the queue. 3. Review with the person.
returns: reviewed labels for the risky items
verify: every routed item gets the person's label before release (T2)
risk: A threshold set too high leaves the person little to review (ours).
evidence on ai: Verification and routing raised label quality [Wang 2024].
skill: haipipe-labeling-scan
