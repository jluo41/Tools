# Venue: Reminder

Time-triggered recurring reminder. Brief, predictable, builds
habit through repetition.


## Constraints

- **Length:** ≤ 200 characters
- **Frequency:** recurring (daily, weekly, event-triggered)
- **Variation:** slight variation across instances to avoid fatigue
- **Tone:** supportive, not nagging


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
  - slot: prompt
    job: name the action to take
    claim_source: released Brief + signed Wisdom handoff
    chars: ~100
  - slot: motivation
    job: brief reason why (varies per instance)
    claim_source: released Commission
    chars: ~80
  - slot: encouragement
    job: positive reinforcement
    claim_source: standard
    chars: ~20
```


## Phase use

### Commission and Generate

Use one narrow grant for the prompt and motivation. The motivation slot cycles
through variants of the same released wager; a different thesis needs a new
Commission.

### Verify and adopt
Draft a set of 3-5 reminder variants that rotate. Each follows
the template but varies the motivation slot. Judge each variant, render the
set to `delivery/render/`, then adopt or decline.
