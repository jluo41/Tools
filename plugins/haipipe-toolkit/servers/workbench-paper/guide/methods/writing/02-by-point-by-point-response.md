By point-by-point response
==========================

One writing method card. The Paper workbench shows it in the shared Guide › Method,
under Writing methods; its papers are the rows of `../../../related/papers.md` whose
`group` is `by point-by-point response`. A claim names its source in brackets; "(ours)" marks the
workbench's own judgment.

family: Writing and response: How is it told, and defended?
move: Quote each reviewer point, answer it, and change the paper for it, saying where;
  route each point to the part of the paper that owns it.
comes from: Noble 2017, ten simple rules for writing a response to reviewers
reads: the reviews · the paper
returns: a response with every point quoted, answered and located
test now: T5 answered
test in use: T5 answered


What the literature says
------------------------

rationale: A response to reviewers quotes the reviews and summarizes each change made
  for them, so the editor can see every point answered [Noble 2017].
context: Peer review of scientific papers [Noble 2017].
steps: 1. Split the reviews into points. 2. Route each to the Story, the Work or a
  Section. 3. Make the change there. 4. Write the answer with the change's place.
strengths: No point is lost, and each change is made where its fault is (ours).
limitations: A point-by-point answer can hide that a reviewer's main concern is not met;
  the summary at the top names it (ours).


Applied to AI
-------------

agent: A writing agent drafts the response; the changes are made through the owning
  step's runs.
steps: 1. Split and route the points. 2. Make the changes. 3. Draft the answers. 4. The
  person signs the round (G5).
returns: the round's response and the changed paper.
verify: Every point has an answer and a located change (T5).
risk: A model may answer politely without changing the paper (ours).
evidence on ai: No study tests agent-drafted responses to reviewers (ours).
skill: haipipe-paper-comments
