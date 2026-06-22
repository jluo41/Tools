---
name: haipipe-paper-structure-bootstrap
description: Scaffold a new paper folder in prospectus mode or manuscript mode. Prospectus mode creates README.md and STATUS.md plus a sparse 0-lifecycle/ (0-seed, optionally 1-pitch) for an early paper repo/submodule, with no manuscript obligations. Manuscript mode creates the full 0-/1-prefix LaTeX layout matching proven Paper-<Name>-<Venue><Year> folders across ProjA/ProjB.
metadata:
  version: "2.0.0"
  last_updated: "2026-06-08"
  summary: "Scaffold a paper folder in prospectus mode or manuscript mode. Prospectus mode creates paper-discovery constraints; manuscript mode creates the proven 0-/1-prefix LaTeX layout."
  changelog:
    - "2.0.0 (2026-06-08): complete rewrite — layout now matches real Paper-MapPhyTrait-npjDM2025 and Paper-Personality2Opioid-MISQ2026 folders (0-sections, 0-displays, 1-rounds, compile scripts, .gitignore). Dropped generic input/notes/figures/output skeleton. Added venue templates and section stubs."
    - "1.1.0 (2026-06-05): renamed from paper-bootstrap to haipipe-paper-structure-bootstrap."
    - "1.0.0 (2026-05-31): baseline metadata added."
---

# Paper Folder Bootstrap

## Overview

Scaffold a paper project directory under `examples/<Project>/paper/`. HAI-Pipe
supports two maturity modes:

| Mode | Use when | Files |
|------|----------|-------|
| `prospectus` | The topic is paper-shaped but not yet evidence-backed | `README.md`, `STATUS.md`, `0-lifecycle/0-seed/0-seed.tex` |
| `manuscript` | The paper has a supported seed and is ready for pitch/plan/draft work | full `0-` / `1-` LaTeX layout |

The preferred project-backed pattern is that each paper folder is its own Git
repo, attached under the project as a submodule when a remote exists:

```text
examples/<Project>/paper/Paper-<Slug>/
```

Prospectus mode is allowed to start early. It must not create manuscript
obligations. Manuscript mode is compilable from day one and uses a **prefix
convention** proven across two published/in-progress manuscripts:

| Prefix | Purpose | Examples |
|--------|---------|---------|
| `0-` | Source of truth — what IS the paper and how it is told | `0-*.tex`, `0-*.bib`, `0-lifecycle/`, `0-sections/`, `0-displays/` |
| `1-` | Process — how the paper is BUILT and REVISED | `1-compile.*`, `1-config.yaml`, `1-rounds/` |

Reference implementations:
- `examples/ProjA-PhyTraitLandScape/paper/Paper-MapPhyTrait-npjDM2025/` (npj Digital Medicine, published)
- `examples/ProjB-PhyTrait-OpioidRx/paper/Paper-Personality2Opioid-MISQ2026/` (MISQ, in progress)

Illustrations:
- `images/stage0-topic-appears-image2.png` — Stage 0 topic classification into
  project-only, paper prospectus, or paper seed.
- `images/stage1-paper-prospectus-folder-image2.png` — Stage 1 prospectus
  folder and evidence-needs handoff before project evidence work.

Use the helper script for quick scaffolding:

```bash
python <skill-dir>/scripts/init_paper_layout.py <paper-root> \
    --name MapPhyTrait --venue npjDM2025 --format IRDM
```

Prospectus mode can be created manually or by a future helper:

```text
/haipipe-paper-structure folder <paper-root> --mode prospectus --project <project-root>
```

## When To Use

- Creating a new paper directory under `examples/<Project>/paper/`
- Starting an early paper-prospectus repo/submodule before evidence is mature
- An existing paper has scattered drafts with no clear source of truth
- Starting a work round and need `1-rounds/vYYMMDD/` structure

Do NOT use for:
- Late-stage section editing within an already-stable structure
- Conference-template conversion (use haipipe-paper-conference instead)

## Prospectus Mode Target Layout

Prospectus mode is the early state of the same lifecycle, not a separate folder
model. It fills only the seed of `0-lifecycle/` and declares maturity
`prospectus`. It creates no manuscript obligations.

```
Paper-<Name>/
│
│  README.md              # paper repo status, parent project link, maturity
│  STATUS.md              # current_layer: 0-seed, maturity: prospectus
│
│  0-lifecycle/
│    README.md            # the 0-seed -> ... -> 5-minimap spine
│    0-seed/
│      0-seed.tex         # why this paper might exist, evidence, kill criteria
│    1-pitch/             # optional at prospectus maturity
│      1-pitch.tex
```

The seed is a standalone-compilable `.tex` file. It is the prospectus contract.
There is no separate project-narrative handoff file; open needs route straight
to the evidence workers.

