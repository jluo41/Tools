# Venue: Dashboard

Data-rich provider-facing dashboard. Multiple panels, charts, KPIs,
action lists. The most complex venue — requires all lifecycle stages.


## Constraints

- **Layout:** multi-panel (summary → detail → action)
- **Data:** real-time or near-real-time refresh
- **Interaction:** drill-down, filter, sort
- **Audience:** typically clinician/provider or executive


## Stage requirements

```yaml
stages:
  seed:       required
  pitch:      required
  claims:     required
  narrative:  required
  display:    required
  section-edit:    required

claims_settlement: full
```


## Lifecycle mappings

### → Claims (full)
Full claim ledger. Each panel/KPI/chart must trace to a claim.
GAPs trigger probe plans — you can't show a metric on a dashboard
without evidence that the metric matters.

### → Narrative (required)
Drill-down arc:
- Level 1: Summary KPIs (headline answer)
- Level 2: Detail panels (supporting evidence)
- Level 3: Action items (what to do about it)

### → Display (required)
Display map: each panel/widget gets a type (metric-card, line-chart,
bar-chart, table, action-list), a claim, a per-unit Job ("show
current vs target"), an evidence anchor (K-id), and a data source
(task or endpoint). The per-unit Job is the absorbed minimap concern.

### → Section-edit (required)
Dashboard copy settles to final wording: panel titles, KPI labels,
action-list phrasing, drill-down captions.

### → Draft
Dashboard spec document with panel layouts, widget specs, data
bindings, and interaction rules. Produced by the draft(artifact)
stage via haipipe-application-artifact reading the venue profile;
render a display unit through /haipipe-task if a wireframe is needed.
