Method
======

1 · The six steps
-----------------

Every question goes through six steps, in three columns: Logic (1-2), Work (3-4) and
Report (5-6). Steps 1, 3 and 5 have methods to choose from; sections 2 to 4 give them.

Steps 1 and 2 happen once, in the **Prototype**; steps 3 to 6 happen on every dataset, in
its **Instance**:

```
Prototype · one per topic, no data          Instance · one per dataset
steps 1-2: the partitions, the questions,   steps 3-6: a tracked copy of each script,
their plans and their scripts       ──▶     one run per partition, the pages, the
                                            handoff
                                            a new dataset is a new Instance of the
                                            same Prototype
```

The questions and their code are written once and run unchanged on each dataset, so two
datasets' answers can be compared: By protocol reuse (§ 2) built into the boards. A
script changed in the Prototype reaches an Instance only as a new tracked copy.

| step | board | what happens | where in the workbench | who decides |
|---|---|---|---|---|
| **1 Ask the question** | Prototype | one ask at its rung, why now, and what would answer it; question-asking methods (§ 2) | Scope › Questions (Ask) · Prototype › Data … Wisdom (Review the questions) | a person signs the question |
| **2 Plan and agree** | Prototype | the steps that would answer it, written before any data is read; then the script, written and reviewed; tests T0-T3 (§ 5) | Prototype › Data … Wisdom (Plan the evidence · Review the evidence plan · Write and Review the script) | a different agent agrees the plan |
| **3 Run each partition** | Instance | the script runs once on each partition; question-answering methods (§ 3) | Insight › each partition (Run a partition) | the run's own receipt |
| **4 Check the run** | Instance | the run is checked against its plan; tests T4 and T7 (§ 5) | Insight › each partition (Check alignment) | an agent that did not write the run |
| **5 Write the page** | Instance | one page per question, a section per partition, read into an answer at its rung; question-results reading methods (§ 4); tests T5 and T6 (§ 5) | Insight › each partition (Write the report) · Check › Checks (Review an answer) | an agent that did not write the page |
| **6 Hand off** | Instance | a Wisdom answer goes to Design; test T8 when new data comes (§ 5) | Delivery › Handoff (Write the counsel · Draft the handoff) | a person signs the handoff |

A person signs only what leaves the board or changes its meaning: the question, a change
the question review proposes, a new partition, and the handoff. A signed change retires
a question with its reason; it is never edited in place. Every method keeps the same
question file, the same plan fields (partition, unit, measure, grouping, uncertainty,
rivals, output columns), the same second agent and the same tests; only its own step
changes.


2 · Step 1 in depth: ask the question
-------------------------------------

2.1 · The ladder: four kinds of question
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Every question sits on one rung of four: Data 数据, Information 信息, Knowledge 知识 and
Wisdom 智慧. The ladder is the same for any data; X and Y below stand for any factor and
any outcome, and the examples come from three kinds of data.

```
rung          the question, for any data                for example
Data          what is there: how many, which fields,    visits per clinic · readings per sensor
              what is missing?                          · orders per day
Information   what pattern: a rate, a trend, a          no-show rate by weekday · failure rate
              difference between groups?                by model · basket size by season
Knowledge     does X change Y, with other things        do reminders cut no-shows? · does heat
              held equal, and how sure are we?          shorten a sensor's life?
Wisdom        what should we do about X?                which clinics get reminders · when to
                                                        replace sensors
```

The rung decides what the answer may say. Data and Information describe: counts, rates
and contrasts, never "because". Knowledge makes one claim, with how sure it is, its
rivals and its limits. Wisdom advises what to do, and a person signs it for Design.
A Data or Information question that says "because" is moved up to Knowledge or refused.

2.2 · Question-asking methods: what exactly are we asking, and what would answer it?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

```
What does the question need fixed first?
├─ its rung                     By rung              always first
├─ a goal it serves             By goal-question-metric
├─ its kind: describe, predict  By question type
│  or explain
├─ the number that answers it   By estimand
├─ a cause, from data already   By target trial      (future)
│  collected
├─ the analysis, before data    By analysis plan
├─ where it is asked, and       By partition and power
│  whether that is enough data
└─ the same plan on new data    By protocol reuse
```

