Method
======

1 · The six steps
-----------------

| step | what happens | methods | where in the workbench | who signs |
|---|---|---|---|---|
| Scope the Block | one topic: its spine and its close condition, and one Job for each inquiry | Scope | Scope › Block, Questions · run Ask a Question | the spine |
| Find the sources | search channels return candidate papers; nothing is filed yet | Find | Work › Papers · run Find papers | none |
| Read one paper per Run | a ticket writes the Result card, facts, receipt and one-entry BibTeX for exactly one paper | Read | Work › Papers · run Read a paper | none |
| Verify the citation | a different agent checks the paper's identity and BibTeX; a person signs what stays unverified | Verify | Check › Citations, Runs · runs Verify a citation, Review a Run | the citation |
| Synthesize the Task | a summary, verdict or landscape written only from the Task's own Results | Synthesize | Work › Tasks · run Synthesize a Task | none |
| Answer the Question | a report Page from the Results; a different agent checks it; the person releases it | Answer | Work › Questions · Check › Reports · Delivery › Reports · runs Write the report, Check a report | the release |

A failed check goes back to the step that owns the fault: a loose topic to Scope, a missing
paper to Find, a wrong fact to Read, a false citation to Verify, a claim with no Result behind
it to Synthesize, an unsupported sentence to Answer. Nothing is fixed in a generated file: a
built report, a Bib or a drawing changes only by rerunning what made it. Every run is in the
Runs panel beside its Space, with the prompt to copy.

One example runs through this page, and it is made up: a team reads the literature on CGM
(continuous glucose monitor) glucose forecasting. The Block is `b03_cgm_forecasting`; one
inquiry is Job `j01_forecast_models`; its Task Page is `t01_transformer_forecasters`; the
Question is "Which model families forecast glucose best 30 minutes ahead?".


2 · Step 1 in depth: scoping the Block
--------------------------------------

A Block is one reading topic of a research Project (`discoveries/bNN_<block>/`), and its
`board.md` header says what it is. In the example, the spine is "what is known about
forecasting CGM glucose with learned models", and the close condition is "every Job has a
verdict and the Question has a released report". Each inquiry is a Job (`jNN_<job>/`). A Job
holds Task Pages; a Task Page is a folder shaped like an article, with a `discovery.yaml`
that says what the Task asks. A Task is often one of three kinds: a verdict (is it true?), a
landscape (what is out there?) or a summary (what does this one source family say?).

| family | method | card |
|---|---|---|
| Scope: How is one literature topic bounded? | By one topic | methods/discovery/01-by-one-topic.md |

| test | asks | when | source |
|---|---|---|---|
| T0 Bounded | the spine and the close condition are written, and each Job asks one inquiry | step 1 | a typology of review types (Grant & Booth 2009) |

In the example, T0 fails if the Block says "CGM" and nothing about when the reading is done.


3 · Step 2 in depth: finding the sources
----------------------------------------

Finding does not file anything. A search channel is one place to look: a database, a
preprint server, a citation graph, a person's reading list. Each channel returns candidate
papers, and the search worker (an agent that only looks) writes down the channel, the query
and the date. A second way to find papers is snowballing: take a paper you already trust, and
follow its reference list (backward) and the papers that cite it (forward). In the example,
the team searches two databases for "glucose forecasting transformer" and then follows the
references of one good paper. Twenty candidates come back; none has a Run yet.

| family | method | card |
|---|---|---|
| Find: How do candidate papers turn up, with the search recorded? | By named channel | methods/discovery/02-by-named-channel.md |
| Find: How do candidate papers turn up, with the search recorded? | By snowballing | methods/discovery/03-by-snowballing.md |

| test | asks | when | source |
|---|---|---|---|
| T1 Search recorded | every channel names its query, its date and how many candidates it returned | step 2 | reporting literature searches (Rethlefsen et al. 2021) |

In the example, T1 fails if the notes say "searched PubMed" with no query and no date.


