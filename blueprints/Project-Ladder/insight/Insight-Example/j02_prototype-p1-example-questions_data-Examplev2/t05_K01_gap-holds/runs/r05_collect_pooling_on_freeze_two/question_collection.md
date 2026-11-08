# Gap by group pools

for: Insight-Example.j02-s02:why-answers-moved @ why_answers_moved

The gap-by-group test moved from UNDETERMINED to POOL when data freeze 2 added rows. Two choices follow for the counsel and the next plan.

## Q1 · Counsel scope
The gap-by-group test now pools the first and second groups: the difference's interval lies inside ±20 points.
**Should the next-round counsel on data freeze 2 speak for both groups?**
- [x] A · Yes: one counsel for the first and second groups.
- [ ] B · Not yet: wait for the gap-over-the-window replication.
Why A: POOL is shown, not just a difference too small to see.

## Q2 · Small group
group_3 is refused for power on both data freezes (40 rows, then 68).
**Take the proposed cut joining group_2 and group_3 into analysis plan 2?**
- [ ] A · Take it: read group_3 beside group_2.
- [ ] B · Decline: keep group_3 apart until it grows.
