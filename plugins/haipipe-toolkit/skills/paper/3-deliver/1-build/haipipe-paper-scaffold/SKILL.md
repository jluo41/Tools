---
name: haipipe-paper-scaffold
description: "THE MANUSCRIPT UPGRADE: add the LaTeX toolchain to a paper that has reached the Display or section frontier. Writes the unnumbered driver tex, sections/ wrappers + leaf stubs with paragraph banners, appendices/, displays/, the venue shell, and 2-src/compile.sh. Everything it writes is UNNUMBERED except 2-src/, because the number is the delete test. Input is a paper plan or a title + section list; output is a compileable skeleton with zero prose. Does NOT create the paper folder itself: that is haipipe-paper-folder, Board-first and minimal. Trigger: scaffold paper, manuscript upgrade, paper skeleton, build paper structure, add latex to a paper, /haipipe-paper-scaffold."
argument-hint: "[plan-path-or-title] [--out <dir>] [--venue <v>] [--no-si]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, AskUserQuestion
metadata:
  version: "0.2.0"
  last_updated: "2026-07-26"
  summary: "The manuscript upgrade: plan → compileable LaTeX skeleton in the ruled layout (structure only, zero prose)."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-paper-scaffold (3-deliver)
================================

Perform the **manuscript upgrade**: give a paper that has reached the Display or section frontier
its LaTeX toolchain. This skill writes structure only: the driver, wrappers, leaf stubs, the
directories, the venue shell, the compile script. It never writes a body sentence; prose belongs to
the section stage.

**This skill does not create a paper.** `haipipe-paper-folder` does that, Board-first and minimal:
a `README`, a `.gitignore`, and `0-lifecycle/` with `board.md` and one Seed page. A paper that never
reaches Display never grows a LaTeX toolchain, and running this skill early is the mistake it is
here to prevent.

If a folder already exists and merely has the wrong shape, stop and route to
`haipipe-paper-restructure` instead. Never scaffold over existing content.

The layout contract (design board QA6, ruled 2026-07-26)
---------------------------------------------------------

**The NUMBER is the delete test.** `rm -rf 0-* 1-* 2-*` must leave a paper that still compiles and
still submits. So everything this skill writes is UNNUMBERED, with exactly one exception:

```text
UNNUMBERED, the deliverable      <paper>.tex · <paper>.bib · sections/ · appendices/
                                 displays/ · <venue>.cls · <venue>.bst
NUMBERED, working machinery      2-src/compile.sh · compile.ps1 · config.yaml · setup.sh
```

There is no top-level `figures/` and no `Figure/`/`Table/` bucket: a display is a UNIT
(`displays/displayNN-<slug>/`) and its render lives inside it, in `assets/`.

Usage
-----

```
/haipipe-paper-scaffold PAPER_PLAN.md --out papers/Paper-Foo-npjDM2026
/haipipe-paper-scaffold "Mapping X from Y with Z" --out paper/ --venue npj
/haipipe-paper-scaffold 1-lifecycle/NARRATIVE_REPORT.md            (asks for out dir + venue)
/haipipe-paper-scaffold <plan> --no-si                           (skip the SI driver)
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

Read the plan doc if given; extract title, sections, subsections, SI blocks.
Anything unresolved → one `AskUserQuestion` round, not several.
Confirm the target directory is empty or absent.

### Step 1: Create the tree

```
<paper-root>/
├── sections/          appendices/          displays/displayNN-<slug>/
└── 2-src/
```

`0-lifecycle/` already exists (this is an upgrade, not a creation) and this skill never writes into
it. Do not pre-create empty process dirs, and never create a numbered folder other than `2-src/`.

### Step 2: Instantiate templates

Templates live in `templates/` next to this SKILL.md; placeholders are `{{LIKE_THIS}}`.
Fill every placeholder; grep `{{` afterward to prove none leaked.

| Template | Becomes | Notes |
|----------|---------|-------|
| `driver.tex.tpl` | `<paper>.tex` | one `\section{} + \input` pair per section from the plan |
| `supplementary.tex.tpl` | `Supplementary-<paper>.tex` | skip with `--no-si`; mirrors the driver preamble |
| `wrapper.tex.tpl` | `NN_<slug>.tex` for each section **with subsections** | only `\input` lines |
| `leaf.tex.tpl` | every `NN_*.tex` without subsections, every `NN-MM_*.tex`, every `X_*.tex` | heading + one paragraph-banner placeholder per planned paragraph (or one TODO banner if the plan has no paragraph level) |
| `compile.sh.tpl` | `2-src/compile.sh` | copy as-is, `chmod +x`; it is invoked from the paper ROOT, so every path inside it is root-relative |
| `sections-README.md.tpl` | `sections/README.md` | file map reflecting the actual scaffolded list |

Also create an empty `<paper>.bib` (a comment header only; the .bib is HUMAN-ONLY thereafter, an agent greps it and never writes it) and copy the venue style file (`arxiv.sty`, `naturemag.bst`, ...) from the gold paper or the venue kit when the venue needs one.

### Step 3: Wire and verify

1. Driver `\input` list matches the files on disk, in `NN` order; wrappers `\input` their `NN-MM` leaves in order.
2. Run `../haipipe-paper-conform/scripts/check_structure.sh <paper-root>` → must exit 0. Its block J
   is the delete test, and an upgrade that leaves J failing is not done.
3. Run `2-src/compile.sh` from the paper root → every master must produce a PDF (stub pages are fine).
   If LaTeX is unavailable, say so explicitly; do not claim the skeleton compiles.

### Step 4: Hand off

Report what to run next: the section stage, to draft prose into the stubs one section at a time. State the conform verdict, including the delete test, in the summary.

Leaf stub shape (what Step 2 writes)
------------------------------------

```latex
\subsection{Trait--Rating Correlation}

% =========================================================
% Para [trait-rating.setup] Setup -- <one-line point from the plan>
% =========================================================
% TODO(draft): /haipipe-paper section-edit fills this paragraph.
```

Banner ids follow `2-phase/REF/paragraph-indexing.md` (`<section-slug>.<para-slug>`, stable, never renumbered).
Scaffolding them now means the write/edit stages inherit stable handles for free.

Return contract
---------------

```
status:    ok | blocked | failed
summary:   what was scaffolded (sections, leaves, SI yes/no, compile result)
artifacts: [<out>/ tree]
next:      the section stage (draft prose) or /haipipe-paper-conform (re-audit)
```
