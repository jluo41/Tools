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
  terminal: adopted
```

## Phase use

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

### Verify and adopt
UI spec with layout, content, interaction, and data binding,
owned by the Design Unit. Judge every widget and binding, render to
`delivery/render/`, then adopt or decline. A drawn screen renders with
`haipipe-design-unit/scripts/render_screen.py` and is judged on that picture;
an ASCII wireframe stands in only while no screen is drawn yet.
