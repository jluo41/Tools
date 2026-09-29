---
name: haipipe-task-for-description
description: >-
  Table-description Task specialist: one Task per stored table produces its
  Table Card, a notebook and a card.md that say what one row is (proven by
  counting), what each column means (typed in a column dictionary, never
  invented), what the values look like (one picture per meaning group), its
  synth_df (one synthetic person's rows in the table, invented values in the
  real columns), what to watch out for, where each column goes, and
  what changed since the earlier version. Works on any parquet table: a raw
  release, a ProcDf, a Record table, an external asset. A raw table in any
  format (CSV, Excel, XML, per-person JSON) gets the same card from its
  full-read Run (description.json), and that Run fails when the card leaves a
  question open. Called by /haipipe-task when task-type=description.
  Trigger: describe a table, table card, what does this table look like, data
  dictionary, column meanings, explain a table, table notebook, what is one
  row, describe every column, synth_df, synthetic patient, synthetic rows.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.4.0"
  last_updated: "2026-09-29"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-task-for-description
===================================

A person opening a table asks five things, in this order: what is one row,
what does each column mean, what do the values look like, what is wrong with
it, and where does it go next. The audit Tasks of a raw Block answer "is the
file healthy?"; this Task answers "what is this table?". Its product is the
**Table Card**: `table_card.md` plus an executed notebook that shows every
table and picture inline.

Two layers, never mixed:

```text
facts     computed by the worker       grain, filled share, distinct values,
                                       typical values, pictures, changes
meaning   typed in the dictionary      what the table is, what one row is,
                                       what each column means, where it goes
```

A column the dictionary does not describe reads `? (not described)`. A meaning
that starts with `?` is a typed guess and counts as unconfirmed. The worker
never writes a meaning.


What every card answers
-----------------------

Whichever way a card is made, it answers these seven questions, in this order.
A card that leaves one open is not finished; say why a question has no answer
("a roster: no event time") rather than leaving it blank.

```text
1 files     which files, how big, how many were read, one file per person or not
2 row       what one row is: the keys that were checked and how often each repeats,
            exact copies of a row, then the sentence those counts support
3 people    the person column, how many people, rows and days per person
4 time      the event-time column, first and last month, rows per year,
            rows dated outside 1990-2026
5 columns   EVERY column: type, role, empty share, distinct values, and what
            the values look like (range, values with counts, or length)
6 links     id and person columns this table shares with other tables
7 flags     what Source has to decide about this table
```

Each column gets one role, and the role decides what the card may show:

```text
role         how it is decided                          what the card shows
empty        no value in any row                        nothing
person       the person column                          people count, never a value
event time   the table's event-time column              first and last month, parse share
time         any other date column                      first and last month, parse share
id           name ends in ID/Id/_id/uuid/guid           length; unique in every row or not
constant     one value in every row                     that value and its count
unit         name has "unit"/"uom", few values          values with counts
flag         yes/no, or only 0 and 1                    values with counts
category     text with at most 50 values, or whole      values with counts
             numbers with at most 10
value        numbers                                    min, 5th pct, median, 95th pct, max, mean
text         anything else                              length only
```

A typed dictionary meaning always wins over the inferred role for reading;
the inferred role only decides what may be shown.


Two ways to make the card
-------------------------

```text
stored parquet table         a describe Task (below): tNN_describe_<table>,
(ProcDf, Record, ext_*,      worker templates/describe_table.py, typed
 a raw release in parquet)   meanings from the column dictionary

raw table in any format      the table's full-read Run writes the card while it
(CSV, Excel, XML, parquet,   reads every row once: description.json in the Run's
 one JSON file per person)   Result, next to the scan; the table's notebook opens
                             with it. No second read of a large file.
```

The full-read route (reference: WellDoc-SPACE Proj01 `b00_rawdata`,
`r07_full_scan` in all 280 scanned tables):

