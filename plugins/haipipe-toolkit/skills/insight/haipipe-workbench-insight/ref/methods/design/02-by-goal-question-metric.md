By goal-question-metric
=======================

One design method card. The Insight workbench shows it in the shared Guide › Method › Design
methods; its papers are the rows of `../../insight-papers.md` whose `group` is
`by goal-question-metric`. A claim names its source in brackets; "(ours)" marks the
workbench's own judgment.

family: From the goal
move: Derive questions from a stated goal and measures from each question, top down; no
  measure is collected that no question asks for.
taxonomy: Any rung; the step from a Wisdom goal down to the Data and Information measures
  that serve it (ours).
comes from: Basili 1994, goal question metric; Basili 1984, goal-directed data collection
reads: goal · ask
returns: the goal, its questions, the evidence needs and measures of each, and a map from
  every word of the ask to a need
test now: T0 covered · T1 specified
test in use: T4 reproduced


What the literature says
------------------------

rationale: Measurement must be defined top down, focused on goals and models; a
  metric-driven, bottom-up approach does not work because there are too many things
  that can be observed [van Solingen 2002]. Data collection starts from the claims
  to be evaluated, which set its goals and the questions the analysis must answer
  [Basili 1984].
context: Software engineering measurement [Basili 1984]; industrial software
  organisations [van Solingen 2001]; measurement tied to business goals and
  strategies [Basili 2010].
steps: 1. State the goal: the object, the purpose, the quality focus, the viewpoint and
  the context [Basili 1994]. 2. Refine the goal into questions. 3. Give each question
  the metrics that answer it. 4. Interpret the measured data against the questions
  and, through them, the goal [van Solingen 2002].
strengths: Every measure carries its reason, written before anything is collected
  (ours). The method extends upward, linking measurement goals to the goals and
  strategies of an organisation [Basili 2010].
limitations: Its support is industrial experience, not comparative studies [van
  Solingen 2001] (ours). It gives no rule for when a question is answered strongly
  enough; that needs a power rule (By partition and power) (ours).


Applied to AI
-------------

agent: The drafter reads the goal and the ask and has not read the task catalog.
steps: 1. Write the goal in its five parts. 2. Split it into questions, one claim
  each. 3. Give each question its evidence needs and each need a measure. 4. Map every
  content word of the ask to a need or a refusal.
returns: The goal, its questions, their evidence needs with measures, and the coverage
  map from words to needs.
verify: A second agent reads the ask and the coverage map and checks that no word is
  unmapped (T0) and that every need has its spec fields (T1).
risk: A drafter that has seen the existing tasks writes needs that fit them, measuring
  what is cheap rather than what is asked (ours).
evidence on ai: No study tests an AI deriving measures from goals yet (ours).
skill: haipipe-insight-evidence-plan
