# Refusal and safety
state: ✅ SETTLED
owner: JL
method: stop a renderer before it guesses a source, extracts raw data, or makes unsupported facts look visual

## Opening
When must a renderer refuse to proceed?

It refuses whenever the source boundary, snapshot integrity, visual brief, or safety condition is incomplete.

## Content
### Numeric refusal
A numeric display requires a values source with task holder, canonical artifact, provenance record, and matching snapshot hash.
The renderer does not browse task folders to find a convenient CSV.

### Concept refusal
A concept display may use narrative context without values.
It must refuse any requested real count, percentage, or estimate that lacks a values source.

### Privacy refusal
An Intake snapshot must be display-safe.
Raw or PHI-bearing data remains in the task environment even when the renderer runs locally.

## Aims
- [x] 🛑 State source and hash refusal rules
      The Intake contract requires an auditable numeric source.
- [x] 🔐 State the aggregate-only privacy boundary
      A paper folder receives only approved summaries.
- [x] 🚫 Prohibit invented facts in illustrations and diagrams
      Real numbers are values inputs regardless of visual form.

## States
Fresh-context validation confirmed that the figure renderer stops before a verified Intake exists.

## Files
- `display/ref/display-intake-contract.md`
  Required fields and refusal rules.
- `display/ref/display-unit-output-contract.md`
  Shared renderer invariants.

## Law
Law: Refuse rather than guess a value, a source, a subset, or a claim.

## Log
260727 · Tested the refusal path against a hypothetical forest plot with no materialized Intake.
