---
name: haipipe-paper-folder
description: "Scaffold a paper folder's CONTENTS, quickly and minimally: README + STATUS.md + .gitignore + four empty container dirs (0-lifecycle, 0-displays, 1-rounds, 1-probes). Stage files are absent-until-written (each stage skill creates its own 0-lifecycle/N-stage/ on first run); manuscript machinery (master tex, 0-sections, compile scripts) is a later on-request upgrade, not part of creation. Reached via /haipipe-paper enter (get-or-create on a missing path) -> haipipe-paper-lifecycle folder; repo creation + submodule wiring belong to enter's get-or-create branch, not this skill. Trigger: paper folder, scaffold paper, new paper folder."
metadata:
  version: "4.0.1"
  last_updated: "2026-07-14"
  summary: "Minimal quick paper-folder scaffold (README + STATUS + .gitignore + empty 0-lifecycle/0-displays/1-rounds/1-probes/); stage files absent-until-written; manuscript machinery is an on-request upgrade. History: ./CHANGELOG.md."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-paper-folder (paper folder scaffold)
====================================================

One job: **scaffold a new paper folder's contents, QUICKLY.**
Three small files + four empty dirs, then stop.
No questionnaire beyond a one-line working title, no LaTeX, no section stubs, no venue assumptions.

Division of labor: `/haipipe-paper enter <paper-path> [--org <owner>]` (the front door; a missing path confirms then creates) handles repo creation + submodule wiring for papers inside Project-* repos (per the papers-inside recipe in `project/haipipe-project/fn/repo-project.md`), then dispatches here via `haipipe-paper-lifecycle folder` to fill the folder.
This skill never runs gh or git submodule commands.


Default Scaffold (the whole job)
---------------------------------

```
Paper-<Name>/
├── README.md           # 1-2 sentences: working title + parent project link
├── STATUS.md           # lifecycle state (template below)
├── .gitignore          # LaTeX artifacts; preserves 0-displays/**/*.pdf (contract below)
├── 0-lifecycle/        # EMPTY -- each stage skill creates its own N-stage/ on first run
├── 0-displays/         # EMPTY -- display units land here (owner: display stage + renderers)
├── 1-rounds/           # EMPTY -- dated work rounds (owner: haipipe-paper-round)
└── 1-probes/           # EMPTY -- the probe-file pool (README.md + flat PPNN_<topic>.md probe files, created on first probe; one cross-stage pool, one file per TOPIC)
```

Absent-until-written: `0-lifecycle/` starts empty.
`/haipipe-paper seed` creates `0-seed/`, resource creates `1-resource/`, claims creates `1-claims/`, and so on down the spine (`0-seed, 1-resource, 1-claims, 2-pitch, 3-narrative, 4-display, 5-section-edit` -- resource and claims SHARE the number 1, as `2-venue/` and `2-pitch/` already do; the number is decoration and nothing renumbers).
Early stages are markdown, so a fresh paper contains no tex and needs no compiler.

STATUS.md template (the stage strip and the enter console parse this; keep the shape):

```markdown
# Paper Status

current_layer: seed
maturity: seed
active_round: none

| Field | Value |
|---|---|
| paper | <one-line working title> |
| current_layer | seed |
| next_layer | claims |
| maturity | seed |
| active_round | none |
| created | YYYY-MM-DD |
```

Do NOT include a `| venue |` row at creation.
`/haipipe-paper-venue` ADDS it when pinning; the stage strip reads the row's absence as venue-unpinned.

.gitignore contract:

```gitignore
.DS_Store
*.aux
*.log
*.out
*.pdf
!0-displays/**/*.pdf
!1-rounds/*/submission/**/*.pdf
!1-rounds/*/rebuttal-report/**/*.pdf
!1-rounds/*/diff/**/*.pdf
*.synctex.gz
*.fdb_latexmk
*.fls
*.toc
*.bbl
*.blg
*.bcf
*.run.xml
.vscode/
_old/
.paper-console.yaml
```

Report tree + next step (`/haipipe-paper enter <path>` then `seed`), with the return-contract tail.


Manuscript Upgrade (on request; NOT part of creation)
------------------------------------------------------

When the paper reaches tex-bearing work (display units, section-edit prose), add the manuscript machinery.
Typically requested once, at the display or section-edit frontier:

```
0-<Name>-<Venue><Year>.tex     # master shell: venue preamble + \input{} per section
0-<Name>-<Venue><Year>.bib     # bibliography (human-curated; agents never add bibtex)
0-sections/                    # section stubs per venue format + README.md section map
1-compile.sh / 1-compile.ps1   # copy from a reference paper, adjust names
1-config.yaml                  # optional: figure/table paths
```

Section format follows the pinned venue (consult the paper's `0-lifecycle/2-venue/2-venue.md` Structural Blueprint first; fallback: `venue/playbook-<venue>` when 2-venue.md is absent):

| Venue format | Sections (in order) |
|---|---|
| IRDM (npj DM) | Abstract, Introduction, Results, Discussion, Methods, Back-matter, SI |
| IMRD (most journals) | Abstract, Introduction, Methods, Results, Discussion, Back-matter, SI |
| IS (MISQ/ISR) | Abstract, Introduction, Literature Review, Theory, Methods/Data, Empirical Analysis, Discussion, Conclusion, Appendices |

Section-file rules: files hold content only (the master shell owns `\section{}`); meta-files list subsections via `\input{}`; subsections `NN-MM_slug.tex`; SI sections letter-prefixed (`A_*.tex`).

Compile script contract: auto-detect all `0-*.tex` (excluding `-DIFF`), 4-pass `pdflatex -> bibtex -> pdflatex -> pdflatex`, clean aux on exit unless `--keep`, `--clean-only` supported, report PDF size + pages.
Canonical implementations to copy: `examples/ProjB-PhyTrait-OpioidRx/paper/Paper-Personality2Opioid-MISQ2026/1-compile.sh` (and `.ps1`).


Not this skill's job
---------------------

```
repo + submodule wiring        -> /haipipe-paper enter (get-or-create branch)
stage files (0-seed.md, ...)   -> each stage skill, on first run
rounds (1-rounds/vYYMMDD/)     -> haipipe-paper-round (contract: ../../../wiki/07-paper-rounds.md)
probe files (PPNN_<topic>.md)  -> /haipipe-paper probe verbs (fn/probes.md)
display units                  -> display stage + renderer family
venue knowledge                -> venue/playbook-<venue> packs
```

Common mistakes: creating stage folders or section stubs at scaffold time (absent-until-written); adding a `| venue |` row before venue pins; generating any tex at creation; `input/notes/figures/output/` generic skeleton; `Figures/`+`Tables/` buckets instead of display-unit folders.

Retired: `scripts/init_paper_layout.py` (generated the pre-2026-07 layout: 1-pitch/2-claims/5-minimap tex spine, venue-template stubs) lives in `_archive/`, kept for reference only.
