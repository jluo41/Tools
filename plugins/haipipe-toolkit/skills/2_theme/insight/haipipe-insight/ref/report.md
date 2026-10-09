# Report · the answering page is a haipipe-page Page

Read when writing or reading an answer. The report is the third column of the
Insight workbench (Logic · Work · Report; JL 261001): the question asks, the
runs compute, the report says what the answer is.

## What it is

**In an Insight Block the run's report is the report** (JL 261005). The work generates it,
`reports/<run>/report.md`: per need its plain lead lines, its figures, its tables
(`block-contract.md` § Runs, reports and the page). The workbench's Report column shows its
lead lines and opens it. The page below is then the short answer that reads those reports:
the point in plain words (the plain-reader rules below), a figure or a few rounded numbers
where they carry it, and a pointer to each run's report. It never retypes a table the report
already shows; it binds the result file instead.

**Two layouts.** In an Insight Block (`block-contract.md`) the answering page is one per
question, `jNN_<level>/tNN_<name>/tNN_<name>.md`, with one section per run
(`<dataset>_<partition>`, partitions in `meta/partitions.md` order); its runs are
`runs/<run>.sh`, its evidence `results/<run>/` and the generated `reports/<run>/report.md`.
The layout below is a register board's, made before the Block; such boards keep it. The
flow and what Insight adds to the Page Face are the same for both.

On a register board the report IS the answering page: one Page Folder per question per partition
(`<L><NN>-<partition>-<slug>/`), at every level, Data, Information, Knowledge
and Wisdom. There is no separate report file and no Insight page shape. The
page is a `haipipe-page` Page Face and is written through that skill's own
flow; this reference adds only what an answer needs on top of it. The page
folder is also a task folder, so the page sits beside the runs it rests on:

```text
<board>/<n>-<partition>/<L><NN>-<partition>-<slug>/
├── <L><NN>-<partition>-<slug>.md                Page Face: Opening · Content (haipipe-page)
├── answers.yaml                                 each evidence need → its result files (evidence-needs.md § 2)
├── draft/<stem>-draft-v<G>.<S>.md               the plan: Structure · Scratch · Draft (haipipe-page)
├── draft/<stem>-evidence-items.md               one Evidence Item per need (evidence-needs.md § 3)
├── draft/records/<stem>-<record>.md             log, files, context, discussion
├── runs/run_bNNjNNtNNrNN_<partition>_<task>.sh  one ticket per task run it rests on
├── runs/run-check-<MMDD>-<slug>.md              the page CHECK (haipipe-page)
└── results/<ticket>/                            each ticket's result, generated
```

The register cell names the page (`✅ <L><NN>-<partition>`), and the page names
the questions back on its `answers:` line. A page may answer several
questions; the register cell is the join.

## The flow

Every answering page is written the `haipipe-page` way (its `SKILL.md`,
`ref/page-template.md`, `ref/page-checklist.md`; the Board's
`ref/writing-rules.md`; the plan grammar in `workbench-page/ref/plan-grammar.md`):

```text
1 needs      the questions' needs and specs are planned and bound          evidence-needs.md
2 structure  the plan's Structure: one C division per need, Bullets in       haipipe-page structure
             reader order, one Evidence Item per bound file of a need
3 draft      the plan's Draft: one candidate sentence line per Bullet        haipipe-page writing
4 adopt      `page.py adopt <page>` writes the Draft into Content             haipipe-page
5 health     `page.py health <page>` has no FAIL                              haipipe-page
6 check      a page CHECK by an agent that did not write the page            haipipe-page-check-agent
7 evidence   `haipipe-insight-check` finds the cell OK                        haipipe-insight-check
```

The Content is never typed into the `.md` directly: it is adopted from the
Draft. `ref/write_answer_page.py <page> <spec.yaml>` formats steps 2 and 3 from
the writer's spec (Opening, divisions, Bullets with their Drafts and Evidence
Items), archives a page written before this shape and carries its log over;
it writes no prose of its own. The page's process records (aims, states, files, log, discussion) live
in `draft/records/`; a drawing lives in `studio/draw/`. A page made before this
reference keeps its old sections until it is rewritten through the flow.

## What Insight adds to the Page Face

Only these, everything else is `haipipe-page`'s:

- **No personal marks.** A board is read by the public: no page, plan, item or
  register line carries a person's name or initials (no `owner:` line).
- **Agents decide the plan.** On an InsightBoard page the plan's `approved:` is
  set by the independent page CHECK: when that agent returns CLOSE, the plan reads
  `approved: ✅ <YYMMDD HHMM> · CHECK <run name>`. No person ticks it.
- **Several claims on one page.** The header's `strength:` carries the label of
  the first question's claim; every judge division states its own label.
