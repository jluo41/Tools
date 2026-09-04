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
  terminal: accepted
```


## Venue template

```yaml
template:
  - slot: prompt
    job: name the action to take
    claim_source: GD0-closed Brief + signed Wisdom handoff
    chars: ~100
  - slot: motivation
    job: brief reason why (varies per instance)
    claim_source: released card grant
    chars: ~80
  - slot: encouragement
    job: positive reinforcement
    claim_source: standard
    chars: ~20
```


## Phase use

### D1/D2 · bet and realize

Use one narrow grant for the prompt and motivation. The motivation slot cycles
through variants of the same released wager; a different thesis needs a new
card.

### D3/D4 · judge and decide
Draft a set of 3-5 reminder variants that rotate. Each follows
the template but varies the motivation slot. Judge each variant, render the
set to `delivery/render/`, then accept or emit.
