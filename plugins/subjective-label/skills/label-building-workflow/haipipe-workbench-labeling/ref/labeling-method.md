Method
======

1 · The six steps
-----------------

| step | what happens | methods | where in the workbench | who signs |
|---|---|---|---|---|
| Prepare the corpus | raw conversations become checked items, one per reply to judge, and whole source groups are held back for the test (section 2) | Prepare | Data › Preparation · runs Normalize source, Choose labeling unit, Create candidate items, Check candidate items, Reserve source groups | the labeling unit; the custodian holds the test |
| Set up the job | the Contract names the question, the person who decides what the labels mean, and the custodian of the held-back test | none | Data › Contract · Embedding · runs Set up the job, Build a map | the Contract |
| Confirm the meanings | each label's meaning is discussed, then confirmed; no round is drawn before (section 3) | Meanings | Labeling › Definition · runs Search outside evidence, Discuss the label meanings | each label's meaning (G0) |
| Label in rounds | a round draws items, models pre-label them blind, the person gives each item its final label, and the guideline is revised from the judgments (section 4) | Rounds | Labeling › Rounds · Guideline · runs Draw one round, Pre-label one prepared round, You label one round, Measure one completed judgment set, Close a measured round, Draft a guideline from accepted judgments | each item's final label; each guideline version |
| Check against the held-back test | models predict the locked test and a different agent scores them; after the scan, the audit of the released labels is drawn and analyzed here too (section 5) | Check and deliver | Quality › Test · Evaluation · Audit · runs Hold back test items, Lock blind answers for the final test, Have one registered model predict the test, Score one closed set of predictions, Select from the complete scorecard set, Draw from one frozen audit design, Blind-label one audit sample, Analyze one completed audit sample | the blind test answers; the audit labels |
| Deliver | the handoff is frozen, the corpus is labeled, risky items go back to the person, and the audited labels are released (section 5) | Check and deliver | Delivery › Handoff · Scan · Final labels · runs Freeze a stopped labeling lineage, Check one frozen production plan, Label one frozen corpus shard, Route risky production items to review, You label one production risk queue, Reconcile reviewed items into a candidate corpus, Publish an accepted audited corpus | the frozen handoff; each reviewed label; the release |

One labeling job is one corpus, one question and one person who decides what the labels
mean. That person is the only source of gold: a model's agreement, or a dataset's own
label, never makes a label true (模型同意不等于正确).

One example runs through this page, and it is made up. A patient writes "I missed this
morning's pill, can I take two tonight?" and the assistant replies "Yes, just double it
tonight." The question is: how unsafe is the assistant's reply?

The steps happen in four Spaces of the workbench, each with its own Views:

| space | what it is for | view | what it shows |
|---|---|---|---|
| Data | turn the corpus into items, set up the job, and map the items | Preparation | the raw corpus, what one item is, the items and their checks |
| Data | | Contract | the job: its question, its decider, its custodian, its counts |
| Data | | Embedding | a map of the items, grouped by similarity |
| Labeling | decide what the labels mean and label in rounds | Definition | each label's meaning, the discussion and the confirmation (G0) |
| Labeling | | Rounds | each round's items, the person's labels and the models' |
| Labeling | | Guideline | the written rules, one version per closed round |
| Quality | check models against the held-back test, and audit the release | Test | the sealed test and its locked blind answers |
| Quality | | Evaluation | the models' scores on the test, and the one chosen |
| Quality | | Audit | a blind sample of the released labels, labeled again |
| Delivery | freeze, label the corpus, and release the labels | Handoff | the frozen guideline and model |
| Delivery | | Scan | the corpus labeled, and the risky items sent to the person |
| Delivery | | Final labels | the released labels and their counts |


2 · Step 1 in depth: prepare the corpus
---------------------------------------

2.1 · From raw files to items
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

```
raw file        one row per conversation, in the dataset's own shape
   ↓ transform.py, one per corpus
transcripts     conversation_id · split_group_id · turns of role and content
   ↓ normalize · choose the unit · make the items · check them
items           one item = the reply to judge, with the turns before it as context
   ↓ reserve
held back       whole source groups, locked away for the test
```

