# Dashboard Style Profile

Drafting guide for dashboard spec artifacts.


## Voice examples

**Dashboard spec excerpt:**
```
Panel 1: Summary KPIs (top row, 3 cards)
──────────────────────────────────────────
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Refill Rate  │ │ At-Risk      │ │ SMS Sent     │
│   78.4%      │ │   4 patients │ │   127 / week │
│ ▲ +2.1pp     │ │ ▼ -2 vs last │ │ ▲ +12%       │
│ target: 80%  │ │ threshold: 5 │ │              │
└──────────────┘ └──────────────┘ └──────────────┘
  claim: C01       claim: C02       claim: C03
  source: T01      source: T02      source: T01
```


## Drafting rules

1. ASCII wireframe for each panel with dimensions hint.
2. Every panel: type, claim, data source, refresh cadence.
3. Interaction notes: drill-down targets, filter scope.
4. KPI cards: current value, trend, target/threshold.
5. Charts: axis labels, legend, data granularity.


## Self-review checklist

```
[ ] Every panel has claim + data source
[ ] KPI cards have current, trend, target
[ ] Drill-down paths specified
[ ] Refresh cadence noted
[ ] cited_K / cited_W in frontmatter
```
