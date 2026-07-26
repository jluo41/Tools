# Paper Adapter for the Display Family

Owner: `haipipe-paper-display`. This is the PAPER half of the display contract. The generic half,
which every renderer follows and which says nothing about papers, is
`display/ref/display-unit-output-contract.md`.

The split, made 2026-07-26, exists because the dependency ran backwards: the reusable Display
family was reading a contract that lived inside the Paper skill, through a path that did not
resolve. Display owns rendering; Paper owns what a display MEANS. Neither reaches into the other.

```text
 the caller (Paper)      decides the unit exists, where it sits, what it must say,
                         what it is called, where it is placed, and who gates it
 the renderer (Display)  fills the unit and returns a bundle
```

## Resolving the unit

Apply this whenever the target is a paper folder: a directory with `displays/`, or `the paper's S pages`,
or `0-lifecycle/`.

1. If the caller passed a unit id (`displayNN-slug`) or `--display-unit <dir>`, use it.
2. Else if the request maps to an existing unit by claim or slug, use that.
3. Else scaffold a new one: `Skill("haipipe-paper-stage", "display scaffold displayNN-<slug>")`.
   Pick the next free `displayNN`.

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

## What the paper owns and the renderer never touches

- the caption's argument, and `\label{fig|tab:<slug>}`
- the stable `display_id` and the float number
- placement: which section, which paragraph, which sentence cites it
- promotion of a candidate into `assets/`, which is a REVISE decision
- the human gate on the unit's `S-Display-<n>` page

## The combined gallery

`0-lifecycle/3-display/4-display.tex` is GENERATED and `\input`s each unit's `float.tex`, so a
correctly filed unit appears in the combined gallery automatically. Renderers never edit
`4-display.tex`. Hand-editing it is a defect.

## The lifecycle handoff

One display asset is one `S-Display-<n>` page, and that page carries the unit's six-link
provenance chain:

```text
① run       the task output that produced the numbers, outside the paper
② data      source/source_data.csv
③ gen code  source/gen_<slug>.py
④ result    assets/<figure.pdf | table-body.tex>
⑤ float     float.tex
⑥ reader    the section, paragraph and sentence that cites it
```

The renderer produces ② ③ ④ and refreshes ⑤. Links ① and ⑥ are the paper's, and they are what
make a number auditable rather than merely reproducible. A rendered unit whose ① is empty was
built from typed numbers, which the generic contract forbids.

Page shape, the per-asset template, and the thirteen-condition completeness checklist live with
the stage: `../../haipipe-paper-stage/stages/4-display/template.md`.
