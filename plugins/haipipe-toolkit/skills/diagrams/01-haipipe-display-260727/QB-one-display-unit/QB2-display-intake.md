# The Display Intake
state: ✅ SETTLED
owner: JL
method: snapshot only the approved small aggregate while retaining a path and hash back to its canonical producer

## Question
What is the source of a Display unit?

The canonical source is the producing task's aggregate.
The Intake is the bounded copy that this unit may read.

## Diagram
```text
task/<holder>/results/<run>/
  source_data.csv + provenance.json       canonical evidence
                 │
                 ▼
unit/intake/manifest.yaml                 holder · run · artifact · hashes · use
unit/intake/inputs/source_data.csv        frozen, display-safe snapshot
```

## Content
### Values
A numeric source records holder, run, canonical artifact, provenance file, origin hash, snapshot path, and snapshot hash.
The renderer reads only the snapshot.

### Context
A diagram or illustration can declare `role: narrative-context` instead of values.
Any real number inside that concept visual still needs a values source.

## Items to Finish
- [x] 📥 Define the Intake manifest and source roles
      The manifest template records values, narrative context, and permitted use.
- [x] 🔐 Require aggregate and safety verification
      Raw or PHI data cannot enter a paper-facing Intake.

## Where we are
The Intake contract is implemented and fresh-context agents followed it correctly.

## Files
- `display/ref/display-intake-contract.md`
  The materialization and refusal rules.
- `display/ref/intake-manifest.template.yaml`
  The copyable schema.

## Law
Law: Intake is a traceable render input, never a new source of truth.

## Log
260727 · JL approved the small-summary-CSV model for display rendering.
