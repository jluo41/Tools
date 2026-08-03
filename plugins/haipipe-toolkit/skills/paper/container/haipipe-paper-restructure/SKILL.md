---
name: haipipe-paper-restructure
description: "Migrate an existing paper into the layout ruled 2026-07-26 (design board QA6, the delete test): un-number the deliverable, split a monolithic driver into sections/ + appendices/, rewire the \\input tree, normalize NN-MM naming, unitize loose assets into displays/unit/assets/, move the build script to 2-src/. Prose stays byte-identical; gated by prose parity + compile parity + the delete test. Also handles in-layout repairs: renumber after deletes, rehouse stray assets. Trigger: restructure paper, migrate paper layout, un-number a paper, convert 0-sections to sections, delete test failing, renumber sections, close numbering gap, /haipipe-paper-restructure."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, AskUserQuestion
metadata:
  argument_hint: "[paper-dir] [--plan-only] [--repair]"
  version: "0.2.0"
  last_updated: "2026-07-26"
  summary: "Existing paper → the ruled layout; prose byte-identical, compile verified, delete test passing."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-paper-restructure (3-deliver)
===================================

Re-house an existing paper in the layout ruled on the design board (QA6) **without changing a
single sentence**. Two modes:

- **Migrate** (default): the folder does not conform at all: a monolithic driver, a numbered
  deliverable, `0-sections/`, `0-displays/`, loose `figures/`, `1-compile.sh` at the root.
  Produce the full ruled tree.
- **Repair** (`--repair`): the folder already follows the layout but has drifted: numbering gaps
  after a delete, a leaf never `\input`, an asset outside its unit.
  Fix only the findings (usually handed over from `haipipe-paper-conform`).

Not this skill: creating a paper from nothing (`haipipe-paper-folder`, Board-first and minimal),
adding the LaTeX toolchain to a paper that never had one (`haipipe-paper-scaffold`), or any wording
change (the section stage).

The target layout, and the test that defines it
-----------------------------------------------

**The NUMBER is the delete test.** `rm -rf 0-* 1-* 2-*` must leave a paper that still compiles and
still submits. Migration is largely the work of making that true.

```text
NUMBERED, working machinery      0-lifecycle/   the board, and nothing but the board
                                 1-probes/      the near side of the wall
                                 2-src/         how the deliverable is BUILT

UNNUMBERED, the deliverable      <paper>.tex · <paper>.bib · <paper>.pdf
                                 sections/ · appendices/ · displays/
                                 <venue>.cls · <venue>.bst
```

The most common migration is therefore a RENAME, not a split: `0-<paper>.tex` loses its prefix,
`0-sections/` becomes `sections/`, `0-displays/` becomes `displays/`, `1-compile.sh` moves into
`2-src/`. Do not treat that as cosmetic: while the prefix is there, the delete test deletes the
manuscript.

There is no top-level `figures/` and no `Figure/`/`Table/` bucket. A display is a UNIT and its render
lives in `displays/displayNN-<slug>/assets/`. Loose assets are unitized during migration.

Usage
-----

```
/haipipe-paper-restructure paper/                      migrate to the ruled layout
/haipipe-paper-restructure paper/ --plan-only          propose the mapping, change nothing
/haipipe-paper-restructure paper/ --repair             fix structure-check findings only
```

The two gates (non-negotiable)
------------------------------

Every restructure run must pass both before it may report `ok`:

| Gate | Check |
|------|-------|
| **Prose parity** | Concatenate all non-comment body text before and after (strip `%`-lines, `\input` lines, whitespace); the two streams must be identical. Moving, splitting, and renaming files is allowed; rewording is not. |
| **Compile parity** | Compile before (if it compiled) and after; after must produce a PDF for every master. Compare page counts; explain any delta (a pure restructure should be ±0). |
| **The delete test** | `haipipe-paper-conform` block J must pass: no target the deliverable reaches, and no master, `.bib`, `.cls` or `.bst`, sits behind a `0-`/`1-`/`2-` prefix. This is the gate that says the migration actually happened. |

Snapshot first: refuse to run on a dirty git tree, or create a `wip-restructure` commit/stash so the migration is one reviewable diff.

Workflow (migrate mode)
-----------------------

### Phase 1: Inventory

1. Find the real source of truth: which `.tex` has `\documentclass` and is actually compiled (check build scripts, Makefile, `latexmkrc`, newest PDF).
2. Map its structure: `\section` / `\subsection` tree, where the prose physically lives, every `\input`/`\include`, every `\includegraphics` path, the `.bib`, style files.
3. Detect existing fragments worth keeping (a partial `sections/` split is remapped, not flattened back).

