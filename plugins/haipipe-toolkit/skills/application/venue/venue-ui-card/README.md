# Venue: UI Card

In-app card or widget. A focused, interactive element embedded
in an existing interface.


## Constraints

- **Size:** fits one screen (no scroll for core content)
- **Interaction:** tap/click for detail, dismiss, act
- **Context:** embedded in an existing app (not standalone)
- **Update:** persistent, refreshed on data change


## Design profile

```yaml
design_profile:
  evidence_bar: full
  narrative: required
  display: required
  section_edit: optional
  terminal: accepted
```

## Phase use

### D1/D2 · bet and realize

Every load-bearing UI element and displayed value maps through the released
card grant. Data bindings name accepted sources; raw results never substitute.

### D2 · hierarchy
Hierarchical arc:
- Header: hook / alert
- Body: detail / evidence
- Action: what to do

### D2 · display requirement
Widget map: header type, body elements (gauge, list, chart),
action button, data sources. Each unit carries a per-unit Job:
one sentence on what the reader must see or do (the absorbed
minimap concern) — if the card has sub-widgets, one Job per widget.

### D2 · optional widget pass
Per-widget review pass on multi-widget cards; simple cards
(header + body + button) skip.

### D3/D4 · judge and decide
UI spec with layout, content, interaction, and data binding,
owned by the Design Unit. Include an ASCII wireframe, judge every widget and
binding, render to `delivery/render/`, then accept or emit.