### `0-lifecycle/0-seed/0-seed.tex` contract

The seed should answer:

- Parent project: path and one-line context.
- Prospectus question: the paper-shaped question.
- Tentative claim shape: what the paper may argue, as a hypothesis not a finding.
- Current evidence status: task/probe/discovery/insight state; say plainly when
  this is not yet a paper seed.
- Open evidence needs: what to get next, with probe/discover/task/insight routes.
- Promotion gate: concrete conditions for promoting to an active paper seed.

Prospectus mode definition of done:

- `STATUS.md` declares `maturity: prospectus` and `current_layer: 0-seed`.
- `0-lifecycle/README.md` explains the lifecycle spine.
- `0-lifecycle/0-seed/0-seed.tex` states the question, evidence status, open
  needs, and promotion gate, with at least one need that routes to
  discover/probe/task/insight.
- No `0-sections/`, no `0-displays/`, no LaTeX wrappers, no compile scripts.

## Target Layout

```
Paper-<Name>-<Venue><Year>/
│
│  # ── 0-prefix: source of truth ─────────────────────────
│  0-<Name>-<Venue><Year>.tex        # main manuscript (modular \input{})
│  0-<Name>-<Venue><Year>.bib        # bibliography
│  0-Supplementary-<Venue><Year>.tex # SI doc (if venue requires separate PDF)
│  <venue>.sty                       # style file (arxiv.sty, misq.cls, etc.)
│
│  # ── 1-prefix: process ─────────────────────────────────
│  1-compile.sh                      # bash: auto-detect 0-*.tex, 4-pass pdflatex
│  1-compile.ps1                     # PowerShell port (toolchain check, same logic)
│  1-config.yaml                     # optional: figure/table paths, eval config
│
│  .gitignore                        # LaTeX artifacts; preserves 0-displays/**/*.pdf
│
│  # ── 0-lifecycle/  (tex-first paper maturation) ─────────
│  0-lifecycle/
│    0-seed/0-seed.tex
│    1-pitch/1-pitch.tex
│    2-claims/2-claims.tex
│    3-narrative/3-narrative.tex
│    4-figures-tables/4-figures-tables.tex
│    5-minimap/5-minimap.tex
│
│  # ── 0-sections/  (modular .tex) ───────────────────────
│  0-sections/
│    README.md                       # section map + inclusion rules
│    00_abstract.tex
│    01_introduction.tex
│    02_results.tex                  # meta-file: \input{} per subsection
│    02-00_overview.tex
│    02-01_<subsection>.tex
│    ...
│    03_discussion.tex               # meta-file or standalone
│    04_methods.tex                  # meta-file: \input{} per subsection
│    04-00_intro.tex
│    04-01_<subsection>.tex
│    ...
│    05_back-matter.tex              # data/code avail, acknowledgments, ethics
│    A_<si-section>.tex              # supplementary sections (A_, B_, C_, ...)
│
│  # ── 0-displays/  (figures & tables) ────────────────────
│  0-displays/
│    README.md                       # paper-level display index
│    display01-<slug>/               # README.md, float.tex, preview.tex, preview.pdf
│      assets/                       # exported figure/table files
│      source/                       # scripts, source data, slides, drawings
│      versions/                     # superseded versions
│
│  # ── 0-extra/  (optional) ──────────────────────────────
│  0-extra/                          # reference papers, slides, ChatGPT logs
│
│  # ── 1-rounds/  (dated work rounds) ──────────────────
│  1-rounds/
│    latest.md                       # active-round pointer
│    vYYMMDD/                        # one folder per round (e.g. v260621)
│      README.md                     # round header: source, date, purpose, status
│      discussion.md                 # raw discussion / review text / notes
│      decisions.md                  # decisions accepted as paper intent
│      todo.md                       # open needs, edits, probes, displays, citations
│      applied.md                    # backfill log: what changed where
│      # external-review rounds may also hold a rebuttal/submission subtree
│      # (Raw-Comment.md, 1-diff/, 1-review/A-E, submission/) added by
│      # haipipe-paper-rebuttal; see ../../ref/paper-rounds.md for the round contract
```

## Section Format Convention

Venue format determines the section structure. Common patterns:

| Venue format | Sections (in order) |
|-------------|---------------------|
| **IRDM** (npj Digital Medicine) | Abstract, Introduction, Results, Discussion, Methods, Back-matter, SI |
| **IMRD** (most journals) | Abstract, Introduction, Methods, Results, Discussion, Back-matter, SI |
| **IS** (MISQ/ISR) | Abstract, Introduction, Literature Review, Theory, Methods/Data, Empirical Analysis, Discussion, Conclusion, Appendices |

