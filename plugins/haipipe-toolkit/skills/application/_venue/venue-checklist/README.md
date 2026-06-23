# Venue: Checklist

Actionable checklist. 5-12 items, each completable, progressing
toward a goal.


## Constraints

- **Items:** 5-12 (fewer = too sparse; more = overwhelming)
- **Item format:** action verb + specific target
- **Completable:** each item has a clear done/not-done state
- **Order:** logical sequence (prep → action → verify)


## Stage requirements

```yaml
stages:
  seed:       required
  pitch:      required
  claims:     required
  narrative:  optional
  display:    skip
  minimap:    skip

claims_depth: medium
```


## Venue template

```yaml
template:
  - slot: title
    job: name the goal
    claim_source: pitch
  - slot: items
    job: each item = one action backed by one claim
    claim_source: one K/W per item
  - slot: completion
    job: what success looks like
    claim_source: primary claim
```


## Lifecycle mappings

### → Claims (medium)
Each checklist item should trace to a K/W entry. Gap check:
if an item has no evidence backing, flag it. Optional probe
if the gap is load-bearing.

### → Narrative (optional)
If the checklist has a natural progression (prep → action →
verify → confirm), writing the narrative makes the order explicit.
Skip if items are independent / unordered.

### → Draft
Each item: action verb + specific object + measurable completion.
"Check blood glucose before breakfast" not "Monitor glucose."