### Phase 2: Mapping plan (always shown to the user)

Produce a migration table and **stop for approval** (this is the whole output under `--plan-only`):

```
SOURCE (today)                          →  TARGET (the ruled layout)
0-<paper>.tex  preamble+title           →  <paper>.tex                      (driver, UN-NUMBERED)
0-<paper>.tex  §Results intro           →  sections/02-00_overview.tex      (leaf)
0-<paper>.tex  §Results/Subsec "Traits" →  sections/02-01_trait-targets.tex
0-sections/methods.tex (whole)          →  sections/04_methods.tex + 04-0M leaves (split at \subsection)
0-sections/A_prompts.tex                →  appendices/A_prompts.tex
0-displays/ (as a folder)               →  displays/                        (rename; units keep their shape)
figures/pipeline.pdf                    →  displays/displayNN-pipeline/assets/pipeline.pdf  (+ rewrite path)
0-displays/Figure/main-result.pdf       →  displays/displayNN-main-result/assets/…  (unitize the flat bucket)
0-<paper>.bib                           →  <paper>.bib                      (+ rewrite \bibliography)
1-compile.sh · 1-config.yaml            →  2-src/compile.sh · 2-src/config.yaml
0-extra/ · 1-board/ (empty or junk)     →  _archive/ or deletion, ASK; never silently drop
```

Naming decisions (`NN` order per venue, slugs from subsection titles) are made here, once, and the user approves them here, once.

### Phase 3: Execute

1. `git mv` / copy content per the table; cut at heading boundaries only, taking each heading's trailing comments and floats with it.
2. Build the driver: preamble + `\section{}` + `\input` lines (driver owns headings; strip `\section{}`/`\subsection{}` lines that became filenames or remain as the task-folder's first line, per `2-phase/REF/tex-file-anatomy.md`).
3. Build wrappers for sections with multiple leaves; pure `\input` lines.
4. Rewrite every path that moved: `\includegraphics`, table `\input`, `\bibliography`.
5. Install `2-src/compile.sh` from `../haipipe-paper-scaffold/templates/compile.sh.tpl` if no conforming build script exists; `chmod +x`. If one exists at the old root path, `git mv` it and fix its internal paths, which are root-relative.
6. Leave `0-lifecycle/` alone. It is the board; migrating it is `/haipipe-board`'s job, not this skill's, and its purity is checked separately by `conform` block D.
7. Do not create a `STATUS.md`. `STATUS.md` is RETIRED (design board QA6, 260726): the frontier is derived from disk, the venue pin lives on `S-Venue-0-venue.md`'s `state:` line, and the Gate Ledger lives in each S page's `## Log`. If one exists, migrate its gate rows onto their S pages FIRST, then remove it, and say in the report which rows moved where. Never drop a ledger row: it is history, and it is the only part of that file that cannot be re-derived.

### Phase 4: Verify

1. Prose-parity gate (script it inline: strip-and-diff; show the diff if it fails and stop).
2. Compile-parity gate via `2-src/compile.sh`, run from the paper root.
3. `../haipipe-paper-conform/scripts/check_structure.sh .` → exit 0. Quote block J's line explicitly in the report: it is the whole point of the migration.
4. Report the file-mapping table again as the change log; suggest a commit message.

Repair mode (`--repair`)
------------------------

Input is a finding list (typically `haipipe-paper-conform` output).
For each finding apply the standard remedy, then re-run both gates once at the end:

| Finding | Remedy |
|---------|--------|
| Numbering gap (`04-05` missing) | Rename downstream leaves up by one **and** rewire their `\input` lines in the same pass; never leave a gap or a dangling input. Stable-ids and `\label`s do not change. |
| Orphan leaf (never `\input`) | Ask: wire it in (where?) or retire it to `_old/`; never silently delete. |
| Wrapper contains prose | Move the prose into the correct leaf (existing or new `NN-MM`); wrapper returns to pure `\input`. |
| Display asset outside its unit | Move it to `displays/<unit>/assets/`, rewrite the referencing path. Never into a `figures/` or `Figure/` bucket: those are the shape being migrated away from. |
| A numbered file the deliverable needs | Drop the prefix, rewrite every reference in the same pass. This is a delete-test failure, the most severe finding there is. |
| Aux files lingering | `2-src/compile.sh --clean-only`. |

Return contract
---------------

```
status:    ok | blocked | failed
summary:   mode, files moved/split/renamed, both gate results (explicit pass/fail)
artifacts: [mapping table, touched paths]
next:      /haipipe-paper-conform (re-audit) or the section stage (resume prose work)
```
