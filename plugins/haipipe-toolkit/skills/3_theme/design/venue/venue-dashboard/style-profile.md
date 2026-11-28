# Dashboard Style Profile

Drafting guide for dashboard spec artifacts.


## Voice examples

**Dashboard spec excerpt:**
```
Panel 1: Summary KPIs (top row, 3 cards)
──────────────────────────────────────────
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ <Rate>       │ │ Flagged      │ │ Sent         │
│   78.4%      │ │   4 <items>  │ │   127 / week │
│ ▲ +2.1pp     │ │ ▼ -2 vs last │ │ ▲ +12%       │
│ target: 80%  │ │ threshold: 5 │ │              │
└──────────────┘ └──────────────┘ └──────────────┘
  input: H1        input: H2        input: H3
  source: W/input  source: W/input  source: W/input
```


## Drafting rules

1. ASCII wireframe for each panel with dimensions hint.
2. Every panel: type, released-input anchor, accepted source, refresh cadence.
3. Interaction notes: drill-down targets, filter scope.
4. KPI cards: current value, trend, target/threshold.
5. Charts: axis labels, legend, data granularity.


## Self-review checklist

```
[ ] Every panel has released-input anchor + accepted source
[ ] KPI cards have current, trend, target
[ ] Drill-down paths specified
[ ] Refresh cadence noted
[ ] Job and Task ids, the pinned goal · method · inputs, and the Run's result/ paths resolve
[ ] Any render manifest binds the exact source and picture inside its Run's result/
```
