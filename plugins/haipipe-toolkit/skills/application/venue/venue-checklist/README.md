# Venue: Checklist

Actionable checklist. 5-12 items, each completable, progressing
toward a goal.


## Constraints

- **Items:** 5-12 (fewer = too sparse; more = overwhelming)
- **Item format:** action verb + specific target
- **Completable:** each item has a clear done/not-done state
- **Order:** logical sequence (prep → action → verify)


## Design profile

```yaml
design_profile:
  evidence_bar: medium
  narrative: optional
  display: none
  section_edit: none
  terminal: accepted
```


## Venue template

```yaml
template:
  - slot: title
    job: name the goal
    claim_source: GD0-closed Brief
  - slot: items
    job: each item = one action backed by the card grant
    claim_source: released card grant
  - slot: completion
    job: what success looks like
    claim_source: GD0-closed Brief + signed Wisdom handoff
```


## Phase use

### D1/D2 · bet and realize

Each checklist item maps through the released card grant. If an item lacks a
load-bearing premise, preserve the gap for D4 EMIT; do not Probe from Design.

### D2 · optional ordering narrative
If the checklist has a natural progression (prep → action →
verify → confirm), writing the narrative makes the order explicit.
Skip if items are independent / unordered.

### D3/D4 · judge and decide
Each item: action verb + specific object + measurable completion.
"Check blood glucose before breakfast" not "Monitor glucose." Render the
exact ordered list to `delivery/render/`, then accept or emit.