4 · Step 3 in depth: reading one paper per Run
----------------------------------------------

A Run is one executable ticket, `runs/rNN_<author><year>_<paper>.sh`. Its Result is the
folder with the same name, `results/rNN_<author><year>_<paper>/`. The Run reads exactly one
paper (its Subject). The Result holds four files: a Result card `rNN_<...>.md` (the paper's
title, cite line, subject, venue, verification, then Question and Readout), `facts.md`, the
receipt `runtime.yaml` and, when the paper is a real article, a one-entry `.bib`. In the
example, candidate 7 becomes `r03_lee2022_glucose_transformer`; a link that names three
papers is split into three Runs. The reader answers the Task's Question from that one paper.

| family | method | card |
|---|---|---|
| Read: How does one paper become one filed Result? | By one paper per Run | methods/discovery/04-by-one-paper-per-run.md |

| test | asks | when | source |
|---|---|---|---|
| T2 One paper | each Run has one Subject, and its ticket and its Result share the same name | step 3 | reporting items for one included study (Page et al. 2021) |

In the example, T2 fails if `r03_lee2022_glucose_transformer.sh` reads two papers, or if its
Result folder is called `r03_lee2022/`.


5 · Step 4 in depth: verifying the citation
-------------------------------------------

A card can describe a paper that is not the one cited. The check asks two things: is the
paper real, with this title, authors, year and DOI (digital object identifier, the paper's
permanent number), and does its BibTeX entry say the same? A different agent from the one
that read the paper runs the check. What it cannot confirm stays marked `NEEDS-VERIFICATION`
on the card, and a person signs it or drops it. In the example, the checker finds that the
DOI in `r03` resolves to a different year; it writes that on the card, and the person fixes
the entry.

| family | method | card |
|---|---|---|
| Verify: How is a paper's identity and citation made true? | By citation check | methods/discovery/05-by-citation-check.md |
| Answer: How does the answer reach the reader, checked? | By independent review | methods/discovery/08-by-independent-review.md |

| test | asks | when | source |
|---|---|---|---|
| T3 Citation true | the title, authors, year and DOI of each cited paper match a database record, or the card says NEEDS-VERIFICATION | step 4 | quotation errors in medical papers (Jergas & Baethge 2015) |
| T4 Independent | an agent that did not write the card checks it | steps 4, 6 | self-preference of model evaluators (Panickssery et al. 2024) |

In the example, T3 fails if a BibTeX entry carries a DOI nobody looked up, and T4 fails if the
reader agent also checked its own card.


6 · Step 5 in depth: synthesizing the Task
------------------------------------------

When the Task's Runs are done, one more file closes it: `summary.md`, `verdict.md` or
`landscape.md`. It is written from the Task's own Results only, so each sentence names the
Run it came from, such as "(r03)". It does not add a paper the Task never read. In the
example, `t01_transformer_forecasters` ends with a landscape: three model families, which
papers use each, and where the Results disagree.

| family | method | card |
|---|---|---|
| Synthesize: How do many Results become one finding? | By own Results only | methods/discovery/06-by-own-results-only.md |

| test | asks | when | source |
|---|---|---|---|
| T5 Own Results | every sentence of the synthesis names a Run of this Task, and no unread paper appears | step 5 | search, appraisal, synthesis and analysis as separate steps (Grant & Booth 2009) |

In the example, T5 fails if the landscape lists a model from a paper that has no Run in the
Task.


7 · Step 6 in depth: answering the Question
-------------------------------------------

A Question of the Block is answered by a report Page in `reports/qNN_<topic>/`: Answer,
Evidence, Limits, Next. Its evidence is the Results of the Block's Tasks, each claim naming its
Run. A different agent checks the Page, and the person releases it. In the example, the
report says "transformer models were not clearly better than recurrent ones at 30 minutes",
citing `r03` and `r05`, and lists the papers that stayed unverified under Limits.

