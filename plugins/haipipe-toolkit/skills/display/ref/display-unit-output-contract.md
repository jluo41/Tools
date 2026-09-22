# Display-Unit Output Contract

Owner: the `display/` family. All five renderer skills (`haipipe-display-table`,
`haipipe-display-figure`, `haipipe-display-diagram`, `haipipe-display-illustration`,
and `haipipe-display-tex`) write into a **unit directory** the caller supplies,
not into a flat `figures/` directory. The caller supplies a verified `intake/` and, when a
wrapper is wanted, the approved caption/label/placement fields. The renderer fills `recipe/` and
`assets/`; it may serialize `float.tex` only from those explicit caller-owned fields, compiles
`preview.pdf`, and updates `README.md`.

For a Page DISPLAY Result, the caller-supplied unit is
`<page>/results/<re-run>/payload/<unit>/`. The Result envelope owns this address; a renderer never
creates a parallel `outline/evidence/display/` or flat `display/` copy. Paper adapters consume the
Page Result unit and may project files into generated delivery output.

This is what makes a rendered asset a first-class, reusable, inspectable display instead of a
loose file.

A View-owned unit lives directly at
`views/<ViewPageStem>/output/<PageID>-Display<n>-<slug>/` (under a PAPER Section
page the unit is instead `Display<n>-<slug>`, because the page id already carries
the section index, `S-<desk>-Main-<N>-<Title>`; JL 260908). It may add
`output.md` as the View-owned semantic brief. This is still the one generic
unit directory: do not mirror it into a second renderer adapter folder. The
View builder may project only a derived `manifest.json`, `float.tex`, winning `assets/`,
and inspection previews into a source-free consumer fixture. `intake/manifest.yaml` remains the
authoritative intake record; the JSON file is a consumer projection, never a second source of truth.

**This is the shared, source-agnostic renderer contract.** It defines the portable unit, not a
caller's delivery layout. A caller that has a paper maps this bundle into its own layout through
the [Paper assembler](../../paper/haipipe-paper-assemble/SKILL.md). A renderer never opens a
paper, resolves a paper root, or creates a lifecycle page.

## Unit layout for new units

```text
<unit-dir>/
├── README.md      claim / kind / caption-job / fragility / status
├── intake/        caller-owned, provenance-bound values and context
│   ├── manifest.yaml
│   └── inputs/    small approved summary CSV/JSON extracts only
├── recipe/        renderer-owned script / FigureSpec / prompt / receipts;
│                  optional editable `<slug>.pptx` + `export.md`
├── float.tex      caller-owned caption + \label + renderer-owned content reference
├── preview.tex    standalone wrapper that \inputs float.tex
├── preview.pdf    compiled preview
├── assets/        the selected rendered asset; its presence is not acceptance
├── candidates/    candidate-mode renders, pre-decision
└── versions/      superseded variants and demoted candidates, kept for history
```

The caller owns where `<unit-dir>` sits and the wrapper's semantic fields (caption, label, and
placement). The renderer is told those fields; it does not derive, invent, or revise them.

The intake schema and materialization rules live in `display-intake-contract.md`.

## Legacy units

`source/` is a legacy directory name that mixed input snapshots with rebuild code.
Existing units remain valid without a rename.
A renderer explicitly handed a legacy unit may preserve its `source/` layout.
It must not create a mixed `source/` plus `intake/recipe/` layout in a new unit.
New units use the layout above.

## Per-renderer asset and recipe mapping

| Renderer | `assets/` | `recipe/` |
|---|---|---|
| `-display-table` | `table-body.tex` | `gen_*.py`, reading `intake/inputs/source_data.csv` |
| `-display-figure` | `figure.pdf` (or `figure.png` when raster output is explicitly selected) | `gen_*.py` (+ `paper_plot_style.py`) |
| `-display-diagram` | `figure.svg` (+ `figure.pdf`) | the FigureSpec `*.json` |
| `-display-illustration` | `figure.png` | `prompt.md` (final prompt + bridge job + score) + `review_log.json` |
| `haipipe-display-tex` | `figure.pdf` (standalone preview/fallback) | hand-authored `<slug>.tex` + `asset.tex` |
| PowerPoint-native manual figure | `figure.pdf` (or `figure.svg`) | editable `<slug>.pptx` + `export.md` (source → exported asset) |

