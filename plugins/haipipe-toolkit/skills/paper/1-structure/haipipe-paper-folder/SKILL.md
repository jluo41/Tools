---
name: haipipe-paper-structure-bootstrap
description: Scaffold a new paper folder in prospectus mode or manuscript mode. Prospectus mode creates README.md, PAPER_PROSPECTUS.md, and NARRATIVE_HANDOFF.md for an early paper repo/submodule. Manuscript mode creates the full 0-/1-prefix LaTeX layout matching proven Paper-<Name>-<Venue><Year> folders across ProjA/ProjB.
metadata:
  version: "2.0.0"
  last_updated: "2026-06-08"
  summary: "Scaffold a paper folder in prospectus mode or manuscript mode. Prospectus mode creates paper-discovery constraints; manuscript mode creates the proven 0-/1-prefix LaTeX layout."
  changelog:
    - "2.0.0 (2026-06-08): complete rewrite — layout now matches real Paper-MapPhyTrait-npjDM2025 and Paper-Personality2Opioid-MISQ2026 folders (0-sections, 0-display, 1-feedback, compile scripts, .gitignore). Dropped generic input/notes/figures/output skeleton. Added venue templates and section stubs."
    - "1.1.0 (2026-06-05): renamed from paper-bootstrap to haipipe-paper-structure-bootstrap."
    - "1.0.0 (2026-05-31): baseline metadata added."
---

# Paper Folder Bootstrap

## Overview

Scaffold a paper project directory under `examples/<Project>/paper/`. HAI-Pipe
supports two maturity modes:

| Mode | Use when | Files |
|------|----------|-------|
| `prospectus` | The topic is paper-shaped but not yet evidence-backed | `README.md`, `PAPER_PROSPECTUS.md`, `NARRATIVE_HANDOFF.md` |
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
| `0-` | Source of truth — what IS the paper and how it is told | `0-*.tex`, `0-*.bib`, `0-pitch/`, `0-sections/`, `0-display/` |
| `1-` | Process — how the paper is BUILT and REVISED | `1-compile.*`, `1-config.yaml`, `1-feedback/` |

Reference implementations:
- `examples/ProjA-PhyTraitLandScape/paper/Paper-MapPhyTrait-npjDM2025/` (npj Digital Medicine, published)
- `examples/ProjB-PhyTrait-OpioidRx/paper/Paper-Personality2Opioid-MISQ2026/` (MISQ, in progress)

Illustrations:
- `images/stage0-topic-appears-image2.png` — Stage 0 topic classification into
  project-only, paper prospectus, or paper seed.
- `images/stage1-paper-prospectus-folder-image2.png` — Stage 1 prospectus
  folder and narrative handoff before project evidence work.

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
- Starting a revision round and need `1-feedback/v<MMDD>/` structure

Do NOT use for:
- Late-stage section editing within an already-stable structure
- Conference-template conversion (use haipipe-paper-conference instead)

## Prospectus Mode Target Layout

```
Paper-<Name>/
│
│  README.md              # paper repo status, parent project link, maturity
│  PAPER_PROSPECTUS.md    # paper-shaped discovery constraint
│  NARRATIVE_HANDOFF.md   # handoff from prospectus to project narrative
```

### `PAPER_PROSPECTUS.md` contract

Required sections:

```markdown
# Paper Prospectus: <working title>

## Parent Project
Path and one-line project context.

## Prospectus Question
The paper-shaped question.

## Tentative Claim Shape
What the paper may eventually argue, phrased as a hypothesis, not a finding.

## Current Evidence Status
What exists now: task plan, narrative notes, literature, runs, probes, insights.
State clearly that this is not yet a paper seed if probes are missing.

## Discovery Constraints
What project discovery should prioritize because of this paper prospectus.

## Narrative Handoff
What the project narrative should do next, including open questions and possible
discover/probe/task/insight routes.

## Promotion Gate
Concrete conditions for promoting this prospectus to an active paper seed.
```

### `NARRATIVE_HANDOFF.md` contract

Required sections:

```markdown
# Narrative Handoff

## Source Prospectus
Path to `PAPER_PROSPECTUS.md`.

## Narrative Job
What the narrative layer should clarify or synthesize.

## Initial Story Hypothesis
The current story possibility, phrased as tentative.

## Open Narrative Questions
Questions narrative must resolve before paper seed promotion.

## Candidate Work The Narrative May Trigger
Discover, probe, task, and insight work that narrative may call for.

## Promotion Check
The conditions under which narrative can recommend promotion to paper seed.
```

Prospectus mode definition of done:

- `README.md` says this is `maturity: prospectus`
- `PAPER_PROSPECTUS.md` states the question, constraints, current evidence status,
  narrative handoff, inquiry tracks, and promotion gate