Every corpus has its own small script that turns its raw files into transcripts; the rest
of the path is the same for every corpus. Labels the dataset came with are written to a
separate file and never enter an item. In the example, the chat becomes one item: the
reply "Yes, just double it tonight" is what the person judges, and the patient's question
is its context.

2.2 · Hold whole groups back
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A source group (one conversation, one patient, one prompt answered several times) sits
entirely on one side: development or the held-back test. If two replies to the same
prompt fell on both sides, the test would reward remembering the prompt, not judging the
reply. The test is reserved before the job's Contract, and its custodian is named.

2.3 · Its method cards
~~~~~~~~~~~~~~~~~~~~~~

Each method is one card in `methods/`: its step, its move, what it reads and returns,
where it comes from and how it is tested; then what the literature says beside how it
applies to AI. Each card's papers are the rows of `labeling-papers.md` whose `group` is
the method.

| family | method | card |
|---|---|---|
| Step 1 · Prepare: which items exist, and which are held back | By unit recipe | methods/01-by-unit-recipe.md |
| Step 1 · Prepare: which items exist, and which are held back | By group-held test | methods/02-by-group-held-test.md |


3 · Step 3 in depth: confirm the meanings
-----------------------------------------

3.1 · Three labels and the space between them
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

```
high          clearly unsafe              the example: double a dose, no advice
low           some risk, or unclear
none          safe
in between    HL · LN · HN · HLN          the person cannot place it in one label
```

Every judgment also lands in one of seven regions: H, L, N for a clear label, and HL, LN,
HN, HLN when the item sits between two or three. An item in between is not an error; it
shows where the meaning still needs a rule (介于两者之间的样本，正是需要补规则的地方).
Each judgment also says how sure the person is: low, medium or high.

3.2 · What the confirmation binds
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The person confirms the question, each label and its meaning, the regions, the
uncertainty levels, and what an unresolved item counts as. The confirmation (G0) keeps a
copy of exactly that text. No round is drawn before it; a later change to a meaning is a
new version, confirmed again.

3.3 · Its method cards
~~~~~~~~~~~~~~~~~~~~~~

| family | method | card |
|---|---|---|
| Step 3 · Meanings: what each label means, confirmed before any round | By discussion then confirm | methods/03-by-discussion-then-confirm.md |
| Step 3 · Meanings: what each label means, confirmed before any round | By in-between regions | methods/04-by-in-between-regions.md |


4 · Step 4 in depth: label in rounds
------------------------------------

4.1 · One round
~~~~~~~~~~~~~~~

```
draw        round 1 at random; later rounds from disagreement and boundaries
   ↓
pre-label   small models label the round blind and seal their answers
   ↓
you label   your first label locks; then the models' answers show; you give the final
   ↓
measure     where you and the models disagree, and why
   ↓
close       the round is kept; the guideline is revised from your judgments
```

In the example: the models said "low". The person first said "high", and it locked. They
then saw "low", kept "high" as the final label, and wrote a rule: "advising a double dose
is high, whatever the tone". That rule goes into the next guideline.

4.2 · Which method when
~~~~~~~~~~~~~~~~~~~~~~~

```
Which items does this round draw?
├─ round 1 ─────────── By random first round   an unbiased first look at the corpus
└─ later rounds ────── By disagreement draw    where models disagree or sit between labels

How does an item get its label?
├─ before you ──────── By weak-model committee   small models pre-label, sealed, never gold
├─ you ─────────────── By blind first judgment   your first label locks before any answer shows
└─ after the round ─── By written guideline      the round's rules, written down and versioned
```

4.3 · What each judgment records
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each judgment is a chain of events, appended and never edited: the item was shown, the
first label and its region, the lock, what was revealed, the final label, the
uncertainty and the reason. Only the person's final label is gold; the models' answers
stay beside it as evidence.

4.4 · Its method cards
~~~~~~~~~~~~~~~~~~~~~~

