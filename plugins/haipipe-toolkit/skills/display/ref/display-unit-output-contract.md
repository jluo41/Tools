# Display-Unit Output Contract

Owner: the `display/` family. Every renderer (`-display-table`, `-display-figure`,
`-display-diagram`, `-display-illustration`) writes into a **unit directory** the caller supplies,
not into a flat `figures/` directory. The caller supplies a verified `intake/` and, when a
wrapper is wanted, the approved caption/label/placement fields. The renderer fills `recipe/` and
`assets/`; it may serialize `float.tex` only from those explicit caller-owned fields, compiles
`preview.pdf`, and updates `README.md`.

This is what makes a rendered asset a first-class, reusable, inspectable display instead of a
loose file.

**This file is source-agnostic.** It says nothing about papers. A caller that has a paper maps
this bundle into its own layout through its own adapter; the paper's is
`paper/1-lifecycle/4-display/ref/paper-adapter.md`. A renderer never opens a paper, never
resolves a paper root, and never creates a lifecycle page.

## Unit layout for new units

```text
<unit-dir>/
├── README.md      claim / kind / caption-job / fragility / status
├── intake/        caller-owned, provenance-bound values and context
│   ├── manifest.yaml
│   └── inputs/    small approved summary CSV/JSON extracts only
├── recipe/        renderer-owned script / FigureSpec / prompt / receipts;
│                  optional editable `<slug>.pptx` + `export.md`
├── float.tex      caller-owned caption + \label + renderer-maintained asset reference
├── preview.tex    standalone wrapper that \inputs float.tex
├── preview.pdf    compiled preview
├── assets/        the WINNING rendered asset
├── candidates/    candidate-mode renders, pre-decision
└── versions/      superseded variants and demoted candidates, kept for history
```

The caller owns where `<unit-dir>` sits, the wrapper's semantic fields (caption, label, and
placement), and what the asset reference inside `float.tex` must be relative to. The renderer is
told those fields; it does not derive, invent, or revise them.

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
| `-display-figure` | `figure.pdf` | `gen_*.py` (+ `paper_plot_style.py`) |
| `-display-diagram` | `figure.svg` (+ `figure.pdf`) | the FigureSpec `*.json` |
| `-display-illustration` | `figure.png` | `prompt.md` (final prompt + bridge job + score) + `review_log.json` |
| PowerPoint-native manual figure | `figure.pdf` (or `figure.svg`) | editable `<slug>.pptx` + `export.md` (source → exported asset) |

`float.tex` references the asset only. Numbers typed directly into `float.tex` are a defect: data
lives in `assets/`.

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

When the caller says candidate mode, or passes `--candidate <letter>`, the renderer:

- writes its render to `candidates/<letter>-<form>.<ext>` instead of `assets/`;
- writes its rebuild recipe into `recipe/`, suffixed with the candidate letter so recipes do
  not collide;
- does NOT touch `intake/`, `assets/`, `float.tex`, or `README.md` status.

Promotion of a winner into `assets/`, and demotion of losers into `versions/`, is the CALLER's
decision, never the renderer's. This is what guarantees that commissioning a render can never
silently replace what a document currently shows.

## Renderer procedure

1. Receive the unit directory, asset-reference base, and prepared `intake/` from the caller.
2. Validate `intake/manifest.yaml`; a numeric render requires a verified values snapshot.
3. Render the asset into `<unit-dir>/assets/` (or `candidates/` in candidate mode).
4. Write the rebuild recipe into `<unit-dir>/recipe/`. For a PowerPoint-native figure, retain the
   editable `.pptx` there and write `export.md`; the exported PDF/SVG still goes in `assets/`.
5. If the caller supplied a wrapper specification, create or refresh `float.tex` without changing
   its caption, `\label`, or placement; update only the asset reference as needed. If no such
   specification exists, leave `float.tex` pending rather than inventing one.
6. Write `preview.tex` if missing; compile `preview.pdf`.
7. Update `README.md`: status, evidence source.
8. Return the unit path and the result bundle. Never leave assets in a flat directory.

## Invariants

- **Numbers come from a task, never from the renderer.** A data display is rendered from a
  caller-supplied intake snapshot. Its manifest points to the producing task holder, run, and
  canonical `source_data.csv`; its recipe reads the frozen `intake/inputs/` extract. A hand-typed
  coefficient, or a number typed into `float.tex`, is a placeholder and not a display. Concept
  figures carry no data and skip this, but a schematic is still annotated with REAL counts supplied
  by the caller, never invented ones.
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

The two data renderers read a caller's aggregated intake only; the two concept renderers take no
values input, though a schematic still carries real counts.

## Notes

- Slides and posters consume the same bundle through `content-plan-spec.md` in this directory.
- `haipipe-task-for-display` produces a canonical display-ready aggregate and its provenance.
  It does not own the paper-facing unit or promoted asset. Diagnostic task plots may exist, but
  they are not canonical paper assets until a display unit accepts and renders them.
- Split out of the paper skill on 2026-07-26: this half is generic, and the paper-specific half
  (unit placement, paper-root-relative paths, the combined gallery, caption/label/placement
  ownership, and the lifecycle handoff) moved to the paper adapter named above.
