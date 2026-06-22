---
name: haipipe-paper-display
description: "Plan, materialize (via task/probe), scaffold, run framework candidate rounds, build, audit, and insert paper display items: figures, tables, diagrams, and preview PDFs under 0-displays/. Displays are RENDERED by a paper-display task from evidence, never hand-authored in float.tex. Use for display-unit README files, ready-to-input figure/table blocks, captions, labels, standalone previews, or figure/table story-evidence contracts."
argument-hint: "[plan|materialize|scaffold|framework|build|audit|insert] [paper-dir-or-display-id] [args...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.3.0"
  last_updated: "2026-06-22"
  summary: "Maintain 0-displays/ as a story/evidence display layer with README.md, per-unit README.md, float.tex, and standalone preview PDFs."
---

Skill: haipipe-paper-display
======================================

Maintain the **display layer** for a concrete paper folder.

Display items are figures, tables, diagrams, and other manuscript-visible
objects that carry evidence and story. A display item is not just a file. It
has a job:

```
What claim does this display support?
Where does the evidence come from?
What should the reader learn in five seconds?
Where does it appear in the paper?
Is it ready to input into the manuscript?
```

Location:

```
<paper>/
└── 0-displays/
    ├── README.md
    ├── display01-hero/
    │   ├── README.md
    │   ├── float.tex
    │   ├── preview.tex
    │   ├── preview.pdf
    │   ├── assets/
    │   ├── source/
    │   └── versions/
    └── displayNN-<slug>/
```

Principles
----------

1. **No orphan displays.** Every figure/table must have a claim, source, section,
   and reader takeaway.
2. **Do not bake captions into image PDFs.** `figure.pdf` is the visual asset;
   `float.tex` owns caption, label, and `\includegraphics`.
3. **Make display blocks ready to input.** Section files should be able to use:
   `\input{0-displays/display01-hero/float.tex}`.
4. **Preview separately.** `preview.pdf` is a standalone review artifact built
   from the same `float.tex`. It lets humans and reviewers inspect the display
   without compiling the whole paper.
5. **Display is a contract layer.** Figure/table generation skills may create
   assets, but this skill records why each display exists and whether it still
   supports the story.
6. **A display is materialized by a task, never hand-authored.** The asset
   (`assets/figure.pdf` for a figure, `assets/table-body.tex` for a table) is
   RENDERED by a paper-display task from evidence (a probe verdict, a parser's
   `metrics.json`, a result table), and `float.tex` only references it via
   `\includegraphics` or `\input`. Numbers typed directly into `float.tex` are a
   placeholder, not a display: route them through `materialize`. A figure-bearing
   claim should be shown as a figure (forest, dose-response curve, panel), not
   only as a typed table.
7. **The stage doc is the gallery.** `0-lifecycle/4-display/4-display.tex` `\input`s each rendered `float.tex`, so the stage PDF doubles as the combined figures-and-tables view; do NOT make a separate `preview-all`. Compile from the paper ROOT so the `0-displays/` paths resolve. Per-unit `preview.pdf` remain as individual review artifacts.
8. **Two display kinds, both task-rendered.** (a) data-driven: a parser turns server logs/CSVs into `metrics.json`, then a render task turns that into `assets/figure.pdf` / `assets/table-body.tex` (robust parser: handle factor-variable rows, leading-dot numbers, SE/CIs). (b) schematic/flow (study-flow, data-provenance, CONSORT): a diagram render task draws the flow and annotates it with REAL Ns pulled from the data description; still a task output, never hand-drawn.

Relationship to ARIS
--------------------

ARIS treats figures/tables mostly as a production phase in Workflow 3:

```
paper-plan -> paper-figure -> paper-write
```

HAI-Pipe treats display as a manuscript layer that crosses story and evidence:

```
pitch -> narrative -> architecture -> plan -> display -> draft/edit -> review
```

The difference matters. A display can fail because the plot is ugly, but it can
also fail because the paper's claim, section role, or one-minute pitch changed.

Modes
-----

### `plan`

Create or refresh `0-displays/README.md` from the paper state.

Inputs to read when present:

- `0-lifecycle/1-pitch/1-pitch.tex`
- `NARRATIVE_REPORT.md`
- `vNN-architecture-minimap.md`
- `PAPER_PLAN.md`
- existing `0-displays/`
- upstream result paths referenced by the user

Output:

```markdown
# Display Index

| ID | Type | Role | Claim | Evidence Source | Section | Status |
|----|------|------|-------|-----------------|---------|--------|
| Fig 1 | hero figure | one-minute story | ... | ... | Introduction | planned |
```

Status vocabulary:

- `planned`: the paper needs this display, but evidence or rendering is not ready.
- `data-ready`: source data or evidence exists.
- `rendered`: visual asset or table body exists.
- `input-ready`: `float.tex` exists and can be `\input` by a section.
- `inserted`: a section file inputs the display.
- `reviewed`: claim, caption, label, numbers, and placement passed review.

### `scaffold`

Create a display item folder from an index row or user request.

Display-unit scaffold:

```text
0-displays/displayNN-slug/
  README.md
  float.tex
  preview.tex
  assets/.gitkeep
  source/.gitkeep
  versions/.gitkeep
```

One display unit can hold one or many concrete results: a main figure, a table
body, appendix variants, robustness previews, and the source needed to rebuild
them.

`README.md` template:

```markdown
# displayNN-slug

## Reader Takeaway
What should a reader understand in five seconds?

## Claim Supported
The exact paper claim this display supports.

## Evidence Source
- Source path:
- Producing task/probe/discovery/insight:
- Last checked:

## Placement
- Main or appendix:
- Target section:
- Called by:

## Caption Job
What the caption must explain without overclaiming.

## Fragility
What could make this display stale or misleading?

## Status
planned / data-ready / rendered / input-ready / inserted / reviewed
```

`float.tex` template for figures:

```latex
\begin{figure}[t]
  \centering
  \includegraphics[width=0.95\textwidth]{0-displays/displayNN-slug/assets/figure.pdf}
  \caption{TODO: concise caption that states the display's job without overclaiming.}
  \label{fig:slug}
\end{figure}
```

`float.tex` template for tables:

```latex
\begin{table}[t]
  \centering
  \caption{TODO: concise caption that states the table's job without overclaiming.}
  \label{tab:slug}
  \input{0-displays/displayNN-slug/assets/table-body.tex}
\end{table}
```

`preview.tex` template:

```latex
\documentclass{article}
\usepackage[margin=1in]{geometry}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{subcaption}
\usepackage{caption}
\begin{document}
\input{0-displays/displayNN-slug/float.tex}
\end{document}
```

For table previews, input the table `float.tex` instead.

### `framework`

Use this mode when the bottleneck is **framework/architecture/Figure 1 planning**
and you want candidate options before final rendering.

Inputs:
- user request (claim + target section + evidence contract)
- optional `0-displays` row ID and existing candidate text

Outputs:
- `0-displays/displayNN-<slug>/README.md` updated with a clear framework claim role
- candidate pack in:
  `0-displays/displayNN-<slug>/source/framework-candidates.md`
- a selected direction in:
  `0-displays/displayNN-<slug>/source/framework-selection.md`
- `float.tex` still points to a TODO render target (not final art)

Workflow:
1. Clarify what job this figure serves in the one-minute story and which claim it
   must defend.
2. Offer 3–5 candidate frameworks (ex: pipeline chain, hub-and-spoke, layered
   stack, audit loop, feedback cycle) with pros/cons and expected reviewer friction.
3. Record the candidates and selection criteria in `source/framework-candidates.md`.
4. After selection, hand over for the final render. **Default render target:**
   `/haipipe-paper-display-illustration` (the Codex bridge gives the most
   paper-ready CVPR-style Figure 1). Choose `/haipipe-paper-display-diagram`
   instead when you need a reproducible, editable vector. Fall back to
   `/haipipe-paper-display-illustration-gemini` if the Codex bridge is unavailable.

Reference hook:
Load `Tools/references/aris/skills/paper-framework-figure-studio-pro/SKILL.md` and
follow its candidate-generation loop when generating alternatives and revision
passes. It is useful when `figure1` requires several concept drafts before settle.