| family | method | card |
|---|---|---|
| Step 4 · Rounds: which items a round draws, and how each gets its label | By random first round | methods/05-by-random-first-round.md |
| Step 4 · Rounds: which items a round draws, and how each gets its label | By disagreement draw | methods/06-by-disagreement-draw.md |
| Step 4 · Rounds: which items a round draws, and how each gets its label | By weak-model committee | methods/07-by-weak-model-committee.md |
| Step 4 · Rounds: which items a round draws, and how each gets its label | By blind first judgment | methods/08-by-blind-first-judgment.md |
| Step 4 · Rounds: which items a round draws, and how each gets its label | By written guideline | methods/09-by-written-guideline.md |


5 · Steps 5 and 6 in depth: how a job is checked
------------------------------------------------

5.1 · The six tests
~~~~~~~~~~~~~~~~~~~

| test | asks | when | source |
|---|---|---|---|
| T0 Meaning | every label's meaning was confirmed before any round | step 3 · Labeling › Definition | the annotation cycle (Pustejovsky & Stubbs 2012) |
| T1 Blind | the person's first label locks before any model answer or reference shows | step 4 · Labeling › Rounds | anchoring (Tversky & Kahneman 1974) |
| T2 Person is gold | no label becomes gold without the person's final judgment | step 4 · step 6 | human label variation (Plank 2022) |
| T3 Sealed | no test item enters a round, a prompt or a guideline; whole groups stay apart | step 1 · step 5 | leakage (Kapoor & Narayanan 2023) |
| T4 Independent | a different agent scores the models on the locked test, by metrics fixed beforehand | step 5 · Quality › Evaluation | self-preference of model evaluators (Panickssery et al. 2024) |
| T5 Audit | a blind sample of the released labels agrees with the person | step 6 · Quality › Audit | inter-coder agreement (Artstein & Poesio 2008) |

T0 and T2 guard the meaning, T1 the person's judgment, T3 and T4 the test, and T5 the
release. A model is chosen to label the corpus only if it passes the locked test; the
labels are released only when the audit agrees and the person signs.

5.2 · Where the truth comes from
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

```
the truth comes from    a score means                           e.g.
the person only         agreement with the person               a new question no one has labeled
dataset labels          agreement with the dataset's labels     a public set labeled by its authors
many raters             closeness to the spread of opinions     every item rated by a hundred people
a measured outcome      whether the labels predict the effect   a click, a donation, a vaccination
```

The six tests are the same in every case; what a score means changes. A dataset's own
labels, when there are any, are kept out of the items and read only when scoring, so the
person still judges blind.

5.3 · What the evidence says
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- On several text-labeling tasks a large language model beat crowd workers (Gilardi et
  al. 2023); by weak-model committee uses models as fast first readers, not as judges.
- Judging which model labels to trust, and sending the rest to people, improved the
  labels' quality (Wang et al. 2024); by risk routing does this in step 6.
- People disagree on subjective labels for good reasons, not only by mistake (Plank
  2022; Aroyo & Welty 2015); the in-between regions keep that disagreement visible.
- Choosing which items to label pays most when labels are few (Settles 2012; Ein-Dor et
  al. 2020); round 1 stays random so the first look is unbiased.
- A test that leaks overstates a model, and random splits overstate it too (Kapoor &
  Narayanan 2023; Søgaard et al. 2021); hence whole groups held back and sealed.

No study tests this whole loop. Its order is our own judgment.

5.4 · Their method cards
~~~~~~~~~~~~~~~~~~~~~~~~

| family | method | card |
|---|---|---|
| Steps 5 and 6 · Check and deliver: is it right, and what is released | By sealed test | methods/10-by-sealed-test.md |
| Steps 5 and 6 · Check and deliver: is it right, and what is released | By independent scorer | methods/11-by-independent-scorer.md |
| Steps 5 and 6 · Check and deliver: is it right, and what is released | By risk routing | methods/12-by-risk-routing.md |
| Steps 5 and 6 · Check and deliver: is it right, and what is released | By audit sample | methods/13-by-audit-sample.md |


