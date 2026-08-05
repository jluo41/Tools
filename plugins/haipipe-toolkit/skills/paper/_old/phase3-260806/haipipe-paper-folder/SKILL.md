---
name: haipipe-paper-folder
description: "Scaffold a paper folder's CONTENTS, quickly and minimally: README + .gitignore + 0-lifecycle/ carrying board.md and one S01 Opening page, so a new paper is runnable on day 0. Every other page is absent-until-allocated; probes are nested below their S03/S04 topic only when one is opened, and 2-src/ plus manuscript machinery is an on-request upgrade at the Display or section frontier. THE NUMBER IS THE DELETE TEST: 0-lifecycle and 2-src are working machinery, everything unnumbered is the deliverable. Reached via /haipipe-paper enter (get-or-create on a missing path), which dispatches here to fill the folder; repo creation + submodule wiring belong to enter's get-or-create branch, not this skill. Trigger: paper folder, scaffold paper, new paper folder."
metadata:
  version: "0.5.2"
  last_updated: "2026-08-05"
  summary: "Minimal Board-first paper-folder scaffold (README + .gitignore + 0-lifecycle/ with board.md and one Seed page); everything else absent-until-allocated; manuscript machinery is an on-request upgrade. History: ./CHANGELOG.md."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-paper-folder (paper folder scaffold)
====================================================

One job: **scaffold a new paper folder's contents, QUICKLY.**
Two small files + a board with one page on it, then stop.
No questionnaire beyond a one-line working title, no LaTeX, no section stubs, no venue assumptions.

Division of labor: `/haipipe-paper enter <paper-path> [--org <owner>]` (the front door; a missing path confirms then creates) handles repo creation + submodule wiring for papers inside Project-* repos (per the papers-inside recipe in `project/haipipe-project/fn/repo-project.md`), then dispatches here (`Skill("haipipe-paper-folder")`) to fill the folder.
This skill never runs gh or git submodule commands.


The layout contract (design board QA6, ruled 2026-07-26)
---------------------------------------------------------

**The NUMBER is the delete test.** A `0-` or `2-` prefix means working machinery; everything
unnumbered is what a journal receives.

```text
rm -rf 0-* 1-* 2-*     and the paper still compiles and still submits
```

Two numbered roots, and only two:

```text
0-lifecycle/   the board, and nothing but the board
2-src/         how the deliverable is BUILT, not what it is
```

A file that breaks the build when deleted has no business carrying a number. `/haipipe-paper-conform`
runs this as an actual test; scaffold to it, and a fresh folder passes on day 0.


Default Scaffold (the whole job)
---------------------------------

```
Paper-<Name>/
├── README.md               # 1-2 sentences: working title + parent project link
├── .gitignore              # LaTeX artifacts; preserves displays/**/*.pdf (contract below)
└── 0-lifecycle/            # THE BOARD, and nothing but the board
    ├── board.md            # the spine; /haipipe-board builds board.html from it
    └── S01-opening/
        └── S-Open-Seed.md      # ONE runnable page, so the paper can be worked immediately
```

That is the whole scaffold. A probe appears only inside its S03/S04 topic's `probes/<topic>/` folder; `2-src/` and everything unnumbered arrive at the manuscript upgrade.

**Board-first, and minimal.** A new paper gets a control plane and one runnable page. Every other
page is absent until its unit is allocated, so an absence is information rather than an oversight.

**One stage, one folder.** The remaining lifecycle folders are created by the stage that first
writes into them, never in advance:

```text
S01-opening/  S02-work/  S03-literature/  S04-value/  S05-display/
S06-main/  S07-appendix/  S08-present/  S09-build/  S10-round/
```

The folder name is the lifecycle stage name, and a page's family places it: `S-Main-7-results.md` is in
`S06-main/`. `haipipe-board/cli/stage.py resolve` owns the filename rule; do not reimplement it here.

**The board is CONTROL-PLANE FIRST.** Every stage folder holds S pages and its
`_archive/`. One owned exception exists: `S05-display/` also holds the display
stage's request inbox, directly compilable gallery `4-display.tex` /
`4-display.pdf`, and `_preview/`. Those artifacts belong to the Display stage
whose Board pages govern them. No other family accepts `.tex`, assets, build
products, or scratch sidecars.

