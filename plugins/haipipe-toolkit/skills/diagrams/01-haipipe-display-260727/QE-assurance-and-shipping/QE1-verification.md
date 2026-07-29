# Verification of a Display unit
state: ✅ SETTLED
owner: JL
method: check source lineage, unit integrity, wrapper ownership, and reader connection as distinct conditions

## Question
What must be verified before a Display unit is complete?

A visually plausible file is not enough.
The unit must pass provenance, rebuild, selection, wrapper, and consumer checks.

## Diagram
```text
① task run ─► ② Intake hash ─► ③ recipe reads Intake ─► ④ selected asset
       └──────────────────────────────► ⑤ approved wrapper ─► ⑥ citing sentence
```

## Content
### Mechanical checks
The manifest must parse.
Declared snapshots must exist and match their hashes.
Numeric elements must trace to a values source.
The recipe must read only declared inputs.

### Human checks
A human decides whether the selected candidate supports the reader's argument.
The Paper gate verifies that caption, label, placement, and sentence usage match the approved unit.

## Items to Finish
- [x] ✅ Define unit-level structural checks
      The Display stage checklist covers Intake, recipe, selected asset, preview, and wrapper.
- [x] 🧠 Keep semantic approval human-owned
      Candidate promotion and Paper placement require a visible gate.

## Where we are
The generic contracts define refusal and integrity checks while Paper retains the final semantic decision.

## Files
- `paper/1-lifecycle/haipipe-paper-stage/stages/4-display/checklist.md`
  Paper-unit completeness checklist.
- `display/ref/display-intake-contract.md`
  Intake verification conditions.

## Law
Law: A complete display is traceable, rebuildable, selected, semantically approved, and actually cited.

## Log
260727 · Joined mechanical lineage checks to the Paper human gate.
