---
id: D02
level: data
question: are the arms and groups the size we expect in each segment?
name: arm balance
ask: In each segment, how many rows does each arm and each group hold, and what share of the segment is each?
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
    what: the rows and share of the segment in each arm
    pass: both arms listed with their counts; an empty arm shown as zero, never dropped
    cut: the cell's partition
    unit: one row of the extract
    measure: rows and their share of the segment
    by: arm
    uncertainty: none, exact counts
    rivals: none
    output:
      share_by_arm.csv: [level, n, share_pct]
  E2:
    kind: compute
    what: the rows and share of the segment in each group
    pass: every group present in the segment listed; a segment of one group says so
    cut: the cell's partition
    unit: one row of the extract
    measure: rows and their share of the segment
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

**Why now**: a contrast between arms is read only once both arms are there in every segment.

**What would answer it**: each arm's and each group's rows and share, segment by segment.
