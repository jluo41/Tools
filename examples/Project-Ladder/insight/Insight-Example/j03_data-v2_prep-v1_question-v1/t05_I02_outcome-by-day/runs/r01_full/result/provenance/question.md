---
id: I02
level: information
question: does the outcome rate move across the days of the window?
name: outcome by day
ask: Across the days of the window, what is the outcome rate each day, and does it drift up or down?
method:
  ask: compare
  answer: rate
  read: trend
partitions:
  asked: [full]
  not_elsewhere: the window is short; a day-by-day rate inside one group is too thin to read
  power: none
needs:
  E1:
    kind: compute
    what: the outcome rate on each day, with its 95% interval
    pass: every day of the window listed, a day with no rows shown as missing
    cut: the whole extract
    unit: one row of the extract
    measure: the share of rows with outcome 1
    by: day of the window
    uncertainty: Wilson 95% interval
    rivals: none
    output:
      rates_by_day.csv: [level, n, k, rate_pct, ci_lo_pct, ci_hi_pct]
  E2:
    kind: compute
    what: the drift, in points per day, with its 95% interval
    pass: one slope and its interval; a slope whose interval crosses zero is said as no clear drift
    cut: the whole extract
    unit: one day
    measure: the slope of the daily rate, points per day
    by: day of the window
    uncertainty: 95% interval of a least-squares slope, weighted by rows per day
    rivals: none
    output:
      trend.csv: [term, slope_pp, slope_lo_pp, slope_hi_pp]
agreed: ✅ 261106
signed: ''
---

Outcome by day
==============

**Why now**: a gap read over a window means little if the rate drifts a lot inside it.

**What would answer it**: the daily rate with its interval, and one drift per day with its interval.
