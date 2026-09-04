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
  terminal: accepted
```


## Venue template

```yaml
template:
  - slot: title
    job: hook + urgency
    claim_source: released card grant
    chars: ~50
  - slot: body
    job: benefit + action hint
    claim_source: GD0-closed Brief + signed Wisdom handoff
    chars: ~100
```


## Phase use

### D1/D2 · bet and realize

Keep the grant narrow: one source for the hook and one for the action. Author
one title, one body, and one deep-link target inside the released card's rails.

### D3/D4 · judge and decide
Title grabs attention. Body gives one reason + one action.
No opt-out in body (handled by OS notification settings). Render the exact
notification to `delivery/render/`, then accept or emit.
