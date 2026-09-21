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


## Run guidance

### Commission and Generate

Use one narrow input scope for the prompt and motivation. The motivation slot cycles
through variants of the same released wager; a different thesis needs a new
Commission.

For a commissioned rotating set, draft the frozen number of variants (default
3-5); each follows the template and varies the motivation slot. A commissioned
single example stays a single example, rather than expanding into a set.

### Verify
Check the frozen `unit.shape/count` and judge every commissioned reminder.
Render inside the current Verify Result if needed; do not draft replacement
variants. Independent Verify pass makes that exact Unit ready for Delivery.
