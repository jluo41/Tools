# 4-edit / shared — tex file anatomy

What **one `.tex` file** should look like in a `0-sections/`-style manuscript.
Grounded in `examples/ProjA-PhyTraitLandScape/paper/Paper-MapPhyTrait-npjDM2025/`.

Every 4-edit sub-skill assumes this layout. Read it once; the topic skills refer
back here instead of repeating it.

## The three kinds of `.tex`

A manuscript split this way has exactly three file roles. Know which one you are
editing before you touch it.

| Role | Example | Contains | Does NOT contain |
|------|---------|----------|------------------|
| **Driver** | `0-<paper>.tex` | `\documentclass`, preamble, `\title`, `\begin{document}`, `\section{}` + `\input` of sections, `\bibliography` | Body prose |
| **Wrapper** | `02_results.tex` | only `\input` of its subsections (the section heading lives in the driver) | Body prose, `\section{}` |
| **Leaf** | `02-05_trait-rating-correlation.tex` | `\subsection{}` + body paragraphs, figures/tables | `\documentclass`, preamble, any `\input` |

In this project the **driver owns the `\section{}` headings** and the wrapper is
pure `\input` (see the real `02_results.tex`: eight `\input` lines, nothing
else). **Edits almost always happen in leaf files.**

## File naming convention

```
NN[-MM]_<slug>.tex
```

- `NN` — top-level section order (`00` abstract → `05` back-matter).
- `NN-MM` — subsection within section `NN` (`02-05` = fifth Results subsection).
- `<slug>` — short kebab-case topic id; should match the `\subsection{}` title.
- `A`–`E` — appendices / supplementary blocks.

The filename **is** the section's structural address. Paragraph banners inside
the file do not repeat it.

## Anatomy of a leaf file

```latex
% optional top matter: a pointer to the side-car logic/diagram file for this section
%% Logic + proposed edits: ../1-feedback/vXXXX/02-05_..._logic.txt

\subsection{Trait--Rating Correlation}

\begin{figure}[htbp]
  \centering
  \includegraphics[width=\textwidth]{0-display/Figures/.../plot.pdf}
  \caption{...}
  \label{fig:trait_satisfaction}
\end{figure}

% =========================================================
% Para [trait-rating.setup] Setup -- why correlate traits with star ratings
% =========================================================
Having characterized the distribution of physician personality traits, we next
examined how these traits relate to the star ratings patients assign...

% =========================================================
% Para [trait-rating.method] Method -- how the correlation was computed
% =========================================================
For each physician with at least five reviews, we computed the mean star rating
... (Figure~\ref{fig:trait_satisfaction}).
```

Rules:

1. **Heading first**, then figures/paragraphs. Nothing of substance above it.
2. **One paragraph banner immediately above each paragraph** (see
   `paragraph-indexing.md`).
3. **Self-contained** — a leaf compiles only via the driver; never add a
   preamble to "test it alone."
4. **Figure/table blocks** carry a stable `\label`; do not churn it.
5. **No project-journal prose in the file** — provenance notes belong in the
   commit message or a side-car `1-feedback/` log, not the `.tex` (one-line
   bracket hints in a banner are the only exception).

## The `\input` tree (how files connect)

```
0-<paper>.tex                       driver  (\documentclass, \section{}, \input)
 ├─ \input 00_abstract              leaf
 ├─ \input 01_introduction          leaf
 ├─ \section{Results}
 │   └─ \input 02_results           wrapper
 │        ├─ \input 02-00_overview  leaf
 │        ├─ \input 02-05_...       leaf
 │        └─ ...
 ├─ \section{Discussion} → \input 03_discussion (wrapper) → 03-0X leaves
 ├─ \section{Methods}    → \input 04_methods    (wrapper) → 04-0X leaves
 └─ \input 05_back-matter           leaf
 (then \bibliography, then \section*{SI-*} appendices A–E)
```

To **add** a subsection: create the leaf, add one `\input` to the wrapper in
reading order. To **reorder**: move the `\input` line and rename the leaf's file
to keep `NN-MM` order; keep figure/`\label` keys and paragraph stable-ids.

## What "good" looks like (quick gate)

- [ ] Right file role for the edit (leaf vs wrapper vs driver).
- [ ] Leaf has its `\subsection{}`; wrapper has only `\input`s; driver owns `\section{}`.
- [ ] Every paragraph has a banner with a stable id.
- [ ] No preamble, no stray `\input` in a leaf.
- [ ] Filename slug still matches the content after the edit.
