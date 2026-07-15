1a-descriptions: <intervention name> (anchored data profile, venue-free)
=========================================================================

Date: YYYY-MM-DD
Status: DRAFT
Ladder rung 1a: what the data looks like, every number anchored and dated.
No raw data, no inline computation -- the doc quotes what probes landed.
How to use: copy to `<intervention>/0-lifecycle/1a-descriptions/1a-descriptions.md`, replace every `<...>`, delete unused sub-items (the DRAFT worker does this during the stage's DPRC).



Datasets
--------

One **DS<n>** per data source: name, scope, where it lives.

- **DS1 - <name>.** <scope in one sentence.> -> `tasks/<task>/` or `discoveries/<topic>/`
- **DS2 - <name>.** <scope.> -> `<pointer>`


Coverage
--------

The breadth floor: each facet is filled (list the D ids) or waived with a one-line why.
Waivers are the reservoir -- the next round's DRAFT re-mines them.

- cohort (N, demographics): <D ids | waived -- why>
- arms/treatments (variants in play): <D ids | waived -- why>
- outcomes (base rates, all outcome vars): <D ids | waived -- why>
- time window / seasonality: <D ids | waived -- why>
- data quality (missingness, field coverage): <D ids | waived -- why>
- benchmark (segment vs population / external): <D ids | waived -- why>
- field disposition: `_DESCRIPTIONS/DS<n>_<name>.md` -- 100% of the schema dispositioned (profiled | waived | excluded) as-of YYYY-MM-DD


Descriptions
------------

One **D<n>** per entry, grouped by dataset: statistic + resolving pointer + as-of date, ONE line each.
Downstream rungs cite these ids (`T1 (D3)`, `C2 (T1; D3)`).

DS1:
- **D1** - <statistic, e.g. cohort N = 128,400> -> `tasks/<task>/results/<file>` (as-of YYYY-MM-DD)
- **D2** - <statistic, e.g. baseline CTR 3.1%> -> `tasks/<task>/results/<file>` (as-of YYYY-MM-DD)

DS2:
- **D3** - <statistic> -> `<pointer>` (as-of YYYY-MM-DD)


Probes
------

<This rung's probe roster (cards in _PROBE/, index row in 1-probe-plans/README.md): one line per PP with status.
D-slots reference these via [AWAITING PP<nn>] until the probe lands. Roster must match disk.>

- PP<nn> - <data-profile question> - <status>


Refresh Log
-----------

One dated line per refresh pass: which D ids changed, which downstream entries were stamped `[STALE ...]`.
(May be empty on first pass.)

- YYYY-MM-DD: refreshed D<n> (<why, e.g. iterate backfill vYYMMDD>); stamped <ids or "none">