- `NARRATIVE_HANDOFF.md` gives narrative a concrete first job and at least one
  open question that can route to discover/probe/task/insight
- No `0-sections/`, no `0-display/`, no LaTeX wrappers, no compile scripts

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
│  .gitignore                        # LaTeX artifacts; preserves 0-display/**/*.pdf
│
│  # ── 0-pitch/  (one-minute story) ───────────────────────
│  0-pitch/
│    PAPER_PITCH.md                  # current one-minute public-facing story
│    PITCH_LOG.md                    # short provenance log for story shifts
│    archive/                        # semantic snapshots of older pitches
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
│  # ── 0-display/  (figures & tables) ────────────────────
│  0-display/
│    DISPLAY_INDEX.md                # figure/table story-evidence contract
│    Figures/                        # figNN folders: DISPLAY.md, figure.pdf, float.tex, preview.pdf
│    Tables/                         # tabNN folders: DISPLAY.md, table-body.tex, float.tex, preview.pdf
│    _old/                           # superseded versions (tracked in git)
│
│  # ── 0-extra/  (optional) ──────────────────────────────
│  0-extra/                          # reference papers, slides, ChatGPT logs
│
│  # ── 1-feedback/  (versioned revision rounds) ──────────
│  1-feedback/
│    v<MMDD>/                        # one folder per revision round
│      Raw-Comment.md                # raw reviewer/editor feedback
│      0-sections-v<MMDD>backup/     # snapshot of 0-sections/ before revision
│      1-diff/                       # latexdiff outputs vs prior version
│      1-review/                     # structured review workflow
│        A-review-content/           # annotated review files
│        B-rebuttal-task/            # experiment plans for rebuttal
│        C-rebuttal-writing/         # rebuttal drafts
│        D-paper-revision/           # revision checklist + guide
│        E-cover-letter/             # cover letter
│        rebuttal-report/            # compiled rebuttal letter
│      submission/                   # final submission bundle
│        cover-letter/
│        submission-figures/          # high-res individual figures
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
4. **Scaffold 0-pitch/**: one-minute `PAPER_PITCH.md`, short `PITCH_LOG.md`,
   and `archive/` for semantic pitch snapshots
5. **Scaffold 0-sections/**: section stubs per venue format + `README.md`
6. **Scaffold 0-display/**: `DISPLAY_INDEX.md`, `Figures/`, `Tables/`, `_old/`
7. **Scaffold 1-prefix process files**:
   - `1-compile.sh` and `1-compile.ps1` (auto-detect `0-*.tex`, 4-pass pdflatex)
   - `.gitignore` (LaTeX artifacts + selective PDF preservation)
   - `1-config.yaml` (optional, with figure/table path defaults)
8. **Create 1-feedback/** as empty dir (revision rounds created on demand)
9. **Report** what was created and the next step (usually: fill `0-pitch/PAPER_PITCH.md`, write the abstract, or fill author info)

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
# but keep figure / table PDFs under 0-display/
!0-display/**/*.pdf
# and keep submission-bundle PDFs for any revision round
!1-feedback/*/submission/**/*.pdf
# and keep the rebuttal-report PDF for any revision round
!1-feedback/*/rebuttal-report/**/*.pdf
# and keep the diff PDFs for any revision round
!1-feedback/*/diff/**/*.pdf
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

## Feedback Round Workflow

When the user starts a revision round (e.g. received reviews):

1. Create `1-feedback/v<MMDD>/`
2. Copy raw reviewer comments into `Raw-Comment.md`
3. Snapshot current `0-sections/` into `0-sections-v<MMDD>backup/`
4. Create review workflow subdirs: `1-review/A-review-content/` through `E-cover-letter/`
5. Hand off to `haipipe-paper-rebuttal` skill for structured rebuttal work

## Memory Rules

Write project memory only for:
- Venue and format lock (e.g. "npj DM, IRDM format, separate SI PDF")
- Dominant contribution type
- Persistent figure-role constraints
- Style file used

Do NOT write memory for transient to-dos or single-round wording preferences.

## Common Mistakes

- Using `input/notes/figures/output/` layout (that's the old generic skeleton)
- Missing the `.gitignore` or not preserving `0-display/**/*.pdf`
- Creating `1-feedback/` subdirs before a review round exists
- Putting section headers in section files (the main `.tex` owns `\section{}`)
- Using flat figure directory instead of `Figures/` + `Tables/` under `0-display/`
- Forgetting the PowerShell compile script (Windows users need it)
- Skipping `0-pitch/PAPER_PITCH.md` and letting the abstract/intro invent
  different public-facing stories

## Output Standard

When bootstrapping is complete, report:
- Paper folder path created
- Venue + format
- Main `.tex` file name
- Number of section stubs created
- Compile scripts present
- Next step (usually: fill `0-pitch/PAPER_PITCH.md`, write abstract, fill author block, or add style file)
