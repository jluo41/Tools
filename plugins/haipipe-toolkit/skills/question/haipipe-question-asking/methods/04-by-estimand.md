By estimand
===========

One question-asking method card (`haipipe-question-asking`). The Insight workbench shows it in
the shared Guide › Method, step 1; its papers are the rows of that workbench's
`insight-papers.md` whose `group` is `by estimand`. A claim names its source in brackets; "(ours)" marks the workbench's own
judgment.

family: Question-asking
move: Name the target quantity in words, its unit, population, measure and summary,
  before any model or task is chosen.
taxonomy: Information (a descriptive estimand) or Knowledge (a causal one); description
  or causal inference [Hernán 2019].
comes from: Lundberg 2021, the theoretical estimand; ICH 2019, the estimand framework
reads: ask · rung
returns: the estimand of each need: unit, population, measure, summary across units,
  grouping, and how events that change the measure are handled
test now: T1 specified · T2 agreed
test in use: T8 reproduced


What the literature says
------------------------

rationale: Every quantitative study must be able to say what its estimand is: the
  target quantity, stated in precise terms that exist outside any statistical model
  [Lundberg 2021]. An estimand describes the effect to be estimated (the question)
  and is distinct from the analysis (how the question is answered) [Kahan 2021].
context: Sociology and the social sciences [Lundberg 2021]; randomised trials under the
  ICH E9(R1) addendum [ICH 2019; Kahan 2024]; the causal roadmap in epidemiology,
  which links a causal model to statistical estimation [Petersen 2014].
steps: 1. Set a theoretical estimand, linked to theory. 2. Link it to an empirical
  estimand under stated identification assumptions. 3. Learn it from data [Lundberg
  2021]. In trials, name its attributes: the population, the treatment, the
  outcome variable, how intercurrent events (events after the start that change
  or end the outcome) are handled, and the population-level summary [Kahan 2024].
strengths: Stating precise estimands expands the theoretical questions a study can
  ask and clarifies how evidence speaks to them [Lundberg 2021]. Two analysts can
  agree on what is asked before they differ on how (ours).
limitations: None of 50 published trial protocols stated the estimand of the primary
  outcome, and in 74% it could not be inferred [Kahan 2021]. Of 255 trials in six
  leading journals, none stated all its attributes, and the primary estimand could
  be determined in 46% [Cro 2022].


Applied to AI
-------------

agent: The drafter reads the ask and its rung and writes each need's estimand in words,
  before any task is read.
steps: 1. Name the unit and the population (the partition). 2. Name the measure and
  its summary across units. 3. Name the grouping or contrast. 4. Name the events that
  change the measure and how each is handled. 5. Say whether the estimand is
  descriptive or causal; a causal one needs a Knowledge question.
returns: The unit, measure, grouping and population rows of each need's work spec.
verify: A second agent writes the estimand from the ask alone and compares (T2); a
  mismatch on unit, population or summary sends the spec back (T1).
risk: An estimand written to match a model or a task already chosen, so the question
  follows the method (ours).
evidence on ai: Eight language models mapped free-text study descriptions to a
  structured specification with accuracy 0.93 to 0.97 on studies in a common data
  model, lower outside it [Kim 2026]. No study tests an AI writing an estimand from
  an ask (ours).
skill: haipipe-insight-evidence-plan
