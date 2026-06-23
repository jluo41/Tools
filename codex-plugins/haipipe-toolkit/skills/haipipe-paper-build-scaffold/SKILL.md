---
name: haipipe-paper-build-scaffold
description: "Build a new paper folder in the gold-standard layout (npjDM2025 contract): driver tex, section wrappers, leaf stubs with paragraph banners, 0-displays, SI driver, 1-compile.sh. Input is a paper plan or just a title + section list; output is a compileable skeleton with zero prose. Trigger: scaffold paper, paper skeleton, new paper folder, build paper structure, init paper dir, 搭论文骨架, /haipipe-paper-build-scaffold."
argument-hint: "[plan-path-or-title] [--out <dir>] [--venue <v>] [--no-si]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, AskUserQuestion
metadata:
  version: "1.1.0"
  last_updated: "2026-06-04"
  summary: "Plan → new conforming paper folder skeleton (structure only, zero prose)."
  changelog:
    - "1.1.0 (2026-06-05): renamed from paper-scaffold to haipipe-paper-build-scaffold (haipipe-paper-* name unification)."
    - "1.0.0 (2026-06-04): initial version, grounded in Paper-MapPhyTrait-npjDM2025."
---

Skill: haipipe-paper-build-scaffold (4-build-submit)
================================

Create a **new** paper folder that conforms to `4-build-submit/_shared/paper-folder-anatomy.md`. This skill writes structure only: drivers, wrappers, leaf stubs, directories, the compile script. It never writes a body sentence; prose belongs to `3-write-edit/haipipe-paper-edit-write`.

If a folder already exists and merely has the wrong shape, stop and route to `haipipe-paper-build-restructure` instead. Never scaffold over existing content.

Usage
-----

```
/haipipe-paper-build-scaffold PAPER_PLAN.md --out papers/Paper-Foo-npjDM2026
/haipipe-paper-build-scaffold "Mapping X from Y with Z" --out paper/ --venue npj
/haipipe-paper-build-scaffold 1-lifecycle/NARRATIVE_REPORT.md            (asks for out dir + venue)
/haipipe-paper-build-scaffold <plan> --no-si                           (skip the SI driver)
```

Inputs
------

| Input | Source | If missing |
|-------|--------|------------|
| Paper slug + title | plan doc, or the argument string | derive slug from title (kebab, `Paper-<Topic>-<Venue><Year>`); confirm with user |
| Section list (NN map + subsection slugs) | `PAPER_PLAN.md` / `PAPER_ARCHITECTURE.md` | fall back to the venue default below; confirm with user |
| Venue + style file | `--venue` or plan doc | ask; this picks section order and the `.sty`/`.bst` to copy |
| SI blocks (lettered leaves) | plan doc | default: scaffold `A_<slug>` placeholder unless `--no-si` |
| Author block | plan doc or user | leave the template's TODO placeholder; never invent authors |

Venue default section maps:

```
npj / nature-style :  00 abstract · 01 introduction · 02 results · 03 discussion · 04 methods · 05 back-matter
conference (ICLR…) :  00 abstract · 01 introduction · 02 related-work · 03 method · 04 experiments · 05 conclusion
is (MISQ/ISR)      :  00 abstract · 01 introduction · 02 theory · 03 method · 04 results · 05 discussion · 06 conclusion
```

Workflow
--------

### Step 0: Resolve inputs

Read the plan doc if given; extract title, sections, subsections, SI blocks. Anything unresolved → one `AskUserQuestion` round, not several. Confirm the target directory is empty or absent.

### Step 1: Create the tree

```
<out>/
├── 0-sections/        0-displays/displayNN-<slug>/
└── 1-rounds/
```

(`0-extra/`, `1-diff/`, `1-review/` are created later by the skills that need them; do not pre-create empty process dirs.)

### Step 2: Instantiate templates

Templates live in `templates/` next to this SKILL.md; placeholders are `{{LIKE_THIS}}`. Fill every placeholder; grep `{{` afterward to prove none leaked.

| Template | Becomes | Notes |
|----------|---------|-------|
| `driver.tex.tpl` | `0-<paper>.tex` | one `\section{} + \input` pair per section from the plan |
| `supplementary.tex.tpl` | `0-Supplementary-<paper>.tex` | skip with `--no-si`; mirrors the driver preamble |
| `wrapper.tex.tpl` | `NN_<slug>.tex` for each section **with subsections** | only `\input` lines |
| `leaf.tex.tpl` | every `NN_*.tex` without subsections, every `NN-MM_*.tex`, every `X_*.tex` | heading + one paragraph-banner placeholder per planned paragraph (or one TODO banner if the plan has no paragraph level) |
| `compile.sh.tpl` | `1-compile.sh` | copy as-is, `chmod +x` |
| `sections-README.md.tpl` | `0-sections/README.md` | file map reflecting the actual scaffolded list |

Also create an empty `0-<paper>.bib` (a comment header only) and copy the venue style file (`arxiv.sty`, `naturemag.bst`, ...) from the gold paper or the venue kit when the venue needs one.

### Step 3: Wire and verify

1. Driver `\input` list matches the files on disk, in `NN` order; wrappers `\input` their `NN-MM` leaves in order.
2. Run `../haipipe-paper-build-check/scripts/check_structure.sh <out>` → must exit 0.
3. Run `./1-compile.sh` inside the folder → every master must produce a PDF (stub pages are fine). If LaTeX is unavailable, say so explicitly; do not claim the skeleton compiles.

### Step 4: Hand off

Report what to run next: `/haipipe-paper-edit-write <plan> --out <out>` to draft prose into the stubs, section by section.

Leaf stub shape (what Step 2 writes)
------------------------------------

```latex
\subsection{Trait--Rating Correlation}

% =========================================================
% Para [trait-rating.setup] Setup -- <one-line point from the plan>
% =========================================================
% TODO(draft): /haipipe-paper-edit-write fills this paragraph.
```

Banner ids follow `3-write-edit/_shared/paragraph-indexing.md` (`<section-slug>.<para-slug>`, stable, never renumbered). Scaffolding them now means the write/edit stages inherit stable handles for free.

Return contract
---------------

```
status:    ok | blocked | failed
summary:   what was scaffolded (sections, leaves, SI yes/no, compile result)
artifacts: [<out>/ tree]
next:      /haipipe-paper-edit-write … (draft prose) or /haipipe-paper-build-check (re-audit)
```