| family | method | card |
|---|---|---|
| Answer: How does the answer reach the reader, checked? | By report from Results | methods/discovery/07-by-report-from-results.md |
| Answer: How does the answer reach the reader, checked? | By independent review | methods/discovery/08-by-independent-review.md |

| test | asks | when | source |
|---|---|---|---|
| T6 Cited | every claim in the report names a Run that exists in the Block | step 6 | reporting what was found and from where (Page et al. 2021) |
| T7 Released | an agent that did not write the report checked it, and the person released it | step 6 | self-preference of model evaluators (Panickssery et al. 2024) |

In the example, T6 fails if the report says "most studies agree" and names no Run.


8 · Why it works
----------------

One paper, one place
~~~~~~~~~~~~~~~~~~~~

Review types differ in how they search, appraise and synthesize (Grant & Booth 2009), so a
Block states its type and keeps those three jobs in separate steps. Each paper has one Run
and one Result, so a claim can always be traced to the one paper behind it.

```
Block        b03_cgm_forecasting           spine · close condition
   ↓ holds
Jobs, Tasks  j01 → t01_transformer_forecasters      one inquiry each
   ↓ read, one paper per Run
Results      r03_lee2022_...               card · facts · receipt · .bib
   ↓ checked, then synthesized
Report       Answer · Evidence · Limits · Next      checked, then released
```

What the evidence says
~~~~~~~~~~~~~~~~~~~~~~

- Literature searches are often poorly reported, so a checklist of search items was agreed
  by consensus (Rethlefsen et al. 2021); each channel keeps its query and date.
- Across 28 studies, about one quote in four had an error, and about one in nine a major one
  (Jergas & Baethge 2015), so each citation is checked against a database.
- A chatbot invented 55% of the citations it wrote with one model version and 18% with a
  later one (Walters & Wilder 2023), so a citation the agent wrote is never trusted until it
  resolves.
- A model judging text tends to score its own output higher (Panickssery et al. 2024), so
  the reader of a paper never checks its own card, and the writer of a report never checks it.
- No study tests this whole loop with agents reading papers; its order is our own judgment.


Reference
---------

Terms
~~~~~

| term | means here |
|---|---|
| Block | one `discoveries/bNN_<block>/` folder: one reading topic and its workbench |
| Job | one inquiry of a Block: a folder `jNN_<job>/` that holds Task Pages |
| Task Page | `jNN/tNN_<task>/tNN_<task>.md`: an article-shaped Page Folder with `discovery.yaml` |
| Run | one ticket `runs/rNN_<author><year>_<paper>.sh` that reads one paper |
| Result | the folder `results/rNN_<...>/` with the same name as its Run |
| Result card | `rNN_<...>.md`: title, cite, subject, venue, verification, Question, Readout |
| Receipt | `runtime.yaml`: what ran, when, and with what status |
| Subject | the one paper (or source) a Run reads |
| Synthesis | the Task's closing file: `summary.md`, `verdict.md` or `landscape.md` |
| Question, report | a register entry in `board.md` and its Page `reports/qNN_<topic>/` |

| term | 中文 | read more |
|---|---|---|
| Systematic review | 系统综述 * | [Wikipedia](https://en.wikipedia.org/wiki/Systematic_review) |
| Literature review | 文献综述 * | [Wikipedia](https://en.wikipedia.org/wiki/Literature_review) |
| BibTeX | BibTeX 引用格式 * | [Wikipedia](https://en.wikipedia.org/wiki/BibTeX) |
| Digital object identifier | 数字对象标识符 * | [Wikipedia](https://en.wikipedia.org/wiki/Digital_object_identifier) |

Rules
~~~~~

1. One Block is one reading topic; it names its close condition, and each Job asks one inquiry.
2. Finding files nothing: each channel keeps its query and date.
3. One Run reads one paper, and its Result has the Run's name.
4. A different agent checks the citation; a person signs what stays unverified.
5. A synthesis uses only the Task's own Results.
6. A report cites Runs; a different agent checks it; the person releases it.
