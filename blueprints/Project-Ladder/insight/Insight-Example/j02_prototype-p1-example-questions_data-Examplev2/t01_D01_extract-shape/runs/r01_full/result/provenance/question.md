---
id: D01
level: data
question: what does the example extract hold?
name: extract shape
ask: How many rows, columns and days does the example extract hold, and how much of each column is missing?
method:
  ask: describe
  answer: count
  read: table
partitions:
  asked: [full]
  not_elsewhere: a question about the extract itself; a cut holds the same columns
  power: none
needs:
  E1:
    kind: compute
    what: the extract's size, its window and the share missing in each column
    pass: every column listed with its missing share, zero included; the row and day counts exact
    cut: the whole extract
    unit: one row of the extract
    measure: counts and the share missing
    by: column
    uncertainty: none, exact counts
    rivals: none
    output:
      shape.json: [n_rows, n_cols, n_days, first_day, last_day]
      missing_by_column.csv: [column, null_pct]
agreed: ✅ 261106
signed: ''
---

Extract shape
=============

**Why now**: every later question reads this extract; its size and gaps come first.

**What would answer it**: the row, column and day counts, and each column's missing share.
