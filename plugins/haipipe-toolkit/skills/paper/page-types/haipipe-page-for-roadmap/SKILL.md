---
name: haipipe-page-for-roadmap
description: >-
  Paper Page Type for a paper's campaign, PLAN AND INTAKE ON ONE PAGE: cut
  into BLOCKS (one ledger row per block, each block a task group serving a
  named Seed E-row, holding its jobs and their runs, with a done-when, a
  budget, and a person's release before anything runs), then registered lap
  by lap as the receipts come home, closing with settle proposals only the
  Seed may write. Use when planning where to dispatch, releasing a block,
  addressing work as B<n>T<n>r<n>, registering receipts, closing a lap, or
  reading what the campaign still owes. Trigger: roadmap page, block board,
  campaign plan, task group, block job run, lap, register QA, intake,
  page-type roadmap.
metadata:
  version: "0.4.0"
  last_updated: "2026-08-28"
  group-token: "SD"
  outline:
    mode: grammar
    source: "this SKILL.md"
    shape: "division 1 is Mission, division 2 is Block Board; then one division per block B<n> in id order, then one division per lap L<n> in id order; Open is last (R<n> direction ids are grandfathered)"
---

# /haipipe-page-for-roadmap · plan the campaign, register what comes home

Load `haipipe-page` first and `haipipe-page-workflow` when running the Page.
Declare `page-type: roadmap`.

## 🧭 Grain and home

Exactly one Roadmap per paper, minted right after the Seed and EVERGREEN (♻️):
it never closes while any E-row is ⬜/🔨 or any released block is running. It
is the story group's third and last page — the plan and the intake desk are
ONE page, because every released block comes home to the row that sent it:

```text
Paper-<Slug>/0-paperboard/A1-SD-story/
├── SD00-ideation/               where the idea came from
├── SD01-seed/                   what the paper IS · the scoreboard
└── SD02-roadmap/                where to go next AND what came back · THIS PAGE
```

The story group is wholly venue-free; the desk layer starts at the
`A2-NA-narrative/` group. In the journey (haipipe-paper-workflow 0.6.0) this
page is P2 Roadmap (route), the planning-and-intake beat of the P1↔P2
establish loop. Boards with a separate `SD03-collection` page are
grandfathered and fold it into this page only on explicit request.

## 🧱 Three layers, one address (JL 260828)

A campaign has three layers, and they are the task layer's own three, so one
string addresses a folder, a log line and a receipt at once:

```text
🗂 BLOCK  B<n>    one task GROUP      the row on this page · THE RELEASE UNIT
📋 JOB    T<n>    one task FOLDER     listed inside the block's own division
▶️ RUN    r<n>    one CONFIGURATION   the thing that actually executes

   B1T2r3  =  block 1, job 2, run 3 · capital B, capital T, lowercase r
```

**Cut blocks by what GATES them, not by topic.** Blocks are the release unit,
so a good cut makes each block differ in what it costs and what it risks: one
that needs no external access, one that spends real budget, one that is pure
arithmetic over what the previous produced, one that touches a one-shot
resource. Then a person releasing a block is answering one question, not four.
A block spanning an elicitation and two gradings can be neither released nor
budgeted as one thing, which is the defect this grain exists to prevent.

**Fix shared axes once, globally.** When jobs sweep the same axis (datasets,
cohorts, sites), the page declares that index once — `d1`, `d2`, … — so a run
id reads without a legend and the same `d3` means the same thing in every
block. State the axis order inside each job when a job sweeps more than one.

**A block with no run count may not be released**, because a campaign whose
size nobody has stated cannot be budgeted, and the estimate is the machine's
job while the release is the person's.

## 📐 Content outline

```text
### 1 · Mission             🔒 what the paper still owes: the Seed's ⬜/🔨
                               E-rows and §8 open tensions, transcribed as a
                               readable debt list · states the Intake law and
                               scope (which QA banks receipts may come from)
### 2 · Block Board         🔥 the whole campaign in one screen · one row per
                               block
#### 3 · B1 · <slug>        one division per block, in id order · lists that
#### 4 · B2 · <slug>           block's jobs with their run ranges
#### 5 · L1 · <date-slug>   one division per LAP, in id order · the register
### N · Open                🔥 what is still out running · always last
```

## 📊 The Block Board · division 2

One row per block, eight columns, every cell a state and never a blank:

```text
id  block             serves   executor                done-when              budget  status       receipt
──────────────────────────────────────────────────────────────────────────────────────────────────────────
B1  exam corpus       E2 E3    tasks/B1_exam_corpus    every arm carries an   4d      ✅ landed    QA/3-….md
    出卷 · 4 jobs                                      outcome and one tag;   no
    34 runs                                            agreement reported     access
B2  elicitation       E1 E5    tasks/B2_elicitation    222 outputs on disk,   2d +    🔵 running   —
    3 jobs · 222 runs                                  no outcome in any      API
                                                       prompt                 spend
B3  grading           E1 E4    tasks/B3_grading        ΔAUC CI excludes 0     3d      ⬜ proposed  —
    4 jobs · 26 runs                                                          needs B2
```

The id column carries the block id and, under it, its job and run counts, so
the board's one screen also states the campaign's size. A row whose counts are
absent is a row nobody can budget.

Status vocabulary: `⬜ proposed` → `▶️ released` → `🔵 running` →
`✅ landed` / `🚫 dropped` (reason in the division). Dropped rows are never
deleted — the graveyard stops the same dead end being re-planned in new words.
A `—` cell is legal only where the status makes it moot; on a live row every
cell is a state, a path, or a testable sentence.

Column laws:

- **serves** names at least one Seed §6 E-row (or an Ideation pilot
  obligation). A block serving nothing may not be released — the same law
  the design family holds for direction cards: no exploring for exploring's
  sake.
- **executor** is the block's own task-group path, and it lives in the TASK
  LAYER's own home, `examples/<Project>/tasks/{G}{NN}_<name>/`, never inside the
  paper repo (JL 260828, overriding 0.3.0). The symmetry is with discoveries:
  evidence layers are consumer-neutral and a page binds them by path, so a task
  inside the paper would make the paper both the consumer of evidence and its
  executor. WHICH project is decided by the block's INPUTS: a block reading only
  workspace stores belongs to the consuming project, and a block reading another
  project's task outputs is EXTENDED there rather than copied here. The task
  layer's own contract owns everything below the group folder — group naming,
  the four phases and their strict file ownership, the self-serving versus
  consumer-serving mode, and the guardrails — and this page neither restates nor
  overrides it. The row and the task group are the SAME OBJECT seen from two
  sides: this page states why the block exists and when it is done,
  `/haipipe-task` runs it. This page never runs anything.
- **MATCH BEFORE SCAFFOLD** (JL 260828). Before a block's folder is created,
  the sibling projects' `tasks/` are searched for a task group already covering
  the same inputs, and the verdict is written on the block's division as REUSE
  (bind the existing outputs by path and drop the job), EXTEND (add a run there,
  not a copy here) or NEW (nothing covers it). This is the probe family's
  match-before-dispatch law applied one layer down, and it exists because the
  failure it prevents is real and was observed: a block was scaffolded to
  recompute arm-level outcomes that a sibling project's task group had already
  produced months earlier. A block whose division carries no match verdict may
  not be released.
- **done-when** is a testable sentence, not a vibe — it is what G3 reads.
- **receipt** is the QA file path the block landed; the same string appears
  in the lap division that registered it and in the E-row cite that flipped
  on it — one string, on two pages. A block lands one receipt for the block,
  not one per run: run-level detail belongs in the task folder, and a roadmap
  that lists runs as receipts has become a second task board.

## 🧾 A block's own division · one per row

Each block's division lists its jobs, their run ranges, and what the block
would teach. Keep the job list a table of ids, not prose:

```text
jobs   B1T1 <job name>   r1-r6    one run per dataset, d1 through d6
       B1T2 <job name>   r1-r12   dataset-major, then threshold
       B1T3 <job name>   r1-r13   r1-r6 coder one, r7-r12 coder two, r13 reconcile
```

A job whose runs sweep more than one axis states the axis ORDER, because
`r9` must resolve to exactly one configuration for anyone reading the log.
Hazards that would invalidate the block's own output are written here BEFORE
release, not discovered during it; a hazard found after a block runs is a
finding about the plan, and it belongs in this division and the Log.

## ✋ Release is a person's act

A machine proposes rows, estimates budgets and run counts, and recommends
order; only a person flips ⬜ proposed to ▶️ released, BLOCK BY BLOCK, with
initials and date in the block's division. Releasing a block releases every
job in it, which is why the cut matters: a block mixing a free job with an
expensive one forces the person to buy both to get either. Gate G2 (Roadmap
plan → dispatch) reads exactly this: every 🔨/⬜ E-row has a ▶️ row serving it
or an explicit waiver on the Seed's Log. Its receipt Log row lives here: when
the gate passes, this page's Log records the gate, the blocks released, and
who released them.
Dropping a row is as human an act as releasing it.

## 📥 The Intake law · stated in division 1

QA files are the SUBSTANCE of what came back; this page REGISTERS them and
never restates them. A lap line carries paths, ids, and one-line readings —
never copied tables, values, or conclusions, which would make this page a
second evidence authority the family forbids. Anyone wanting the finding
opens the QA file; anyone wanting the paper-grade assertion reads the Seed's
E-row. Division 1 states this law and the campaign's intake scope; a receipt
from outside the named banks is named and explained before it counts.

## 🔁 A lap · one division per batch brought home

One lap = one batch of released blocks dispatched and brought home together.
Each lap division carries four blocks, all register-shaped:

```text
ran        which ▶️ released Block Board rows this lap dispatched (B ids)
cards      the probe/ card ids raised for them (PP<NN>, one per block)
landed     one line per receipt: B id → QA path → one-line reading
settle     the E-flips this lap PROPOSES: E-row id → QA path · the Seed
           writes the flip; this block is a proposal, never the account
```

The join is one string on two pages: the lap's `landed` path = the block
row's receipt cell (this page) = the E-row's cite after the Seed settles
(that page). Gate G3 (lap → Seed) reads a lap: done-when tests hold, every
card binds a landed QA path, and the settle is written on the Seed — its
receipt Log row lives here.

A settle proposal reads discovery verdicts through the shared adapter
(novel → HIGH · partial → MEDIUM · preempted → LOW · inconclusive → stays
⬜), and the intake re-check screens every closest-prior list for this
paper's own preprints and versions, which are never prior art against their
own manuscript unless the Seed rules otherwise.

## 🃏 Dispatch rides the existing probe machinery

This page's `probe/` lane IS the campaign's dispatch surface: one card per
released block, stripped to a neutral Q-executor and handed to the
task/discovery orchestrators exactly as any page's PROBE phase does. Nothing
new is invented — the orchestrators, QA banks, claim rules, and `working`
state discipline all apply unchanged. `/haipipe-task` is what actually runs a
released block: the block's executor path IS the task group it scaffolds, its
jobs become that group's task folders, and its runs become those folders'
configurations. This page states why the work exists and when it is done; it
never scaffolds, never configures, and never reports a number.

A card whose executor died before Report is HELD, never answered: the lap
registers the halt AS a halt and re-dispatches under the executor layer's
reclaim rule. A null result is a COMPLETED search that found nothing; a halt
gathered nothing and rejected nothing, and conflating the two mis-decides
the claim the card serves.

```text
pagex/     binds SD01-seed (the §6 gap list the plan serves and the E-rows
           the settle proposals point at)
probe/     the dispatch cards · one per released block · receipts land here
           first, then are registered on the lap
```

Two pens, never crossed: this page plans and registers; the Seed alone
writes E-row flips.

## ✅ Closing checks

- Division 1 transcribes every current ⬜/🔨 E-row and states the Intake law
  and scope; none is silently missing.
- Every Block Board row has no blank cell; every status is from the fixed
  vocabulary; every ▶️/🔵/✅ row carries a person's release with date.
- Every row's serves column resolves to a real E-row id on SD01-seed §6.
- Every block states its job count and its run count; no row is unbudgeted.
- Every block has a division listing its jobs with run ranges, and every job
  sweeping more than one axis states the axis order.
- Every shared sweep axis is declared once, globally, so a run id resolves
  without a legend.
- Every lap's `ran` ids resolve to ▶️/🔵/✅ Block Board rows; every `landed`
  path exists on disk and matches the block row's receipt cell; no lap line
  restates QA content beyond a one-line reading.
- Every card in `probe/` belongs to a named lap or sits in Open; nothing
  dispatched is unregistered.
- Every settle proposal names a real E-row and the exact QA path; the Seed's
  matching flip (when made) cites the same path.
- Open lists every still-running card; an empty Open beside 🔵 rows on the
  Block Board is a defect on one side or the other.
- Dropped rows are all present with reasons; nothing planned has vanished.
- The page names no venue and contains no manuscript prose.
- The current outline is approved and CHECK closes the built version.

This variant owns no scripts. The generic Page template and workflow own the
frame, plugins, receipts, and lifecycle.
