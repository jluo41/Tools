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
  minimap:    optional

claims_depth: full
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
action button, data sources.

### → Minimap (optional)
If the card has sub-widgets, assign jobs per widget.
Simple cards (header + body + button) may skip.

### → Draft
UI spec with layout, content, interaction, and data binding.
May include ASCII wireframe.