### How this mode compares with the render skills

- If the figure is **conceptual architecture/pipeline** and you are still
  unsure about the high-level topology or storytelling (multiple options to choose
  from), use `framework` first to create 3–5 candidates.
- For the final render of a settled Figure 1, default to
  `/haipipe-paper-display-illustration` (Codex AI raster, richest result).
- If the topology is already decided and you need a **reproducible, editable
  vector**, use `/haipipe-paper-display-diagram` with a FigureSpec JSON.
- If the Codex bridge is unavailable or you specifically want the Gemini backend,
  use `/haipipe-paper-display-illustration-gemini`.

### `materialize`

Turn a `planned` / `data-ready` display into a real RENDERED asset by actively
calling the evidence and render workers. This stage never hand-authors a figure
or pastes numbers into `float.tex`.

Routing (use `../ref/delivery-need.md`):

```text
claim has no confirmed verdict yet     -> /haipipe-probe plan from-need <need>
asset needs rendering from evidence    -> /haipipe-task-for-display <need>
```

`/haipipe-task-for-display` creates or extends a **paper-display task group**
folder (e.g. `tasks/Z0N_Display_<topic>/`) and a per-display **task folder** that
RENDERS the figure/table from the evidence (a probe verdict, or a parser's
`metrics.json`) into:

```text
assets/figure.pdf          (graphical display: forest, dose-response curve, panel)
assets/table-body.tex      (LaTeX-native table body)
source_data.csv            (the exact numbers behind the asset)
metrics.json               (machine-readable summary, for re-derivation)
```

The task renders; the paper then backfills the rendered asset path into the
display unit and points `float.tex` at it (`\includegraphics` / `\input`). A
display reaches status `rendered` only when its asset exists on disk as a task
output, not when numbers are typed into `float.tex`. Prefer reusing an existing
display task group (extend it with a new config) over creating a new one.

### `build`

Compile standalone preview PDFs for one display item or all display items with
`preview.tex`.

Rules:

- Compile from the paper root so paths match the main paper.
- Use `pdflatex -interaction=nonstopmode`.
- A successful build creates or refreshes `preview.pdf`.
- Do not modify the main paper while building previews.
- Do not treat preview success as proof that the display supports its claim.

### `audit`

Check display/story/evidence consistency.

Audit questions:

- Does every `0-displays/README.md` row have a concrete claim and evidence source?
- Does every major display have a unit `README.md`?
- Does `float.tex` exist for each inserted display?
- Does `preview.pdf` compile?
- Does the caption match the actual asset/table body?
- Does the display support the exact claim made in the target section?
- Are numbers, datasets, baselines, panel letters, and labels synchronized?
- Does the display belong in main text or appendix?
- Is any display orphaned: asset exists but no index row, or index row exists
  but no asset/float?

Route failures:

| Failure | Route |
|---------|-------|
| caption typo, stale label, path issue | edit display item |
| `float.tex` inlines pasted numbers (no rendered asset) | `materialize` (call `/haipipe-task-for-display`) |
| missing asset/table body | `materialize` (render via the paper-display task) |
| unsupported claim | `haipipe-paper-lifecycle narrative` or upstream task/probe |
| wrong figure sequence | `haipipe-paper-lifecycle architecture` or `plan` |
| hero figure does not sell story | `haipipe-paper-lifecycle pitch` or `architecture` |

### `insert`

Insert a ready display into a section file by adding:

```latex
\input{0-displays/displayNN-slug/float.tex}
```

Rules:

- Only insert displays with status `input-ready` or better.
- Insert near the paragraph whose claim the display supports.
- Do not duplicate an existing input line.
- After insertion, update `0-displays/README.md` status to `inserted`.

Handoff
-------

After any mode, report:

- display items created or changed
- paths to `0-displays/README.md`, unit `README.md`, `float.tex`, and `preview.pdf`
- current status for each touched item
- next command, usually one of:

```text
/haipipe-paper-lifecycle display build <paper-dir>
/haipipe-paper-lifecycle display audit <paper-dir>
/haipipe-paper-lifecycle figure <paper-dir>
/haipipe-paper-lifecycle plan <paper-dir>
```