These eight methods serve any board's question, so they live in the question world
(`haipipe-question-asking`); whether an ask is a good one is judged by its seven tests
(`haipipe-question-review`).

| family | method | card |
|---|---|---|
| Question-asking | By rung | ../../../question/haipipe-question-asking/methods/01-by-rung.md |
| Question-asking | By goal-question-metric | ../../../question/haipipe-question-asking/methods/02-by-goal-question-metric.md |
| Question-asking | By question type | ../../../question/haipipe-question-asking/methods/03-by-question-type.md |
| Question-asking | By estimand | ../../../question/haipipe-question-asking/methods/04-by-estimand.md |
| Question-asking | By target trial | ../../../question/haipipe-question-asking/methods/05-by-target-trial.md |
| Question-asking | By analysis plan | ../../../question/haipipe-question-asking/methods/06-by-analysis-plan.md |
| Question-asking | By partition and power | ../../../question/haipipe-question-asking/methods/07-by-partition-and-power.md |
| Question-asking | By protocol reuse | ../../../question/haipipe-question-asking/methods/08-by-protocol-reuse.md |


3 · Step 3 in depth: run each partition
---------------------------------------

Question-answering methods: how does the run find the answer? A run either looks first (reads
the data, then asks what a pattern means) or asks first (the test is fixed, then
computed). A pattern found by looking first is a new question for step 1, not yet an
answer.

```
Does the question name its test?
├─ no, look first     By exploring                   by eye, simple tables
│                     By automated insight search    score many cuts (future)
│                     By pattern mining              rules and subgroups (future)
└─ yes, ask first     By hypothesis test             one stated test
                      By model comparison            explain against predict
```

| family | method | card |
|---|---|---|
| Question-answering | By exploring | methods/answer/01-by-exploring.md |
| Question-answering | By automated insight search | methods/answer/02-by-automated-insight-search.md |
| Question-answering | By pattern mining | methods/answer/03-by-pattern-mining.md |
| Question-answering | By model comparison | methods/answer/04-by-model-comparison.md |
| Question-answering | By hypothesis test | methods/answer/05-by-hypothesis-test.md |


4 · Step 5 in depth: write the page
-----------------------------------

Question-results reading methods: does the answer survive the ways it could be wrong? Before a page
claims anything beyond one analysis of one sample, it tries the other ways the answer
could come out.

```
How could the answer be wrong?
├─ another analysis would change it    By multiverse
├─ it differs by partition             By heterogeneity
└─ another explanation fits            By sensemaking
```

| family | method | card |
|---|---|---|
| Question-results reading | By multiverse | methods/read/01-by-multiverse.md |
| Question-results reading | By heterogeneity | methods/read/02-by-heterogeneity.md |
| Question-results reading | By sensemaking | methods/read/03-by-sensemaking.md |


5 · Steps 2, 4, 5 and 6 in depth: checking
------------------------------------------

5.1 · Nine tests, each at its step
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

```
step 2 Plan and agree    T0 Covered · T1 Specified · T2 Agreed · T3 Powered
step 4 Check the run     T4 Spec · T7 Robustness
step 5 Write the page    T5 Fidelity · T6 Independent check
step 6 in use            T8 Replication, when new data comes
```

| test | asks | when | source |
|---|---|---|---|
| T0 Covered | every word of the ask maps to a step or a refusal | step 2 · Plan | requirements traceability (Gotel & Finkelstein 1994) |
| T1 Specified | each step names partition, unit, measure, grouping, uncertainty, rivals, output | step 2 · Plan | analysis plan content (Gamble et al. 2017; Chan et al. 2013) |
| T2 Agreed | a different agent that did not draft the plan agrees it | step 2 · Agree | review before results (Chambers 2013) |
| T3 Powered | each partition can detect the smallest effect that matters | step 2 · Agree | power analysis (Cohen 1992; Lakens 2022) |
| T4 Spec | the run's files and columns are the ones the plan names | step 4 · Check | reproducible computation (Sandve et al. 2013; Peng 2011) |
| T5 Fidelity | each sentence says what its result says | step 5 · Page check | faithfulness to the source (Maynez et al. 2020) |
| T6 Independent check | an agent that did not write the page checks it | step 5 · Page check | self-preference and failed self-correction (Panickssery et al. 2024; Huang et al. 2023) |
| T7 Robustness | rival analyses give the same sign and size | step 4 · Check | multiverse and specification curve (Steegen et al. 2016; Simonsohn et al. 2020) |
| T8 Replication | another extract, partition or time window gives it again | step 6 · in use | replication projects (Open Science Collaboration 2015; Camerer et al. 2018) |

