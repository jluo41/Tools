# Venue: Push Notification

Mobile push notification. Even shorter than SMS — title + body,
single tap action.


## Constraints

- **Title:** ≤ 50 characters
- **Body:** ≤ 100 characters
- **Action:** single tap → deep link to app screen
- **Rich media:** optional image (1:1 ratio, ≤ 1MB)


## Stage requirements

```yaml
stages:
  seed:       required
  pitch:      required
  claims:     required
  narrative:  skip
  display:    skip
  minimap:    skip

claims_depth: light
```


## Venue template

```yaml
template:
  - slot: title
    job: hook + urgency
    claim_source: primary claim
    chars: ~50
  - slot: body
    job: benefit + action hint
    claim_source: action claim (W)
    chars: ~100
```


## Lifecycle mappings

### → Claims (light)
2 K/W entries max — one for the hook, one for the action.

### → Draft
Title grabs attention. Body gives one reason + one action.
No opt-out in body (handled by OS notification settings).
