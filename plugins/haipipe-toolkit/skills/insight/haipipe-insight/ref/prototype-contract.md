# Prototype and Instance · the question owns its code

Read when making, growing or checking an Insight board of the Prototype kind.
It replaces, for boards made this way, the task Block, the page tickets that
call it, `answers.yaml`, config `answers:` lines and the hand-kept register
grid (`board-contract.md` keeps the older layout for boards made before it).

Why it exists: when the code that answers questions is cut by method (one
"rates" task serving ten questions), each new question is fitted to an
existing run, its spec is written from that run, and a check that compares the
two cannot fail. Here each question carries its own code, so a run can only
answer the question it sits in.

## Two boards

```text
insights/Prototype-Insight-<Topic>/       the design: partitions, questions, code · no data
insights/Instance-Insight-<Dataset>/      one extract read through one Prototype · its pages
```

A Prototype serves every extract that meets its input contract. A new extract
is a new Instance of the same Prototype. A new subject with a different input
is a new Prototype. Prototypes never import each other's questions; a generic
question is copied into a new Prototype at its birth, its origin noted in the
question's log.

## The Prototype

```text
Prototype-Insight-<Topic>/
├── board.md                    board-kind: insight-prototype · the topic
├── 0-Meta/
│   ├── meta.md                 what the extract holds: grain, window, sources, limits
│   ├── partitions.md           every partition, its filter, in order, and why it exists
│   └── thresholds.yaml         shared floors, alphas, seeds · power.smallest_effect_pp
├── 1-Data/
│   ├── rung.md                     the rung's opening, writing rule and law (prose)
│   ├── src/                        functions two or more of this rung's scripts share
│   └── D01-<name>/
│       ├── D01-<name>.md           the question: YAML block, then prose
│       └── scripts/<name>.py       its entry script (SPEC line), helpers beside it
├── 2-Information/I01-<name>/ …
├── 3-Knowledge/K01-<name>/ …
├── 4-Wisdom/W01-<name>/            the question file only, no script
├── studio/                       optional: the Prototype's drawings (the workbench's Prototype › RoadMap Draw)
└── src/                        functions shared across rungs, when two rungs need one
```

- **Question id** = `<L><NN>`, the start of its folder name `<L><NN>-<name>`: L is
  D, I, K or W and the folder sits in that rung's folder (D in `1-Data`, I in
  `2-Information`, K in `3-Knowledge`, W in `4-Wisdom`); NN numbers the
  questions of a rung from 01, once, never reused; `<name>` is a few lowercase
  words joined by `-`. A need is `<L><NN>.E<n>` (`I03.E1`).
- **No B-J-T-R inside a Prototype.** The board is the block, the rung letter the
  job, the question folder the task, an Instance's partition run the run. The run
  rules of `haipipe-task` hold unchanged: one stem for ticket and result, a
  receipt written before the work and finalized after its gate, heavy output in
  `_WorkSpace/ProjectResult/` with a `heavy.yaml` pointer, paths relative to the
  SPACE root, review by an agent that did not write the code.
- A theme inside a board (funnel, time, geography) is a `group:` field, never a
  code folder.

### 0-Meta

```text
meta.md          the meta page: what the extract holds, its grain, window, sources, limits
partitions.md    every partition, its filter, in order (YAML), then the reasons in prose
thresholds.yaml  every shared value (floors, alphas, seeds) and power.smallest_effect_pp
```

```yaml
---
partitions:
  - {name: full, where: []}
  - name: alpha
    where: [{column: <col>, eq: <value>}]
  - {name: cross, of: [alpha, beta]}
---
```

`full` is required and unfiltered. `cross` holds no rows of its own: a cross
run receives every listed partition. Operators: eq, ne, lt, lte, gt, gte,
isin, notin, notna. A filter that selects no rows refuses the run. A partition
may carry `plain:` words; the prose below the YAML says why each partition
exists and how its bounds read.

### The question file (v2)

The question keeps the words its asker wrote. Every field below except the
partitions block and the needs' output map is prose, carried as written.