- The card is built batch by batch while the table is read once
  (`code/haiutils/haistep/table_card.py`: `TableCard.feed`, `finish`,
  `check_card`). A reader that works file by file (AI-READI's per-person JSON)
  builds one card per file and merges them; the merge is exact.
- Keys checked, in this order: id-named columns, file-path columns, the
  person, person + event time, and every column together (exact copies). The
  first unique one gives the sentence: "one row is one `BGEntryID`", "one row
  is one person at one `time`". When none is unique the card says which key
  repeats and on how many rows.
- Percentiles come from a uniform sample of 20,000 values per column; min,
  max, mean, counts and months come from every row.
- A drop that ships its own data dictionary (a BIDS-style
  `{column: {description, unit, levels}}` file) names it in the Run config
  (`column_dictionary:`); each column's documented meaning goes into the card.
- The Run fails when `check_card` finds an open question, and its Ticket
  requires `description.json`.
- The table notebook asks one question per section, the card's answers first:
  what one row is, a table of every column, then one small picture per column
  (values by count for categories and flags; a min-to-max range with the median
  for numbers).


Where it sits
-------------

```text
tasks/bNN_<block>/
├── src/column_dictionary.yaml            one dictionary per table family (all versions)
└── jNN_<dataset>_raw/                    or any Job that owns a stored table
    ├── src/describe_table.py             copied from templates/, same in every Job
    └── tNN_describe_<table>/             ONE Task per table
        ├── tNN_describe_<table>.md
        ├── scripts/config/r01_describe_<table>.yaml
        ├── runs/r01_describe_<table>.sh  the Block's canonical Ticket
        ├── notebooks/r01_describe_<table>.ipynb   executed: every section inline
        └── results/r01_describe_<table>/
            ├── table_card.md             the card a person reads
            ├── columns.csv               one row per column: meaning + facts
            ├── grain.csv                 each candidate key, rows that share one
            ├── gotchas.csv               computed or typed in the dictionary
            ├── figures/*.png             column map, grain, one per meaning group
            └── metrics.json              summary.headline
```

- In a raw Block (`b00`), the Task sits beside the audit Tasks of each dataset
  Job. A dataset of many tables gets one Task per table
  (`t11_describe_<table>` onward, as `haipipe-task-for-raw` numbers them); a
  dataset of one wide table gets one Task (DrFirst: `t12_describe_cohort_table`).
- The dictionary lives at the lowest folder that owns every version of the
  table: the Block's `src/` when several dataset Jobs carry the same table.
  One dictionary for all versions means a meaning is typed once.
- Other stores work the same way: the config's `table:` names a ProcDf, a
  Record table, or an `ext_*` asset table instead of a raw file.
- **Server-resident data** (PHI, read only on the server): the profile Run runs
  there and brings back masked metadata only, and an inline server Run brings
  back no executed notebook. The notebooks are then built on the laptop after a
  pull, from those fetched Results and `synth_df`, by the Job's
  `src/build_notebooks.py` (sources `src/table_notebook.py`,
  `src/dataset_notebook.py`, views `src/table_views.py`), into the same
  `<task>/notebooks/<dataset>_<table>.ipynb` and
  `t93_source_handoff/notebooks/<dataset>_overview.ipynb`. They are a view, like
  a board build, not a Run; they are kept out of the cluster's deploy. REACH
  PD2D `b00_rawdata/j51_reachpd2d_v260922_raw` is the reference.


The Table Card, section by section
----------------------------------

Spec and the reasons behind each rule: `ref/table-card.md`. In order:

```text
the table   what it is (typed), file, rows × columns, time span, column map picture
①  grain    "One row is ..." (typed), then the proof: every candidate key's
            distinct count and rows that share a key; exact duplicate rows,
            and what is left once they are dropped
②  columns  one table and one picture per meaning group: meaning, role,
            filled %, distinct, typical values
③  synth_df one synthetic person's rows in this table (§ synth_df below);
            without a typed story, one made-up row of typical values
④  gotchas  grain breaks, duplicates, empty and constant columns, undescribed
            or unconfirmed meanings, dictionary notes
⑤  feeds    which downstream reader (ProcName, CaseFn...) reads each column
⑥  changes  added, removed, retyped, or 20-point fill moves since compare_to
```


synth_df: one synthetic person, at the Task and at the Task type
----------------------------------------------------------------

A column list says what a table can hold; `synth_df` shows what it does hold,
as rows a reader can point at. It is the table's rows for ONE made-up person,
in the real columns and their real order, with invented values (JL 260929).

```text
Task level        every table Task's notebook shows its table's synth_df under
                  "What do one person's rows look like?", right after "What is
                  this table?", then draws those rows the way the table is read
                  (values on their cut-points, events on a time line, periods as
                  bars, months as stacks)
dataset level     the dataset notebook shows the same person through every table:
                  one time line of all her dated rows, and her rows per table
Task type level   this section: every description or raw-profile Task of any
                  Project shows a synth_df; a new dataset types its story once
```

- **One story per dataset**, typed once in the Job's `src/`
  (`synthetic_individual.yaml`, read by `synthetic_individual.py`), so her visit
  ids and days agree in every table that records the same visit. The builder
  fills what follows from the story: ids, each table's own time columns, flags.
- **Invented, never copied or sampled.** No value comes from a real row, so
  `synth_df` is laptop-safe and shareable even for a server-resident PHI table;
  it is never used for a substantive result.
- **Obeys the table's rule.** A row sits in a filtered table only if the rule
  that fills the table would put it there (an HbA1c of 6.1 in a prediabetes
  table, 6.8 in a diabetes one), so the rows teach the rule.
- **Fails on drift.** A story key that is not a column of the table stops the
  build; a story therefore never outlives a schema change silently.
- A dataset with no typed story shows one made-up row of typical values
  (each column's most common value or median; identifying columns show a
  placeholder), still named `synth_df`.

Reference: REACH-SPACE `examples/Project-REACH-PD2D/tasks/b00_rawdata/j51_reachpd2d_v260922_raw/`
(`src/synthetic_individual.yaml`, 28 tables).


Commands
--------

```text
/haipipe-task-for-description scaffold <job> <table>   Task folder, config, Ticket, worker copy
/haipipe-task-for-description seed <dictionary>        fill the dictionary from the tables and seeds
/haipipe-task-for-description run <task>               run the Ticket; read the card back
/haipipe-task-for-description review <task>            check the card against the rules below
```

**scaffold.** Copy `templates/describe_table.py` into `<job>/src/`. Make the
Task folder above. The Ticket is a copy of the Block's canonical Ticket with
`WORKER_NAME="describe_table"`, `RUN_OPERATION="table-description"`, and
`REQUIRED_RESULTS=("metrics.json" "table_card.md" "columns.csv" "grain.csv"
"gotchas.csv")`. Start the config from `templates/r01_describe_table.yaml`.

**seed.** Run `templates/seed_dictionary.py` from the SPACE root with every
version of the table (`--table`), every contract that already states column
meanings (`--seed`: any YAML with `columns: [{name, meaning}]`, such as a
ProcName card), and the group list if one exists (`--groups-from`). It adds
missing columns as `?`, fills `?` from seeds with `source:`, and never
overwrites a typed meaning. Then type the rest from evidence (ETL code,
vendor notes, renamed contract entries) and record `source:` for each. A
meaning you cannot source stays `?` or starts with `?`; ask the data owner.
Format: `ref/dictionary.md`.

**run.** Run the Ticket, then read `table_card.md` and the pictures before
reporting. The headline in `metrics.json` is the one-line answer.

**review.** Every section present; every meaning sourced or marked `?`; no
identifying value, count below `min_cell`, or real row in the card or
notebook; no absolute path anywhere (`grep -rn "/Users/\|/home/"`).


Rules
-----

1. **Grain first, and proven.** The card opens with the typed "One row is"
   and the count that checks it. A key that does not hold says by how much.
2. **Meaning is typed, facts are computed.** The worker never guesses a
   meaning; `?` is shown as `?`.
3. **Privacy floor.** Identifying groups or columns show shape only (filled,
   distinct, length). Counts below `min_cell` (default 11) show as `<11`.
   The example row is made up from typical values. Free text shows lengths.
4. **Pictures carry the reading.** Column map first, then one panel per
   meaning group; the notebook shows each inline, never only as a file.
5. **Paths are SPACE-relative** in the card, the CSVs, the notebook and the
   receipt. The config names paths with `{key}` placeholders filled from the
   Job defaults, plus `{job}` and `{block}`.
6. **One dictionary per table family**, all versions, so a meaning is typed
   once and every version's card reads the same words.
7. **Every column, every time.** The card lists all columns, including the
   empty and constant ones; a table with no rows says so. A notebook that
   only draws what a scanner happened to count is not a description.
8. **A raw table is described from its full read**, never from a sample: the
   400-row sample of a schema pass misjudged how empty 21 of MetaboNet's 37
   columns are.
9. **Every section answers one question, named in its title, answer first.**
   A reader jumps to the question they have ("What is one row?", "Whose data
   is it, and when?", "What does each column hold?", "What should Source watch
   out for?", "How was it read?") and reads the bold first line. A section
   that tells a story instead makes the reader follow it to the end (JL 260927).
10. **Keep only what helps a person read the data.** The page leads with its
   notebook link; a Run or file that only the code needs (file lists, sample
   passes, placeholders for tables a drop lacks) stays out of the reader's way
   (JL 260927).
11. **A notebook is named for what it shows** (`<dataset>_<table>.ipynb`,
   `<dataset>_overview.ipynb`), never after its Run, so two open notebooks never
   share a name. Its cells stay short: the drawing code lives in the Block's
   `src/` (WellDoc: `table_views.py`, `dataset_views.py`) and each cell is one
   call under its question, so the notebook reads from top to bottom (JL 260927).
12. **Every table notebook shows its synth_df**, and every dataset notebook shows
   the same person through all its tables (§ synth_df). A notebook is generated
   from its `.py`: never edit it; change the `.py` and rebuild (JL 260929).


Related
-------

- `haipipe-task-for-raw`: the raw Block (`b00`) these Tasks usually sit in,
  its audit Tasks, and its `t11_profile_<table>` metadata passes; its
  `r07_full_scan` writes the card for raw tables in any format.
- `haipipe-data-raw understand`: the life story of one data point
  (`datapoint-timeline.txt`); the card describes columns, the timeline
  describes when a value becomes visible.
- `haipipe-data-source`: the ProcName contracts whose `columns:` meanings
  seed the dictionary, and which the card's `feeds:` section points to.
- `notebook-cell-python`: the `# %%` script-to-notebook convention the worker
  follows.