For table, plot, diagram, and illustration units, `float.tex` references the approved asset.
For TeX-native units, `float.tex` may `\input` the hand-authored source in `recipe/` so a consumer
with the declared preamble can use the document's native fonts and macros. `assets/figure.pdf` is
the standalone fallback for consumers that cannot use that preamble. Both paths keep caption,
label, and placement caller-owned. Numbers typed directly into `float.tex` are a defect; values
come from the admitted intake.

## Execution and review boundaries

A parent Workflow is a list of Runs. One invocation that produces one bounded display unit may be
one Run. The renderer's numbered Steps, script or tool calls, compile, review, and retry loop stay
inside that Run. Give separate Runs only to independently closable unit targets with their own
receipts. `origin.run` records upstream provenance and is not renamed to the display Run.

Renderer scores and self-checks are advisory. A single caller-directed render may be written to
`assets/` while its `accepted:` status remains pending. When alternatives are being compared, keep
unselected work in `candidates/`, show the candidate and review notes to the caller, and wait for
the caller's selection before promoting a winner into `assets/`. Only the authorized human owner
records `accepted:` after the selected asset has a compiled and inspected preview. A score
threshold never selects or accepts an asset.

## Editable PowerPoint sources

PowerPoint is an allowed **authoring format** for a figure that needs human layout work.
It does not replace the display unit or become an input to LaTeX: keep the editable
`<slug>.pptx` in `recipe/`, export its approved visual to `assets/figure.pdf` (or SVG), and let
`float.tex` reference that exported asset as usual.

`recipe/export.md` records the source filename, export target, and the command or manual steps
needed to repeat the export. The Board can link the PPTX beside the compiled `preview.pdf`, but
the PDF remains the review artifact because it includes the actual float, caption, label, and
placement.

An editable PPTX does not relax the evidence contract: numeric labels still come only from the
declared intake, and a changed source follows the normal candidate → review → promotion path.
Legacy PPTX files under `versions/` remain linkable as historical editable sources; new work uses
`recipe/`.

## Candidate mode

When alternatives are being compared, or the caller asks for candidate mode, use a candidate id
according to that renderer's instructions; there is no shared command-line flag. The renderer:

- writes its render to `candidates/<letter>-<form>.<ext>` instead of `assets/`;
- writes its rebuild recipe into `recipe/`, suffixed with the candidate letter so recipes do
  not collide;
- does NOT touch `intake/`, `assets/`, `float.tex`, or `README.md` status.

The illustration renderer is a bridge-managed exception: unselected images remain in its declared
scratch workspace at `<work-root>/figures/ai_generated/`; it may write preflight and candidate
receipts in `recipe/` while comparing. It does not write the active asset or wrapper until the
caller selects a candidate, then records the final prompt and review receipt in `recipe/`.

The candidate asset is shown directly for selection; candidate mode leaves the unit's active
`assets/`, `float.tex`, and `preview.pdf` unchanged. The caller selects a winner and promotes it
into `assets/`; losing variants may move to `versions/`. After promotion, rebuild and inspect the
unit's `preview.pdf`. Promotion is the caller's decision, and `accepted:` is a separate human
decision recorded only after that preview is inspected.

Show the actual candidate file and identify it by candidate id; never present the unit's existing
`preview.pdf` as if it contained that candidate. If the caption or float context affects the
choice, create a candidate-named preview under `candidates/` using the candidate asset and the
unchanged caller-owned caption, label, and placement. Do not overwrite `float.tex` or the canonical
`preview.pdf` to make that preview.

## Renderer procedure

1. Receive the unit directory, asset-reference base, and prepared `intake/` from the caller.
2. Validate `intake/manifest.yaml`; a numeric render requires a verified values snapshot.
3. Render a single caller-directed result into `<unit-dir>/assets/`; in candidate mode, render it
   into `<unit-dir>/candidates/` and leave the active asset untouched.
