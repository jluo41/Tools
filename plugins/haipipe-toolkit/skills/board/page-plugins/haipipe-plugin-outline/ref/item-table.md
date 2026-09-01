# The item table · `<stem>-items.md` · one row per evidence mark

The item table is the eighth record kind in `<page>/outline/` (JL 260901: "I
want in the outline plugin to maintain the evidence item table"). It answers
one question the seven other files cannot: **for each thing the plan owes,
where does it come from, how big is the gap, and did a person decide to make
it?** The SURVEY cycle writes the rows, a person writes `Decide`, and the
machine never writes into this file at all: the item's STATUS is derived at
render time and lands in the generated twin, `<stem>-evidence.md`.

```text
<stem>-items.md      AUTHORED   the survey: Need · Route · Run · Decide
<stem>-evidence.md   GENERATED  the same rows joined to the disk: + Has · Status
```

## The law behind the table · every number is answered by a RUN

JL 260901: "evidence is linked to the runs!!!" A run is the atom of evidence:
one real address in the project's `tasks/` tree, config + code + results, and
it carries NO interpretation. The item row points at the run; the run's
results say whether the number exists; the plan's `Answered:` line says whether
the page has used it; and the reading of the number is written only on the
page, at EMBED, under the page's own stake. Nothing in `tasks/` ever says what a
result means, which is exactly why any page may bind to it.

Two lanes are not runs and the table says so in the `Route` column: a 📚
citation is answered by a verified bib entry a person supplies (`person`), and
a 🖼 display is built by its own recipe run from numbers that runs produced.
The discoveries/ tree joins the same grammar later (a discovery folder is the
task, a sweep is its run, `sources.md` its results); until then citations are
`person`.

## The grammar · one record per marked bullet, the folder's one record shape

```text
# <stem> · items
page: <stem>
kind: items · authored · SURVEY writes the rows, a person writes Decide, Status is never here
plan: v<N>                       the plan version the rows were surveyed against
surveyed: YYMMDD HHMM · <who>

### C2.P3.B1 · 📮 S5 · C1: +9.34 MME per visit, comparison owed
- **Need**: the mean per-encounter total MME in the LBP sample, so 9.34 can be read as a share
- **Route**: task
- **Run**: new-run · tasks/R01_Reg_TraitOpioid/D01-reg_visitlbp_1stpair · one descriptive pass, secure server
- **Decide**: ☑ make · JL 260901
> Comment JL · aggregate values only, nothing row-level leaves the server · 260901
```

- **The head is the plan's own words**: `### <address> · <mark> <the bullet's head>`,
  byte-identical to the head `cli/evidence-status.py` prints, so the two files
  join by address and a reader sees the same line in both.
- **One row per mark, no row without a mark.** A bullet with no mark owes
  nothing and gets no row; a mark with no row means SURVEY has not run on this
  plan version, and the render says so.
- **The four labels are fixed, in this order.** A fifth label is a defect;
  the comment lane holds anything else.

## The four columns

```text
label     who writes it   value
──────────────────────────────────────────────────────────────────────────────
Need      SURVEY          one line: exactly what is owed, in the plan's words
Route     SURVEY          task · discovery · bibex · display · pagex
Run       SURVEY          <outcome> · <address> [· <note>]   then LAND appends
                          ` → <result file>` when the material exists on disk
Decide    a PERSON        ☐ make (undecided) · ☑ make · ☑ defer · <reason>
                          · ☑ drop · <reason>   signed `· <who> YYMMDD`
```

**The outcome words**, one per row, authored at SURVEY and then frozen. Each
names how far up the `tasks/` tree the gap sits (block > job > task > run, the
b/j/t/r grammar), so a stranger reads the cost off the word:

```text
found        a run exists AND its results answer the need    LAND binds; nothing to make
rerun        the run exists, results missing or stale         LAND executes it again
new-run      the task exists, no run gives this exact thing   LAND mints one r<NN>_ config
new-task     the job exists, no task computes this            LAND scaffolds t<NN>, then a run
new-job      the block exists, no job covers this             LAND scaffolds j<NN> first
new-block    nothing in tasks/ touches this                   LAND scaffolds b<NN> first
person       a citation, or a number only a person holds      LAND transcribes what you supply
none         no run could ever produce it                     not makeable: the bullet is wrong
                                                              → SHAPE, never Decide = make
```

`add-run`, `borrow`, `new-folder` and the T0-T4 cost ladder were considered and
retired on 260901: a run is the atom, so binding to another page's number is
binding to its run; the level words say the cost; there is nothing to borrow.

**The search order that produces the outcome**, cheapest first, by READING:
this page's own earlier rows → the project's `tasks/` tree by block, job, task,
run (their QA/ digests and `results/` listings are the index) → nothing. A
project with a mature tree should survey mostly `found`; a page whose rows are
all `new-*` says something about the project, not the page.

## The derived status · never in this file

`cli/evidence-status.py` joins every row to the disk and writes the twin file.
One word per row, one emoji, computed from three things: the row's `Run`
address, that run's results on disk, and the plan's `Answered:` line.

```text
state        meaning                                  derived from                  next act
────────────────────────────────────────────────────────────────────────────────────────────
⬜ owed      mark exists, no run bound                 no row, or no address         SURVEY
🔗 bound     the row names a run and you said make    address + ☑ make              LAND
🟢 landed    the bound run's result is on disk        the `→` file exists           EMBED
📌 folded    the plan carries the number              bullet has Answered:          nothing
✅ accepted  the page passed CHECK                     accepted: ✅ on the page      nothing
⚠️ stale     folded, but the result changed since     result newer than the plan    EMBED again
⏸ deferred   Decide = defer                            the row                       you
✖ dropped    Decide = drop                             the row                       none
⛔ blocked   outcome none                              the row                       SHAPE
```

`stale` is the reopen law made visible: a rerun upstream flips a folded row by
mtime alone, so the page never silently carries an old number. A person who
types a status into either file has copied the disk, and the copy is wrong the
moment the disk moves; `check.py`'s `evidence-hand-edited` tooth exists for
exactly that.

## Who writes what, and when

```text
SHAPE    writes no row; marks in the plan are the placeholders
SURVEY   writes every row: Need · Route · Run (outcome + address); a person writes Decide
LAND     appends ` → <result file>` to a row's Run line when the material lands
EMBED    writes the plan's Answered: line; touches this file not at all
render   derives Status into <stem>-evidence.md, never into this file
```

A row is SURVEY-complete when it has its outcome, its address where one exists,
and a signed Decide. The cycle's gate is every row complete. LAND refuses a row
whose Decide is `☐`.
