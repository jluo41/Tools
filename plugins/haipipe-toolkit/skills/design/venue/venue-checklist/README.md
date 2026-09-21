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
```


## Venue template

```yaml
template:
  - slot: title
    job: name the goal
    claim_source: released Brief
  - slot: items
    job: each item = one action backed by Commission inputs
    claim_source: released Commission
  - slot: completion
    job: what success looks like
    claim_source: released Brief + signed Wisdom handoff
```


## Run guidance

### Commission and Generate

Each checklist item maps through released Commission inputs. If an item lacks a
load-bearing premise, return a named gap; do not Probe from Design.

### Generate · optional ordering narrative
If the checklist has a natural progression (prep → action →
verify → confirm), writing the narrative makes the order explicit.
Skip if items are independent / unordered.

### Verify
Each item: action verb + specific object + measurable completion.
"Check blood glucose before breakfast" not "Monitor glucose." If a preview is needed, render the exact ordered list inside the current Result.
Independent Verify pass makes that exact list ready for Delivery.