```yaml
---
id: I03                            # <L><NN>, the start of the folder name
rung: information                  # data | information | knowledge | wisdom
question: who is in the population?          # the short wording a reader scans (the Queue's)
name: Patient Demographics                   # five words or fewer, the folder's <name> in slug form
ask: <the full question, one sentence>
source:                            # where it came from, when it was carried (optional)
  board: ../<old board>            #   register, old id, Gen-1 cell, the old cells and where it stood
  register: MT02-question-information
  id: QI3
  cells: {full: 🟡 I03-full, alpha: 🚫 full-only}
partitions:
  asked: all                       # all | [full, …] | cross
  not_elsewhere: <why>             # required unless asked is all
  power: none                      # or {test: rate_precision | two_proportion | script, outcome: <col>,
                                   #     groups: <col>, alpha, target_power, effect: <pp>, effect_reason: <why>}
needs:
  E1:
    kind: compute
    what: <what a run must produce>
    pass: <what a result must contain to count; admits a null>
    cut: the cell's partition      # | the whole extract | cross
    unit: <what one row is>
    measure: <the quantity>
    by: <the grouping or the contrast>
    uncertainty: <the interval or test, or none: exact counts>
    rivals: <the rivals adjusted for, or none>
    output:
      <file>.csv: [<column>, …]          # columns in order
      metrics.json: [<dotted.key>, …]    # a json file may be shared by several needs
  E2: {kind: cite, what: <what is borrowed>, from: D01.E1}
  E3: {kind: judge, what: <the reading>, from: [E1, E2]}
  E4: {kind: compute, what: …, retired: <why>}   # history: kept, never run, never cited
agreed: ✅ 261002                  # ⬜ until an agent that did not draft the needs agrees them
---

<Name>
======

**Why now**: <why the board asks it now: what waits on it, what it replicates>

**What would answer it**: <the evidence in words, before any need>

**<any other field the register carried>**: <as written>
```

Rules, checked by `haipipe-insight-check` `ref/check_instance.py`: question,
name, ask, Why now and What would answer it are present; every live compute
need has the nine spec fields; kinds are legal at the rung (D compute; I
compute, cite; K compute, cite, judge; W cite, judge); a cite names a live need
one rung below (the same rung only from a cross question); a judge reads live
needs. A need is never edited once a result is bound to it: it gets
`retired: <reason>` and a new id.

**A signed change** (the question review proposes, a person signs) is applied without
editing any carried word in place:

```yaml
# a need replaced: the old need stays, a successor need gets the next id
  E3: {kind: compute, what: …, retired: "split into D05 (signed ✅ 261002)"}
  E5: {kind: compute, what: …, supersedes: E3}
# a question replaced (split, merge, move, reworded ask): the old file stays as history
retired: moved to Information as I19 (signed ✅ 261002)
superseded_by: [I19]                 # [] when nothing replaces it
# the new question names where it came from
source: {from: [D04], signed: ✅ 261002, review: <the review file>}
changes:                             # every signed change to a question, in order
  - {signed: ✅ 261002, change: <the signed line, as worded>}
```

A retired question is asked nowhere, has no live needs, keeps no scripts, and is not on
the workbench; its ids are never reused. New and changed needs start `agreed: ⬜` until an
agent that did not draft them agrees them.

**What the check does not do.** It never adds a need to cover a word of the
ask, and it never rewords an ask. Whether a question is good is the question
review's (`haipipe-insight-question` GI1, Q1-Q7): the check only flags
suspects as notes (Q1 the ask joins two questions, Q2 a need no judge reads,
Q4 a cause word in a Data or Information ask, Q6 two questions compute the same
table). A reviewer proposes keep, split, merge or move; a person signs a
change; the old question is retired with a reason, never edited in place.

**Can it generalize to a partition?** `partitions:` answers it in two halves,
both written before any result exists:

```text
meaning   logic: inside a partition, is it the same question? A question about the
          extract itself (full-only) or about whether to segment (defer) is asked on
          full only, with not_elsewhere saying why; a field constant inside a
          partition is reported as untestable, never dropped
power     data: can this partition's rows answer it? The runner computes the minimum
          detectable effect (MDE) from the partition's n and base rate, BEFORE any
          outcome contrast; answerable when the MDE is at most the smallest effect,
          the board-wide thresholds.yaml power.smallest_effect_pp unless the question
          sets power.effect with its reason
```

