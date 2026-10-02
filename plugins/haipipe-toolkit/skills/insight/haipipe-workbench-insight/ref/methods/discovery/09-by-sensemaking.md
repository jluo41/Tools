By sensemaking
==============

One discovery method card. The Insight workbench shows it in Scope › Methods ›
Discovery methods; its papers are the rows of `../../insight-papers.md` whose
`group` is `by sensemaking`. A claim names its source in brackets; "(ours)" marks the
workbench's own judgment.

family: From many analyses
move: Hold several explanations of a result at once, fit each to the evidence, and keep
  the one the evidence does not rule out, with its rivals named.
taxonomy: Causal and mechanistic [Leek 2015]; causal inference [Hernán 2019].
comes from: Pirolli 2005, the foraging and sensemaking loops; Klein 2006, the data/frame
  model; Chamberlin 1890, multiple working hypotheses
reads: question · the lower pages' answers · the rival explanations
returns: the claim, its strength, each rival and why it is or is not ruled out, and the
  claim's boundary
test now: T1 the claim says what its results say · T2 a different agent's rivals
test in use: T4 the claim holds on the next partition


What the literature says
------------------------

rationale: Analysts move between a foraging loop that gathers evidence and a sensemaking
  loop that builds and tests a story [Pirolli 2005]. A frame explains the data, and
  the data can question, elaborate or replace the frame [Klein 2006]. Hold several
  explanations at once rather than one favoured one [Chamberlin 1890].
context: Intelligence analysis [Pirolli 2005; Dhami 2019]; naturalistic decision making
  [Klein 2006]; information retrieval and interface design [Russell 1993].
steps: 1. Gather the evidence and find a representation for it [Russell 1993]. 2. Write
  the explanations that could produce it [Chamberlin 1890]. 3. Name the result that
  would rule each one out [Platt 1964]. 4. Keep the one left, with its rivals and
  its boundary.
strengths: Choosing and changing the representation lowers the cost of the analysis
  [Russell 1993]. A test devised to exclude alternative hypotheses is what Platt
  credits for the fields that move fastest [Platt 1964].
limitations: In a randomized study of 50 analysts, those trained to analyse competing
  hypotheses skipped some of its steps, showed mixed evidence of less confirmation
  bias, and may have judged less consistently [Dhami 2019]. A story can be coherent
  and wrong; coherence is not a test (ours).


Applied to AI
-------------

agent: The agent reads the results and Information pages a Knowledge question builds on,
  and writes the claim with its rivals (ours).
steps: 1. Read the cited results. 2. Write the claim and at least two rivals. 3. For each
  rival, name the result that rules it out, or say it stands. 4. Write the boundary.
returns: The claim, its strength, its rivals with their status, and its boundary, on the
  Knowledge page.
verify: A different agent writes its own rivals before it reads the page, then checks
  that each is addressed (T2).
risk: An agent may write rivals it can easily dismiss and miss the one that matters
  (ours).
evidence on AI: No study tests an AI agent's rival explanations against known truth yet
  (ours).
skill: haipipe-insight-knowledge
