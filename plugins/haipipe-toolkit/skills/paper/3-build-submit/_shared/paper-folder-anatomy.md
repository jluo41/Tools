# 4-build-submit / shared : paper folder anatomy

What a whole paper folder should look like. Every paper build skill creates,
migrates toward, or audits against this contract.

The companion doc `2-section-edit/_shared/tex-file-anatomy.md` defines the anatomy of
one `.tex` file: driver / wrapper / leaf roles, paragraph banners, and local
editing rules. This doc defines the folder those files live in.

## The canonical tree

```text
<paper>/                                  e.g. Paper-Personality-Opioid-MedJournal/
├── STATUS.md                             state, maturity, active round, next gates
├── 0-<paper>.tex                         DRIVER: \documentclass, preamble, \section{} + \input
├── 0-<paper>.bib                         bibliography, same stem as the driver
├── 0-Supplementary-<paper>.tex           SI DRIVER, optional but standard
├── 0-lifecycle/                          tex-first paper maturation spine
│   ├── 0-seed/
│   │   └── 0-seed.tex                    why this paper might exist
│   ├── 1-pitch/
│   │   └── 1-pitch.tex                   one-minute venue-facing argument
│   ├── 2-claims/
│   │   └── 2-claims.tex                  claim ledger, support/GAP status
│   ├── 3-narrative/
│   │   └── 3-narrative.tex               paper-owned story arc
│   ├── 4-display/
│   │   └── 4-display.tex          claim -> display map
│   └── 5-minimap/
│       └── 5-minimap.tex                 paragraph jobs + display/evidence anchors
├── 0-sections/                           all body prose, split per the grammar below
│   ├── README.md                         one-screen map of section files
│   ├── 00_abstract.tex
│   ├── 01_introduction.tex
│   ├── 02_results.tex
│   ├── 02-00_overview.tex ... 02-0M_*.tex
│   ├── 03_discussion.tex + 03-0M_*.tex
│   ├── 04_methods.tex    + 04-0M_*.tex
│   ├── 05_back-matter.tex
│   └── A_*.tex  B_*.tex  C_*.tex         SI leaves, \input by the SI driver
├── 0-displays/                           figure/table display units
│   ├── README.md                         display index: role, claim, source, status
│   ├── display01-<slug>/
│   │   ├── README.md                     display contract
│   │   ├── float.tex                     LaTeX float/caption/label
│   │   ├── preview.tex                   standalone review wrapper
│   │   ├── preview.pdf                   one-display review PDF
│   │   ├── assets/                       exported figure/table files
│   │   ├── source/                       scripts, source data, slides, drawings
│   │   └── versions/                     retired exports
│   └── displayNN-<slug>/
├── 0-extra/                              optional cover letter, IRB, checklists
├── 1-rounds/                             dated work rounds
│   ├── latest.md                         active round pointer and summary
│   └── vYYMMDD/
│       ├── README.md                     round source, purpose, maturity, status
│       ├── discussion.md                 raw discussion / review / meeting notes
│       ├── decisions.md                  accepted paper intent
│       ├── todo.md                       open needs and edits
│       └── applied.md                    what changed where
├── 1-config.yaml                         paths + metric definitions
├── 1-compile.sh                          build entry point
├── 1-diff/vs-<ref>/                      optional diff packages
├── 1-review/{A-E,DECISIONS.md,HANDOFF.md}/ optional active review pipeline
└── <venue>.sty / *.bst                   venue style files at top level
```

## The `0-` / `1-` prefix semantics

| Prefix | Meaning | Examples |
|---|---|---|
| `0-` | Manuscript source of truth: what defines the paper and what the venue receives | `0-<paper>.tex`, `0-lifecycle/`, `0-sections/`, `0-displays/`, `0-extra/` |
| `1-` | Process artifacts: how the paper gets built, discussed, revised, checked | `1-rounds/`, `1-compile.sh`, `1-config.yaml`, `1-diff/`, `1-review/` |

Sorting puts manuscript before process. A submission package is "everything
needed from `0-` plus compiled PDFs"; `1-` folders explain the process and are
not submitted unless the venue explicitly asks for them.

## Lifecycle rules

`0-lifecycle/` is the paper's maturation spine. It is intentionally TeX-first
so each stage can compile to a reviewable PDF.

| Stage | Job | Handoff trigger |
|---|---|---|
| `0-seed` | record why the paper might exist | paper is viable enough to pitch |
| `1-pitch` | make the one-minute argument | claims need to be made explicit |
| `2-claims` | maintain support/GAP ledger | unsupported claim needs probe/discover/task |
| `3-narrative` | shape this paper's story | story needs display map or claim repair |
| `4-display` | map displays to claims | display output/source is missing or ready |
| `5-minimap` | map paragraphs to jobs, displays, evidence | ready for section writing/editing |

The lifecycle is not linear. If a paragraph reveals an unsupported claim, loop
back to `2-claims`. If a display cannot carry the claim, loop back to
`4-display`. If coauthor discussion creates new open work, record it in
`1-rounds/<round>/todo.md` and route each item to the right lifecycle stage.

## Maturity ladder

Use maturity to describe how real the paper is; do not confuse it with the
current layer.

| Maturity | Meaning | Expected artifacts |
|---|---|---|
| `prospectus` | paper-shaped possibility | seed/pitch |
| `scaffold` | manuscript folder exists | lifecycle files, sections, compile script |
| `claim-ledger` | claims are explicit | `2-claims` C-slots and open needs |
| `display-map` | displays are planned | `4-display` maps claim -> display |
| `section-map` | paragraph jobs are mapped | `5-minimap` maps paragraphs/displays |
| `draft` | prose exists | main paper compiles with rough sections |
| `submission-candidate` | checks mostly pass | compile, citations, displays, claims stable |
| `submitted` | external venue state exists | submission metadata and frozen PDF |
| `revision` | external/coauthor comments active | `1-rounds/<round>/todo.md` and `applied.md` |
| `accepted/published` | final external state | camera-ready/final links |

