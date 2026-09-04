# Venue: Dashboard

Data-rich provider-facing dashboard. Multiple panels, charts, KPIs,
action lists. The most complex venue in this reference family.


## Constraints

- **Layout:** multi-panel (summary → detail → action)
- **Data:** real-time or near-real-time refresh
- **Interaction:** drill-down, filter, sort
- **Audience:** typically clinician/provider or executive


## Design profile

```yaml
design_profile:
  evidence_bar: full
  narrative: required
  display: required
  section_edit: required
  terminal: accepted
```

## Phase use

### D1/D2 · bet and realize

Every panel, KPI, chart, and action maps through the released card grant and an
accepted data-source contract. A load-bearing gap is preserved for D4 EMIT;
Design does not Probe it locally.

### D2 · drill-down narrative
Drill-down arc:
- Level 1: Summary KPIs (headline answer)
- Level 2: Detail panels (supporting evidence)
- Level 3: Action items (what to do about it)

### D2 · display requirement
Display map: each panel/widget gets a type (metric-card, line-chart,
bar-chart, table, action-list), a per-unit Job ("show current vs target"),
a grant anchor, and an accepted data source Folder. The per-unit Job is the
absorbed minimap concern.

### D2 · section pass
Dashboard copy settles to final wording: panel titles, KPI labels,
action-list phrasing, drill-down captions.

### D3/D4 · judge and decide
Dashboard spec document with panel layouts, widget specs, data
bindings, and interaction rules. Judge every visible metric and interaction,
render through `delivery/render/`, then accept or emit. Executable build work,
when commissioned, belongs to a downstream Task Folder.
