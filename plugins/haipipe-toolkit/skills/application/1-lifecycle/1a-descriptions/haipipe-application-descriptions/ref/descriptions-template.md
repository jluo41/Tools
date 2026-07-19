1a-descriptions: <intervention name> (anchored data profile, venue-free)
=========================================================================

Date: YYYY-MM-DD
Status: DRAFT
Ladder rung 1a: what the data looks like, every number anchored and dated.
No raw data, no inline computation -- the doc quotes what probes landed.



Dataset
-------

The data this profile draws on -- one source, several files, or a whole folder; list what's here.

- <name / file / folder> -- <scope in one sentence> -> `tasks/<task>/` or `discoveries/<topic>/`
- <name / file / folder> -- <scope> -> `<pointer>`


Coverage
--------

The breadth floor: each facet is filled (list the short ids, e.g. D1, D3) or waived with a one-line why.
Waivers are the reservoir -- the next round's DRAFT re-mines them.

- cohort (N, demographics): <D ids | waived -- why>
- arms/treatments (variants in play): <D ids | waived -- why>
- outcomes (base rates, all outcome vars): <D ids | waived -- why>
- time window / seasonality: <D ids | waived -- why>
- data quality (missingness, field coverage): <D ids | waived -- why>
- benchmark (segment vs population / external): <D ids | waived -- why>


Descriptions
------------

One subsection per described topic; grows every round. Each is a statistic + resolving pointer + as-of date.
Downstream rungs cite each by its short id (Description 3 -> D3): `T1 (D3)`, `C2 (T1; D3)`.

## Description 1 · <topic, e.g. cohort size>

<statistic, e.g. cohort N = 128,400> -> `tasks/<task>/results/<file>` (as-of YYYY-MM-DD)

## Description 2 · <topic, e.g. baseline click rate>

<statistic, e.g. CTR 3.1%> -> `<pointer>` (as-of YYYY-MM-DD)


Q-consumer
----------

<Data-profile questions this rung raises. One ## Q-Desc-<n> block each.>

## Q-Desc-1 · <question title>

Ask: <what this question wants to know; one sentence per line.>

Why: <which Description / coverage facet needs it, and what breaks if it stays open.>
## Q-Desc-2 · <question title>

Ask: <what it wants.>

Why: <which slot needs it.>