# display · the family map

One door, five renderers, one constitution, and the tooling beside them.
A display is one UNIT: a folder holding the approved inputs, the recipe that draws, and the winning render.

```
hai-display/            🚪 THE DOOR · say what you want, it routes by kind
                               (a caller who knows the kind may skip it)
hai-display/_parts/table/      📊 renderer · aggregated CSV/JSON → booktabs LaTeX
hai-display/_parts/figure/     📈 renderer · results → plot (line/bar/scatter/heatmap)
hai-display/_parts/diagram/    📐 renderer · FigureSpec JSON → editable SVG
hai-display/_parts/illustration/ 🎨 renderer · AI concept figure via the codex bridge
hai-display/_parts/tex/        ✒️ renderer · hand-authored TeX: TikZ, algorithm
                               blocks, display equations · the writer is a person
hai-display-method/      🕒 renderer · how the study works: timeline on one clock,
                               workflow of the dataset, regression design (YAML spec)
ref/                        📜 THE CONSTITUTION · display-unit-output-contract.md
                               + display-intake-contract.md; every renderer obeys them
                               + display-revise-loop.md; every shown display passes it
html-ppt/                   🔧 vendored runtime (MIT, upstream github) · the board's
                               slide decks link its assets AT THIS PATH · do not move
                               not a listed skill: its guide is html-ppt/PART.md, read by path
hai-display/_parts/html-to-svg/ · hai-display/_parts/icon-to-svg/ 🔧 converters
hai-display/_parts/figure-to-svg/              🔧 converter
(retired 260816)            🗃 the poster and slides renderers, their paper-side doors, and the
                               content-plan spec that only they used; no longer on disk
                               (git history). `_parts/slide/` is a newer, different renderer
```

Why `ref/` stays at the family root, not under the door: the door, its `_parts/` renderers,
`hai-display-method`, `agents/hai-display-unit-agent.md` and paper-side skills all cite
`display/ref/`, and `<Project-SPACE>` review notes cite it by that path.

Start at `hai-display/SKILL.md`. The Excalidraw drawing skills (hai-draw, -report, -section, -read,
-revise, -workflow, -job, -task, -slide, -ideation) live in `../draw/hai-draw/gallery/` since 2026-10-16.
Page DISPLAY Results, View pages, and Paper sections are callers; each supplies
its unit path and owns the resulting acceptance decision. A draft Task's unit is
`<task>/display/Display<n>-<slug>/` (JL 261016; an older Page: a DISPLAY Result's
`<page>/results/<re-run>/payload/<unit>/`). The Paper adapter may project that
source unit into generated delivery files. The View caller keeps its unit at the
View-owned path in the shared contract.

A Board Page talk is authored by the `workbench-task-draft` Slides lane from
the page and framed in its own tab; it is not a display renderer's job.

## Unit and Run boundary

The caller supplies each unit path. A draft Task's unit is `<task>/display/Display<n>-<slug>/`, beside
`draft/` and `evidence/` (an older Page: a DISPLAY Result's `<page>/results/<re-run>/payload/<unit>/`); renderer
skills do not write to the retired `outline/evidence/display/` or keep a second copy. A Paper adapter may project
approved unit files into generated delivery output, while the unit remains the source.

A parent Workflow is a list of Runs. One invocation producing one bounded unit may be one Run;
renderer Steps, tool calls, compiles, reviews, and retries stay inside it. `origin.run` names the
upstream source Run and remains provenance.

The converters (`figure-to-svg`, `html-to-svg`, and `icon-to-svg`) produce standalone files by
default and do not create or promote a display unit. If a converted asset will serve a Page, View,
or Paper display, its caller places it in a supplied unit and follows that unit's intake, candidate,
review, promotion, and acceptance rules.