- **Header lines**: `answers: <QID>, …` (the questions it answers),
  `strength: STRONG | MODERATE | WEAK` (Knowledge only), and `results-read:
  <YYYY-MM-DDTHH:MM:SSZ>` (when the writer last read the page's results). The
  `state:` line keeps the state word and open items only; `folder-kind:` names
  the level.
- **An answer-first, plain-word Opening.** The visible paragraph asks the
  question in plain words, defining each term it uses inline, then answers it
  in one or two sentences. No question, need, page or run id appears in it; a
  page may be named after its plain description as a short handle. Interval
  detail stays in Content. The drawer keeps `haipipe-page`'s parts:
  `**Where this Page sits:**` (the neighbouring pages, by what they show),
  `**Why it matters:**` (the consequence for the reader, such as what a design
  can or cannot do), and `**Covered elsewhere:**` (what this page leaves out).
- **Content follows the needs.** One numbered division per need, in need
  order, named by its subject in plain words. A compute or cite need's Bullets
  carry its Evidence Item; a judge need's Bullets carry `Evidence: none · judge
  <QID>.E<n> from …`. A Knowledge page's judge division holds the proposition,
  its strength and the reason, the rivals and the boundary.
- **Figures** come from the bound results (`results/<ticket>/fig_<name>.png`),
  each with its caption line above it, as `haipipe-page` requires.

## Plain-reader rules

The reader is a person who has not seen the data (JL 261004: "as simple and
understandable as possible"). The Content keeps every fact and its trace; these rules
decide how it reads. The workbench and the web delivery show a Page in reader mode: a
subsection's sentences run on as one paragraph and its evidence folds into one Sources
list (🔍 Evidence shows every sentence with its lanes). Word and LaTeX carry the same
paragraphs, subsections and tables.

1. **Lead with the point.** A subsection's first sentence says what it shows in plain
   words, with at most one number.
2. **A list is a table.** Three or more parallel items with counts (column kinds,
   groups, flags, partitions) go in one pipe table under the lead sentence, as the
   lead Bullet's Draft, never one sentence per item. The table exports to Word and
   LaTeX as a real table.
3. **Round in prose.** A percentage to one decimal (two significant figures under 1%),
   a count with its separators. Exact values stay in the results and in tables.
4. **Names only when needed.** A field name appears only where the reader will look it
   up, in backticks; otherwise say what it holds.
5. **Close with what it allows.** A subsection ends with one sentence on what a reader
   can or cannot do with it, at the level's strength: arithmetic consequence below
   Knowledge (a cut on these fields reads under half the rows), never a cause or a
   recommendation.
6. **Short.** At most four sentences besides the table; a fifth fact is a table row or
   another subsection.

The Opening follows rule 3 too. A Page written before these rules keeps its text until
its next writing Run applies them.

## Its runs

- A ticket is a call-through: it sets `RESULT_DIR` to the page's own
  `results/<ticket name>/` and `RUN_TICKET` to itself, then runs the task's own
  ticket in the Project's DIKW Block (`work/b5N_<topic>_dikw/jNN_…/tNN_…/runs/rNN_<dataset>_<cut>.sh`).
- The name is the full task address plus the partition and the task:
  `run_bNNjNNtNNrNN_<partition>_<task>.sh`. Ticket and result share the stem.
- One task run often feeds several pages; each page calls it with its own
  ticket and keeps its own result, so a page never reads a sibling's folder for
  its own evidence.
- A Knowledge page computes whenever its question has a compute need; a page
  whose needs are only cite and judge (every Wisdom page) has no `runs/` of
  its own beyond its Page Runs.
- The run draws its figures: every worker ends with a Look step that saves
  `fig_<name>.png` from the tables it just wrote. Heavy output (a file over
  10 MB, a row-level table) goes to
  `_WorkSpace/ProjectResult/<Project>/<page path>/results/<ticket>/` with a
  `heavy.yaml` pointer in the result.

## Who writes and who checks

The level's folder skill (`haipipe-insight-data`, `-information`,
`-knowledge`, `-wisdom`) owns what the answer must contain; `haipipe-page`
owns how the page is written. A writing agent plans and drafts; a different
agent runs the page CHECK; the register cell settles at GI6 only after both
checks pass. Writing a page never settles a cell by itself.

## Rerunning

A rerun is the page's tickets, run again: `bash <page>/runs/<ticket>.sh`. It
replaces `results/<ticket>/` and reopens the page and everything that cites it:
`haipipe-insight-check` reports the page STALE until its Draft is reread
against the new results, adopted again, and `results-read:` is updated.
Never edit a result by hand; change the task code or config and rerun.
