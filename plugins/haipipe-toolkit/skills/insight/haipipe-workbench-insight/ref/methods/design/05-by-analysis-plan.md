By analysis plan
================

One design method card. The Insight workbench shows it in the shared Guide › Method › Design
methods; its papers are the rows of `../../insight-papers.md` whose `group` is
`by analysis plan`. A claim names its source in brackets; "(ours)" marks the
workbench's own judgment.

family: From the claim
move: Write the questions, the analysis and the rule that decides the answer before the
  outcome is seen, and keep every later change visible as a deviation.
taxonomy: Any rung; the line between work that generates a hypothesis and work that
  tests one [Nosek 2018].
comes from: Nosek 2018, preregistration; Simmons 2011, researcher degrees of freedom
reads: ask · work spec
returns: a frozen plan with its time stamp: questions, needs, analyses, decision rules;
  after the run, a deviation log
test now: T1 specified · T2 agreed
test in use: T4 reproduced


What the literature says
------------------------

rationale: Mistaking an explanation made after the outcome for a prediction made
  before it reduces the credibility of findings; defining the questions and the
  analysis plan first keeps the two apart [Nosek 2018]. Undisclosed flexibility in
  collecting, analysing and reporting data raises the false-positive rate far above
  the nominal rate [Simmons 2011]. Presenting a hypothesis made after the results as
  if it came before them (HARKing) distorts the record [Kerr 1998].
context: Psychology [Simmons 2011; Scheel 2021]; large clinical trials [Kaplan 2015];
  data that already exist, where preregistration still helps with care [Nosek
  2018].
steps: 1. State the questions and hypotheses. 2. State the analysis of each: the data,
  exclusions, model and test. 3. State the rule that decides the answer. 4. Register
  it with a time stamp before the outcome is seen [Nosek 2018]. 5. Report every
  deviation from it [Claesen 2021].
strengths: Large heart, lung and blood trials showing a benefit fell from 17 of 30
  before 2000 to 2 of 25 after, when outcomes had to be registered first [Kaplan
  2015]. Registered Reports had 44% positive results against 96% in the standard
  literature [Scheel 2021].
limitations: Of 27 preregistered studies, 2 had no deviations from the plan and 9
  disclosed none of theirs [Claesen 2021]. Teams that planned on a blinded copy of
  the data deviated less from their plan than teams that preregistered, for about
  the same time [Sarafoglou 2023].


Applied to AI
-------------

agent: The drafter writes the plan without reading the outcome or the existing results;
  a different agent agrees it.
steps: 1. Write the work spec of each need. 2. Write the decision rule and the power
  rule. 3. Freeze the plan with its time stamp. 4. Run it, one run for one question.
  5. List each deviation and its reason on the page.
returns: The frozen spec and the deviation log.
verify: The agreeing agent checks that the plan was frozen before the run and that the
  run follows it (T2); a deviation with no reason fails.
risk: An agent that reads the data and then writes the plan is HARKing by
  construction [Kerr 1998] (ours).
evidence on ai: On 12 datasets and research questions with analyses by expert
  analysts, language model agents were often limited to basic analyses; agents that
  could interact with the data made more varied, but still not optimal, analysis
  decisions [Gu 2024 BLADE].
skill: haipipe-insight-evidence-plan
