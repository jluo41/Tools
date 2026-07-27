# 2-phase/REF : paper folder anatomy

What a whole paper folder should look like. Every paper build skill creates,
migrates toward, or audits against this contract. `haipipe-paper-conform`
is its executable form: if the two ever disagree, the script is the one that
ran and this doc is the one that is wrong.

The companion doc `2-phase/REF/tex-file-anatomy.md` defines the anatomy of
one `.tex` file: driver / wrapper / leaf roles, paragraph banners, and local
editing rules. This doc defines the folder those files live in.

## The canonical tree

Ruled 2026-07-26 on the design board (`skills/diagrams/01-haipipe-paper-260725`, face QA6).

```text
<paper>/                              e.g. Paper-Personality2Opioid-MISQ2026/
│
├── 0-lifecycle/                      ✂️ THE BOARD, and nothing but the board
│   ├── board.md · board.html         the spine; /haipipe-board builds the html
│   ├── 0-seed/       S-Seed-*.md
│   ├── 1-work/       S-Work-*.md      resources · claims
│   ├── 2-venue/      S-Venue-*.md     venue (carries the `venue:` PIN) · pitch · narrative
│   ├── 3-display/    S-Display-*.md
│   ├── 4-main/       S-Main-*.md
│   ├── 5-appendix/   S-Appendix-*.md
│   ├── 6-submission/ S-Submission-*.md
│   ├── 7-round/      S-Round-*.md     one page per round
│   └── _archive/
│
├── 1-probes/                         ✂️ the near side of the wall
│   └── PPnn_<topic>/QXn_<slug>.md    topic-scoped, cross-stage, one file per question
│
├── 2-src/                            ✂️ how the deliverable is BUILT, not what it is
│   └── compile.sh · compile.ps1 · config.yaml · setup.sh
│
├── <paper>.tex                       📦 the driver: \documentclass, preamble, \input per section
├── <paper>.bib                       📦 bibliography. HUMAN-ONLY: an agent greps, never writes
├── <paper>.pdf                       📦 the compiled artifact
├── Supplementary-<paper>.tex         📦 optional second driver
├── sections/                         📦 GENERATED from 4-main pages. One way, md to tex
│   ├── README.md                     one-screen map of section files
│   └── NN_<slug>.tex · NN-MM_<slug>.tex
├── appendices/                       📦 GENERATED from 5-appendix pages; A_*.tex .. Z_*.tex
├── displays/                         📦 one folder per unit; THE ONLY home of an asset
│   └── displayNN-<slug>/
│       ├── float.tex                 📦 the \caption + \label a section \inputs
│       ├── assets/                   📦 the promoted render: figure.pdf | table-body.tex
│       ├── README.md · preview.tex · preview.pdf     ✂️ never ship
│       └── source/ · candidates/ · versions/         ✂️ never ship
└── <venue>.cls · <venue>.bst         📦 the venue shell, copied, never authored
```

There is NO top-level `figures/`, and no `Figure/`/`Table/` bucket. A display is
a UNIT and its render lives inside it. There is no `STATUS.md`: see below.

## The prefix semantics: the NUMBER is the delete test

```text
rm -rf 0-* 1-* 2-*     and the paper still compiles and still submits
```

| Prefix | Meaning | Examples |
|---|---|---|
| `0-` `1-` `2-` | **working machinery**, deletable at submission | `0-lifecycle/`, `1-probes/`, `2-src/` |
| unnumbered | **the deliverable**, what a journal receives | `<paper>.tex`, `.bib`, `.pdf`, `sections/`, `appendices/`, `displays/`, the venue shell |

Three numbered folders, and only three. A file that breaks the build when
deleted has no business carrying a number, and a number is a promise that the
thing is deletable.

This INVERTS the pre-2026-07-26 rule, under which `0-` meant "manuscript source
of truth" and `0-<paper>.tex` sat beside `0-lifecycle/`. The prefix then told a
reader nothing, which is the only job a prefix has.

`haipipe-paper-conform` runs this as an actual test: block J resolves every
`\input`, `\includegraphics` and `\bibliography` target the masters reach and
asserts none sits behind a number.

## STATUS.md is retired

There is no stored frontier. `current_layer` and `maturity` are DERIVED, from
each S page's own `state:` and from disk; the venue pin lives in
`S-Venue-0-venue.md`'s `state:` line; and the Gate Ledger, the one part that is
HISTORY and cannot be derived, lives in each S page's own `## Log`, one row on
the page whose gate it was.

## Lifecycle rules

`0-lifecycle/` is the paper's maturation spine. Early stages (seed, resource, claims, pitch, narrative) are MARKDOWN (argument documents need no compilation); display and section-edit carry tex. Venue pins between claims and pitch.

| Stage | Job | Handoff trigger |
|---|---|---|
| `0-seed` | record why the paper might exist | viable enough to ask what it NEEDS |
| `1-resource` | what must EXIST for the paper to be testable, does it exist, can it CARRY the claim (venue-FREE) | every demand is HAVE+FIT, COMMISSIONED with an owner + date, or a SCOPE CUT said out loud |
| `1-claims` | maintain support/GAP ledger (venue-FREE) | claims solid enough to pick a venue |
| `2-pitch` | cover letter / one-minute story (venue-ALIGNED) | story needs an arc |
| `3-narrative` | shape this paper's story | story needs a display map |
| `4-display` | map displays to claims | display output/source is missing or ready |
| `5-section-edit` | per-section DRAFT-PROBE-REVISE-CHECK | sections converge to submission |