T4 to T6 ask whether the answer was computed and written right. Only T7 and T8 ask
whether it is there in the world, not just in one analysis of one sample.

5.2 · What the evidence says
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Plan first (T0-T2).** When outcomes had to be registered in advance, large heart,
  lung and blood trials showing a benefit fell from 17 of 30 to 2 of 25 (Kaplan & Irvin
  2015); Registered Reports had 44% positive results against 96% elsewhere (Scheel et
  al. 2021). A plan is not kept by itself: of 27 preregistered studies, 9 disclosed none
  of their deviations (Claesen et al. 2021).
- **Enough data (T3).** Small samples make a significant result less likely to be true
  (Button et al. 2013).
- **A second checker (T6).** A language model scores its own output higher than others'
  (Panickssery et al. 2024); the best agents solve about a quarter to a third of
  data-analysis benchmarks (Majumder et al. 2024; Chen et al. 2024).
- **Other analyses (T7).** 29 teams given the same data and question reported odds
  ratios from 0.89 to 2.93 (Silberzahn et al. 2018); flexible analysis raises false
  positives far above the stated rate (Simmons et al. 2011). In visual exploration, over
  60% of reported insights on data with known truth were false (Zgraggen et al. 2018).
- **Splits by group (T7).** Of 117 subgroup claims in trial abstracts, 46 had a
  significant test of the difference, and none of 5 attempts to confirm one succeeded
  (Wallach et al. 2017).
- **New data (T8).** Of 100 psychology studies, 97% were significant and 36% of their
  replications were (Open Science Collaboration 2015).

No study compares these methods head to head on one question. The workbench is itself
a bet: does a question planned before the data, agreed by a second agent and powered
per partition give answers that hold on the next extract (T8) more often than one
fitted to the runs already in hand?


6 · Why it works
----------------

6.1 · Insight learns from our own data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Insight looks at what we sent and what happened, and works out the rule behind it. In
the Design family's words, that is induction (归纳推理): we know the thing and the
result, and look for the rule.

```
📚 Discovery   reads papers           ──▶  external insights ──┐
🔎 Insight     reads our own data     ──▶  internal insights ──┼──▶ 🎨 Design ──▶ 🧪 Exp
                    ▲                      (a signed handoff)  ┘     invents        a trial
                    └──────────── the Exp's data is the next extract ◀──────────────┘
```

Insight never designs, and it never searches papers to answer a question; that search
is Discovery's work. Design reads only a signed Insight answer, never a page in progress.

6.2 · Why the plan comes before the data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Data can be cut many ways, and some cut always looks interesting. If the question and
its analysis are chosen after looking, the answer has shaped the question, and a pattern
made by noise or by our own choices passes as a finding (Gelman & Loken 2014). Writing
the plan first (step 2) separates testing a prediction from fitting a story to results
already in hand (Nosek et al. 2018). A question that came out of the data, a pattern
someone noticed, is welcome: it is a new question, planned again before it is answered.


Reference
---------

R1 · Terms and people
~~~~~~~~~~~~~~~~~~~~~

