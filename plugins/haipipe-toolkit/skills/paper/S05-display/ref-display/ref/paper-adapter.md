# Paper Adapter for the Display Family

Owner: `haipipe-paper-display`. This is the PAPER half of the display contract. The generic half,
which every renderer follows and which says nothing about papers, is
`display/ref/display-unit-output-contract.md`.

The split, made 2026-07-26, exists because the dependency ran backwards: the reusable Display
family was reading a contract that lived inside the Paper skill, through a path that did not
resolve. Display owns rendering; Paper owns what a display MEANS. Neither reaches into the other.

```text
 the caller (Paper)      decides the unit exists, where it sits, what it must say,
                         what it is called, where it is placed, who gates it,
                         and which approved inputs enter its intake
 the renderer (Display)  validates intake, fills recipe/assets, and returns a bundle;
                         it serializes a wrapper only from Paper-approved fields
```

## Display Intake is the paper-facing bridge

For a data display, the Paper Display stage creates the unit's `intake/` before it commissions a
renderer.
The intake copies only the small display-ready aggregate and records its canonical task origin.
The task output, not the paper copy, remains the source of truth.

```text
tasks/<holder>/results/<run>/source_data.csv     canonical aggregate
        │
        ▼
displays/displayNN-<slug>/intake/
  ├── manifest.yaml     holder + run + canonical artifact + hashes + use
  └── inputs/source_data.csv
        │
        ▼
recipe/gen_<slug>.py -> assets/figure.pdf -> float.tex -> the citing sentence
```

The manifest follows `display/ref/display-intake-contract.md`.
For a concept figure, the intake records narrative context instead of a values CSV.
If the concept figure contains real numbers, those numbers enter through a values source exactly
as they would for a plot or table.

## Resolving the unit

Apply this whenever the target is a paper folder: a directory with `displays/`, or `the paper's S pages`,
or `0-lifecycle/`.

1. If the caller passed a unit id (`displayNN-slug`) or `--display-unit <dir>`, use it.
2. Else if the request maps to an existing unit by claim or slug, use that.
3. Else allocate the next identity that is free in **both** `S-Display-N` and
   `displays/displayNN-<slug>/`. Create the Paper page through the real creator:

   ```sh
   python3 <haipipe-paper-stage>/create-page.py display <paper-root> \
     --family Display --unit <N> --slug <slug> --directory 3-display
   ```

   Then create the matching display-unit layout from the shared output contract and fill the
   page's brief, Intake, and `### Wrapper` before finalization. This explicit per-unit path is
   used while the Display stage's central-artifact migration (`QB2b`) remains open; do not invent
   a `display scaffold` subcommand.

Only when no paper and no `displays/` is found does a renderer fall back to a flat
`figures/ai_generated/`, and it says so in its return.

The unit directory handed to the renderer is therefore
`displays/displayNN-<slug>/`, and that is the only thing the renderer needs to know about this
paper.

## Paths are paper-root-relative

`float.tex` is `\input` from the paper root and compiled there, so its asset reference must be the
full path from the paper root:

```latex
\includegraphics{displays/displayNN-<slug>/assets/figure.pdf}   % NOT assets/figure.pdf
```

Same for `preview.tex`'s `\input`. `preview.pdf` compiles FROM THE PAPER ROOT so `displays/`
paths resolve. The caller passes this base to the renderer; the renderer does not derive it.

## What the paper owns and the renderer never changes

- the caption's argument, `\label{fig|tab:<slug>}`, and float placement
- the stable `display_id` and the float number
- placement: which section, which paragraph, which sentence cites it
- promotion of a candidate into `assets/`, which is a REVISE decision
- the human gate on the unit's `S-Display-<n>` page

Paper may give those approved wrapper fields to a renderer so it can serialize an initial
`float.tex`, or refresh that wrapper's asset reference. That mechanical write does not transfer
semantic ownership: a renderer never chooses or changes the caption, label, placement, unit id,
or citation location.

For a paper unit, the canonical wrapper specification is the `### Wrapper` block on its
`S-Display-<n>` page. It records the approved caption text, `\label`, and placement. Candidate
renders may proceed without it; finalization and `float.tex` serialization may not.

## The combined gallery

`0-lifecycle/3-display/4-display.tex` is GENERATED and `\input`s each unit's `float.tex`, so a
correctly filed unit appears in the combined gallery automatically. Renderers never edit
`4-display.tex`. Hand-editing it is a defect.

## The lifecycle handoff

One display asset is one `S-Display-<n>` page, and that page carries the unit's six-link
provenance chain:

```text
① run       the task holder and run that produced the canonical aggregate, outside the paper
② intake    intake/manifest.yaml + intake/inputs/source_data.csv
③ recipe    recipe/gen_<slug>.py | FigureSpec | prompt | `<slug>.pptx` + export.md
④ result    assets/<figure.pdf | table-body.tex>
⑤ float     float.tex
⑥ reader    the section, paragraph and sentence that cites it
```

The Paper Display stage materializes ②; the renderer produces ③ and ④ and may serialize ⑤ from
Paper-approved wrapper fields.
Links ① and ⑥ are the paper's, and they are what make a number auditable rather than merely
reproducible. A numeric rendered unit whose ① or ② is empty was built from typed or untraceable
numbers, which the generic contract forbids.

Existing units that retain the legacy `source/` layout are not migrated automatically.
Their S page records the old paths until a deliberate unit migration occurs.
Legacy `.pptx` files under `versions/` are editable historical sources; a repaired or new
PowerPoint-native figure places its canonical source in `recipe/` and exports a PDF/SVG into
`assets/` before `float.tex` and `preview.pdf` are refreshed.

Page shape, the per-asset template, and the thirteen-condition completeness checklist live with
the stage: `../../haipipe-paper-stage/stages/4-display/template.md`.
