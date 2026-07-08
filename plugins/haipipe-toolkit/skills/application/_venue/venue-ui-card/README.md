# Venue: UI Card

In-app card or widget. A focused, interactive element embedded
in an existing interface.


## Constraints

- **Size:** fits one screen (no scroll for core content)
- **Interaction:** tap/click for detail, dismiss, act
- **Context:** embedded in an existing app (not standalone)
- **Update:** persistent, refreshed on data change


## Stage requirements

```yaml
stages:
  seed:       required
  pitch:      required
  claims:     required
  narrative:  required
  display:    required
  section-edit:    optional

claims_settlement: full
```


## Lifecycle mappings

### → Claims (full)
Full claim ledger. Each UI element must trace to a claim.

### → Narrative (required)
Hierarchical arc:
- Header: hook / alert
- Body: detail / evidence
- Action: what to do

### → Display (required)
Widget map: header type, body elements (gauge, list, chart),
action button, data sources. Each unit carries a per-unit Job:
one sentence on what the reader must see or do (the absorbed
minimap concern) — if the card has sub-widgets, one Job per widget.

### → Section-edit (optional)
Per-widget review pass on multi-widget cards; simple cards
(header + body + button) skip.

### → Draft
UI spec with layout, content, interaction, and data binding,
produced by haipipe-application-artifact reading the venue profile.
May include an ASCII wireframe.
