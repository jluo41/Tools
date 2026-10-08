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
```

## Run guidance

### Inputs and generate ③

Every load-bearing UI element and displayed value maps through the Job's
inputs/ fence (its manifest). Data bindings name accepted sources; raw results never substitute.

### generate ③ · hierarchy
Hierarchical arc:
- Header: hook / alert
- Body: detail / evidence
- Action: what to do

### generate ③ · display requirement
Widget map: header type, body elements (gauge, list, chart),
action button, data sources. Each unit carries a per-unit Job:
one sentence on what the reader must see or do (the absorbed
minimap concern) — if the unit has sub-widgets, one Job per widget.

### generate ③ · optional widget pass
Per-widget review pass on multi-widget cards; simple cards
(header + body + button) skip.

### verify ④ (another agent)
UI spec with layout, content, interaction, and data binding,
owned by the Design Unit. Judge every widget and binding against the actual
screen rendered with `haipipe-design-unit/scripts/render_screen.py`. Write the
picture and manifest inside the current Run's result/ and pin them before completion.
An ASCII wireframe can guide internal drafting but cannot satisfy visual checks.
A passed verify ④, then t99's rank ⑤ and a person's release, put the exact screen in delivery/.
