Table Card: the spec
====================

What `templates/describe_table.py` writes, and why each part is there. The
card is for a person who has never seen the table and reads the first line
and the pictures first.


Order of the card
-----------------

```text
the table     typed `what`; file (SPACE-relative); rows × columns; time span
              of `table.time`; described columns; `made by`; column map
①  grain      typed `row`, then the proof
②  columns    per meaning group: a table and a picture
③  example    a made-up row
④  gotchas    what to watch out for
⑤  feeds      where each column goes
⑥  changes    since `compare_to` (only when the config names one)
```

The order follows the questions a reader asks. Grain comes before columns
because every column's meaning depends on what a row is ("clicked" per
message or per patient?).


① Grain
-------

- `table.row` is a sentence a person types: "one message about one
  prescription". The worker cannot know it.
- `table.grain` is the key that should make each row unique. The worker
  counts it: distinct keys, rows that share a key with another row, and the
  share of rows whose key is unique.
- Candidates tested: the declared key, `table.grain_candidates`, the
  config's `grain_candidates`, and each single column of those keys.
- Exact duplicate rows are counted by hashing every column of every row. When
  the declared key fails, the card says how many rows still repeat it once
  exact copies are dropped: that separates "the export duplicated rows" from
  "the grain is wrong".


② Columns by meaning
--------------------

One table per group, in the dictionary's group order, then `undescribed`:

```text
column · meaning · role · filled_pct · distinct · values
```

- `role`: identifier, time, category, flag, number, text. Typed in the
  dictionary, or inferred from the type and marked `(inferred)`.
- `filled_pct`: rows neither null nor blank. `nonnull_pct` (in columns.csv)
  counts non-null only, which is what `⑥ changes` compares.
- `values`: top 3 values with their share for a category or flag; min,
  median, max for a number; first and last date for a time; lengths for
  text; shape only for identifying columns.
- The group picture has one panel per column with values to show: top
  `top_k` values (share of rows), a histogram up to the 99th percentile, or
  rows per month.


③ The made-up example row
-------------------------

Each value is its own column's most common value (or median, or median date).
Identifying columns show `<column_name>`, text shows `<text, about N chars>`.
The row shows what values look like; the combination may never occur, and
the card says so. An optional typed `table.example_story` reads the row as
one sentence.


④ Gotchas
---------

Computed: declared key repeats, exact duplicates, columns empty in every row,
columns with one value, columns the dictionary does not describe, meanings
typed as a guess (`?...`), dictionary columns absent from this version, and
the change counts of ⑥. Typed: `table.notes` and each column's `notes`.


⑥ Changes since the earlier version
-----------------------------------

Schema and parquet null counts only, so it costs nothing on a large file:
columns added, removed, retyped, or whose non-null share moved 20 points or
more.


Privacy
-------

- Identifying: a group with `identifying: true`, or a column with
  `identifying: true` (a column setting wins over its group).
- An identifying column shows filled share, distinct count, and length range;
  never a value, in the card, the CSVs, the pictures, or the example row.
- A count below `min_cell` shows as `<min_cell>` and its value as
  `(small cell)`.
- Text longer than `max_value_width` shows lengths only.
- The example row is made up; nothing is copied from a real row.


Paths
-----

Everything written or shown is SPACE-relative: the user name and the checkout
folder differ per machine. The Ticket relativizes the executed notebook and
the receipt; the worker writes its own files with `space_rel()`.


Cost
----

One column is read at a time, so a wide table never has to fit in memory.
The duplicate check reads batches of 250,000 rows. DrFirst OptTimeR1Extended
(2.0 M rows × 107 columns, 790 MB) takes about 40 seconds, and twice that
with the executed notebook.
