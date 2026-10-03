By exploring
============

One discovery method card. The Insight workbench shows it in the shared Guide › Method ›
Discovery methods; its papers are the rows of `../../insight-papers.md` whose
`group` is `by exploring`. A claim names its source in brackets; "(ours)" marks the
workbench's own judgment.

family: From the data: look first, then ask what a pattern means
move: Look at the extract with simple displays and summaries before any model, and write
  down what is seen as an observation, not yet a finding.
taxonomy: Exploratory [Leek 2015]; description [Hernán 2019].
comes from: Tukey 1977, exploratory data analysis; Tukey 1962, data analysis as a science
reads: question · the extract · its columns
returns: the observations, each with the table or figure it was seen in, and the number
  of views looked at
test now: T0 spec · T1 each observation says what its table says
test in use: T4 seen again on another partition


What the literature says
------------------------

rationale: Look at the data first, with simple displays and summaries, before a model
  says what to look for [Tukey 1977]. Data analysis is a science of its own, with
  procedures for analysing data and ways to interpret their results [Tukey 1962].
  Exploration complements confirmatory tests; it does not replace them [Behrens
  1997].
context: Statistics and data analysis [Tukey 1977]; psychology [Behrens 1997]; visual
  analysis tools such as Tableau [Battle 2019].
steps: 1. Summarise each column and its missing values. 2. Plot distributions and
  relations. 3. Note what stands out. 4. Write what would check it (ours).
strengths: Analysts were over 80% accurate on focused tasks with measurably correct
  answers, and their analyses overlapped, so exploration is predictable [Battle
  2019]. A look at the data can be framed as a model check against a reference
  distribution, which joins exploration to confirmation [Hullman 2021].
limitations: The more views are examined, the more spurious patterns are found: on
  synthetic data with known truth, over 60% of the insights users reported were
  false [Zgraggen 2018]. Taking an exploratory finding as confirmatory is the
  forking paths problem [Pu 2018; Gelman 2014]. An observation needs a stated test
  on data it was not found in; fixing that test in advance is a Design method
  (ours).


Applied to AI
-------------

agent: The agent reads the question's work spec and the extract's columns, and runs only
  the summaries the spec allows (ours).
steps: 1. Profile each column the spec names. 2. Draw the displays the question needs.
  3. Write each observation with the table or figure it comes from. 4. Count the
  views looked at, so a later test can correct for them [Zgraggen 2018].
returns: The observations, each tied to its result file, and the number of views looked
  at.
verify: A different agent checks that each observation says what its table shows (T1,
  T2). An observation becomes a claim only after another method tests it (ours).
risk: An agent can look at many cuts quickly and report the striking ones, which
  multiplies false patterns [Zgraggen 2018].
evidence on AI: On 264 discovery tasks drawn from published papers, the best LLM system
  scored only 25% [Majumder 2024]. No study tests an agent's exploratory
  observations against known truth yet (ours).
skill: haipipe-insight-data
