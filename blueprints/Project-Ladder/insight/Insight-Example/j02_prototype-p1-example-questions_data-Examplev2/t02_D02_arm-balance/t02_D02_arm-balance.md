---
question: D02
answer-status: answered
answer: The arms are close to even in every cut (arm A holds 44% to 50% of a cut), and group_3 is a small share of the rows.
how-sure: exact counts in every cut
check: ✅ 261106 · another agent
takeaways:
  full: 'Arm A 48% and arm B 52% of 960 rows; groups: group_1 56%, group_2 37%, group_3 7%.'
  first: Arm A 47% and arm B 53% of 541 rows; one group only (group_1).
  second: Arm A 50% and arm B 50% of 351 rows; one group only (group_2).
  third: Arm A 44% and arm B 56% of 68 rows; one group only (group_3).
results-read: '2026-11-06T18:58:36Z'
goal: In each cut, how many rows does each arm and each group hold, and what share of the cut is each?
---

# D02 · arm balance

**The ask**: In each cut, how many rows does each arm and each group hold, and what share of the cut is each?

Both arms must be present in a cut before a gap between them is read there.

## Full

Arm A 48% and arm B 52% of 960 rows; groups: group_1 56%, group_2 37%, group_3 7%.

- Arm A holds 459 rows and arm B 501 (r01_full · share_by_arm.csv).
- By group: group_1 56%, group_2 37%, group_3 7% (r01_full · share_by_group.csv).

## First

Arm A 47% and arm B 53% of 541 rows; one group only (group_1).

- Arm A holds 254 rows and arm B 287 (r02_first · share_by_arm.csv).
- The cut is one group, group_1, so its group share is 100% (r02_first · share_by_group.csv).

## Second

Arm A 50% and arm B 50% of 351 rows; one group only (group_2).

- Arm A holds 175 rows and arm B 176 (r03_second · share_by_arm.csv).
- The cut is one group, group_2, so its group share is 100% (r03_second · share_by_group.csv).

## Third

Arm A 44% and arm B 56% of 68 rows; one group only (group_3).

- Arm A holds 30 rows and arm B 38 (r05_third · share_by_arm.csv).
- The cut is one group, group_3, so its group share is 100% (r05_third · share_by_group.csv).