Never judge a partition by whether its result is still significant: that
selects partitions by their outcome, and a difference in significance is not
a significant difference. The page reports each partition's estimate with its
interval; whether partitions differ is a cross question.

### Making a Prototype from a register board

A board made the register way (`board-contract.md`) already holds its
questions' meaning. Carry it, never redraft it:

```text
1  carry     ref/carry_over.py <old board> <Prototype> --report <md>
             writes board.md, 0-Meta (meta, partitions, thresholds), each rung's rung.md
             (the register's Opening, Queue and Law) and one question file v2 per
             register division, word for word; ids Q<L><n> → <L><NN>; a LOGIC refusal
             (full-only, defer) is not asked there, a DATA refusal (thin, no measure)
             is asked and the run refuses it again or answers it
2  verify    carry_over.py --check: every field equal and every division rebuilt byte
             for byte from the new file; a second run writes the same bytes
3  review    the question review (Q1-Q7) proposes; a person signs each change
4  scripts   per question, from its live needs: the output files and columns are the
             old ones, so the new results compare with the old board's
```

### The script

```python
"""<L><NN> · <one line>. Writes exactly the question file's output files."""
SPEC = "<L><NN>"                  # the question it answers; the runner checks it
COLUMNS = ["<col>", …]            # the extract columns it reads, or "all" (the filter's are added)

def run(df, ctx):                 # cross questions get ctx.partitions = {name: df} and ctx.full (the whole extract)
    ...
    return {"<file>.csv": table, …}
```

A script reads no path, writes no file, names no dataset and no partition. It
may call `ctx.refuse(reason)` when its probe shows the extract cannot answer
(the cell becomes 🚫 with that reason), and `ctx.constant(column)` to learn
whether a column is constant in this partition, and `ctx.beside(<file>)` for a
file the extract's preparation wrote beside it (its manifest, its data
dictionary); `ctx.extract` is the extract's path. `ctx.wilson`, `ctx.holm` and
`ctx.thresholds` (0-Meta/thresholds.yaml) are provided. Functions two scripts
share sit in the Prototype's `src/` (or a rung's `src/`) and are imported by name; every rung's `src/` is
importable, the question's own rung first, and the receipt follows every module a script imports.

## The Instance

The Instance mirrors the Prototype: the same `0-Meta` and rung folders, the same
question folders at the same paths. A question folder in the Prototype holds the
spec and the template code; in the Instance it holds the working copy of the
code, one run per partition, what each run computed and reported, and the
question's page.

```text
Instance-Insight-<Dataset>/
├── board.md                          board-kind: insight-instance
│                                     prototype: ../Prototype-Insight-<Topic>
│                                     extract: <path under the SPACE root, a .parquet>
├── 0-Meta/status.md                  the question × partition grid, written only by the checker (--write)
├── 1-Data/ … 4-Wisdom/
│   └── <L><NN>-<name>/               the same folder as in the Prototype
│       ├── <L><NN>-<name>.md         THE PAGE: what the question found here, across its partitions
│       ├── draft/                    the page flow's plan, Evidence Items, records/, previous/
│       ├── scripts/                  a copy of the Prototype question's scripts/, free to adapt
│       │   └── prototype.lock        each copied file's sha256 at the copy: the base of every sync
│       ├── runs/
│       │   ├── <partition>.sh        one run ticket per partition the question is asked on
│       │   └── run-<kind>-<MMDD>-<slug>.md   the page's own runs (write, check), from page.py
│       ├── results/<partition>/      what that run computed: runtime.yaml · partition_power.csv ·
│       │                             the spec's files · provenance/ (the exact spec and scripts it ran)
│       └── reports/<partition>/      that run's report.md, generated from its results
```

- **A partition is a run**: `runs/<partition>.sh` writes `results/<partition>/`
  and `reports/<partition>/`; ticket, result and report share the stem.
