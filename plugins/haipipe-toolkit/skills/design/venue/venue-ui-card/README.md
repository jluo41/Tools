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

### Commission and Generate

Every load-bearing UI element and displayed value maps through released
Commission inputs. Data bindings name accepted sources; raw results never substitute.

### Generate · hierarchy
Hierarchical arc:
- Header: hook / alert
- Body: detail / evidence
- Action: what to do

### Generate · display requirement
Widget map: header type, body elements (gauge, list, chart),
action button, data sources. Each unit carries a per-unit Job:
one sentence on what the reader must see or do (the absorbed
minimap concern) — if the unit has sub-widgets, one Job per widget.

### Generate · optional widget pass
Per-widget review pass on multi-widget cards; simple cards
(header + body + button) skip.

### Verify
UI spec with layout, content, interaction, and data binding,
owned by the Design Unit. Judge every widget and binding against the actual
screen rendered with `haipipe-design-unit/scripts/render_screen.py`. Write the
picture and manifest inside the current Result and pin them before completion.
An ASCII wireframe can guide internal drafting but cannot satisfy visual checks.
Independent Verify pass makes the exact screen ready for Delivery.
