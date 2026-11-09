---
id: K02
level: knowledge
question: does the arm gap hold across the window?
name: gap over the window
ask: Does the gap between arm B and arm A hold in both halves of the window, or does it move with the daily drift?
method:
  ask: test
  answer: replicate
  read: verdict
partitions:
  asked: [full]
  not_elsewhere: the halves of one group's window are too thin to read
  power: none
needs:
  E1: {kind: cite, what: the gap on the whole extract, from: I01.E2}
  E2: {kind: cite, what: the daily drift, the rival this test speaks to, from: I02.E2}
  E3:
    kind: compute
    what: the gap in each half of the window and their difference, with a verdict
    pass: three rows (each half's gap and their difference) and one verdict word with its rule
    cut: the whole extract
    unit: one row of the extract
    measure: the gap in points in each half, and their difference
    by: window half
    output:
      halves.csv: [part, gap_pp, gap_lo_pp, gap_hi_pp]
      verdict.json: [verdict, test, p_value, rule]
  E4: {kind: judge, what: whether the gap holds over time, from: [E1, E2, E3]}
agreed: ⬜
signed: ''
source: {from: [proposals/gap-over-the-window.md]}
---

Gap over the window
===================

**Why now**: K01 was narrowed to the pooling test, so nothing tests the gap over time, and I02's drift moved between
the two data versions.

**What would answer it**: the gap in each half of the window, their difference with its interval, and a verdict.
