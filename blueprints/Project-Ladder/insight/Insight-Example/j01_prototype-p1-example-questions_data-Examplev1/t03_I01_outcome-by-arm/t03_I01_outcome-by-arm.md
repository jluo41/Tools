---
question: I01
answer-status: answered
answer: Arm B's outcome rate is 19 points above arm A's on the whole extract (50% against 31%), and B leads in every cut that could be read.
how-sure: Wilson intervals per arm; the gap's interval excludes zero on full
check: ✅ 261106 · another agent
takeaways:
  full: 'Arm B 50% against arm A 31%: a gap of 19 points (95% 11 to 27).'
  first: 'Arm B 51% against arm A 31%: a gap of 20 points (95% 10 to 30).'
  second: 'Arm B 51% against arm A 35%: a gap of 16 points (95% 3 to 29).'
  third: 'Refused for power: its 40 rows cannot detect a 20-point gap (the smallest it could detect is 43 points); the refusal is the answer on this cut.'
results-read: '2026-11-06T18:58:28Z'
goal: In each cut, what is the outcome rate in arm A and in arm B, and how wide is the gap between them?
---

# I01 · outcome by arm

**The ask**: In each cut, what is the outcome rate in arm A and in arm B, and how wide is the gap between them?

Each arm's outcome rate and the gap between them, cut by cut.

## Full

Arm B 50% against arm A 31%: a gap of 19 points (95% 11 to 27).

- Arm A: 87 of 282 rows, 30.9% (95% 25.7 to 36.5) (r01_full · rates_by_arm.csv).
- Arm B: 159 of 318 rows, 50.0% (95% 44.5 to 55.5) (r01_full · rates_by_arm.csv).
- The gap B - A is 19.1 points (95% 11.5 to 26.8) (r01_full · gap.csv).

## First

Arm B 51% against arm A 31%: a gap of 20 points (95% 10 to 30).

- Arm A: 51 of 166 rows, 30.7% (95% 24.2 to 38.1) (r02_first · rates_by_arm.csv).
- Arm B: 94 of 184 rows, 51.1% (95% 43.9 to 58.2) (r02_first · rates_by_arm.csv).
- The gap B - A is 20.4 points (95% 10.3 to 30.4) (r02_first · gap.csv).

## Second

Arm B 51% against arm A 35%: a gap of 16 points (95% 3 to 29).

- Arm A: 35 of 100 rows, 35.0% (95% 26.4 to 44.7) (r03_second · rates_by_arm.csv).
- Arm B: 56 of 110 rows, 50.9% (95% 41.7 to 60.1) (r03_second · rates_by_arm.csv).
- The gap B - A is 15.9 points (95% 2.7 to 29.1) (r03_second · gap.csv).

## Third

Refused for power: its 40 rows cannot detect a 20-point gap (the smallest it could detect is 43 points); the refusal is the answer on this cut.
