# How We Do Display (figures & tables)

A guide to the `4-display` layer: how a figure or table actually gets made, where
it lives, which renderer to pick, and the lessons that shaped the workflow. The
orchestrator is `haipipe-paper-display`; the renderers are its `-display-*`
siblings. Worked reference: `examples/ProjB-PhyTrait-OpioidRx/paper/Paper-Personality-Opioid-MedJournal/0-displays/display08-conceptual-framework`.

## 1. The one rule: a display is a unit, not a loose file

Every figure/table is a **display unit** under `0-displays/displayNN-<slug>/`:

```text
0-displays/displayNN-<slug>/
├── README.md      claim / kind / caption-job / fragility / status
├── float.tex      caption + \label + \includegraphics/\input  (PAPER-ROOT-relative path)
├── preview.tex    standalone wrapper
├── preview.pdf    compiled from the paper root
├── assets/        the rendered asset (figure.pdf / figure.png / table-body.tex)
├── source/        the REBUILD SPEC (script / FigureSpec / prompt) + provenance
└── versions/      optional history
```

You never hand-edit `assets/`. You edit `source/` (the recipe) and re-render.
The full contract: `haipipe-paper-display/ref/display-unit-output-contract.md`.

## 2. The renderer family — DATA vs CONCEPT

```
                 produces from DATA (exact, auditable)   produces a CONCEPT (designed)
  ───────────────────────────────────────────────────────────────────────────────────
  -display-table     CSV -> LaTeX booktabs table         -display-diagram   JSON -> editable SVG (no icons)
  -display-figure    CSV/JSON -> matplotlib plot          -display-illustration  AI raster (icons, memorable)
                                                            └ -illustration-gemini  Gemini fallback
```

- **Has a CSV/JSON behind it?** -> `table` (typeset) or `figure` (plot). Direct,
  data-driven, reproducible.
- **It's an idea (architecture / mechanism / framework)?** -> `diagram` (precise,
  editable, deterministic, but PLAIN box-and-arrow) or `illustration` (AI, icon-rich
  and memorable, but raster + unverifiable + you cannot edit one element).

`illustration` default backend is the Codex bridge; `-gemini` is the named fallback.

## 3. How to make one (end to end)

```
1. Settle the MODEL first (upstream): what does this display claim? For a concept
   figure, decide the variables/paths at 2-claims / 3-narrative, NOT while drawing.
2. Scaffold the unit:   haipipe-paper-display scaffold displayNN-<slug>
3. Render with the right renderer -> writes into the unit (assets/ + source/).
4. float.tex: caption + \label + asset reference (paper-root-relative path).
5. Compile preview.pdf from the PAPER ROOT (so 0-displays/ paths resolve).
6. README status -> rendered. 4-display.tex \inputs each float.tex (the gallery).
```

## 4. Choosing a renderer (decision)

| You want | Use | Trade-off |
|---|---|---|
| a typeset results/coefficient table | `-display-table` | data-driven, exact |
| a data plot (line/bar/scatter/heat) | `-display-figure` | data-driven, exact |
| an editable, precise architecture/flow diagram | `-display-diagram` | deterministic + editable, but **no icons** (plain) |
| a memorable, icon-rich hero / Figure 1 | `-display-illustration` | beautiful + icons, but **AI raster**: unverifiable, not element-editable |

For a flagship Figure 1 (Nature-style), illustration is usually the right medium:
boxes-and-arrows alone are not enough. For a clinical journal, keep the same icons
but more restrained. Pick by what the figure must DO, not by habit.

## 5. AI illustration done right (the controlled-render recipe)

AI illustration fails when the brief is loose; it does not fail because "AI is
random." The fix is control, not avoidance:

1. **Settle the model upstream.** The figure REFLECTS the model; it must never
   invent it. (See the lesson below.)
2. **Write a precise brief**: exact nodes, what is a node vs an annotation, flow
   direction, and an EXPLICIT icon list (so icons are intentional, not random).
3. **Optionally structure-lock**: feed a clean skeleton image via the bridge's
   `referenceImagePaths` so the AI beautifies without reinventing structure.
4. **Iterate with strict review**: render -> read the image -> score 1-10 against
   the model AND check for garbled/duplicated text -> refine -> re-render until >= 9.
5. **Render is scratch, finalize promotes.** The bridge hard-locks output to
   `figures/ai_generated/`; `finalize --display-unit` then promotes the accepted
   image to `assets/figure.png`, preserving a hand-written `float.tex` caption.
6. **Keep the rebuild spec** (final prompt + bridge job + score) in `source/prompt.md`.

## 6. The lesson that shaped this (display08)

We first drew the agreeableness->opioid framework with TWO boxes: "agreeableness"
(exposure) and "clinical firmness" (a protective moderator). That was wrong:
"clinical firmness" is not a second variable, it is the protective READING of the
LOW end of the one agreeableness axis. The figure had reified a rhetorical phrase
from the pitch into a pseudo-construct.

Takeaways, now baked into how we work:

- **The model is decided upstream (claims/narrative), the figure only renders it.**
  If you find yourself defining structure while drawing, stop and fix the model.
- **An AI figure will happily draw a framing phrase as if it were a model node.**
  That is exactly why concept figures need a settled model + strict review.
- **v2 fix:** one spectrum axis (firm <-> accommodating), firmness demoted to a grey
  footnote annotation, vulnerability as the only real moderator, icons made explicit.
  Correct AND memorable. See `display08-conceptual-framework/source/prompt.md` for
  the v1 -> v2 diff.

## 7. Rules of thumb

- A display is a UNIT; assets are derived; edit `source/`, re-render.
- Numbers live in `assets/` (CSV-derived), never typed into `float.tex`.
- Data figures/tables must be reproducible and exact; AI rasters are concept-only,
  never a stand-in for a data display.
- Settle the model before you draw it.
- Paths in `float.tex`/`preview.tex` are paper-root-relative.
