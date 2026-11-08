---
id: D02
level: data
question: are the arms and groups the size we expect in each cut?
name: arm balance
ask: In each cut, how many rows does each arm and each group hold, and what share of the cut is each?
method:
  ask: describe
  answer: count
  read: table
partitions:
  asked: all
  power: none
needs:
  E1:
    kind: compute
    what: the rows and share of the cut in each arm
    pass: both arms listed with their counts; an empty arm shown as zero, never dropped
    cut: the cell's partition
    unit: one row of the extract
    measure: rows and their share of the cut
    by: arm
    uncertainty: none, exact counts
    rivals: none
    output:
      share_by_arm.csv: [level, n, share_pct]
  E2:
    kind: compute
    what: the rows and share of the cut in each group
    pass: every group present in the cut listed; a cut of one group says so
    cut: the cell's partition
    unit: one row of the extract
    measure: rows and their share of the cut
    by: group
    uncertainty: none, exact counts
    rivals: none
    output:
      share_by_group.csv: [level, n, share_pct]
agreed: ✅ 261106
signed: ''
---

Arm balance
===========

**Why now**: a contrast between arms is read only once both arms are there in every cut.

**What would answer it**: each arm's and each group's rows and share, cut by cut.