6 · Why it works
----------------

6.1 · A subjective label has no answer key
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"How unsafe is this reply?" has no answer waiting to be found; someone has to decide what
"unsafe" means here (主观标签没有现成的答案，需要有人来定义). Two careful people can
disagree, and both can be right by their own rule (Plank 2022). So one named person
decides the meaning, writes it down, and keeps it the same from round to round.

```
meaning     the person decides it, once, and confirms it (G0)
   ↓
rules       the guideline writes it down, round by round
   ↓
labels      every label follows the rules, so it can be checked
```

6.2 · Models are fast readers, not judges
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Models label quickly and often well (Gilardi et al. 2023), but when several agree they can
share the same mistake. So their labels are sealed before the person looks, compared
after, and never promoted to gold.

6.3 · A test seen once is no longer a test
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If test items shape the guideline, the test only measures how well the guideline
remembers them (Kapoor & Narayanan 2023). The held-back test is locked from step 1 and
opened once, in step 5.


Reference
---------

R1 · Terms
~~~~~~~~~~

| term | 中文 | meaning |
|---|---|---|
| item | 样本 | one reply to judge, with the turns before it as context |
| source group | 来源组 | items that must stay together: one conversation, patient or prompt |
| held-back test | 留出测试集 | whole source groups locked away until step 5 |
| custodian | 保管人 | the person who holds the held-back test |
| G0 | 含义确认 | the person's confirmation of what each label means |
| region | 区域 | H, L, N, or between them: HL, LN, HN, HLN |
| round | 轮次 | one batch the person labels, with the models' sealed answers beside |
| guideline | 标注指南 | the written rules, one version per closed round |
| weak model | 弱模型 | a small model that pre-labels; its answers are never gold |
| handoff | 交接 | the frozen guideline and model chosen to label the corpus |
| scan | 批量标注 | labeling the corpus with the handoff, risky items back to the person |
| audit | 抽查 | a blind sample of the released labels, labeled again by the person |

R2 · How annotation tools cover the steps
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Three tools people use to label text, beside our methods, step by step: Label Studio
([repository](https://github.com/HumanSignal/label-studio)), an open-source labeling tool
with model pre-labels through its ML backend; Prodigy ([site](https://prodi.gy)), a
scriptable annotation tool built around model-in-the-loop recipes; and Argilla
([repository](https://github.com/argilla-io/argilla)), an open-source tool for human
feedback on model and LLM outputs. The cells are our reading of their documentation on
2026-10-03, and the coverage is our own judgment; both are to be checked.

| step | our methods | Label Studio | Prodigy | Argilla | coverage |
|---|---|---|---|---|---|
| Prepare the corpus | By unit recipe · By group-held test | data import · labeling config | loaders · recipes | dataset settings: fields · records | Both · raw files become items. Ours only · whole source groups held back before any label |
| Set up the job | none | project · members and roles | recipe arguments: dataset · labels | workspace · users · dataset settings | Both · a project with its labels and annotators. Ours only · a named decider and a custodian of the test |
| Confirm the meanings | By discussion then confirm · By in-between regions | labeling instructions | label names | guidelines · question descriptions | Both · written instructions. Ours only · meanings confirmed before any item (G0) · in-between regions |
| Label in rounds | By random first round · By disagreement draw · By weak-model committee · By blind first judgment · By written guideline | ML backend pre-labels · active learning | teach recipes: model in the loop | suggestions from models · several responses per record | Both · model pre-labels and chosen items. Ours only · the first label locks before any pre-label shows. Gap · many annotators on one item |
| Check against the held-back test | By sealed test · By independent scorer · By audit sample | agreement between annotators | train with an evaluation set | agreement metrics | Both · labels scored against answers. Ours only · a sealed test, scored by a different agent by fixed metrics |
| Deliver | By risk routing | review stream · export | review recipe · export | export to the Hugging Face Hub | Both · review and export. Ours only · risky items routed back to the person before release |
