s04 · Does the arm gap hold from data-v1 to data-v2
===================================================
view: findings

**Stage:** agreed

**Why:** Does the arm gap hold from data-v1 to data-v2?

**Feeds:** Q01


Q01 · Answer
------------

### Opening

The same analysis plan ran on two data versions (j01, j02); only the data moved. This reads the arm gap and the pooling
verdict across the two Jobs.

### Answer

Yes: arm B leads arm A on both data versions, 19 points on data-v1 and 15 points on data
data-v2, with overlapping intervals. With more rows the pooling verdict moved from UNDETERMINED to POOL.

### Evidence

- j01, I01 on full: a gap of 19.1 points (95% 11.5 to 26.8).
- j02, I01 on full: a gap of 15.1 points (95% 8.9 to 21.2).
- K01 on cross: UNDETERMINED in j01, POOL in j02 (j02's reports/vs-j01.md).

### Limits

Data version 2 holds every row of data-v1, so the two Jobs are not independent samples: this is the same gap
read on more rows, not a replication.

### Next

The next plan's K02 (proposed from j02) tests the gap across the window's halves.


Files
-----

```text
s04-q01-gap-across-data-versions/
└── s04-q01-gap-across-data-versions.md        this face
```


Decided
-------

(none yet: a decision is one line, s04-D01 · <what was decided> (<who> <date>))


Open
----

1. <the first open point>
