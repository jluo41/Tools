# Display-Unit Output Contract

Owner: the `display/` family. Every renderer (`-display-table`, `-display-figure`,
`-display-diagram`, `-display-illustration`) writes into a **unit directory** the caller supplies,
not into a flat `figures/` directory. The unit is the contract: the renderer fills `assets/`,
`source/`, and `float.tex`, compiles `preview.pdf`, and updates `README.md`.

This is what makes a rendered asset a first-class, reusable, inspectable display instead of a
loose file.

**This file is source-agnostic.** It says nothing about papers. A caller that has a paper maps
this bundle into its own layout through its own adapter; the paper's is
`paper/1-lifecycle/4-display/ref/paper-adapter.md`. A renderer never opens a paper, never
resolves a paper root, and never creates a lifecycle page.

## Unit layout the renderer must produce

```text
<unit-dir>/
├── README.md      claim / kind / source / caption-job / fragility / status
├── float.tex      caption + \label + the asset reference
├── preview.tex    standalone wrapper that \inputs float.tex
├── preview.pdf    compiled preview
├── assets/        the WINNING rendered asset
├── candidates/    candidate-mode renders, pre-decision
├── source/        the rebuild spec (script / spec / prompt) + provenance
└── versions/      superseded variants and demoted candidates, kept for history
```

The caller owns where `<unit-dir>` sits and what the asset reference inside `float.tex` must be
relative to. The renderer is told both; it does not derive them.

## Per-renderer asset and source mapping

| Renderer | `assets/` | `source/` (rebuild spec) |
|---|---|---|
| `-display-table` | `table-body.tex` | `gen_*.py` + the aggregated CSV (path/ref) |
| `-display-figure` | `figure.pdf` | `gen_*.py` (+ `paper_plot_style.py`) |
| `-display-diagram` | `figure.svg` (+ `figure.pdf`) | the FigureSpec `*.json` |
| `-display-illustration` | `figure.png` | `prompt.md` (final prompt + bridge job + score) + `review_log.json` |

`float.tex` references the asset only. Numbers typed directly into `float.tex` are a defect: data
lives in `assets/`.

## Candidate mode

When the caller says candidate mode, or passes `--candidate <letter>`, the renderer:

- writes its render to `candidates/<letter>-<form>.<ext>` instead of `assets/`;
- still writes its rebuild spec into `source/`, suffixed with the candidate letter so specs do
  not collide;
- does NOT touch `assets/`, `float.tex`, or `README.md` status.

Promotion of a winner into `assets/`, and demotion of losers into `versions/`, is the CALLER's
decision, never the renderer's. This is what guarantees that commissioning a render can never
silently replace what a document currently shows.

## Renderer procedure

1. Receive the unit directory and the asset-reference base from the caller.
2. Render the asset into `<unit-dir>/assets/` (or `candidates/` in candidate mode).
3. Write the rebuild spec into `<unit-dir>/source/`.
4. Write or refresh `float.tex`: caption, `\label`, asset reference.
5. Write `preview.tex` if missing; compile `preview.pdf`.
6. Update `README.md`: status, evidence source.
7. Return the unit path and the result bundle. Never leave assets in a flat directory.

## Invariants

- **Numbers come from a task, never from the renderer.** A data display is rendered from
  caller-supplied evidence: a probe verdict, a parser's `metrics.json`, a `source_data.csv`. The
  rebuild spec in `source/` points at that output. A hand-typed coefficient, or a number typed
  into `float.tex`, is a placeholder and not a display. Concept figures carry no data and skip
  this, but a schematic is still annotated with REAL counts supplied by the caller, never
  invented ones.
- **Publication display hygiene.** Every rendered display must read in grayscale and be
  colorblind-safe: encode the key contrast with position, shape, or weight, never with hue alone.
  No title baked inside the image; the title lives only in `float.tex`'s `\caption{}`.
- **Refuse rather than guess.** Stop when the brief is incomplete, the named source is missing,
  or a numeric display has no verified aggregate. Do not search for data, invent it, or guess
  placement.

## Sibling renderers

| Display kind | Renderer |
|---|---|
| data plot (line/bar/scatter/heatmap/box) | `haipipe-display-figure` |
| typeset LaTeX table (booktabs) | `haipipe-display-table` |
| deterministic editable vector diagram (architecture/workflow/pipeline/topology) | `haipipe-display-diagram` |
| AI concept illustration | `haipipe-display-illustration` |

The two data renderers read a caller's aggregated output only; the two concept renderers take no
data, though a schematic still carries real counts.

## Notes

- Slides and posters consume the same bundle through `content-plan-spec.md` in this directory.
- The task-rendered path (`/haipipe-task-for-display`) writes into this SAME unit layout.
- Split out of the paper skill on 2026-07-26: this half is generic, and the paper-specific half
  (unit placement, paper-root-relative paths, the combined gallery, caption/label/placement
  ownership, and the lifecycle handoff) moved to the paper adapter named above.
