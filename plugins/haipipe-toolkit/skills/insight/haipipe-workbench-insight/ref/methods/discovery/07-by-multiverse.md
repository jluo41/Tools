By multiverse
=============

One discovery method card. The Insight workbench shows it in Scope › Methods ›
Discovery methods; its papers are the rows of `../../insight-papers.md` whose
`group` is `by multiverse`. A claim names its source in brackets; "(ours)" marks the
workbench's own judgment.

family: From many analyses: check what was found against the ways it could be wrong
move: Run one question through every reasonable analysis (each defensible cut, exclusion,
  coding and model), and report how much the answer moves.
taxonomy: Any type, as a robustness check [Leek 2015]; any of the three tasks [Hernán
  2019].
comes from: Steegen 2016, multiverse analysis; Simonsohn 2020, specification curve;
  Silberzahn 2018, many analysts
reads: question · its work spec · the defensible choices at each step
returns: the answer under every specification, the share with the same sign, and the
  choices that move it most
test now: T3 the same sign and size across the multiverse
test in use: T4 replication on new data


What the literature says
------------------------

rationale: Processing data involves choices among several reasonable options, and one
  analysis of one processed dataset can mislead [Steegen 2016]. Analytic decisions
  are defensible, arbitrary and motivated, and add variability that standard errors
  do not show [Simonsohn 2020].
context: Psychology [Steegen 2016; Silberzahn 2018]; neuroimaging [Botvinik-Nezer 2020];
  social science [Breznau 2022].
steps: 1. List the justified, valid and non-redundant specifications. 2. Run them all and
  plot the results. 3. Infer jointly across them [Simonsohn 2020]. 4. Name the
  choices the result is most fragile to [Steegen 2016].
strengths: It shows how much a conclusion depends on arbitrary choices, and which choices
  matter most [Steegen 2016]. Of three published findings, one was robust, one weak
  and one not robust at all [Simonsohn 2020]. The shared analysis can be written
  once with its alternatives and compiled into every path [Liu 2021].
limitations: The set of reasonable specifications is itself a choice (ours). Coded
  decisions left over 95% of the variance between 73 teams' results unexplained
  [Breznau 2022], so a listed multiverse may miss what drives disagreement. Teams'
  expertise and prior beliefs did not explain the spread either [Silberzahn 2018].


Applied to AI
-------------

agent: The agent builds the specifications from the work spec's rivals line and runs
  each as its own task output (ours).
steps: 1. Read the spec's cut, unit, measure and rivals. 2. List the alternatives at each
  step. 3. Run every path. 4. Report the curve and the share that agree.
returns: The specification curve, the share with the same sign, and the most consequential
  choices.
verify: A different agent adds a specification the first did not list and checks that the
  answer holds (T2, T3).
risk: An agent may list only the paths it already ran; flexibility in analysis raises
  false positives [Simmons 2011].
evidence on AI: On 12 research questions with expert analyses as ground truth, LLMs were
  often limited to basic analyses, and agents that work on the data made more
  diverse but still not optimal decisions [Gu 2024 BLADE].
skill: haipipe-insight-by-multiverse (proposed)
