# Venue: Reminder

Time-triggered recurring reminder. Brief, predictable, builds
habit through repetition.


## Constraints

- **Length:** ≤ 200 characters
- **Frequency:** recurring (daily, weekly, event-triggered)
- **Variation:** slight variation across instances to avoid fatigue
- **Tone:** supportive, not nagging


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
  - slot: prompt
    job: name the action to take
    claim_source: action claim (W)
    chars: ~100
  - slot: motivation
    job: brief reason why (varies per instance)
    claim_source: primary claim (K)
    chars: ~80
  - slot: encouragement
    job: positive reinforcement
    claim_source: standard
    chars: ~20
```


## Lifecycle mappings

### → Claims (light)
1-2 K/W entries. The motivation slot cycles through different
framings across reminder instances.

### → Draft
Draft a set of 3-5 reminder variants that rotate. Each follows
the template but varies the motivation slot.