The lifecycle is not linear. If a paragraph reveals an unsupported claim, loop
back to `1-claims`. If a display cannot carry the claim, loop back to
`4-display`. If coauthor discussion creates new open work, record it in
the current `S-Round` page's open items and route each item to the right lifecycle stage.

## Maturity ladder

Use maturity to describe how real the paper is; do not confuse it with the
current layer.

| Maturity | Meaning | Expected artifacts |
|---|---|---|
| `seed` | paper-shaped possibility | board.md + S-Seed-0-seed.md only |
| `scaffold` | manuscript folder exists | S pages, sections/, 2-src/compile.sh |
| `claim-ledger` | claims are explicit | `1-claims` C-slots and open needs |
| `display-map` | displays are planned | `4-display` maps claim -> display |
| `section-map` | per-section pages exist | `4-main/S-Main-*.md` outlines |
| `draft` | prose exists | main paper compiles with rough sections |
| `submission-candidate` | checks mostly pass | compile, citations, displays, claims stable |
| `submitted` | external venue state exists | submission metadata and frozen PDF |
| `revision` | external/coauthor comments active | an open `S-Round` page |
| `accepted/published` | final external state | camera-ready/final links |

## `sections/` naming grammar

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
  `2-phase/REF/tex-file-anatomy.md` for what goes inside each file role.
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

Both documents `\input` from `sections/` and `appendices/`. An SI leaf never appears in the
main driver and vice versa.

## `displays/` rules

`displays/` is the paper's display layer. Figures and tables are not just
assets; each unit carries a claim, evidence source, reader takeaway, caption,
status, and placement.

- Use one display-unit folder per figure/table family:
  `displays/display01-main-gradient/`.
- A display unit may contain one or many concrete results. For example,
  `display03-heterogeneity/` can hold a main table, appendix table, robustness
  preview, and the source scripts needed to regenerate them.
- each unit's own `README.md` is its contract; there is no paper-level display index file, because the board's `3-display/` pages are the index:
  `ID | Type | Claim | Evidence Source | Section | Status | Canonical PDF`.
- Each display unit has `README.md` with:
  `purpose`, `claim`, `source`, `inputs`, `exports`, `caption`, `placement`,
  `status`, and `open needs`.
- `float.tex` owns the LaTeX float, caption, label, and asset/table-body input.
  Section prose owns the lead-in and placement decision.
- `preview.tex` compiles one display unit to `preview.pdf`; this gives each
  display its own reviewable PDF and lets the same unit be used in
  `0-lifecycle/3-display`, `0-lifecycle/4-main`, and the main paper.
- Main/SI paper paths are written relative to the paper root, for example:
  `\input{displays/display01-main-gradient/float.tex}`.
- Do not bake captions into figure PDFs. Assets are clean visual/table exports;
  captions live in LaTeX.
- Source files live next to exports inside the display-unit folder. Retired
  assets move to unit-local `versions/`; do not delete provenance.

## `0-lifecycle/7-round/` rules (one S page per round)

`0-lifecycle/7-round/` is the paper working-memory layer. A round is any dated work burst:
agent discussion, author discussion, coauthor comments, reviewer comments,
decision pass, or application of edits.

- Each round is one `S-Round-<n>-<vYYMMDD>.md` page directly under
  `0-lifecycle/7-round/`; received letters may sit beside their owning page.
- The page's `## Discussion` stores raw discussion and incoming comments.
- Its `## Items to Finish` is the only round queue.
- Decisions and applied work are recorded in the same page's Content and
  `## Log`; there is no `latest.md` or five-file round sidecar bundle.

Rounds are process memory, not manuscript source. If a decision changes the
paper, backfill it into the right S page, `sections/`, or `displays/`.

## `2-src/compile.sh` contract

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

Mechanical version: `3-deliver/1-build/haipipe-paper-conform/scripts/check_structure.sh <paper-dir>`.

- [ ] NO `STATUS.md` exists; the frontier is derived from each S page's `state:`.
- [ ] Allocated Board families use `0-seed`, `1-work`, `2-venue`,
      `3-display`, `4-main`, `5-appendix`, `6-submission`, and `7-round`;
      absent-until-allocated families need not be pre-created.
- [ ] Exactly one driver per document; each `0-*.tex` master has `\documentclass`.
- [ ] `2-src/compile.sh` is present, executable, and compiles all masters green.
- [ ] Every `sections/*.tex` matches the naming grammar; `NN` and `NN-MM`
      sequences are contiguous.
- [ ] Every section file is `\input` exactly once, with no orphans or double inputs.
- [ ] Every `\input` and `\includegraphics` target exists on disk.
- [ ] Every display unit has a complete
      `README.md`.
- [ ] Every display unit has claim, evidence source, status, and a canonical
      preview PDF when the display is marked ready.
- [ ] `the S-Round pages themselves (no stored pointer)` exists when any active round is open.
- [ ] No stray aux files remain after compile cleanup.
