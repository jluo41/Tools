---
name: haipipe-paper-structure-display
description: "Plan, scaffold, build, audit, and insert paper display items: figures, tables, diagrams, and preview PDFs under 0-display/. Use for display layer, DISPLAY_INDEX.md, ready-to-input figure/table blocks, captions, labels, standalone previews, or figure/table story-evidence contracts."
argument-hint: "[plan|scaffold|build|audit|insert] [paper-dir-or-display-id] [args...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: "1.0.0"
  last_updated: "2026-06-20"
  summary: "Maintain 0-display/ as a story/evidence display layer with DISPLAY_INDEX.md, per-item DISPLAY.md, float.tex, and standalone preview PDFs."
---

Skill: haipipe-paper-structure-display
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
└── 0-display/
    ├── DISPLAY_INDEX.md
    ├── Figures/
    │   └── fig01-hero/
    │       ├── DISPLAY.md
    │       ├── figure.pdf
    │       ├── float.tex
    │       ├── preview.tex
    │       ├── preview.pdf
    │       ├── sources/
    │       └── versions/
    ├── Tables/
    │   └── tab01-main-results/
    │       ├── DISPLAY.md
    │       ├── table-body.tex
    │       ├── float.tex
    │       ├── preview.tex
    │       ├── preview.pdf
    │       ├── data/
    │       └── versions/
    └── _old/
```

Principles
----------

1. **No orphan displays.** Every figure/table must have a claim, source, section,
   and reader takeaway.
2. **Do not bake captions into image PDFs.** `figure.pdf` is the visual asset;
   `float.tex` owns caption, label, and `\includegraphics`.
3. **Make display blocks ready to input.** Section files should be able to use:
   `\input{0-display/Figures/fig01-hero/float.tex}`.
4. **Preview separately.** `preview.pdf` is a standalone review artifact built
   from the same `float.tex`. It lets humans and reviewers inspect the display
   without compiling the whole paper.
5. **Display is a contract layer.** Figure/table generation skills may create
   assets, but this skill records why each display exists and whether it still
   supports the story.

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

Create or refresh `0-display/DISPLAY_INDEX.md` from the paper state.

Inputs to read when present:

- `0-pitch/PAPER_PITCH.md`
- `NARRATIVE_REPORT.md`
- `vNN-architecture-minimap.md`
- `PAPER_PLAN.md`
- existing `0-display/`
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

Figure scaffold:

```text
0-display/Figures/figNN-slug/
  DISPLAY.md
  float.tex
  preview.tex
  sources/.gitkeep
  versions/.gitkeep
```

Table scaffold:

```text
0-display/Tables/tabNN-slug/
  DISPLAY.md
  table-body.tex
  float.tex
  preview.tex
  data/.gitkeep
  versions/.gitkeep
```

`DISPLAY.md` template:

```markdown
# Display: <Fig/Table ID> -- <short title>

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
  \includegraphics[width=0.95\textwidth]{0-display/Figures/figNN-slug/figure.pdf}
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
  \input{0-display/Tables/tabNN-slug/table-body.tex}
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
\input{0-display/Figures/figNN-slug/float.tex}
\end{document}
```

For table previews, input the table `float.tex` instead.

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

- Does every `DISPLAY_INDEX.md` row have a concrete claim and evidence source?
- Does every major display have `DISPLAY.md`?
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
| missing asset/table body | figure/table production skill |
| unsupported claim | `haipipe-paper-structure narrative` or upstream task/probe |
| wrong figure sequence | `haipipe-paper-structure architecture` or `plan` |
| hero figure does not sell story | `haipipe-paper-structure pitch` or `architecture` |

### `insert`

Insert a ready display into a section file by adding:

```latex
\input{0-display/Figures/figNN-slug/float.tex}
```

or:

```latex
\input{0-display/Tables/tabNN-slug/float.tex}
```

Rules:

- Only insert displays with status `input-ready` or better.
- Insert near the paragraph whose claim the display supports.
- Do not duplicate an existing input line.
- After insertion, update `DISPLAY_INDEX.md` status to `inserted`.

Handoff
-------

After any mode, report:

- display items created or changed
- paths to `DISPLAY_INDEX.md`, `DISPLAY.md`, `float.tex`, and `preview.pdf`
- current status for each touched item
- next command, usually one of:

```text
/haipipe-paper-structure display build <paper-dir>
/haipipe-paper-structure display audit <paper-dir>
/haipipe-paper-structure figure <paper-dir>
/haipipe-paper-structure plan <paper-dir>
```