- **The run report is generated** (`reports/<partition>/report.md`: the
  question, the partition, the status, the power table, and each compute need
  with its pass line and every output file as a table). It is never written by
  hand; rerun the ticket to change it.
- **The page is one per question, one section per partition** (in partitions.md
  order; a partition the question is not asked on has no section), written through the `haipipe-page` flow
  (`ref/write_answer_page.py`, `page.py adopt`, a CHECK by another agent). It
  reads the run reports and results of every partition the question is asked
  on; its Evidence Items name the need (`**Need**: I01.E1`) and the partition's
  file (`results/<partition>/<file>`). A sentence that two partitions differ
  needs a test, so it belongs to a cross question. The header carries
  `question:`, `partitions:` and `results-read:`; there is no `state:` line.
- **A cite** reads the cited question's file by its path from this folder
  (`../../1-Data/D01-<name>/results/full/<file>`).

### Scripts in both boards

The Instance runs its own copy of the scripts; the spec stays in the Prototype
only, so the question and its output files never fork. `scripts/prototype.lock`
records, per file, the Prototype file's sha256 when it was copied.
`ref/sync_instance.py <instance>` compares base, Prototype now and Instance now:

```text
in sync            neither changed since the copy
instance changed   a local adaptation: an agent that did not write it reviews it
                   (--reviewed <file>), then keep it or offer it to the Prototype
prototype changed  an update is waiting: --pull copies it in and moves the base
both changed       a conflict: merge by hand, then --pull --keep-instance
new in prototype   --pull copies it
```

`--diff` prints the Instance file against the Prototype file. Every pull or
local edit makes the affected runs STALE until rerun, and the checker marks a
cell whose scripts differ from the Prototype's with ⚑.

## The run

`runs/<partition>.sh` calls `ref/run_question.py <question folder> <partition>`. In order:

```text
1 resolve   question folder → Instance → Prototype spec; the partition from the ticket's name
2 receipt   results/<partition>/runtime.yaml: running · ticket · extract · sha256 of the spec,
            the Instance scripts, the Prototype scripts, and the shared files the run rests on
            (partitions.md; only the src/ modules its scripts import, followed through their imports;
            only the thresholds.yaml sections its code names, plus power for a powered question);
            provenance/ copies
3 load      COLUMNS + the filter's columns, from the extract board.md names
4 filter    the partition's where (cross: every listed partition)
5 power     partition_power.csv, from n and the base rate, before any contrast;
            not answerable → status refused · reason underpowered
6 script    the Instance copy's run(df, ctx) → tables
7 gate      the files and their columns equal the Prototype spec's output lines; no column
            is a row key the extract carries; no table has a row per input row
8 write     the tables; receipt ok · ended · duration · outputs; reports/<partition>/report.md
```

A gate failure writes no table and leaves the receipt `failed` with the
problem; the report still says so. Heavy output, when a question has any, goes
to `_WorkSpace/ProjectResult/<Project>/insights/<Instance>/<rung>/<question>/<partition>/`.

## Status is computed

```text
—              the Prototype does not ask the question on this partition
🚫 <reason>     the run refused: underpowered (with its MDE), or the probe's reason
🟡             the run is ok, but the page is missing, unchecked, older than the run,
               or cites nothing of this partition
✅ <YYMMDD>     the page's latest CHECK closed CLOSE after this partition's run ended,
               results-read: is not older, and every need is cited
STALE          the spec, the Instance scripts, 0-Meta's partitions or thresholds, or a
               src/ module the scripts import changed since the run (sha256)
⚑ (suffix)     the Instance scripts differ from the Prototype's
```

A page CHECK is run by an agent that did not write the page, read-only; its
verdict is recorded with `ref/record_check.py <page> <VERDICT> <review file>`,
which opens and closes the page's check Run and, on CLOSE, approves the plan
(a v0 plan is promoted to v1.0).

Nobody types a cell. `haipipe-insight-check` `ref/check_instance.py <instance>`
prints the grid, the notes and the problems (`--write` also writes
`0-Meta/status.md`), and exits 1 on any problem; with `--strict`, also on any
🟡, STALE or waiting Prototype update.
