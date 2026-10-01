# Report · the answering page says what its own results show

Read when writing or reading an answer. The report is the third column of the
Insight workbench (Logic · Work · Report; JL 261001): the question asks, the
runs compute, the report says what the answer is.

## What it is

The report IS the answering page's `.md`: one page per question per partition
(`<L><NN>-<partition>-<slug>/<L><NN>-<partition>-<slug>.md` answers one
question on one partition, e.g. an `I<NN>-full-<slug>.md` page answers a QI on `full`). There is
no separate report file. The page folder is also a task folder, so the page
sits beside the runs it rests on and their results:

```text
<board>/<n>-<partition>/<L><NN>-<partition>-<slug>/
├── <L><NN>-<partition>-<slug>.md                the page = the report
├── answers.yaml                                 which result file answers which evidence need
├── runs/run_bNNjNNtNNrNN_<partition>_<task>.sh  one ticket per task run it rests on
└── results/run_bNNjNNtNNrNN_<partition>_<task>/ that ticket's result: tables,
                                                 metrics.json, fig_*.png, runtime.yaml
```

The register cell names the page (`✅ <L><NN>-<partition>`), and the page names the question
back (`answers QI2` on its state line). A page may answer several questions
(one Knowledge page may answer QK2, QK3 and QK4); the register cell is the join.

## Its needs

The page answers the evidence needs its questions list (`evidence-needs.md`).
`answers.yaml` binds each need: a compute need to a ticket, the narrowest files
of its result and the fields its `pass:` names; a cite need to the page that
binds the borrowed need; a judge need to `judge`. The text cites each need
`[<QID>.E<n>]` at the sentence that answers it, and `results-read:` records
when the writer last read the results. `haipipe-insight-check` reads all three.

## Its runs

- A ticket is a call-through: it sets `RESULT_DIR` to the page's own
  `results/<ticket name>/` and `RUN_TICKET` to itself, then runs the task's own
  ticket in the Project's DIKW Block (`tasks/b5N_<topic>_dikw/jNN_…/tNN_…/runs/rNN_<dataset>_<cut>.sh`).
- The name is the full task address plus the partition and the task:
  `run_bNNjNNtNNrNN_<partition>_<task>.sh`, e.g. `run_b5Nj21t01r02_alpha_rates.sh`. Ticket and result share the stem.
- One task run often feeds several pages (one rates run on `full` may feed
  a Data page, several Information pages and the cross contrast): each page calls it with its own ticket and keeps
  its own result, so a page never reads a sibling's folder for its own evidence.
- A Knowledge page computes whenever its question has a compute need; a page
  whose needs are only cite and judge (every Wisdom page) has no `runs/`.
- The run draws its figures: every worker ends with a Look step that saves
  `fig_<name>.png` from the tables it just wrote, so a figure never shows a
  number the tables do not hold. Heavy output (a file over 10 MB, a row-level
  table) goes to `_WorkSpace/ProjectResult/<Project>/<page path>/results/<ticket>/`
  with a `heavy.yaml` pointer in the result.

## Shape

```markdown
# <headline: the finding, in plain words>

state: ✅ SETTLED · answers QI2 · <one-line reading>
page-type: information
owner: <owner>
runs: run_b5Nj21t01r01_full_rates, run_b5Nj21t02r01_full_contrast
results-read: <YYYY-MM-DDTHH:MM:SSZ>

## Opening
<the question, then the answer in one or two sentences carrying the key numbers>

## Content
<the evidence: each number cited as results/<ticket>/<file> with its need [QI2.E1], the figure that
shows it embedded as ![caption](results/<ticket>/fig_<name>.png), nulls and
contradictions, the limit>
```

- **headline** states the finding ("Segment beta responds at half the rate"), not the
  topic ("Engagement over time").
- **runs:** names every ticket whose results the page reads; **results-read:**
  when it last read them. A result that ended later makes the page stale.
- Every bound need is cited `[<QID>.E<n>]` at least once.
- Every number traces to a file in one of those results. A `run receipt` line
  cites `results/<ticket>/runtime.yaml`.
- A Knowledge page states its strength (STRONG, MODERATE or WEAK) and cites the
  Information pages it rests on; a Data or Information page asserts no strength.

## Who writes it

The level's folder skill (`haipipe-insight-data`, `-information` or
`-knowledge`, which also writes the pooling verdict) reads the page's results,
or for Knowledge the pages below it, and writes the page. The register cell
still settles at GI6; writing a page does not settle a cell by itself.

## Rerunning

A rerun is the page's tickets, run again: `bash <page>/runs/<ticket>.sh`. It
replaces `results/<ticket>/` and reopens the page and everything that cites it:
`haipipe-insight-check` reports the page STALE until it is reread and its
`results-read:` updated.
Never edit a result by hand; change the task code or config and rerun.
