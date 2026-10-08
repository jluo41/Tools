# Venue: Push Notification

Mobile push notification. Even shorter than SMS — title + body,
single tap action.


## Constraints

- **Title:** ≤ 50 characters
- **Body:** ≤ 100 characters
- **Action:** single tap → deep link to app screen
- **Rich media:** optional image (1:1 ratio, ≤ 1MB)


## Design profile

```yaml
design_profile:
  evidence_bar: light
  narrative: none
  display: none
  section_edit: none
```


## Venue template

```yaml
template:
  - slot: title
    job: hook + urgency
    claim_source: the pinned goal · method version · inputs version
    chars: ~50
  - slot: body
    job: benefit + action hint
    claim_source: the signed goal (board.md ## Goals) and the shared rules (design-goal.md) + signed Wisdom handoff
    chars: ~100
```


## Run guidance

### Inputs and generate ③

Keep the fence narrow: one source for the hook and one for the action. Author
one title, one body, and one deep-link target inside the pinned goal's and rules' rails.

### verify ④ (another agent)
Title grabs attention. Body gives one reason + one action.
No opt-out in body (handled by OS notification settings). Render the exact
notification inside the current Run's result/ if needed for visual checks. A passed verify ④, then t99's rank ⑤ and a person's release, put
it in delivery/.