4. Write the rebuild recipe into `<unit-dir>/recipe/`. For a PowerPoint-native figure, retain the
   editable `.pptx` there and write `export.md`; the exported PDF/SVG still goes in `assets/`.
5. For a selected asset, if the caller supplied a wrapper specification, create or refresh
   `float.tex` without changing its caption, `\label`, or placement. Use the renderer-specific
   content reference above. If no wrapper specification exists, leave `float.tex` pending rather
   than inventing one. Candidate mode does not edit the active wrapper.
6. Write `preview.tex` if missing. For table, figure, diagram, and illustration units, compile
   `preview.pdf` for the selected asset from the supplied asset-reference base. For a TeX-native
   unit, follow the TeX renderer's two wrapper compiles from their own directories so relative
   `\\input` paths resolve, and write the standalone fallback to `assets/figure.pdf`. Candidate
   mode leaves the active preview unchanged until promotion.
7. Update `README.md`: status, evidence source.
8. Return the unit path and the result bundle. Never leave assets in a flat directory.

## Invariants

- **Numbers come through an admitted producer, never from the renderer.** A data display is rendered from a
  caller-supplied intake snapshot. For a non-Page holder, its manifest points to the producing Task holder,
  Run, and canonical `source_data.csv`. For a Board Page, it points through the page-service `values.yaml`
  admitted as the Evidence Item's Local Input; the upstream Task and Run remain in that provenance chain.
  Its recipe reads the frozen `intake/inputs/` extract. A hand-typed
  coefficient, or a number typed into `float.tex`, is a placeholder and not a display. Concept
  renderers do not calculate values. They may show a real count, percentage, or estimate only when
  the caller declares a verified `role: values` intake source; they never invent one.
- **Publication display hygiene.** Every rendered display must read in grayscale and be
  colorblind-safe: encode the key contrast with position, shape, or weight, never with hue alone.
  No title baked inside the image; the title lives only in the caller-owned `\caption{}` in
  `float.tex`.
- **Refuse rather than guess.** Stop when the brief is incomplete, the named intake source is
  missing, its snapshot hash does not match, or a numeric display has no verified aggregate.
  Do not search for data, invent it, or guess placement.

## Sibling renderers

| Display kind | Renderer |
|---|---|
| data plot (line/bar/scatter/heatmap/box) | `haipipe-display-figure` |
| typeset LaTeX table (booktabs) | `haipipe-display-table` |
| deterministic editable vector diagram (architecture/workflow/pipeline/topology) | `haipipe-display-diagram` |
| AI concept illustration | `haipipe-display-illustration` |
| TeX-native unit sharing the paper's fonts and math — tikz, an `algorithm2e` block, or a display equation | `haipipe-display-tex` (hand-authored: the writer is a person, not a script) |

`haipipe-display` is the DOOR over this table: a caller who knows the kind may call a renderer
directly, and a caller who does not says what they want to the door.

The two data renderers require an aggregated values intake. Concept renderers have no default values
input; a concept unit that displays verified figures declares a separate `role: values` source.

## Notes

- The poster and slides renderers retired 2026-08-16 (JL), with the `content-plan-spec.md` that
  fed them; both are parked under `_todo/`. A board page's talk is the slide workbench's deck.
- `haipipe-task-for-display` produces a canonical display-ready aggregate and its provenance.
  It does not own the paper-facing unit or promoted asset. Diagnostic task plots may exist, but
  they are not canonical assets until a display unit accepts and renders them. For a Board Page,
  this aggregate first crosses the Page family's one numeric door through
  `haipipe-task-for-page`; only a non-Page holder consumes it directly.
- Split out of the paper skill on 2026-07-26: this half is generic, and the paper-specific half
  (unit placement, paper-root-relative paths, the combined gallery, caption/label/placement
  ownership, and the lifecycle handoff) moved to the paper adapter named above.
