# Evidence needs · the one join of Logic, Work and Report

Read when asking, planning, binding, writing or checking any answer on an
InsightBoard. This is the contract that keeps the three columns aligned
(JL 261001: "the biggest issue is that insight question and insight work are
not aligned, and then we have the insight report").

## Why it exists

A question, its work and its report have three different grains: a question
is one ask, a task run computes many groupings for many questions, and one
page may answer several questions. Joined only through the page (register
cell → page → tickets), nothing says WHICH output answers WHICH part of the
ask, and work drifts toward whatever task already exists. Evidence needs make
the join explicit at the grain of the ask, and the work spec makes the work
follow the question rather than the other way round:

```text
LOGIC    register   QK2 · E1 compute + its work spec · E2 judge
            │                     │
WORK     page       answers.yaml  QK2.E1 → results/<ticket>/<spec output file>
            │                     │
REPORT   page       Evidence Item E01-VALUE-… · Need: QK2.E1 → the Bullet → the sentence
```

One id, `<QID>.E<n>`, runs through all three. The question says what would
answer it and how it must be computed before any task is looked at; the work
binds each need to the run that computes exactly that; the page plans one
Evidence Item per need and adopts the sentences that realize it.

## 1 · The needs and their work specs, in the register (Logic)

Under each question's `**What would answer it**:` paragraph, the register
lists its needs, one line each. Every compute need carries its work spec on
the indented lines below it:

```markdown
**The ask**: <the question in one sentence>
**What would answer it**: <one paragraph: the evidence in words>
- E1 · compute · <what a run must produce> · pass: <what a result must show to count>
    cut: <partition> | the cell's partition | cross
    unit: <what one row is, e.g. one sent invitation>
    measure: <the quantity the ask names>
    by: <the grouping or the contrast>
    uncertainty: <the interval or test, e.g. Wilson 95% interval per cell>
    rivals: <the rivals adjusted for, or none>
    output: <file named for the measure>.csv [<column>, …] ; <file>.json [<dotted.key>, …]
- E2 · cite · <what is borrowed from a lower question> · from: QI3.E1
- E3 · judge · <the reading the page must make> · from: E1, E2
**Needs agreed**: ⬜
```

**Hard rules: the question owns its run.** A plan is made for its ask, never
for the tasks that happen to exist. These hold before any binding, and the
check enforces each one mechanically:

```text
1  one run, one question   a run's config lists the needs of ONE question; code may be
                           shared, the run is the question's own, named for its measure
2  coverage adds no need   a phrase of the ask is covered by an existing need, a partial
                           (why it cannot close) or a refusal; a word the needs do not
                           reach is a question for the review (is the ask one thing?),
                           never a reason to add a need. The needs a question's asker
                           wrote are kept; a carried question keeps its needs one for one
3  needs form a logic      each need is one thing, and together they make one argument
                           from the observed to the claim; "one thing" and "a logic" are
                           review tests (haipipe-insight-question GI1 Q1, Q2) that
                           propose a split or a merge for a person to sign
4  propose before search   the drafter writes the run proposal (inputs, the computation
                           in one sentence, the output file and its header) from the
                           register and the extract's column list alone, before reading
                           any task, config or result; the drafter has not read the tasks
5  reuse only identical    an existing run is reused only when it already writes the
                           proposed files and columns and nothing the ask does not name;
                           fitting it by adding a column for another question is a new run
```

A Data or Information ask states no cause ("does X move engagement"). The check
flags a cause word in a Data or Information ask as a review note (Q4 level); the
question review proposes the rewording to an association ("does engagement
differ by X") or a Knowledge successor with its adjusted contrast, and a person
signs it. The ask is never reworded silently.

```text
compute   a number or table a run must produce. Legal at Data, Information and
          Knowledge (a Knowledge compute need is an adjudication test: a gain with
          its uncertainty, an adjusted contrast, a held-out score, a size
          calculation). `pass:` and all seven spec keys are required.
cite      a need already answered for another question, named by its full id
          (`from: QI3.E1`). The cited question's level is one below (Information
          cites Data, Knowledge cites Information, Wisdom cites Knowledge); the
          same level only on a cross page, the board's two exceptions (the cross
          contrast reads mirrored Information, the pooling verdict reads the
          heterogeneity claim).
judge     a reading the page makes from named needs (`from: E1, E2` or full ids).
          Legal at Knowledge and Wisdom only: Data and Information make no claims.
```

- **The spec comes first.** It is written from the ask alone, before any task,
  config or result is opened. It says what the computation IS; whether a task
  already does it is decided afterwards, against the spec.
- **One need, one thing.** Usually one to four per question. A rival a
  Knowledge question names ("…rather than age") is its own compute need (an
  adjusted contrast), never a sentence the page reasons away.
- **`pass:` admits a null.** It says what a result must contain to count as an
  answer (an interval, an adjustment, a held-out split), never which answer it
  must give.
- **Ask words that force a compute need.** "with its uncertainty",
  "interval", "adjusted for", "rather than <rival>", "held-out", "smallest",
  "how much would X gain", "separate A from B", "survive in every stratum":
  each names a computation, so the need is `compute` at its level, whatever
  pages already exist.
- **An extract-level property** (a column inventory, the catalog) is computed
  once for the whole extract: its spec's `cut:` is `the whole extract`, and a
  partition page may bind it.
- **A refusal is computed.** "The extract has no field for this" or "the design
  never varies this" is a compute need whose run shows the absence (a column
  inventory, a probe of the sent text); a refusal read off another page is not
  evidence.
- **Agreement, by an independent agent.** One agent drafts the needs and
  specs; a different agent that did not draft them reviews each against its ask
  (does every forcing word have a compute need, does every spec compute what the
  ask names, does every `pass:` admit a null) and either agrees them,
  `**Needs agreed**: ✅ <YYMMDD>`, or returns fixes to the drafter. No person is a
  gate on the plan. A board is read by the public, so the mark carries the date
  and no name or initials. Agreeing fixes what counts as an answer, and how it is
  computed, before work starts.
- **Frozen once bound.** After the first bound result lands, a need or its spec
  is never edited in place: append `· retired: <reason>` and add a new id.
- A question with no need lines, or a compute need with no spec, is
  **unplanned**: legal on a board made before this contract, reported by the
  check, and closed by planning it.

## 2 · The binding, in the page folder (Work)

Each answering page folder holds `answers.yaml`, authored by the bind step
(`haipipe-insight-bind`), never generated:

```yaml
# answers.yaml · which result answers which evidence need (haipipe-insight ref/evidence-needs.md)
QI4:
  E1:
    ticket: run_bNNjNNtNNrNN_<partition>_<task>
    files: [<spec output file>.csv]
  E2:
    pages: [I03-<partition>]
QK2:
  E1: {ticket: run_bNNjNNtNNrNN_<partition>_<task>, files: [<spec output file>.csv]}
  E2: judge
  E3: {refused: "<why the answer is an absence>", ticket: run_bNNjNNtNNrNN_<partition>_<probe>, files: [<probe table>.csv]}
```

- **The question's own run, or new work.** A compute need binds a run whose
  config serves that question alone (hard rule 1) and that writes exactly the
  proposed files and columns (hard rule 5). An existing task's code may be
  reused through a new config of its own for the question; an existing run of
  another question is never extended to fit. Otherwise a new task is built
  from the proposal (`haipipe-task`, in the level's Job). New computation is
  released when the reviewing agent has agreed the need's spec; the bind step
  never releases its own.
- **compute** binds `ticket` (a file in the page's `runs/`, its result in
  `results/<ticket>/`) and `files`, which include every spec output file. A
  cross page that reads one run per partition binds `tickets: [<ticket>, …]`
  instead; every listed ticket must hold the files. The
  required columns are the spec's; an optional `fields:` list adds more.
- **cite** binds `pages`; omitted, it resolves to the page the register names
  for the cited question on this page's partition.
- **judge** binds the word `judge`.
- **refused** binds a reason AND the probe run that shows it (`ticket`,
  `files`). Legal only on a cell that settles `🟡 … final` or `🚫`.
- **The called config lists the needs it serves**: `answers: [QK2.E1, QI4.E1]`,
  one id per need any page binds to it. It is re-derived from the board's
  `answers.yaml` files (`haipipe-insight-bind` ref/sync_config_answers.py) and
  checked from the need's side; it is never the join.
- One run serves one question's needs, on every page of that question; one
  need binds where its answer is.

## 3 · The report, through the page's Evidence Items (Report)

The answering page is a `haipipe-page` Page Face written through its own flow
(`ref/report.md`). Each compute or cite need becomes Evidence Items in the
page's `draft/<stem>-evidence-items.md`: one item per bound file, every item of
the need carrying the same `**Need**:` id. The plan cites each item from the
Bullet that reads it:

```markdown
### E01-VALUE-<slug> · C2.P2.B1 · <what the item supplies>

- **Need**: QK2.E1
- **Artifact**: `results/<ticket>/<spec output file>` · <the columns read>
- **Expected**: <the need's pass condition>
- **Accept**: <the observable check>
- **Supporting Runs**: Execution · bound · <ticket>
- **Status**: landed
```

- A need is **cited** when a Page sentence realizes (`<!-- realizes: … -->`) a
  Bullet whose Evidence Item carries `**Need**:` with its id. A cite need's item
  names the borrowed id too (`**Need**: QK2.E2 ← QI3.E1`).
- A judge need has no item: its Bullet reads `Evidence: none · judge <QID>.E<n>
  from E1, E2` and a realized sentence makes the reading.
- The item's Artifact names a file the binding binds for that need; the two
  never disagree.
- An inline `[<QID>.E<n>]` tag in a sentence is also read, for pages written
  before this contract; new pages keep ids out of the prose.
- `results-read: <YYYY-MM-DDTHH:MM:SSZ>` in the page header records when the
  writer last read the page's results. A bound result whose `runtime.yaml`
  `ended:` is later makes the page **stale**: its reading is owed again.

## 4 · The check

`haipipe-insight-check` (`ref/check_evidence.py <board>`) reads the registers,
each answering page, its `answers.yaml`, tickets, results, Evidence Items, plan
and text, and the configs the tickets call, and returns one verdict per
register cell that names a page:

```text
OK          every need planned with its spec, bound, fit, cited and current
GAP         a need or spec is incomplete, unbound, its ticket or file is missing,
            its run is not ok, a spec column is absent, its config does not list
            it, its cut is not the page's, a refusal has no probe run, a citation
            is missing, or a kind breaks its level
STALE       a bound result ended after the page's results-read
UNBOUND     the page has no answers.yaml entry for the question
UNPLANNED   the question has no need lines, or a compute need has no spec
```

A cell marked `✅` whose verdict is GAP, STALE or UNBOUND is an **overclaim**:
the check exits 1. UNPLANNED is reported and fails only under `--strict`. The
check is mechanical; a person or a different agent from the page's writer
runs it (make and judge apart). It does not judge the prose: that is the
page's own CHECK (`ref/report.md`).

## 5 · Where each level stands

```text
Data          compute needs; bound to its tickets
Information   compute needs; cite only for the cross contrast (I-from-I)
Knowledge     compute needs for every test its ask or rivals name; cite needs for
              Information it rests on; judge needs for the claim, strength, boundary
Wisdom        cite needs (Knowledge) and judge needs only; a compute need on a
              Wisdom question is misrouted: register a Knowledge successor
```

A Knowledge or Wisdom page with no compute need has no `runs/`. A compute need
answered by reasoning from other pages, because no run exists, is a GAP and
never a WEAK claim.

## 6 · Backfilling a board made before this contract

For each question: plan its needs and specs from the prose
(`haipipe-insight-evidence-plan`), have an independent agent agree them, bind each need on
the answering page (`haipipe-insight-bind`, which commissions any missing run
through `haipipe-task`), sync the configs' `answers:`, rewrite the page through
the `haipipe-page` flow (`ref/report.md`), then run both checks. A cell the
check finds overclaimed drops to `🟡` in the register until its page is
rewritten.
