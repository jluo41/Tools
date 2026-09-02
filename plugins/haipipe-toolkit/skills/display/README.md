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
A board page's units follow `haipipe-plugin-evidence/ref/displays.md` (the
page-side rules); a paper's units follow the paper stage.
A board page's talk is not a renderer's job: it is the slide plugin's deck, authored from the page and framed in its own tab.
