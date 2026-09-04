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
  grant: H1        grant: H2        grant: H3
  source: PageX    source: PageX    source: PageX
```


## Drafting rules

1. ASCII wireframe for each panel with dimensions hint.
2. Every panel: type, card-grant anchor, accepted source, refresh cadence.
3. Interaction notes: drill-down targets, filter scope.
4. KPI cards: current value, trend, target/threshold.
5. Charts: axis labels, legend, data granularity.


## Self-review checklist

```
[ ] Every panel has grant anchor + accepted source
[ ] KPI cards have current, trend, target
[ ] Drill-down paths specified
[ ] Refresh cadence noted
[ ] Card id, grant, and exact render version resolve in the Design Folder
```