## `0-sections/` naming grammar

```text
NN_<slug>.tex          top-level section file, leaf or wrapper
NN-MM_<slug>.tex       subsection leaf inside section NN
X_<slug>.tex           SI block, X in A..Z, \input by the SI driver
```

- `NN` follows the venue's section order. Biomedical/journal order is often
  abstract, introduction, results, discussion, methods, back matter; conference
  papers may use intro, related work, method, experiments, discussion.
- `MM` starts at `00` and is contiguous: no gaps.
- The filename is the structural address. See
  `2-section-edit/_shared/tex-file-anatomy.md` for what goes inside each file role.
- When a numbered file is deleted or merged, downstream files are renamed in
  the same pass and every `\input` line is rewired in that same pass.

## The two-document rule

When a paper has Supplementary Information, the main manuscript and SI are two
standalone documents:

| Document | Entry point | Owns |
|---|---|---|
| Main manuscript | `0-<paper>.tex` | sections `00`..`05`, bibliography |
| Supplementary Information | `0-Supplementary-<paper>.tex` | SI leaves `A_*`..`Z_*`, its own S-counters |

The SI driver mirrors the main preamble, then resets counters so displays
number independently:

```latex
\setcounter{table}{0}\setcounter{figure}{0}
\renewcommand{\thetable}{S\arabic{table}}
\renewcommand{\thefigure}{S\arabic{figure}}
```

Both documents `\input` from `0-sections/`. An SI leaf never appears in the
main driver and vice versa.

## `0-displays/` rules

`0-displays/` is the paper's display layer. Figures and tables are not just
assets; each unit carries a claim, evidence source, reader takeaway, caption,
status, and placement.

- Use one display-unit folder per figure/table family:
  `0-displays/display01-main-gradient/`.
- A display unit may contain one or many concrete results. For example,
  `display03-heterogeneity/` can hold a main table, appendix table, robustness
  preview, and the source scripts needed to regenerate them.
- `0-displays/README.md` is the paper-level display index:
  `ID | Type | Claim | Evidence Source | Section | Status | Canonical PDF`.
- Each display unit has `README.md` with:
  `purpose`, `claim`, `source`, `inputs`, `exports`, `caption`, `placement`,
  `status`, and `open needs`.
- `float.tex` owns the LaTeX float, caption, label, and asset/table-body input.
  Section prose owns the lead-in and placement decision.
- `preview.tex` compiles one display unit to `preview.pdf`; this gives each
  display its own reviewable PDF and lets the same unit be used in
  `0-lifecycle/4-display`, `0-lifecycle/5-minimap`, and the main paper.
- Main/SI paper paths are written relative to the paper root, for example:
  `\input{0-displays/display01-main-gradient/float.tex}`.
- Do not bake captions into figure PDFs. Assets are clean visual/table exports;
  captions live in LaTeX.
- Source files live next to exports inside the display-unit folder. Retired
  assets move to unit-local `versions/`; do not delete provenance.

## `1-rounds/` rules

`1-rounds/` is the paper working-memory layer. A round is any dated work burst:
agent discussion, author discussion, coauthor comments, reviewer comments,
decision pass, or application of edits.

- Round folders are direct children of `1-rounds/`: `1-rounds/v260621/`.
- The round id is the branch/round name. Do not add another branch folder.
- `latest.md` points to the active round and may include a short summary.
- `discussion.md` stores raw discussion and incoming comments.
- `decisions.md` stores accepted paper intent.
- `todo.md` stores open needs and their target: lifecycle stage, probe,
  discover, task, display, insight, or paper edit.
- `applied.md` records what changed where after items are handled.

Rounds are process memory, not manuscript source. If a decision changes the
paper, backfill it into `0-lifecycle/`, `0-sections/`, `0-displays/`, or
`STATUS.md`.

## `1-compile.sh` contract

The build entry point every conforming folder ships:

1. Self-locating: if invoked from a subdirectory, it searches upward for itself
   and re-runs from the paper root.
2. Auto-discovery: compiles every `0-*.tex` master except generated diff files.
3. Standard pipeline: pdflatex -> bibtex -> pdflatex x2 per master, nonstop.
4. Cleanup is the default: remove aux files on success, failure, or interrupt;
   `--keep` opts out, `--clean-only` only cleans.
5. Verifiable output: prints per-master PDF size and page count; exits nonzero
   if any PDF failed.

## Quick conformance gate

Mechanical version: `4-build-submit/haipipe-paper-build-check/scripts/check_structure.sh <paper-dir>`.

- [ ] `STATUS.md` exists and reports current layer, maturity, and active round.
- [ ] `0-lifecycle/0-seed` through `0-lifecycle/5-minimap` exist with stage TeX.
- [ ] Exactly one driver per document; each `0-*.tex` master has `\documentclass`.
- [ ] `1-compile.sh` is present, executable, and compiles all masters green.
- [ ] Every `0-sections/*.tex` matches the naming grammar; `NN` and `NN-MM`
      sequences are contiguous.
- [ ] Every section file is `\input` exactly once, with no orphans or double inputs.
- [ ] Every `\input` and `\includegraphics` target exists on disk.
- [ ] `0-displays/README.md` exists or every display unit has a complete
      `README.md`.
- [ ] Every display unit has claim, evidence source, status, and a canonical
      preview PDF when the display is marked ready.
- [ ] `1-rounds/latest.md` exists when any active round is open.
- [ ] No stray aux files remain after compile cleanup.
