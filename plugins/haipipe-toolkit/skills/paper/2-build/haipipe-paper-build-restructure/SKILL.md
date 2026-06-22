---
name: haipipe-paper-build-restructure
description: "Migrate an existing paper into the gold-standard folder layout (npjDM2025 contract): split a monolithic main.tex into 0-sections/ driver/wrapper/leaf files, rewire the \\input tree, normalize NN-MM naming, relocate display assets to 0-displays/. Prose stays byte-identical; gated by prose parity + compile parity. Also handles in-layout repairs: renumber after deletes, rehouse stray assets. Trigger: restructure paper, split main.tex, migrate paper layout, convert to 0-sections, renumber sections, close numbering gap, 重构论文目录, /haipipe-paper-build-restructure."
argument-hint: "[paper-dir] [--plan-only] [--repair]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, AskUserQuestion
metadata:
  version: "1.1.0"
  last_updated: "2026-06-04"
  summary: "Existing paper → gold layout; prose byte-identical, compile verified."
  changelog:
    - "1.1.0 (2026-06-05): renamed from paper-restructure to haipipe-paper-build-restructure (haipipe-paper-* name unification)."
    - "1.0.0 (2026-06-04): initial version."
---

Skill: haipipe-paper-build-restructure (2-build)
===================================

Re-house an existing paper in the layout defined by `2-build/_shared/paper-folder-anatomy.md` **without changing a single sentence**. Two modes:

- **Migrate** (default): the folder does not conform at all (monolithic `main.tex`, flat `sections/`, ad-hoc names). Produce the full gold tree.
- **Repair** (`--repair`): the folder already follows the layout but has drifted: numbering gaps after a delete, a leaf never `\input`, figures outside `0-displays/`. Fix only the findings (usually handed over from `haipipe-paper-build-check`).

Not this skill: building a folder from nothing (`haipipe-paper-build-scaffold`), or any wording change (`3-edit`).

Usage
-----

```
/haipipe-paper-build-restructure paper/                      migrate to gold layout
/haipipe-paper-build-restructure paper/ --plan-only          propose the mapping, change nothing
/haipipe-paper-build-restructure paper/ --repair             fix structure-check findings only
```

The two gates (non-negotiable)
------------------------------

Every restructure run must pass both before it may report `ok`:

| Gate | Check |
|------|-------|
| **Prose parity** | Concatenate all non-comment body text before and after (strip `%`-lines, `\input` lines, whitespace); the two streams must be identical. Moving, splitting, and renaming files is allowed; rewording is not. |
| **Compile parity** | Compile before (if it compiled) and after; after must produce a PDF for every master. Compare page counts; explain any delta (a pure restructure should be ±0). |

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
SOURCE (today)                          →  TARGET (gold layout)
main.tex  preamble+title                →  0-<paper>.tex                    (driver)
main.tex  §Results intro                →  0-sections/02-00_overview.tex    (leaf)
main.tex  §Results/Subsec "Traits"      →  0-sections/02-01_trait-targets.tex
sections/methods.tex (whole)            →  0-sections/04_methods.tex + 04-0M leaves (split at \subsection)
figs/pipeline.pdf                       →  0-displays/Figures/pipeline.pdf   (+ rewrite \includegraphics path)
refs.bib                                →  0-<paper>.bib                    (+ rewrite \bibliography)
compile via: (none found)               →  1-compile.sh                     (from paper-scaffold templates)
```

Naming decisions (`NN` order per venue, slugs from subsection titles) are made here, once, and the user approves them here, once.

### Phase 3: Execute

1. `git mv` / copy content per the table; cut at heading boundaries only, taking each heading's trailing comments and floats with it.
2. Build the driver: preamble + `\section{}` + `\input` lines (driver owns headings; strip `\section{}`/`\subsection{}` lines that became filenames or remain as the leaf's first line, per `3-edit/_shared/tex-file-anatomy.md`).
3. Build wrappers for sections with multiple leaves; pure `\input` lines.
4. Rewrite every path that moved: `\includegraphics`, table `\input`, `\bibliography`.
5. Install `1-compile.sh` from `../haipipe-paper-build-scaffold/templates/compile.sh.tpl` if no conforming build script exists; `chmod +x`.

### Phase 4: Verify

1. Prose-parity gate (script it inline: strip-and-diff; show the diff if it fails and stop).
2. Compile-parity gate via `./1-compile.sh`.
3. `../haipipe-paper-build-check/scripts/check_structure.sh .` → exit 0.
4. Report the file-mapping table again as the change log; suggest a commit message.

Repair mode (`--repair`)
------------------------

Input is a finding list (typically `haipipe-paper-build-check` output). For each finding apply the standard remedy, then re-run both gates once at the end:

| Finding | Remedy |
|---------|--------|
| Numbering gap (`04-05` missing) | Rename downstream leaves up by one **and** rewire their `\input` lines in the same pass; never leave a gap or a dangling input. Stable-ids and `\label`s do not change. |
| Orphan leaf (never `\input`) | Ask: wire it in (where?) or retire it to `_old/`; never silently delete. |
| Wrapper contains prose | Move the prose into the correct leaf (existing or new `NN-MM`); wrapper returns to pure `\input`. |
| Display asset outside `0-displays/` | Move it under `Figures/`/`Tables/`, rewrite the referencing path. |
| Aux files lingering | `./1-compile.sh --clean-only`. |

Return contract
---------------

```
status:    ok | blocked | failed
summary:   mode, files moved/split/renamed, both gate results (explicit pass/fail)
artifacts: [mapping table, touched paths]
next:      /haipipe-paper-build-check (re-audit) or /haipipe-paper-edit (resume prose work)
```
