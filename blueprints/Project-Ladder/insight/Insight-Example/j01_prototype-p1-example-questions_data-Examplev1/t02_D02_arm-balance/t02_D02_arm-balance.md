---
question: D02
answer-status: answered
answer: Arm A holds 40% to 48% of a cut's rows and arm B the rest; group_3 is the smallest group.
how-sure: exact counts in every cut
check: ✅ 261106 · another agent
takeaways:
  full: 'Arm A 47% and arm B 53% of 600 rows; groups: group_1 58%, group_2 35%, group_3 7%.'
  first: Arm A 47% and arm B 53% of 350 rows; one group only (group_1).
  second: Arm A 48% and arm B 52% of 210 rows; one group only (group_2).
  third: Arm A 40% and arm B 60% of 40 rows; one group only (group_3).
results-read: '2026-11-06T19:06:21Z'
goal: In each cut, how many rows does each arm and each group hold, and what share of the cut is each?
---

# D02 · arm balance

**The ask**: In each cut, how many rows does each arm and each group hold, and what share of the cut is each?

Both arms must be present in a cut before a gap between them is read there.

## Full

Arm A 47% and arm B 53% of 600 rows; groups: group_1 58%, group_2 35%, group_3 7%.

- Arm A holds 282 rows and arm B 318 (r01_full · share_by_arm.csv).
- By group: group_1 58%, group_2 35%, group_3 7% (r01_full · share_by_group.csv).

## First

Arm A 47% and arm B 53% of 350 rows; one group only (group_1).

- Arm A holds 166 rows and arm B 184 (r02_first · share_by_arm.csv).
- The cut is one group, group_1, so its group share is 100% (r02_first · share_by_group.csv).

## Second

Arm A 48% and arm B 52% of 210 rows; one group only (group_2).

- Arm A holds 100 rows and arm B 110 (r03_second · share_by_arm.csv).
- The cut is one group, group_2, so its group share is 100% (r03_second · share_by_group.csv).

## Third

Arm A 40% and arm B 60% of 40 rows; one group only (group_3).

- Arm A holds 16 rows and arm B 24 (r05_third · share_by_arm.csv).
- The cut is one group, group_3, so its group share is 100% (r05_third · share_by_group.csv).
