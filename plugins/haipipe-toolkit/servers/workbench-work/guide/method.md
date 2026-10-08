Method
======

1 · The eight steps, by level
-----------------------------

Each step sits at the level it acts on, numbered in the order the work runs: a Block asks the
Question and answers it, a Job holds a line of Tasks, a Task is planned, built, run and read.
"Where" is the frame's Space the step is done in, and the run that starts it in that Space's
Runs panel. Guide › Method shows each level's steps as cards.

**Block · the Question and its report**

| step | what happens | methods | where in the workbench | who signs |
|---|---|---|---|---|
| 1 · Ask the Question | one main topic: the question, what we expect and what would answer it; a different agent reviews it | Question-asking | Audience Report › All · run Ask a Question | the question |
| 7 · Write the report | the Question's report: Opening, Answer, Evidence, Limits, Next, each claim citing an exact Result | Report | Audience Report › All · run Write the report | none |
| 8 · Check and deliver | an agent that did not write the report checks it; an answered report is built and released | Report | Audience Report › All · run Check a report; Delivery · run Build the delivery | the release |

**Job · one line of work**

| step | what happens | methods | where in the workbench | who signs |
|---|---|---|---|---|
| Lay out the Job | one line of work: its Tasks, in the order they run; each Task then takes steps 2 to 6 | Run | Work Details · run Add a Task | none |

**Task · planned, built, run and read**

| step | what happens | methods | where in the workbench | who signs |
|---|---|---|---|---|
| 2 · Plan the Task | the Task's contract, written before its code: what it reads, what it returns, how it is checked | Run | Description › Plan · run Plan a Task | none |
| 3 · Build the Task | the worker, its config and its Ticket, in the Task Folder | Run | Work Details › Code · run Build the Task | none |
| 4 · Review the code | an agent that did not write the code reads it before the Ticket runs | Run | Work Details › Review · run Review the Task code | none |
| 5 · Run the Ticket | the Ticket runs one config and writes one Result with its receipt; heavy output goes to its store | Run | Runs · run Run a Task | none |
| 6 · Report the Run | what the Run shows, read from its Result alone | Report | Audience Report › Report · run Write the report | none |

A failed check goes back to the step that owns the fault: a vague question to Ask, a wrong
number to the worker and its Ticket (never to the Result), an unsupported sentence to Write.
Nothing is fixed in a generated file: a Result, a receipt, a figure or a built page is
changed only by rerunning what made it. Every run is in the Runs panel beside its Space,
with the prompt to start it.

One example runs through this page, and it is made up: a Block that asks how one month of
clinic visits reads, one row per visit, with a Task that counts the visits per clinic.


2 · Step 1 in depth: asking the Question
----------------------------------------

A Block's Question is one main topic, recorded once in the register in `board.md` with its
report folder `reports/qNN_<topic>/` (`haipipe-question`). Its Logic is three lines a
person signs: the question, what we expect, and what would answer it. In the example:
"How does the visits extract read?", "one row per visit, one clinic per row", and "a card
with the row count, the clinics and the columns, citing the Tasks' Results".

The question is shaped and judged by the question skills every board shares, not by this
workbench: `haipipe-question-asking` picks the method that fixes what the question needs
first (its level, its goal, its type, the number that answers it, a cause, the analysis,
where and with how much data, or the same plan on new data), and `haipipe-question-review`
judges it by seven tests (one thing, logic, consumer, level, answerable, new, open) by an
agent that did not write it. A Task Block's Question is a topic: the asks inside it are its
Tasks' Runs.

| test | asks | when | source |
|---|---|---|---|
| T0 Signed | the question, what we expect and what would answer it are written and signed before its Tasks run | step 1 | preregistration (Nosek et al. 2018) |


3 · Steps 2 to 5 in depth: the Run methods
------------------------------------------

A Task is planned before it is built, its code is read by someone else before it runs, and
only its Ticket writes its Result. In the example, the Task's plan says it reads the
extract and returns `visits_per_clinic.csv`; the reviewer finds a filter that drops
visits with no clinic; the fixed worker runs through its Ticket, which writes the table and
`runtime.yaml`.

| family | method | card |
|---|---|---|
| Run: How is each Result made, and can it be made again? | By contract first | methods/run/01-by-contract-first.md |
| Run: How is each Result made, and can it be made again? | By independent review | methods/run/02-by-independent-review.md |
| Run: How is each Result made, and can it be made again? | By ticket and receipt | methods/run/03-by-ticket-and-receipt.md |
| Run: How is each Result made, and can it be made again? | By declared pipeline | methods/run/04-by-declared-pipeline.md |
| Run: How is each Result made, and can it be made again? | By light result | methods/run/05-by-light-result.md |