| term | 中文 | what it means here | read more |
|---|---|---|---|
| DIKW | 数据 · 信息 · 知识 · 智慧 | the ladder of § 2.1 | [Wikipedia](https://en.wikipedia.org/wiki/DIKW_pyramid) · [中文维基](https://zh.wikipedia.org/wiki/DIKW体系) |
| Induction | 归纳推理 | from cases to a rule: Insight's reasoning | [Wikipedia](https://en.wikipedia.org/wiki/Inductive_reasoning) · [中文维基](https://zh.wikipedia.org/wiki/归纳推理) |
| Preregistration | 预注册 | the plan written before the data (step 2) | [Wikipedia](https://en.wikipedia.org/wiki/Preregistration_(science)) |
| Estimand | | the exact number that would answer a question | [Wikipedia](https://en.wikipedia.org/wiki/Estimand) |
| Goal question metric | | every measure has a question, every question a goal | [Wikipedia](https://en.wikipedia.org/wiki/GQM) |
| Forking paths | | choices made after seeing data produce false findings | [Wikipedia](https://en.wikipedia.org/wiki/Forking_paths_problem) |
| Data dredging | | searching many cuts until one looks significant | [Wikipedia](https://en.wikipedia.org/wiki/Data_dredging) |
| Multiverse analysis | | one question through every reasonable analysis | [Wikipedia](https://en.wikipedia.org/wiki/Multiverse_analysis) |
| Replication crisis | | why T8 matters | [Wikipedia](https://en.wikipedia.org/wiki/Replication_crisis) |
| Prototype | | one board per topic: partitions, questions, plans and scripts; no data | § 1 |
| Instance | | one board per dataset, read through one Prototype: runs, pages, handoff | § 1 |

| person | what they gave | read more |
|---|---|---|
| Russell L. Ackoff | data, information, knowledge, wisdom (1989) | [Wikipedia](https://en.wikipedia.org/wiki/Russell_L._Ackoff) |
| Jennifer Rowley | the DIKW hierarchy reviewed (2007) | [the paper](https://doi.org/10.1177/0165551506070706) |
| Jeff Leek and Roger Peng | six types of data question (2015) | [the paper](https://doi.org/10.1126/science.aaa6146) |
| Miguel Hernán | three data science tasks: describe, predict, explain (2019) | [the paper](https://doi.org/10.1080/09332480.2019.1579578) |
| Brian Nosek | the case for writing the plan first (2018) | [the paper](https://doi.org/10.1073/pnas.1708274114) |
| Andrew Gelman and Eric Loken | the garden of forking paths (2014) | [the paper](https://doi.org/10.1511/2014.111.460) |
| Sara Steegen and others | multiverse analysis (2016) | [the paper](https://doi.org/10.1177/1745691616658637) |
| Thomas C. Chamberlin | multiple working hypotheses (1890) | [the paper](https://doi.org/10.1126/science.ns-15.366.92) |
| Kees Dorst | induction and abduction, as the Design family uses them (2011) | [the paper](https://doi.org/10.1016/j.destud.2011.07.006) |

The family names and their Chinese (question-asking 提问, question-answering 求答 and
question-results reading 解读 methods) and the words Prototype and Instance are ours.

R2 · Which kind of question each method serves
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Leek & Peng 2015 sort data questions into six types; Hernán et al. 2019 sort data
science into three tasks. Data and Information questions are description; Knowledge is
prediction or causal inference; Wisdom uses the answers below it (the mapping is ours).

| method | Leek & Peng type | Hernán task |
|---|---|---|
| By question type | names one of the six | names one of the three |
| By exploring | exploratory | description |
| By automated insight search | exploratory | description |
| By pattern mining | exploratory | description |
| By model comparison | predictive against inferential or causal | prediction against causal inference |
| By hypothesis test | inferential | description or causal inference |
| By multiverse | any type, as a robustness check | any task |
| By heterogeneity | inferential or causal, across groups | description across cuts, or causal inference |
| By sensemaking | causal and mechanistic | causal inference |

R3 · Where the workbench's rules come from
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| rule | method it comes from (ours) |
|---|---|
| one run answers one question | By analysis plan: a run serving several questions drifts toward whichever comes out |
| every word of the ask is covered or refused | By goal-question-metric |
| the plan is drafted before any existing run is read | By analysis plan, applied to code |
| reuse a run only when its output is identical | By protocol reuse |
| no cause word at Data or Information | By rung; a kept causal ask goes to Knowledge and By target trial |
| partitions and power fixed before any outcome | By partition and power |
| partitions differ only by a test of the difference | By heterogeneity |
