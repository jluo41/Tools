Discovery methods
=================

An answer is found from data in many ways. Every discovery method turns a question and
the data into a claim: a question goes in, a run computes, a page says what the run
shows. The methods differ in two ways: whether they look first (read the data, then ask
what a pattern means) or ask first (state the question's type or test, then compute only
that), and in how they guard against finding what is not there, a pattern made by noise
or by the analyst's own choices (Gelman & Loken 2014). Design methods (the other view)
say how the inquiry is planned before any data is read; these say how the answer is
found once it is.

The Scope Space renders this file as its Methods › Discovery methods view. The papers named here
are listed, with their journals, in its Papers view (`insight-papers.md`).


1 · The shared loop
-------------------

```
Question ─────▶ Method ───────▶ Compute ────────▶ Check ─────────▶ Page ──────────▶ Use
the ask, its    choose one:     one run for one    a different      the answer at    a Knowledge
rung and its    look first or   question; its      agent checks     its rung, each   claim or Wisdom
work spec       ask first       code reads the     the run against  sentence tied    counsel that a
                                spec               its spec and     to its result;   later question
                                                   its rivals       CHECKed by       or a design
                                                                    another agent    reads
                                                                                       │
                  a refuted or fragile answer is a new Question ◀──────────────────────┘
```

Only the Method step and Compute differ from one method to another: what the chosen
method reads before it computes, and what its run must return. Every method keeps the
same Question and its work spec (cut or partition, unit, measure, grouping, uncertainty,
rivals, output columns), the same Check, the same Page and the same tests.


2 · Nine methods
----------------

Each method is one card in `methods/discovery/`: its move, what it reads before it
computes, what it returns, how its answer is tested and where the method comes from;
then what the literature says (its rationale, context, steps, strengths and limitations)
beside how it applies to AI (the agent, its steps, what it returns, how a second agent
verifies it, its risk, and the evidence on AI). The cards fall into three families by
where the answer starts: the data (1 to 3, look first), the question (4 to 6, ask first),
or many analyses of one question (7 to 9, check what was found). A card marked
`status: future` is a method to add later; no question is answered that way yet. The
Discovery methods view shows the cards, each with its papers (`insight-papers.md`,
`group` = the method).

| family | method | card |
|---|---|---|
| From the data | By exploring | methods/discovery/01-by-exploring.md |
| From the data | By automated insight search | methods/discovery/02-by-automated-insight-search.md |
| From the data | By pattern mining | methods/discovery/03-by-pattern-mining.md |
| From the question | By question type | methods/discovery/04-by-question-type.md |
| From the question | By model comparison | methods/discovery/05-by-model-comparison.md |
| From the question | By hypothesis test | methods/discovery/06-by-hypothesis-test.md |
| From many analyses | By multiverse | methods/discovery/07-by-multiverse.md |
| From many analyses | By heterogeneity | methods/discovery/08-by-heterogeneity.md |
| From many analyses | By sensemaking | methods/discovery/09-by-sensemaking.md |

Leek & Peng 2015 sort data analysis questions into six types: descriptive, exploratory,
inferential, predictive, causal and mechanistic. Hernán et al. 2019 sort data science
into three tasks: description, prediction and causal inference (counterfactual
prediction). Each card names its type and task on its `taxonomy` line:

| method | Leek & Peng type | Hernán task |
|---|---|---|
| By exploring | exploratory | description |
| By automated insight search | exploratory | description |
| By pattern mining | exploratory | description |
| By question type | names one of the six | names one of the three |
| By model comparison | predictive against inferential or causal | prediction against causal inference |
| By hypothesis test | inferential | description or causal inference |
| By multiverse | any type, as a robustness check | any task |
| By heterogeneity | inferential or causal, across groups | description across cuts, or causal inference |
| By sensemaking | causal and mechanistic | causal inference |

The families follow the types (ours): the data family finds exploratory patterns, which
are hypotheses, not findings; the question family answers inferential, predictive and
causal questions with an analysis chosen first; the many-analyses family checks that an
answer of any type survives the choices behind it. A Data or Information question is
description; a Knowledge question is inferential, predictive or causal; a Wisdom
question uses the answers below it.


3 · How an answer is tested
---------------------------

| test | asks | when | source |
|---|---|---|---|
| T0 Spec | the run's files and columns are the ones the spec names | now · Check | reproducible computation (Sandve et al. 2013; Peng 2011) |
| T1 Fidelity | each sentence says what its result says | now · Page CHECK | faithfulness to the source (Maynez et al. 2020) |
| T2 Independent check | an agent that did not write the page checks it | now · Page CHECK | self-preference and failed self-correction (Panickssery et al. 2024; Huang et al. 2023) |
| T3 Robustness | rival analyses and the multiverse give the same sign and size | now · Check | multiverse and specification curve (Steegen et al. 2016; Simonsohn et al. 2020) |
| T4 Replication | another extract, partition or time window gives it again | later · new data | replication projects (Open Science Collaboration 2015; Camerer et al. 2018) |

T0 to T2 ask: was the answer computed and written right? Only T3 and T4 ask: is the
answer there in the world, and not in one analysis of one sample? Every method gets T0
to T2. A method that claims a finding beyond its sample gets T3, and T4 when new data
comes. Each method's tests are on its card.


4 · What the evidence says about the methods
--------------------------------------------

- One question, many analysts, many answers: 29 teams on one dataset reported odds ratios
  from 0.89 to 2.93, and 20 of 29 found a significant effect (Silberzahn et al. 2018);
  over 95% of the variance between 73 teams' results stayed unexplained by their coded
  decisions (Breznau et al. 2022). One run is one point of a multiverse; T3 is not
  optional for a Knowledge claim.
- Flexibility in collection, analysis and reporting raises the false-positive rate far
  above the stated alpha (Simmons et al. 2011). Looking first is a search, and a search
  must be paid for.
- In visual exploration, over 60% of the insights users reported on data with known
  truth were false (Zgraggen et al. 2018). An exploratory observation is a hypothesis
  for another method to test.
- Of 117 subgroup claims in trial abstracts, 46 had a significant interaction test and
  none of 5 corroboration attempts found the effect (Wallach et al. 2017). A split across
  partitions needs its own test.
- When the analysis is fixed before the results, positive results fall from 96% to 44%,
  plausibly through less publication bias and less inflated Type I error (Scheel et al.
  2021). Asking first makes a positive answer rarer.
- Of 100 psychology studies, 97% were significant and 36% of their replications were,
  with effects halved (Open Science Collaboration 2015). An answer that held on one
  sample is not yet T4.
- LLM agents are weak data analysts so far: the best system scored 25% on DiscoveryBench
  (Majumder et al. 2024); the best agent solved 32.4% of ScienceAgentBench (Chen et al.
  2024); agents were often limited to basic analyses on BLADE (Gu et al. 2024). Their
  output needs T0 to T2 by a different agent, since a model favours its own output
  (Panickssery et al. 2024).

No study compares these methods head to head on one question. The method is itself a
bet: does looking first and then checking against many analyses find answers that
replicate (T4) as often as asking first? Answer one question by several methods and
compare them now (T0 to T3) and on the next partition or time window (T4).
