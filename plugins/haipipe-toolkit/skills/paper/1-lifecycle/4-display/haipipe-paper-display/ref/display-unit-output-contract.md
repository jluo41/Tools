# Display-Unit Output Contract

Owner: `haipipe-paper-display`. Every display **renderer**
(`-display-table`, `-display-figure`, `-display-diagram`,
`-display-illustration`, `-display-illustration-gemini`) writes its output into a
`0-displays/displayNN-<slug>/` unit, NOT into a flat `figures/` directory. The
unit is the contract; the renderer fills `assets/`, `source/`, and `float.tex`,
then compiles `preview.pdf` and updates `README.md`.

This is what makes a rendered asset a first-class, reusable, gallery-visible
display instead of a loose file. The flat `figures/ai_generated/` (or `figures/`)
default is a FALLBACK only — used when there is no paper / no `0-displays/`.

## When the contract applies

Apply it whenever the target is a paper folder (a directory with `0-displays/`,
or `STATUS.md`, or `0-lifecycle/`). Resolve the unit:

1. If the caller passed a unit id (`displayNN-slug`) or `--display-unit <dir>`, use it.
2. Else if the request maps to an existing unit (by claim/slug), use that.
3. Else SCAFFOLD a new one: `Skill("haipipe-paper-display", "scaffold displayNN-<slug>")`
   (or create the skeleton directly per the scaffold template). Pick the next free
   `displayNN`.

Only if no paper / no `0-displays/` is found, fall back to `figures/ai_generated/`
and say so in the return tail.

## Unit layout the renderer must produce

```text
0-displays/displayNN-<slug>/
├── README.md      claim / kind / source / caption-job / fragility / status
├── float.tex      caption + \label + \includegraphics{assets/...} (figures) or \input{assets/table-body.tex} (tables)
├── preview.tex    standalone wrapper: \input{0-displays/displayNN-<slug>/float.tex}
├── preview.pdf    compiled FROM THE PAPER ROOT so 0-displays/ paths resolve
├── assets/        the rendered asset
├── source/        the rebuild spec (script / spec / prompt) + provenance
└── versions/      optional: superseded variants kept for history
```

**Paths are PAPER-ROOT-relative, not unit-relative.** `float.tex` is `\input` from
the paper root and compiled there, so its asset reference must be the full path
from the paper root, e.g. `\includegraphics{0-displays/displayNN-<slug>/assets/figure.pdf}`
(NOT `assets/figure.pdf`). Same for `preview.tex`'s `\input`.

## Per-renderer asset + source mapping

| Renderer | `assets/` | `source/` (rebuild spec) |
|---|---|---|
| `-display-table` | `table-body.tex` | `gen_*.py` + the aggregated CSV (path/ref) |
| `-display-figure` | `figure.pdf` | `gen_*.py` (+ `paper_plot_style.py`) |
| `-display-diagram` | `figure.svg` (+ `figure.pdf`) | the FigureSpec `*.json` |
| `-display-illustration` / `-gemini` | `figure.png` | `prompt.md` (final prompt + bridge job + score) + `review_log.json` |

`float.tex` references the asset only (`\includegraphics` / `\input`); numbers
typed directly into `float.tex` are a defect (data must live in `assets/`).

## Renderer procedure (append to the renderer's own workflow)

1. Resolve/scaffold the unit (above).
2. Render the asset into `0-displays/<unit>/assets/`.
3. Write the rebuild spec into `0-displays/<unit>/source/`.
4. Write/refresh `float.tex` (caption + `\label{fig|tab:<slug>}` + asset reference).
5. Write `preview.tex` if missing; compile `preview.pdf` from the PAPER ROOT
   (`pdflatex -output-directory 0-displays/<unit> 0-displays/<unit>/preview.tex`).
6. Update `README.md` (`## Status` -> `rendered`; fill Evidence Source).
7. Return the unit path; do NOT leave assets in a flat `figures/` dir.

## Notes

- Scaffold template + `float.tex`/`preview.tex`/`README.md` templates live in the
  `haipipe-paper-display` SKILL (`scaffold` verb). This contract is the renderer
  side of that same structure.
- The `4-display.tex` stage doc `\input`s each unit's `float.tex`, so a correctly
  filed unit shows up in the combined gallery automatically.
- This is the direct-renderer path; the task-rendered path
  (`/haipipe-task-for-display`) writes into the SAME unit layout.
