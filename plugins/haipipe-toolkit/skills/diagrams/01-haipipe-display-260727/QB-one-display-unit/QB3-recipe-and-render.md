# Recipe and render
state: ✅ SETTLED
owner: JL
method: keep the transformation reproducible and make it read only declared Intake material

## Opening
How does a Display unit turn Intake into a visual?

The renderer writes a recipe into `recipe/` and renders an asset from declared Intake inputs.

## Content
### One rebuild path per form
Tables write a generation script.
Plots write a plotting script and style module.
Diagrams write a FigureSpec.
Illustrations record the final prompt and review receipt.

### Candidate first when the decision is not made
The recipe may render into `candidates/` before a human has selected the result.
Candidate work cannot alter the live asset or wrapper.

## Aims
- [x] ⚙️ Give every renderer a recipe location
      The output contract maps form to asset and rebuild artifact.
- [x] 🔎 Make the input boundary inspectable
      The recipe may be audited against the manifest and snapshot hashes.

## States
All four renderer skills now route rebuild material to `recipe/` for new units.

## Files
- `display/ref/display-unit-output-contract.md`
  Per-renderer asset and recipe mapping.

## Law
Law: Values live in Intake; transformations live in recipe.

## Log
260727 · Split former mixed `source/` layouts into values and rebuild paths.
