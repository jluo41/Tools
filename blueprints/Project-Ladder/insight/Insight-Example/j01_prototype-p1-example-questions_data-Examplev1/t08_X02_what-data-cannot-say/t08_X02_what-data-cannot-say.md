---
question: X02
answer-status: answered
answer: It cannot say whether the groups differ (the difference spans -21 to +12 points); group_3 was refused for power; and it covers only 10 days.
how-sure: 'these limits are exact: counts, a refused cut and an interval'
check: ✅ 261106 · another agent
figures:
- name: gap-by-group
  title: The groups' gaps cannot yet be told apart
  kind: dots
  table: t05_K01_gap-holds/runs/r04_cross/result/pooling.csv
  label: part
  value: gap_pp
  low: gap_lo_pp
  high: gap_hi_pp
  zero: no gap
  axis: gap B - A, points
results-read: '2026-11-06T18:59:05Z'
goal: In plain words, what can the example data not say, and which cut or question shows the limit?
---

# X02 · what data cannot say

**The ask**: In plain words, what can the example data not say, and which cut or question shows the limit?

What the example data cannot say, read before acting on what it does.

## Answer

- The window is 10 days of made-up rows (D01 · t01).
- The small group: group_3 was refused for power (I01 · t03).
- The pooling test gives UNDETERMINED (K01 · t05).

## What it rests on

- The extract's size and window (D01 · t01).
- Each cut's arm rates, and the cut refused for power (I01 · t03).
- The pooling test (K01 · t05).
