# The Display-unit contract
state: ✅ SETTLED
owner: JL
method: make one directory an inspectable bundle with stable ownership for inputs, rebuilds, candidates, and selected output

## Opening
What must every new Display unit contain?

A unit contains one approved input boundary, one rebuild path, reversible alternatives, and one selected asset.

## Diagram
```text
displayNN-<slug>/
├── README.md       brief and status mirror
├── intake/         approved, provenance-bound inputs
├── recipe/         rebuild code, FigureSpec, prompt, receipts
├── candidates/     unpromoted alternatives
├── assets/         selected visual only
├── versions/       retired alternatives
├── float.tex       consumer wrapper
└── preview.*       local review surface
```

## Content
### The folder names are roles
`intake/` is not code.
`recipe/` is not a data source.
`assets/` is not a scratch directory.
`candidates/` is not a second final location.

### New versus legacy units
New units use this split shape.
An existing `source/` folder remains valid only as a documented compatibility case.

## Aims
- [x] 📦 Publish one generic output contract
      All renderers use the same new-unit layout.
- [x] 🧹 Preserve legacy compatibility without mixing layouts
      A new unit never creates both `source/` and `intake/recipe/`.

## States
The generic output contract is shared by table, figure, diagram, and illustration renderers.

## Files
- `display/ref/display-unit-output-contract.md`
  The authoritative folder contract.

## Law
Law: A unit is a bundle with roles, not a directory where output happens to land.

## Log
260727 · Formalized the new unit layout around Intake, recipe, candidates, and assets.
