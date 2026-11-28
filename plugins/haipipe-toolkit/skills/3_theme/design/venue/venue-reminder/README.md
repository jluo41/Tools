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
    claim_source: the signed goal (board.md ## Goals) and the shared rules (design-goal.md) + signed Wisdom handoff
    chars: ~100
  - slot: motivation
    job: brief reason why (varies per instance)
    claim_source: the pinned goal · method version · inputs version
    chars: ~80
  - slot: encouragement
    job: positive reinforcement
    claim_source: standard
    chars: ~20
```


## Run guidance

### Inputs and generate ③

Use one narrow fence for the prompt and motivation. The motivation slot cycles
through variants of the same idea; a different thesis is a different idea in t00,
so its own design Task.

For a rotating set, draft the goal's N variants (default 3-5); each follows the
template and varies the motivation slot. A goal of N = 1 stays a single example,
rather than expanding into a set.

### verify ④ (another agent)
Check the goal's N and judge every reminder of the design.
Render inside the current verify's result/ if needed; do not draft replacement
variants. A passed verify ④, then t99's rank ⑤ and a person's release, put that exact design in delivery/.
