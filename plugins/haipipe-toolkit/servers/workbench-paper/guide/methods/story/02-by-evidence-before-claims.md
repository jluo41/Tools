By evidence before claims
=========================

One story method card. The Paper workbench shows it in the shared Guide › Method,
under Story methods; its papers are the rows of `../../../related/papers.md` whose
`group` is `by evidence before claims`. A claim names its source in brackets; "(ours)" marks the
workbench's own judgment.

family: Story: What do we claim, on what evidence?
move: Name the evidence each claim needs, and what result would count against it, before
  the Task work that produces it runs.
comes from: Chambers & Tzavella 2022, Registered Reports; Kaplan & Irvin 2015, null
  effects after registration; Scheel et al. 2021, positive results
reads: the Story's claims
returns: each question's Logic: its evidence needs, fixed before the Work
test now: T2 fixed first
test in use: T3 reproduced


What the literature says
------------------------

rationale: In a Registered Report the questions and methods are reviewed before results
  exist [Chambers 2022]. Large trials showing a benefit fell from 17 of 30 to 2 of 25
  once outcomes had to be registered first [Kaplan 2015], and Registered Reports had 44%
  positive first hypotheses against 96% in standard reports [Scheel 2021].
context: Psychology and clinical trials, where outcomes are registered before data are
  collected [Chambers 2022; Kaplan 2015; Scheel 2021].
steps: 1. For each question, write the evidence that would answer it. 2. Write what
  would count against the claim. 3. Then run the Task work. 4. Record any change to the
  plan with its reason.
strengths: The answer cannot shape the question it answers (ours).
limitations: Exploratory findings still matter; they are reported as new questions, not
  as answers to the planned ones (ours).


Applied to AI
-------------

agent: The Story agent writes each question's Logic; the Task orchestrator runs the Work
  after it.
steps: 1. Write the Logic column. 2. Review it. 3. Commission the Task work. 4. Report
  from its Results.
returns: Story › Logic + Work + Report, one row per question.
verify: Each question's Logic is dated before its first Run (T2).
risk: An agent that has read the Results may write a Logic that fits them; the Logic is
  written first (ours).
evidence on ai: No study tests agents fixing evidence needs before analysis (ours).
skill: haipipe-paper-story
