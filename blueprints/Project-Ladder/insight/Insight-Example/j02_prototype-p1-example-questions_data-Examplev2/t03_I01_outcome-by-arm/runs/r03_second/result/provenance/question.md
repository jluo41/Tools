---
id: I01
level: information
question: how often does the outcome happen in each arm?
name: outcome by arm
ask: In each cut, what is the outcome rate in arm A and in arm B, and how wide is the gap between them?
method:
  ask: compare
  answer: rate
  read: interval
partitions:
  asked: all
  power: {test: two_proportion, outcome: outcome, groups: arm, alpha: 0.05, target_power: 0.8}
needs:
  E1:
    kind: compute
    what: the outcome rate in each arm, with its 95% interval
    pass: both arms with n, k and a Wilson interval; a rate of zero shown, never left out
    cut: the cell's partition
    unit: one row of the extract
    measure: the share of rows with outcome 1
    by: arm
    uncertainty: Wilson 95% interval
    rivals: none
    output:
      rates_by_arm.csv: [level, n, k, rate_pct, ci_lo_pct, ci_hi_pct]
  E2:
    kind: compute
    what: the gap, arm B minus arm A, in points, with its 95% interval
    pass: one row, the gap and its interval; a gap whose interval crosses zero is said as such
    cut: the cell's partition
    unit: one row of the extract
    measure: the difference of two rates, in points
    by: arm B against arm A
    uncertainty: Wald 95% interval of a difference of proportions
    rivals: none
    output:
      gap.csv: [contrast, gap_pp, gap_lo_pp, gap_hi_pp]
agreed: ✅ 261106
signed: ''
---

Outcome by arm
==============

**Why now**: the gap between the arms is what the example is about; every later level rests on it.

**What would answer it**: each arm's rate with its interval, and the gap with its interval, cut by cut.
