# Venue: Dashboard

Data-rich provider-facing dashboard. Multiple panels, charts, KPIs,
action lists. The most complex venue in this reference family.


## Constraints

- **Layout:** multi-panel (summary → detail → action)
- **Data:** real-time or near-real-time refresh
- **Interaction:** drill-down, filter, sort
- **Audience:** typically a professional user or an executive


## Design profile

```yaml
design_profile:
  evidence_bar: full
  narrative: required
  display: required
  section_edit: required
```

## Run guidance

### Inputs and generate ③

Every panel, KPI, chart, and action maps through the Job's inputs/ fence (its
manifest) and an accepted data-source contract. A load-bearing gap returns as a named hold;
Design does not Probe it locally.

### generate ③ · drill-down narrative
Drill-down arc:
- Level 1: Summary KPIs (headline answer)
- Level 2: Detail panels (supporting evidence)
- Level 3: Action items (what to do about it)

### generate ③ · display requirement
Display map: each panel/widget gets a type (metric-card, line-chart,
bar-chart, table, action-list), a per-unit Job ("show current vs target"),
    an input anchor, and an accepted data source Folder. The per-unit Job is the
absorbed minimap concern.

### generate ③ · section pass
Dashboard copy settles to final wording: panel titles, KPI labels,
action-list phrasing, drill-down captions.

### verify ④ (another agent)
Dashboard spec document with panel layouts, widget specs, data
bindings, and interaction rules. Judge every visible metric and interaction,
render inside the current Run's result/ for visual checks. A passed verify ④, then t99's rank ⑤ and a person's release, put
the exact spec in delivery/. Executable build work belongs to a downstream Task Folder.
