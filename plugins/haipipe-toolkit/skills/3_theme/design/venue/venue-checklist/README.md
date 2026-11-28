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
    claim_source: the signed goal (board.md ## Goals) and the shared rules (design-goal.md)
  - slot: items
    job: each item = one action backed by a fence file
    claim_source: the pinned goal · method version · inputs version
  - slot: completion
    job: what success looks like
    claim_source: the signed goal (board.md ## Goals) and the shared rules (design-goal.md) + signed Wisdom handoff
```


## Run guidance

### Inputs and generate ③

Each checklist item maps through the Job's inputs/ fence (its manifest). If an item lacks a
load-bearing premise, return a named gap; do not Probe from Design.

### generate ③ · optional ordering narrative
If the checklist has a natural progression (prep → action →
verify → confirm), writing the narrative makes the order explicit.
Skip if items are independent / unordered.

### verify ④ (another agent)
Each item: action verb + specific object + measurable completion.
"<verb> <the specific object> <when>" not "<monitor the thing>." If a preview is needed, render the exact ordered list inside the current Run's result/.
A passed verify ④, then t99's rank ⑤ and a person's release, put that exact list in delivery/.
