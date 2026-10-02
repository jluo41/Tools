By automated insight search
===========================

One discovery method card. The Insight workbench shows it in Scope › Methods ›
Discovery methods; its papers are the rows of `../../insight-papers.md` whose
`group` is `by automated insight search`. A claim names its source in brackets; "(ours)"
marks the workbench's own judgment.

family: From the data
move: Enumerate the cuts of the extract, score each candidate pattern by how interesting
  it is, and return the top k.
status: future: a method to add later; no question is answered this way yet
taxonomy: Exploratory [Leek 2015]; description [Hernán 2019].
comes from: Tang 2017, top-k insights; Vartak 2015, views ranked by deviation
reads: question · the extract · its dimensions and measures
returns: the top k insights, each with its score, its cut, and the number of candidates
  searched
test now: T0 spec · T1 each insight says what its result says
test in use: T3 survives a correction for the number searched · T4 found again on
  another partition


What the literature says
------------------------

rationale: An insight is an interesting observation derived from aggregates over several
  steps, and a search can return the top k [Tang 2017]. Views of a data subset can
  be ranked by how far they deviate from a reference [Vartak 2015].
context: Business intelligence over multi-dimensional data [Tang 2017; Ding 2019];
  visualization recommendation [Vartak 2015]; tools that recommend insights to
  their users [Law 2020].
steps: 1. Define the insight types and how each is scored [Ding 2019]. 2. Enumerate the
  subspaces and aggregates. 3. Prune and score the candidates [Vartak 2015]. 4.
  Return the top k [Tang 2017].
strengths: One formulation covers several insight types, and it was evaluated on 447 real
  datasets and with expert and non-expert users [Ding 2019]. A review names 12
  types of automated insight and four purposes for automating them [Law 2020].
limitations: The score measures how unusual a pattern is, not whether it holds beyond the
  sample (ours). A long search is a multiple comparisons problem: the more
  comparisons, the more spurious insights [Zgraggen 2018]. Searching many patterns
  needs control of false discoveries [Hämäläinen 2019].


Applied to AI
-------------

agent: An LLM agent turns a question into a sequence of analysis actions over the data
  and returns insights [Ma 2023].
steps: 1. Read the question and the extract's schema. 2. Issue analysis actions on the
  cuts the spec names [Ma 2023]. 3. Score and rank the insights. 4. Return the top
  k with the number searched.
returns: The ranked insights, each with its cut, its result file and the size of the
  search.
verify: A different agent checks each sentence against its table (T1, T2) and re-runs the
  top insights on another partition (T4).
risk: Ranking by surprise rewards noise; a long search finds a striking pattern by chance
  (ours).
evidence on AI: On 100 datasets with planted insights, an end-to-end analysis agent did
  better than agents that answer single queries [Sahu 2024]. A user study and a
  case study show an LLM exploration system helping users find insights [Ma 2023].
skill: haipipe-insight-by-automated-insight-search (proposed)
