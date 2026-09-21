# display · the family map

One door, five renderers, one constitution, and the tooling beside them.
A display is one UNIT: a folder holding the approved inputs, the recipe that draws, and the winning render.

```
haipipe-display/            🚪 THE DOOR · say what you want, it routes by kind
                               (a caller who knows the kind may skip it)
haipipe-display-table/      📊 renderer · aggregated CSV/JSON → booktabs LaTeX
haipipe-display-figure/     📈 renderer · results → plot (line/bar/scatter/heatmap)
haipipe-display-diagram/    📐 renderer · FigureSpec JSON → editable SVG
haipipe-display-illustration/ 🎨 renderer · AI concept figure via the codex bridge
haipipe-display-tex/        ✒️ renderer · hand-authored TeX: TikZ, algorithm
                               blocks, display equations · the writer is a person
ref/                        📜 THE CONSTITUTION · display-unit-output-contract.md
                               + display-intake-contract.md; every renderer obeys them
html-ppt/                   🔧 vendored runtime (MIT, upstream github) · the board's
                               slide decks link its assets AT THIS PATH · do not move
html-to-svg/ · icon-to-svg/ 🔧 converters
figure-to-svg/              🔧 converter
_todo/                      🗃 parked, not deleted · retired 260816: the poster and
                               slides renderers, their paper-side doors, and the
                               content-plan spec that only they used
```

Start at `haipipe-display/SKILL.md`.
Page DISPLAY Results, View pages, and Paper sections are callers; each supplies
its unit path and owns the resulting acceptance decision. A Page Result unit uses
`<page>/results/<re-run>/payload/<unit>/`. The Paper adapter may project that
source unit into generated delivery files. The View caller keeps its unit at the
View-owned path in the shared contract.

A Board Page talk is authored by the `haipipe-plugin-delivery` Slides lane from
the page and framed in its own tab; it is not a display renderer's job.

## Unit and Run boundary

The caller supplies each unit path. A Page DISPLAY Result owns
`<page>/results/<re-run>/payload/<unit>/`; renderer skills do not write to the retired
`outline/evidence/display/` or flat `display/` locations. A Paper adapter may project approved unit
files into generated delivery output, while the Page Result remains the source unit.

A parent Workflow is a list of Runs. One invocation producing one bounded unit may be one Run;
renderer Steps, tool calls, compiles, reviews, and retries stay inside it. `origin.run` names the
upstream source Run and remains provenance.

The converters (`figure-to-svg`, `html-to-svg`, and `icon-to-svg`) produce standalone files by
default and do not create or promote a display unit. If a converted asset will serve a Page, View,
or Paper display, its caller places it in a supplied unit and follows that unit's intake, candidate,
review, promotion, and acceptance rules.
