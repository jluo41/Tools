# One unit has a page and a folder
state: ✅ SETTLED
owner: JL
method: bind governance to an S page and artifacts to a unit directory without storing either twice

## Question
Why does one display have both an `S-Display-N` page and a `displays/displayNN-<slug>/` folder?

The page is the decision record.
The folder is the reproducible visual bundle.

## Boundary
- ✅ The page contains claim, reader takeaway, provenance links, wrapper, gate, and decision history.
- ✅ The folder contains Intake, recipe, candidates, assets, preview, and the serialized float.
- 🚫 Neither is a second home for raw task data or a free-form alternative to the other.

## Diagram
```text
S-Display-N-forest-plot.md                  displays/display12-forest-plot/
──────────────────────────                  ────────────────────────────────
why this reader needs it                     what the renderer reads and writes
① run · ② Intake · ③ recipe                  intake/ · recipe/ · candidates/
wrapper · placement · gate                   assets/ · float.tex · preview.pdf
```

## Content
### The page is a human surface
The S page answers whether the display should exist, what it is meant to show, and whether it may enter the manuscript.
Its `### Wrapper` is the canonical Paper-owned caption, label, and placement specification.

### The folder is a machine-visible bundle
The unit folder lets a renderer rebuild and verify the actual visual without rereading an entire lifecycle Board.
The manifest links the folder back to the S page through `requested_by`.

## Items to Finish
- [x] 🔗 Define the cross-link in both directions
      `requested_by` points to the S page and provenance link ② points to the manifest.
- [x] 🧱 Keep semantic and artifact fields separate
      The wrapper and gate remain on the page while recipe and asset remain in the folder.

## Where we are
The page-folder pair is the atomic operational unit for a paper display.

## Files
- `display/ref/intake-manifest.template.yaml`
  Carries the `requested_by` pointer.
- `paper/1-lifecycle/haipipe-paper-stage/stages/4-display/template.md`
  Carries the six-link provenance chain and wrapper.

## Law
Law: A page decides; a folder renders. Neither replaces the other.

## Log
260727 · The page-folder distinction was made explicit to prevent Board prose from becoming a data store.