Rules (from Paper-MapPhyTrait):
- Section files contain ONLY content — the main `.tex` handles `\section{}` headers
- Meta-files (e.g. `02_results.tex`) list subsections via `\input{}`
- Subsections use `NN-MM_slug.tex` naming: `02-01_dataset-characteristics.tex`
- SI sections use letter prefix: `A_bigfive-prompt.tex`, `B_subfive-prompt.tex`

## Bootstrap Order

1. **Collect inputs**: paper name, venue, format (IRDM/IMRD/IS), whether SI is separate PDF.
2. **Create the root folder**: `Paper-<Name>-<Venue><Year>/`
3. **Scaffold 0-prefix source files**:
   - Main `.tex` with venue-appropriate preamble + modular `\input{}` skeleton
   - `.bib` (empty with header comment)
   - SI `.tex` if venue requires separate PDF
4. **Scaffold 0-lifecycle/**: seed, pitch, claims, narrative, figures/tables,
   and minimap stage TeX files
5. **Scaffold 0-sections/**: section stubs per venue format + `README.md`
6. **Scaffold 0-displays/**: paper display index plus display-unit folders
7. **Scaffold 1-prefix process files**:
   - `1-compile.sh` and `1-compile.ps1` (auto-detect `0-*.tex`, 4-pass pdflatex)
   - `.gitignore` (LaTeX artifacts + selective PDF preservation)
   - `1-config.yaml` (optional, with figure/table path defaults)
8. **Create 1-rounds/latest.md** as the active-round pointer
9. **Report** what was created and the next step (usually: fill
   `0-lifecycle/0-seed/0-seed.tex` and `0-lifecycle/1-pitch/1-pitch.tex`,
   write the abstract, or fill author info)

## Compile Script Contract

Both `1-compile.sh` and `1-compile.ps1` must:
- Auto-detect ALL `0-*.tex` files (excluding `-DIFF` variants)
- Run the standard 4-pass pipeline per document: `pdflatex → bibtex → pdflatex → pdflatex`
- Clean auxiliary files on exit (default) unless `--keep`/`-Keep` flag
- Support `--clean-only`/`-CleanOnly` for aux-only cleanup
- Check for `pdflatex` on PATH (PS1 version provides install hints)
- Report PDF size and page count on success

## .gitignore Contract

```gitignore
# macOS
.DS_Store

# LaTeX build artifacts
*.aux
*.log
*.out
*.pdf
# but keep figure / table PDFs under 0-displays/
!0-displays/**/*.pdf
# and keep submission-bundle PDFs for any revision round
!1-rounds/*/submission/**/*.pdf
# and keep the rebuttal-report PDF for any revision round
!1-rounds/*/rebuttal-report/**/*.pdf
# and keep the diff PDFs for any revision round
!1-rounds/*/diff/**/*.pdf
*.synctex.gz
*.fdb_latexmk
*.fls
*.toc
*.bbl
*.blg
*.bcf
*.run.xml

# Editor directories
.vscode/

# Old files
_old/
```

## Round Workflow

When the user opens a work round (discussion, coauthor/reviewer comments,
decisions, or applied edits to track):

1. Create `1-rounds/vYYMMDD/` (date-stamped, e.g. `v260621/`).
2. Add the round contract files: `README.md`, `discussion.md`, `decisions.md`,
   `todo.md`, `applied.md`. See `../../ref/paper-rounds.md` for their semantics.
3. Point `1-rounds/latest.md` at the active round.
4. For an external-review round, hand off to `haipipe-paper-rebuttal`, which adds
   the heavier rebuttal/submission subtree (`Raw-Comment.md`, `1-diff/`,
   `1-review/A-E`, `submission/`) inside the same round folder.

## Memory Rules

Write project memory only for:
- Venue and format lock (e.g. "npj DM, IRDM format, separate SI PDF")
- Dominant contribution type
- Persistent figure-role constraints
- Style file used

Do NOT write memory for transient to-dos or single-round wording preferences.

## Common Mistakes

- Using `input/notes/figures/output/` layout (that's the old generic skeleton)
- Missing the `.gitignore` or not preserving `0-displays/**/*.pdf`
- Creating `1-rounds/` subdirs before a review round exists
- Putting section headers in section files (the main `.tex` owns `\section{}`)
- Using `Figures/` + `Tables/` buckets instead of display-unit folders under `0-displays/`
- Forgetting the PowerShell compile script (Windows users need it)
- Skipping `0-lifecycle/1-pitch/1-pitch.tex` and letting the abstract/intro
  invent different public-facing stories

## Output Standard

When bootstrapping is complete, report:
- Paper folder path created
- Venue + format
- Main `.tex` file name
- Number of section stubs created
- Compile scripts present
- Next step (usually: fill `0-lifecycle/0-seed/0-seed.tex` and
  `0-lifecycle/1-pitch/1-pitch.tex`, write
  abstract, fill author block, or add style file)
