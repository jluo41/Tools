---
question: X02
answer-status: answered
answer: It cannot speak for group_3 (group_3 has not been read yet), and it covers only 16 days; the two groups pool (their difference spans -14 to +12 points), but that says nothing of a third group.
how-sure: 'these limits are exact: counts, a refused cut and an interval'
check: ''
figures:
- name: gap-by-group
  title: The groups' gaps can be pooled
  kind: dots
  table: t05_K01_gap-holds/runs/r04_cross/result/pooling.csv
  label: part
  value: gap_pp
  low: gap_lo_pp
  high: gap_hi_pp
  zero: no gap
  axis: gap B - A, points
results-read: '2026-11-06T18:59:07Z'
goal: In plain words, what can the example data not say, and which cut or question shows the limit?
---

# X02 · what data cannot say

**The ask**: In plain words, what can the example data not say, and which cut or question shows the limit?

What the example data cannot say, read before acting on what it does.

## Answer

- The window is 16 days of made-up rows (D01 · t01).
- The small group: group_3 has not been read yet (I01 · t03).
- The pooling test gives POOL (K01 · t05).

## What it rests on

- The extract's size and window (D01 · t01).
- Each cut's arm rates, and the cut refused for power (I01 · t03).
- The pooling test (K01 · t05).
