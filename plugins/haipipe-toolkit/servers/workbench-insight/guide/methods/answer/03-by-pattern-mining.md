By pattern mining
=================

One question-answering method card. The Insight workbench shows it in the shared Guide › Method,
under Question-answering methods; its papers are the rows of `../../../related/papers.md` whose
`group` is `by pattern mining`. A claim names its source in brackets; "(ours)" marks the
workbench's own judgment.

family: Question-answering
move: Run a pattern search (association rules, subgroups of a target) over the extract,
  and keep only the patterns that pass a test with false discoveries controlled.
status: future: a method to add later; no question is answered this way yet
taxonomy: Exploratory [Leek 2015]; description [Hernán 2019].
comes from: Fayyad 1996, knowledge discovery in databases; Agrawal 1993, association rules
reads: question · the extract · a target column
returns: the surviving patterns, each with its support and its test, and the number of
  patterns tested
test now: T4 spec · T7 survives false discovery control
test in use: T8 holds on another partition or time window


What the literature says
------------------------

rationale: Mining patterns is one step of a knowledge discovery process that also
  selects, preprocesses and interprets the data [Fayyad 1996]. Every association
  rule between items in a large database can be found efficiently [Agrawal 1993].
context: Retail transactions [Agrawal 1993]; databases in science and business [Fayyad
  1996]; subgroups that stand out on a target variable [Herrera 2011; Atzmueller
  2015].
steps: 1. Select and preprocess the data [Fayyad 1996]. 2. Mine the candidate patterns
  [Agrawal 1993]. 3. Test each pattern, and control false discoveries over all
  those evaluated [Hämäläinen 2019]. 4. Interpret what survives [Fayyad 1996].
strengths: Statistical tests put a strict upper limit on the risk of experimentwise error
  in a pattern search [Webb 2007]. Tests also filter out uninformative variations
  of the key patterns [Hämäläinen 2019].
limitations: Without tests, a pattern search carries an extreme risk of false
  discoveries [Webb 2007]. A pattern is an association; it says nothing about cause
  (ours).


Applied to AI
-------------

agent: The agent runs a mining library on the columns the spec names; it does not pick
  the patterns it reports by eye (ours).
steps: 1. Fix the target, the item columns and the minimum support in the spec. 2. Mine.
  3. Test every pattern, with a correction for the number tested [Benjamini 1995].
  4. Report what survives, with the count tested.
returns: The surviving patterns with their tests, and the number of patterns tested.
verify: A different agent re-runs the mining on a held-out partition (T8) and checks that
  the count tested matches the run (T4).
risk: An agent may report a pattern that only looks strong because thousands were tested
  [Webb 2007].
evidence on AI: No study tests an LLM agent mining patterns with false discovery control
  yet (ours).
skill: haipipe-insight-by-pattern-mining (proposed)
