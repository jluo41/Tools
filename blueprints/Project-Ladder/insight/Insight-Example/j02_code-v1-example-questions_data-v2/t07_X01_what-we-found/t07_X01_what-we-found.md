---
question: X01
answer-status: answered
answer: Arm B's outcome rate is about 15 points higher than arm A's (47% against 32%), on 960 made-up rows.
how-sure: firm on the whole population; the two groups pool
check: ✅ 261106 · another agent
figures:
- name: outcome-by-arm
  title: Arm B's outcome rate is the higher one
  kind: bars
  table: t03_I01_outcome-by-arm/runs/r01_full/result/rates_by_arm.csv
  label: level
  value: rate_pct
  count: k
  of: n
  rows:
    A: Arm A
    B: Arm B
  mark:
    B: best
  axis: outcome rate, %
results-read: '2026-11-06T19:06:23Z'
goal: In one plain line, what did the example find about arm B against arm A?
---

# X01 · what we found

**The ask**: In one plain line, what did the example find about arm B against arm A?

The plain answer a leader reads first.

## Answer

- The gap holds on the whole extract, its interval clear of zero (I01 · t03).
- The two groups share it: one counsel serves both (K01 · t05).

## What it rests on

- Each arm's rate and the gap B - A, cut by cut (I01 · t03).
- The pooling test of the first and second groups (K01 · t05).
