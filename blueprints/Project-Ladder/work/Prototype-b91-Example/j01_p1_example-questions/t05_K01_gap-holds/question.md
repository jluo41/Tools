---
id: K01
level: knowledge
question: is the arm gap the same in the first and second groups?
name: gap by group
ask: Is the gap between arm B and arm A the same in the first and second groups, so that one counsel serves both?
method:
  ask: test
  answer: pool or split
  read: verdict
partitions:
  asked: cross
  not_elsewhere: a test of whether two cuts differ is asked once, on cross; inside one cut there is nothing to pool
  power: none
needs:
  E1: {kind: cite, what: the gap B - A in the first and in the second group, from: I01.E2}
  E2:
    kind: compute
    what: the two groups' gaps, their difference, and the pooling verdict
    pass: three rows (each group's gap and their difference) with intervals, and one verdict word (POOL, SPLIT or UNDETERMINED) with its rule; a difference that cannot be told from zero is never POOL on that alone
    cut: cross
    unit: one group's gap, as I01 wrote it
    measure: the difference of two gaps, in points
    by: group (first against second)
    uncertainty: the gaps' 95% intervals; a z test of their difference
    rivals: none
    output:
      pooling.csv: [part, gap_pp, gap_lo_pp, gap_hi_pp]
      verdict.json: [verdict, test, p_value, rule]
  E3: {kind: judge, what: whether one counsel serves both groups, from: [E1, E2]}
agreed: ✅ 261106
signed: ''
changes:
- {in: p1, change: "narrowed to the pooling test on cross after the plan review returned it (two tests in one need); the replication across the window's halves is dropped"}
---

Gap by group
============

**Why now**: Wisdom may counsel on one population only if the groups' gaps can be pooled.

**What would answer it**: the first and second groups' gaps side by side, their difference with its interval, and a
pooling verdict: POOL, SPLIT or UNDETERMINED.
