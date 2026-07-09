1a-descriptions: <intervention name> (anchored data profile, venue-free)
=========================================================================

Date: YYYY-MM-DD
Status: DRAFT
Ladder rung 1a: what the data looks like, every number anchored and dated.
No raw data, no inline computation -- the doc quotes what probes landed.


Datasets
--------

One **DS<n>** per data source: name, scope, where it lives.

- **DS1 - <name>.** <scope in one sentence.> -> `tasks/<task>/` or `discoveries/<topic>/`
- **DS2 - <name>.** <scope.> -> `<pointer>`


Descriptions
------------

One **D<n>** per entry, grouped by dataset: statistic + resolving pointer + as-of date, ONE line each.
Downstream rungs cite these ids (`T1 (D3)`, `C2 (T1; D3)`).

DS1:
- **D1** - <statistic, e.g. cohort N = 128,400> -> `tasks/<task>/results/<file>` (as-of YYYY-MM-DD)
- **D2** - <statistic, e.g. baseline CTR 3.1%> -> `tasks/<task>/results/<file>` (as-of YYYY-MM-DD)

DS2:
- **D3** - <statistic> -> `<pointer>` (as-of YYYY-MM-DD)


Refresh Log
-----------

One dated line per refresh pass: which D ids changed, which downstream entries were stamped `[STALE ...]`.
(May be empty on first pass.)

- YYYY-MM-DD: refreshed D<n> (<why, e.g. iterate backfill vYYMMDD>); stamped <ids or "none">
