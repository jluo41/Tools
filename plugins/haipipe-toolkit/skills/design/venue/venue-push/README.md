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
  terminal: adopted
```


## Venue template

```yaml
template:
  - slot: title
    job: hook + urgency
    claim_source: released Commission
    chars: ~50
  - slot: body
    job: benefit + action hint
    claim_source: released Brief + signed Wisdom handoff
    chars: ~100
```


## Phase use

### Commission and Generate

Keep the grant narrow: one source for the hook and one for the action. Author
one title, one body, and one deep-link target inside the released Commission's rails.

### Verify and adopt
Title grabs attention. Body gives one reason + one action.
No opt-out in body (handled by OS notification settings). Render the exact
notification to `delivery/render/`, then adopt or decline.
