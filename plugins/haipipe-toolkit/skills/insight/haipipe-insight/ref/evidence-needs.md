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
ask, so a page can cite real files that do not answer its question, and every
gate still passes because every number traces. Evidence needs make the join
explicit at the grain of the ask:

```text
LOGIC    register   QK2 · What would answer it        E1 compute · E2 judge
            │                                           │
WORK     page       answers.yaml  QK2.E1 → results/<ticket>/<file> [fields]
            │                                           │
REPORT   page .md   "… the gain sits at or below zero [QK2.E1] …"
```

One id, `<QID>.E<n>`, runs through all three. The question says what would
answer it before any run exists; the work binds each need to the narrowest
files that answer it; the report cites each need where it answers it.

## 1 · The needs, in the register (Logic)

Under each question's `**What would answer it**:` paragraph, the register
lists its needs, one line each:

```markdown
**What would answer it**: <one paragraph: the evidence in words>
- E1 · compute · <what a run must produce> · pass: <what a result must show to count>
- E2 · cite · <what is borrowed from a lower question> · from: QI3.E1
- E3 · judge · <the reading the page must make> · from: E1, E2
**Needs agreed**: ⬜
```

```text
compute   a number or table a run must produce. Binds to a page ticket and the
          files of its result. Legal at Data, Information and Knowledge
          (a Knowledge compute need is an adjudication test: a gain with its
          uncertainty, an adjusted contrast, a held-out score, a size
          calculation). `pass:` is required.
cite      a need already answered for another question, named by its full id
          (`from: QI3.E1`). Binds to the page(s) that bind that need. The
          cited question's rung is the same or one below (Wisdom cites
          Knowledge; the cross group's two exceptions stand, board-contract.md).
judge     a reading the page makes from named needs (`from: E1, E2` or full
          ids). Binds no file. Legal at Knowledge and Wisdom only: Data and
          Information make no claims.
```

- **One need, one thing.** Usually one to four per question. A rival a
  Knowledge question names ("…rather than age") is its own compute need (an
  adjusted contrast), never a sentence the page reasons away.
- **`pass:` admits a null.** It says what a result must contain to count as an
  answer (an interval, an adjustment, a held-out split), never which answer it
  must give.
- **Ask words that force a compute need.** "with its uncertainty",
  "interval", "adjusted for", "rather than <rival>", "held-out", "smallest",
  "how much would X gain", "separate A from B", "survive in every stratum":
  each names a computation, so the need is `compute` at its rung, whatever
  pages already exist.
- **Agreement.** An agent may draft the needs; a person agrees them:
  `**Needs agreed**: ✅ <initials> <YYMMDD>`. Agreeing fixes what counts as an
  answer before work starts, as the Expected line fixes the prior.
- **Frozen once bound.** After the first bound result lands, a need is never
  edited in place: append `· retired: <reason>` and add a new id. A retired
  need keeps its citations as history and is not checked.
- A question with no need lines is **unplanned**: legal on a board made
  before this contract, reported by the check, and closed by backfilling
  needs from its prose.

## 2 · The binding, in the page folder (Work)

Each answering page folder holds `answers.yaml`, authored by the bind step
(`haipipe-insight-bind`), never generated:

```yaml
# answers.yaml · which result answers which evidence need (haipipe-insight ref/evidence-needs.md)
QI4:
  E1:
    ticket: run_bNNjNNtNNrNN_<partition>_<task>
    files: [<table>.csv]
    fields: [<column the pass condition names>, …]
  E2:
    pages: [I03-<partition>]
QK2:
  E1: {ticket: run_bNNjNNtNNrNN_<partition>_<task>, files: [<table>.csv], fields: [ci_lo_pp, ci_hi_pp]}
  E2: judge
  E3: {refused: "<why no run can produce it here>"}
```

- **compute** binds `ticket` (a file in the page's `runs/`, its result in
  `results/<ticket>/`), `files` (the narrowest files that answer the need:
  `rates_by_weekday.csv`, not the whole result) and optional `fields`
  (columns of a CSV header, or dotted keys of a JSON file, that carry what
  `pass:` names). `fields` is the mechanical fit test.
- **cite** binds `pages`; omitted, it resolves to the page the register names
  for the cited question on this page's partition.
- **judge** binds the word `judge`.
- **refused** binds a reason. Legal only on a cell that settles `🟡 … final` or
  `🚫`; a ✅ cell has no refused need.
- One run may serve many needs and many pages; one need binds where its
  answer is. A task config's `answers:` names the questions its calling pages
  bind, derived from `answers.yaml`; it is a cross-check, never the join.

## 3 · The citations, in the report (Report)

The page cites each need it answers, at the sentence that answers it:

```markdown
One weekday sits <x>pp below the reference day beside the calendar trend [QI4.E1]
(`results/run_bNNjNNtNNrNN_full_<task>/<table>.csv`).
```

- Every bound need of every question the page answers is cited at least once.
- A cite need is cited by its own id or by the id it borrows (`[QI3.E1]`).
- A judge need is cited where the reading is made, after its `from:` needs.
- `results-read: <YYYY-MM-DDTHH:MM:SSZ>` in the page header records when the
  writer last read the page's results. A bound result whose `runtime.yaml`
  `ended:` is later makes the page **stale**: its reading is owed again.

## 4 · The check

`haipipe-insight-check` (`ref/check_evidence.py <board>`) reads the registers,
each answering page, its `answers.yaml`, tickets, results and text, and
returns one verdict per register cell that names a page:

```text
OK          every need planned, bound, fit, cited and current
GAP         a need is unbound, its ticket or file is missing, its run is not ok,
            a field is absent, a citation is missing, or a kind breaks its rung
STALE       a bound result ended after the page's results-read
UNBOUND     the page has no answers.yaml entry for the question
UNPLANNED   the question has no need lines (a board made before this contract)
```

A cell marked `✅` whose verdict is GAP, STALE or UNBOUND is an **overclaim**:
the check exits 1. UNPLANNED is reported and fails only under `--strict`. The
check is mechanical; a person or a different agent from the page's writer
runs it (make and judge apart).

## 5 · Where each rung stands

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

For each question: write its needs from the prose (`haipipe-insight-evidence-plan`),
have a person agree them, bind each need on the answering page
(`haipipe-insight-bind`, which commissions any missing run through
`haipipe-task`), add the citations and `results-read:` to the page, then run
the check. A cell the check finds overclaimed drops to `🟡` in the register
until its page is rewritten.
