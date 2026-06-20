# 2-build / shared : paper folder anatomy

What a **whole paper folder** should look like. Grounded in `examples/ProjA-PhyTraitLandScape/paper/Paper-MapPhyTrait-npjDM2025` (published npj Digital Medicine 2025). Every 2-build skill creates, migrates toward, or audits against this contract.

The companion doc `3-edit/_shared/tex-file-anatomy.md` defines the anatomy of **one `.tex` file** (driver / wrapper / leaf roles, paragraph banners). This doc defines the **folder** those files live in. Read both; they never contradict.

## The canonical tree

```
<paper>/                                  e.g. Paper-MapPhyTrait-npjDM2025/
├── 0-<paper>.tex                         DRIVER: \documentclass, preamble, \section{} + \input
├── 0-<paper>.bib                         bibliography (same stem as the driver)
├── 0-Supplementary-<paper>.tex           SI DRIVER: standalone second document (optional but standard)
├── 0-pitch/                              one-minute paper story + provenance
│   ├── PAPER_PITCH.md                    current public-facing pitch
│   ├── PITCH_LOG.md                      short record of why the pitch changed
│   └── archive/                          semantic snapshots of old pitch versions
├── 0-sections/                           all body prose, split per the naming grammar below
│   ├── README.md                         one-screen map of the section files
│   ├── 00_abstract.tex                       leaf
│   ├── 01_introduction.tex                   leaf
│   ├── 02_results.tex                        wrapper (only \input lines)
│   ├── 02-00_overview.tex ... 02-07_*.tex    leaves
│   ├── 03_discussion.tex + 03-0M_*.tex       wrapper + leaves
│   ├── 04_methods.tex    + 04-0M_*.tex       wrapper + leaves
│   ├── 05_back-matter.tex                    leaf (\section*{} blocks: data/code availability, contributions, ethics)
│   └── A_*.tex  B_*.tex  C_*.tex ...         SI leaves, \input by the SI driver
├── 0-display/                            every display asset the tex includes
│   ├── DISPLAY_INDEX.md                  display contract: role, claim, source, section, status
│   ├── Figures/                          figure folders with asset + float.tex + preview.pdf
│   └── Tables/                           table folders with body + float.tex + preview.pdf
├── 0-extra/                              (optional) cover letter, IRB, reporting checklists
├── 1-compile.sh                          THE build entry point (contract below)
├── 1-feedback/                           process: reviewer/co-author feedback by date
│   └── v<MMDD>/                          e.g. v0516/, v0604/: letters, logic sidecars, rebuttals
├── 1-diff/vs-<ref>/                      (optional) diff packages, written by paper-diff-folder
├── 1-review/                             (optional) active review session pipeline (A-E, DECISIONS.md)
└── <venue>.sty / *.bst                   venue style files at top level (e.g. arxiv.sty, naturemag.bst)
```

## The `0-` / `1-` prefix semantics

The two prefixes are the folder's whole filing system:

| Prefix | Meaning | Examples |
|--------|---------|----------|
| `0-` | **the manuscript itself**: what the venue ultimately receives or what defines how it is told | `0-<paper>.tex`, `0-<paper>.bib`, `0-Supplementary-*.tex`, `0-pitch/`, `0-sections/`, `0-display/`, `0-extra/` |
| `1-` | **process artifacts**: how the manuscript gets built and revised | `1-compile.sh`, `1-feedback/`, `1-diff/`, `1-review/`, `1-config.yaml` |

Sorting puts manuscript before process. A submission package is "everything `0-` plus the compiled PDFs"; nothing under `1-` ever goes to the venue.

`0-pitch/` is the exception inside `0-`: it is not submitted as prose, but it is
part of the manuscript's source of truth. It records how this specific paper is
explained to a reader before the reader sees the LaTeX.

## `0-pitch/` rules

`0-pitch/` is the one-minute story layer for this concrete manuscript. It lives
inside the paper folder, not the project-level `narratives/`, because the same
project story can produce several papers with different venue-facing pitches.

Files:

- `PAPER_PITCH.md` — current one-minute version. A random reader should
  understand what the paper is about, why it matters, what is surprising, why to
  believe it, and what remains fragile.
- `PITCH_LOG.md` — short provenance log. It records the source and reason for
  each semantic pitch shift; it does not duplicate every old pitch in full.
- `archive/` — semantic snapshots such as `v01_seed.md`,
  `v02_discovery-shift.md`, and `v03_probe-supported.md`. Archive only when the
  story state changes, not for typo edits.

Pitch principle:

> Pitch can start as intuition, but every later shift must cite a source.

Valid sources include author judgment, literature review, `discoveries/`,
`tasks/`, `probes/`, `insights/`, reviewer feedback, or venue strategy. If the
pitch is not readable in one minute, it is too long.

## `0-sections/` naming grammar

```
NN_<slug>.tex          top-level section file (leaf or wrapper)
NN-MM_<slug>.tex       subsection leaf inside section NN
X_<slug>.tex           SI block, X in A..Z, \input by the SI driver
```

- `NN` follows the venue's section order. npj order: `00` abstract, `01` introduction, `02` results, `03` discussion, `04` methods, `05` back-matter. A conference paper would use its own order (intro, related work, method, experiments, ...); the grammar is the same.
- `MM` starts at `00` (typically an overview/intro leaf) and is **contiguous**: no gaps.
- `<slug>` is short kebab-case and matches the `\subsection{}` title.
- The filename **is** the structural address. See `3-edit/_shared/tex-file-anatomy.md` for what goes inside each file role.