**No STATUS.md.** The frontier is DERIVED from disk, by the enter console and by each page's own
`state:`. A stored frontier can only go stale, and a stale one is worse than none: it becomes a
third answer to "where is this paper" that disagrees with the other two. Do not create the file.

.gitignore contract:

```gitignore
.DS_Store
*.aux
*.log
*.out
*.pdf
!displays/**/*.pdf
!0-lifecycle/**/*.pdf
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

When the paper reaches tex-bearing work (display units, section prose), add the manuscript
machinery. Typically requested once, at the Display or section frontier. The venue shell,
`sections/`, the `.bib`, the driver `.tex` and `2-src/` arrive TOGETHER; a paper that never reaches
Display never grows a LaTeX toolchain.

```
<Name>-<Venue><Year>.tex       # the driver: venue preamble + \input per section   UNNUMBERED
<Name>-<Venue><Year>.bib       # bibliography. HUMAN-ONLY: an agent greps it, never writes it
sections/                      # GENERATED from 0-lifecycle/S06-main/ pages. One way, md to tex
appendices/                    # GENERATED from 0-lifecycle/S07-appendix/ pages
displays/                      # one folder per unit; THE ONLY home of an asset
0-lifecycle/S05-display/
  4-display.tex · 4-display.pdf  # Display-owned review gallery; inputs unit float.tex files
<venue>.cls · <venue>.bst      # the venue shell, copied, never authored
2-src/compile.sh · compile.ps1 · config.yaml · setup.sh        # NUMBERED: how it is built
```

Note what is NOT here: there is no top-level `figures/`, and no `Figure/`/`Table/` bucket. A display
is a UNIT (`displays/displayNN-<slug>/`) and its render lives inside it, in `assets/`. A second home
for the same kind of thing is the defect this layout exists to prevent.

Section format follows the pinned venue (consult the paper's `0-lifecycle/S01-opening/S-Open-Venue.md`
Structural Blueprint first; fallback: `venue/playbook-<venue>` when it is absent):

| Venue format | Sections (in order) |
|---|---|
| IRDM (npj DM) | Abstract, Introduction, Results, Discussion, Methods, Back-matter, SI |
| IMRD (most journals) | Abstract, Introduction, Methods, Results, Discussion, Back-matter, SI |
| IS (MISQ/ISR) | Abstract, Introduction, Literature Review, Theory, Methods/Data, Empirical Analysis, Discussion, Conclusion, Appendices |

Section-file rules: files hold content only (the driver owns `\section{}`); wrapper files list
subsections via `\input{}`; subsections `NN-MM_slug.tex`; appendix leaves letter-prefixed (`A_*.tex`).

Compile script contract: auto-detect the unnumbered master `*.tex` (excluding `-DIFF`), 4-pass
`pdflatex -> bibtex -> pdflatex -> pdflatex`, clean aux on exit unless `--keep`, `--clean-only`
supported, report PDF size + pages. It lives at `2-src/compile.sh` and is invoked from the paper
root, so every path inside it is root-relative.

After any upgrade, run `/haipipe-paper-conform` and report its verdict. An upgrade that leaves the
delete test failing is not done.


Not this skill's job
---------------------

```
repo + submodule wiring        -> /haipipe-paper enter (get-or-create branch)
S pages (S-Seed-…, S-Main-…)   -> each stage, when its unit is allocated
board.html                     -> /haipipe-board (never hand-write it)
rounds                         -> S-Round pages in 0-lifecycle/S10-round/, one page per round
probe entry pages              -> /haipipe-paper probe verbs, nested under the owning S03/S04 topic
display units                  -> the Display stage + the renderer family
venue knowledge                -> venue/playbook-<venue> packs
is this folder correct?        -> /haipipe-paper-conform (report-only; the machine test)
```

Common mistakes: creating family folders or section stubs at scaffold time (absent-until-allocated);
creating a `STATUS.md`; generating any tex at creation; putting the compile script at the root as
`1-compile.sh` instead of in `2-src/`; an `input/notes/figures/output/` generic skeleton; a
top-level `figures/` or `Figures/`+`Tables/` buckets instead of display-unit folders.

Retired: `scripts/init_paper_layout.py` (generated the pre-2026-07 layout: 1-pitch/2-claims/5-minimap
tex spine, venue-template stubs) lives in `_archive/`, kept for reference only.