| test | asks | when | source |
|---|---|---|---|
| T1 Planned | the Task's plan names what it reads, returns and how it is checked, before its code | step 2 | registered reports (Chambers & Tzavella 2021) |
| T2 Reviewed | a code review by an agent other than the author is recorded before the Ticket runs | step 4 | self-preference of model evaluators (Panickssery et al. 2024) |
| T3 Receipt | the Run's receipt is complete and every required Result file exists | step 5 | reproducible computational research (Sandve et al. 2013) |
| T4 Generated | no file in a Result was changed after its Ticket wrote it | step 5 | provenance records (Moreau & Missier 2013) |
| T5 Light | a Result holds the light files; heavy output sits in its store, with a pointer | step 5 | good enough practices (Wilson et al. 2017) |

In the example, T2 fails if the reviewer is the agent that wrote the filter, and T4 fails
if someone fixes a count in `visits_per_clinic.csv` by hand instead of rerunning the Ticket.


4 · Steps 6 to 8 in depth: the Report methods
---------------------------------------------

The answer is written from exact Results, not from memory of a notebook: each claim in the
report names the Result it came from, and the report records when it read them. An agent
that wrote nothing in the report checks it; a person releases it.

| family | method | card |
|---|---|---|
| Report: How does the answer reach the reader, checked? | By report from results | methods/report/01-by-report-from-results.md |
| Report: How does the answer reach the reader, checked? | By independent check | methods/report/02-by-independent-check.md |

| test | asks | when | source |
|---|---|---|---|
| T6 Cited | every claim in the report names the exact Result it came from | step 7 | notebook reproducibility (Pimentel et al. 2019) |
| T7 Fresh | no cited Result is newer than the report's recorded reading of it | step 7 · step 8 | (ours) |
| T8 Independent | an agent that did not write the report checks it | step 8 | self-preference of model evaluators (Panickssery et al. 2024) |

In the example, T6 fails if the report says "about 40 clinics" with no Result behind it, and
T7 fails if the Ticket was rerun after the report read its table.


5 · Why it works
----------------

The question comes first
~~~~~~~~~~~~~~~~~~~~~~~~

What a Block asks decides which Tasks are worth running, so the Question is written and
signed before them, with what would count as its answer. A Run that answers no Question
still shows in the workbench, under "Not under a Question", so nothing is hidden.

```
Question     how does the visits extract read?        Logic, signed
   ↓ answered by
Tasks        count visits · list columns · dates       Work, one Ticket each
   ↓ write
Results      tables, figures, receipts                 generated, never edited
   ↓ cited by
Report       Opening · Answer · Evidence · Limits      written, then checked
```

What the evidence says
~~~~~~~~~~~~~~~~~~~~~~

- Fixing the hypothesis and the analysis before seeing results separates confirmation from
  exploration (Nosek et al. 2018).
- Recording how every result was produced, and keeping the exact scripts, is what lets a
  result be made again (Sandve et al. 2013).
- Most public notebooks do not rerun to the same results (Pimentel et al. 2019), so a
  report cites the Results of Tickets, not a notebook's state.
- A model judging text tends to score its own output higher (Panickssery et al. 2024), so
  the author of code or a report never reviews it.
- No study tests this whole loop on agent-run Tasks; its order is our own judgment.


Reference
---------

Terms
~~~~~

| term | means here |
|---|---|
| Block | one `tasks/bNN_<block>/` folder: one workbench, its Questions, Jobs and drawings |
| Job | one `jNN_<job>/` folder: Tasks that share code and defaults (`src/`) |
| Task | one `tNN_<task>/` folder: one contract, its worker, configs and Tickets |
| Run, Ticket | one `runs/rNN_<run>.sh`: runs one config, writes one Result |
| Result, receipt | `results/rNN_<run>/` and its `runtime.yaml`; written only by its Ticket |
| Question, report | a register entry in `board.md` and its Page `reports/qNN_<topic>/` |

| term | 中文 | read more |
|---|---|---|
| Preregistration | 预注册 | [Wikipedia](https://en.wikipedia.org/wiki/Preregistration_(science)) |
| Reproducibility | 可重复性 * | [Wikipedia](https://en.wikipedia.org/wiki/Reproducibility) |
| Data provenance (lineage) | 数据溯源 * | [Wikipedia](https://en.wikipedia.org/wiki/Data_lineage) · [W3C PROV](https://www.w3.org/TR/prov-overview/) |
| Code review | 代码审查 | [Wikipedia](https://en.wikipedia.org/wiki/Code_review) · [中文维基](https://zh.wikipedia.org/wiki/代码审查) |
| Literate programming | 文学编程 | [Wikipedia](https://en.wikipedia.org/wiki/Literate_programming) · [中文维基](https://zh.wikipedia.org/wiki/文学编程) |

Rules
~~~~~

1. One Question is one main topic; its Logic is signed by a person.
2. A Task's code is reviewed by an agent that did not write it, before its Ticket runs.
3. Only a Ticket writes its Result; a wrong Result means fixing the worker or config and
   rerunning the Ticket.
4. A Result stays light; heavy output goes to its store with a pointer.
5. A report's claims cite exact Results; another agent checks it; a person releases it.