**The gap rule.** When a numbered file is deleted or merged, downstream files are renamed in the same pass to close the gap (`04-06 → 04-05`, `04-07 → 04-06`), and every `\input` line is rewired in that same pass. Never leave a hole; never leave a dangling `\input`. Paragraph stable-ids and `\label` keys do not change during the rename.

## The two-document rule

Since the npj tech-check (v0604), the paper is **two standalone documents**:

| Document | Entry point | Owns |
|----------|-------------|------|
| Main manuscript | `0-<paper>.tex` | sections `00`..`05`, bibliography |
| Supplementary Information | `0-Supplementary-<paper>.tex` | SI leaves `A_*`..`Z_*`, its own S-counters |

The SI driver mirrors the main preamble, then resets counters so displays number independently:

```latex
\setcounter{table}{0}\setcounter{figure}{0}
\renewcommand{\thetable}{S\arabic{table}}
\renewcommand{\thefigure}{S\arabic{figure}}
```

Both documents `\input` from the same `0-sections/` pool; an SI leaf never appears in the main driver and vice versa. Venues that want SI inside the main PDF simply skip the second driver and `\input` the lettered leaves after `\bibliography`.

## `0-display/` rules

`0-display/` is the manuscript's display layer. Figures and tables are not just
assets; each one carries a claim, evidence source, reader takeaway, caption, and
placement.

- `DISPLAY_INDEX.md` is required. It is the one-screen contract for every
  figure/table:
  `ID | Type | Role | Claim | Evidence Source | Section | Status`.
- Two top-level homes: `Figures/` and `Tables/`. Appendix-specific variants
  (`AppendixFigure/`, `AppendixTable/`) appear when the venue wants separated
  numbering.
- Prefer one folder per major display item:
  `0-display/Figures/fig01-hero/` or
  `0-display/Tables/tab01-main-results/`.
- A figure folder may contain:
  `DISPLAY.md`, `figure.pdf`, `float.tex`, `preview.tex`, `preview.pdf`,
  `sources/`, and `versions/`.
- A table folder may contain:
  `DISPLAY.md`, `table-body.tex`, `float.tex`, `preview.tex`, `preview.pdf`,
  `data/`, and `versions/`.
- **All `\includegraphics` and table-`\input` paths are written relative to the
  paper root** (e.g. `0-display/Figures/fig01-hero/figure.pdf`), because both
  drivers and display previews compile from the root.
- The main paper should input display blocks, not copy/paste them:
  `\input{0-display/Figures/fig01-hero/float.tex}` or
  `\input{0-display/Tables/tab01-main-results/float.tex}`.
- `float.tex` owns the LaTeX float, caption, label, and asset/table-body input.
  Section prose owns the lead-in and placement decision.
- Do not bake captions into image PDFs. `figure.pdf` is the clean visual asset;
  `preview.pdf` is a standalone review artifact compiled from `preview.tex` and
  the same `float.tex`.
- Regenerating a table should usually update `table-body.tex`, not the section
  prose. Regenerating a figure should usually update `figure.pdf`, not the
  section prose.
- Figure/table **sources** (`.pptx`, `.svg`, plotting build dirs, scripts,
  source data) live next to their exports inside the display item folder;
  retired assets move to `_old/` or item-local `versions/`, they are not deleted.

## `1-compile.sh` contract

The build entry point every conforming folder ships. Behavior (see the gold copy for the implementation):

1. **Self-locating**: if invoked from a subdirectory, it searches upward for itself and re-runs from the paper root.
2. **Auto-discovery**: compiles every `0-*.tex` master (excluding generated `*-DIFF*` files), so adding the SI driver required zero script changes.
3. **Standard pipeline**: pdflatex → bibtex → pdflatex ×2 per master, nonstop mode.
4. **Cleanup is the default**: an EXIT trap removes aux files (`*.aux *.log *.bbl ...`, including under `0-sections/` and `0-display/`) on success, failure, or interrupt; `--keep` opts out, `--clean-only` does only the cleanup.
5. **Verifiable output**: prints per-master PDF size + page count; exits nonzero if any PDF failed.

## `1-feedback/` rules

- One subfolder per feedback event, named `v<MMDD>` (e.g. `v0516`, `v0604`).
- Holds the inbound letter, per-section logic/diagram sidecars (`02-05_*_logic.txt`), and the outbound rebuttal drafts.
- Provenance prose lives here (or in commit messages), **never inside the `.tex` files**.

## Quick conformance gate

Mechanical version: `2-build/haipipe-paper-build-check/scripts/check_structure.sh <paper-dir>`.

- [ ] Exactly one driver per document; each `0-*.tex` master has `\documentclass`.
- [ ] `1-compile.sh` present, executable, and compiles all masters green.
- [ ] Every `0-sections/*.tex` matches the naming grammar; `NN` and `NN-MM` sequences contiguous.
- [ ] Every section file is `\input` exactly once (no orphans, no double-inputs).
- [ ] Wrappers contain only `\input` lines; leaves contain no `\input`/`\documentclass`; drivers own `\section{}`.
- [ ] Every `\input` and `\includegraphics` target exists on disk; `\bibliography{}` resolves.
- [ ] `0-display/DISPLAY_INDEX.md` exists; every major figure/table has a claim, evidence source, section, status, and ready input path when inserted.
- [ ] No stray aux files in the tree (the EXIT trap should have cleaned them).
