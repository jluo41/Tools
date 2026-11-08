---
title: Does the arm gap hold from data freeze 1 to data freeze 2?
level: knowledge
answer-status: answered
reads: the Jobs' answers (I01 and K01 in j01 and j02)
---

# Does the arm gap hold from data freeze 1 to data freeze 2?

## Opening

The same analysis plan ran on two data freezes (j01, j02); only the data moved. This reads the arm gap and the pooling
verdict across the two Jobs.

## Answer

Yes: arm B leads arm A on both freezes, 19 points on data freeze 1 and 15 points on data
freeze 2, with overlapping intervals. With more rows the pooling verdict moved from UNDETERMINED to POOL.

## Evidence

- j01, I01 on full: a gap of 19.1 points (95% 11.5 to 26.8).
- j02, I01 on full: a gap of 15.1 points (95% 8.9 to 21.2).
- K01 on cross: UNDETERMINED in j01, POOL in j02 (j02's reports/vs-j01.md).

## Limits

Data freeze 2 holds every row of data freeze 1, so the two Jobs are not independent samples: this is the same gap
read on more rows, not a replication.

## Next

The next plan's K02 (proposed from j02) tests the gap across the window's halves.
