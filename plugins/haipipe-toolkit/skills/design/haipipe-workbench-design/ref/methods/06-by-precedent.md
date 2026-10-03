By precedent
============

One design method card. Guide › Method shows it among its method cards; its
papers are the rows of `../design-papers.md` whose `group` is `by precedent`. A
claim names its source in brackets; "(ours)" marks the workbench's own judgment.

family: Internal Insights: induction, then abduction-1; the how comes from our own
  data, as signed insights
reasoning: analogy: a past design and its result → adapted to new requirements
move: Find the closest past design and adapt it to these requirements.
taxonomy: Adaptation: an intervention shown to work is adapted to a new sub-population,
  condition or context, outside the eight categories unless framed as development
  [O'Cathain 2019 taxonomy].
comes from: Kolodner 1993, case-based reasoning; Aamodt & Plaza 1994, retrieve, reuse,
  revise, retain; Alexander 1977, A Pattern Language
reads: design requirements · internal insights: past designs and their results
returns: the design, the case it adapted and how
test now: T1 not a copy of the case
test in use: T4 against the case


What the literature says
------------------------

rationale: Solve a new problem by adapting a remembered case [Kolodner 1993]: retrieve,
  reuse, revise, retain [Aamodt & Plaza 1994]. Proven solutions can be written
  as reusable patterns [Alexander 1977]. An intervention shown to work can be
  adapted to a new sub-population, condition or context [O'Cathain 2019
  taxonomy].
context: Problem solving and learning in AI [Aamodt & Plaza 1994]; architecture
  [Alexander 1977]; engineering design by analogy [Jiang 2021].
steps: 1. Retrieve the most similar case. 2. Reuse its solution. 3. Revise it to the new
  problem. 4. Retain what was learned [Aamodt & Plaza 1994].
strengths: Drawing on analogies can ease design fixation and improve ideation [Jiang
  2021].
limitations: No study tests the method against another (ours). A design close to its
  case may only copy it (ours).


Applied to AI
-------------

agent: The agent reads the design requirements and the past designs the board has sent,
  with their results in the Exp. A published case would be an external insight.
steps: 1. Retrieve the past design closest to this goal by meaning. 2. Take it as the
  base. 3. Revise it to the goal and its rules. 4. Name the case and what changed.
returns: The design, the case it adapted, the case's result, and what changed.
verify: Verify checks the design is not a copy of its case (T1) and the rules (T0); the
  Exp runs it against the case (T4).
risk: Retrieval returns a design that only looks similar; a copy adds nothing new
  (ours).
evidence on AI: Data-driven retrieval and mapping of analogies is surveyed [Jiang 2021];
  no study tests an AI designing messages by precedent yet (ours).
skill: haipipe-design-by-precedent (proposed)
